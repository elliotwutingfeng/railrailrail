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

import immutabledict

from railrailrail.network.station import SingaporeStation


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

    __stages: immutabledict.immutabledict[str, tuple[SingaporeStation]] = (
        immutabledict.immutabledict(
            {
                "phase_1_1": (
                    SingaporeStation("NS15", "Yio Chu Kang"),
                    SingaporeStation("NS16", "Ang Mo Kio"),
                    SingaporeStation("NS17", "Bishan"),
                    SingaporeStation("NS18", "Braddell"),
                    SingaporeStation("NS19", "Toa Payoh"),
                ),  # 7 November 1987
                "phase_1_2": (
                    SingaporeStation("EW15", "Tanjong Pagar"),
                    SingaporeStation("EW16", "Outram Park"),
                    SingaporeStation("NS20", "Novena"),
                    SingaporeStation("NS21", "Newton"),
                    SingaporeStation("NS22", "Orchard"),
                    SingaporeStation("NS23", "Somerset"),
                    SingaporeStation("NS24", "Dhoby Ghaut"),
                    SingaporeStation("NS25", "City Hall"),
                    SingaporeStation("NS26", "Raffles Place"),
                ),  # 12 December 1987
                "phase_1a": (
                    SingaporeStation("EW17", "Tiong Bahru"),
                    SingaporeStation("EW18", "Redhill"),
                    SingaporeStation("EW19", "Queenstown"),
                    SingaporeStation("EW20", "Commonwealth"),
                    SingaporeStation("EW21", "Buona Vista"),
                    SingaporeStation("EW23", "Clementi"),
                ),  # 12 March 1988
                "phase_2b_1": (
                    SingaporeStation("EW24", "Jurong East"),
                    SingaporeStation("EW25", "Chinese Garden"),
                    SingaporeStation("EW26", "Lakeside"),
                ),  # 5 November 1988
                "phase_2b_2": (
                    SingaporeStation("NS13", "Yishun"),
                    SingaporeStation("NS14", "Khatib"),
                ),  # 20 December 1988
                "phase_2a_1": (
                    SingaporeStation("EW4", "Tanah Merah"),
                    SingaporeStation("EW5", "Bedok"),
                    SingaporeStation("EW6", "Kembangan"),
                    SingaporeStation("EW7", "Eunos"),
                    SingaporeStation("EW8", "Paya Lebar"),
                    SingaporeStation("EW9", "Aljunied"),
                    SingaporeStation("EW10", "Kallang"),
                    SingaporeStation("EW11", "Lavender"),
                    SingaporeStation("EW12", "Bugis"),
                    SingaporeStation("EW13", "City Hall"),  # EWL section.
                    SingaporeStation("EW14", "Raffles Place"),  # EWL section.
                    SingaporeStation("NS27", "Marina Bay"),
                ),  # 4 November 1989
                "phase_2a_2": (
                    SingaporeStation("EW1", "Pasir Ris"),
                    SingaporeStation("EW2", "Tampines"),
                    SingaporeStation("EW3", "Simei"),
                ),  # 16 December 1989
                "phase_2b_3": (
                    SingaporeStation("NS1", "Jurong East"),
                    SingaporeStation("NS2", "Bukit Batok"),
                    SingaporeStation("NS3", "Bukit Gombak"),
                    SingaporeStation("NS4", "Choa Chu Kang"),
                ),  # 10 March 1990
                "phase_2b_4": (SingaporeStation("EW27", "Boon Lay"),),  # 6 July 1990
                "woodlands_extension": (
                    SingaporeStation("NS5", "Yew Tee"),
                    SingaporeStation("NS7", "Kranji"),
                    SingaporeStation("NS8", "Marsiling"),
                    SingaporeStation("NS9", "Woodlands"),
                    SingaporeStation("NS10", "Admiralty"),
                    SingaporeStation("NS11", "Sembawang"),
                ),  # 10 February 1996
                "bplrt": (
                    SingaporeStation("BP1", "Choa Chu Kang"),
                    SingaporeStation("BP2", "South View"),
                    SingaporeStation("BP3", "Keat Hong"),
                    SingaporeStation("BP4", "Teck Whye"),
                    SingaporeStation("BP5", "Phoenix"),
                    SingaporeStation("BP6", "Bukit Panjang"),
                    SingaporeStation("BP7", "Petir"),
                    SingaporeStation("BP8", "Pending"),
                    SingaporeStation("BP9", "Bangkit"),
                    SingaporeStation("BP10", "Fajar"),
                    SingaporeStation("BP11", "Segar"),
                    SingaporeStation("BP12", "Jelapang"),
                    SingaporeStation("BP13", "Senja"),
                    SingaporeStation("BP14", "Ten Mile Junction"),
                ),  # 6 November 1999
                "ewl_expo": (
                    SingaporeStation("CG", "Tanah Merah"),
                    SingaporeStation("CG1", "Expo"),
                ),  # 10 January 2001
                "dover": (SingaporeStation("EW22", "Dover"),),  # 18 October 2001
                "ewl_changi_airport": (
                    SingaporeStation("CG2", "Changi Airport"),
                ),  # 8 February 2002
                "sklrt_east_loop": (
                    SingaporeStation("STC", "Sengkang"),
                    SingaporeStation("SE1", "Compassvale"),
                    SingaporeStation("SE2", "Rumbia"),
                    SingaporeStation("SE3", "Bakau"),
                    SingaporeStation("SE4", "Kangkar"),
                    SingaporeStation("SE5", "Ranggung"),
                ),  # 18 January 2003
                "nel": (
                    SingaporeStation("NE1", "HarbourFront"),
                    SingaporeStation("NE3", "Outram Park"),
                    SingaporeStation("NE4", "Chinatown"),
                    SingaporeStation("NE5", "Clarke Quay"),
                    SingaporeStation("NE6", "Dhoby Ghaut"),
                    SingaporeStation("NE7", "Little India"),
                    SingaporeStation("NE8", "Farrer Park"),
                    SingaporeStation("NE9", "Boon Keng"),
                    SingaporeStation("NE10", "Potong Pasir"),
                    SingaporeStation("NE12", "Serangoon"),
                    SingaporeStation("NE13", "Kovan"),
                    SingaporeStation("NE14", "Hougang"),
                    SingaporeStation("NE16", "Sengkang"),
                    SingaporeStation("NE17", "Punggol"),
                ),  # 20 June 2003
                "pglrt_east_loop_and_sklrt_west_loop": (
                    SingaporeStation("PTC", "Punggol"),
                    SingaporeStation("PE1", "Cove"),
                    SingaporeStation("PE2", "Meridian"),
                    SingaporeStation("PE3", "Coral Edge"),
                    SingaporeStation("PE4", "Riviera"),
                    SingaporeStation("PE5", "Kadaloor"),
                    SingaporeStation("SW4", "Thanggam"),
                    SingaporeStation("SW5", "Fernvale"),
                    SingaporeStation("SW6", "Layar"),
                    SingaporeStation("SW7", "Tongkang"),
                    SingaporeStation("SW8", "Renjong"),
                ),  # 29 January 2005
                "buangkok": (SingaporeStation("NE15", "Buangkok"),),  # 15 January 2006
                "oasis": (SingaporeStation("PE6", "Oasis"),),  # 15 June 2007
                "farmway": (SingaporeStation("SW2", "Farmway"),),  # 15 November 2007
                "ewl_boon_lay_extension": (
                    SingaporeStation("EW28", "Pioneer"),
                    SingaporeStation("EW29", "Joo Koon"),
                ),  # 28 February 2009
                "ccl_3": (
                    SingaporeStation("CC12", "Bartley"),
                    SingaporeStation("CC13", "Serangoon"),
                    SingaporeStation("CC14", "Lorong Chuan"),
                    SingaporeStation("CC15", "Bishan"),
                    SingaporeStation("CC16", "Marymount"),
                ),  # 28 May 2009
                "ccl_1_and_ccl_2": (
                    SingaporeStation("CC1", "Dhoby Ghaut"),
                    SingaporeStation("CC2", "Bras Basah"),
                    SingaporeStation("CC3", "Esplanade"),
                    SingaporeStation("CC4", "Promenade"),
                    SingaporeStation("CC5", "Nicoll Highway"),
                    SingaporeStation("CC6", "Stadium"),
                    SingaporeStation("CC7", "Mountbatten"),
                    SingaporeStation("CC8", "Dakota"),
                    SingaporeStation("CC9", "Paya Lebar"),
                    SingaporeStation("CC10", "MacPherson"),
                    SingaporeStation("CC11", "Tai Seng"),
                ),  # 17 April 2010
                "ten_mile_junction_temporary_closure": (),  # 10 December 2010
                "woodleigh_and_damai": (
                    SingaporeStation("NE11", "Woodleigh"),
                    SingaporeStation("PE7", "Damai"),
                ),  # 20 June 2011
                "ccl_4_and_ccl_5": (
                    SingaporeStation("CC17", "Caldecott"),
                    SingaporeStation("CC19", "Botanic Gardens"),
                    SingaporeStation("CC20", "Farrer Road"),
                    SingaporeStation("CC21", "Holland Village"),
                    SingaporeStation("CC22", "Buona Vista"),
                    SingaporeStation("CC23", "one-north"),
                    SingaporeStation("CC24", "Kent Ridge"),
                    SingaporeStation("CC25", "Haw Par Villa"),
                    SingaporeStation("CC26", "Pasir Panjang"),
                    SingaporeStation("CC27", "Labrador Park"),
                    SingaporeStation("CC28", "Telok Blangah"),
                    SingaporeStation("CC29", "HarbourFront"),
                ),  # 8 October 2011
                "ten_mile_junction_reopen": (
                    SingaporeStation("BP14", "Ten Mile Junction"),
                ),  # 30 December 2011
                "ccl_e": (
                    SingaporeStation("CE0X", "Stadium"),  # Pseudo station_code
                    SingaporeStation("CE0Y", "Nicoll Highway"),  # Pseudo station_code
                    SingaporeStation("CE0Z", "Promenade"),  # Pseudo station_code
                    SingaporeStation("CE1", "Bayfront"),
                    SingaporeStation("CE2", "Marina Bay"),
                ),  # 14 January 2012
                "cheng_lim": (SingaporeStation("SW1", "Cheng Lim"),),  # 1 January 2013
                "dtl_1": (
                    SingaporeStation("DT14", "Bugis"),
                    SingaporeStation("DT15", "Promenade"),
                    SingaporeStation("DT16", "Bayfront"),
                    SingaporeStation("DT17", "Downtown"),
                    SingaporeStation("DT18", "Telok Ayer"),
                    SingaporeStation("DT19", "Chinatown"),
                ),  # 22 December 2013
                "pglrt_west_loop": (
                    SingaporeStation("PW5", "Nibong"),
                    SingaporeStation("PW6", "Sumang"),
                    SingaporeStation("PW7", "Soo Teck"),
                ),  # 29 June 2014
                "marina_south_pier": (
                    SingaporeStation("NS28", "Marina South Pier"),
                ),  # 23 November 2014
                "kupang": (SingaporeStation("SW3", "Kupang"),),  # 27 June 2015
                "dtl_2": (
                    SingaporeStation("DT1", "Bukit Panjang"),
                    SingaporeStation("DT2", "Cashew"),
                    SingaporeStation("DT3", "Hillview"),
                    SingaporeStation("DT5", "Beauty World"),
                    SingaporeStation("DT6", "King Albert Park"),
                    SingaporeStation("DT7", "Sixth Avenue"),
                    SingaporeStation("DT8", "Tan Kah Kee"),
                    SingaporeStation("DT9", "Botanic Gardens"),
                    SingaporeStation("DT10", "Stevens"),
                    SingaporeStation("DT11", "Newton"),
                    SingaporeStation("DT12", "Little India"),
                    SingaporeStation("DT13", "Rochor"),
                ),  # 27 December 2015
                "sam_kee": (SingaporeStation("PW1", "Sam Kee"),),  # 29 February 2016
                "punggol_point": (
                    SingaporeStation("PW3", "Punggol Point"),
                ),  # 29 December 2016
                "samudera": (SingaporeStation("PW4", "Samudera"),),  # 31 March 2017
                "ewl_tuas_extension": (
                    SingaporeStation("EW30", "Gul Circle"),
                    SingaporeStation("EW31", "Tuas Crescent"),
                    SingaporeStation("EW32", "Tuas West Road"),
                    SingaporeStation("EW33", "Tuas Link"),
                ),  # 18 June 2017
                "dtl_3": (
                    SingaporeStation("DT20", "Fort Canning"),
                    SingaporeStation("DT21", "Bencoolen"),
                    SingaporeStation("DT22", "Jalan Besar"),
                    SingaporeStation("DT23", "Bendemeer"),
                    SingaporeStation("DT24", "Geylang Bahru"),
                    SingaporeStation("DT25", "Mattar"),
                    SingaporeStation("DT26", "MacPherson"),
                    SingaporeStation("DT27", "Ubi"),
                    SingaporeStation("DT28", "Kaki Bukit"),
                    SingaporeStation("DT29", "Bedok North"),
                    SingaporeStation("DT30", "Bedok Reservoir"),
                    SingaporeStation("DT31", "Tampines West"),
                    SingaporeStation("DT32", "Tampines"),
                    SingaporeStation("DT33", "Tampines East"),
                    SingaporeStation("DT34", "Upper Changi"),
                    SingaporeStation("DT35", "Expo"),
                ),  # 21 October 2017
                "ten_mile_junction_permanent_closure": (),  # 13 January 2019
                "canberra": (SingaporeStation("NS12", "Canberra"),),  # 2 November 2019
                "tel_1": (
                    SingaporeStation("TE1", "Woodlands North"),
                    SingaporeStation("TE2", "Woodlands"),
                    SingaporeStation("TE3", "Woodlands South"),
                ),  # 31 January 2020
                "tel_2": (
                    SingaporeStation("TE4", "Springleaf"),
                    SingaporeStation("TE5", "Lentor"),
                    SingaporeStation("TE6", "Mayflower"),
                    SingaporeStation("TE7", "Bright Hill"),
                    SingaporeStation("TE8", "Upper Thomson"),
                    SingaporeStation("TE9", "Caldecott"),
                ),  # 28 August 2021
                "tel_3": (
                    SingaporeStation("TE11", "Stevens"),
                    SingaporeStation("TE12", "Napier"),
                    SingaporeStation("TE13", "Orchard Boulevard"),
                    SingaporeStation("TE14", "Orchard"),
                    SingaporeStation("TE15", "Great World"),
                    SingaporeStation("TE16", "Havelock"),
                    SingaporeStation("TE17", "Outram Park"),
                    SingaporeStation("TE18", "Maxwell"),
                    SingaporeStation("TE19", "Shenton Way"),
                    SingaporeStation("TE20", "Marina Bay"),
                    SingaporeStation("TE22", "Gardens by the Bay"),
                ),  # 13 November 2022
                "tel_4": (
                    SingaporeStation("TE23", "Tanjong Rhu"),
                    SingaporeStation("TE24", "Katong Park"),
                    SingaporeStation("TE25", "Tanjong Katong"),
                    SingaporeStation("TE26", "Marine Parade"),
                    SingaporeStation("TE27", "Marine Terrace"),
                    SingaporeStation("TE28", "Siglap"),
                    SingaporeStation("TE29", "Bayshore"),
                ),  # 23 June 2024
                "teck_lee": (SingaporeStation("PW2", "Teck Lee"),),  # 15 August 2024
                "punggol_coast_extension": (
                    SingaporeStation("NE18", "Punggol Coast"),
                ),  # 2024
                "hume": (SingaporeStation("DT4", "Hume"),),  # 2025
                "tel_5_and_dtl_3e": (
                    SingaporeStation("TE30", "Bedok South"),
                    SingaporeStation("TE31", "Sungei Bedok"),
                    SingaporeStation("DT36", "Xilin"),
                    SingaporeStation("DT37", "Sungei Bedok"),
                ),  # 2026
                "ccl_6": (
                    SingaporeStation("CC30", "Keppel"),
                    SingaporeStation("CC31", "Cantonment"),
                    SingaporeStation("CC32", "Prince Edward Road"),
                    SingaporeStation("CC33", "Marina Bay"),
                    SingaporeStation("CC34", "Bayfront"),
                ),  # 2026
                "jrl_1": (
                    SingaporeStation("JS1", "Choa Chu Kang"),
                    SingaporeStation("JS2", "Choa Chu Kang West"),
                    SingaporeStation("JS3", "Tengah"),
                    SingaporeStation("JS4", "Hong Kah"),
                    SingaporeStation("JS5", "Corporation"),
                    SingaporeStation("JS6", "Jurong West"),
                    SingaporeStation("JS7", "Bahar Junction"),
                    SingaporeStation("JS8", "Boon Lay"),
                    SingaporeStation("JW1", "Gek Poh"),
                    SingaporeStation("JW2", "Tawas"),
                ),  # 2027
                "founders_memorial": (
                    SingaporeStation("TE22A", "Founders' Memorial"),
                ),  # 2028
                "jrl_2": (
                    SingaporeStation("JE0", "Tengah"),  # Pseudo station_code
                    SingaporeStation("JE1", "Tengah Plantation"),
                    SingaporeStation("JE2", "Tengah Park"),
                    SingaporeStation("JE3", "Bukit Batok West"),
                    SingaporeStation("JE4", "Toh Guan"),
                    SingaporeStation("JE5", "Jurong East"),
                    SingaporeStation("JE6", "Jurong Town Hall"),
                    SingaporeStation("JE7", "Pandan Reservoir"),
                ),  # 2028
                "jrl_3": (
                    SingaporeStation("JS9", "Enterprise"),
                    SingaporeStation("JS10", "Tukang"),
                    SingaporeStation("JS11", "Jurong Hill"),
                    SingaporeStation("JS12", "Jurong Pier"),
                    SingaporeStation("JW3", "Nanyang Gateway"),
                    SingaporeStation("JW4", "Nanyang Crescent"),
                    SingaporeStation("JW5", "Peng Kang Hill"),
                ),  # 2029
                "crl_1": (
                    SingaporeStation("CR2", "Aviation Park"),
                    SingaporeStation("CR3", "Loyang"),
                    SingaporeStation("CR4", "Pasir Ris East"),
                    SingaporeStation("CR5", "Pasir Ris"),
                    SingaporeStation("CR6", "Tampines North"),
                    SingaporeStation("CR7", "Defu"),
                    SingaporeStation("CR8", "Hougang"),
                    SingaporeStation("CR9", "Serangoon North"),
                    SingaporeStation("CR10", "Tavistock"),
                    SingaporeStation("CR11", "Ang Mo Kio"),
                    SingaporeStation("CR12", "Teck Ghee"),
                    SingaporeStation("CR13", "Bright Hill"),
                ),  # 2030
                "crl_2": (
                    SingaporeStation("CR14", "Turf City"),
                    SingaporeStation("CR15", "King Albert Park"),
                    SingaporeStation("CR16", "Maju"),
                    SingaporeStation("CR17", "Clementi"),
                    SingaporeStation("CR18", "West Coast"),
                    SingaporeStation("CR19", "Jurong Lake District"),
                ),  # 2032
                "crl_pe": (
                    SingaporeStation("CP1", "Pasir Ris"),
                    SingaporeStation("CP2", "Elias"),
                    SingaporeStation("CP3", "Riviera"),
                    SingaporeStation("CP4", "Punggol"),
                ),  # 2032
                "brickland": (SingaporeStation("NS3A", "Brickland"),),  # 2034
                "cg_tel_c": (
                    SingaporeStation(
                        "CR1", "Changi Airport Terminal 5"
                    ),  # Unknown official name
                    SingaporeStation(
                        "TE32", "Changi Airport Terminal 5"
                    ),  # Unknown official name
                    SingaporeStation("TE33", "Changi Airport"),
                    SingaporeStation("TE34", "Expo"),
                    SingaporeStation("TE35", "Tanah Merah"),
                ),  # 2040
                "future": (
                    SingaporeStation("CC18", "Bukit Brown"),
                    SingaporeStation("DT", "Sungei Kadut"),
                    SingaporeStation("NS6", "Sungei Kadut"),
                    SingaporeStation("TE4A", "Tagore"),
                    SingaporeStation("TE10", "Mount Pleasant"),
                    SingaporeStation("TE21", "Marina South"),
                ),  # Unknown opening dates
            }
        )
    )

    __stages_defunct: immutabledict.immutabledict[str, tuple[SingaporeStation]] = (
        immutabledict.immutabledict(
            {
                "ccl_6": (
                    SingaporeStation("CE0X", "Stadium"),  # Pseudo station_code
                    SingaporeStation("CE0Y", "Nicoll Highway"),  # Pseudo station_code
                    SingaporeStation("CE0Z", "Promenade"),  # Pseudo station_code
                    SingaporeStation("CE1", "Bayfront"),
                    SingaporeStation("CE2", "Marina Bay"),
                ),
                "ten_mile_junction_temporary_closure": (
                    SingaporeStation("BP14", "Ten Mile Junction"),
                ),
                "ten_mile_junction_permanent_closure": (
                    SingaporeStation("BP14", "Ten Mile Junction"),
                ),
                "cg_tel_c": (
                    SingaporeStation("CG2", "Changi Airport"),
                    SingaporeStation("CG1", "Expo"),
                    SingaporeStation("CG", "Tanah Merah"),
                ),
            }
        )
    )

    def __new__(cls, name, bases, dct):
        stations: set[SingaporeStation] = set()
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
                station.station_code for station in stations
            )
            for station_code, count in station_code_counts.items():
                if count > 1:
                    raise AttributeError(
                        f"Not allowed: Multiple stations with station code {station_code} must not exist concurrently."
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
        self.stations: set[SingaporeStation] = set()
        for (
            current_stage,
            current_stage_stations,
        ) in (
            Stage.stages.items()
        ):  # Add/Remove stations from all stages up to and including `stage`.
            self.stations.update(current_stage_stations)
            self.stations.difference_update(
                Stage.stages_defunct.get(current_stage, set())
            )
            if current_stage == stage:
                break
