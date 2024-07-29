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

from railrailrail.network.conditional_transfers import ConditionalTransfers
from railrailrail.network.dwell_time import DwellTime
from railrailrail.network.segments import Segments
from railrailrail.network.stage import Stage
from railrailrail.network.station import Station
from railrailrail.network.terminal import Terminal
from railrailrail.network.transfers import Transfers
from railrailrail.network.walks import Walks
from railrailrail.utils import Coordinates


class Config:
    """Create and update existing rail network configuration files with preset values for
    each stage of the Singapore MRT/LRT system.

    A helper classmethod for parsing configuration files is provided. See `parse_network_config`.
    """

    def __init__(self, stage: Stage):
        """Setup network `Config` based on `stage`.

        Args:
            stage (Stage): Rail network stage.
        """
        self.stage = stage
        self.stations: list[Station] = self._get_stations()

        # Station lookup tables.
        self._station_codes_by_station_name: dict[str, set[str]] = defaultdict(set)
        for station in self.stations:
            self._station_codes_by_station_name[station.station_name].add(
                station.station_code
            )
        self._stations_by_line_code: defaultdict[str, set[Station]] = defaultdict(set)
        for station in self.stations:
            self._stations_by_line_code[station.line_code].add(station)

        # Network config sections.
        self.station_code_to_station: dict[str, Station] = {
            station.station_code: station for station in self.stations
        }
        self.non_linear_line_terminals: dict[str, set[str]] = (
            self._generate_non_linear_line_terminals()
        )
        self.segment_adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = (
            self._generate_segment_adjacency_matrix()
        )
        self.transfer_adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = (
            self._generate_transfer_adjacency_matrix()
        )
        self.conditional_transfers: dict[str, dict[str, int]] = (
            self._generate_conditional_transfers()
        )

    def _get_stations(self) -> list[Station]:
        """Generate list of operational train station codes and station names,
        sorted by station code in ascending order.

        Order is important as stations are almost always connected in sequential order.

        Returns:
            list[Station]: Train stations sorted by station code in ascending order.
        """

        return sorted(
            self.stage.stations,
            key=Station.sort_key,
        )

    def _generate_segment_adjacency_matrix(
        self,
    ) -> defaultdict[str, OrderedDict[str, dict]]:
        """Create an travel time / dwell time adjacency matrix for all segments between stations with different names
        on the network.

        Returns:
            defaultdict[str, OrderedDict[str, dict]]: Travel time adjacency matrix.
        """
        # Uni-directionally link up all adjacent stations on same line based on the fact that most adjacent stations
        # are arranged by station code in sequential order (same line code and in ascending station number order).
        adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = defaultdict(
            OrderedDict
        )
        for stations in self._stations_by_line_code.values():
            line_stations = sorted(
                stations,
                key=Station.sort_key,
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
                    "duration": Segments.segments.get(
                        f"{station_code}-{next_station_code}", dict()
                    ).get(
                        "duration", -1
                    ),  # Invalid negative value, to be manually updated by user.
                }

        if (
            "EW14" not in self.station_code_to_station
            and "EW15" in self.station_code_to_station
            and "NS26" in self.station_code_to_station
        ):
            # Special case: EWL still part of NSL.
            station_code, next_station_code = "EW15", "NS26"
            adjacency_matrix[station_code][next_station_code] = {
                "duration": Segments.segments.get(
                    f"{station_code}-{next_station_code}", dict()
                ).get(
                    "duration", -1
                ),  # Invalid negative value, to be manually updated by user.
            }

        # Add dwell time for each rail segment.
        terminal_station_codes: set[str] = Terminal.get_terminals(
            self.non_linear_line_terminals, adjacency_matrix
        )
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
        for start_station_name, end_station_name, duration in Walks.routes:
            for start_station_code in self._station_codes_by_station_name[
                start_station_name
            ]:
                for end_station_code in self._station_codes_by_station_name[
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
        for segment in ConditionalTransfers.conditional_transfer_segments:
            # Skip conditional interchange segments made obsolete by new stations.
            if (
                isinstance(segment.defunct_with_station_code, str)
                and segment.defunct_with_station_code in self.station_code_to_station
            ):
                continue
            station_a, station_b = segment.station_code_pair
            if (
                station_a in self.station_code_to_station
                and station_b in self.station_code_to_station
            ):
                dwell_time_asc, dwell_time_desc = DwellTime.get_dwell_time(
                    terminal_station_codes,
                    interchange_station_codes.union({segment.interchange_station_code}),
                    station_a,
                    station_b,
                )
                adjacency_matrix[station_a][station_b] = {
                    **Segments.segments[f"{station_a}-{station_b}"],
                    "edge_type": segment.edge_type,
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
        interchanges: dict[str, set[str]] = {
            station_name: station_codes
            for (
                station_name,
                station_codes,
            ) in self._station_codes_by_station_name.items()
            if len(station_codes) >= 2
        }
        adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = defaultdict(
            OrderedDict
        )
        pairs = []
        for station_name, station_codes in interchanges.items():
            if station_name in Transfers.interchange_transfers:
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
            duration = Transfers.interchange_transfers[station_name]
            adjacency_matrix[start][end] = {"duration": duration}

        return adjacency_matrix

    def _generate_conditional_transfers(self) -> dict[str, dict[str, int]]:
        # Filter out unused conditional transfers.
        edge_types: set[str] = set()
        for start in self.segment_adjacency_matrix:
            for _, segment_details in self.segment_adjacency_matrix[start].items():
                edge_type = segment_details.get("edge_type", None)
                if isinstance(edge_type, str):
                    edge_types.add(edge_type)
        conditional_transfers: defaultdict[str, dict[str, int]] = defaultdict(dict)
        for start in ConditionalTransfers.conditional_transfers:
            for end, duration in ConditionalTransfers.conditional_transfers[
                start
            ].items():
                if {start, end}.issubset(edge_types):
                    conditional_transfers[start][end] = duration
        return dict(conditional_transfers)

    def _generate_non_linear_line_terminals(self) -> dict[str, set[str]]:
        non_linear_line_terminals: dict[str, set[str]] = dict()

        for line_code in (
            Terminal.looped_line_code_to_terminals
        ):  # Only include looped line terminals that exist.
            if line_code not in self._stations_by_line_code:
                continue
            terminal_station_codes: set[str] = set()
            for station_code in Terminal.looped_line_code_to_terminals[line_code]:
                if station_code in self.station_code_to_station:
                    terminal_station_codes.add(station_code)
            if terminal_station_codes:
                non_linear_line_terminals[line_code] = terminal_station_codes

        if (
            "CC34" in self.station_code_to_station
        ):  # Special case: Circle Line becomes a looped line at Stage 6.
            non_linear_line_terminals["CC"] = {"CC1"}

        if (
            "EW14" not in self.station_code_to_station
            and "EW15" in self.station_code_to_station
            and "NS26" in self.station_code_to_station
        ):  # Special case: EWL still part of NSL.
            terminals = {
                sorted(
                    self._stations_by_line_code["EW"],
                    key=Station.sort_key,
                )[-1].station_code,
                sorted(
                    self._stations_by_line_code["NS"],
                    key=Station.sort_key,
                )[0].station_code,
            }  # Highest EW and Lowest NS
            non_linear_line_terminals["EW"] = terminals.copy()
            non_linear_line_terminals["NS"] = terminals.copy()
        return non_linear_line_terminals

    @classmethod
    def __get_updated_stations(
        cls,
        network_stations: tomlkit.items.Table,
        stations: list[Station],
        do_not_comment_new_lines: bool,
    ) -> tomlkit.items.Table:
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
            if not do_not_comment_new_lines:
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
        do_not_comment_new_lines: bool,
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
            if not do_not_comment_new_lines:
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

    @classmethod
    def __get_updated_network_conditional_transfers(
        cls,
        network_conditional_transfers: tomlkit.items.Table,
        conditional_transfers: dict[str, dict[str, int]],
        do_not_comment_new_lines: bool,
    ) -> tomlkit.items.Table:
        for start in network_conditional_transfers:
            for end, duration in network_conditional_transfers[start].items():
                existing_comment = network_conditional_transfers[start][
                    end
                ].trivia.comment
                # Mark modified conditional transfers with comment
                if (
                    start in conditional_transfers
                    and end in conditional_transfers[start]
                    and conditional_transfers[start][end] != duration
                ):
                    network_conditional_transfers[start][end].comment(
                        f"NEW -> {conditional_transfers[start][end]}{' | %s' % existing_comment if existing_comment else ''}"
                    )
                # Mark defunct conditional transfers with comment
                elif (
                    start not in conditional_transfers
                    or end not in conditional_transfers[start]
                ):
                    network_conditional_transfers[start][end].comment(
                        f"DEFUNCT{' | %s' % existing_comment if existing_comment else ''}"
                    )

        # Add new conditional transfers
        for start in conditional_transfers:
            for end, duration in conditional_transfers[start].items():
                has_start = start in network_conditional_transfers
                has_end = end in network_conditional_transfers.get(start, dict())
                if has_start and has_end:
                    continue
                network_conditional_transfers[tomlkit.key([start, end])] = (
                    conditional_transfers[start][end]
                )
                if not do_not_comment_new_lines:
                    network_conditional_transfers[start][end].comment("NEW")

        # Sort conditional transfers
        updated_conditional_transfers = tomlkit.table()
        for start in sorted(network_conditional_transfers):
            for end in sorted(network_conditional_transfers[start]):
                updated_conditional_transfers[tomlkit.key([start, end])] = (
                    network_conditional_transfers[start][end]
                )
        return updated_conditional_transfers

    @classmethod
    def __get_updated_non_linear_line_terminals(
        cls,
        network_non_linear_line_terminals: tomlkit.items.Table,
        non_linear_line_terminals: dict[str, set[str]],
        do_not_comment_new_lines: bool,
    ) -> tomlkit.items.Table:
        for line_code, station_codes in network_non_linear_line_terminals.items():
            for station_code, val in station_codes.items():
                # Mark modified terminals with comment
                if (
                    station_code in non_linear_line_terminals.get(line_code, set())
                    and val != 1
                ):
                    existing_comment = network_non_linear_line_terminals[line_code][
                        station_code
                    ].trivia.comment
                    network_non_linear_line_terminals[line_code][station_code].comment(
                        f"NEW -> {1}{' | %s' % existing_comment if existing_comment else ''}"
                    )
                # Mark defunct terminals with comment
                if station_code not in non_linear_line_terminals.get(line_code, set()):
                    existing_comment = network_non_linear_line_terminals[line_code][
                        station_code
                    ].trivia.comment
                    network_non_linear_line_terminals[line_code][station_code].comment(
                        f"DEFUNCT{' | %s' % existing_comment if existing_comment else ''}"
                    )

        # Add new terminals
        for line, station_codes in non_linear_line_terminals.items():
            for station_code in station_codes:
                if station_code not in network_non_linear_line_terminals.get(
                    line, set()
                ):
                    network_non_linear_line_terminals[
                        tomlkit.key([line, station_code])
                    ] = 1
                    if not do_not_comment_new_lines:
                        network_non_linear_line_terminals[line][station_code].comment(
                            "NEW"
                        )

        # Sort lines
        updated_non_linear_line_terminals = tomlkit.table()
        for line_code in sorted(network_non_linear_line_terminals):
            for station_code in sorted(
                network_non_linear_line_terminals[line_code],
                key=Station.to_station_code_components,
            ):
                updated_non_linear_line_terminals[
                    tomlkit.key([line_code, station_code])
                ] = network_non_linear_line_terminals[line_code][station_code]

        return updated_non_linear_line_terminals

    def update_network(
        self, network: tomlkit.TOMLDocument, do_not_comment_new_lines: bool = False
    ) -> None:
        """Update contents of `network` configuration in-place.

        - Newly added entries are marked as NEW.
        - Entries to be modified will have their new content added as an inline-comment.
        - Entries made defunct will be marked as DEFUNCT with an inline-comment.
        - Existing comments are preserved.

        Args:
            network (tomlkit.TOMLDocument): Network configuration to be updated.
            do_not_comment_new_lines (bool, optional): If enabled, no inline comments will be added for new lines. Defaults to False.
        """

        network["schema"] = network.get("schema", 1)
        network["stations"] = self.__get_updated_stations(
            network.get("stations", tomlkit.table()),
            self.stations,
            do_not_comment_new_lines,
        )
        network["segments"] = self.__get_updated_network_adjacency_matrix(
            network.get("segments", tomlkit.table()),
            self.segment_adjacency_matrix,
            do_not_comment_new_lines,
        )
        network["transfers"] = self.__get_updated_network_adjacency_matrix(
            network.get("transfers", tomlkit.table()),
            self.transfer_adjacency_matrix,
            do_not_comment_new_lines,
        )
        network["conditional_transfers"] = (
            self.__get_updated_network_conditional_transfers(
                network.get("conditional_transfers", tomlkit.table()),
                self.conditional_transfers,
                do_not_comment_new_lines,
            )
        )
        network["non_linear_line_terminals"] = (
            self.__get_updated_non_linear_line_terminals(
                network.get("non_linear_line_terminals", tomlkit.table()),
                self.non_linear_line_terminals,
                do_not_comment_new_lines,
            )
        )

    def update_network_config_file(
        self, path: pathlib.Path, do_not_comment_new_lines: bool = False
    ) -> None:
        """Overwrite contents of network configuration file at `path` with updated
        network data.

        Args:
            path (pathlib.Path): Path to network configuration file.
            do_not_comment_new_lines (bool, optional): If enabled, no inline comments will be added for new lines. Defaults to False.
        """
        try:
            with open(path, "rb") as f:
                network: tomlkit.TOMLDocument = tomlkit.load(f)
        except OSError:
            network: tomlkit.TOMLDocument = tomlkit.TOMLDocument()
        self.update_network(network, do_not_comment_new_lines)
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

        conditional_transfers = network.get("conditional_transfers", None)
        if not isinstance(conditional_transfers, dict):
            raise ValueError(
                "Invalid config file: 'conditional_transfers' key must exist, even if there are no values."
            )

        non_linear_line_terminals = network.get("non_linear_line_terminals", None)
        if not isinstance(non_linear_line_terminals, dict):
            raise ValueError(
                "Invalid config file: 'non_linear_line_terminals' key must exist, even if there are no values."
            )

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
            conditional_transfers,
            non_linear_line_terminals,
            stations,
            station_coordinates,
        )
