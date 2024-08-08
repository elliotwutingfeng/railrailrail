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
import pandas as pd
import shapely.geometry

from railrailrail.railgraph import RailGraph


def contains_point(
    polygon: shapely.geometry.polygon.Polygon, lat: float, lon: float
) -> bool:
    return polygon.contains(shapely.geometry.Point(lon, lat))


def get_stage_journeys(stage: str) -> tuple[str, dict, RailGraph]:
    network_path = (
        pathlib.Path(__file__).parent.parent / "config" / f"network_{stage}.toml"
    )
    coordinates_path = (
        pathlib.Path(__file__).parent.parent / "config" / "station_coordinates.csv"
    )
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


def make_stage_journeys_dataframe(stage: str, journeys: dict):
    df = (
        pd.DataFrame.from_dict(
            journeys,
            orient="index",
            columns=[
                "path_distance",
                "haversine_distance",
                "nodes",
                "edges",
                "costs",
                "total_cost",
            ],
        )
        .reset_index()
        .rename(columns={"index": "start_and_end"})
    )

    df[["start", "end"]] = pd.DataFrame(df["start_and_end"].tolist(), index=df.index)
    df.drop(columns=["start_and_end"], inplace=True)

    df["circuity"] = df["path_distance"] / df["haversine_distance"]

    df.sort_values(
        by=["circuity", "haversine_distance", "path_distance", "start", "end"],
        inplace=True,
    )

    df.name = stage
    return df


def get_station_agg_stats(df: pd.DataFrame, rail_graph: RailGraph) -> pd.DataFrame:
    agg_functions = ["mean", "median", "std"]
    df = df.query(
        "total_cost != 0"
    )  # Remove trips between stations from the same interchange.
    df = (
        df.groupby("start")
        .agg(
            {
                "circuity": agg_functions,
                "path_distance": agg_functions,
                "haversine_distance": agg_functions,
            }
        )
        .reset_index(0)
    )
    df.columns = ["_".join(col).strip("_") for col in df.columns.values]
    df["station_name"] = df["start"].apply(
        lambda station_code: rail_graph.station_code_to_station[
            station_code
        ].station_name
    )

    df["latitude"] = df["start"].apply(
        lambda start: rail_graph.station_coordinates[start].latitude
    )
    df["longitude"] = df["start"].apply(
        lambda start: rail_graph.station_coordinates[start].longitude
    )

    return df


def get_planning_area_to_region_df():
    planning_area_to_region = {
        "ANG MO KIO": "NORTH-EAST",
        "BEDOK": "EAST",
        "BISHAN": "CENTRAL",
        "BOON LAY": "WEST",
        "BUKIT BATOK": "WEST",
        "BUKIT MERAH": "CENTRAL",
        "BUKIT PANJANG": "WEST",
        "BUKIT TIMAH": "CENTRAL",
        "CENTRAL WATER CATCHMENT": "NORTH",
        "CHANGI": "EAST",
        "CHANGI BAY": "EAST",
        "CHOA CHU KANG": "WEST",
        "CLEMENTI": "WEST",
        "DOWNTOWN CORE": "CENTRAL",
        "GEYLANG": "CENTRAL",
        "HOUGANG": "NORTH-EAST",
        "JURONG EAST": "WEST",
        "JURONG WEST": "WEST",
        "KALLANG": "CENTRAL",
        "LIM CHU KANG": "NORTH",
        "MANDAI": "NORTH",
        "MARINA EAST": "CENTRAL",
        "MARINA SOUTH": "CENTRAL",
        "MARINE PARADE": "CENTRAL",
        "MUSEUM": "CENTRAL",
        "NEWTON": "CENTRAL",
        "NORTH-EASTERN ISLANDS": "NORTH-EAST",
        "NOVENA": "CENTRAL",
        "ORCHARD": "CENTRAL",
        "OUTRAM": "CENTRAL",
        "PASIR RIS": "EAST",
        "PAYA LEBAR": "EAST",
        "PIONEER": "WEST",
        "PUNGGOL": "NORTH-EAST",
        "QUEENSTOWN": "CENTRAL",
        "RIVER VALLEY": "CENTRAL",
        "ROCHOR": "CENTRAL",
        "SELETAR": "NORTH-EAST",
        "SEMBAWANG": "NORTH",
        "SENGKANG": "NORTH-EAST",
        "SERANGOON": "NORTH-EAST",
        "SIMPANG": "NORTH",
        "SINGAPORE RIVER": "CENTRAL",
        "SOUTHERN ISLANDS": "CENTRAL",
        "STRAITS VIEW": "CENTRAL",
        "SUNGEI KADUT": "NORTH",
        "TAMPINES": "EAST",
        "TANGLIN": "CENTRAL",
        "TENGAH": "WEST",
        "TOA PAYOH": "CENTRAL",
        "TUAS": "WEST",
        "WESTERN ISLANDS": "WEST",
        "WESTERN WATER CATCHMENT": "WEST",
        "WOODLANDS": "NORTH",
        "YISHUN": "NORTH",
    }
    return (
        pd.DataFrame.from_dict(
            planning_area_to_region, orient="index", columns=["region"]
        )
        .reset_index(0)
        .rename(columns={"index": "planning_area"})
    )
