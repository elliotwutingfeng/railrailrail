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

import pathlib
import math
import pytest
import tomllib
from dijkstar.algorithm import NoPathError, PathInfo

from railrailrail.railgraph import RailGraph


class TestRailGraph:
    def setup_method(self):
        coordinates_path = (
            pathlib.Path(__file__).resolve().parent / "test_station_coordinates.csv"
        )
        with open(
            pathlib.Path(__file__).resolve().parent / "test_trips.toml", "rb"
        ) as f:
            self.trips: dict = tomllib.load(f)
        for trip in self.trips:
            network_path = (
                pathlib.Path(__file__).resolve().parent
                / f"test_network_{self.trips[trip]["input"]["network"]}.toml"
            )
            self.trips[trip]["rail_graph"] = RailGraph.from_file(
                network_path, coordinates_path
            )
            self.trips[trip]["pathinfo"] = PathInfo(
                nodes=self.trips[trip]["output"]["nodes"],
                edges=list(map(tuple, self.trips[trip]["output"]["edges"])),
                costs=self.trips[trip]["output"]["costs"],
                total_cost=self.trips[trip]["output"]["total_cost"],
            )

        self.single_node_path = PathInfo(nodes=[""], edges=[], costs=[], total_cost=0)

    def test_init(self):
        with pytest.raises(ValueError):
            RailGraph(
                edges=[],
                stations=dict(),
                station_coordinates=dict(),
                transfer_time="",
                dwell_time="",
            )
        with pytest.raises(ValueError):
            RailGraph(
                edges=[],
                stations=dict(),
                station_coordinates=dict(),
                transfer_time=0,
                dwell_time="",
            )
        with pytest.raises(ValueError):
            RailGraph(
                edges=[],
                stations=dict(),
                station_coordinates=dict(),
                transfer_time=0,
                dwell_time=0,
            )
        with pytest.raises(ValueError):
            RailGraph(
                edges=[],
                stations={"EX1": ["Easy"]},
                station_coordinates=dict(),
                transfer_time=0,
                dwell_time=0,
            )
        with pytest.raises(ValueError):
            RailGraph(
                edges=[
                    ("EX1", "HX1", {"duration": 20}),
                ],
                stations={"EX1": "Easy", "HX1": "How"},
                station_coordinates=dict(),
                transfer_time=0,
                dwell_time=0,
            )

    def test_find_shortest_path(self):
        for trip, trip_details in self.trips.items():
            rail_graph = trip_details["rail_graph"]
            start = trip_details["input"]["start"]
            end = trip_details["input"]["end"]
            walk = trip_details["input"]["walk"]
            expected_pathinfo = trip_details["pathinfo"]

            actual_pathinfo = rail_graph.find_shortest_path(start, end, walk)
            assert (
                expected_pathinfo.nodes == actual_pathinfo.nodes
            ), f"{start}-{end} | Expected {expected_pathinfo.nodes}. Got {actual_pathinfo.nodes}."

            assert (  # TODO Edges may contain floats. Use math.isclose for float elements.
                expected_pathinfo.edges == actual_pathinfo.edges
            ), f"{start}-{end} | Expected {expected_pathinfo.edges}. Got {actual_pathinfo.edges}."

            assert (
                len(expected_pathinfo.costs) == len(actual_pathinfo.costs)
                and all(
                    math.isclose(a, b, rel_tol=0.01)
                    for (a, b) in zip(expected_pathinfo.costs, actual_pathinfo.costs)
                )
            ), f"{start}-{end} | Expected {expected_pathinfo.costs}. Got {actual_pathinfo.costs}."

            assert math.isclose(
                expected_pathinfo.total_cost,
                actual_pathinfo.total_cost,
                rel_tol=0.01,
            ), f"{start}-{end} | Expected {expected_pathinfo.total_cost}. Got {actual_pathinfo.total_cost}."

            with pytest.raises(NoPathError):
                rail_graph.find_shortest_path("AA", "BB")

    def test_make_directions(self):
        for trip, trip_details in self.trips.items():
            start = trip_details["input"]["start"]
            end = trip_details["input"]["end"]
            rail_graph = trip_details["rail_graph"]

            actual_directions = rail_graph.make_directions(trip_details["pathinfo"])
            assert (
                trip_details["output"]["directions"] == actual_directions
            ), f"{start}-{end} | Wrong directions."

            # At least 2 stations needed for journey.
            with pytest.raises(ValueError):
                rail_graph.make_directions(self.single_node_path)

    def test_path_and_haversine_distance(self):
        for trip, trip_details in self.trips.items():
            start = trip_details["input"]["start"]
            end = trip_details["input"]["end"]
            rail_graph = trip_details["rail_graph"]

            expected = (
                trip_details["output"]["path_distance"],
                trip_details["output"]["haversine_distance"],
            )
            actual = rail_graph.path_and_haversine_distance(trip_details["pathinfo"])
            assert all(
                math.isclose(p[0], p[1], rel_tol=0.01) for p in zip(expected, actual)
            ), f"{start}-{end} | Expected {expected}. Got {actual}."

            # At least 2 stations needed for journey.
            with pytest.raises(ValueError):
                rail_graph.path_and_haversine_distance(self.single_node_path)
