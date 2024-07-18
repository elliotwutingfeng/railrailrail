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
            pathlib.Path(__file__).resolve().parent / "test_network_tel_4.toml"
        )
        coordinates_path = (
            pathlib.Path(__file__).resolve().parent / "test_station_coordinates.csv"
        )
        self.rail_graph = RailGraph.from_file(network_path, coordinates_path)

        self.test_trips_short = (
            {
                "start": "DT3",
                "end": "DT7",
                "walk": False,
                "total_cost": 8.5,
            },  # $ _ $ _ $
            {
                "start": "NS1",
                "end": "EW18",
                "walk": False,
                "total_cost": 20.5,
            },  # $ transfer $ _ $
            {
                "start": "NE8",
                "end": "CC13",
                "walk": False,
                "total_cost": 10.0,
            },  # $ _ $ transfer $
            {
                "start": "TE16",
                "end": "NS20",
                "walk": False,
                "total_cost": 18.5,
            },  # $ _ $ transfer $ _ $
            {
                "start": "CC3",
                "end": "CE2",
                "walk": False,
                "total_cost": 17.0,
            },  # $ _ $ semi-transfer $ _ $
            {
                "start": "BP7",
                "end": "BP13",
                "walk": False,
                "total_cost": 11.0,
            },  # $ _ $ semi-transfer $ _ $
            {
                "start": "SW1",
                "end": "SE1",
                "walk": False,
                "total_cost": 12.0,
            },  # $ _ $ semi-transfer $ _ $
            {
                "start": "PW1",
                "end": "PE1",
                "walk": False,
                "total_cost": 13.0,
            },  # $ _ $ semi-transfer $ _ $
            {
                "start": "DT21",
                "end": "CC3",
                "walk": True,
                "total_cost": 5.5,
            },  # $ walk $ _ $
            {
                "start": "EW13",
                "end": "DT18",
                "walk": True,
                "total_cost": 7.5,
            },  # $ _ $ walk $
            {
                "start": "DT23",
                "end": "CC3",
                "walk": True,
                "total_cost": 9.5,
            },  # $ _ $ walk $ _ $
            {
                "start": "NE5",
                "end": "CC2",
                "walk": True,
                "total_cost": 10.5,
            },  # $ _ $ walk $ walk $
        )
        self.test_trips_full = (
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
                        "DT35",
                        "DT34",
                        "DT33",
                        "DT32",
                        "DT31",
                        "DT30",
                        "DT29",
                        "DT28",
                        "DT27",
                        "DT26",
                        "DT25",
                        "DT24",
                        "DT23",
                        "DT22",
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
                        (7.0, "", ""),
                        (2, "", ""),
                        (3, "", ""),
                        (2, "", ""),
                        (2, "", ""),
                        (3, "", ""),
                        (2, "", ""),
                        (2, "", ""),
                        (2, "", ""),
                        (2, "", ""),
                        (2, "", ""),
                        (2, "", ""),
                        (2, "", ""),
                        (2, "", ""),
                        (5, "", "walk"),
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
                        0.5,
                        2.5,
                        3.5,
                        2.5,
                        2.5,
                        3.5,
                        2.5,
                        2.5,
                        2.5,
                        2.5,
                        2.5,
                        2.5,
                        2.5,
                        2.5,
                        5.0,
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
                    total_cost=84.0,
                ),
                "path_and_haversine_distance": (32547.57447742016, 21919.188739992347),
                "directions": [
                    "Start at CG1 Expo",
                    "Transfer to DT35 Expo",
                    "Board train towards terminus DT1 Bukit Panjang",
                    "Alight at DT22 Jalan Besar",
                    "Walk to DT13 Rochor",
                    "Board train towards terminus DT1 Bukit Panjang",
                    "Alight at DT1 Bukit Panjang",
                    "Transfer to BP6 Bukit Panjang",
                    "Board train in direction of BP7 Petir",
                    "Alight at BP10 Fajar",
                    "Total duration: 84 minutes",
                    "Approximate path distance: 32.5 km, Haversine distance: 21.9 km, Circuity ratio: 1.5",
                ],
            },
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
        for trip in self.test_trips_short:
            pathinfo = self.rail_graph.find_shortest_path(
                trip["start"], trip["end"], trip["walk"]
            )
            expected = trip["total_cost"]
            actual = pathinfo.total_cost
            assert math.isclose(
                expected, actual
            ), f"{trip["start"]}-{trip["end"]} | Expected {expected}. Got {actual}."

        for trip in self.test_trips_full:
            pathinfo = self.rail_graph.find_shortest_path(
                trip["start"], trip["end"], trip["walk"]
            )
            assert pathinfo == trip["pathinfo"]  # Shallow comparison

        with pytest.raises(NoPathError):
            self.rail_graph.find_shortest_path("AA", "BB")

    def test_make_directions(self):
        for trip in self.test_trips_full:
            assert (
                self.rail_graph.make_directions(trip["pathinfo"]) == trip["directions"]
            )

        # At least 2 stations needed for journey.
        with pytest.raises(ValueError):
            self.rail_graph.make_directions(self.single_node_path)

    def test_path_and_haversine_distance(self):
        for trip in self.test_trips_full:
            expected = trip["path_and_haversine_distance"]
            actual = self.rail_graph.path_and_haversine_distance(trip["pathinfo"])
            assert all(
                math.isclose(p[0], p[1]) for p in zip(expected, actual)
            ), f"Expected {expected}. Got {actual}."

        # At least 2 stations needed for journey.
        with pytest.raises(ValueError):
            self.rail_graph.path_and_haversine_distance(self.single_node_path)
