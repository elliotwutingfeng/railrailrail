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

import math
import pathlib
import unittest

import pytest
from dijkstar.algorithm import NoPathError, PathInfo

from railrailrail.railgraph import RailGraph


class TestRailGraph(unittest.TestCase):
    def setUp(self):
        network_path = (
            pathlib.Path(__file__).resolve().parent.parent
            / "config"
            / "network_tel_4.toml"
        )
        network_path.parent.mkdir(parents=True, exist_ok=True)

        coordinates_path = (
            pathlib.Path(__file__).resolve().parent.parent
            / "config"
            / "station_coordinates.csv"
        )
        self.rail_graph = RailGraph.from_file(network_path, coordinates_path)

        self.rail_graph.transfer_time = 7
        self.rail_graph.dwell_time = 0.5
        self.test_trips = (
            {
                "start": "TE26",
                "end": "NE14",
                "walk": False,
                "pathinfo": PathInfo(
                    nodes=[
                        "TE26",
                        "TE25",
                        "TE24",
                        "TE23",
                        "TE22",
                        "TE20",
                        "TE19",
                        "TE18",
                        "TE17",
                        "NE3",
                        "NE4",
                        "NE5",
                        "NE6",
                        "NE7",
                        "NE8",
                        "NE9",
                        "NE10",
                        "NE11",
                        "NE12",
                        "NE13",
                        "NE14",
                    ],
                    edges=[
                        (1, "", ""),
                        (3, "", ""),
                        (2, "", ""),
                        (4, "", ""),
                        (3, "", ""),
                        (2, "", ""),
                        (1, "", ""),
                        (2, "", ""),
                        (7.0, "", ""),
                        (1, "", ""),
                        (2, "", ""),
                        (3, "", ""),
                        (1, "", ""),
                        (1, "", ""),
                        (2, "", ""),
                        (3, "", ""),
                        (1, "", ""),
                        (2, "", ""),
                        (3, "", ""),
                        (2, "", ""),
                    ],
                    costs=[
                        1.5,
                        3.5,
                        2.5,
                        4.5,
                        3.5,
                        2.5,
                        1.5,
                        2.5,
                        7.5,
                        1.5,
                        2.5,
                        3.5,
                        1.5,
                        1.5,
                        2.5,
                        3.5,
                        1.5,
                        2.5,
                        3.5,
                        2.5,
                    ],
                    total_cost=56.0,
                ),
                "path_and_haversine_distance": (21589.336417276852, 7766.81178008197),
                "directions": [
                    "Start at TE26 Marine Parade",
                    "Board train towards terminus TE1 Woodlands North",
                    "Alight at TE17 Outram Park",
                    "Transfer to NE3 Outram Park",
                    "Board train towards terminus NE17 Punggol",
                    "Alight at NE14 Hougang",
                    "Total duration: 56 minutes",
                    "Approximate path distance: 21.6 km, Haversine distance: 7.8 km, Circuity ratio: 2.8",
                ],
            },
            {
                "start": "CG1",
                "end": "BP10",
                "walk": True,
                "pathinfo": PathInfo(
                    nodes=[
                        "CG1",
                        "CG",
                        "EW4",
                        "EW5",
                        "EW6",
                        "EW7",
                        "EW8",
                        "EW9",
                        "EW10",
                        "EW11",
                        "EW12",
                        "DT14",
                        "DT13",
                        "DT12",
                        "DT11",
                        "DT10",
                        "DT9",
                        "DT8",
                        "DT7",
                        "DT6",
                        "DT5",
                        "DT3",
                        "DT2",
                        "DT1",
                        "BP6",
                        "BP7",
                        "BP8",
                        "BP9",
                        "BP10",
                    ],
                    edges=[
                        (3, "", ""),
                        (7.0, "", ""),
                        (3, "", ""),
                        (3, "", ""),
                        (3, "", ""),
                        (2, "", ""),
                        (2, "", ""),
                        (3, "", ""),
                        (2, "", ""),
                        (3, "", ""),
                        (7.0, "", ""),
                        (2, "", ""),
                        (1, "", ""),
                        (3, "", ""),
                        (2, "", ""),
                        (2, "", ""),
                        (2, "", ""),
                        (2, "", ""),
                        (2, "", ""),
                        (2, "", ""),
                        (3, "", ""),
                        (2, "", ""),
                        (2, "", ""),
                        (7.0, "", ""),
                        (1, "bukit_panjang_service_b", ""),
                        (2, "", ""),
                        (1, "", ""),
                        (2, "", ""),
                    ],
                    costs=[
                        3.5,
                        7.5,
                        3.5,
                        3.5,
                        3.5,
                        2.5,
                        2.5,
                        3.5,
                        2.5,
                        3.5,
                        7.5,
                        2.5,
                        1.5,
                        3.5,
                        2.5,
                        2.5,
                        2.5,
                        2.5,
                        2.5,
                        2.5,
                        3.5,
                        2.5,
                        2.5,
                        7.5,
                        1.5,
                        2.5,
                        1.5,
                        2.5,
                    ],
                    total_cost=90.0,
                ),
                "path_and_haversine_distance": (29733.464784303258, 21919.188739992347),
                "directions": [
                    "Start at CG1 Expo",
                    "Board train towards terminus CG Tanah Merah",
                    "Alight at CG Tanah Merah",
                    "Switch over at EW4 Tanah Merah",
                    "Board train towards terminus EW33 Tuas Link",
                    "Alight at EW12 Bugis",
                    "Transfer to DT14 Bugis",
                    "Board train towards terminus DT1 Bukit Panjang",
                    "Alight at DT1 Bukit Panjang",
                    "Transfer to BP6 Bukit Panjang",
                    "Board train in direction of BP7 Petir",
                    "Alight at BP10 Fajar",
                    "Total duration: 90 minutes",
                    "Approximate path distance: 29.7 km, Haversine distance: 21.9 km, Circuity ratio: 1.4",
                ],
            },
        )

        self.single_node_path = PathInfo(nodes=[""], edges=[], costs=[], total_cost=0)

    def test_find_shortest_path(self):
        for trip in self.test_trips:
            pathinfo = self.rail_graph.find_shortest_path(
                trip["start"], trip["end"], trip["walk"]
            )
            assert pathinfo == trip["pathinfo"]  # Shallow comparison

        with pytest.raises(NoPathError):
            self.rail_graph.find_shortest_path("AA", "BB")

    def test_make_directions(self):
        for trip in self.test_trips:
            assert (
                self.rail_graph.make_directions(trip["pathinfo"]) == trip["directions"]
            )

        # At least 2 stations needed for journey.
        with pytest.raises(ValueError):
            self.rail_graph.make_directions(self.single_node_path)

    def test_path_and_haversine_distance(self):
        for trip in self.test_trips:
            expected = trip["path_and_haversine_distance"]
            actual = self.rail_graph.path_and_haversine_distance(trip["pathinfo"])
            assert all(
                math.isclose(p[0], p[1]) for p in zip(expected, actual)
            ), f"Expected {expected}. Got {actual}."

        # At least 2 stations needed for journey.
        with pytest.raises(ValueError):
            self.rail_graph.path_and_haversine_distance(self.single_node_path)
