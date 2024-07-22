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

from __future__ import annotations

import dataclasses
import re
from collections import OrderedDict, defaultdict


@dataclasses.dataclass(frozen=True)
class Station:
    station_code: str
    station_name: str

    real_station_code: str = dataclasses.field(init=False)
    full_station_name: str = dataclasses.field(init=False)
    line_code: str = dataclasses.field(init=False)
    station_number: int = dataclasses.field(init=False)
    station_number_suffix: str = dataclasses.field(init=False)
    is_pseudo_station_code: bool = dataclasses.field(init=False)

    ___match_expr: re.Pattern[str] = re.compile(
        r"^([A-Z]{2})([0-9]|[1-9][0-9]?)([A-Z]?)$", re.ASCII
    )

    def __post_init__(self):
        real_station_code = self.station_code  # TODO Add mapping.
        line_code, station_number, station_number_suffix = (
            self.to_station_code_components(self.station_code)
        )
        object.__setattr__(self, "real_station_code", real_station_code)
        object.__setattr__(
            self, "full_station_name", f"{real_station_code} {self.station_name}"
        )
        object.__setattr__(self, "line_code", line_code)
        object.__setattr__(self, "station_number", int(station_number))
        object.__setattr__(self, "station_number_suffix", station_number_suffix)
        object.__setattr__(self, "is_pseudo_station_code", station_number == 0)

    @classmethod
    def to_station_code_components(cls, station_code: str) -> tuple[str, int, str]:
        """Split station code into its components; line code, station number, and station number
        suffix.

        Can be used as a key function for sorting station codes in sequential order.

        Supports station codes with alphabetical suffixes like NS3 -> NS3A -> NS4.

        Args:
            station_code (str): Station code to be split up.

        Raises:
            ValueError: Invalid station code.

        Returns:
            tuple[str, int, str]: Separated station components.
            For example ("NS", 3, "A") or ("NS", 4, "").
        """
        # Check for 2-alphabet or 3-alphabet
        if len(station_code) in (2, 3) and all(
            ("A" <= letter <= "Z") for letter in station_code
        ):
            return station_code, -1, ""

        station_code_components_match = cls.___match_expr.match(station_code)
        if station_code_components_match is None:
            raise ValueError(f"Invalid station code: {station_code}")
        matcher_groups: tuple[str, str, str] = station_code_components_match.groups(
            default=""
        )
        line_code, station_number_str, station_number_suffix = matcher_groups
        station_number = int(station_number_str)
        return line_code, station_number, station_number_suffix

    @classmethod
    def get_interchanges(cls, stations: list[Station]) -> tuple[set[Station]]:
        """Group stations by interchange. Non-interchange station codes are excluded.

        Args:
            stations (list[Station]): Stations to be grouped.

        Returns:
            tuple[set[Station]]: Stations grouped by interchange.
        """
        interchange_stations_by_station_name: defaultdict[str, set[Station]] = (
            defaultdict(set)
        )
        for station in stations:
            interchange_stations_by_station_name[station.station_name].add(station)
        interchanges: tuple[set[Station]] = tuple(
            stations
            for stations in interchange_stations_by_station_name.values()
            if len(stations) >= 2
        )
        return interchanges

    @classmethod
    def get_terminals(
        cls, adjacency_matrix: defaultdict[str, OrderedDict[str, dict]]
    ) -> set[str]:
        """Identify terminal stations from a uni-directional adjacency matrix by counting their neighbours.
        Stations with purely alphabetic station codes will be identified as terminals.

        Args:
            adjacency_matrix (defaultdict[str, OrderedDict[str, dict]]): Uni-directional adjacency matrix
            of station codes linked in ascending order.

        Returns:
            set[str]: Terminal station codes.
        """
        terminals: set[str] = set()

        bi_directional_adjacency_matrix = defaultdict(OrderedDict)
        for station_code in adjacency_matrix:
            for next_station_code in adjacency_matrix[station_code]:
                bi_directional_adjacency_matrix[station_code][next_station_code] = None
                bi_directional_adjacency_matrix[next_station_code][station_code] = None

        for station_code, neighbours in bi_directional_adjacency_matrix.items():
            # Stations with less than 2 neighbours are terminals.
            # Stations with purely alphabetic station codes will be identified as terminals.
            if (
                len(neighbours) < 2
                or cls.to_station_code_components(station_code)[1] == -1
            ):
                terminals.add(station_code)

        return terminals
