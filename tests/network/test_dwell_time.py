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

from railrailrail.network.dwell_time import DwellTime


class TestDwellTime:
    @pytest.mark.parametrize(
        "terminal_station_codes,interchange_station_codes,current_station,next_station,expected_dwell_times",
        [
            ({}, {}, "SW1", "STC", (28, 28)),
            ({}, {"SW1"}, "SW1", "STC", (28, 45)),
            ({"SW1"}, {}, "SW1", "STC", (28, 60)),
            ({"SW1"}, {"SW1"}, "SW1", "STC", (28, 60)),
            #
            ({}, {"STC"}, "SW1", "STC", (45, 28)),
            ({}, {"STC", "SW1"}, "SW1", "STC", (45, 45)),
            ({"SW1"}, {"STC"}, "SW1", "STC", (45, 60)),
            ({"SW1"}, {"STC", "SW1"}, "SW1", "STC", (45, 60)),
            #
            ({"STC"}, {}, "SW1", "STC", (60, 28)),
            ({"STC"}, {"STC"}, "SW1", "STC", (60, 28)),
            ({"STC"}, {"SW1"}, "SW1", "STC", (60, 45)),
            ({"STC"}, {"STC", "SW1"}, "SW1", "STC", (60, 45)),
            ({"STC", "SW1"}, {}, "SW1", "STC", (60, 60)),
            ({"STC", "SW1"}, {"STC"}, "SW1", "STC", (60, 60)),
            ({"STC", "SW1"}, {"SW1"}, "SW1", "STC", (60, 60)),
            ({"STC", "SW1"}, {"STC", "SW1"}, "SW1", "STC", (60, 60)),
        ],
    )
    def test_get_dwell_time(
        self,
        terminal_station_codes,
        interchange_station_codes,
        current_station,
        next_station,
        expected_dwell_times,
    ):
        assert (
            DwellTime.get_dwell_time(
                terminal_station_codes,
                interchange_station_codes,
                current_station,
                next_station,
            )
            == expected_dwell_times
        )
