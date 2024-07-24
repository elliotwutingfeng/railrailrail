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
from collections import defaultdict

import immutabledict


@dataclasses.dataclass(frozen=True)
class Station:
    """Train Station."""

    station_code: str
    station_name: str

    # The following fields are excluded from hashing.
    real_station_code: str = dataclasses.field(compare=False, init=False)
    full_station_name: str = dataclasses.field(compare=False, init=False)
    line_code: str = dataclasses.field(compare=False, init=False)
    station_number: int = dataclasses.field(compare=False, init=False)
    station_number_suffix: str = dataclasses.field(compare=False, init=False)
    has_pseudo_station_code: bool = dataclasses.field(compare=False, init=False)

    missing_station_codes: immutabledict.immutabledict[str, str] = (
        immutabledict.immutabledict({"CG": "EW4"})
    )
    succeeding_station_codes: immutabledict.immutabledict[str, str] = (
        immutabledict.immutabledict(
            {
                "TE33": "CG2",
                "TE34": "CG1",
                "TE35": "EW4",
                "CC33": "CE2",
                "CC34": "CE1",
            }
        )
    )
    pseudo_station_codes: immutabledict.immutabledict[str, str] = (
        immutabledict.immutabledict(
            {
                "CE0X": "CC6",
                "CE0Y": "CC5",
                "CE0Z": "CC4",
                "JE0": "JS3",
            }
        )
    )  # For temporary Circle Line Extension, and Jurong Region Line East Branch.

    match_expr: re.Pattern[str] = re.compile(
        r"^([A-Z]{2})([0-9]|[1-9][0-9]?)([A-Z]?)$", re.ASCII
    )

    # Missing/future/pseudo station codes.
    equivalent_station_code_pairs: tuple[tuple[str, str]] = dataclasses.field(
        compare=False,
        default=tuple(
            (k, v)
            for k, v in {
                **missing_station_codes,
                **succeeding_station_codes,
                **pseudo_station_codes,
            }.items()
        ),
    )

    def __post_init__(self):
        real_station_code = self.pseudo_station_codes.get(
            self.station_code, self.station_code
        )
        line_code, station_number, station_number_suffix = (
            self.to_station_code_components(self.station_code)
        )  # Based on pseudo station code, if any.
        object.__setattr__(self, "real_station_code", real_station_code)
        object.__setattr__(
            self, "full_station_name", f"{real_station_code} {self.station_name}"
        )
        object.__setattr__(self, "line_code", line_code)
        object.__setattr__(self, "station_number", int(station_number))
        object.__setattr__(self, "station_number_suffix", station_number_suffix)
        object.__setattr__(
            self,
            "has_pseudo_station_code",
            self.station_code in self.pseudo_station_codes,
        )

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

        station_code_components_match = cls.match_expr.match(station_code)
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
        """Group stations by interchange. Non-interchange stations are excluded.

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
