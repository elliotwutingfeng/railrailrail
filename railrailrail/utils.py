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
from math import atan2, cos, radians, sin, sqrt


@dataclasses.dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float

    latitude_radians: float = dataclasses.field(init=False)
    longitude_radians: float = dataclasses.field(init=False)

    # Earth radius from World Geodetic System 1984 (WGS 84)
    # Department of Defense World Geodetic System 1984, Its Definition and Relationships With Local Geodetic Systems
    # (2014-07-08)
    # https://earth-info.nga.mil/php/download.php?file=coord-wgs84#.pdf
    __earth_radius_in_metres = 6378137

    def __post_init__(self):
        object.__setattr__(self, "latitude_radians", radians(self.latitude))
        object.__setattr__(self, "longitude_radians", radians(self.longitude))

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
        lat1 = initial_coord.latitude_radians
        lon1 = initial_coord.longitude_radians
        lat2 = final_coord.latitude_radians
        lon2 = final_coord.longitude_radians

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return cls.__earth_radius_in_metres * c
