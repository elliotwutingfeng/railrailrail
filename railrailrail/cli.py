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
from railrailrail.coordinates import Coordinates
from railrailrail.logger import logger
from railrailrail.railgraph import RailGraph


def parse_args(args: list[str]) -> Namespace:
    parser = ArgumentParser(
        prog="railrailrail",
        description="Route planner for all stages of the Singapore MRT/LRT rail network (1987-2040+).",
        epilog="",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug output.")

    subparser_description = "Calculate fastest route or generate preset config files."
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help=subparser_description,
        description=subparser_description,
    )
    generate_parser_description = "Generate config file(s) with preset values."
    generate_parser = subparsers.add_parser(
        "generate",
        help=generate_parser_description,
        description=generate_parser_description,
    )
    route_parser_description = "Find fastest route between any 2 station codes."
    route_parser = subparsers.add_parser(
        "route", help=route_parser_description, description=route_parser_description
    )

    generate_group = generate_parser.add_mutually_exclusive_group(required=True)
    generate_group.add_argument(
        "--coordinates",
        action="store_true",
        help="Generate train station coordinates file.",
    )
    generate_group.add_argument(
        "--network",
        choices=["all", *Stage.stages],
        help="Generate preset network config file(s) for train network stage. Use 'all' to generate preset network config files for all stages.",
    )

    generate_parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="Path to save generated file at.",
    )

    route_group = route_parser.add_argument_group("route arguments")
    route_group.add_argument(
        "--start",
        type=str,
        default=None,
        required=True,
        help="Origin station code.",
    )
    route_group.add_argument(
        "--end",
        type=str,
        default=None,
        required=True,
        help="Destination station code.",
    )
    route_group.add_argument(
        "--walk", action="store_true", help="Allow station transfers by walking."
    )
    route_group.add_argument(
        "--network-file",
        type=str,
        default=None,
        required=True,
        help="Path to network config file.",
    )
    route_group.add_argument(
        "--coordinates-file",
        type=str,
        default=None,
        required=True,
        help="Path to station coordinates file.",
    )

    parsed_args = parser.parse_args(args)

    if (
        parsed_args.command == "generate"
        and parsed_args.network == "all"
        and not pathlib.Path(parsed_args.path).is_dir()
    ):
        raise parser.error(
            "when --network is 'all', --path must be path to an existing directory."
        )
    return parsed_args


if __name__ == "__main__":  # pragma: no cover
    args: Namespace = parse_args(sys.argv[1:])

    if args.debug:
        logger.setLevel("INFO")

    if args.command == "generate":
        if args.network:
            networks: list[str] = (
                list(Stage.stages) if args.network == "all" else [args.network]
            )
            network_path = pathlib.Path(args.path)
            for network in networks:
                config = Config(Stage(stage=network))
                network_filepath = (
                    network_path / f"network_{network}.toml"
                    if args.network == "all"
                    else network_path
                )
                config.update_network_config_file(network_filepath)
        if args.coordinates:
            Coordinates.update_coordinates_file(pathlib.Path(args.path))

    if args.command == "route":
        rail_graph = RailGraph.from_file(args.network_file, args.coordinates_file)
        pathinfo = rail_graph.find_shortest_path(
            start_station_code=args.start.upper(),
            end_station_code=args.end.upper(),
            walk=args.walk,
        )
        print("\n".join(rail_graph.make_directions(pathinfo)))
