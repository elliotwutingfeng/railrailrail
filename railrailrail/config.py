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

import csv
import itertools
import json
import pathlib
import tomllib
import warnings
from collections import OrderedDict, defaultdict

import tomlkit

from railrailrail.network.conditional_interchange import ConditionalInterchange
from railrailrail.network.durations import Durations
from railrailrail.network.dwell_time import DwellTime
from railrailrail.network.stage import Stage
from railrailrail.network.station import Station
from railrailrail.network.terminal import Terminal
from railrailrail.network.walking_train_map import WalkingTrainMap
from railrailrail.utils import Coordinates


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
            key=lambda station: (
                station.line_code,
                station.station_number,
                station.station_number_suffix,
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
        station_code_to_station: dict[str, Station] = {
            station.station_code: station for station in self.stations
        }

        stations_by_line_code: defaultdict[str, set[Station]] = defaultdict(
            set
        )  # Order is important as stations are almost always connected in sequential order.
        for station in self.stations:  # Group stations by line.
            stations_by_line_code[station.line_code].add(station)

        # Uni-directionally link up all adjacent stations on same line based on the fact that most adjacent stations
        # are arranged by station code in sequential order (same line code and in ascending station number order).
        adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = defaultdict(
            OrderedDict
        )
        for stations in stations_by_line_code.values():
            line_stations = sorted(
                stations,
                key=lambda station: (
                    station.line_code,
                    station.station_number,
                    station.station_number_suffix,
                ),
            )
            for station, next_station in zip(line_stations[:-1], line_stations[1:]):
                station_code, next_station_code = (
                    station.station_code,
                    next_station.station_code,
                )
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

        if (
            "EW14" not in station_code_to_station
            and "EW15" in station_code_to_station
            and "NS26" in station_code_to_station
        ):
            # Special case: EWL still part of NSL.
            station_code, next_station_code = "EW15", "NS26"
            adjacency_matrix[station_code][next_station_code] = {
                "duration": Durations.segments.get(
                    f"{station_code}-{next_station_code}", dict()
                ).get(
                    "duration", -1
                ),  # Invalid negative value, to be manually updated by user.
            }

        # Add dwell time for each rail segment.
        terminal_station_codes: set[str] = Terminal.get_terminals(adjacency_matrix)
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

        # Create and mark segments that need to be treated differently from
        # most other segments. Currently this only means checking if a segment is
        # adjacent to a conditional interchange.
        for segment in ConditionalInterchange.segments:
            # Skip conditional interchange segments made obsolete by new stations.
            if (
                isinstance(segment.defunct_with_station_code, str)
                and segment.defunct_with_station_code in station_code_to_station
            ):
                continue
            station_a, station_b = segment.station_code_pair
            if (
                station_a in station_code_to_station
                and station_b in station_code_to_station
            ):
                dwell_time_asc, dwell_time_desc = DwellTime.get_dwell_time(
                    terminal_station_codes,
                    interchange_station_codes.union({segment.interchange_station_code}),
                    station_a,
                    station_b,
                )
                adjacency_matrix[station_a][station_b] = {
                    **Durations.segments[f"{station_a}-{station_b}"],
                    "edge_type": segment.edge_type.name,
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

        return adjacency_matrix

    @classmethod
    def __get_updated_stations(
        cls, network_stations: tomlkit.items.Table, stations: list[Station]
    ):
        station_code_to_station_name = {
            station.station_code: station.station_name for station in stations
        }
        # Mark modified stations with comment
        for station_code, station_name in network_stations.items():
            if (
                station_code in station_code_to_station_name
                and station_name != station_code_to_station_name[station_code]
            ):
                existing_comment = network_stations[station_code].trivia.comment
                network_stations[station_code].comment(
                    f"NEW -> {station_code_to_station_name[station_code]}{' | %s' % existing_comment if existing_comment else ''}"
                )

        # Mark defunct stations with comment
        for defunct_station_code in set(network_stations).difference(
            station_code_to_station_name
        ):
            existing_comment = network_stations[defunct_station_code].trivia.comment
            network_stations[defunct_station_code].comment(
                f"DEFUNCT{' | %s' % existing_comment if existing_comment else ''}"
            )

        # Add new stations
        for new_station_code in set(station_code_to_station_name).difference(
            network_stations
        ):
            network_stations[new_station_code] = station_code_to_station_name[
                new_station_code
            ]
            network_stations[new_station_code].comment("NEW")

        # Sort stations
        updated_stations = tomlkit.table()
        for station_code in sorted(
            network_stations, key=Station.to_station_code_components
        ):
            updated_stations[station_code] = network_stations[station_code]
        return updated_stations

    @classmethod
    def __get_updated_network_adjacency_matrix(
        cls,
        network_adjacency_matrix: tomlkit.items.Table,
        adjacency_matrix: defaultdict[str, OrderedDict[str, dict]],
    ) -> tomlkit.items.Table:
        # Mark modified edges with comment
        for station_pair, edge_details in network_adjacency_matrix.items():
            first_station, second_station = station_pair.split("-", 1)
            if (
                first_station in adjacency_matrix
                and second_station in adjacency_matrix[first_station]
            ):
                new_edge_details = adjacency_matrix[first_station][second_station]
                if edge_details != new_edge_details:  # Shallow dict comparison
                    existing_comment = network_adjacency_matrix[
                        station_pair
                    ].trivia.comment
                    network_adjacency_matrix[station_pair].comment(
                        f"NEW -> {json.dumps(new_edge_details)}{' | %s' % existing_comment if existing_comment else ''}"
                    )

        adjacency_matrix_edges = {
            f"{first_station}-{second_station}"
            for first_station in adjacency_matrix
            for second_station in adjacency_matrix[first_station]
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
        network["stations"] = self.__get_updated_stations(
            network.get("stations", tomlkit.table()), self.stations
        )
        network["segments"] = self.__get_updated_network_adjacency_matrix(
            network.get("segments", tomlkit.table()),
            self.segment_adjacency_matrix,
        )
        network["transfers"] = self.__get_updated_network_adjacency_matrix(
            network.get("transfers", tomlkit.table()),
            self.transfer_adjacency_matrix,
        )

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

    @classmethod
    def parse_network_config(
        cls, network_path: pathlib.Path, coordinates_path: pathlib.Path
    ) -> tuple:
        """Parse network configuration file and station coordinates file.

        Args:
            network_path (pathlib.Path): Path to network configuration file.
            coordinates_path (pathlib.Path): Path to station coordinates file.

        Raises:
            ValueError: Invalid config file.

        Returns:
            tuple: Parsed network configuration data.
        """
        with open(network_path, "rb") as f:
            network = tomllib.load(f)

        schema = network.get("schema", None)
        if schema != 1:
            raise ValueError("Invalid config file: 'schema' must be 1.")
        stations = network.get("stations", None)
        if not isinstance(stations, dict) or not stations:
            raise ValueError("Invalid config file: 'stations' must not be empty.")
        default_transfer_time = network.get("default_transfer_time", None)
        if type(default_transfer_time) is not int:
            raise ValueError(
                "Invalid config file: 'default_transfer_time' must be int."
            )
        default_dwell_time = network.get("default_dwell_time", None)
        if type(default_dwell_time) is not int:
            raise ValueError("Invalid config file: 'default_dwell_time'  must be int.")

        segments = network.get("segments", None)
        if not isinstance(segments, dict) or not segments:
            raise ValueError("Invalid config file: 'segments' must not be empty.")

        segments_ = dict()
        for segment_link, segment_details in segments.items():
            vertices = tuple(segment_link.split("-", 2))
            if len(vertices) != 2:
                raise ValueError(
                    f"Invalid config file: Segment link must be in format 'AB1-AB2'. Got {segment_link}."
                )
            if not isinstance(segment_details, dict):
                raise ValueError("Invalid config file: Segment details must be a dict.")
            segments_[vertices] = segment_details

        transfers = network.get("transfers", None)
        if not isinstance(transfers, dict):
            raise ValueError(
                "Invalid config file: 'transfers' key must exist, even if there are no values."
            )

        transfers_ = dict()
        for transfer, transfer_details in transfers.items():
            vertices = tuple(transfer.split("-", 2))
            if len(vertices) != 2:
                raise ValueError(
                    f"Invalid config file: Transfer must be in format 'AB1-AB2'. Got {transfer}."
                )
            if not isinstance(transfer_details, dict):
                raise ValueError(
                    "Invalid config file: Transfer details must be a dict."
                )
            transfers_[vertices] = transfer_details

        station_coordinates: dict[str, Coordinates] = dict()
        with open(coordinates_path, "r") as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # Skip column headers.
            for row in csv_reader:
                station_coordinates[row[0]] = Coordinates(float(row[2]), float(row[3]))

        # Assign coordinates to missing/future/pseudo station codes.
        for code1, code2 in Station.equivalent_station_code_pairs:
            station_coordinates[code1] = station_coordinates[code2]

        return (
            segments_,
            transfers_,
            stations,
            station_coordinates,
            default_transfer_time,
            default_dwell_time,
        )
