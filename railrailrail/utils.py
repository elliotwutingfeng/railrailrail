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
    # Earth radius from World Geodetic System 1984 (WGS 84)
    # Department of Defense World Geodetic System 1984, Its Definition and Relationships With Local Geodetic Systems
    # (2014-07-08)
    # https://earth-info.nga.mil/php/download.php?file=coord-wgs84#.pdf
    __earth_radius_in_metres = 6378137

    @classmethod
    def haversine_distance(
        cls, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """Great-circle (shortest) distance between 2 points on Earth in metres.

        Args:
            lat1 (float): Latitude of first point in decimal degrees.
            lon1 (float): Longitude of first point in decimal degrees.
            lat2 (float): Latitude of second point in decimal degrees.
            lon2 (float): Longitude of second point in decimal degrees.

        Returns:
            float: Shortest distance between 2 points in metres.
        """
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return cls.__earth_radius_in_metres * c


class StationUtils:
    ___match_expr: re.Pattern[str] = re.compile("^([A-Z]{2})([0-9]+)([A-Z]?)$")

    @classmethod
    def __station_code_matcher(cls, station_code: str) -> re.Match[str] | None:
        return cls.___match_expr.match(station_code)

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

        station_code_components_match = cls.__station_code_matcher(station_code)
        if station_code_components_match is None:
            raise ValueError(f"Invalid station code: {station_code}")
        matcher_groups: tuple[str, str, str] = station_code_components_match.groups(
            default=""
        )
        line_code, station_number_str, station_number_suffix = matcher_groups
        station_number = int(station_number_str)
        return line_code, station_number, station_number_suffix
