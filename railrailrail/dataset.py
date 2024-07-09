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

import types
from collections import defaultdict

from railrailrail.logger import logger
from railrailrail.utils import StationUtils


class RailExpansion:
    future_stages: types.MappingProxyType = types.MappingProxyType(
        {
            "punggol_coast_extension": (("NE18", "Punggol Coast"),),  # 2024
            "teck_lee": (("PW2", "Teck Lee"),),  # 2024
            "hume": (("DT4", "Hume"),),  # 2025
            "tel_5_and_dtl_3e": (
                ("TE30", "Bedok South"),
                ("TE31", "Sungei Bedok"),
                ("DT36", "Xilin"),
                ("DT37", "Sungei Bedok"),
            ),  # 2026
            "ccl_6": (
                ("CC30", "Keppel"),
                ("CC31", "Cantonment"),
                ("CC32", "Prince Edward Road"),
                ("CC33", "Marina Bay"),
                ("CC34", "Bayfront"),
            ),  # 2026
            "jrl_1": (
                ("JS1", "Choa Chu Kang"),
                ("JS2", "Choa Chu Kang West"),
                ("JS3", "Tengah"),
                ("JS4", "Hong Kah"),
                ("JS5", "Corporation"),
                ("JS6", "Jurong West"),
                ("JS7", "Bahar Junction"),
                ("JS8", "Boon Lay"),
                ("JW1", "Gek Poh"),
                ("JW2", "Tawas"),
            ),  # 2027
            "founders_memorial": (("TE22A", "Founders' Memorial"),),  # 2028
            "jrl_2": (
                ("JE0", "Tengah"),  # Pseudo station_code
                ("JE1", "Tengah Plantation"),
                ("JE2", "Tengah Park"),
                ("JE3", "Bukit Batok West"),
                ("JE4", "Toh Guan"),
                ("JE5", "Jurong East"),
                ("JE6", "Jurong Town Hall"),
                ("JE7", "Pandan Reservoir"),
            ),  # 2028
            "jrl_3": (
                ("JS9", "Enterprise"),
                ("JS10", "Tukang"),
                ("JS11", "Jurong Hill"),
                ("JS12", "Jurong Pier"),
                ("JW3", "Nanyang Gateway"),
                ("JW4", "Nanyang Crescent"),
                ("JW5", "Peng Kang Hill"),
            ),  # 2029
            "crl_1": (
                ("CR2", "Aviation Park"),
                ("CR3", "Loyang"),
                ("CR4", "Pasir Ris East"),
                ("CR5", "Pasir Ris"),
                ("CR6", "Tampines North"),
                ("CR7", "Defu"),
                ("CR8", "Hougang"),
                ("CR9", "Serangoon North"),
                ("CR10", "Tavistock"),
                ("CR11", "Ang Mo Kio"),
                ("CR12", "Teck Ghee"),
                ("CR13", "Bright Hill"),
            ),  # 2030
            "crl_2": (
                ("CR14", "Turf City"),
                ("CR15", "King Albert Park"),
                ("CR16", "Maju"),
                ("CR17", "Clementi"),
                ("CR18", "West Coast"),
                ("CR19", "Jurong Lake District"),
            ),  # 2032
            "crl_pe": (
                ("CP1", "Pasir Ris"),
                ("CP2", "Elias"),
                ("CP3", "Riviera"),
                ("CP4", "Punggol"),
            ),  # 2032
            "brickland": (("NS3A", "Brickland"),),  # 2034
            "cg_tel_c": (
                ("CR1", "Changi Airport Terminal 5"),
                ("TE32", "Changi Airport Terminal 5"),
                ("TE33", "Changi Airport"),
                ("TE34", "Expo"),
                ("TE35", "Tanah Merah"),
            ),  # 2040
            "future": (
                ("CC18", "Bukit Brown"),
                ("DT", "Sungei Kadut"),
                ("NS6", "Sungei Kadut"),
                ("TE4A", "Tagore"),
                ("TE10", "Mount Pleasant"),
                ("TE21", "Marina South"),
            ),  # Unknown opening dates
        }
    )

    future_stages_defunct: types.MappingProxyType = types.MappingProxyType(
        {
            "ccl_6": (
                ("CE0X", "Stadium"),  # Pseudo station_code
                ("CE0Y", "Nicoll Highway"),  # Pseudo station_code
                ("CE0Z", "Promenade"),  # Pseudo station_code
                ("CE1", "Bayfront"),
                ("CE2", "Marina Bay"),
            ),
            "cg_tel_c": (
                ("CG2", "Changi Airport"),
                ("CG1", "Expo"),
                ("CG", "Tanah Merah"),
            ),
        }
    )

    def __init__(self, stage: str | None = None) -> None:
        self.new_stations: set[tuple[str, str]] = set()
        self.defunct_stations: set[tuple[str, str]] = set()
        if stage not in RailExpansion.future_stages:
            return
        for (
            current_stage,
            current_stage_stations,
        ) in RailExpansion.future_stages.items():
            self.new_stations.update(current_stage_stations)
            if current_stage in RailExpansion.future_stages_defunct:
                self.defunct_stations.update(
                    RailExpansion.future_stages_defunct[current_stage]
                )
            if (
                current_stage == stage
            ):  # Add stations from all stages up to and including `stage`.
                break

    def update_stations(self, stations: set[tuple[str, str]]) -> None:
        for station_code, station_name in self.new_stations:
            stations.add((station_code, station_name))
        for station_code, station_name in self.defunct_stations:
            try:
                stations.remove((station_code, station_name))
            except KeyError:
                logger.info("Key %s not found", station_code)


class WalkingTrainMap:
    """LTA Walking Train Map (WTM)"""

    routes: tuple[tuple[str, str, int]] = (
        ("Bras Basah", "Bencoolen", 2),
        ("Dhoby Ghaut", "Bencoolen", 5),
        ("Esplanade", "City Hall", 5),
        ("Marina Bay", "Downtown", 5),
        ("Rochor", "Jalan Besar", 5),
        ("Telok Ayer", "Raffles Place", 5),
        ("Shenton Way", "Downtown", 6),
        ("Bras Basah", "City Hall", 7),
        ("Downtown", "Raffles Place", 7),
        ("Maxwell", "Tanjong Pagar", 8),
        ("Telok Ayer", "Tanjong Pagar", 8),
        ("Jalan Besar", "Bugis", 9),
        ("Rochor", "Bencoolen", 9),
        ("Boon Keng", "Bendemeer", 10),
        ("Bras Basah", "Bugis", 10),
        ("Chinatown", "Maxwell", 10),
        ("Clarke Quay", "Raffles Place", 10),
        ("Fort Canning", "Clarke Quay", 10),
        ("Little India", "Jalan Besar", 10),
        ("Shenton Way", "Tanjong Pagar", 10),
        ("Chinatown", "Raffles Place", 11),
        ("Maxwell", "Telok Ayer", 11),
        ("Esplanade", "Bugis", 12),
        ("Shenton Way", "Raffles Place", 12),
    )


class SemiInterchange:
    """A semi-interchange is a station that is positioned between different sections of the
    same line that are not directly connected to each other. For example, STC Sengkang is the
    semi-interchange for the Sengkang LRT East Loop and Sengkang LRT West Loop.

    A semi-interchange behaves as an interchange only when previous edge and next edge are of specific types
    as outlined in `edge pairs`. For example, there will be an interchange transfer when
    moving from "bahar_east" to "bahar_west", but not from "bahar_west" to "bahar_east".

    Nearly all edges adjacent to a semi-interchange are non-sequential,
    except for BP6-BP7, JS6-JS7, JS7-JS8 which are sequential.
    """

    edges: tuple[tuple[str, str, str]] = (
        ("BP6", "BP13", "bukit_panjang_service_a"),
        ("BP6", "BP7", "bukit_panjang_service_b"),
        ("STC", "SW1", "sengkang_west_loop"),
        ("STC", "SW8", "sengkang_west_loop"),
        ("STC", "SE1", "sengkang_east_loop"),
        ("STC", "SE5", "sengkang_east_loop"),
        ("PTC", "PW1", "punggol_west_loop"),
        ("PTC", "PW7", "punggol_west_loop"),
        ("PTC", "PE1", "punggol_east_loop"),
        ("PTC", "PE7", "punggol_east_loop"),
        (
            "CC4",
            "CC5",
            "promenade_east",
        ),
        (
            "CC3",
            "CC4",
            "promenade_west",
        ),
        (
            "CC4",
            "CC34",
            "promenade_south",
        ),
        ("JS6", "JS7", "bahar_east"),
        ("JS7", "JW1", "bahar_west"),
        ("JS7", "JS8", "bahar_south"),
    )

    edge_pairs: frozenset[tuple[str, str]] = frozenset(
        (
            ("punggol_west_loop", "punggol_east_loop"),
            ("punggol_east_loop", "punggol_west_loop"),
            ("sengkang_west_loop", "sengkang_east_loop"),
            ("sengkang_east_loop", "sengkang_west_loop"),
            ("bukit_panjang_service_a", "bukit_panjang_service_b"),
            ("bukit_panjang_service_b", "bukit_panjang_service_a"),
            ("promenade_south", "promenade_west"),
            ("promenade_west", "promenade_south"),
            ("promenade_east", "promenade_south"),
            ("bahar_east", "bahar_west"),
            ("bahar_west", "bahar_south"),
            ("bahar_south", "bahar_east"),
        )
    )

    @classmethod
    def is_semi_interchange_transfer(cls, previous_edge_type: str, next_edge_type: str):
        return (previous_edge_type, next_edge_type) in cls.edge_pairs


class Terminal:
    lines_with_unusual_terminals = frozenset(
        (
            "BP",
            "CE",
            "JS",
            "JW",
            "JE",
            "PTC",
            "PE",
            "PW",
            "STC",
            "SE",
            "SW",
        )
    )

    @classmethod
    def get_terminals(cls, station_codes: set[str]):
        station_codes_by_line_code = defaultdict(list)
        for station_code in station_codes:
            line_code, _, _ = StationUtils.to_station_code_components(station_code)
            if line_code in cls.lines_with_unusual_terminals:
                continue  # JS + LRT lines all terminate at a single main station. JW terminates at JS1 Choa Chu Kang.
            station_codes_by_line_code[line_code].append(station_code)

        terminals_by_line_code: dict[str, tuple[str, str]] = dict()
        for line_code in station_codes_by_line_code:
            if len(station_codes_by_line_code[line_code]) < 2:
                raise ValueError("A line must have at least 2 stations.")
            station_codes_by_line_code[line_code].sort(
                key=StationUtils.to_station_code_components
            )
            terminals_by_line_code[line_code] = (
                station_codes_by_line_code[line_code][0],
                station_codes_by_line_code[line_code][-1],
            )
        return terminals_by_line_code


class Durations:
    """Standard durations for all adjacent rail edges on the same line.
    This includes edges that have yet to exist (e.g. NS3 -> NS3A),
    and edges that will be removed in the future (e.g. NS3 -> NS4).
    """

    edges = {
        "BP1-BP2": {"duration": 2},
        "BP2-BP3": {"duration": 1},
        "BP3-BP4": {"duration": 2},
        "BP4-BP5": {"duration": 1},
        "BP5-BP6": {"duration": 1},
        "BP6-BP7": {"duration": 1},
        "BP6-BP13": {"duration": 2},
        "BP7-BP8": {"duration": 2},
        "BP8-BP9": {"duration": 1},
        "BP9-BP10": {"duration": 2},
        "BP10-BP11": {"duration": 1},
        "BP11-BP12": {"duration": 1},
        "BP12-BP13": {"duration": 2},
        "CC1-CC2": {"duration": 3},
        "CC2-CC3": {"duration": 3},
        "CC3-CC4": {"duration": 3},
        "CC4-CC5": {"duration": 6},
        "CC4-CC34": {"duration": 3},
        "CC5-CC6": {"duration": 2},
        "CC6-CC7": {"duration": 2},
        "CC7-CC8": {"duration": 2},
        "CC8-CC9": {"duration": 2},
        "CC9-CC10": {"duration": 2},
        "CC10-CC11": {"duration": 2},
        "CC11-CC12": {"duration": 2},
        "CC12-CC13": {"duration": 2},
        "CC13-CC14": {"duration": 2},
        "CC14-CC15": {"duration": 2},
        "CC15-CC16": {"duration": 2},
        "CC16-CC17": {"duration": 2},
        "CC17-CC18": {"duration": 2},
        "CC17-CC19": {"duration": 5},
        "CC18-CC19": {"duration": 4},
        "CC19-CC20": {"duration": 2},
        "CC20-CC21": {"duration": 2},
        "CC21-CC22": {"duration": 2},
        "CC22-CC23": {"duration": 2},
        "CC23-CC24": {"duration": 2},
        "CC24-CC25": {"duration": 2},
        "CC25-CC26": {"duration": 2},
        "CC26-CC27": {"duration": 2},
        "CC27-CC28": {"duration": 2},
        "CC28-CC29": {"duration": 2},
        "CC29-CC30": {"duration": 2},
        "CC30-CC31": {"duration": 1},
        "CC31-CC32": {"duration": 1},
        "CC32-CC33": {"duration": 1},
        "CC33-CC34": {"duration": 2},
        "CC33-DT17": {"duration": 5},
        "CE0X-CE0Y": {"duration": 2},
        "CE0Y-CE0Z": {"duration": 6},
        "CE0Z-CE1": {"duration": 3},
        "CE1-CE2": {"duration": 2},
        "CG-CG1": {"duration": 3},
        "CG1-CG2": {"duration": 4},
        "CP1-CP2": {"duration": 4},
        "CP2-CP3": {"duration": 6},
        "CP3-CP4": {"duration": 4},
        "CR1-CR2": {"duration": 4},
        "CR2-CR3": {"duration": 6},
        "CR3-CR4": {"duration": 3},
        "CR4-CR5": {"duration": 3},
        "CR5-CR6": {"duration": 2},
        "CR6-CR7": {"duration": 8},
        "CR7-CR8": {"duration": 2},
        "CR8-CR9": {"duration": 4},
        "CR9-CR10": {"duration": 3},
        "CR10-CR11": {"duration": 3},
        "CR11-CR12": {"duration": 2},
        "CR12-CR13": {"duration": 3},
        "CR13-CR14": {"duration": 9},
        "CR14-CR15": {"duration": 3},
        "CR15-CR16": {"duration": 2},
        "CR16-CR17": {"duration": 4},
        "CR17-CR18": {"duration": 2},
        "CR18-CR19": {"duration": 5},
        "DT-DT1": {"duration": 7},
        "DT1-DT2": {"duration": 2},
        "DT2-DT3": {"duration": 2},
        "DT3-DT4": {"duration": 2},
        "DT3-DT5": {"duration": 3},
        "DT4-DT5": {"duration": 3},
        "DT5-DT6": {"duration": 2},
        "DT6-DT7": {"duration": 2},
        "DT7-DT8": {"duration": 2},
        "DT8-DT9": {"duration": 2},
        "DT9-DT10": {"duration": 2},
        "DT10-DT11": {"duration": 2},
        "DT11-DT12": {"duration": 3},
        "DT12-DT13": {"duration": 1},
        "DT13-DT14": {"duration": 2},
        "DT14-DT15": {"duration": 2},
        "DT15-DT16": {"duration": 2},
        "DT16-DT17": {"duration": 2},
        "DT17-DT18": {"duration": 1},
        "DT18-DT19": {"duration": 2},
        "DT19-DT20": {"duration": 2},
        "DT20-DT21": {"duration": 2},
        "DT21-DT22": {"duration": 1},
        "DT22-DT23": {"duration": 2},
        "DT23-DT24": {"duration": 2},
        "DT24-DT25": {"duration": 2},
        "DT25-DT26": {"duration": 2},
        "DT26-DT27": {"duration": 2},
        "DT27-DT28": {"duration": 2},
        "DT28-DT29": {"duration": 2},
        "DT29-DT30": {"duration": 2},
        "DT30-DT31": {"duration": 3},
        "DT31-DT32": {"duration": 2},
        "DT32-DT33": {"duration": 2},
        "DT33-DT34": {"duration": 3},
        "DT34-DT35": {"duration": 2},
        "DT35-DT36": {"duration": 1},
        "DT36-DT37": {"duration": 2},
        "EW1-EW2": {"duration": 3},
        "EW2-EW3": {"duration": 3},
        "EW3-EW4": {"duration": 3},
        "EW4-EW5": {"duration": 3},
        "EW5-EW6": {"duration": 3},
        "EW6-EW7": {"duration": 3},
        "EW7-EW8": {"duration": 2},
        "EW8-EW9": {"duration": 2},
        "EW9-EW10": {"duration": 3},
        "EW10-EW11": {"duration": 2},
        "EW11-EW12": {"duration": 3},
        "EW12-EW13": {"duration": 2},
        "EW13-EW14": {"duration": 2},
        "EW14-EW15": {"duration": 2},
        "EW15-EW16": {"duration": 2},
        "EW16-EW17": {"duration": 3},
        "EW17-EW18": {"duration": 3},
        "EW18-EW19": {"duration": 2},
        "EW19-EW20": {"duration": 3},
        "EW20-EW21": {"duration": 2},
        "EW21-EW22": {"duration": 3},
        "EW22-EW23": {"duration": 2},
        "EW23-EW24": {"duration": 5},
        "EW24-EW25": {"duration": 2},
        "EW25-EW26": {"duration": 3},
        "EW26-EW27": {"duration": 2},
        "EW27-EW28": {"duration": 3},
        "EW28-EW29": {"duration": 3},
        "EW29-EW30": {"duration": 4},
        "EW30-EW31": {"duration": 2},
        "EW31-EW32": {"duration": 2},
        "EW32-EW33": {"duration": 2},
        "JE0-JE1": {"duration": 3},
        "JE1-JE2": {"duration": 2},
        "JE2-JE3": {"duration": 2},
        "JE3-JE4": {"duration": 3},
        "JE4-JE5": {"duration": 2},
        "JE5-JE6": {"duration": 2},
        "JE6-JE7": {"duration": 2},
        "JS1-JS2": {"duration": 2},
        "JS2-JS3": {"duration": 4},
        "JS3-JS4": {"duration": 2},
        "JS4-JS5": {"duration": 3},
        "JS5-JS6": {"duration": 2},
        "JS6-JS7": {"duration": 2},
        "JS7-JS8": {"duration": 2},
        "JS7-JW1": {"duration": 2},
        "JS8-JS9": {"duration": 2},
        "JS9-JS10": {"duration": 2},
        "JS10-JS11": {"duration": 2},
        "JS11-JS12": {"duration": 2},
        "JW1-JW2": {"duration": 2},
        "JW2-JW3": {"duration": 2},
        "JW3-JW4": {"duration": 2},
        "JW4-JW5": {"duration": 2},
        "NE1-NE3": {"duration": 4},
        "NE3-NE4": {"duration": 1},
        "NE4-NE5": {"duration": 2},
        "NE5-NE6": {"duration": 3},
        "NE6-NE7": {"duration": 1},
        "NE7-NE8": {"duration": 1},
        "NE8-NE9": {"duration": 2},
        "NE9-NE10": {"duration": 3},
        "NE10-NE11": {"duration": 1},
        "NE11-NE12": {"duration": 2},
        "NE12-NE13": {"duration": 3},
        "NE13-NE14": {"duration": 2},
        "NE14-NE15": {"duration": 2},
        "NE15-NE16": {"duration": 2},
        "NE16-NE17": {"duration": 3},
        "NE17-NE18": {"duration": 3},
        "NS1-NS2": {"duration": 3},
        "NS2-NS3": {"duration": 3},
        "NS3-NS3A": {"duration": 2},
        "NS3-NS4": {"duration": 4},
        "NS3A-NS4": {"duration": 2},
        "NS4-NS5": {"duration": 2},
        "NS5-NS6": {"duration": 3},
        "NS5-NS7": {"duration": 5},
        "NS6-NS7": {"duration": 2},
        "NS7-NS8": {"duration": 3},
        "NS8-NS9": {"duration": 3},
        "NS9-NS10": {"duration": 3},
        "NS10-NS11": {"duration": 3},
        "NS11-NS12": {"duration": 3},
        "NS12-NS13": {"duration": 3},
        "NS13-NS14": {"duration": 2},
        "NS14-NS15": {"duration": 5},
        "NS15-NS16": {"duration": 3},
        "NS16-NS17": {"duration": 4},
        "NS17-NS18": {"duration": 2},
        "NS18-NS19": {"duration": 2},
        "NS19-NS20": {"duration": 3},
        "NS20-NS21": {"duration": 2},
        "NS21-NS22": {"duration": 3},
        "NS22-NS23": {"duration": 2},
        "NS23-NS24": {"duration": 2},
        "NS24-NS25": {"duration": 3},
        "NS25-NS26": {"duration": 2},
        "NS26-NS27": {"duration": 2},
        "NS27-NS28": {"duration": 2},
        "PE1-PE2": {"duration": 1},
        "PE2-PE3": {"duration": 1},
        "PE3-PE4": {"duration": 1},
        "PE4-PE5": {"duration": 1},
        "PE5-PE6": {"duration": 1},
        "PE6-PE7": {"duration": 1},
        "PTC-PW1": {"duration": 2},
        "PTC-PW7": {"duration": 3},
        "PTC-PE1": {"duration": 3},
        "PTC-PE7": {"duration": 2},
        "PW1-PW2": {"duration": 1},
        "PW1-PW3": {"duration": 2},
        "PW2-PW3": {"duration": 1},
        "PW3-PW4": {"duration": 1},
        "PW4-PW5": {"duration": 1},
        "PW5-PW6": {"duration": 1},
        "PW6-PW7": {"duration": 1},
        "SE1-SE2": {"duration": 1},
        "SE2-SE3": {"duration": 1},
        "SE3-SE4": {"duration": 1},
        "SE4-SE5": {"duration": 2},
        "STC-SW1": {"duration": 2},
        "STC-SW8": {"duration": 3},
        "STC-SE1": {"duration": 2},
        "STC-SE5": {"duration": 3},
        "SW1-SW2": {"duration": 1},
        "SW2-SW3": {"duration": 1},
        "SW3-SW4": {"duration": 1},
        "SW4-SW5": {"duration": 1},
        "SW5-SW6": {"duration": 1},
        "SW6-SW7": {"duration": 1},
        "SW7-SW8": {"duration": 1},
        "TE1-TE2": {"duration": 2},
        "TE2-TE3": {"duration": 2},
        "TE3-TE4": {"duration": 5},
        "TE4-TE4A": {"duration": 2},
        "TE4-TE5": {"duration": 3},
        "TE4A-TE5": {"duration": 2},
        "TE5-TE6": {"duration": 3},
        "TE6-TE7": {"duration": 2},
        "TE7-TE8": {"duration": 2},
        "TE8-TE9": {"duration": 3},
        "TE9-TE10": {"duration": 2},
        "TE9-TE11": {"duration": 4},
        "TE10-TE11": {"duration": 2},
        "TE11-TE12": {"duration": 3},
        "TE12-TE13": {"duration": 1},
        "TE13-TE14": {"duration": 2},
        "TE14-TE15": {"duration": 2},
        "TE15-TE16": {"duration": 2},
        "TE16-TE17": {"duration": 2},
        "TE17-TE18": {"duration": 2},
        "TE18-TE19": {"duration": 1},
        "TE19-TE20": {"duration": 2},
        "TE20-TE21": {"duration": 2},
        "TE20-TE22": {"duration": 3},
        "TE21-TE22": {"duration": 1},
        "TE22-TE22A": {"duration": 2},
        "TE22-TE23": {"duration": 4},
        "TE22A-TE23": {"duration": 2},
        "TE23-TE24": {"duration": 2},
        "TE24-TE25": {"duration": 3},
        "TE25-TE26": {"duration": 1},
        "TE26-TE27": {"duration": 2},
        "TE27-TE28": {"duration": 2},
        "TE28-TE29": {"duration": 2},
        "TE29-TE30": {"duration": 1},
        "TE30-TE31": {"duration": 1},
        "TE31-TE32": {"duration": 10},
        "TE32-TE33": {"duration": 3},
        "TE33-TE34": {"duration": 4},
        "TE34-TE35": {"duration": 3},
    }
