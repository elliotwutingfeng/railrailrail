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
import pathlib
import tomllib
from collections import defaultdict
from itertools import combinations

from dijkstar import Graph, find_path
from dijkstar.algorithm import PathInfo

from railrailrail.dataset import SemiInterchange, Terminal
from railrailrail.logger import logger
from railrailrail.utils import GeographicUtils, StationUtils


class RailGraph:
    """Graph for calculating shortest route and time cost between any 2 stations."""

    def __init__(
        self,
        edges: list[tuple[str, str, dict]],
        stations: dict[str, str],
        station_coordinates: dict,
        transfer_time: float | int = 7.0,
        dwell_time: float | int = 1.0,
    ) -> None:
        """Setup rail network graph

        Args:
            edges (list[tuple[str, str, dict]]): Duration between every adjacent pair of stations from the same line.
            stations (dict[str, str]): Map of station codes to station names.
            transfer_time (float | int, optional): Time taken to switch lines at an interchange station. Defaults to 7.0.
            dwell_time (float | int, optional): Time taken by train to either drop off
            or pick up passengers at a station. Defaults to 1.0.

        Raises:
            ValueError: A station cannot belong to more than one interchange.
        """
        if type(transfer_time) not in (float, int) or float(transfer_time) < 0:
            raise ValueError("transfer_time must be non-negative float|int.")
        if type(dwell_time) not in (float, int) or float(dwell_time) < 0:
            raise ValueError("dwell_time must be non-negative float|int.")
        if not isinstance(stations, dict) or not stations:
            raise ValueError("stations must be dict and not empty.")
        for k, v in stations.items():
            if type(k) is not str or type(v) is not str:
                raise ValueError("stations must be dict[str, str]")

        self.transfer_time = transfer_time
        self.dwell_time = dwell_time
        self._stations = stations
        self._station_coordinates = station_coordinates

        aggregator: defaultdict[str, set[str]] = defaultdict(set)
        for station_code, station_name in self._stations.items():
            aggregator[station_name].add(station_code)
        self._interchanges: tuple[set[str]] = tuple(
            station_codes
            for station_codes in aggregator.values()
            if len(station_codes) >= 2
        )
        if sum(map(len, self._interchanges)) != len(set().union(*self._interchanges)):
            raise ValueError("A station cannot belong to more than one interchange.")

        # Undirected Graph allows for different time cost when moving in opposite direction.
        self._graph = Graph(undirected=False)
        self._graph_without_walk = Graph(undirected=False)

        for edge in edges:
            start, end, edge_details = edge
            duration = edge_details.get("duration", None)
            if (type(duration) not in (float, int)) or not (1 <= float(duration) <= 19):
                raise ValueError("duration must be number in range 1-19")
            edge_type = edge_details.get("edge_type", "")
            mode = edge_details.get("mode", "")
            edge = (duration, edge_type, mode)
            for u, v in [(start, end), (end, start)]:
                self._graph.add_edge(u, v, edge)
                if mode != "walk":
                    self._graph_without_walk.add_edge(u, v, edge)

        for (
            interchange_substations
        ) in (
            self._interchanges
        ):  # Link up unique pairs of substations on the same interchange station.
            for start, end in combinations(interchange_substations, 2):
                self._graph.add_edge(start, end, (transfer_time, "", ""))
                self._graph.add_edge(end, start, (transfer_time, "", ""))
                self._graph_without_walk.add_edge(start, end, (transfer_time, "", ""))
                self._graph_without_walk.add_edge(end, start, (transfer_time, "", ""))

    @classmethod
    def from_file(cls, network_path: pathlib.Path, coordinates_path: pathlib.Path):
        with open(network_path, "rb") as f:
            network = tomllib.load(f)

        stations = network.get("stations", None)
        if not isinstance(stations, dict) or not stations:
            raise ValueError("Invalid config file: 'stations' must not be empty.")
        transfer_time = network.get("transfer_time", None)
        if type(transfer_time) not in (float, int):
            raise ValueError("Invalid config file: 'transfer_time' must be float|int.")
        dwell_time = network.get("dwell_time", None)
        if type(dwell_time) not in (float, int):
            raise ValueError("Invalid config file: 'dwell_time'  must be float|int.")
        edges = network.get("edges", None)
        if not isinstance(edges, dict) or not edges:
            raise ValueError("Invalid config file: 'edges' must not be empty.")

        edges_: list[tuple[str, str, dict]] = []
        for edge, edge_details in edges.items():
            vertices = edge.split("-", 2)
            if len(vertices) != 2:
                raise ValueError(
                    f"Invalid config file: Edge must be in format 'AB1-AB2'. Got {edge}."
                )
            start, end = vertices[0], vertices[1]
            if not isinstance(edge_details, dict):
                raise ValueError("Invalid config file: Edge details must be a dict.")
            edges_.append((start, end, edge_details))

        station_coordinates = dict()
        with open(coordinates_path, "r") as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            for row in csv_reader:
                station_coordinates[row[0]] = (float(row[2]), float(row[3]))

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
            edges_,
            stations,
            station_coordinates,
            float(transfer_time),
            float(dwell_time),
        )

    def _cost_func(
        self,
        current_station: str,
        next_station: str,
        edge_to_next_station: tuple,
        edge_to_current_station: tuple,
    ) -> float:
        """Compute time cost of travelling from current station to next station. This cost is
        dynamically adjusted to include additional `self.transfer_time` if the preceding
        and succeeding edges imply a sub-interchange transfer. `self.dwell_time` is always added.

        Args:
            current_station (str): Not used.
            next_station (str): Not used.
            edge_to_next_station (tuple): Edge to next station.
            edge_to_current_station (tuple): Edge to current station.

        Returns:
            float: Time cost in minutes.
        """
        next_travel_time, next_edge_type, next_edge_mode = edge_to_next_station
        if isinstance(edge_to_current_station, tuple):
            previous_edge_type, previous_edge_mode = (
                edge_to_current_station[1],
                edge_to_current_station[2],
            )
        else:
            previous_edge_type, previous_edge_mode = "", ""

        cost = next_travel_time + self.dwell_time
        if SemiInterchange.is_semi_interchange_transfer(
            previous_edge_type, next_edge_type
        ):
            cost += self.transfer_time
        return cost

    def find_shortest_path(
        self,
        start: str,
        end: str,
        walk: bool = False,
    ) -> PathInfo:
        """Find shortest path between 2 stations `start` and `end`. Excludes extraneous
        `self.transfer_time` and `self.dwell_time` if the journey starts and/or ends
        at interchange stations.

        Args:
            start (str): Station code of station to board from.
            end (str): Station code of station to alight from.
            walk (bool): Allow station transfers by walking.

        Returns:
            PathInfo: `dijkstar.algorithm.PathInfo` modified with timings modified for
            journeys that start and/or end at interchange stations.
        """
        pathinfo = find_path(
            graph=self._graph if walk else self._graph_without_walk,
            s=start,
            d=end,
            cost_func=self._cost_func,
        )
        # Subtract `self.transfer_time` and `self.dwell_time` for interchange stations
        # visited at either start or end of journey.
        first_2_stations: set[str | None] = {None}
        last_2_stations: set[str | None] = {None}
        if len(pathinfo.nodes) >= 2:
            first_2_stations = {pathinfo.nodes[0], pathinfo.nodes[1]}
            last_2_stations = {pathinfo.nodes[-2], pathinfo.nodes[-1]}
        if any(
            last_2_stations.issubset(interchange) for interchange in self._interchanges
        ):
            pathinfo.costs[-1] -= self.transfer_time + self.dwell_time
            pathinfo.edges[-1] = (
                pathinfo.edges[-1][0] - self.transfer_time,
                pathinfo.edges[-1][1],
            )
            pathinfo = pathinfo._replace(
                total_cost=pathinfo.total_cost - self.transfer_time - self.dwell_time
            )
        if len(pathinfo.nodes) == 2:
            return pathinfo
        if any(
            first_2_stations.issubset(interchange) for interchange in self._interchanges
        ):
            pathinfo.costs[0] -= self.transfer_time + self.dwell_time
            pathinfo.edges[0] = (
                pathinfo.edges[0][0] - self.transfer_time,
                pathinfo.edges[0][1],
            )
            pathinfo = pathinfo._replace(
                total_cost=pathinfo.total_cost - self.transfer_time - self.dwell_time
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
            f"Start at {pathinfo.nodes[0]} {self._stations[pathinfo.nodes[0]]}"
        ]
        for edge_idx, (u, v, edge_details) in enumerate(
            zip(pathinfo.nodes[:-1], pathinfo.nodes[1:], pathinfo.edges)
        ):
            u_is_pseudo_station_code = (
                StationUtils.to_station_code_components(u)[1] == 0
            )
            v_is_pseudo_station_code = (
                StationUtils.to_station_code_components(v)[1] == 0
            )
            at_pseudo_station = u_is_pseudo_station_code or v_is_pseudo_station_code
            u_ = v if u_is_pseudo_station_code else u
            v_ = u if v_is_pseudo_station_code else v
            if status == "at_station":
                if any(
                    {u, v}.issubset(a) for a in self._interchanges
                ):  # Interchange transfer.
                    if at_pseudo_station:
                        steps.append(f"Switch over at {v_} {self._stations[v_]}")
                    else:
                        steps.append(f"Transfer to {v_} {self._stations[v_]}")
                elif edge_details[2] == "walk":  # Walk to the next station.
                    steps.append(f"Alight at {u_} {self._stations[u_]}")
                    steps.append(f"Walk to {v_} {self._stations[v_]}")
                    status = "walking"
                elif edge_idx < len(
                    pathinfo.edges
                ) and SemiInterchange.is_semi_interchange_transfer(
                    pathinfo.edges[edge_idx - 1][1], pathinfo.edges[edge_idx][1]
                ):  # Semi-interchange transfer
                    steps.append(f"Switch over at {u_} {self._stations[u_]}")
                    steps.append(f"Board train towards {v_} {self._stations[v_]}")
                    status = "in_train"
                else:  # Board a train.
                    terminal: str | None = Terminal.get_terminal(self._graph, u, v)
                    steps.append(
                        f"Board train towards {v_} {self._stations[v_]}"  # Unusual terminal.
                        if terminal is None
                        else f"Board train towards {Terminal.terminals_with_pseudo_station_codes.get(terminal, terminal)} {self._stations[terminal]}"
                    )
                    status = "in_train"
            elif status == "in_train":
                if any(
                    {u, v}.issubset(a) for a in self._interchanges
                ):  # Interchange transfer.
                    steps.append(f"Alight at {u_} {self._stations[u_]}")
                    if at_pseudo_station:
                        steps.append(f"Switch over at {v_} {self._stations[v_]}")
                    else:
                        steps.append(f"Transfer to {v_} {self._stations[v_]}")
                    status = "at_station"
                elif edge_details[2] == "walk":  # Walk to the next station.
                    steps.append(f"Alight at {u_} {self._stations[u_]}")
                    steps.append(f"Walk to {v_} {self._stations[v_]}")
                    status = "walking"
                elif edge_idx < len(
                    pathinfo.edges
                ) and SemiInterchange.is_semi_interchange_transfer(
                    pathinfo.edges[edge_idx - 1][1], pathinfo.edges[edge_idx][1]
                ):  # Semi-interchange transfer
                    steps.append(f"Switch over at {u_} {self._stations[u_]}")
                    steps.append(f"Board train towards {v_} {self._stations[v_]}")
                    status = "in_train"
            elif status == "walking":
                steps.append(f"Board train towards {v_} {self._stations[v_]}")
                status = "in_train"
        if status == "in_train":
            steps.append(f"Alight at {v_} {self._stations[v_]}")
        steps.append(
            f"""Total duration: {
                int(pathinfo.total_cost)
                if pathinfo.total_cost == int(pathinfo.total_cost)
                else int(pathinfo.total_cost) + 1} minutes"""
        )
        path_distance, haversine_distance = self.path_and_haversine_distance(pathinfo)
        steps.append(
            f"Approximate path distance: {path_distance/ 1000 :.1f} km, "
            f"Haversine distance: {haversine_distance / 1000 :.1f} km, "
            f"Circuity ratio: {(path_distance / haversine_distance ) if haversine_distance > 0 else 1 :.1f}"
        )
        return steps

    def path_and_haversine_distance(self, pathinfo: PathInfo):
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
