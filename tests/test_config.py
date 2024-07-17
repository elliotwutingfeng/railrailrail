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

import json
import pathlib
import unittest
from collections import OrderedDict, defaultdict

import pytest
import tomlkit

from railrailrail.config import Config
from railrailrail.dataset import Stage


class TestConfig(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, request, mocker):
        self.mocker = mocker
        _ = request

    def setUp(self) -> None:
        self.config_phase_2b_3 = Config(Stage("phase_2b_3"))
        self.config_phase_1_1 = Config(Stage("phase_1_1"))
        self.config_ewl_expo = Config(Stage("ewl_expo"))
        self.config_dover = Config(Stage("dover"))
        self.config_tel_3 = Config(Stage("tel_3"))

    def test_adjacency_matrix(self):
        expected_phase_2b_3_adjacency_matrix = defaultdict(
            OrderedDict[str, dict],
            {
                "EW1": OrderedDict({"EW2": {"duration": 3}}),
                "EW2": OrderedDict({"EW3": {"duration": 3}}),
                "EW3": OrderedDict({"EW4": {"duration": 3}}),
                "EW4": OrderedDict({"EW5": {"duration": 3}}),
                "EW5": OrderedDict({"EW6": {"duration": 3}}),
                "EW6": OrderedDict({"EW7": {"duration": 3}}),
                "EW7": OrderedDict({"EW8": {"duration": 2}}),
                "EW8": OrderedDict({"EW9": {"duration": 2}}),
                "EW9": OrderedDict({"EW10": {"duration": 3}}),
                "EW10": OrderedDict({"EW11": {"duration": 2}}),
                "EW11": OrderedDict({"EW12": {"duration": 3}}),
                "EW12": OrderedDict({"EW13": {"duration": 2}}),
                "EW13": OrderedDict({"EW14": {"duration": 2}}),
                "EW14": OrderedDict({"EW15": {"duration": 2}}),
                "EW15": OrderedDict({"EW16": {"duration": 2}}),
                "EW16": OrderedDict({"EW17": {"duration": 3}}),
                "EW17": OrderedDict({"EW18": {"duration": 3}}),
                "EW18": OrderedDict({"EW19": {"duration": 2}}),
                "EW19": OrderedDict({"EW20": {"duration": 3}}),
                "EW20": OrderedDict({"EW21": {"duration": 2}}),
                "EW21": OrderedDict({"EW23": {"duration": 5}}),
                "EW23": OrderedDict({"EW24": {"duration": 5}}),
                "EW24": OrderedDict({"EW25": {"duration": 2}}),
                "EW25": OrderedDict({"EW26": {"duration": 3}}),
                "NS1": OrderedDict({"NS2": {"duration": 3}}),
                "NS2": OrderedDict({"NS3": {"duration": 3}}),
                "NS3": OrderedDict({"NS4": {"duration": 4}}),
                "NS13": OrderedDict({"NS14": {"duration": 2}}),
                "NS14": OrderedDict({"NS15": {"duration": 5}}),
                "NS15": OrderedDict({"NS16": {"duration": 3}}),
                "NS16": OrderedDict({"NS17": {"duration": 4}}),
                "NS17": OrderedDict({"NS18": {"duration": 2}}),
                "NS18": OrderedDict({"NS19": {"duration": 2}}),
                "NS19": OrderedDict({"NS20": {"duration": 3}}),
                "NS20": OrderedDict({"NS21": {"duration": 2}}),
                "NS21": OrderedDict({"NS22": {"duration": 3}}),
                "NS22": OrderedDict({"NS23": {"duration": 2}}),
                "NS23": OrderedDict({"NS24": {"duration": 2}}),
                "NS24": OrderedDict({"NS25": {"duration": 3}}),
                "NS25": OrderedDict({"NS26": {"duration": 2}}),
                "NS26": OrderedDict({"NS27": {"duration": 2}}),
            },
        )
        assert json.dumps(self.config_phase_2b_3.adjacency_matrix) == json.dumps(
            expected_phase_2b_3_adjacency_matrix
        )

    def test_update_network(self):
        # Updated from blank slate; everything is NEW.
        network = tomlkit.TOMLDocument()
        Config.update_network(
            network,
            self.config_phase_1_1.stations,
            self.config_phase_1_1.adjacency_matrix,
        )
        assert tomlkit.dumps(network) == (
            'schema = 1\ntransfer_time = 7\ndwell_time = 0.5\n\n[stations]\nNS15 = "Yio Chu Kang" # NEW\n'
            'NS16 = "Ang Mo Kio" # NEW\nNS17 = "Bishan" # NEW\nNS18 = "Braddell" # NEW\nNS19 = "Toa Payoh" # NEW\n\n'
            "[edges]\nNS15-NS16 = {duration = 3} # NEW\nNS16-NS17 = {duration = 4} # NEW\n"
            "NS17-NS18 = {duration = 2} # NEW\nNS18-NS19 = {duration = 2} # NEW\n"
        )

        # Add Dover infill station.
        network = tomlkit.TOMLDocument()
        Config.update_network(
            network,
            self.config_ewl_expo.stations,
            self.config_ewl_expo.adjacency_matrix,
        )
        assert "EW21-EW22" not in network["edges"]
        assert "EW22-EW23" not in network["edges"]
        Config.update_network(
            network,
            self.config_dover.stations,
            self.config_dover.adjacency_matrix,
        )
        assert "EW21-EW22" in network["edges"]
        assert "EW22-EW23" in network["edges"]
        assert "EW21-EW23" in network["edges"]
        assert network["edges"]["EW21-EW23"].trivia.comment == "# DEFUNCT"

        # Modify existing station and edge details.
        network["stations"]["EW22"] = "Dover Test"
        network["edges"]["EW21-EW22"]["duration"] = 42
        Config.update_network(
            network,
            self.config_dover.stations,
            self.config_dover.adjacency_matrix,
        )
        assert network["stations"]["EW22"].trivia.comment.startswith("# NEW ->")
        assert network["edges"]["EW21-EW22"].trivia.comment.startswith("# NEW ->")

        # Defunct station.
        network["stations"]["XY1"] = "Test"
        network["edges"]["EW21-XY1"] = {"duration": 5}
        Config.update_network(
            network,
            self.config_dover.stations,
            self.config_dover.adjacency_matrix,
        )
        assert network["stations"]["XY1"].trivia.comment == "# DEFUNCT"
        assert network["edges"]["EW21-XY1"].trivia.comment == "# DEFUNCT"

    def test_update_network_config_file(self):
        path = pathlib.Path("network_test.toml")
        mocked_open = self.mocker.patch(
            "railrailrail.config.open", self.mocker.mock_open()
        )
        self.config_tel_3.update_network_config_file(path)
        calls = [
            self.mocker.call(path, "rb"),
            self.mocker.call().__enter__(),
            self.mocker.call().read(),
            self.mocker.call().__exit__(None, None, None),
            self.mocker.call(path, "w"),
            self.mocker.call().__enter__(),
            self.mocker.call().write(self.mocker.ANY),
            self.mocker.call().__exit__(None, None, None),
        ]
        mocked_open.assert_has_calls(calls, any_order=False)
