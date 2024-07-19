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

import json
import pathlib
from collections import OrderedDict, defaultdict

import tomlkit

from railrailrail.dataset import Durations, SemiInterchange, Stage, WalkingTrainMap
from railrailrail.utils import StationUtils


class Config:
    def __init__(self, stage: Stage) -> None:
        self.stations: list[tuple[str, str]] = self._get_stations(stage)
        self.station_codes_by_station_name: dict[str, set[str]] = defaultdict(set)
        for station_code, station_name in self.stations:
            self.station_codes_by_station_name[station_name].add(station_code)
        self.adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = (
            self._generate_adjacency_matrix(self.stations)
        )

    def _get_stations(self, stage: Stage) -> list[tuple[str, str]]:
        """Generate list of train station codes and station names operational at a given `stage`,
        sorted by station code in ascending order.

        Args:
            stage (Stage): Rail network stage to get stations from.

        Returns:
            list[tuple[str, str]]: Train stations sorted by station code in ascending order.
            For example, ("CC1", "Dhoby Ghaut"), ("NE6", "Dhoby Ghaut"), ("NS24", "Dhoby Ghaut").
        """

        return sorted(
            stage.stations,
            key=lambda station: StationUtils.to_station_code_components(station[0]),
        )

    def _generate_adjacency_matrix(
        self, stations: list[tuple[str, str]]
    ) -> defaultdict[str, OrderedDict[str, dict]]:
        """Create an travel time adjacency matrix for all stations on the network.

        Args:
            stations (list[tuple[str, str]]): List of station code/station name pairs.

        Returns:
            defaultdict[str, OrderedDict[str, dict]]: Travel time adjacency matrix.
        """
        station_codes: list[str] = [station_code for station_code, _ in stations]

        station_codes_by_line_code: defaultdict[str, OrderedDict[str, None]] = (
            defaultdict(OrderedDict)
        )  # Order is important as stations are almost always connected in sequential order.
        for station_code in station_codes:  # Group stations by line.
            line_code, _, _ = StationUtils.to_station_code_components(station_code)
            station_codes_by_line_code[line_code][station_code] = None

        # Uni-directionally link up all adjacent stations on same line based on the fact that most adjacent stations
        # are arranged by station code in sequential order (same line code and in ascending station number order).
        adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = defaultdict(
            OrderedDict
        )
        for line_code in station_codes_by_line_code:
            line_station_codes = sorted(
                station_codes_by_line_code[line_code],
                key=StationUtils.to_station_code_components,
            )
            for station_code, next_station_code in zip(
                line_station_codes[:-1], line_station_codes[1:]
            ):
                if (station_code, next_station_code) == ("BP13", "BP14"):
                    continue  # Special case: No link between BP13 and BP14.
                if (station_code, next_station_code) == ("NS4", "NS13"):
                    continue  # Special case: No link between NS4 and NS13.
                adjacency_matrix[station_code][next_station_code] = {
                    "duration": Durations.edges.get(
                        f"{station_code}-{next_station_code}", dict()
                    ).get("duration", 0)
                }

        # Add walking paths from LTA Walking Train Map (WTM)
        for start_station_name, end_station_name, duration in WalkingTrainMap.routes:
            for start_station_code in self.station_codes_by_station_name[
                start_station_name
            ]:
                for end_station_code in self.station_codes_by_station_name[
                    end_station_name
                ]:
                    adjacency_matrix[start_station_code][end_station_code] = {
                        "duration": duration,
                        "mode": "walk",
                    }

        # Mark edges that need to be treated differently from
        # most other edges. Currently this only means checking if an edge is
        # adjacent to a semi-interchange.
        for start, end, edge_type in SemiInterchange.edges:
            # Skip semi-interchange edges made obsolete by new stations.
            if (start, end) == ("STC", "SW2") and "SW1" in station_codes:
                continue
            if (start, end) == ("STC", "SW4") and "SW2" in station_codes:
                continue
            if (start, end) == ("PTC", "PE5") and "PE6" in station_codes:
                continue
            if (start, end) == ("PTC", "PE6") and "PE7" in station_codes:
                continue
            if (start, end) == ("PTC", "PW5") and "PW1" in station_codes:
                continue

            if start in station_codes and end in station_codes:
                adjacency_matrix[start][end] = {
                    **Durations.edges[f"{start}-{end}"],
                    "edge_type": edge_type,
                }

        return adjacency_matrix

    @classmethod
    def update_network(
        cls,
        network: tomlkit.TOMLDocument,
        stations: list[tuple[str, str]],
        adjacency_matrix: defaultdict[str, OrderedDict[str, dict]],
    ) -> None:
        """Replace contents of `network` configuration in-place
        with `stations` and `adjacency_matrix`.

        - Newly added entries are marked as NEW.
        - Entries to be modified will have their new content added as an inline-comment.
        - Entries made defunct will be marked as DEFUNCT with an inline-comment.
        - Existing comments are preserved.

        Args:
            network (tomlkit.TOMLDocument): Network configuration to be updated.
            stations (list[tuple[str, str]]): After the update, `network` should only have
            these stations.
            adjacency_matrix (defaultdict[str, OrderedDict[str, dict]]): After the update,
            `network` should only have these adjacency matrix edges.
        """

        network["schema"] = network.get("schema", 1)
        network["transfer_time"] = network.get("transfer_time", 7)
        network["dwell_time"] = network.get("dwell_time", 0.5)

        ### stations ###

        stations_ = {k: v for (k, v) in stations}
        network_stations = (
            network["stations"] if "stations" in network else tomlkit.table()
        )

        # Mark modified stations with comment
        for station_code, station_name in network_stations.items():
            if station_code in stations_ and station_name != stations_[station_code]:
                existing_comment = network_stations[station_code].trivia.comment
                network_stations[station_code].comment(
                    f"NEW -> {stations_[station_code]}{' | %s' % existing_comment if existing_comment else ''}"
                )

        # Mark defunct stations with comment
        for defunct_station_code in set(network_stations).difference(stations_):
            existing_comment = network_stations[defunct_station_code].trivia.comment
            network_stations[defunct_station_code].comment(
                f"DEFUNCT{' | %s' % existing_comment if existing_comment else ''}"
            )

        # Add new stations
        for new_station_code in set(stations_).difference(network_stations):
            network_stations[new_station_code] = stations_[new_station_code]
            network_stations[new_station_code].comment("NEW")

        # Sort stations
        updated_stations = tomlkit.table()
        for station_code in sorted(
            network_stations, key=StationUtils.to_station_code_components
        ):
            updated_stations[station_code] = network_stations[station_code]
        network["stations"] = updated_stations

        ### adjacency matrix ###

        network_adjacency_matrix = (
            network["edges"] if "edges" in network else tomlkit.table()
        )

        # Mark modified edges with comment
        for station_pair, edge_details in network_adjacency_matrix.items():
            station_pair_ = station_pair.split("-", 1)
            if (
                station_pair_[0] in adjacency_matrix
                and station_pair_[1] in adjacency_matrix[station_pair_[0]]
            ):
                new_edge_details = adjacency_matrix[station_pair_[0]][station_pair_[1]]
                if edge_details != new_edge_details:  # Shallow dict comparison
                    existing_comment = network_adjacency_matrix[
                        station_pair
                    ].trivia.comment
                    network_adjacency_matrix[station_pair].comment(
                        f"NEW -> {json.dumps(new_edge_details)}{' | %s' % existing_comment if existing_comment else ''}"
                    )

        adjacency_matrix_edges = {
            f"{a}-{b}" for a in adjacency_matrix for b in adjacency_matrix[a]
        }

        # Mark defunct adjacency matrix entries with comment
        for defunct_edge in set(network_adjacency_matrix).difference(
            adjacency_matrix_edges
        ):
            existing_comment = network_adjacency_matrix[defunct_edge].trivia.comment
            network_adjacency_matrix[defunct_edge].comment(
                f"DEFUNCT{' | %s' % existing_comment if existing_comment else ''}"
            )

        # Add new adjacency matrix entries
        for new_edge in set(adjacency_matrix_edges).difference(
            network_adjacency_matrix
        ):
            vertices = new_edge.split("-", 1)
            start, end = vertices[0], vertices[1]
            it = tomlkit.inline_table()
            it.update(adjacency_matrix[start][end])
            network_adjacency_matrix[new_edge] = it
            network_adjacency_matrix[new_edge].comment("NEW")

        # Sort adjacency matrix entries
        updated_adjacency_matrix = tomlkit.table()
        for edge in sorted(
            network_adjacency_matrix,
            key=lambda x: (
                StationUtils.to_station_code_components(x.split("-", 1)[0]),
                StationUtils.to_station_code_components(x.split("-", 1)[1]),
            ),
        ):
            updated_adjacency_matrix[edge] = network_adjacency_matrix[edge]
        network["edges"] = updated_adjacency_matrix

    def update_network_config_file(self, path: pathlib.Path) -> None:
        """Overwrites contents of network file at `path` with updated
        network data. See `Config.update_network`.

        Args:
            path (pathlib.Path): Path to network file.
        """
        try:
            with open(path, "rb") as f:
                network: tomlkit.TOMLDocument = tomlkit.load(f)
        except OSError:
            network: tomlkit.TOMLDocument = tomlkit.TOMLDocument()
        Config.update_network(network, self.stations, self.adjacency_matrix)
        with open(path, "w") as f:
            tomlkit.dump(network, f)
