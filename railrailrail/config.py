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

import io
import json
import pathlib
import zipfile
from collections import OrderedDict, defaultdict

import requests
import tomlkit
import xlrd

from railrailrail.dataset import (
    Durations,
    RailExpansion,
    SemiInterchange,
    WalkingTrainMap,
)
from railrailrail.utils import StationUtils


class Config:
    STATION_DATA_ENDPOINT = (
        "https://datamall.lta.gov.sg/content/dam/datamall/datasets/Geospatial/"
        "Train%20Station%20Codes%20and%20Chinese%20Names.zip"
    )

    def __init__(self, rail_expansion: RailExpansion) -> None:
        self.stations: list[tuple[str, str]] = self._get_stations(
            Config.STATION_DATA_ENDPOINT, rail_expansion
        )
        self.station_codes_by_station_name: dict[str, set[str]] = defaultdict(set)
        for station_code, station_name in self.stations:
            self.station_codes_by_station_name[station_name].add(station_code)
        self.adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = (
            self._generate_adjacency_matrix(self.stations)
        )

    def update_network_config(self, path: pathlib.Path) -> None:
        try:
            with open(path, "rb") as f:
                network: tomlkit.TOMLDocument = tomlkit.load(f)
        except OSError:
            network: tomlkit.TOMLDocument = tomlkit.TOMLDocument()
        self._update_network(network, self.stations, self.adjacency_matrix)
        with open(path, "w") as f:
            tomlkit.dump(network, f)

    def _get_stations(
        self, endpoint: str, rail_expansion: RailExpansion | None = None
    ) -> list[tuple[str, str]]:
        """Download train station codes and station names.

        Args:
            endpoint (str): HTTPS address of zipped XLS file containing train station codes and names.
            rail_expansion (RailExpansion | None): Include stations that have yet to be opened. Defaults to None.

        Returns:
            list[tuple[str, str]]: Train stations sorted by station code in ascending order.
            For example, ("CC1", "Dhoby Ghaut"), ("NE6", "Dhoby Ghaut"), ("NS24", "Dhoby Ghaut").
        """
        with requests.Session() as session:
            res = session.get(endpoint, timeout=30)
            res.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(res.content), "r") as z:
            excel_bytes = z.read(
                z.infolist()[0]
            )  # Zip file should only contain one XLS file.
            workbook = xlrd.open_workbook(file_contents=excel_bytes)
            sheet = workbook.sheet_by_index(0)

        stations: set[tuple[str, str]] = {
            (sheet.cell_value(row_idx, 0).strip(), sheet.cell_value(row_idx, 1).strip())
            for row_idx in range(1, sheet.nrows)
        }

        if isinstance(rail_expansion, RailExpansion):
            rail_expansion.update_stations(stations)

        # If CG-TEL conversion incomplete, add missing CG station code for EW4 Tanah Merah interchange.
        if any(station[0].startswith("CG") for station in stations):
            stations.add(("CG", "Tanah Merah"))

        # If Circle Line Stage 6 is incomplete, add pseudo station codes for Marina Bay - Stadium shuttle service.
        if any(station[0].startswith("CE") for station in stations):
            stations.update(
                {
                    ("CE0X", "Stadium"),  # Pseudo station_code
                    ("CE0Y", "Nicoll Highway"),  # Pseudo station_code
                    ("CE0Z", "Promenade"),  # Pseudo station_code
                }
            )

        return sorted(
            stations,
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
        )
        for station_code in station_codes:  # Group stations by line
            line_code, _, _ = StationUtils.to_station_code_components(station_code)
            station_codes_by_line_code[line_code][station_code] = None

        # Uni-directionally link up all adjacent stations on same line based on the fact that most adjacent stations
        # are arranged by station code in sequential order (same line code and in ascending station number order).
        adjacency_matrix: defaultdict[str, OrderedDict[str, dict]] = defaultdict(
            OrderedDict
        )
        for line_code in station_codes_by_line_code:
            line_station_codes = sorted(
                station_codes_by_line_code[line_code].keys(),
                key=StationUtils.to_station_code_components,
            )
            for station_code, next_station_code in zip(
                line_station_codes[:-1], line_station_codes[1:]
            ):
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
            if start in station_codes and end in station_codes:
                adjacency_matrix[start][end] = {
                    **Durations.edges[f"{start}-{end}"],
                    "edge_type": edge_type,
                }

        return adjacency_matrix

    def _update_network(
        self,
        network: tomlkit.TOMLDocument,
        stations: list[tuple[str, str]],
        adjacency_matrix: defaultdict[str, OrderedDict[str, dict]],
    ) -> None:
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
                network_stations[station_code].comment(
                    f"NEW -> {stations_[station_code]}"
                )

        # Mark defunct stations with comment
        for defunct_station_code in set(network_stations).difference(stations_):
            network_stations[defunct_station_code].comment("DEFUNCT")

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
                    network_adjacency_matrix[station_pair].comment(
                        f"NEW -> {json.dumps(new_edge_details)}"
                    )

        adjacency_matrix_edges = {
            f"{a}-{b}" for a in adjacency_matrix for b in adjacency_matrix[a]
        }

        # Mark defunct adjacency matrix entries with comment
        for defunct_edge in set(network_adjacency_matrix).difference(
            adjacency_matrix_edges
        ):
            network_adjacency_matrix[defunct_edge].comment("DEFUNCT")

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
