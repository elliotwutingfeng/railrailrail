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

import re
from math import atan2, cos, radians, sin, sqrt


class GeographicUtils:
    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        r = 6373000  # Approximate radius of earth in metres

        return r * c


class StationUtils:
    @staticmethod
    def to_station_code_components(station_code: str) -> tuple[str, int, str]:
        """Split station code into its components; line code, station number, and station number
        suffix.

        Can be used as a key function for sorting station codes in sequential order.

        Supports station codes with alphabetical suffixes like NS3 -> NS3A -> NS4.

        Args:
            station_code (str): Station code to be split up.

        Returns:
            tuple[str, int, str]: Separated station components.
            For example ("NS", 3, "A") or ("NS", 4, "").
        """
        line_code, station_number, station_number_suffix = (
            station_code,
            0,
            "",
        )  # Default values for invalid station code.

        matcher = lambda station_code: re.match(
            "([A-Z]+)([0-9]+)([A-Z]*)", station_code
        )  # Ensure station code matches correct format.
        station_code_components_match = matcher(station_code)
        if station_code_components_match is None:
            return line_code, station_number, station_number_suffix
        matcher_groups: tuple[str, str, str] = station_code_components_match.groups("")
        line_code, station_number_str, station_number_suffix = matcher_groups
        station_number = int(station_number_str)
        return line_code, station_number, station_number_suffix
