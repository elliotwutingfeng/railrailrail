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
from collections import OrderedDict, defaultdict

import pytest
import tomlkit

from railrailrail.config import Config
from railrailrail.network.stage import Stage


class TestConfig:
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, request, mocker):
        self.mocker = mocker
        _ = request

    def setup_method(self):
        self.config_phase_2b_3 = Config(Stage("phase_2b_3"))
        self.config_phase_1_1 = Config(Stage("phase_1_1"))
        self.config_ewl_expo = Config(Stage("ewl_expo"))
        self.config_dover = Config(Stage("dover"))
        self.config_tel_3 = Config(Stage("tel_3"))

        self.config_phase_1_1_toml_str = (
            "schema = 1\n\n"
            '[stations]\nNS15 = "Yio Chu Kang"\n'
            'NS16 = "Ang Mo Kio"\nNS17 = "Bishan"\nNS18 = "Braddell"\nNS19 = "Toa Payoh"\n\n'
            "[segments]\nNS15-NS16 = {duration = 180, dwell_time_asc = 60, dwell_time_desc = 28}\n"
            "NS16-NS17 = {duration = 240, dwell_time_asc = 28, dwell_time_desc = 28}\n"
            "NS17-NS18 = {duration = 120, dwell_time_asc = 28, dwell_time_desc = 28}\n"
            "NS18-NS19 = {duration = 120, dwell_time_asc = 28, dwell_time_desc = 60}\n\n[transfers]\n\n"
            "[conditional_transfers]\n\n[non_linear_line_terminals]\n"
        )

    def test_segment_adjacency_matrix(self):
        expected_phase_2b_3_segment_adjacency_matrix = defaultdict(
            OrderedDict[str, dict],
            {
                "EW1": OrderedDict(
                    {
                        "EW2": {
                            "duration": 180,
                            "dwell_time_asc": 60,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW2": OrderedDict(
                    {
                        "EW3": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW3": OrderedDict(
                    {
                        "EW4": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW4": OrderedDict(
                    {
                        "EW5": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW5": OrderedDict(
                    {
                        "EW6": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW6": OrderedDict(
                    {
                        "EW7": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW7": OrderedDict(
                    {
                        "EW8": {
                            "duration": 120,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW8": OrderedDict(
                    {
                        "EW9": {
                            "duration": 120,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW9": OrderedDict(
                    {
                        "EW10": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW10": OrderedDict(
                    {
                        "EW11": {
                            "duration": 120,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW11": OrderedDict(
                    {
                        "EW12": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW12": OrderedDict(
                    {
                        "EW13": {
                            "duration": 120,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 45,
                        }
                    }
                ),
                "EW13": OrderedDict(
                    {
                        "EW14": {
                            "duration": 120,
                            "dwell_time_asc": 45,
                            "dwell_time_desc": 45,
                        }
                    }
                ),
                "EW14": OrderedDict(
                    {
                        "EW15": {
                            "duration": 120,
                            "dwell_time_asc": 45,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW15": OrderedDict(
                    {
                        "EW16": {
                            "duration": 120,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW16": OrderedDict(
                    {
                        "EW17": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW17": OrderedDict(
                    {
                        "EW18": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW18": OrderedDict(
                    {
                        "EW19": {
                            "duration": 120,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW19": OrderedDict(
                    {
                        "EW20": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW20": OrderedDict(
                    {
                        "EW21": {
                            "duration": 120,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW21": OrderedDict(
                    {
                        "EW23": {
                            "duration": 300,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW23": OrderedDict(
                    {
                        "EW24": {
                            "duration": 300,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 45,
                        }
                    }
                ),
                "EW24": OrderedDict(
                    {
                        "EW25": {
                            "duration": 120,
                            "dwell_time_asc": 45,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "EW25": OrderedDict(
                    {
                        "EW26": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 60,
                        }
                    }
                ),
                "NS1": OrderedDict(
                    {
                        "NS2": {
                            "duration": 180,
                            "dwell_time_asc": 60,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS2": OrderedDict(
                    {
                        "NS3": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS3": OrderedDict(
                    {
                        "NS4": {
                            "duration": 240,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 60,
                        }
                    }
                ),
                "NS13": OrderedDict(
                    {
                        "NS14": {
                            "duration": 120,
                            "dwell_time_asc": 60,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS14": OrderedDict(
                    {
                        "NS15": {
                            "duration": 300,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS15": OrderedDict(
                    {
                        "NS16": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS16": OrderedDict(
                    {
                        "NS17": {
                            "duration": 240,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS17": OrderedDict(
                    {
                        "NS18": {
                            "duration": 120,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS18": OrderedDict(
                    {
                        "NS19": {
                            "duration": 120,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS19": OrderedDict(
                    {
                        "NS20": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS20": OrderedDict(
                    {
                        "NS21": {
                            "duration": 120,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS21": OrderedDict(
                    {
                        "NS22": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS22": OrderedDict(
                    {
                        "NS23": {
                            "duration": 120,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS23": OrderedDict(
                    {
                        "NS24": {
                            "duration": 120,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS24": OrderedDict(
                    {
                        "NS25": {
                            "duration": 180,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 45,
                        }
                    }
                ),
                "NS25": OrderedDict(
                    {
                        "NS26": {
                            "duration": 120,
                            "dwell_time_asc": 45,
                            "dwell_time_desc": 45,
                        }
                    }
                ),
                "NS26": OrderedDict(
                    {
                        "NS27": {
                            "duration": 120,
                            "dwell_time_asc": 45,
                            "dwell_time_desc": 60,
                        }
                    }
                ),
            },
        )
        assert json.dumps(
            self.config_phase_2b_3.segment_adjacency_matrix
        ) == json.dumps(expected_phase_2b_3_segment_adjacency_matrix)

    def test_transfer_adjacency_matrix(self):
        expected_phase_2b_3_transfer_adjacency_matrix = defaultdict(
            OrderedDict[str, dict],
            {
                "EW13": OrderedDict({"NS25": {"duration": 360}}),
                "EW14": OrderedDict({"NS26": {"duration": 360}}),
                "EW24": OrderedDict({"NS1": {"duration": 420}}),
                "NS1": OrderedDict({"EW24": {"duration": 420}}),
                "NS25": OrderedDict({"EW13": {"duration": 360}}),
                "NS26": OrderedDict({"EW14": {"duration": 360}}),
            },
        )
        assert json.dumps(
            self.config_phase_2b_3.transfer_adjacency_matrix
        ) == json.dumps(expected_phase_2b_3_transfer_adjacency_matrix)

    def test_make_network(self):
        network = self.config_phase_1_1.make_network()
        assert tomlkit.dumps(network) == self.config_phase_1_1_toml_str

    def test_compare_toml(self):
        original = self.config_phase_1_1_toml_str.split("\n")
        modified = original.copy()
        modified.insert(-2, "\n")  # Add newline before [non_linear_line_terminals].
        modified[-2] = (
            "[linear_line_terminals]"  # Modify [non_linear_line_terminals] to [linear_line_terminals].
        )
        del modified[2]  # Remove [stations].
        del modified[0]  # Remove schema = 1.
        del modified[-1]  # Remove last blank line.
        diffed = Config.compare_toml(original, modified)
        # Only blank lines will be silently added or removed.
        assert diffed == (
            "# schema = 1\n\n"
            '# [stations]\nNS15 = "Yio Chu Kang"\n'
            'NS16 = "Ang Mo Kio"\nNS17 = "Bishan"\nNS18 = "Braddell"\nNS19 = "Toa Payoh"\n\n'
            "[segments]\nNS15-NS16 = {duration = 180, dwell_time_asc = 60, dwell_time_desc = 28}\n"
            "NS16-NS17 = {duration = 240, dwell_time_asc = 28, dwell_time_desc = 28}\n"
            "NS17-NS18 = {duration = 120, dwell_time_asc = 28, dwell_time_desc = 28}\n"
            "NS18-NS19 = {duration = 120, dwell_time_asc = 28, dwell_time_desc = 60}\n\n[transfers]\n\n"
            "[conditional_transfers]\n\n\n# [non_linear_line_terminals]\n[linear_line_terminals] # MODIFIED"
        )

    def test_update_network_config_file(self):
        config_file_path = pathlib.Path("network_test.toml")

        open_calls = [
            self.mocker.call(config_file_path, "r"),
            self.mocker.call().__enter__(),
            self.mocker.call().read(),
            self.mocker.call().__exit__(None, None, None),
            self.mocker.call(config_file_path, "w"),
            self.mocker.call().__enter__(),
            self.mocker.call().write(self.mocker.ANY),
            self.mocker.call().__exit__(None, None, None),
        ]
        mocked_open = self.mocker.patch(
            "railrailrail.config.open", self.mocker.mock_open()
        )
        self.config_tel_3.update_network_config_file(config_file_path)
        mocked_open.assert_has_calls(open_calls, any_order=False)

        open_calls = [
            self.mocker.call(config_file_path, "r"),
            self.mocker.call(config_file_path, "w"),
        ]
        mocked_open = self.mocker.patch(
            "railrailrail.config.open",
            side_effect=[OSError, self.mocker.mock_open().return_value],
        )
        self.config_tel_3.update_network_config_file(config_file_path)
        mocked_open.assert_has_calls(open_calls, any_order=False)
