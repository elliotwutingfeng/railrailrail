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

from railrailrail.utils import GeographicUtils


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
