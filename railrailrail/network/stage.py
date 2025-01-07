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
import datetime

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

    __stages: immutabledict.immutabledict[
        str, tuple[tuple[SingaporeStation], str, datetime.datetime]
    ] = immutabledict.immutabledict(
        {
            "phase_1_1": (
                (
                    SingaporeStation("NS15", "Yio Chu Kang"),
                    SingaporeStation("NS16", "Ang Mo Kio"),
                    SingaporeStation("NS17", "Bishan"),
                    SingaporeStation("NS18", "Braddell"),
                    SingaporeStation("NS19", "Toa Payoh"),
                ),
                "Phase 1 1",
                datetime.datetime.strptime("7 November 1987", "%d %B %Y"),
            ),
            "phase_1_2": (
                (
                    SingaporeStation("EW15", "Tanjong Pagar"),
                    SingaporeStation("EW16", "Outram Park"),
                    SingaporeStation("NS20", "Novena"),
                    SingaporeStation("NS21", "Newton"),
                    SingaporeStation("NS22", "Orchard"),
                    SingaporeStation("NS23", "Somerset"),
                    SingaporeStation("NS24", "Dhoby Ghaut"),
                    SingaporeStation("NS25", "City Hall"),
                    SingaporeStation("NS26", "Raffles Place"),
                ),
                "Phase 1 2",
                datetime.datetime.strptime("12 December 1987", "%d %B %Y"),
            ),
            "phase_1a": (
                (
                    SingaporeStation("EW17", "Tiong Bahru"),
                    SingaporeStation("EW18", "Redhill"),
                    SingaporeStation("EW19", "Queenstown"),
                    SingaporeStation("EW20", "Commonwealth"),
                    SingaporeStation("EW21", "Buona Vista"),
                    SingaporeStation("EW23", "Clementi"),
                ),
                "Phase 1A",
                datetime.datetime.strptime("12 March 1988", "%d %B %Y"),
            ),
            "phase_2b_1": (
                (
                    SingaporeStation("EW24", "Jurong East"),
                    SingaporeStation("EW25", "Chinese Garden"),
                    SingaporeStation("EW26", "Lakeside"),
                ),
                "Phase 2B 1",
                datetime.datetime.strptime("5 November 1988", "%d %B %Y"),
            ),
            "phase_2b_2": (
                (
                    SingaporeStation("NS13", "Yishun"),
                    SingaporeStation("NS14", "Khatib"),
                ),
                "Phase 2B 2",
                datetime.datetime.strptime("20 December 1988", "%d %B %Y"),
            ),
            "phase_2a_1": (
                (
                    SingaporeStation("EW4", "Tanah Merah"),
                    SingaporeStation("EW5", "Bedok"),
                    SingaporeStation("EW6", "Kembangan"),
                    SingaporeStation("EW7", "Eunos"),
                    SingaporeStation("EW8", "Paya Lebar"),
                    SingaporeStation("EW9", "Aljunied"),
                    SingaporeStation("EW10", "Kallang"),
                    SingaporeStation("EW11", "Lavender"),
                    SingaporeStation("EW12", "Bugis"),
                    SingaporeStation("EW13", "City Hall"),  #   EWL section.
                    SingaporeStation("EW14", "Raffles Place"),  #   EWL section.
                    SingaporeStation("NS27", "Marina Bay"),
                ),
                "Phase 2A 1",
                datetime.datetime.strptime("4 November 1989", "%d %B %Y"),
            ),
            "phase_2a_2": (
                (
                    SingaporeStation("EW1", "Pasir Ris"),
                    SingaporeStation("EW2", "Tampines"),
                    SingaporeStation("EW3", "Simei"),
                ),
                "Phase 2A 2",
                datetime.datetime.strptime("16 December 1989", "%d %B %Y"),
            ),
            "phase_2b_3": (
                (
                    SingaporeStation("NS1", "Jurong East"),
                    SingaporeStation("NS2", "Bukit Batok"),
                    SingaporeStation("NS3", "Bukit Gombak"),
                    SingaporeStation("NS4", "Choa Chu Kang"),
                ),
                "Phase 2B 3",
                datetime.datetime.strptime("10 March 1990", "%d %B %Y"),
            ),
            "phase_2b_4": (
                (SingaporeStation("EW27", "Boon Lay"),),
                "",
                datetime.datetime.strptime("6 July 1990", "%d %B %Y"),
            ),
            "woodlands_extension": (
                (
                    SingaporeStation("NS5", "Yew Tee"),
                    SingaporeStation("NS7", "Kranji"),
                    SingaporeStation("NS8", "Marsiling"),
                    SingaporeStation("NS9", "Woodlands"),
                    SingaporeStation("NS10", "Admiralty"),
                    SingaporeStation("NS11", "Sembawang"),
                ),
                "Phase 2B 4",
                datetime.datetime.strptime("10 February 1996", "%d %B %Y"),
            ),
            "bplrt": (
                (
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
                ),
                "Bukit Panjang LRT",
                datetime.datetime.strptime("6 November 1999", "%d %B %Y"),
            ),
            "ewl_expo": (
                (
                    SingaporeStation("CG", "Tanah Merah"),
                    SingaporeStation("CG1", "Expo"),
                ),
                "East West Line Expo",
                datetime.datetime.strptime("10 January 2001", "%d %B %Y"),
            ),
            "dover": (
                (SingaporeStation("EW22", "Dover"),),
                "Dover",
                datetime.datetime.strptime("18 October 2001", "%d %B %Y"),
            ),
            "ewl_changi_airport": (
                (SingaporeStation("CG2", "Changi Airport"),),
                "East West Line Changi Airport",
                datetime.datetime.strptime("8 February 2002", "%d %B %Y"),
            ),
            "sklrt_east_loop": (
                (
                    SingaporeStation("STC", "Sengkang"),
                    SingaporeStation("SE1", "Compassvale"),
                    SingaporeStation("SE2", "Rumbia"),
                    SingaporeStation("SE3", "Bakau"),
                    SingaporeStation("SE4", "Kangkar"),
                    SingaporeStation("SE5", "Ranggung"),
                ),
                "Sengkang LRT East Loop",
                datetime.datetime.strptime("18 January 2003", "%d %B %Y"),
            ),
            "nel": (
                (
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
                ),
                "North East Line",
                datetime.datetime.strptime("20 June 2003", "%d %B %Y"),
            ),
            "pglrt_east_loop_and_sklrt_west_loop": (
                (
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
                ),
                "Punggol LRT East Loop and Sengkang LRT West Loop",
                datetime.datetime.strptime("29 January 2005", "%d %B %Y"),
            ),
            "buangkok": (
                (SingaporeStation("NE15", "Buangkok"),),
                "Buangkok",
                datetime.datetime.strptime("15 January 2006", "%d %B %Y"),
            ),
            "oasis": (
                (SingaporeStation("PE6", "Oasis"),),
                "Oasis",
                datetime.datetime.strptime("15 June 2007", "%d %B %Y"),
            ),
            "farmway": (
                (SingaporeStation("SW2", "Farmway"),),
                "Farmway",
                datetime.datetime.strptime("15 November 2007", "%d %B %Y"),
            ),
            "ewl_boon_lay_extension": (
                (
                    SingaporeStation("EW28", "Pioneer"),
                    SingaporeStation("EW29", "Joo Koon"),
                ),
                "East West Line Boon Lay Extension",
                datetime.datetime.strptime("28 February 2009", "%d %B %Y"),
            ),
            "ccl_3": (
                (
                    SingaporeStation("CC12", "Bartley"),
                    SingaporeStation("CC13", "Serangoon"),
                    SingaporeStation("CC14", "Lorong Chuan"),
                    SingaporeStation("CC15", "Bishan"),
                    SingaporeStation("CC16", "Marymount"),
                ),
                "Circle Line Stage 3",
                datetime.datetime.strptime("28 May 2009", "%d %B %Y"),
            ),
            "ccl_1_and_ccl_2": (
                (
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
                ),
                "Circle Line Stage 1 and Circle Line Stage 2",
                datetime.datetime.strptime("17 April 2010", "%d %B %Y"),
            ),
            "ten_mile_junction_temporary_closure": (
                (),
                "Ten Mile Junction Temporary Closure",
                datetime.datetime.strptime("10 December 2010", "%d %B %Y"),
            ),
            "woodleigh_and_damai": (
                (
                    SingaporeStation("NE11", "Woodleigh"),
                    SingaporeStation("PE7", "Damai"),
                ),
                "Woodleigh and Damai",
                datetime.datetime.strptime("20 June 2011", "%d %B %Y"),
            ),
            "ccl_4_and_ccl_5": (
                (
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
                ),
                "Circle Line Stage 4 and Circle Line Stage 5",
                datetime.datetime.strptime("8 October 2011", "%d %B %Y"),
            ),
            "ten_mile_junction_reopen": (
                (SingaporeStation("BP14", "Ten Mile Junction"),),
                "Ten Mile Junction Reopen",
                datetime.datetime.strptime("30 December 2011", "%d %B %Y"),
            ),
            "ccl_e": (
                (
                    SingaporeStation("CE0X", "Stadium"),  #   Pseudo station_code
                    SingaporeStation("CE0Y", "Nicoll Highway"),  #   Pseudo station_code
                    SingaporeStation("CE0Z", "Promenade"),  #   Pseudo station_code
                    SingaporeStation("CE1", "Bayfront"),
                    SingaporeStation("CE2", "Marina Bay"),
                ),
                "Circle Line Extension",
                datetime.datetime.strptime("14 January 2012", "%d %B %Y"),
            ),
            "cheng_lim": (
                (SingaporeStation("SW1", "Cheng Lim"),),
                "Cheng Lim",
                datetime.datetime.strptime("1 January 2013", "%d %B %Y"),
            ),
            "dtl_1": (
                (
                    SingaporeStation("DT14", "Bugis"),
                    SingaporeStation("DT15", "Promenade"),
                    SingaporeStation("DT16", "Bayfront"),
                    SingaporeStation("DT17", "Downtown"),
                    SingaporeStation("DT18", "Telok Ayer"),
                    SingaporeStation("DT19", "Chinatown"),
                ),
                "Downtown Line 1",
                datetime.datetime.strptime("22 December 2013", "%d %B %Y"),
            ),
            "pglrt_west_loop": (
                (
                    SingaporeStation("PW5", "Nibong"),
                    SingaporeStation("PW6", "Sumang"),
                    SingaporeStation("PW7", "Soo Teck"),
                ),
                "Punggol LRT West Loop",
                datetime.datetime.strptime("29 June 2014", "%d %B %Y"),
            ),
            "marina_south_pier": (
                (SingaporeStation("NS28", "Marina South Pier"),),
                "Marina South Pier",
                datetime.datetime.strptime("23 November 2014", "%d %B %Y"),
            ),
            "kupang": (
                (SingaporeStation("SW3", "Kupang"),),
                "Kupang",
                datetime.datetime.strptime("27 June 2015", "%d %B %Y"),
            ),
            "dtl_2": (
                (
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
                ),
                "Downtown Line 2",
                datetime.datetime.strptime("27 December 2015", "%d %B %Y"),
            ),
            "sam_kee": (
                (SingaporeStation("PW1", "Sam Kee"),),
                "Sam Kee",
                datetime.datetime.strptime("29 February 2016", "%d %B %Y"),
            ),
            "punggol_point": (
                (SingaporeStation("PW3", "Punggol Point"),),
                "Punggol Point",
                datetime.datetime.strptime("29 December 2016", "%d %B %Y"),
            ),
            "samudera": (
                (SingaporeStation("PW4", "Samudera"),),
                "Samudera",
                datetime.datetime.strptime("31 March 2017", "%d %B %Y"),
            ),
            "ewl_tuas_extension": (
                (
                    SingaporeStation("EW30", "Gul Circle"),
                    SingaporeStation("EW31", "Tuas Crescent"),
                    SingaporeStation("EW32", "Tuas West Road"),
                    SingaporeStation("EW33", "Tuas Link"),
                ),
                "East West Line Tuas Extension",
                datetime.datetime.strptime("18 June 2017", "%d %B %Y"),
            ),
            "dtl_3": (
                (
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
                ),
                "Downtown Line 3",
                datetime.datetime.strptime("21 October 2017", "%d %B %Y"),
            ),
            "ten_mile_junction_permanent_closure": (
                (),
                "Ten Mile Junction Permanent Closure",
                datetime.datetime.strptime("13 January 2019", "%d %B %Y"),
            ),
            "canberra": (
                (SingaporeStation("NS12", "Canberra"),),
                "Canberra",
                datetime.datetime.strptime("2 November 2019", "%d %B %Y"),
            ),
            "tel_1": (
                (
                    SingaporeStation("TE1", "Woodlands North"),
                    SingaporeStation("TE2", "Woodlands"),
                    SingaporeStation("TE3", "Woodlands South"),
                ),
                "Thomson-East Coast Line 1",
                datetime.datetime.strptime("31 January 2020", "%d %B %Y"),
            ),
            "tel_2": (
                (
                    SingaporeStation("TE4", "Springleaf"),
                    SingaporeStation("TE5", "Lentor"),
                    SingaporeStation("TE6", "Mayflower"),
                    SingaporeStation("TE7", "Bright Hill"),
                    SingaporeStation("TE8", "Upper Thomson"),
                    SingaporeStation("TE9", "Caldecott"),
                ),
                "Thomson-East Coast Line 2",
                datetime.datetime.strptime("28 August 2021", "%d %B %Y"),
            ),
            "tel_3": (
                (
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
                ),
                "Thomson-East Coast Line 3",
                datetime.datetime.strptime("13 November 2022", "%d %B %Y"),
            ),
            "tel_4": (
                (
                    SingaporeStation("TE23", "Tanjong Rhu"),
                    SingaporeStation("TE24", "Katong Park"),
                    SingaporeStation("TE25", "Tanjong Katong"),
                    SingaporeStation("TE26", "Marine Parade"),
                    SingaporeStation("TE27", "Marine Terrace"),
                    SingaporeStation("TE28", "Siglap"),
                    SingaporeStation("TE29", "Bayshore"),
                ),
                "Thomson-East Coast Line 4",
                datetime.datetime.strptime("23 June 2024", "%d %B %Y"),
            ),
            "teck_lee": (
                (SingaporeStation("PW2", "Teck Lee"),),
                "Teck Lee",
                datetime.datetime.strptime("15 August 2024", "%d %B %Y"),
            ),
            "nel_extension": (
                (SingaporeStation("NE18", "Punggol Coast"),),
                "North East Line Extension",
                datetime.datetime.strptime("10 December 2024", "%d %B %Y"),
            ),
            "hume": (
                (SingaporeStation("DT4", "Hume"),),
                "Hume",
                datetime.datetime.strptime("31 December 2025", "%d %B %Y"),  # TBC
            ),
            "tel_5_and_dtl_3e": (
                (
                    SingaporeStation("TE30", "Bedok South"),
                    SingaporeStation("TE31", "Sungei Bedok"),
                    SingaporeStation("DT36", "Xilin"),
                    SingaporeStation("DT37", "Sungei Bedok"),
                ),
                "Thomson-East Coast Line 5 and Downtown Line 3 Extension",
                datetime.datetime.strptime("30 November 2026", "%d %B %Y"),  # TBC
            ),
            "ccl_6": (
                (
                    SingaporeStation("CC30", "Keppel"),
                    SingaporeStation("CC31", "Cantonment"),
                    SingaporeStation("CC32", "Prince Edward Road"),
                    SingaporeStation("CC33", "Marina Bay"),
                    SingaporeStation("CC34", "Bayfront"),
                ),
                "Circle Line 6",
                datetime.datetime.strptime("31 December 2026", "%d %B %Y"),  # TBC
            ),
            "jrl_1": (
                (
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
                ),
                "Jurong Region Line 1",
                datetime.datetime.strptime("31 December 2027", "%d %B %Y"),  # TBC
            ),
            "founders_memorial": (
                (SingaporeStation("TE22A", "Founders' Memorial"),),
                "Founders' Memorial",
                datetime.datetime.strptime("30 November 2028", "%d %B %Y"),  # TBC
            ),
            "jrl_2": (
                (
                    SingaporeStation("JE0", "Tengah"),  #   Pseudo station_code
                    SingaporeStation("JE1", "Tengah Plantation"),
                    SingaporeStation("JE2", "Tengah Park"),
                    SingaporeStation("JE3", "Bukit Batok West"),
                    SingaporeStation("JE4", "Toh Guan"),
                    SingaporeStation("JE5", "Jurong East"),
                    SingaporeStation("JE6", "Jurong Town Hall"),
                    SingaporeStation("JE7", "Pandan Reservoir"),
                ),
                "Jurong Region Line 2",
                datetime.datetime.strptime("31 December 2028", "%d %B %Y"),  # TBC
            ),
            "jrl_3": (
                (
                    SingaporeStation("JS9", "Enterprise"),
                    SingaporeStation("JS10", "Tukang"),
                    SingaporeStation("JS11", "Jurong Hill"),
                    SingaporeStation("JS12", "Jurong Pier"),
                    SingaporeStation("JW3", "Nanyang Gateway"),
                    SingaporeStation("JW4", "Nanyang Crescent"),
                    SingaporeStation("JW5", "Peng Kang Hill"),
                ),
                "Jurong Region Line 3",
                datetime.datetime.strptime("31 December 2029", "%d %B %Y"),  # TBC
            ),
            "crl_1": (
                (
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
                ),
                "Cross Island Line 1",
                datetime.datetime.strptime("31 December 2030", "%d %B %Y"),  # TBC
            ),
            "crl_2": (
                (
                    SingaporeStation("CR14", "Turf City"),
                    SingaporeStation("CR15", "King Albert Park"),
                    SingaporeStation("CR16", "Maju"),
                    SingaporeStation("CR17", "Clementi"),
                    SingaporeStation("CR18", "West Coast"),
                    SingaporeStation("CR19", "Jurong Lake District"),
                ),
                "Cross Island Line 2",
                datetime.datetime.strptime("30 November 2032", "%d %B %Y"),  # TBC
            ),
            "crl_pe": (
                (
                    SingaporeStation("CP1", "Pasir Ris"),
                    SingaporeStation("CP2", "Elias"),
                    SingaporeStation("CP3", "Riviera"),
                    SingaporeStation("CP4", "Punggol"),
                ),
                "Cross Island Line Punggol Extension",
                datetime.datetime.strptime("31 December 2032", "%d %B %Y"),  # TBC
            ),
            "brickland": (
                (SingaporeStation("NS3A", "Brickland"),),
                "Brickland",
                datetime.datetime.strptime("31 December 2034", "%d %B %Y"),  # TBC
            ),
            "dtl_2e": (
                (
                    SingaporeStation(
                        "DE1", "Yew Tee Village"
                    ),  #   Unknown official name
                    SingaporeStation("DE2", "Sungei Kadut"),
                    SingaporeStation("NS6", "Sungei Kadut"),
                ),
                "Downtown Line 2 Extension",
                datetime.datetime.strptime("31 December 2035", "%d %B %Y"),  # TBC
            ),
            "cg_tel_c": (
                (
                    SingaporeStation(
                        "CR1", "Changi Airport Terminal 5"
                    ),  #   Unknown official name
                    SingaporeStation(
                        "TE32", "Changi Airport Terminal 5"
                    ),  #   Unknown official name
                    SingaporeStation("TE33", "Changi Airport"),
                    SingaporeStation("TE34", "Expo"),
                    SingaporeStation("TE35", "Tanah Merah"),
                ),
                "Changi Airport Branch - Thomson-East Coast Line Conversion",
                datetime.datetime.strptime("31 December 2040", "%d %B %Y"),  # TBC
            ),
            "future": (
                (
                    SingaporeStation("CC18", "Bukit Brown"),
                    SingaporeStation("TE4A", "Tagore"),
                    SingaporeStation("TE10", "Mount Pleasant"),
                    SingaporeStation("TE21", "Marina South"),
                ),
                "Future",
                datetime.datetime.strptime("9999", "%Y"),  # TBC
            ),  #   Unknown opening dates
        }
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
        if not set(cls.__stages_defunct).issubset(cls.__stages):
            raise AttributeError(
                "__stages must contain all stages in __stages_defunct."
            )  # pragma: no cover
        stages_descriptions: set[str] = set()
        for stage, stage_details in cls.__stages.items():
            stage_stations, stage_description, _ = stage_details
            if stage_description in stages_descriptions:
                raise AttributeError(
                    f"Duplicate stage description not allowed: {stage_description}"
                )  # pragma: no cover
            stages_descriptions.add(stage_description)
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

        cls.stages = immutabledict.immutabledict(
            {stage: stations for stage, (stations, _, _) in cls.__stages.items()}
        )
        cls.stages_defunct = cls.__stages_defunct
        cls.stages_info = {
            stage: (stage_description, stage_timestamp)
            for stage, (_, stage_description, stage_timestamp) in cls.__stages.items()
        }
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
