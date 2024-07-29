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

from railrailrail.network.conditional_transfers import ConditionalTransfersSegment
from railrailrail.network.dwell_time import DwellTime
from railrailrail.network.segments import Segments
from railrailrail.network.stage import Stage
from railrailrail.network.station import Station
from railrailrail.network.terminal import Terminal
from railrailrail.network.walks import Walks


class TestStage:
    def test_stages(self):
        assert Stage.stages
        assert Stage.stages_defunct

    def test_bad_stage(self):
        with pytest.raises(ValueError):
            Stage("this_is_not_a_real_stage")


class TestWalks:
    def test_routes(self):
        assert Walks.routes


class TestTerminal:
    def test_get_approaching_terminal(self):
        non_linear_line_terminals = {"BP": {"BP1": 1, "BP14": 1}}
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
                    Terminal.get_approaching_terminal(
                        graph,
                        non_linear_line_terminals,
                        edge_node_pairs[i][0],
                        edge_node_pairs[j][1],
                    )
                    == "NS8"
                )
                assert (
                    Terminal.get_approaching_terminal(
                        graph,
                        non_linear_line_terminals,
                        edge_node_pairs[j][1],
                        edge_node_pairs[i][0],
                    )
                    == "NS1"
                )

        # Reject lines with loops
        graph = Graph(undirected=False)
        graph.add_edge("BP1", "BP2", (1, "", ""))
        assert (
            Terminal.get_approaching_terminal(
                graph, non_linear_line_terminals, "BP1", "BP2"
            )
            is None
        )

        # Journeys on lines without loops must start and end on stations with same line code.
        with pytest.raises(ValueError):
            Terminal.get_approaching_terminal(
                graph, non_linear_line_terminals, "EW1", "NS2"
            )

        # Journey cannot start and end at the same station.
        with pytest.raises(ValueError):
            Terminal.get_approaching_terminal(
                graph, non_linear_line_terminals, "EW1", "EW1"
            )


class TestSegments:
    def test_segments(self):
        assert Segments.segments


class TestStation:
    def test_to_station_code_components(self):
        # Valid station codes
        assert Station.to_station_code_components("NS1") == ("NS", 1, "")
        assert Station.to_station_code_components("NS3A") == ("NS", 3, "A")
        assert Station.to_station_code_components("TE22A") == ("TE", 22, "A")
        assert Station.to_station_code_components("CG") == ("CG", -1, "")
        assert Station.to_station_code_components("STC") == ("STC", -1, "")

        # Invalid station codes
        with pytest.raises(ValueError):
            Station.to_station_code_components("")
        with pytest.raises(ValueError):
            Station.to_station_code_components("1")
        with pytest.raises(ValueError):
            Station.to_station_code_components("1A")
        with pytest.raises(ValueError):
            Station.to_station_code_components("A")
        with pytest.raises(ValueError):
            Station.to_station_code_components("A1")
        with pytest.raises(ValueError):
            Station.to_station_code_components("A1A")
        with pytest.raises(ValueError):
            Station.to_station_code_components("XYZ0")
        with pytest.raises(ValueError):
            Station.to_station_code_components("XYZ1")
        with pytest.raises(ValueError):
            Station.to_station_code_components("XYZ1A")

    def test_get_interchanges(self):
        with pytest.raises(ValueError):
            Station.get_interchanges([Station("AB1", "X"), Station("AB2", "X")])


class TestDwellTime:
    def test_get_dwell_time(self):
        terminal_station_codes = {"STC"}
        interchange_station_codes = {"STC"}
        assert DwellTime.get_dwell_time(
            terminal_station_codes, interchange_station_codes, "SW1", "STC"
        ) == (60, 28)


class TestConditionalTransfersSegment:
    def test_post_init(self):
        with pytest.raises(ValueError):
            ConditionalTransfersSegment(("AB1", "AB2"), "", "AB1")
        with pytest.raises(ValueError):
            ConditionalTransfersSegment(("AB1", "AB1"), "x", "AB1")
        with pytest.raises(ValueError):
            ConditionalTransfersSegment(("AB1", "AB2"), "x", "AB3")
