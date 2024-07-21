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
