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

from dijkstar import Graph

from railrailrail.utils import StationUtils


class StageMeta(type):
    """Stations added and/or removed at every stage of the MRT/LRT network.

    MRT/LRT Network phases before BPLRT

    * phase_1_1: NS15 Yio Chu Kang - NS19 Toa Payoh | 7 November 1987
    * phase_1_2: NS20 Novena - EW16 Outram Park | 12 December 1987
    * phase_1a: EW17 Tiong Bahru - EW23 Clementi | 12 March 1988
    * phase_2b_1: EW24 Jurong East - EW26 Lakeside | 5 November 1988
    * phase_2b_2: NS13 Yishun - NS14 Khatib | 20 December 1988
    * phase_2a_1: EW 12 Bugis - EW4 Tanah Merah and NS27 Marina Bay | 4 November 1989
    * phase_2a_2: EW3 Simei - EW1 Pasir Ris | 16 December 1989
    * phase_2b_3: NS1 Jurong East - NS4 Choa Chu Kang | 10 March 1990
    * phase_2b_4: EW27 Boon Lay | 6 July 1990
    * woodlands_extension: NS5 Yew Tee - NS11 Sembawang | 10 February 1996

    Sources

    * Phase 1, 1A | Project to go on line in three stages (The Straits Times, 8 July 1986, Page 8) | https://eresources.nlb.gov.sg/newspapers/digitised/article/straitstimes19860708-1.2.54.13.2
    * Phase 2A, 2B | MRT seeks design advice for next two phases (The Business Times, 19 May 1984, Page 1) | https://eresources.nlb.gov.sg/newspapers/digitised/article/biztimes19840519-1.2.6
    * Phase 2B | Last viaduct beam for MRT phase 2B now in place (The Straits Times, 10 January 1988, Page 16) | https://eresources.nlb.gov.sg/newspapers/digitised/article/straitstimes19880110-1.2.22.26
    * Woodlands Extension | Woodlands extension almost ready (The Straits Times, 4 October 1995, Page 3) | https://eresources.nlb.gov.sg/newspapers/digitised/article/straitstimes19951004-1.2.64.3.2
    """

    __stages: types.MappingProxyType = types.MappingProxyType(
        {
            "phase_1_1": (
                ("NS15", "Yio Chu Kang"),
                ("NS16", "Ang Mo Kio"),
                ("NS17", "Bishan"),
                ("NS18", "Braddell"),
                ("NS19", "Toa Payoh"),
            ),  # 7 November 1987
            "phase_1_2": (
                ("EW13", "City Hall"),
                ("EW14", "Raffles Place"),
                ("EW15", "Tanjong Pagar"),
                ("EW16", "Outram Park"),
                ("NS20", "Novena"),
                ("NS21", "Newton"),
                ("NS22", "Orchard"),
                ("NS23", "Somerset"),
                ("NS24", "Dhoby Ghaut"),
                ("NS25", "City Hall"),
                ("NS26", "Raffles Place"),
            ),  # 12 December 1987
            "phase_1a": (
                ("EW17", "Tiong Bahru"),
                ("EW18", "Redhill"),
                ("EW19", "Queenstown"),
                ("EW20", "Commonwealth"),
                ("EW21", "Buona Vista"),
                ("EW23", "Clementi"),
            ),  # 12 March 1988
            "phase_2b_1": (
                ("EW24", "Jurong East"),
                ("EW25", "Chinese Garden"),
                ("EW26", "Lakeside"),
            ),  # 5 November 1988
            "phase_2b_2": (
                ("NS13", "Yishun"),
                ("NS14", "Khatib"),
            ),  # 20 December 1988
            "phase_2a_1": (
                ("EW4", "Tanah Merah"),
                ("EW5", "Bedok"),
                ("EW6", "Kembangan"),
                ("EW7", "Eunos"),
                ("EW8", "Paya Lebar"),
                ("EW9", "Aljunied"),
                ("EW10", "Kallang"),
                ("EW11", "Lavender"),
                ("EW12", "Bugis"),
                ("NS27", "Marina Bay"),
            ),  # 4 November 1989
            "phase_2a_2": (
                ("EW1", "Pasir Ris"),
                ("EW2", "Tampines"),
                ("EW3", "Simei"),
            ),  # 16 December 1989
            "phase_2b_3": (
                ("NS1", "Jurong East"),
                ("NS2", "Bukit Batok"),
                ("NS3", "Bukit Gombak"),
                ("NS4", "Choa Chu Kang"),
            ),  # 10 March 1990
            "phase_2b_4": (("EW27", "Boon Lay"),),  # 6 July 1990
            "woodlands_extension": (
                ("NS5", "Yew Tee"),
                ("NS7", "Kranji"),
                ("NS8", "Marsiling"),
                ("NS9", "Woodlands"),
                ("NS10", "Admiralty"),
                ("NS11", "Sembawang"),
            ),  # 10 February 1996
            "bplrt": (
                ("BP1", "Choa Chu Kang"),
                ("BP2", "South View"),
                ("BP3", "Keat Hong"),
                ("BP4", "Teck Whye"),
                ("BP5", "Phoenix"),
                ("BP6", "Bukit Panjang"),
                ("BP7", "Petir"),
                ("BP8", "Pending"),
                ("BP9", "Bangkit"),
                ("BP10", "Fajar"),
                ("BP11", "Segar"),
                ("BP12", "Jelapang"),
                ("BP13", "Senja"),
                ("BP14", "Ten Mile Junction"),
            ),  # 6 November 1999
            "ewl_expo": (
                ("CG", "Tanah Merah"),
                ("CG1", "Expo"),
            ),  # 10 January 2001
            "dover": (("EW22", "Dover"),),  # 18 October 2001
            "ewl_changi_airport": (("CG2", "Changi Airport"),),  # 8 February 2002
            "sklrt_east_loop": (
                ("STC", "Sengkang"),
                ("SE1", "Compassvale"),
                ("SE2", "Rumbia"),
                ("SE3", "Bakau"),
                ("SE4", "Kangkar"),
                ("SE5", "Ranggung"),
            ),  # 18 January 2003
            "nel": (
                ("NE1", "HarbourFront"),
                ("NE3", "Outram Park"),
                ("NE4", "Chinatown"),
                ("NE5", "Clarke Quay"),
                ("NE6", "Dhoby Ghaut"),
                ("NE7", "Little India"),
                ("NE8", "Farrer Park"),
                ("NE9", "Boon Keng"),
                ("NE10", "Potong Pasir"),
                ("NE12", "Serangoon"),
                ("NE13", "Kovan"),
                ("NE14", "Hougang"),
                ("NE16", "Sengkang"),
                ("NE17", "Punggol"),
            ),  # 20 June 2003
            "pglrt_east_loop_and_sklrt_west_loop": (
                ("PTC", "Punggol"),
                ("PE1", "Cove"),
                ("PE2", "Meridian"),
                ("PE3", "Coral Edge"),
                ("PE4", "Riviera"),
                ("PE5", "Kadaloor"),
                ("SW4", "Thanggam"),
                ("SW5", "Fernvale"),
                ("SW6", "Layar"),
                ("SW7", "Tongkang"),
                ("SW8", "Renjong"),
            ),  # 29 January 2005
            "buangkok": (("NE15", "Buangkok"),),  # 15 January 2006
            "oasis": (("PE6", "Oasis"),),  # 15 June 2007
            "farmway": (("SW2", "Farmway"),),  # 15 November 2007
            "ewl_boon_lay_extension": (
                ("EW28", "Pioneer"),
                ("EW29", "Joo Koon"),
            ),  # 28 February 2009
            "ccl_3": (
                ("CC12", "Bartley"),
                ("CC13", "Serangoon"),
                ("CC14", "Lorong Chuan"),
                ("CC15", "Bishan"),
                ("CC16", "Marymount"),
            ),  # 28 May 2009
            "ccl_1_and_ccl_2": (
                ("CC1", "Dhoby Ghaut"),
                ("CC2", "Bras Basah"),
                ("CC3", "Esplanade"),
                ("CC4", "Promenade"),
                ("CC5", "Nicoll Highway"),
                ("CC6", "Stadium"),
                ("CC7", "Mountbatten"),
                ("CC8", "Dakota"),
                ("CC9", "Paya Lebar"),
                ("CC10", "MacPherson"),
                ("CC11", "Tai Seng"),
            ),  # 17 April 2010
            "ten_mile_junction_temporary_closure": (),  # 10 December 2010
            "woodleigh_and_damai": (
                ("NE11", "Woodleigh"),
                ("PE7", "Damai"),
            ),  # 20 June 2011
            "ccl_4_and_ccl_5": (
                ("CC17", "Caldecott"),
                ("CC19", "Botanic Gardens"),
                ("CC20", "Farrer Road"),
                ("CC21", "Holland Village"),
                ("CC22", "Buona Vista"),
                ("CC23", "one-north"),
                ("CC24", "Kent Ridge"),
                ("CC25", "Haw Par Villa"),
                ("CC26", "Pasir Panjang"),
                ("CC27", "Labrador Park"),
                ("CC28", "Telok Blangah"),
                ("CC29", "HarbourFront"),
            ),  # 8 October 2011
            "ten_mile_junction_reopen": (
                ("BP14", "Ten Mile Junction"),
            ),  # 30 December 2011
            "ccl_e": (
                ("CE0X", "Stadium"),  # Pseudo station_code
                ("CE0Y", "Nicoll Highway"),  # Pseudo station_code
                ("CE0Z", "Promenade"),  # Pseudo station_code
                ("CE1", "Bayfront"),
                ("CE2", "Marina Bay"),
            ),  # 14 January 2012
            "cheng_lim": (("SW1", "Cheng Lim"),),  # 1 January 2013
            "dtl_1": (
                ("DT14", "Bugis"),
                ("DT15", "Promenade"),
                ("DT16", "Bayfront"),
                ("DT17", "Downtown"),
                ("DT18", "Telok Ayer"),
                ("DT19", "Chinatown"),
            ),  # 22 December 2013
            "pglrt_west_loop": (
                ("PW5", "Nibong"),
                ("PW6", "Sumang"),
                ("PW7", "Soo Teck"),
            ),  # 29 June 2014
            "marina_south_pier": (("NS28", "Marina South Pier"),),  # 23 November 2014
            "kupang": (("SW3", "Kupang"),),  # 27 June 2015
            "dtl_2": (
                ("DT1", "Bukit Panjang"),
                ("DT2", "Cashew"),
                ("DT3", "Hillview"),
                ("DT5", "Beauty World"),
                ("DT6", "King Albert Park"),
                ("DT7", "Sixth Avenue"),
                ("DT8", "Tan Kah Kee"),
                ("DT9", "Botanic Gardens"),
                ("DT10", "Stevens"),
                ("DT11", "Newton"),
                ("DT12", "Little India"),
                ("DT13", "Rochor"),
            ),  # 27 December 2015
            "sam_kee": (("PW1", "Sam Kee"),),  # 29 February 2016
            "punggol_point": (("PW3", "Punggol Point"),),  # 29 December 2016
            "samudera": (("PW4", "Samudera"),),  # 31 March 2017
            "ewl_tuas_extension": (
                ("EW30", "Gul Circle"),
                ("EW31", "Tuas Crescent"),
                ("EW32", "Tuas West Road"),
                ("EW33", "Tuas Link"),
            ),  # 18 June 2017
            "dtl_3": (
                ("DT20", "Fort Canning"),
                ("DT21", "Bencoolen"),
                ("DT22", "Jalan Besar"),
                ("DT23", "Bendemeer"),
                ("DT24", "Geylang Bahru"),
                ("DT25", "Mattar"),
                ("DT26", "MacPherson"),
                ("DT27", "Ubi"),
                ("DT28", "Kaki Bukit"),
                ("DT29", "Bedok North"),
                ("DT30", "Bedok Reservoir"),
                ("DT31", "Tampines West"),
                ("DT32", "Tampines"),
                ("DT33", "Tampines East"),
                ("DT34", "Upper Changi"),
                ("DT35", "Expo"),
            ),  # 21 October 2017
            "ten_mile_junction_permanent_closure": (),  # 13 January 2019
            "canberra": (("NS12", "Canberra"),),  # 2 November 2019
            "tel_1": (
                ("TE1", "Woodlands North"),
                ("TE2", "Woodlands"),
                ("TE3", "Woodlands South"),
            ),  # 31 January 2020
            "tel_2": (
                ("TE4", "Springleaf"),
                ("TE5", "Lentor"),
                ("TE6", "Mayflower"),
                ("TE7", "Bright Hill"),
                ("TE8", "Upper Thomson"),
                ("TE9", "Caldecott"),
            ),  # 28 August 2021
            "tel_3": (
                ("TE11", "Stevens"),
                ("TE12", "Napier"),
                ("TE13", "Orchard Boulevard"),
                ("TE14", "Orchard"),
                ("TE15", "Great World"),
                ("TE16", "Havelock"),
                ("TE17", "Outram Park"),
                ("TE18", "Maxwell"),
                ("TE19", "Shenton Way"),
                ("TE20", "Marina Bay"),
                ("TE22", "Gardens by the Bay"),
            ),  # 13 November 2022
            "tel_4": (
                ("TE23", "Tanjong Rhu"),
                ("TE24", "Katong Park"),
                ("TE25", "Tanjong Katong"),
                ("TE26", "Marine Parade"),
                ("TE27", "Marine Terrace"),
                ("TE28", "Siglap"),
                ("TE29", "Bayshore"),
            ),  # 23 June 2024
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

    __stages_defunct: types.MappingProxyType = types.MappingProxyType(
        {
            "ccl_6": (
                ("CE0X", "Stadium"),  # Pseudo station_code
                ("CE0Y", "Nicoll Highway"),  # Pseudo station_code
                ("CE0Z", "Promenade"),  # Pseudo station_code
                ("CE1", "Bayfront"),
                ("CE2", "Marina Bay"),
            ),
            "ten_mile_junction_temporary_closure": (("BP14", "Ten Mile Junction"),),
            "ten_mile_junction_permanent_closure": (("BP14", "Ten Mile Junction"),),
            "cg_tel_c": (
                ("CG2", "Changi Airport"),
                ("CG1", "Expo"),
                ("CG", "Tanah Merah"),
            ),
        }
    )

    def __new__(cls, name, bases, dct):
        stations: set[tuple[str, str]] = set()
        for stage, stage_stations in cls.__stages.items():
            stage_stations_set = set(stage_stations)
            stage_defunct_stations_set = set(cls.__stages_defunct.get(stage, ()))

            stations_added_and_removed_at_same_stage = stage_stations_set.intersection(
                stage_defunct_stations_set
            )
            if stations_added_and_removed_at_same_stage:
                raise AttributeError(
                    f"Never add and remove the same station at the same stage: {stations_added_and_removed_at_same_stage}"
                )  # pragma: no cover
            existing_stations_added_again = stage_stations_set.intersection(stations)
            if existing_stations_added_again:
                raise AttributeError(
                    f"Do not attempt to re-add existing stations: {existing_stations_added_again}"
                )  # pragma: no cover
            non_existent_stations_to_be_removed = stage_defunct_stations_set.difference(
                stations
            )
            if non_existent_stations_to_be_removed:
                raise AttributeError(
                    f"Do not attempt to remove non-existing stations: {non_existent_stations_to_be_removed}"
                )  # pragma: no cover

            stations.update(stage_stations_set)
            stations.difference_update(stage_defunct_stations_set)

        if len(stations) != len(
            set(
                " ".join([station_code, station_name])
                for station_code, station_name in stations
            )
        ):
            raise AttributeError(
                "No station code should be paired with more than one name."
            )  # pragma: no cover

        cls.stages = cls.__stages
        cls.stages_defunct = cls.__stages_defunct
        return super().__new__(cls, name, bases, dct)


class Stage(metaclass=StageMeta):
    def __init__(self, stage: str):
        """Setup `Stage` with stations operational as of given `stage`.

        Args:
            stage (str): Rail network Stage codename. Must be in `Stage.stages`.

        Raises:
            ValueError: No such stage.
        """
        if stage not in Stage.stages:
            raise ValueError(f"No such stage: {stage}")
        self.stations: set[tuple[str, str]] = set()
        for (
            current_stage,
            current_stage_stations,
        ) in Stage.stages.items():
            self.stations.update(current_stage_stations)
            if current_stage in Stage.stages_defunct:
                self.stations.difference_update(Stage.stages_defunct[current_stage])
            if (
                current_stage == stage
            ):  # Add/Remove stations from all stages up to and including `stage`.
                break


class WalkingTrainMapMeta(type):
    """LTA Walking Train Map (WTM)

    https://www.lta.gov.sg/content/dam/ltagov/who_we_are/statistics_and_publications/pdf/connect_nov_2018_fa_12nov.pdf
    """

    __routes: tuple[tuple[str, str, int]] = (
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

    def __new__(cls, name, bases, dct):
        pairs: set[tuple[str, str]] = set()
        for station_name_1, station_name_2, duration in cls.__routes:
            if (
                station_name_1 == station_name_2
                or not isinstance(station_name_1, str)
                or not isinstance(station_name_2, str)
                or type(duration) not in (float, int)
                or duration <= 0
            ):
                raise AttributeError(
                    f"Route must be between 2 different names with a positive duration. Got {station_name_1}, {station_name_2}, {duration}"
                )  # pragma: no cover
            pair = tuple(sorted([station_name_1, station_name_2]))
            if pair in pairs:
                raise AttributeError(
                    f"Duplicate route not allowed: {station_name_1}, {station_name_2}"
                )  # pragma: no cover
            pairs.add(pair)
        cls.routes = cls.__routes
        return super().__new__(cls, name, bases, dct)


class WalkingTrainMap(metaclass=WalkingTrainMapMeta):
    pass


class ConditionalInterchange:
    """A conditional interchange is a station that is positioned between different sections of the
    same line that are not directly connected to each other. For example, STC Sengkang is the
    conditional interchange for the Sengkang LRT East Loop and Sengkang LRT West Loop.

    A conditional interchange behaves as an interchange only when previous segment and next segment are
    of specific types as outlined in `segment_pairs`. For example, there will be an interchange transfer when
    moving from "bahar_east" to "bahar_west", but not from "bahar_west" to "bahar_east".

    Nearly all segments adjacent to a conditional interchange are non-sequential,
    except for BP6-BP7, JS6-JS7, JS7-JS8 which are sequential.
    """

    segments: tuple[tuple[str, str, str]] = (
        ("BP5", "BP6", "bukit_panjang_main"),
        ("BP6", "BP13", "bukit_panjang_service_a"),
        ("BP6", "BP7", "bukit_panjang_service_b"),
        ("BP6", "BP14", "bukit_panjang_service_c"),
        #
        ("STC", "SE1", "sengkang_east_loop"),
        ("STC", "SE5", "sengkang_east_loop"),
        ("STC", "SW1", "sengkang_west_loop"),
        (
            "STC",
            "SW2",
            "sengkang_west_loop",
        ),  # Defunct with SW1 | cheng_lim
        (
            "STC",
            "SW4",
            "sengkang_west_loop",
        ),  # Defunct with SW2 | farmway
        ("STC", "SW8", "sengkang_west_loop"),
        #
        ("PTC", "PE1", "punggol_east_loop"),
        ("PTC", "PE5", "punggol_east_loop"),  # Defunct with PE6 | oasis
        ("PTC", "PE6", "punggol_east_loop"),  # Defunct with PE7 | woodleigh_and_damai
        ("PTC", "PE7", "punggol_east_loop"),
        ("PTC", "PW1", "punggol_west_loop"),
        ("PTC", "PW5", "punggol_west_loop"),  # Defunct with PW1 | sam_kee
        ("PTC", "PW7", "punggol_west_loop"),
        #
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
        #
        ("JS6", "JS7", "bahar_east"),
        ("JS7", "JW1", "bahar_west"),
        ("JS7", "JS8", "bahar_south"),
    )

    # TODO change to dict that maps pairs to transfer durations.
    segment_pairs: frozenset[tuple[str, str]] = frozenset(
        (
            ("punggol_west_loop", "punggol_east_loop"),
            ("punggol_east_loop", "punggol_west_loop"),
            #
            ("sengkang_west_loop", "sengkang_east_loop"),
            ("sengkang_east_loop", "sengkang_west_loop"),
            #
            ("bukit_panjang_service_a", "bukit_panjang_service_b"),
            ("bukit_panjang_service_b", "bukit_panjang_service_a"),
            # Assume Service C always involves transfer at BP6.
            ("bukit_panjang_service_c", "bukit_panjang_main"),
            ("bukit_panjang_service_c", "bukit_panjang_service_a"),
            ("bukit_panjang_service_c", "bukit_panjang_service_b"),
            ("bukit_panjang_main", "bukit_panjang_service_c"),
            ("bukit_panjang_service_a", "bukit_panjang_service_c"),
            ("bukit_panjang_service_b", "bukit_panjang_service_c"),
            #
            ("promenade_south", "promenade_west"),
            ("promenade_west", "promenade_south"),
            ("promenade_east", "promenade_south"),
            #
            ("bahar_east", "bahar_west"),
            ("bahar_west", "bahar_south"),
            ("bahar_south", "bahar_east"),
        )
    )

    @classmethod
    def is_conditional_interchange_transfer(
        cls, previous_edge_type: str, next_edge_type: str
    ) -> bool:  # TODO this should return (bool, float) where float is transfer duration
        return (previous_edge_type, next_edge_type) in cls.segment_pairs


class Terminal:
    __looped_lines = frozenset(
        (
            "BP",
            "JS",
            "JW",
            "PE",
            "PTC",
            "PW",
            "SE",
            "STC",
            "SW",
        )
    )  # These lines all terminate at one station like JS1, except for BPLRT (Service A/B -> BP1, Service C -> BP14).

    pseudo_stations: types.MappingProxyType = types.MappingProxyType(
        {
            "CE0X": "CC6",
            "CE0Y": "CC5",
            "CE0Z": "CC4",
            "JE0": "JS3",
        }
    )  # For temporary Circle Line Extension and Jurong Region Line East Branch.

    @classmethod
    def get_terminal(cls, graph: Graph, start: str, end: str) -> str | None:
        if start == end:
            raise ValueError(f"start and end must be different. Got {start} and {end}")
        start_line_code, _, _ = StationUtils.to_station_code_components(start)
        end_line_code, _, _ = StationUtils.to_station_code_components(end)
        if start_line_code in cls.__looped_lines or (
            start_line_code == "CC" and "CC34" in graph
        ):
            # Circle Line becomes a looped line at Stage 6.
            return None
        if start_line_code != end_line_code:
            raise ValueError(
                f"start_line_code and end_line_code must be the same. Got {start_line_code} and {end_line_code}"
            )
        is_ascending: bool = (
            sorted([start, end], key=StationUtils.to_station_code_components)[0]
            == start
        )
        # From start, traverse nodes in ascending or descending order with same line code until dead end is reached.
        next_node = start
        while True:
            node_and_neighbours = sorted(
                list(
                    node
                    for node in graph.get_incoming(next_node)
                    if node[:2] == start_line_code
                )
                + [next_node],
                key=StationUtils.to_station_code_components,
            )
            next_node_index = node_and_neighbours.index(next_node) + (
                1 if is_ascending else -1
            )
            if next_node_index < 0 or next_node_index >= len(node_and_neighbours):
                return next_node
            next_node = node_and_neighbours[next_node_index]


class DurationsMeta(type):
    """Standard duration presets."""

    # All possible rail segments between any 2 adjacent stations on the same line.
    # This includes segments that have yet to exist (e.g. NS3 -> NS3A),
    # and segments that no longer exist or will be removed in the future (e.g. BP6 -> BP14, NS3 -> NS4).
    __segments: tuple = (
        ("BP1-BP2", ("duration", 2)),
        ("BP2-BP3", ("duration", 1)),
        ("BP3-BP4", ("duration", 2)),
        ("BP4-BP5", ("duration", 1)),
        ("BP5-BP6", ("duration", 1)),
        ("BP6-BP7", ("duration", 1)),
        ("BP6-BP13", ("duration", 2)),
        ("BP6-BP14", ("duration", 1)),
        ("BP7-BP8", ("duration", 2)),
        ("BP8-BP9", ("duration", 1)),
        ("BP9-BP10", ("duration", 2)),
        ("BP10-BP11", ("duration", 1)),
        ("BP11-BP12", ("duration", 1)),
        ("BP12-BP13", ("duration", 2)),
        ("CC1-CC2", ("duration", 3)),
        ("CC2-CC3", ("duration", 3)),
        ("CC3-CC4", ("duration", 3)),
        ("CC4-CC5", ("duration", 6)),
        ("CC4-CC34", ("duration", 3)),
        ("CC5-CC6", ("duration", 2)),
        ("CC6-CC7", ("duration", 2)),
        ("CC7-CC8", ("duration", 2)),
        ("CC8-CC9", ("duration", 2)),
        ("CC9-CC10", ("duration", 2)),
        ("CC10-CC11", ("duration", 2)),
        ("CC11-CC12", ("duration", 2)),
        ("CC12-CC13", ("duration", 2)),
        ("CC13-CC14", ("duration", 2)),
        ("CC14-CC15", ("duration", 2)),
        ("CC15-CC16", ("duration", 2)),
        ("CC16-CC17", ("duration", 2)),
        ("CC17-CC18", ("duration", 2)),
        ("CC17-CC19", ("duration", 5)),
        ("CC18-CC19", ("duration", 4)),
        ("CC19-CC20", ("duration", 2)),
        ("CC20-CC21", ("duration", 2)),
        ("CC21-CC22", ("duration", 2)),
        ("CC22-CC23", ("duration", 2)),
        ("CC23-CC24", ("duration", 2)),
        ("CC24-CC25", ("duration", 2)),
        ("CC25-CC26", ("duration", 2)),
        ("CC26-CC27", ("duration", 2)),
        ("CC27-CC28", ("duration", 2)),
        ("CC28-CC29", ("duration", 2)),
        ("CC29-CC30", ("duration", 2)),
        ("CC30-CC31", ("duration", 1)),
        ("CC31-CC32", ("duration", 1)),
        ("CC32-CC33", ("duration", 1)),
        ("CC33-CC34", ("duration", 2)),
        ("CC33-DT17", ("duration", 5)),
        ("CE0X-CE0Y", ("duration", 2)),
        ("CE0Y-CE0Z", ("duration", 6)),
        ("CE0Z-CE1", ("duration", 3)),
        ("CE1-CE2", ("duration", 2)),
        ("CG-CG1", ("duration", 3)),
        ("CG1-CG2", ("duration", 4)),
        ("CP1-CP2", ("duration", 4)),
        ("CP2-CP3", ("duration", 6)),
        ("CP3-CP4", ("duration", 4)),
        ("CR1-CR2", ("duration", 4)),
        ("CR2-CR3", ("duration", 6)),
        ("CR3-CR4", ("duration", 3)),
        ("CR4-CR5", ("duration", 3)),
        ("CR5-CR6", ("duration", 2)),
        ("CR6-CR7", ("duration", 8)),
        ("CR7-CR8", ("duration", 2)),
        ("CR8-CR9", ("duration", 4)),
        ("CR9-CR10", ("duration", 3)),
        ("CR10-CR11", ("duration", 3)),
        ("CR11-CR12", ("duration", 2)),
        ("CR12-CR13", ("duration", 3)),
        ("CR13-CR14", ("duration", 9)),
        ("CR14-CR15", ("duration", 3)),
        ("CR15-CR16", ("duration", 2)),
        ("CR16-CR17", ("duration", 4)),
        ("CR17-CR18", ("duration", 2)),
        ("CR18-CR19", ("duration", 5)),
        ("DT-DT1", ("duration", 7)),
        ("DT1-DT2", ("duration", 2)),
        ("DT2-DT3", ("duration", 2)),
        ("DT3-DT4", ("duration", 2)),
        ("DT3-DT5", ("duration", 3)),
        ("DT4-DT5", ("duration", 3)),
        ("DT5-DT6", ("duration", 2)),
        ("DT6-DT7", ("duration", 2)),
        ("DT7-DT8", ("duration", 2)),
        ("DT8-DT9", ("duration", 2)),
        ("DT9-DT10", ("duration", 2)),
        ("DT10-DT11", ("duration", 2)),
        ("DT11-DT12", ("duration", 3)),
        ("DT12-DT13", ("duration", 1)),
        ("DT13-DT14", ("duration", 2)),
        ("DT14-DT15", ("duration", 2)),
        ("DT15-DT16", ("duration", 2)),
        ("DT16-DT17", ("duration", 2)),
        ("DT17-DT18", ("duration", 1)),
        ("DT18-DT19", ("duration", 2)),
        ("DT19-DT20", ("duration", 2)),
        ("DT20-DT21", ("duration", 2)),
        ("DT21-DT22", ("duration", 1)),
        ("DT22-DT23", ("duration", 2)),
        ("DT23-DT24", ("duration", 2)),
        ("DT24-DT25", ("duration", 2)),
        ("DT25-DT26", ("duration", 2)),
        ("DT26-DT27", ("duration", 2)),
        ("DT27-DT28", ("duration", 2)),
        ("DT28-DT29", ("duration", 2)),
        ("DT29-DT30", ("duration", 2)),
        ("DT30-DT31", ("duration", 3)),
        ("DT31-DT32", ("duration", 2)),
        ("DT32-DT33", ("duration", 2)),
        ("DT33-DT34", ("duration", 3)),
        ("DT34-DT35", ("duration", 2)),
        ("DT35-DT36", ("duration", 1)),
        ("DT36-DT37", ("duration", 2)),
        ("EW1-EW2", ("duration", 3)),
        ("EW2-EW3", ("duration", 3)),
        ("EW3-EW4", ("duration", 3)),
        ("EW4-EW5", ("duration", 3)),
        ("EW5-EW6", ("duration", 3)),
        ("EW6-EW7", ("duration", 3)),
        ("EW7-EW8", ("duration", 2)),
        ("EW8-EW9", ("duration", 2)),
        ("EW9-EW10", ("duration", 3)),
        ("EW10-EW11", ("duration", 2)),
        ("EW11-EW12", ("duration", 3)),
        ("EW12-EW13", ("duration", 2)),
        ("EW13-EW14", ("duration", 2)),
        ("EW14-EW15", ("duration", 2)),
        ("EW15-EW16", ("duration", 2)),
        ("EW16-EW17", ("duration", 3)),
        ("EW17-EW18", ("duration", 3)),
        ("EW18-EW19", ("duration", 2)),
        ("EW19-EW20", ("duration", 3)),
        ("EW20-EW21", ("duration", 2)),
        ("EW21-EW22", ("duration", 3)),
        ("EW21-EW23", ("duration", 5)),
        ("EW22-EW23", ("duration", 2)),
        ("EW23-EW24", ("duration", 5)),
        ("EW24-EW25", ("duration", 2)),
        ("EW25-EW26", ("duration", 3)),
        ("EW26-EW27", ("duration", 2)),
        ("EW27-EW28", ("duration", 3)),
        ("EW28-EW29", ("duration", 3)),
        ("EW29-EW30", ("duration", 4)),
        ("EW30-EW31", ("duration", 2)),
        ("EW31-EW32", ("duration", 2)),
        ("EW32-EW33", ("duration", 2)),
        ("JE0-JE1", ("duration", 3)),
        ("JE1-JE2", ("duration", 2)),
        ("JE2-JE3", ("duration", 2)),
        ("JE3-JE4", ("duration", 3)),
        ("JE4-JE5", ("duration", 2)),
        ("JE5-JE6", ("duration", 2)),
        ("JE6-JE7", ("duration", 2)),
        ("JS1-JS2", ("duration", 2)),
        ("JS2-JS3", ("duration", 4)),
        ("JS3-JS4", ("duration", 2)),
        ("JS4-JS5", ("duration", 3)),
        ("JS5-JS6", ("duration", 2)),
        ("JS6-JS7", ("duration", 2)),
        ("JS7-JS8", ("duration", 2)),
        ("JS7-JW1", ("duration", 2)),
        ("JS8-JS9", ("duration", 2)),
        ("JS9-JS10", ("duration", 2)),
        ("JS10-JS11", ("duration", 2)),
        ("JS11-JS12", ("duration", 2)),
        ("JW1-JW2", ("duration", 2)),
        ("JW2-JW3", ("duration", 2)),
        ("JW3-JW4", ("duration", 2)),
        ("JW4-JW5", ("duration", 2)),
        ("NE1-NE3", ("duration", 4)),
        ("NE3-NE4", ("duration", 1)),
        ("NE4-NE5", ("duration", 2)),
        ("NE5-NE6", ("duration", 3)),
        ("NE6-NE7", ("duration", 1)),
        ("NE7-NE8", ("duration", 1)),
        ("NE8-NE9", ("duration", 2)),
        ("NE9-NE10", ("duration", 3)),
        ("NE10-NE11", ("duration", 1)),
        ("NE10-NE12", ("duration", 3)),
        ("NE11-NE12", ("duration", 2)),
        ("NE12-NE13", ("duration", 3)),
        ("NE13-NE14", ("duration", 2)),
        ("NE14-NE15", ("duration", 2)),
        ("NE14-NE16", ("duration", 4)),
        ("NE15-NE16", ("duration", 2)),
        ("NE16-NE17", ("duration", 3)),
        ("NE17-NE18", ("duration", 3)),
        ("NS1-NS2", ("duration", 3)),
        ("NS2-NS3", ("duration", 3)),
        ("NS3-NS3A", ("duration", 2)),
        ("NS3-NS4", ("duration", 4)),
        ("NS3A-NS4", ("duration", 2)),
        ("NS4-NS5", ("duration", 2)),
        ("NS5-NS6", ("duration", 3)),
        ("NS5-NS7", ("duration", 5)),
        ("NS6-NS7", ("duration", 2)),
        ("NS7-NS8", ("duration", 3)),
        ("NS8-NS9", ("duration", 3)),
        ("NS9-NS10", ("duration", 3)),
        ("NS10-NS11", ("duration", 3)),
        ("NS11-NS12", ("duration", 3)),
        ("NS11-NS13", ("duration", 5)),
        ("NS12-NS13", ("duration", 3)),
        ("NS13-NS14", ("duration", 2)),
        ("NS14-NS15", ("duration", 5)),
        ("NS15-NS16", ("duration", 3)),
        ("NS16-NS17", ("duration", 4)),
        ("NS17-NS18", ("duration", 2)),
        ("NS18-NS19", ("duration", 2)),
        ("NS19-NS20", ("duration", 3)),
        ("NS20-NS21", ("duration", 2)),
        ("NS21-NS22", ("duration", 3)),
        ("NS22-NS23", ("duration", 2)),
        ("NS23-NS24", ("duration", 2)),
        ("NS24-NS25", ("duration", 3)),
        ("NS25-NS26", ("duration", 2)),
        ("NS26-NS27", ("duration", 2)),
        ("NS27-NS28", ("duration", 2)),
        ("PE1-PE2", ("duration", 1)),
        ("PE2-PE3", ("duration", 1)),
        ("PE3-PE4", ("duration", 1)),
        ("PE4-PE5", ("duration", 1)),
        ("PE5-PE6", ("duration", 1)),
        ("PE6-PE7", ("duration", 1)),
        ("PTC-PE1", ("duration", 3)),
        ("PTC-PE5", ("duration", 4)),
        ("PTC-PE6", ("duration", 3)),
        ("PTC-PE7", ("duration", 2)),
        ("PTC-PW1", ("duration", 2)),
        ("PTC-PW5", ("duration", 5)),
        ("PTC-PW7", ("duration", 3)),
        ("PW1-PW2", ("duration", 1)),
        ("PW1-PW3", ("duration", 2)),
        ("PW1-PW5", ("duration", 4)),
        ("PW2-PW3", ("duration", 1)),
        ("PW3-PW4", ("duration", 1)),
        ("PW3-PW5", ("duration", 2)),
        ("PW4-PW5", ("duration", 1)),
        ("PW5-PW6", ("duration", 1)),
        ("PW6-PW7", ("duration", 1)),
        ("SE1-SE2", ("duration", 1)),
        ("SE2-SE3", ("duration", 1)),
        ("SE3-SE4", ("duration", 1)),
        ("SE4-SE5", ("duration", 2)),
        ("STC-SE1", ("duration", 2)),
        ("STC-SE5", ("duration", 3)),
        ("STC-SW1", ("duration", 2)),
        ("STC-SW2", ("duration", 3)),
        ("STC-SW4", ("duration", 5)),
        ("STC-SW8", ("duration", 3)),
        ("SW1-SW2", ("duration", 1)),
        ("SW2-SW3", ("duration", 1)),
        ("SW2-SW4", ("duration", 2)),
        ("SW3-SW4", ("duration", 1)),
        ("SW4-SW5", ("duration", 1)),
        ("SW5-SW6", ("duration", 1)),
        ("SW6-SW7", ("duration", 1)),
        ("SW7-SW8", ("duration", 1)),
        ("TE1-TE2", ("duration", 2)),
        ("TE2-TE3", ("duration", 2)),
        ("TE3-TE4", ("duration", 5)),
        ("TE4-TE4A", ("duration", 2)),
        ("TE4-TE5", ("duration", 3)),
        ("TE4A-TE5", ("duration", 2)),
        ("TE5-TE6", ("duration", 3)),
        ("TE6-TE7", ("duration", 2)),
        ("TE7-TE8", ("duration", 2)),
        ("TE8-TE9", ("duration", 3)),
        ("TE9-TE10", ("duration", 2)),
        ("TE9-TE11", ("duration", 4)),
        ("TE10-TE11", ("duration", 2)),
        ("TE11-TE12", ("duration", 3)),
        ("TE12-TE13", ("duration", 1)),
        ("TE13-TE14", ("duration", 2)),
        ("TE14-TE15", ("duration", 2)),
        ("TE15-TE16", ("duration", 2)),
        ("TE16-TE17", ("duration", 2)),
        ("TE17-TE18", ("duration", 2)),
        ("TE18-TE19", ("duration", 1)),
        ("TE19-TE20", ("duration", 2)),
        ("TE20-TE21", ("duration", 2)),
        ("TE20-TE22", ("duration", 3)),
        ("TE21-TE22", ("duration", 1)),
        ("TE22-TE22A", ("duration", 2)),
        ("TE22-TE23", ("duration", 4)),
        ("TE22A-TE23", ("duration", 2)),
        ("TE23-TE24", ("duration", 2)),
        ("TE24-TE25", ("duration", 3)),
        ("TE25-TE26", ("duration", 1)),
        ("TE26-TE27", ("duration", 2)),
        ("TE27-TE28", ("duration", 2)),
        ("TE28-TE29", ("duration", 2)),
        ("TE29-TE30", ("duration", 1)),
        ("TE30-TE31", ("duration", 1)),
        ("TE31-TE32", ("duration", 10)),
        ("TE32-TE33", ("duration", 3)),
        ("TE33-TE34", ("duration", 4)),
        ("TE34-TE35", ("duration", 3)),
    )

    # Transfers at all possible interchanges, including defunct and future interchanges.
    # Estimates based on walking time + waiting time (5 min for MRT / 6 min for LRT).
    #
    # As a simplification, treat transfer time in both directions as equal.
    # TODO: Update in the future when more direction-specific transfer time is available.
    #
    # Rule of thumb for future interchanges
    # elevated/elevated -> 7 min
    # underground/underground -> 9 min
    # underground/elevated -> 12 min
    __interchange_transfers: tuple = (
        ("Ang Mo Kio", 10),
        ("Bayfront", 6),
        ("Bishan", 8),
        ("Boon Lay", 10),
        ("Botanic Gardens", 8),
        ("Bright Hill", 9),
        ("Bugis", 9),
        ("Bukit Panjang", 10),
        ("Buona Vista", 8),
        ("Caldecott", 9),
        ("Changi Airport Terminal 5", 9),
        ("Chinatown", 7),
        ("Choa Chu Kang", 7),
        ("City Hall", 6),
        ("Clementi", 12),
        ("Dhoby Ghaut", 8),
        ("Expo", 8),
        ("HarbourFront", 7),
        ("Hougang", 9),
        ("Jurong East", 7),
        ("King Albert Park", 9),
        ("Little India", 8),
        ("MacPherson", 6),
        ("Marina Bay", 10),
        ("Newton", 9),
        ("Nicoll Highway", 6),  # Interchange for ccl_e
        ("Orchard", 8),
        ("Outram Park", 8),
        ("Pasir Ris", 12),
        ("Paya Lebar", 8),
        ("Promenade", 7),
        ("Punggol", 7),
        ("Raffles Place", 6),
        ("Riviera", 12),
        ("Sengkang", 7),
        ("Serangoon", 8),
        ("Stadium", 6),  # Interchange for ccl_e
        ("Stevens", 7),
        ("Sungei Bedok", 9),
        ("Sungei Kadut", 12),
        ("Tampines", 12),
        ("Tanah Merah", 7),
        ("Tengah", 6),
        ("Woodlands", 9),
    )

    # Transfers at all possible conditional interchanges, including defunct and future conditional interchanges.
    #
    # As a simplification, treat transfer time in both directions as equal.
    # TODO: Update in the future when more direction-specific transfer time is available.
    #
    __conditional_interchange_transfers: tuple = (
        ("Bahar Junction", 6),
        ("Bukit Panjang", 7),
        ("Promenade", 7),
        ("Punggol", 6),
        ("Sengkang", 6),
    )

    def __new__(cls, name, bases, dct):
        cls.segments = dict()
        pairs: set[tuple[str, str]] = set()
        for segment, *details in cls.__segments:
            # Validate segment format
            segment_parts = segment.split("-", 2)
            if len(segment_parts) != 2:
                raise AttributeError(
                    "Segment must consist of 2 station codes separated by a single dash '-'"
                )  # pragma: no cover
            station_code_1, station_code_2 = segment_parts
            if station_code_1 == station_code_2:
                raise AttributeError(
                    f"Segment nodes cannot be the same: {segment}"
                )  # pragma: no cover
            StationUtils.to_station_code_components(
                station_code_1
            )  # Raises ValueError if invalid.
            StationUtils.to_station_code_components(
                station_code_2
            )  # Raises ValueError if invalid.

            # Check for duplicate segments
            pair = tuple(sorted([station_code_1, station_code_2]))
            if pair in pairs:
                raise AttributeError(
                    f"Duplicate segment not allowed: {segment}"
                )  # pragma: no cover
            pairs.add(pair)

            # Validate segment details
            segment_details = dict(details)
            if type(segment_details.get("duration", None)) not in (float, int):
                raise AttributeError(
                    "Segment duration must be int | float."
                )  # pragma: no cover
            cls.segments[segment] = segment_details

        cls.interchange_transfers = {
            station_name: duration
            for station_name, duration in cls.__interchange_transfers
        }
        if len(cls.interchange_transfers) != len(cls.__interchange_transfers):
            raise AttributeError("Duplicate station names are not allowed.")

        cls.conditional_interchange_transfers = {
            station_name: duration
            for station_name, duration in cls.__conditional_interchange_transfers
        }
        if len(cls.conditional_interchange_transfers) != len(
            cls.__conditional_interchange_transfers
        ):
            raise AttributeError("Duplicate station names are not allowed.")

        return super().__new__(cls, name, bases, dct)


class Durations(metaclass=DurationsMeta):
    pass
