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
import sys
from argparse import ArgumentParser, Namespace

from railrailrail.config import Config, Stage
from railrailrail.logger import logger
from railrailrail.railgraph import RailGraph


def parse_args(args: list[str]) -> Namespace:
    parser = ArgumentParser(
        prog="railrailrail",
        description="Find fastest route between any 2 stations on the Singapore rail network.",
        epilog="",
    )
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--generate-config", action="store_true", help="Generate network config file."
    )
    mode_group.add_argument(
        "--route",
        action="store_true",
        help="Find fastest route between any 2 station codes.",
    )
    mode_group.add_argument(
        "--interactive",
        action="store_true",
        help="Open interactive terminal user interface.",
    )

    route_group = parser.add_argument_group("route arguments")
    route_group.add_argument(
        "--start",
        type=str,
        default=None,
        help="Origin station code.",
    )
    route_group.add_argument(
        "--end",
        type=str,
        default=None,
        help="Destination station code.",
    )
    route_group.add_argument(
        "--walk", action="store_true", help="Allow station transfers by walking."
    )

    parser.add_argument(
        "--network",
        choices=["now", *Stage.stages],
        default="now",
        help="Choose from train network as it appears today (default), or as it would be at any specified future stage.",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug output.")

    parsed_args = parser.parse_args(args)

    if parsed_args.route:
        if not parsed_args.start or not parsed_args.end:
            parser.error("the following arguments are required: --start, --end")

    return parsed_args


if __name__ == "__main__":  # pragma: no cover
    args: Namespace = parse_args(sys.argv[1:])

    if args.debug:
        logger.setLevel("INFO")

    args.network = (
        "tel_4" if args.network == "now" else args.network
    )  # Contemporary train network; to be updated as the real train network expands.

    network_path = (
        pathlib.Path(__file__).resolve().parent.parent
        / "config"
        / f"network_{args.network}.toml"
    )
    network_path.parent.mkdir(parents=True, exist_ok=True)

    coordinates_path = (
        pathlib.Path(__file__).resolve().parent.parent
        / "config"
        / "station_coordinates.csv"
    )

    if args.generate_config:
        config = Config(Stage(stage=args.network))
        config.update_network_config_file(network_path)

    if args.route:
        rail_graph = RailGraph.from_file(network_path, coordinates_path)
        pathinfo = rail_graph.find_shortest_path(
            start_station_code=args.start.upper(),
            end_station_code=args.end.upper(),
            walk=args.walk,
        )
        print("\n".join(rail_graph.make_directions(pathinfo)))
