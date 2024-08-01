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

from railrailrail.cli import parse_args


class TestCli:
    def test_parse_args(self):
        assert parse_args(
            [
                "route",
                "--network-file",
                str(pathlib.Path("config_examples", "network_tel_4.toml")),
                "--coordinates-file",
                str(pathlib.Path("config_examples", "station_coordinates.csv")),
                "--start",
                "NE1",
                "--end",
                "NE3",
            ]
        )

        with pytest.raises(SystemExit):
            assert parse_args(["route", "--network-file", "network_tel_4.toml"])

        with pytest.raises(SystemExit):
            assert parse_args(
                ["generate", "--network", "all", "--path", "not_real_directory_path"]
            )
