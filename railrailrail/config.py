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

from railrailrail.dataset import (
    ConditionalInterchange,
    Durations,
    Stage,
    WalkingTrainMap,
)
from railrailrail.utils import StationUtils


class Config:
    def __init__(self, stage: Stage):
        """Setup network `Config` based on `stage`.

        Args:
            stage (Stage): Rail network stage.
        """
        self.stage = stage
        self.stations: list[tuple[str, str]] = self._get_stations()
        self.station_codes_by_station_name: dict[str, set[str]] = defaultdict(set)
        for station_code, station_name in self.stations:
            self.station_codes_by_station_name[station_name].add(station_code)
        self.segment_adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = (
            self._generate_segment_adjacency_matrix()
        )
        self.transfer_adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = (
            self._generate_transfer_adjacency_matrix()
        )

    def _get_stations(self) -> list[tuple[str, str]]:
        """Generate list of operational train station codes and station names,
        sorted by station code in ascending order.

        Returns:
            list[tuple[str, str]]: Train stations sorted by station code in ascending order.
            For example, ("CC1", "Dhoby Ghaut"), ("NE6", "Dhoby Ghaut"), ("NS24", "Dhoby Ghaut").
        """

        return sorted(
            self.stage.stations,
            key=lambda station: StationUtils.to_station_code_components(station[0]),
        )

    def _generate_segment_adjacency_matrix(
        self,
    ) -> defaultdict[str, OrderedDict[str, dict]]:
        """Create an travel time adjacency matrix for all segments between stations with different names
        on the network.

        Returns:
            defaultdict[str, OrderedDict[str, dict]]: Travel time adjacency matrix.
        """
        station_codes: list[str] = [station_code for station_code, _ in self.stations]

        station_codes_by_line_code: defaultdict[str, OrderedDict[str, None]] = (
            defaultdict(OrderedDict)
        )  # Order is important as stations are almost always connected in sequential order.
        for station_code in station_codes:  # Group stations by line.
            line_code, _, _ = StationUtils.to_station_code_components(station_code)
            station_codes_by_line_code[line_code][station_code] = None

        # Uni-directionally link up all adjacent stations on same line based on the fact that most adjacent stations
        # are arranged by station code in sequential order (same line code and in ascending station number order).
        adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = defaultdict(
            OrderedDict
        )
        for line_code in station_codes_by_line_code:
            line_station_codes = sorted(
                station_codes_by_line_code[line_code],
                key=StationUtils.to_station_code_components,
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
                    ).get("duration", 0)
                }

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
                    }

        # Mark segments that need to be treated differently from
        # most other segments. Currently this only means checking if a segment is
        # adjacent to a conditional interchange.
        for start, end, edge_type in ConditionalInterchange.segments:
            # Skip conditional interchange segments made obsolete by new stations.
            if (start, end) == ("STC", "SW2") and "SW1" in station_codes:
                continue
            if (start, end) == ("STC", "SW4") and "SW2" in station_codes:
                continue
            if (start, end) == ("PTC", "PE5") and "PE6" in station_codes:
                continue
            if (start, end) == ("PTC", "PE6") and "PE7" in station_codes:
                continue
            if (start, end) == ("PTC", "PW5") and "PW1" in station_codes:
                continue

            if start in station_codes and end in station_codes:
                adjacency_matrix[start][end] = {
                    **Durations.segments[f"{start}-{end}"],
                    "edge_type": edge_type,
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
        for station_code, station_name in self.stations:
            interchange_station_codes_by_station_name[station_name].add(station_code)
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
                StationUtils.to_station_code_components(station_codes[0]),
                StationUtils.to_station_code_components(station_codes[1]),
            )
        )
        for start, end, station_name in pairs:
            duration = Durations.interchange_transfers[station_name]
            adjacency_matrix[start][end] = {"duration": duration}
        return adjacency_matrix

    @classmethod
    def __get_updated_network_adjacency_matrix(
        cls,
        network_adjacency_matrix: tomlkit.items.Table,
        adjacency_matrix: defaultdict[str, OrderedDict[str, dict]],
    ) -> tomlkit.items.Table:
        # Mark modified segments with comment
        for station_pair, segment_details in network_adjacency_matrix.items():
            station_pair_ = station_pair.split("-", 1)
            if (
                station_pair_[0] in adjacency_matrix
                and station_pair_[1] in adjacency_matrix[station_pair_[0]]
            ):
                new_segment_details = adjacency_matrix[station_pair_[0]][
                    station_pair_[1]
                ]
                if segment_details != new_segment_details:  # Shallow dict comparison
                    existing_comment = network_adjacency_matrix[
                        station_pair
                    ].trivia.comment
                    network_adjacency_matrix[station_pair].comment(
                        f"NEW -> {json.dumps(new_segment_details)}{' | %s' % existing_comment if existing_comment else ''}"
                    )

        adjacency_matrix_segments = {
            f"{a}-{b}" for a in adjacency_matrix for b in adjacency_matrix[a]
        }

        # Mark defunct adjacency matrix entries with comment
        for defunct_segment in set(network_adjacency_matrix).difference(
            adjacency_matrix_segments
        ):
            existing_comment = network_adjacency_matrix[defunct_segment].trivia.comment
            network_adjacency_matrix[defunct_segment].comment(
                f"DEFUNCT{' | %s' % existing_comment if existing_comment else ''}"
            )

        # Add new adjacency matrix entries
        for new_segment in set(adjacency_matrix_segments).difference(
            network_adjacency_matrix
        ):
            vertices = new_segment.split("-", 1)
            start, end = vertices[0], vertices[1]
            it = tomlkit.inline_table()
            it.update(adjacency_matrix[start][end])
            network_adjacency_matrix[new_segment] = it
            network_adjacency_matrix[new_segment].comment("NEW")

        # Sort adjacency matrix entries
        updated_network_adjacency_matrix = tomlkit.table()
        for segment in sorted(
            network_adjacency_matrix,
            key=lambda pair: tuple(
                map(StationUtils.to_station_code_components, pair.split("-", 1))
            ),
        ):
            updated_network_adjacency_matrix[segment] = network_adjacency_matrix[
                segment
            ]
        return updated_network_adjacency_matrix

    @classmethod
    def update_network(
        cls,
        network: tomlkit.TOMLDocument,
        stations: list[tuple[str, str]],
        segment_adjacency_matrix: defaultdict[str, OrderedDict[str, dict]],
        transfer_adjacency_matrix: defaultdict[str, OrderedDict[str, dict]],
    ) -> None:
        """Replace contents of `network` configuration in-place
        with stations, segments, and transfers.

        - Newly added entries are marked as NEW.
        - Entries to be modified will have their new content added as an inline-comment.
        - Entries made defunct will be marked as DEFUNCT with an inline-comment.
        - Existing comments are preserved.

        Args:
            network (tomlkit.TOMLDocument): Network configuration to be updated.
            stations (list[tuple[str, str]]): After the update, `network` should only have
            these stations.
            segment_adjacency_matrix (defaultdict[str, OrderedDict[str, dict]]): After the update,
            `network` should only have these segments.
            transfer_adjacency_matrix (defaultdict[str, OrderedDict[str, dict]]): After the update,
            `network` should only have these transfers.
        """

        network["schema"] = network.get("schema", 1)
        network["default_transfer_time"] = network.get("default_transfer_time", 7)
        network["default_dwell_time_asc"] = network.get("default_dwell_time_asc", 0.5)
        network["default_dwell_time_desc"] = network.get("default_dwell_time_desc", 0.5)

        ### stations ###

        stations_ = {k: v for (k, v) in stations}
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
            network_stations, key=StationUtils.to_station_code_components
        ):
            updated_stations[station_code] = network_stations[station_code]
        network["stations"] = updated_stations

        ### segment adjacency matrix ###

        network["segments"] = cls.__get_updated_network_adjacency_matrix(
            network["segments"] if "segments" in network else tomlkit.table(),
            segment_adjacency_matrix,
        )

        ### transfer adjacency matrix ###

        network["transfers"] = cls.__get_updated_network_adjacency_matrix(
            network["transfers"] if "transfers" in network else tomlkit.table(),
            transfer_adjacency_matrix,
        )

    def update_network_config_file(self, path: pathlib.Path) -> None:
        """Overwrite contents of network configuration file at `path` with updated
        network data. See `Config.update_network`.

        Args:
            path (pathlib.Path): Path to network configuration file.
        """
        try:
            with open(path, "rb") as f:
                network: tomlkit.TOMLDocument = tomlkit.load(f)
        except OSError:
            network: tomlkit.TOMLDocument = tomlkit.TOMLDocument()
        Config.update_network(
            network,
            self.stations,
            self.segment_adjacency_matrix,
            self.transfer_adjacency_matrix,
        )
        with open(path, "w") as f:
            tomlkit.dump(network, f)
