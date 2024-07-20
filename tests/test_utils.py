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

import pytest

from railrailrail.utils import GeographicUtils, StationUtils


class TestGeographicUtils:
    def test_haversine_distance(self):
        # Bukit Timah Hill Summit to Singapore Parliament House
        assert (
            int(
                GeographicUtils.haversine_distance(
                    1.354681, 103.776375, 1.2891, 103.8504
                )
            )
            == 11007
        )


class TestStationUtils:
    def test_to_station_code_components(self):
        # Valid station codes
        assert StationUtils.to_station_code_components("NS1") == ("NS", 1, "")
        assert StationUtils.to_station_code_components("NS3A") == ("NS", 3, "A")
        assert StationUtils.to_station_code_components("TE22A") == ("TE", 22, "A")
        assert StationUtils.to_station_code_components("CG") == ("CG", -1, "")
        assert StationUtils.to_station_code_components("STC") == ("STC", -1, "")

        # Invalid station codes
        with pytest.raises(ValueError):
            StationUtils.to_station_code_components("")
        with pytest.raises(ValueError):
            StationUtils.to_station_code_components("1")
        with pytest.raises(ValueError):
            StationUtils.to_station_code_components("1A")
        with pytest.raises(ValueError):
            StationUtils.to_station_code_components("A")
        with pytest.raises(ValueError):
            StationUtils.to_station_code_components("A1")
        with pytest.raises(ValueError):
            StationUtils.to_station_code_components("A1A")
        with pytest.raises(ValueError):
            StationUtils.to_station_code_components("XYZ0")
        with pytest.raises(ValueError):
            StationUtils.to_station_code_components("XYZ1")
        with pytest.raises(ValueError):
            StationUtils.to_station_code_components("XYZ1A")
