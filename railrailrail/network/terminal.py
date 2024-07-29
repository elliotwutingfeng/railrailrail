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

from collections import OrderedDict, defaultdict

from dijkstar import Graph

from railrailrail.network.station import Station


class Terminal:
    """For identifying terminal stations."""

    looped_line_code_to_terminals: dict[str, set[str]] = {
        "BP": {"BP1", "BP14"},
        "JS": {"JS1"},
        "JW": {"JS1"},
        "PE": {"PTC"},
        "PTC": {"PTC"},
        "PW": {"PTC"},
        "SE": {"STC"},
        "STC": {"STC"},
        "SW": {"STC"},
    }  # These lines all terminate at one station like JS1,
    # except for BPLRT (Service A/B -> BP1, Service C -> BP14).

    @classmethod
    def get_terminals(
        cls,
        non_linear_line_terminals: dict[str, dict[str, int]],
        adjacency_matrix: defaultdict[str, OrderedDict[str, dict]],
    ) -> set[str]:
        """Identify terminal stations from a uni-directional adjacency matrix by counting their neighbours.
        Stations with purely alphabetic station codes will be identified as terminals.

        Args:
            non_linear_line_terminals (dict[str, dict[str, int]]): Map of non-linear line codes to terminal station codes.
            adjacency_matrix (defaultdict[str, OrderedDict[str, dict]]): Uni-directional adjacency matrix
            of station codes linked in ascending order.

        Returns:
            set[str]: Terminal station codes.
        """
        terminals: set[str] = set()

        bi_directional_adjacency_matrix = defaultdict(dict)
        for station_code in adjacency_matrix:
            for next_station_code in adjacency_matrix[station_code]:
                bi_directional_adjacency_matrix[station_code][next_station_code] = None
                bi_directional_adjacency_matrix[next_station_code][station_code] = None

        for station_code, neighbours in bi_directional_adjacency_matrix.items():
            # Stations with less than 2 neighbours are terminals.
            # Stations with purely alphabetic station codes will be identified as terminals.
            line_code, station_number, _ = Station.to_station_code_components(
                station_code
            )
            if line_code in non_linear_line_terminals:
                if station_code in non_linear_line_terminals[line_code]:
                    terminals.add(station_code)
            elif len(neighbours) < 2 or station_number == -1:
                terminals.add(station_code)

        return terminals

    @classmethod
    def get_approaching_terminal(
        cls,
        graph: Graph,
        non_linear_line_terminals: dict[str, dict[str, int]],
        start: str,
        end: str,
    ) -> str | None:
        if start == end:
            raise ValueError(f"start and end must be different. Got {start} and {end}")
        start_station_code_components = Station.to_station_code_components(start)
        end_station_code_components = Station.to_station_code_components(end)
        start_line_code, _, _ = start_station_code_components
        end_line_code, _, _ = end_station_code_components
        if start_line_code in non_linear_line_terminals:
            return None
        if start_line_code != end_line_code:
            raise ValueError(
                f"start_line_code and end_line_code must be the same on linear lines. Got {start_line_code} and {end_line_code}"
            )
        is_ascending: bool = start_station_code_components < end_station_code_components
        # From start, traverse nodes in ascending or descending order with same line code until dead end is reached.
        next_station_code = start
        while True:
            station_and_neighbours = sorted(
                [
                    *(
                        station_code
                        for station_code in graph.get_incoming(next_station_code)
                        if Station.to_station_code_components(station_code)[0]
                        == start_line_code
                    ),
                    next_station_code,
                ],
                key=Station.to_station_code_components,
            )
            next_station_index = station_and_neighbours.index(next_station_code) + (
                1 if is_ascending else -1
            )
            if next_station_index < 0 or next_station_index >= len(
                station_and_neighbours
            ):
                return next_station_code
            next_station_code = station_and_neighbours[next_station_index]
