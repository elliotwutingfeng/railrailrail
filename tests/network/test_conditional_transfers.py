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
        (
            "station_code_pair",
            "edge_type",
            "interchange_station_code",
            "defunct_with_station_code",
            "match",
        ),
        [
            (("AB1", "AB2"), "", "AB1", None, "edge_type must be a non-empty string"),
            (
                ("AB1", "AB1"),
                "x",
                "AB1",
                None,
                "station_code_pair must be 2 different station codes",
            ),
            (
                ("AB1", "AB2"),
                "x",
                "AB3",
                None,
                "station_code_pair must contain interchange_station_code",
            ),
            (
                ("AB1", "AB2"),
                "x",
                "AB1",
                "AB1",
                "defunct_with_station_code must not be in station_code_pair",
            ),
            (
                ("AB1", "AB2"),
                "x",
                "AB1",
                "AB2",
                "defunct_with_station_code must not be in station_code_pair",
            ),
        ],
    )
    def test_post_init(
        self,
        station_code_pair,
        edge_type,
        interchange_station_code,
        defunct_with_station_code,
        match,
    ):
        with pytest.raises(ValueError, match=match):
            ConditionalTransfersSegment(
                station_code_pair,
                edge_type,
                interchange_station_code,
                defunct_with_station_code,
            )
