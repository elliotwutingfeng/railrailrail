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
import shutil
import sys
from argparse import ArgumentParser, Namespace

from railrailrail.config import Config, Stage
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
        default="all",
        help="Generate preset network config file(s) for train network stage. Use 'all' to generate preset network config files for all stages. Defaults to 'all'.",
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

    return parsed_args


if __name__ == "__main__":  # pragma: no cover
    args: Namespace = parse_args(sys.argv[1:])

    if args.debug:
        logger.setLevel("INFO")

    parent_path: pathlib.Path = pathlib.Path(__file__).resolve().parent

    if args.command == "generate":
        if args.network:
            networks: list[str] = (
                list(Stage.stages) if args.network == "all" else [args.network]
            )
            for network in networks:
                config = Config(Stage(stage=network))
                network_path = parent_path.parent / "config" / f"network_{network}.toml"
                network_path.parent.mkdir(parents=True, exist_ok=True)
                # No inline comments (e.g. # NEW) will be added if file does not exist yet.
                config.update_network_config_file(
                    network_path, do_not_comment_new_lines=not network_path.is_file()
                )
        if args.coordinates:
            coordinates_path = parent_path.parent / "config" / "station_coordinates.csv"
            example_coordinates_path = (
                parent_path.parent / "config_examples" / "station_coordinates.csv"
            )
            if coordinates_path.is_file():
                raise FileExistsError(
                    f"Coordinates file already exists at {coordinates_path}. Remove it before generating a new coordinates file."
                )
            shutil.copy(src=example_coordinates_path, dst=coordinates_path)

    if args.command == "route":
        rail_graph = RailGraph.from_file(args.network_file, args.coordinates_file)
        pathinfo = rail_graph.find_shortest_path(
            start_station_code=args.start.upper(),
            end_station_code=args.end.upper(),
            walk=args.walk,
        )
        print("\n".join(rail_graph.make_directions(pathinfo)))
