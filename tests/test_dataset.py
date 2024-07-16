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

import unittest

from dijkstar import Graph

from railrailrail.dataset import (
    Durations,
    SemiInterchange,
    Stage,
    Terminal,
    WalkingTrainMap,
)


class TestStage(unittest.TestCase):
    def test_stages(self):
        stations: set[tuple[str, str]] = set()
        for stage, stage_stations in Stage.stages.items():
            stage_stations_set = set(stage_stations)
            stage_defunct_stations_set = set(Stage.stages_defunct.get(stage, ()))

            # Never add and remove the same station at the same stage.
            assert not stage_stations_set.intersection(stage_defunct_stations_set)
            # Do not attempt to re-add existing stations
            assert not stage_stations_set.intersection(stations)
            # Do not attempt to remove non-existing stations.
            assert stage_defunct_stations_set.issubset(stations)

            stations.update(stage_stations_set)
            stations.difference_update(stage_defunct_stations_set)

        # No station code should be paired with more than one name.
        assert len(stations) == len(
            set(
                " ".join([station_code, station_name])
                for station_code, station_name in stations
            )
        )


class TestWalkingTrainMap(unittest.TestCase):
    def test_routes(self):
        assert WalkingTrainMap.routes


class TestSemiInterchange(unittest.TestCase):
    def test_is_semi_interchange_transfer(self):
        assert SemiInterchange.is_semi_interchange_transfer("bahar_east", "bahar_west")
        assert not SemiInterchange.is_semi_interchange_transfer(
            "bahar_west", "bahar_east"
        )


class TestTerminal(unittest.TestCase):
    def test_get_terminal(self):
        graph = Graph(undirected=False)
        edge_node_pairs = (
            ("NS1", "NS2"),
            ("NS2", "NS3"),
            ("NS3", "NS4"),
            ("NS4", "NS5"),
            ("NS5", "NS7"),
            ("NS7", "NS8"),
        )
        for node_1, node_2 in edge_node_pairs:
            graph.add_edge(node_1, node_2, (1, "", ""))
            graph.add_edge(node_2, node_1, (1, "", ""))
        for i in range(len(edge_node_pairs)):
            for j in range(i + 1, len(edge_node_pairs)):
                assert (
                    Terminal.get_terminal(
                        graph, edge_node_pairs[i][0], edge_node_pairs[j][1]
                    )
                    == "NS8"
                )
                assert (
                    Terminal.get_terminal(
                        graph, edge_node_pairs[j][1], edge_node_pairs[i][0]
                    )
                    == "NS1"
                )

        # Reject lines with loops
        graph = Graph(undirected=False)
        graph.add_edge("BP1", "BP2", (1, "", ""))
        assert Terminal.get_terminal(graph, "BP1", "BP2") is None


class TestDurations(unittest.TestCase):
    def test_edges(self):
        assert Durations.edges
