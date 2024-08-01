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

import itertools
import pathlib

import dijkstar

from railrailrail.railgraph import RailGraph


def get_stage_journeys(stage: str) -> tuple[str, dict, RailGraph]:
    network_path = pathlib.Path("config_examples") / f"network_{stage}.toml"
    coordinates_path = pathlib.Path("config_examples") / "station_coordinates.csv"
    rail_graph = RailGraph.from_file(network_path, coordinates_path)

    real_stations = {
        station_code: station
        for (station_code, station) in rail_graph.station_code_to_station.items()
        if not station.has_pseudo_station_code
    }  # Exclude pseudo station codes like CE0Y.

    # Run all possible pair permutations of stations on the RailGraph.
    journeys = dict()
    for start, end in itertools.permutations(real_stations, 2):
        try:
            pathinfo = rail_graph.find_shortest_path(start, end, walk=True)
        except dijkstar.algorithm.NoPathError:
            continue  # Skip cases where graph is not strongly connected (e.g. Sengkang LRT before NEL was opened)
        path_distance, haversine_distance = rail_graph.path_and_haversine_distance(
            pathinfo
        )
        if path_distance and haversine_distance:
            journeys[(start, end)] = (
                path_distance,
                haversine_distance,
                pathinfo.nodes,
                pathinfo.edges,
                pathinfo.costs,
                pathinfo.total_cost,
            )
    return stage, journeys, rail_graph
