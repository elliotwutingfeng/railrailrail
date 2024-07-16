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
import unittest
from collections import OrderedDict, defaultdict

from railrailrail.config import Config
from railrailrail.dataset import Stage


class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.config_phase_2b_3 = Config(Stage("phase_2b_3"))
        self.config_dtl_1 = Config(Stage("dtl_1"))
        self.config_tel_3 = Config(Stage("tel_3"))

    def test_adjacency_matrix(self):
        expected_adjacency_matrix = defaultdict(
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
            expected_adjacency_matrix
        )

    def test_update_network(self):
        pass
