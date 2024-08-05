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

from railrailrail.network.station import SingaporeStation


class TestStation:
    @pytest.mark.parametrize(
        "station_code,station_code_components",
        [
            (("NS1"), ("NS", 1, "")),
            (("NS3A"), ("NS", 3, "A")),
            (("TE22A"), ("TE", 22, "A")),
            (("CG"), ("CG", -1, "")),
            (("STC"), ("STC", -1, "")),
            ((""), None),
            (("1"), None),
            (("1A"), None),
            (("A"), None),
            (("A1"), None),
            (("A1A"), None),
            (("XYZ0"), None),
            (("XYZ1"), None),
            (("XYZ1A"), None),
        ],
    )
    def test_to_station_code_components(self, station_code, station_code_components):
        if station_code_components is None:
            with pytest.raises(ValueError):  # Invalid station codes
                SingaporeStation.to_station_code_components(station_code)
        else:
            assert (
                SingaporeStation.to_station_code_components(station_code)
                == station_code_components
            )  # Valid station codes

    def test_get_interchanges(self):
        assert SingaporeStation.get_interchanges(
            [
                SingaporeStation("AB1", "X"),
                SingaporeStation("AC1", "X"),
                SingaporeStation("AC2", "Y"),
            ]
        ) == ({SingaporeStation("AB1", "X"), SingaporeStation("AC1", "X")},)
        with pytest.raises(ValueError):
            SingaporeStation.get_interchanges(
                [SingaporeStation("AB1", "X"), SingaporeStation("AB2", "X")]
            )
