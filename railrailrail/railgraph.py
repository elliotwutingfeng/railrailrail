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

from __future__ import annotations

import csv
import itertools
import pathlib
import tomllib
import typing

from dijkstar import Graph
from dijkstar.algorithm import PathInfo, find_path

from railrailrail.dataset.conditional_interchange import ConditionalInterchange
from railrailrail.dataset.station import Station
from railrailrail.dataset.terminal import Terminal
from railrailrail.logger import logger
from railrailrail.utils import GeographicUtils


class RailGraph:
    """Graph for calculating shortest route and time cost between any 2 stations."""

    __minimum_duration = 0
    __maximum_duration = 3600  # 3600 seconds = 1 hour

    def __init__(
        self,
        segments: dict[tuple[str, str], dict],
        transfers: dict[tuple[str, str], dict],
        stations: dict[str, str],
        station_coordinates: dict[str, tuple[float, float]],
        default_transfer_time: int = 420,
        default_dwell_time: int = 30,
    ):
        """Setup rail network graph.

        Args:
            segments (dict[tuple[str, str], dict]): Every adjacent pair of stations directly connected to each
            other either by rail (same line), or by walking.
            transfers (dict[tuple[str, str], dict]): Every pair of stations that belong to the same interchange.
            stations (dict[str, str]): Map of station codes to station names.
            station_coordinates (dict[str, tuple[float, float]]): Map of station codes to station latitude and longitude.
            default_transfer_time (int, optional): Time taken to switch lines at an interchange station in seconds. Defaults to 420.
            default_dwell_time (int, optional): Time taken by train to either drop off or pick up passengers at a station in seconds. Defaults to 30.
        """
        if type(default_transfer_time) is not int or default_transfer_time < 0:
            raise ValueError("default_transfer_time must be non-negative int.")
        if type(default_dwell_time) is not int or default_dwell_time < 0:
            raise ValueError("default_dwell_time must be non-negative int.")
        if not isinstance(stations, dict) or not stations:
            raise ValueError("stations must be dict and not empty.")
        for k, v in stations.items():
            if type(k) is not str or type(v) is not str:
                raise ValueError("stations must be dict[str, str]")

        self.transfers = transfers
        self._stations = {
            station_code: Station(station_code, station_name)
            for station_code, station_name in stations.items()
        }
        self._station_coordinates = station_coordinates
        self.default_transfer_time = default_transfer_time
        self.default_dwell_time = default_dwell_time

        self._interchanges = Station.get_interchanges(list(self._stations.values()))

        # Undirected Graph allows for different time cost when moving in opposite direction.
        self._graph = Graph(undirected=False)
        self._graph_without_walk_segments = Graph(undirected=False)

        for (start, end), segment_details in segments.items():
            for station_code in (start, end):
                if station_code not in self._stations:
                    raise ValueError(
                        f"Station {station_code} in segment {start}-{end} does not have a name."
                    )

            duration = segment_details.get("duration", None)
            if (type(duration) is not int) or not (
                self.__minimum_duration <= duration <= self.__maximum_duration
            ):
                raise ValueError(
                    f"Segment duration must be number in range {self.__minimum_duration}-{self.__maximum_duration}"
                )

            edge_type = segment_details.get("edge_type", "")
            mode = segment_details.get("mode", "")
            dwell_time_asc = segment_details.get("dwell_time_asc", 0)
            dwell_time_desc = segment_details.get("dwell_time_asc", 0)

            is_ascending: bool = Station.to_station_code_components(
                start
            ) < Station.to_station_code_components(end)

            edge = (
                duration,
                edge_type,
                mode,
                dwell_time_asc if is_ascending else dwell_time_desc,
            )
            self._graph.add_edge(start, end, edge)
            if mode != "walk":
                self._graph_without_walk_segments.add_edge(start, end, edge)

            edge = (
                duration,
                edge_type,
                mode,
                dwell_time_desc if is_ascending else dwell_time_asc,
            )
            self._graph.add_edge(end, start, edge)
            if mode != "walk":
                self._graph_without_walk_segments.add_edge(end, start, edge)

        for interchange_substations in (
            self._interchanges
        ):  # Link up unique pairs of substations on the same interchange station.
            for start, end in itertools.permutations(interchange_substations, 2):
                if (start.station_code, end.station_code) not in self.transfers:
                    raise ValueError(
                        f"{start.station_code}-{end.station_code} not found in [transfers]."
                    )
                transfer_details = self.transfers[
                    (start.station_code, end.station_code)
                ]
                duration = transfer_details.get("duration", None)
                if (type(duration) is not int) or not (
                    self.__minimum_duration <= duration <= self.__maximum_duration
                ):
                    raise ValueError(
                        f"Transfer duration must be number in range {self.__minimum_duration}-{self.__maximum_duration}"
                    )
                edge_type = transfer_details.get("edge_type", "")
                mode = transfer_details.get("mode", "")
                dwell_time_asc = transfer_details.get(
                    "dwell_time_asc", self.default_dwell_time
                )
                dwell_time_desc = transfer_details.get(
                    "dwell_time_asc", self.default_dwell_time
                )

                is_ascending: bool = (
                    start.line_code,
                    start.station_number,
                    start.station_number_suffix,
                ) < (end.line_code, end.station_number, end.station_number_suffix)
                edge = (
                    duration,
                    edge_type,
                    mode,
                    dwell_time_asc if is_ascending else dwell_time_desc,
                )
                self._graph.add_edge(start.station_code, end.station_code, edge)
                self._graph_without_walk_segments.add_edge(
                    start.station_code, end.station_code, edge
                )

    @classmethod
    def from_file(
        cls, network_path: pathlib.Path, coordinates_path: pathlib.Path
    ) -> RailGraph:
        """Setup rail network graph from network configuration file.

        Args:
            network_path (pathlib.Path): Path to network configuration file.
            coordinates_path (pathlib.Path): Path to station coordinates file.

        Raises:
            ValueError: Invalid config file.

        Returns:
            RailGraph: Rail network graph.
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
        for segment, segment_details in segments.items():
            vertices = segment.split("-", 2)
            if len(vertices) != 2:
                raise ValueError(
                    f"Invalid config file: Segment must be in format 'AB1-AB2'. Got {segment}."
                )
            if not isinstance(segment_details, dict):
                raise ValueError("Invalid config file: Segment details must be a dict.")
            start, end = vertices[0], vertices[1]
            segments_[(start, end)] = segment_details

        transfers = network.get("transfers", None)
        if not isinstance(transfers, dict):
            raise ValueError(
                "Invalid config file: 'transfers' key must exist, even if there are no values."
            )

        transfers_ = dict()
        for transfer, transfer_details in transfers.items():
            vertices = transfer.split("-", 2)
            if len(vertices) != 2:
                raise ValueError(
                    f"Invalid config file: Transfer must be in format 'AB1-AB2'. Got {transfer}."
                )
            if not isinstance(transfer_details, dict):
                raise ValueError(
                    "Invalid config file: Transfer details must be a dict."
                )
            start, end = vertices[0], vertices[1]
            transfers_[(start, end)] = transfer_details

        station_coordinates = dict()
        with open(coordinates_path, "r") as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # Skip column headers.
            for row in csv_reader:
                station_coordinates[row[0]] = float(row[2]), float(row[3])

        # Assign coordinates to missing/future/pseudo station codes.
        equivalent_station_code_pairs = (
            ("CG", "EW4"),
            ("TE33", "CG2"),
            ("TE34", "CG1"),
            ("TE35", "EW4"),
            ("CC33", "CE2"),
            ("CC34", "CE1"),
            ("CE0X", "CC6"),
            ("CE0Y", "CC5"),
            ("CE0Z", "CC4"),
            ("JE0", "JS3"),
        )
        for code1, code2 in equivalent_station_code_pairs:
            station_coordinates[code1] = station_coordinates[code2]

        return cls(
            segments_,
            transfers_,
            stations,
            station_coordinates,
            default_transfer_time,
            default_dwell_time,
        )

    def _cost_func(self, start: str, end: str) -> typing.Callable[..., int]:
        def cost_func_aux(
            current_station: str,
            next_station: str,
            edge_to_next_station: tuple,
            edge_to_current_station: tuple | None,
        ) -> int:
            """Compute time cost of travelling from current station to next station.

            Transfer time is added if the preceding and succeeding edges imply a sub-interchange transfer.

            Dwell time is added for every station unless if walking away from the station.

            Any transfer time involving the `start` station
            or `end` station of the entire journey will be excluded.

            Transfers involving `end` station will also not have any dwell time.

            Args:
                current_station (str): Current station.
                next_station (str): Next station.
                edge_to_next_station (tuple): Edge to next station.
                edge_to_current_station (tuple | None): Edge to current station.

            Returns:
                int: Time cost in seconds.
            """
            (
                next_travel_time,
                next_edge_type,
                next_edge_mode,
                next_dwell_time,
            ) = edge_to_next_station

            dwell_time = next_dwell_time

            if isinstance(edge_to_current_station, tuple):
                (
                    previous_edge_duration,
                    previous_edge_type,
                    previous_edge_mode,
                    previous_dwell_time,
                ) = edge_to_current_station
            else:
                (
                    previous_edge_duration,
                    previous_edge_type,
                    previous_edge_mode,
                    previous_dwell_time,
                ) = (0, "", "", 0)
            _ = previous_edge_duration
            _ = previous_edge_mode
            _ = previous_dwell_time

            cost = next_travel_time
            if (
                next_edge_mode == "walk"
            ):  # Walking away from station -> Not waiting for train to depart.
                dwell_time = 0

            if ConditionalInterchange.is_conditional_interchange_transfer(
                previous_edge_type, next_edge_type
            ):
                cost += self.default_transfer_time  # TODO Use network config timing.

            if current_station == start or next_station == end:
                if (
                    (current_station, next_station) in self.transfers
                ):  # Exclude transfer time for transfers at start or end of journey.
                    cost -= next_travel_time
                    if (
                        next_station == end
                    ):  # Exclude dwell time for transfer at end of journey.
                        dwell_time = 0

            return cost + dwell_time

        return cost_func_aux

    def find_shortest_path(
        self,
        start: str,
        end: str,
        walk: bool = False,
    ) -> PathInfo:
        """Find shortest path between 2 stations `start` and `end`.

        Pseudo station codes like "CE0Y" are considered invalid.

        Args:
            start (str): Station code of station to start from.
            end (str): Station code of station to arrive at.
            walk (bool): Allow station transfers by walking.

        Raises:
            ValueError: Invalid station code.

        Returns:
            PathInfo: Shortest path between 2 stations `start` and `end`.
        """
        for station_code in (start, end):
            _, station_number, _ = Station.to_station_code_components(station_code)
            if station_number == 0:  # Reject pseudo station codes.
                raise ValueError(f"Pseudo station code not allowed: {station_code}")

        pathinfo = find_path(
            self._graph if walk else self._graph_without_walk_segments,
            start,
            end,
            cost_func=self._cost_func(start, end),
        )
        logger.info("%s", pathinfo)
        return pathinfo

    def make_directions(self, pathinfo: PathInfo) -> list[str]:
        """Make step-by-step directions for a given journey.

        Args:
            pathinfo (PathInfo): Journey path information.

        Returns:
            list[str]: Step-by-step directions.
        """
        if len(pathinfo.nodes) < 2:
            raise ValueError("At least 2 stations needed for journey.")
        status = "at_station"  # at_station | in_train | walking
        steps: list[str] = [
            f"Start at {self._stations[pathinfo.nodes[0]].full_station_name}"
        ]
        for edge_idx, (u, v, edge_details) in enumerate(
            zip(pathinfo.nodes[:-1], pathinfo.nodes[1:], pathinfo.edges)
        ):
            at_pseudo_station = (
                self._stations[u].has_pseudo_station_code
                or self._stations[v].has_pseudo_station_code
            )
            u_ = self._stations[u].real_station_code
            v_ = self._stations[v].real_station_code
            if status == "walking":
                if edge_details[2] == "walk":  # Walk to the next station.
                    # Replace previous walking step with this walking step, effectively merging both steps into one step.
                    # Instead of A -> walk -> B -> walk -> C, do A -> walk -> C instead.
                    steps.pop()
                    steps.append(f"Walk to {self._stations[v_].full_station_name}")
                    status = "walking"
                else:
                    terminal: str | None = Terminal.get_terminal(self._graph, u, v)
                    steps.append(
                        f"Board train in direction of {self._stations[v_].full_station_name}"  # Unusual terminal. Use next station instead.
                        if terminal is None
                        else f"Board train towards terminus {self._stations[terminal].full_station_name}"
                    )
                    status = "in_train"
            elif status == "at_station":
                if (u, v) in self.transfers:  # Interchange transfer.
                    steps.append(
                        f"{'Switch over at' if at_pseudo_station else 'Transfer to'} {self._stations[v_].full_station_name}"
                    )
                elif edge_details[2] == "walk":  # Walk to the next station.
                    steps.append(f"Walk to {self._stations[v_].full_station_name}")
                    status = "walking"
                elif (
                    0 < edge_idx
                    and ConditionalInterchange.is_conditional_interchange_transfer(
                        pathinfo.edges[edge_idx - 1][1], pathinfo.edges[edge_idx][1]
                    )
                ):  # Conditional interchange transfer
                    raise RuntimeError(
                        "Something is not right; this conditional interchange transfer is also an interchange transfer. "
                        "Check ConditionalInterchange class and rail network structure. PathInfo: %s"
                        % pathinfo
                    )
                else:  # Board a train.
                    terminal: str | None = Terminal.get_terminal(self._graph, u, v)
                    steps.append(
                        f"Board train in direction of {self._stations[v_].full_station_name}"  # Unusual terminal. Use next station instead.
                        if terminal is None
                        else f"Board train towards terminus {self._stations[terminal].full_station_name}"
                    )
                    status = "in_train"
            elif status == "in_train":
                if (u, v) in self.transfers:  # Interchange transfer.
                    steps.append(f"Alight at {self._stations[u_].full_station_name}")
                    steps.append(
                        f"{'Switch over at' if at_pseudo_station else 'Transfer to'} {self._stations[v_].full_station_name}"
                    )
                    status = "at_station"
                elif edge_details[2] == "walk":  # Walk to the next station.
                    steps.append(f"Alight at {self._stations[u_].full_station_name}")
                    steps.append(f"Walk to {self._stations[v_].full_station_name}")
                    status = "walking"
                elif (
                    0 < edge_idx
                    and ConditionalInterchange.is_conditional_interchange_transfer(
                        pathinfo.edges[edge_idx - 1][1], pathinfo.edges[edge_idx][1]
                    )
                ):  # Conditional interchange transfer
                    steps.append(
                        f"Switch over at {self._stations[u_].full_station_name}"
                    )
                    terminal: str | None = Terminal.get_terminal(self._graph, u, v)
                    steps.append(
                        f"Board train in direction of {self._stations[v_].full_station_name}"  # Unusual terminal. Use next station instead.
                        if terminal is None
                        else f"Board train towards terminus {self._stations[terminal].full_station_name}"
                    )
                    status = "in_train"
        if steps and steps[-1].startswith("Switch over"):
            steps.pop()  # Special case: Final edge is interchange transfer from pseudo station like JE0 -> JS3.
        if status == "in_train":
            steps.append(f"Alight at {self._stations[v_].full_station_name}")
        steps.append(
            f"""Total duration: {pathinfo.total_cost // 60} minutes {pathinfo.total_cost % 60} seconds"""
        )
        path_distance, haversine_distance = self.path_and_haversine_distance(pathinfo)
        steps.append(
            f"Approximate path distance: {path_distance/ 1000 :.1f} km, "
            f"Haversine distance: {haversine_distance / 1000 :.1f} km, "
            f"Circuity ratio: {(path_distance / haversine_distance ) if haversine_distance > 0 else 1 :.1f}"
        )
        return steps

    def path_and_haversine_distance(self, pathinfo: PathInfo) -> tuple[float, float]:
        """Estimated path distance and haversine (great-circle) distance between origin station and
        destination station.

        The path distance returned by this method is a rough estimate made by
        treating paths between adjacent stations as haversine (great-circle) paths.

        Args:
            pathinfo (PathInfo): Journey path information.

        Raises:
            ValueError: At least 2 stations needed for journey.

        Returns:
            tuple[float, float]: Path distance and Haversine distance between origin station and destination station.
        """
        nodes = pathinfo.nodes
        if len(nodes) < 2:
            raise ValueError("At least 2 stations needed for journey.")
        lat1, lon1 = self._station_coordinates[nodes[0]]
        lat2, lon2 = self._station_coordinates[nodes[-1]]
        haversine_distance: float = GeographicUtils.haversine_distance(
            lat1, lon1, lat2, lon2
        )
        path_distance: float = 0
        for current_node, next_node in zip(nodes[:-1], nodes[1:]):
            lat1, lon1 = self._station_coordinates[current_node]
            lat2, lon2 = self._station_coordinates[next_node]
            path_distance += GeographicUtils.haversine_distance(lat1, lon1, lat2, lon2)

        logger.info(
            "Approximate path distance: %.3f km, Haversine distance: %.3f km, Circuity ratio: %.2f",
            path_distance / 1000,
            haversine_distance / 1000,
            (path_distance / haversine_distance) if haversine_distance > 0 else 1,
        )
        return path_distance, haversine_distance
