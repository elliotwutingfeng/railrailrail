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

import collections
import types

from railrailrail.dataset.station import Station


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

    __stages: types.MappingProxyType[str, tuple[Station]] = types.MappingProxyType(
        {
            "phase_1_1": (
                Station("NS15", "Yio Chu Kang"),
                Station("NS16", "Ang Mo Kio"),
                Station("NS17", "Bishan"),
                Station("NS18", "Braddell"),
                Station("NS19", "Toa Payoh"),
            ),  # 7 November 1987
            "phase_1_2": (
                Station("EW13", "City Hall"),
                Station("EW14", "Raffles Place"),
                Station("EW15", "Tanjong Pagar"),
                Station("EW16", "Outram Park"),
                Station("NS20", "Novena"),
                Station("NS21", "Newton"),
                Station("NS22", "Orchard"),
                Station("NS23", "Somerset"),
                Station("NS24", "Dhoby Ghaut"),
                Station("NS25", "City Hall"),
                Station("NS26", "Raffles Place"),
            ),  # 12 December 1987
            "phase_1a": (
                Station("EW17", "Tiong Bahru"),
                Station("EW18", "Redhill"),
                Station("EW19", "Queenstown"),
                Station("EW20", "Commonwealth"),
                Station("EW21", "Buona Vista"),
                Station("EW23", "Clementi"),
            ),  # 12 March 1988
            "phase_2b_1": (
                Station("EW24", "Jurong East"),
                Station("EW25", "Chinese Garden"),
                Station("EW26", "Lakeside"),
            ),  # 5 November 1988
            "phase_2b_2": (
                Station("NS13", "Yishun"),
                Station("NS14", "Khatib"),
            ),  # 20 December 1988
            "phase_2a_1": (
                Station("EW4", "Tanah Merah"),
                Station("EW5", "Bedok"),
                Station("EW6", "Kembangan"),
                Station("EW7", "Eunos"),
                Station("EW8", "Paya Lebar"),
                Station("EW9", "Aljunied"),
                Station("EW10", "Kallang"),
                Station("EW11", "Lavender"),
                Station("EW12", "Bugis"),
                Station("NS27", "Marina Bay"),
            ),  # 4 November 1989
            "phase_2a_2": (
                Station("EW1", "Pasir Ris"),
                Station("EW2", "Tampines"),
                Station("EW3", "Simei"),
            ),  # 16 December 1989
            "phase_2b_3": (
                Station("NS1", "Jurong East"),
                Station("NS2", "Bukit Batok"),
                Station("NS3", "Bukit Gombak"),
                Station("NS4", "Choa Chu Kang"),
            ),  # 10 March 1990
            "phase_2b_4": (Station("EW27", "Boon Lay"),),  # 6 July 1990
            "woodlands_extension": (
                Station("NS5", "Yew Tee"),
                Station("NS7", "Kranji"),
                Station("NS8", "Marsiling"),
                Station("NS9", "Woodlands"),
                Station("NS10", "Admiralty"),
                Station("NS11", "Sembawang"),
            ),  # 10 February 1996
            "bplrt": (
                Station("BP1", "Choa Chu Kang"),
                Station("BP2", "South View"),
                Station("BP3", "Keat Hong"),
                Station("BP4", "Teck Whye"),
                Station("BP5", "Phoenix"),
                Station("BP6", "Bukit Panjang"),
                Station("BP7", "Petir"),
                Station("BP8", "Pending"),
                Station("BP9", "Bangkit"),
                Station("BP10", "Fajar"),
                Station("BP11", "Segar"),
                Station("BP12", "Jelapang"),
                Station("BP13", "Senja"),
                Station("BP14", "Ten Mile Junction"),
            ),  # 6 November 1999
            "ewl_expo": (
                Station("CG", "Tanah Merah"),
                Station("CG1", "Expo"),
            ),  # 10 January 2001
            "dover": (Station("EW22", "Dover"),),  # 18 October 2001
            "ewl_changi_airport": (
                Station("CG2", "Changi Airport"),
            ),  # 8 February 2002
            "sklrt_east_loop": (
                Station("STC", "Sengkang"),
                Station("SE1", "Compassvale"),
                Station("SE2", "Rumbia"),
                Station("SE3", "Bakau"),
                Station("SE4", "Kangkar"),
                Station("SE5", "Ranggung"),
            ),  # 18 January 2003
            "nel": (
                Station("NE1", "HarbourFront"),
                Station("NE3", "Outram Park"),
                Station("NE4", "Chinatown"),
                Station("NE5", "Clarke Quay"),
                Station("NE6", "Dhoby Ghaut"),
                Station("NE7", "Little India"),
                Station("NE8", "Farrer Park"),
                Station("NE9", "Boon Keng"),
                Station("NE10", "Potong Pasir"),
                Station("NE12", "Serangoon"),
                Station("NE13", "Kovan"),
                Station("NE14", "Hougang"),
                Station("NE16", "Sengkang"),
                Station("NE17", "Punggol"),
            ),  # 20 June 2003
            "pglrt_east_loop_and_sklrt_west_loop": (
                Station("PTC", "Punggol"),
                Station("PE1", "Cove"),
                Station("PE2", "Meridian"),
                Station("PE3", "Coral Edge"),
                Station("PE4", "Riviera"),
                Station("PE5", "Kadaloor"),
                Station("SW4", "Thanggam"),
                Station("SW5", "Fernvale"),
                Station("SW6", "Layar"),
                Station("SW7", "Tongkang"),
                Station("SW8", "Renjong"),
            ),  # 29 January 2005
            "buangkok": (Station("NE15", "Buangkok"),),  # 15 January 2006
            "oasis": (Station("PE6", "Oasis"),),  # 15 June 2007
            "farmway": (Station("SW2", "Farmway"),),  # 15 November 2007
            "ewl_boon_lay_extension": (
                Station("EW28", "Pioneer"),
                Station("EW29", "Joo Koon"),
            ),  # 28 February 2009
            "ccl_3": (
                Station("CC12", "Bartley"),
                Station("CC13", "Serangoon"),
                Station("CC14", "Lorong Chuan"),
                Station("CC15", "Bishan"),
                Station("CC16", "Marymount"),
            ),  # 28 May 2009
            "ccl_1_and_ccl_2": (
                Station("CC1", "Dhoby Ghaut"),
                Station("CC2", "Bras Basah"),
                Station("CC3", "Esplanade"),
                Station("CC4", "Promenade"),
                Station("CC5", "Nicoll Highway"),
                Station("CC6", "Stadium"),
                Station("CC7", "Mountbatten"),
                Station("CC8", "Dakota"),
                Station("CC9", "Paya Lebar"),
                Station("CC10", "MacPherson"),
                Station("CC11", "Tai Seng"),
            ),  # 17 April 2010
            "ten_mile_junction_temporary_closure": (),  # 10 December 2010
            "woodleigh_and_damai": (
                Station("NE11", "Woodleigh"),
                Station("PE7", "Damai"),
            ),  # 20 June 2011
            "ccl_4_and_ccl_5": (
                Station("CC17", "Caldecott"),
                Station("CC19", "Botanic Gardens"),
                Station("CC20", "Farrer Road"),
                Station("CC21", "Holland Village"),
                Station("CC22", "Buona Vista"),
                Station("CC23", "one-north"),
                Station("CC24", "Kent Ridge"),
                Station("CC25", "Haw Par Villa"),
                Station("CC26", "Pasir Panjang"),
                Station("CC27", "Labrador Park"),
                Station("CC28", "Telok Blangah"),
                Station("CC29", "HarbourFront"),
            ),  # 8 October 2011
            "ten_mile_junction_reopen": (
                Station("BP14", "Ten Mile Junction"),
            ),  # 30 December 2011
            "ccl_e": (
                Station("CE0X", "Stadium"),  # Pseudo station_code
                Station("CE0Y", "Nicoll Highway"),  # Pseudo station_code
                Station("CE0Z", "Promenade"),  # Pseudo station_code
                Station("CE1", "Bayfront"),
                Station("CE2", "Marina Bay"),
            ),  # 14 January 2012
            "cheng_lim": (Station("SW1", "Cheng Lim"),),  # 1 January 2013
            "dtl_1": (
                Station("DT14", "Bugis"),
                Station("DT15", "Promenade"),
                Station("DT16", "Bayfront"),
                Station("DT17", "Downtown"),
                Station("DT18", "Telok Ayer"),
                Station("DT19", "Chinatown"),
            ),  # 22 December 2013
            "pglrt_west_loop": (
                Station("PW5", "Nibong"),
                Station("PW6", "Sumang"),
                Station("PW7", "Soo Teck"),
            ),  # 29 June 2014
            "marina_south_pier": (
                Station("NS28", "Marina South Pier"),
            ),  # 23 November 2014
            "kupang": (Station("SW3", "Kupang"),),  # 27 June 2015
            "dtl_2": (
                Station("DT1", "Bukit Panjang"),
                Station("DT2", "Cashew"),
                Station("DT3", "Hillview"),
                Station("DT5", "Beauty World"),
                Station("DT6", "King Albert Park"),
                Station("DT7", "Sixth Avenue"),
                Station("DT8", "Tan Kah Kee"),
                Station("DT9", "Botanic Gardens"),
                Station("DT10", "Stevens"),
                Station("DT11", "Newton"),
                Station("DT12", "Little India"),
                Station("DT13", "Rochor"),
            ),  # 27 December 2015
            "sam_kee": (Station("PW1", "Sam Kee"),),  # 29 February 2016
            "punggol_point": (Station("PW3", "Punggol Point"),),  # 29 December 2016
            "samudera": (Station("PW4", "Samudera"),),  # 31 March 2017
            "ewl_tuas_extension": (
                Station("EW30", "Gul Circle"),
                Station("EW31", "Tuas Crescent"),
                Station("EW32", "Tuas West Road"),
                Station("EW33", "Tuas Link"),
            ),  # 18 June 2017
            "dtl_3": (
                Station("DT20", "Fort Canning"),
                Station("DT21", "Bencoolen"),
                Station("DT22", "Jalan Besar"),
                Station("DT23", "Bendemeer"),
                Station("DT24", "Geylang Bahru"),
                Station("DT25", "Mattar"),
                Station("DT26", "MacPherson"),
                Station("DT27", "Ubi"),
                Station("DT28", "Kaki Bukit"),
                Station("DT29", "Bedok North"),
                Station("DT30", "Bedok Reservoir"),
                Station("DT31", "Tampines West"),
                Station("DT32", "Tampines"),
                Station("DT33", "Tampines East"),
                Station("DT34", "Upper Changi"),
                Station("DT35", "Expo"),
            ),  # 21 October 2017
            "ten_mile_junction_permanent_closure": (),  # 13 January 2019
            "canberra": (Station("NS12", "Canberra"),),  # 2 November 2019
            "tel_1": (
                Station("TE1", "Woodlands North"),
                Station("TE2", "Woodlands"),
                Station("TE3", "Woodlands South"),
            ),  # 31 January 2020
            "tel_2": (
                Station("TE4", "Springleaf"),
                Station("TE5", "Lentor"),
                Station("TE6", "Mayflower"),
                Station("TE7", "Bright Hill"),
                Station("TE8", "Upper Thomson"),
                Station("TE9", "Caldecott"),
            ),  # 28 August 2021
            "tel_3": (
                Station("TE11", "Stevens"),
                Station("TE12", "Napier"),
                Station("TE13", "Orchard Boulevard"),
                Station("TE14", "Orchard"),
                Station("TE15", "Great World"),
                Station("TE16", "Havelock"),
                Station("TE17", "Outram Park"),
                Station("TE18", "Maxwell"),
                Station("TE19", "Shenton Way"),
                Station("TE20", "Marina Bay"),
                Station("TE22", "Gardens by the Bay"),
            ),  # 13 November 2022
            "tel_4": (
                Station("TE23", "Tanjong Rhu"),
                Station("TE24", "Katong Park"),
                Station("TE25", "Tanjong Katong"),
                Station("TE26", "Marine Parade"),
                Station("TE27", "Marine Terrace"),
                Station("TE28", "Siglap"),
                Station("TE29", "Bayshore"),
            ),  # 23 June 2024
            "punggol_coast_extension": (Station("NE18", "Punggol Coast"),),  # 2024
            "teck_lee": (Station("PW2", "Teck Lee"),),  # 2024
            "hume": (Station("DT4", "Hume"),),  # 2025
            "tel_5_and_dtl_3e": (
                Station("TE30", "Bedok South"),
                Station("TE31", "Sungei Bedok"),
                Station("DT36", "Xilin"),
                Station("DT37", "Sungei Bedok"),
            ),  # 2026
            "ccl_6": (
                Station("CC30", "Keppel"),
                Station("CC31", "Cantonment"),
                Station("CC32", "Prince Edward Road"),
                Station("CC33", "Marina Bay"),
                Station("CC34", "Bayfront"),
            ),  # 2026
            "jrl_1": (
                Station("JS1", "Choa Chu Kang"),
                Station("JS2", "Choa Chu Kang West"),
                Station("JS3", "Tengah"),
                Station("JS4", "Hong Kah"),
                Station("JS5", "Corporation"),
                Station("JS6", "Jurong West"),
                Station("JS7", "Bahar Junction"),
                Station("JS8", "Boon Lay"),
                Station("JW1", "Gek Poh"),
                Station("JW2", "Tawas"),
            ),  # 2027
            "founders_memorial": (Station("TE22A", "Founders' Memorial"),),  # 2028
            "jrl_2": (
                Station("JE0", "Tengah"),  # Pseudo station_code
                Station("JE1", "Tengah Plantation"),
                Station("JE2", "Tengah Park"),
                Station("JE3", "Bukit Batok West"),
                Station("JE4", "Toh Guan"),
                Station("JE5", "Jurong East"),
                Station("JE6", "Jurong Town Hall"),
                Station("JE7", "Pandan Reservoir"),
            ),  # 2028
            "jrl_3": (
                Station("JS9", "Enterprise"),
                Station("JS10", "Tukang"),
                Station("JS11", "Jurong Hill"),
                Station("JS12", "Jurong Pier"),
                Station("JW3", "Nanyang Gateway"),
                Station("JW4", "Nanyang Crescent"),
                Station("JW5", "Peng Kang Hill"),
            ),  # 2029
            "crl_1": (
                Station("CR2", "Aviation Park"),
                Station("CR3", "Loyang"),
                Station("CR4", "Pasir Ris East"),
                Station("CR5", "Pasir Ris"),
                Station("CR6", "Tampines North"),
                Station("CR7", "Defu"),
                Station("CR8", "Hougang"),
                Station("CR9", "Serangoon North"),
                Station("CR10", "Tavistock"),
                Station("CR11", "Ang Mo Kio"),
                Station("CR12", "Teck Ghee"),
                Station("CR13", "Bright Hill"),
            ),  # 2030
            "crl_2": (
                Station("CR14", "Turf City"),
                Station("CR15", "King Albert Park"),
                Station("CR16", "Maju"),
                Station("CR17", "Clementi"),
                Station("CR18", "West Coast"),
                Station("CR19", "Jurong Lake District"),
            ),  # 2032
            "crl_pe": (
                Station("CP1", "Pasir Ris"),
                Station("CP2", "Elias"),
                Station("CP3", "Riviera"),
                Station("CP4", "Punggol"),
            ),  # 2032
            "brickland": (Station("NS3A", "Brickland"),),  # 2034
            "cg_tel_c": (
                Station("CR1", "Changi Airport Terminal 5"),
                Station("TE32", "Changi Airport Terminal 5"),
                Station("TE33", "Changi Airport"),
                Station("TE34", "Expo"),
                Station("TE35", "Tanah Merah"),
            ),  # 2040
            "future": (
                Station("CC18", "Bukit Brown"),
                Station("DT", "Sungei Kadut"),
                Station("NS6", "Sungei Kadut"),
                Station("TE4A", "Tagore"),
                Station("TE10", "Mount Pleasant"),
                Station("TE21", "Marina South"),
            ),  # Unknown opening dates
        }
    )

    __stages_defunct: types.MappingProxyType[str, tuple[Station]] = (
        types.MappingProxyType(
            {
                "ccl_6": (
                    Station("CE0X", "Stadium"),  # Pseudo station_code
                    Station("CE0Y", "Nicoll Highway"),  # Pseudo station_code
                    Station("CE0Z", "Promenade"),  # Pseudo station_code
                    Station("CE1", "Bayfront"),
                    Station("CE2", "Marina Bay"),
                ),
                "ten_mile_junction_temporary_closure": (
                    Station("BP14", "Ten Mile Junction"),
                ),
                "ten_mile_junction_permanent_closure": (
                    Station("BP14", "Ten Mile Junction"),
                ),
                "cg_tel_c": (
                    Station("CG2", "Changi Airport"),
                    Station("CG1", "Expo"),
                    Station("CG", "Tanah Merah"),
                ),
            }
        )
    )

    def __new__(cls, name, bases, dct):
        stations: set[Station] = set()
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

            # Ensure no station code has multiple names.
            station_code_counts = collections.Counter(
                [station.station_code for station in stations]
            )
            for station_code, count in station_code_counts.items():
                if count > 1:
                    raise AttributeError(
                        f"Not allowed: Multiple stations with station code {station_code} must not exist concurrently."
                    )

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
        self.stations: set[Station] = set()
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
