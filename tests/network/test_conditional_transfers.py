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

from railrailrail.network.conditional_transfers import ConditionalTransfersSegment


class TestConditionalTransfersSegment:
    @pytest.mark.parametrize(
        "station_code_pair,edge_type,interchange_station_code,defunct_with_station_code",
        [
            (("AB1", "AB2"), "", "AB1", None),
            (("AB1", "AB1"), "x", "AB1", None),
            (("AB1", "AB2"), "x", "AB3", None),
            (("AB1", "AB2"), "x", "AB1", "AB1"),
            (("AB1", "AB2"), "x", "AB1", "AB2"),
        ],
    )
    def test_post_init(
        self,
        station_code_pair,
        edge_type,
        interchange_station_code,
        defunct_with_station_code,
    ):
        with pytest.raises(ValueError):
            ConditionalTransfersSegment(
                station_code_pair,
                edge_type,
                interchange_station_code,
                defunct_with_station_code,
            )
