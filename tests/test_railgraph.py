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
import re
import pytest
import tomllib
import tomlkit
from dijkstar.algorithm import PathInfo, NoPathError

from railrailrail.railgraph import RailGraph


class TestRailGraph:
    def setup_method(self):
        parent_path: pathlib.Path = pathlib.Path(__file__).resolve().parent

        test_coordinates_path = (
            parent_path.parent / "config_examples" / "station_coordinates.csv"
        )

        with open(parent_path / "test_trips.toml", "rb") as f:
            self.trips: dict = tomllib.load(f)
        for trip in self.trips:
            test_network_path = (
                parent_path.parent
                / "config_examples"
                / f"network_{self.trips[trip]["input"]["network"]}.toml"
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

    @pytest.mark.parametrize(
        (
            "segments,transfers,conditional_transfers,non_linear_line_terminals,"
            "station_code_pseudonyms,stations,station_coordinates,match"
        ),
        [
            (
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                "stations must be non-empty dict.",
            ),
            (
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                {"EX1": ["Easy"]},
                dict(),
                "stations must be dict[str, str]",
            ),
            (
                {
                    ("EX1", "HX1"): {
                        "duration_asc": 999999,
                        "duration_desc": 999999,
                        "dwell_time_asc": 999999,
                        "dwell_time_desc": 999999,
                    }
                },
                dict(),
                dict(),
                dict(),
                dict(),
                {"EX1": "Easy", "HX1": "How"},
                dict(),
                "Segment duration_asc must be number in range 0-3600",
            ),
            (
                {
                    ("EX1", "HX1"): {
                        "duration_asc": 0,
                        "duration_desc": 999999,
                        "dwell_time_asc": 999999,
                        "dwell_time_desc": 999999,
                    }
                },
                dict(),
                dict(),
                dict(),
                dict(),
                {"EX1": "Easy", "HX1": "How"},
                dict(),
                "Segment duration_desc must be number in range 0-3600",
            ),
            (
                {
                    ("EX1", "HX1"): {
                        "duration_asc": 0,
                        "duration_desc": 0,
                        "dwell_time_asc": 999999,
                        "dwell_time_desc": 999999,
                    }
                },
                dict(),
                dict(),
                dict(),
                dict(),
                {"EX1": "Easy", "HX1": "How"},
                dict(),
                "Segment dwell_time_asc must be number in range 0-3600",
            ),
            (
                {
                    ("EX1", "HX1"): {
                        "duration_asc": 0,
                        "duration_desc": 0,
                        "dwell_time_asc": 0,
                        "dwell_time_desc": 999999,
                    }
                },
                dict(),
                dict(),
                dict(),
                dict(),
                {"EX1": "Easy", "HX1": "How"},
                dict(),
                "Segment dwell_time_desc must be number in range 0-3600",
            ),
            (
                {
                    ("EX1", "HX1"): {
                        "duration_asc": 0,
                        "duration_desc": 0,
                        "dwell_time_asc": 0,
                        "dwell_time_desc": 0,
                    },
                    ("EX1", "GX1"): {
                        "duration_asc": 0,
                        "duration_desc": 0,
                        "dwell_time_asc": 0,
                        "dwell_time_desc": 0,
                    },
                },
                dict(),
                dict(),
                dict(),
                dict(),
                {"EX1": "Easy", "HX1": "How"},
                dict(),
                "Station GX1 in segment EX1-GX1 does not have a name.",
            ),
            (
                {
                    ("EX1", "GX1"): {
                        "duration_asc": 0,
                        "duration_desc": 0,
                        "dwell_time_asc": 0,
                        "dwell_time_desc": 0,
                    },
                },
                dict(),
                dict(),
                dict(),
                dict(),
                {"EX1": "Easy", "HX1": "How", "GX1": "How", "KX1": "Get"},
                dict(),
                "GX1-HX1 not found in [transfers].",
            ),
        ],
    )
    def test_init(
        self,
        segments,
        transfers,
        conditional_transfers,
        non_linear_line_terminals,
        station_code_pseudonyms,
        stations,
        station_coordinates,
        match,
    ):
        with pytest.raises(ValueError, match=re.escape(match)):
            RailGraph(
                segments,
                transfers,
                conditional_transfers,
                non_linear_line_terminals,
                station_code_pseudonyms,
                stations,
                station_coordinates,
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


def __generate_test_trips():  # pragma: no cover
    """Helper function to re-generate test trips for test_trips.toml

    Generated test cases are printed to stdout.
    """
    parent_path: pathlib.Path = pathlib.Path(__file__).resolve().parent

    with open(parent_path / "test_trips.toml", "rb") as f:
        trips = tomllib.load(f)

    data_ = dict()
    for trip, trip_details in trips.items():
        network = trip_details["input"]["network"]
        start = trip_details["input"]["start"]
        end = trip_details["input"]["end"]
        walk = trip_details["input"]["walk"]
        rail_graph = RailGraph.from_file(
            parent_path.parent / "config_examples" / f"network_{network}.toml",
            parent_path.parent / "config_examples" / "station_coordinates.csv",
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
    __generate_test_trips()  # Run this file `test_railgraph.py` to print updated test cases to stdout.
