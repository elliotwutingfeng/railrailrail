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

import pytest
from dijkstar import Graph

from railrailrail.dataset import (
    ConditionalInterchange,
    Durations,
    Stage,
    Terminal,
    WalkingTrainMap,
)


class TestStage:
    def test_stages(self):
        assert Stage.stages
        assert Stage.stages_defunct

    def test_bad_stage(self):
        with pytest.raises(ValueError):
            Stage("this_is_not_a_real_stage")


class TestWalkingTrainMap:
    def test_segments(self):
        assert WalkingTrainMap.segments


class TestConditionalInterchange:
    def test_is_conditional_interchange_transfer(self):
        assert ConditionalInterchange.is_conditional_interchange_transfer(
            "bahar_east", "bahar_west"
        )
        assert not ConditionalInterchange.is_conditional_interchange_transfer(
            "bahar_west", "bahar_east"
        )


class TestTerminal:
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

        # Journeys on lines without loops must start and end on stations with same line code.
        with pytest.raises(ValueError):
            Terminal.get_terminal(graph, "EW1", "NS2")

        # Journey cannot start and end at the same station.
        with pytest.raises(ValueError):
            Terminal.get_terminal(graph, "EW1", "EW1")


class TestDurations:
    def test_segments(self):
        assert Durations.segments
