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
import pandas as pd
import pytest
import tomllib
import tomlkit
import warnings
from dijkstar.algorithm import PathInfo, NoPathError

from railrailrail.railgraph import RailGraph


class TestRailGraph:
    def setup_method(self):
        coordinates_path = (
            pathlib.Path(__file__).resolve().parent.parent
            / "config"
            / "station_coordinates.csv"
        )

        test_coordinates_path = (
            pathlib.Path(__file__).resolve().parent / "test_station_coordinates.csv"
        )

        # Warn if content in coordinates_path and test_coordinates_path are different.
        # Different order of rows does not count as different.
        coordinates_csv = pd.read_csv(coordinates_path)
        coordinates_csv = coordinates_csv.sort_values(list(coordinates_csv.columns))
        test_coordinates_csv = pd.read_csv(test_coordinates_path)
        test_coordinates_csv = test_coordinates_csv.sort_values(
            list(test_coordinates_csv.columns)
        )

        if not coordinates_csv.equals(test_coordinates_csv):
            warnings.warn(
                "Coordinates file at %s is different from test coordinates file at %s"
                % (coordinates_path, test_coordinates_path)
            )

        with open(
            pathlib.Path(__file__).resolve().parent / "test_trips.toml", "rb"
        ) as f:
            self.trips: dict = tomllib.load(f)
        for trip in self.trips:
            test_network_path = (
                pathlib.Path(__file__).resolve().parent
                / f"test_network_{self.trips[trip]["input"]["network"]}.toml"
            )
            self.trips[trip]["rail_graph"] = RailGraph.from_file(
                test_network_path, test_coordinates_path
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
                segments=dict(),
                transfers=dict(),
                conditional_transfers=dict(),
                stations=dict(),
                station_coordinates=dict(),
                default_dwell_time="",
            )
        with pytest.raises(ValueError):
            RailGraph(
                segments=dict(),
                transfers=dict(),
                conditional_transfers=dict(),
                stations=dict(),
                station_coordinates=dict(),
                default_dwell_time="",
            )
        with pytest.raises(ValueError):
            RailGraph(
                segments=dict(),
                transfers=dict(),
                conditional_transfers=dict(),
                stations=dict(),
                station_coordinates=dict(),
                default_dwell_time=0,
            )
        with pytest.raises(ValueError):
            RailGraph(
                segments=dict(),
                transfers=dict(),
                conditional_transfers=dict(),
                stations={"EX1": ["Easy"]},
                station_coordinates=dict(),
                default_dwell_time=0,
            )
        with pytest.raises(ValueError):
            RailGraph(
                segments={("EX1", "HX1"): {"duration": 999999}},
                transfers=dict(),
                conditional_transfers=dict(),
                stations={"EX1": "Easy", "HX1": "How"},
                station_coordinates=dict(),
                default_dwell_time=0,
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

            assert (
                expected_pathinfo.edges == actual_pathinfo.edges
            ), f"{start}-{end} | Expected {expected_pathinfo.edges}. Got {actual_pathinfo.edges}."

            assert (
                expected_pathinfo.costs == actual_pathinfo.costs
            ), f"{start}-{end} | Expected {expected_pathinfo.costs}. Got {actual_pathinfo.costs}."

            assert (
                expected_pathinfo.total_cost == actual_pathinfo.total_cost
            ), f"{start}-{end} | Expected {expected_pathinfo.total_cost}. Got {actual_pathinfo.total_cost}."

            with pytest.raises(ValueError):
                rail_graph.find_shortest_path("AA1", "BB2")

            if trip_details["input"]["network"] == "sklrt_east_loop":
                with pytest.raises(NoPathError):
                    rail_graph.find_shortest_path(
                        "NS4", "SE5"
                    )  # Sengkang East Loop was isolated.

            if trip_details["input"]["network"] == "tel_4":
                with pytest.raises(ValueError):
                    rail_graph.find_shortest_path(
                        "EW6", "CE0Y"
                    )  # Sengkang East Loop was isolated.

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


def generate_test_trips():  # pragma: no cover
    """Helper function to re-generate test trips for test_trips.toml

    Generated test cases are printed to stdout.
    """

    with open(pathlib.Path(__file__).resolve().parent / "test_trips.toml", "rb") as f:
        trips = tomllib.load(f)

    data_ = dict()
    for trip, trip_details in trips.items():
        network = trip_details["input"]["network"]
        start = trip_details["input"]["start"]
        end = trip_details["input"]["end"]
        walk = trip_details["input"]["walk"]
        rail_graph = RailGraph.from_file(
            f"tests/test_network_{network}.toml", "tests/test_station_coordinates.csv"
        )
        pathinfo = rail_graph.find_shortest_path(start, end, walk)
        path_distance, haversine_distance = rail_graph.path_and_haversine_distance(
            pathinfo
        )
        data_[trip] = dict()
        data = data_[trip]
        data["nodes"] = pathinfo.nodes
        data["edges"] = pathinfo.edges
        data["costs"] = pathinfo.costs
        data["total_cost"] = pathinfo.total_cost
        data["path_distance"] = path_distance
        data["haversine_distance"] = haversine_distance
        data["directions"] = rail_graph.make_directions(pathinfo)

    rows = []
    for row in tomlkit.dumps(data_).split("\n"):
        if row.startswith("[trip_") and row.endswith("]"):
            row = row.removesuffix("]") + ".output]"
        rows.append(row)
    print("\n".join(rows))


if __name__ == "__main__":  # pragma: no cover
    generate_test_trips()  # Run this file `test_railgraph.py` to print updated test cases to stdout.
