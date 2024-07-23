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

from dijkstar import Graph

from railrailrail.dataset.station import Station


class Terminal:
    __looped_lines = frozenset(
        (
            "BP",
            "JS",
            "JW",
            "PE",
            "PTC",
            "PW",
            "SE",
            "STC",
            "SW",
        )
    )  # These lines all terminate at one station like JS1, except for BPLRT (Service A/B -> BP1, Service C -> BP14).

    @classmethod
    def get_terminal(cls, graph: Graph, start: str, end: str) -> str | None:
        if start == end:
            raise ValueError(f"start and end must be different. Got {start} and {end}")
        start_station_code_components = Station.to_station_code_components(start)
        end_station_code_components = Station.to_station_code_components(end)
        start_line_code, _, _ = start_station_code_components
        end_line_code, _, _ = end_station_code_components
        if start_line_code in cls.__looped_lines or (
            start_line_code == "CC" and "CC34" in graph
        ):
            # Circle Line becomes a looped line at Stage 6.
            return None
        if start_line_code != end_line_code:
            raise ValueError(
                f"start_line_code and end_line_code must be the same. Got {start_line_code} and {end_line_code}"
            )
        is_ascending: bool = start_station_code_components < end_station_code_components
        # From start, traverse nodes in ascending or descending order with same line code until dead end is reached.
        next_node = start
        while True:
            node_and_neighbours = sorted(
                [
                    *(
                        node
                        for node in graph.get_incoming(next_node)
                        if node[:2] == start_line_code
                    ),
                    next_node,
                ],
                key=Station.to_station_code_components,
            )
            next_node_index = node_and_neighbours.index(next_node) + (
                1 if is_ascending else -1
            )
            if next_node_index < 0 or next_node_index >= len(node_and_neighbours):
                return next_node
            next_node = node_and_neighbours[next_node_index]
