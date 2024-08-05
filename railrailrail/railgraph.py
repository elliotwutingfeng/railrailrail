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

import itertools
import pathlib
import typing

from dijkstar import Graph
from dijkstar.algorithm import PathInfo, find_path

from railrailrail.config import Config
from railrailrail.coordinates import Coordinates
from railrailrail.logger import logger
from railrailrail.network.station import SingaporeStation
from railrailrail.network.terminal import Terminal


class RailGraph:
    """Graph for calculating shortest route and time cost between any 2 stations."""

    __minimum_duration = 0
    __maximum_duration = 3600  # 3600 seconds = 1 hour

    def __init__(
        self,
        segments: dict[tuple[str, str], dict],
        transfers: dict[tuple[str, str], dict],
        conditional_transfers: dict[str, dict[str, int]],
        non_linear_line_terminals: dict[str, dict[str, int]],
        station_code_pseudonyms: dict[str, str],
        stations: dict[str, str],
        station_coordinates: dict[str, Coordinates],
    ):
        """Setup rail network graph.

        Args:
            segments (dict[tuple[str, str], dict]): Every adjacent pair of stations directly connected to each
            other either by rail (same line), or by walking.
            transfers (dict[tuple[str, str], dict]): Every pair of stations that belong to the same interchange.
            conditional_transfers (dict[str, dict[str, int]]): Edge type sequences for conditional transfers.
            non_linear_line_terminals (dict[str, dict[str, int]]): Map of non-linear line codes to terminal station codes.
            station_code_pseudonyms (dict[str, str]): Map of pseudo station codes to real station codes.
            stations (dict[str, str]): Map of station codes to station names.
            station_coordinates (dict[str, Coordinates]): Map of station codes to station latitude and longitude.
        """
        if not isinstance(stations, dict) or not stations:
            raise ValueError("stations must be non-empty dict.")
        for k, v in stations.items():
            if type(k) is not str or type(v) is not str:
                raise ValueError("stations must be dict[str, str]")

        self.transfers = transfers
        self.conditional_transfers = conditional_transfers
        self.non_linear_line_terminals = non_linear_line_terminals
        self.station_code_to_station = {
            station_code: SingaporeStation(
                station_code,
                station_name,
                station_code_pseudonyms.get(station_code, None),
            )
            for station_code, station_name in stations.items()
        }
        self.station_coordinates = station_coordinates

        # Undirected Graph allows for different time cost when moving in opposite direction.
        self._graph = Graph(undirected=False)
        self._graph_without_walk_segments = Graph(undirected=False)

        for (start, end), segment_details in segments.items():
            for station_code in (start, end):
                if station_code not in self.station_code_to_station:
                    raise ValueError(
                        f"Station {station_code} in segment {start}-{end} does not have a name."
                    )

            duration_asc = segment_details.get("duration_asc", None)
            if (type(duration_asc) is not int) or not (
                self.__minimum_duration <= duration_asc <= self.__maximum_duration
            ):
                raise ValueError(
                    f"Segment duration_asc must be number in range {self.__minimum_duration}-{self.__maximum_duration}"
                )
            duration_desc = segment_details.get("duration_desc", None)
            if (type(duration_desc) is not int) or not (
                self.__minimum_duration <= duration_desc <= self.__maximum_duration
            ):
                raise ValueError(
                    f"Segment duration_desc must be number in range {self.__minimum_duration}-{self.__maximum_duration}"
                )

            edge_type = segment_details.get("edge_type", "")
            mode = segment_details.get("mode", "")

            # Dwell time is mandatory for segments.
            dwell_time_asc = segment_details.get("dwell_time_asc", None)
            if type(dwell_time_asc) is not int or not (
                self.__minimum_duration <= dwell_time_asc <= self.__maximum_duration
            ):
                raise ValueError(
                    f"Segment dwell_time_asc must be number in range {self.__minimum_duration}-{self.__maximum_duration}"
                )
            dwell_time_desc = segment_details.get("dwell_time_desc", None)
            if type(dwell_time_desc) is not int or not (
                self.__minimum_duration <= dwell_time_desc <= self.__maximum_duration
            ):
                raise ValueError(
                    f"Segment dwell_time_desc must be number in range {self.__minimum_duration}-{self.__maximum_duration}"
                )

            is_ascending: bool = SingaporeStation.to_station_code_components(
                start
            ) < SingaporeStation.to_station_code_components(end)

            edge = (
                duration_asc if is_ascending else duration_desc,
                edge_type,
                mode,
                dwell_time_asc if is_ascending else dwell_time_desc,
            )
            self._graph.add_edge(start, end, edge)
            if mode != "walk":
                self._graph_without_walk_segments.add_edge(start, end, edge)

            edge = (
                duration_desc if is_ascending else duration_asc,
                edge_type,
                mode,
                dwell_time_desc if is_ascending else dwell_time_asc,
            )
            self._graph.add_edge(end, start, edge)
            if mode != "walk":
                self._graph_without_walk_segments.add_edge(end, start, edge)

        self.__add_interchange_transfers()

    def __add_interchange_transfers(self):
        interchanges = SingaporeStation.get_interchanges(
            list(self.station_code_to_station.values())
        )
        for interchange_substations in (
            interchanges
        ):  # Link up unique pairs of substations on the same interchange station.
            for start, end in itertools.permutations(
                sorted(interchange_substations, key=SingaporeStation.sort_key), 2
            ):
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
                dwell_time_asc = 0  # Transfers have no dwell time.
                dwell_time_desc = 0  # Transfers have no dwell time.

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
        """Setup rail network graph from network config file.

        Args:
            network_path (pathlib.Path): Path to network config file.
            coordinates_path (pathlib.Path): Path to station coordinates file.

        Returns:
            RailGraph: Rail network graph.
        """

        return cls(*Config.parse_network_config(network_path, coordinates_path))

    def _cost_func(self, start: str, end: str) -> typing.Callable[..., int]:
        def cost_func_aux(
            current_station: str,
            next_station: str,
            edge_to_next_station: tuple,
            edge_to_current_station: tuple | None,
        ) -> int:
            """Compute time cost of travelling from current station to next station.

            Transfer time is added if the preceding and succeeding edge types imply a conditional interchange transfer.

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
                next_edge_duration,
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

            cost = next_edge_duration
            if (
                next_edge_mode == "walk"
            ):  # Walking away from station -> Not waiting for train to depart.
                dwell_time = 0

            cost += self.conditional_transfers.get(previous_edge_type, dict()).get(
                next_edge_type, 0
            )

            if current_station == start or next_station == end:
                if (
                    (current_station, next_station) in self.transfers
                ):  # Exclude transfer time for transfers at start or end of journey.
                    cost -= next_edge_duration
                    if (
                        next_station == end
                    ):  # Exclude dwell time for transfer at end of journey.
                        dwell_time = 0

            return cost + dwell_time

        return cost_func_aux

    def find_shortest_path(
        self,
        start_station_code: str,
        end_station_code: str,
        walk: bool = False,
    ) -> PathInfo:
        """Find shortest path between 2 stations `start` and `end`.

        Pseudo station codes are considered invalid.

        Args:
            start_station_code (str): Station code of station to start from.
            end_station_code (str): Station code of station to arrive at.
            walk (bool): Allow station transfers by walking.

        Raises:
            ValueError: Invalid station code.

        Returns:
            PathInfo: Shortest path between 2 stations `start` and `end`.
        """
        for station_code in (start_station_code, end_station_code):
            station = self.station_code_to_station.get(station_code, None)
            if station is None:
                raise ValueError(f"Station code not found: {station_code}")
            if station.has_pseudo_station_code:
                raise ValueError(f"Station code pseudonym not allowed: {station_code}")

        pathinfo = find_path(
            self._graph if walk else self._graph_without_walk_segments,
            start_station_code,
            end_station_code,
            cost_func=self._cost_func(start_station_code, end_station_code),
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
            f"Start at {self.station_code_to_station[pathinfo.nodes[0]].full_station_name}"
        ]
        for edge_idx, (
            current_station_code,
            next_station_code,
            edge_details,
        ) in enumerate(zip(pathinfo.nodes[:-1], pathinfo.nodes[1:], pathinfo.edges)):
            current_station = self.station_code_to_station[current_station_code]
            next_station = self.station_code_to_station[next_station_code]
            at_pseudo_station = (
                current_station.has_pseudo_station_code
                or next_station.has_pseudo_station_code
            )
            current_station_full_name = current_station.full_station_name
            next_station_full_name = next_station.full_station_name

            def get_terminal_full_station_name() -> str | None:
                terminal_station: SingaporeStation | None = (
                    self.station_code_to_station.get(
                        Terminal.get_approaching_terminal(
                            self._graph,
                            self.non_linear_line_terminals,
                            current_station_code,
                            next_station_code,
                        ),
                        None,
                    )
                )
                return (
                    None
                    if terminal_station is None
                    else terminal_station.full_station_name
                )

            if status == "walking":
                if edge_details[2] == "walk":  # Walk to the next station.
                    # Replace previous walking step with this walking step, effectively merging both steps into one step.
                    # Instead of A -> walk -> B -> walk -> C, do A -> walk -> C instead.
                    steps.pop()
                    steps.append(f"Walk to {next_station_full_name}")
                    status = "walking"
                else:
                    terminal_full_station_name: str | None = (
                        get_terminal_full_station_name()
                    )
                    steps.append(
                        f"Board train in direction of {next_station_full_name}"  # Non linear line. Use next station instead.
                        if terminal_full_station_name is None
                        else f"Board train towards terminus {terminal_full_station_name}"
                    )
                    status = "in_train"
            elif status == "at_station":
                if (
                    current_station_code,
                    next_station_code,
                ) in self.transfers:  # Interchange transfer.
                    steps.append(
                        f"{'Switch over at' if at_pseudo_station else 'Transfer to'} {next_station_full_name}"
                    )
                elif edge_details[2] == "walk":  # Walk to the next station.
                    steps.append(f"Walk to {next_station_full_name}")
                    status = "walking"
                elif (
                    0 < edge_idx
                    and self.conditional_transfers.get(
                        pathinfo.edges[edge_idx - 1][1], dict()
                    ).get(pathinfo.edges[edge_idx][1], None)
                    is not None
                ):  # Conditional interchange transfer
                    raise RuntimeError(
                        "Something is not right; conditional interchange transfers should not be interchange transfers. "
                        "Check ConditionalInterchange class and rail network structure. PathInfo: %s"
                        % pathinfo
                    )
                else:  # Board a train.
                    terminal_full_station_name: str | None = (
                        get_terminal_full_station_name()
                    )
                    steps.append(
                        f"Board train in direction of {next_station_full_name}"  # Non linear line. Use next station instead.
                        if terminal_full_station_name is None
                        else f"Board train towards terminus {terminal_full_station_name}"
                    )
                    status = "in_train"
            elif status == "in_train":
                if (
                    current_station_code,
                    next_station_code,
                ) in self.transfers:  # Interchange transfer.
                    steps.append(f"Alight at {current_station_full_name}")
                    steps.append(
                        f"{'Switch over at' if at_pseudo_station else 'Transfer to'} {next_station_full_name}"
                    )
                    status = "at_station"
                elif edge_details[2] == "walk":  # Walk to the next station.
                    steps.append(f"Alight at {current_station_full_name}")
                    steps.append(f"Walk to {next_station_full_name}")
                    status = "walking"
                elif (
                    0 < edge_idx
                    and self.conditional_transfers.get(
                        pathinfo.edges[edge_idx - 1][1], dict()
                    ).get(pathinfo.edges[edge_idx][1], None)
                    is not None
                ):  # Conditional interchange transfer
                    steps.append(f"Switch over at {current_station_full_name}")
                    terminal_full_station_name: str | None = (
                        get_terminal_full_station_name()
                    )
                    steps.append(
                        f"Board train in direction of {next_station_full_name}"  # Non linear line. Use next station instead.
                        if terminal_full_station_name is None
                        else f"Board train towards terminus {terminal_full_station_name}"
                    )
                    status = "in_train"
        if steps and steps[-1].startswith("Switch over"):
            steps.pop()  # Special case: Final edge is interchange transfer from pseudo station code like JE0 -> JS3.
        if status == "in_train":
            steps.append(f"Alight at {next_station_full_name}")
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
        haversine_distance: float = Coordinates.haversine_distance(
            self.station_coordinates[nodes[0]], self.station_coordinates[nodes[-1]]
        )
        path_distance: float = sum(
            Coordinates.haversine_distance(
                self.station_coordinates[current_node],
                self.station_coordinates[next_node],
            )
            for current_node, next_node in zip(nodes[:-1], nodes[1:])
        )

        logger.info(
            "Approximate path distance: %.3f km, Haversine distance: %.3f km, Circuity ratio: %.2f",
            path_distance / 1000,
            haversine_distance / 1000,
            (path_distance / haversine_distance) if haversine_distance > 0 else 1,
        )
        return path_distance, haversine_distance
