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

import pathlib

import pytest

from railrailrail.coordinates import Coordinates


class TestCoordinates:
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, request, mocker):
        self.mocker = mocker
        _ = request

    def test_haversine_distance(self):
        # Bukit Timah Hill Summit to Singapore Parliament House
        assert (
            int(
                Coordinates.haversine_distance(
                    Coordinates(1.354681, 103.776375), Coordinates(1.2891, 103.8504)
                )
            )
            == 11007
        )

    def test_update_coordinates_file(self):
        coordinates_path = pathlib.Path("station_coordinates.csv")
        example_coordinates_path = (
            pathlib.Path(__file__).resolve().parent.parent
            / "config_examples"
            / "station_coordinates.csv"
        )

        mocked_copy = self.mocker.patch("shutil.copy")

        # Modify in-place.
        mocked_open = self.mocker.mock_open()
        mocked_open.return_value.read.side_effect = ["a", "b"]
        mocked_open = self.mocker.patch("builtins.open", mocked_open)
        open_calls = [
            self.mocker.call(example_coordinates_path, "r"),
            self.mocker.call().__enter__(),
            self.mocker.call().read(),
            self.mocker.call().__exit__(None, None, None),
            self.mocker.call(coordinates_path, "r"),
            self.mocker.call().__enter__(),
            self.mocker.call().read(),
            self.mocker.call().__exit__(None, None, None),
            self.mocker.call(coordinates_path, "w"),
            self.mocker.call().__enter__(),
            self.mocker.call().write("- b\n+ a"),
            self.mocker.call().__exit__(None, None, None),
        ]

        Coordinates.update_coordinates_file(coordinates_path)
        mocked_open.assert_has_calls(open_calls)

        # Direct copy.
        mocked_open = self.mocker.mock_open()
        self.mocker.patch("builtins.open", mocked_open)
        Coordinates.update_coordinates_file(coordinates_path)
        mocked_copy.assert_called_once_with(
            src=example_coordinates_path, dst=coordinates_path
        )
