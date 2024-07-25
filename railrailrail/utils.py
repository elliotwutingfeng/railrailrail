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
import math


@dataclasses.dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float

    # Earth radius from World Geodetic System 1984 (WGS 84)
    # Department of Defense World Geodetic System 1984, Its Definition and Relationships With Local Geodetic Systems
    # (2014-07-08)
    # https://earth-info.nga.mil/php/download.php?file=coord-wgs84#.pdf
    __earth_radius_in_metres = 6378137

    @classmethod
    def haversine_distance(
        cls, initial_coord: Coordinates, final_coord: Coordinates
    ) -> float:
        """Great-circle (shortest) distance between 2 points on Earth in metres.

        Args:
            initial_coord (float): Coordinates of of initial point in decimal degrees.
            final_coord (float): Coordinates of final point in decimal degrees.

        Returns:
            float: Shortest distance between 2 points in metres.
        """
        lat1 = math.radians(initial_coord.latitude)
        lon1 = math.radians(initial_coord.longitude)
        lat2 = math.radians(final_coord.latitude)
        lon2 = math.radians(final_coord.longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return cls.__earth_radius_in_metres * c
