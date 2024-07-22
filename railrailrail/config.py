"""
Copyright 2024 Wu Tingfeng <wutingfeng@outlook.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import itertools
import json
import pathlib
import warnings
from collections import OrderedDict, defaultdict

import tomlkit

from railrailrail.dataset.conditional_interchange import ConditionalInterchange
from railrailrail.dataset.durations import Durations
from railrailrail.dataset.dwell_time import DwellTime
from railrailrail.dataset.stage import Stage
from railrailrail.dataset.station import Station
from railrailrail.dataset.walking_train_map import WalkingTrainMap


class Config:
    def __init__(self, stage: Stage):
        """Setup network `Config` based on `stage`.

        Args:
            stage (Stage): Rail network stage.
        """
        self.stage = stage
        self.stations: list[Station] = self._get_stations()
        self.station_codes_by_station_name: dict[str, set[str]] = defaultdict(set)
        for station in self.stations:
            self.station_codes_by_station_name[station.station_name].add(
                station.station_code
            )
        self.segment_adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = (
            self._generate_segment_adjacency_matrix()
        )
        self.transfer_adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = (
            self._generate_transfer_adjacency_matrix()
        )

    def _get_stations(self) -> list[Station]:
        """Generate list of operational train station codes and station names,
        sorted by station code in ascending order.

        Returns:
            list[Station]: Train stations sorted by station code in ascending order.
        """

        return sorted(
            self.stage.stations,
            key=lambda station: Station.to_station_code_components(
                station.station_code
            ),
        )

    def _generate_segment_adjacency_matrix(
        self,
    ) -> defaultdict[str, OrderedDict[str, dict]]:
        """Create an travel time / dwell time adjacency matrix for all segments between stations with different names
        on the network.

        Returns:
            defaultdict[str, OrderedDict[str, dict]]: Travel time adjacency matrix.
        """
        stations: dict[str, str] = {
            station.station_code: station.station_name for station in self.stations
        }

        station_codes_by_line_code: defaultdict[str, OrderedDict[str, None]] = (
            defaultdict(OrderedDict)
        )  # Order is important as stations are almost always connected in sequential order.
        for station_code in stations:  # Group stations by line.
            line_code, _, _ = Station.to_station_code_components(station_code)
            station_codes_by_line_code[line_code][station_code] = None

        # Uni-directionally link up all adjacent stations on same line based on the fact that most adjacent stations
        # are arranged by station code in sequential order (same line code and in ascending station number order).
        adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = defaultdict(
            OrderedDict
        )
        for line_code in station_codes_by_line_code:
            line_station_codes = sorted(
                station_codes_by_line_code[line_code],
                key=Station.to_station_code_components,
            )
            for station_code, next_station_code in zip(
                line_station_codes[:-1], line_station_codes[1:]
            ):
                if (station_code, next_station_code) == ("BP13", "BP14"):
                    continue  # Special case: No link between BP13 and BP14.
                if (station_code, next_station_code) == ("NS4", "NS13"):
                    continue  # Special case: No link between NS4 and NS13.
                adjacency_matrix[station_code][next_station_code] = {
                    "duration": Durations.segments.get(
                        f"{station_code}-{next_station_code}", dict()
                    ).get(
                        "duration", -1
                    ),  # Invalid negative value, to be manually updated by user.
                }

        # Add dwell time for each rail segment.
        terminal_station_codes: set[str] = Station.get_terminals(adjacency_matrix)
        interchange_station_codes: set[str] = {
            station.station_code
            for station in set().union(*Station.get_interchanges(self.stations))
        }
        for station_code in adjacency_matrix:
            for next_station_code in adjacency_matrix[station_code]:
                dwell_time_asc, dwell_time_desc = DwellTime.get_dwell_time(
                    terminal_station_codes,
                    interchange_station_codes,
                    station_code,
                    next_station_code,
                )
                adjacency_matrix[station_code][next_station_code].update(
                    {
                        "dwell_time_asc": dwell_time_asc,
                        "dwell_time_desc": dwell_time_desc,
                    }
                )

        # Add walking paths from LTA Walking Train Map (WTM)
        for start_station_name, end_station_name, duration in WalkingTrainMap.routes:
            for start_station_code in self.station_codes_by_station_name[
                start_station_name
            ]:
                for end_station_code in self.station_codes_by_station_name[
                    end_station_name
                ]:
                    adjacency_matrix[start_station_code][end_station_code] = {
                        "duration": duration,
                        "mode": "walk",
                        "dwell_time_asc": 0,
                        "dwell_time_desc": 0,
                    }  # No dwell time for walking routes.

        # Mark segments that need to be treated differently from
        # most other segments. Currently this only means checking if a segment is
        # adjacent to a conditional interchange.
        for (
            start,
            end,
            edge_type,
            conditional_interchange,
        ) in ConditionalInterchange.segments:
            # Skip conditional interchange segments made obsolete by new stations.
            if (start, end) == ("STC", "SW2") and "SW1" in stations:
                continue
            if (start, end) == ("STC", "SW4") and "SW2" in stations:
                continue
            if (start, end) == ("PTC", "PE5") and "PE6" in stations:
                continue
            if (start, end) == ("PTC", "PE6") and "PE7" in stations:
                continue
            if (start, end) == ("PTC", "PW5") and "PW1" in stations:
                continue

            if start in stations and end in stations:
                dwell_time_asc, dwell_time_desc = DwellTime.get_dwell_time(
                    terminal_station_codes,
                    interchange_station_codes.union(set([conditional_interchange])),
                    start,
                    end,
                )
                adjacency_matrix[start][end] = {
                    **Durations.segments[f"{start}-{end}"],
                    "edge_type": edge_type,
                    "dwell_time_asc": dwell_time_asc,
                    "dwell_time_desc": dwell_time_desc,
                }

        return adjacency_matrix

    def _generate_transfer_adjacency_matrix(
        self,
    ) -> defaultdict[str, OrderedDict[str, dict]]:
        """Create an travel time adjacency matrix for all transfers between stations with same names
        on the network.

        Returns:
            defaultdict[str, OrderedDict[str, dict]]: Travel time adjacency matrix.
        """
        interchange_station_codes_by_station_name: defaultdict[str, set[str]] = (
            defaultdict(set)
        )
        for station in self.stations:
            interchange_station_codes_by_station_name[station.station_name].add(
                station.station_code
            )
        interchanges: dict[str, set[str]] = {
            station_name: station_codes
            for (
                station_name,
                station_codes,
            ) in interchange_station_codes_by_station_name.items()
            if len(station_codes) >= 2
        }
        adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = defaultdict(
            OrderedDict
        )
        pairs = []
        for station_name, station_codes in interchanges.items():
            if station_name in Durations.interchange_transfers:
                for start, end in itertools.combinations(station_codes, 2):
                    # As a simplification, treat transfer time in both directions as equal.
                    # TODO: Update in the future when more direction-specific transfer time is available.
                    pairs.append((start, end, station_name))
                    pairs.append((end, start, station_name))
            else:
                warnings.warn(
                    f"No transfer durations available for station {station_name}."
                )
        pairs.sort(
            key=lambda station_codes: (
                Station.to_station_code_components(station_codes[0]),
                Station.to_station_code_components(station_codes[1]),
            )
        )
        for start, end, station_name in pairs:
            duration = Durations.interchange_transfers[station_name]
            adjacency_matrix[start][end] = {"duration": duration}

        is_ewl_open: bool = (
            Station("EW12", "Bugis") in self.stations
        )  # Special case: Check if EWL is open.
        if not is_ewl_open:
            for start, end in (
                ("EW13", "NS25"),
                ("NS25", "EW13"),
                ("EW14", "NS26"),
                ("NS26", "EW14"),
            ):
                if adjacency_matrix.get(start, dict()).get(end, dict()):
                    adjacency_matrix[start][end] = {
                        "duration": 0
                    }  # Zero transfer time before EWL opening.

        return adjacency_matrix

    @classmethod
    def __get_updated_network_adjacency_matrix(
        cls,
        network_adjacency_matrix: tomlkit.items.Table,
        adjacency_matrix: defaultdict[str, OrderedDict[str, dict]],
    ) -> tomlkit.items.Table:
        # Mark modified edges with comment
        for station_pair, edge_details in network_adjacency_matrix.items():
            station_pair_ = station_pair.split("-", 1)
            if (
                station_pair_[0] in adjacency_matrix
                and station_pair_[1] in adjacency_matrix[station_pair_[0]]
            ):
                new_edge_details = adjacency_matrix[station_pair_[0]][station_pair_[1]]
                if edge_details != new_edge_details:  # Shallow dict comparison
                    existing_comment = network_adjacency_matrix[
                        station_pair
                    ].trivia.comment
                    network_adjacency_matrix[station_pair].comment(
                        f"NEW -> {json.dumps(new_edge_details)}{' | %s' % existing_comment if existing_comment else ''}"
                    )

        adjacency_matrix_edges = {
            f"{a}-{b}" for a in adjacency_matrix for b in adjacency_matrix[a]
        }

        # Mark defunct adjacency matrix entries with comment
        for defunct_edge in set(network_adjacency_matrix).difference(
            adjacency_matrix_edges
        ):
            existing_comment = network_adjacency_matrix[defunct_edge].trivia.comment
            network_adjacency_matrix[defunct_edge].comment(
                f"DEFUNCT{' | %s' % existing_comment if existing_comment else ''}"
            )

        # Add new adjacency matrix entries
        for new_edge in set(adjacency_matrix_edges).difference(
            network_adjacency_matrix
        ):
            vertices = new_edge.split("-", 1)
            start, end = vertices[0], vertices[1]
            it = tomlkit.inline_table()
            it.update(adjacency_matrix[start][end])
            network_adjacency_matrix[new_edge] = it
            network_adjacency_matrix[new_edge].comment("NEW")

        # Sort adjacency matrix entries
        updated_network_adjacency_matrix = tomlkit.table()
        for edge in sorted(
            network_adjacency_matrix,
            key=lambda pair: tuple(
                map(Station.to_station_code_components, pair.split("-", 1))
            ),
        ):
            updated_network_adjacency_matrix[edge] = network_adjacency_matrix[edge]
        return updated_network_adjacency_matrix

    def update_network(self, network: tomlkit.TOMLDocument) -> None:
        """Update contents of `network` configuration in-place.

        - Newly added entries are marked as NEW.
        - Entries to be modified will have their new content added as an inline-comment.
        - Entries made defunct will be marked as DEFUNCT with an inline-comment.
        - Existing comments are preserved.

        Args:
            network (tomlkit.TOMLDocument): Network configuration to be updated.
        """

        network["schema"] = network.get("schema", 1)
        network["default_transfer_time"] = network.get("default_transfer_time", 420)
        network["default_dwell_time"] = network.get("default_dwell_time", 30)

        ### stations ###

        stations_ = {
            station.station_code: station.station_name for station in self.stations
        }
        network_stations = (
            network["stations"] if "stations" in network else tomlkit.table()
        )

        # Mark modified stations with comment
        for station_code, station_name in network_stations.items():
            if station_code in stations_ and station_name != stations_[station_code]:
                existing_comment = network_stations[station_code].trivia.comment
                network_stations[station_code].comment(
                    f"NEW -> {stations_[station_code]}{' | %s' % existing_comment if existing_comment else ''}"
                )

        # Mark defunct stations with comment
        for defunct_station_code in set(network_stations).difference(stations_):
            existing_comment = network_stations[defunct_station_code].trivia.comment
            network_stations[defunct_station_code].comment(
                f"DEFUNCT{' | %s' % existing_comment if existing_comment else ''}"
            )

        # Add new stations
        for new_station_code in set(stations_).difference(network_stations):
            network_stations[new_station_code] = stations_[new_station_code]
            network_stations[new_station_code].comment("NEW")

        # Sort stations
        updated_stations = tomlkit.table()
        for station_code in sorted(
            network_stations, key=Station.to_station_code_components
        ):
            updated_stations[station_code] = network_stations[station_code]
        network["stations"] = updated_stations

        network["segments"] = self.__get_updated_network_adjacency_matrix(
            network["segments"] if "segments" in network else tomlkit.table(),
            self.segment_adjacency_matrix,
        )  # segments

        network["transfers"] = self.__get_updated_network_adjacency_matrix(
            network["transfers"] if "transfers" in network else tomlkit.table(),
            self.transfer_adjacency_matrix,
        )  # transfers

    def update_network_config_file(self, path: pathlib.Path) -> None:
        """Overwrite contents of network configuration file at `path` with updated
        network data.

        Args:
            path (pathlib.Path): Path to network configuration file.
        """
        try:
            with open(path, "rb") as f:
                network: tomlkit.TOMLDocument = tomlkit.load(f)
        except OSError:
            network: tomlkit.TOMLDocument = tomlkit.TOMLDocument()
        self.update_network(network)
        with open(path, "w") as f:
            tomlkit.dump(network, f)
