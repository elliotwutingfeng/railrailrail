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
        self.config_phase_1_2 = Config(Stage("phase_1_2"))
        self.config_ewl_expo = Config(Stage("ewl_expo"))
        self.config_dover = Config(Stage("dover"))
        self.config_tel_3 = Config(Stage("tel_3"))

        self.config_phase_1_1_toml_str = (
            "schema = 1\n\n"
            '[stations]\nNS15 = "Yio Chu Kang"\n'
            'NS16 = "Ang Mo Kio"\nNS17 = "Bishan"\nNS18 = "Braddell"\nNS19 = "Toa Payoh"\n\n'
            "[segments]\nNS15-NS16 = {duration_asc = 115, duration_desc = 115, dwell_time_asc = 60, dwell_time_desc = 28}\n"
            "NS16-NS17 = {duration_asc = 160, duration_desc = 160, dwell_time_asc = 28, dwell_time_desc = 28}\n"
            "NS17-NS18 = {duration_asc = 95, duration_desc = 95, dwell_time_asc = 28, dwell_time_desc = 28}\n"
            "NS18-NS19 = {duration_asc = 95, duration_desc = 95, dwell_time_asc = 28, dwell_time_desc = 60}\n\n[transfers]\n\n"
            "[conditional_transfers]\n\n[non_linear_line_terminals]\n\n[station_code_pseudonyms]\n"
        )

    def test_segment_adjacency_matrix(self):
        expected_phase_1_2_segment_adjacency_matrix = defaultdict(
            OrderedDict[str, dict],
            {
                "EW15": OrderedDict(
                    {
                        "EW16": {
                            "duration_asc": 85,
                            "duration_desc": 85,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 60,
                        },
                        "NS26": {
                            "duration_asc": 105,
                            "duration_desc": 105,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        },
                    }
                ),
                "NS15": OrderedDict(
                    {
                        "NS16": {
                            "duration_asc": 115,
                            "duration_desc": 115,
                            "dwell_time_asc": 60,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS16": OrderedDict(
                    {
                        "NS17": {
                            "duration_asc": 160,
                            "duration_desc": 160,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS17": OrderedDict(
                    {
                        "NS18": {
                            "duration_asc": 95,
                            "duration_desc": 95,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS18": OrderedDict(
                    {
                        "NS19": {
                            "duration_asc": 95,
                            "duration_desc": 95,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS19": OrderedDict(
                    {
                        "NS20": {
                            "duration_asc": 110,
                            "duration_desc": 110,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS20": OrderedDict(
                    {
                        "NS21": {
                            "duration_asc": 100,
                            "duration_desc": 100,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS21": OrderedDict(
                    {
                        "NS22": {
                            "duration_asc": 110,
                            "duration_desc": 110,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS22": OrderedDict(
                    {
                        "NS23": {
                            "duration_asc": 100,
                            "duration_desc": 100,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS23": OrderedDict(
                    {
                        "NS24": {
                            "duration_asc": 75,
                            "duration_desc": 75,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS24": OrderedDict(
                    {
                        "NS25": {
                            "duration_asc": 85,
                            "duration_desc": 85,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
                "NS25": OrderedDict(
                    {
                        "NS26": {
                            "duration_asc": 100,
                            "duration_desc": 100,
                            "dwell_time_asc": 28,
                            "dwell_time_desc": 28,
                        }
                    }
                ),
            },
        )
        assert json.dumps(self.config_phase_1_2.segment_adjacency_matrix) == json.dumps(
            expected_phase_1_2_segment_adjacency_matrix
        )

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
        modified.insert(-4, "\n")  # Add newline before [non_linear_line_terminals].
        modified[-4] = (
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
            "[segments]\nNS15-NS16 = {duration_asc = 115, duration_desc = 115, dwell_time_asc = 60, dwell_time_desc = 28}\n"
            "NS16-NS17 = {duration_asc = 160, duration_desc = 160, dwell_time_asc = 28, dwell_time_desc = 28}\n"
            "NS17-NS18 = {duration_asc = 95, duration_desc = 95, dwell_time_asc = 28, dwell_time_desc = 28}\n"
            "NS18-NS19 = {duration_asc = 95, duration_desc = 95, dwell_time_asc = 28, dwell_time_desc = 60}\n\n[transfers]\n\n"
            "[conditional_transfers]\n\n\n# [non_linear_line_terminals]\n[linear_line_terminals] # MODIFIED\n\n[station_code_pseudonyms]"
        )

    def test_update_network_config_file(self):
        config_file_path = pathlib.Path("network_test.toml")

        mocked_open = self.mocker.patch(
            "railrailrail.config.open", self.mocker.mock_open()
        )  # Overwrite existing file.
        self.config_tel_3.update_network_config_file(config_file_path)
        assert mocked_open.call_count == 2

        mocked_open = self.mocker.patch(
            "railrailrail.config.open",
            side_effect=[OSError, self.mocker.mock_open().return_value],
        )  # Create new file if it is empty or does not exist.
        self.config_tel_3.update_network_config_file(config_file_path)
        assert mocked_open.call_count == 2
