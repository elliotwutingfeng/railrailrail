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
from argparse import ArgumentParser

from railrailrail.config import Config, RailExpansion
from railrailrail.logger import logger
from railrailrail.railgraph import RailGraph

if __name__ == "__main__":
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
        choices=["now"] + list(RailExpansion.future_stages.keys()),
        default="now",
        help="Choose from train network as it appears today (default), or as it would be at any specified future stage.",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug output.")
    args = parser.parse_args()

    if args.debug:
        logger.setLevel("INFO")

    network_path = (
        pathlib.Path(__file__).resolve().parent.parent
        / "config"
        / ("network.toml" if args.network == "now" else f"network_{args.network}.toml")
    )
    network_path.parent.mkdir(parents=True, exist_ok=True)

    coordinates_path = (
        pathlib.Path(__file__).resolve().parent.parent
        / "config"
        / "station_coordinates.csv"
    )

    if args.generate_config:
        config = Config(RailExpansion(args.network))
        config.update_network_config(network_path)

    if args.route:
        if not args.start or not args.end:
            parser.error("the following arguments are required: --start, --end")
        rail_graph = RailGraph.from_file(network_path, coordinates_path)
        pathinfo = rail_graph.find_shortest_path(
            start=args.start.upper(), end=args.end.upper(), walk=args.walk
        )
        print("\n".join(rail_graph.make_directions(pathinfo)))
