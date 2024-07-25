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


class ConditionalInterchange:
    """A conditional interchange is a station that is positioned between different sections of the
    same line that are not directly connected to each other. For example, STC Sengkang is the
    conditional interchange for the Sengkang LRT East Loop and Sengkang LRT West Loop.

    A conditional interchange behaves as an interchange only when previous segment and next segment are
    of specific types as outlined in `edge_type_pairs`. For example, there will be an interchange transfer when
    moving from "bahar_east" to "bahar_west", but not from "bahar_west" to "bahar_east".

    Nearly all segments adjacent to a conditional interchange are non-sequential,
    except for BP6-BP7, JS6-JS7, JS7-JS8 which are sequential.
    """

    # (start, end, edge_type, conditional_interchange_station_code)
    segments: tuple[tuple[str, str, str, str]] = (
        ("BP5", "BP6", "bukit_panjang_main", "BP6"),
        ("BP6", "BP13", "bukit_panjang_service_a", "BP6"),
        ("BP6", "BP7", "bukit_panjang_service_b", "BP6"),
        ("BP6", "BP14", "bukit_panjang_service_c", "BP6"),
        #
        ("STC", "SE1", "sengkang_east_loop", "STC"),
        ("STC", "SE5", "sengkang_east_loop", "STC"),
        ("STC", "SW1", "sengkang_west_loop", "STC"),
        ("STC", "SW2", "sengkang_west_loop", "STC"),  # Defunct with SW1 | cheng_lim
        ("STC", "SW4", "sengkang_west_loop", "STC"),  # Defunct with SW2 | farmway
        ("STC", "SW8", "sengkang_west_loop", "STC"),
        #
        ("PTC", "PE1", "punggol_east_loop", "PTC"),
        ("PTC", "PE5", "punggol_east_loop", "PTC"),  # Defunct with PE6 | oasis
        (
            "PTC",
            "PE6",
            "punggol_east_loop",
            "PTC",
        ),  # Defunct with PE7 | woodleigh_and_damai
        ("PTC", "PE7", "punggol_east_loop", "PTC"),
        ("PTC", "PW1", "punggol_west_loop", "PTC"),
        ("PTC", "PW5", "punggol_west_loop", "PTC"),  # Defunct with PW1 | sam_kee
        ("PTC", "PW7", "punggol_west_loop", "PTC"),
        #
        ("CC4", "CC5", "promenade_east", "CC4"),
        ("CC3", "CC4", "promenade_west", "CC4"),
        ("CC4", "CC34", "promenade_south", "CC4"),
        #
        ("JS6", "JS7", "bahar_east", "JS7"),
        ("JS7", "JW1", "bahar_west", "JS7"),
        ("JS7", "JS8", "bahar_south", "JS7"),
    )

    # TODO change to dict that maps pairs to transfer durations.
    edge_type_pairs: frozenset[tuple[str, str]] = frozenset(
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
    ) -> bool:  # TODO this should return (bool, int) where int is transfer duration
        return (previous_edge_type, next_edge_type) in cls.edge_type_pairs
