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

import dataclasses
import enum


@enum.verify(enum.UNIQUE)
class EdgeType(enum.Enum):
    bukit_panjang_main = 0
    bukit_panjang_service_a = 1
    bukit_panjang_service_b = 2
    bukit_panjang_service_c = 3
    sengkang_east_loop = 4
    sengkang_west_loop = 5
    punggol_east_loop = 6
    punggol_west_loop = 7
    promenade_east = 8
    promenade_west = 9
    promenade_south = 10
    bahar_east = 11
    bahar_west = 12
    bahar_south = 13


@dataclasses.dataclass(frozen=True)
class ConditionalInterchangeSegment:
    station_code_pair: tuple[str, str]
    edge_type: EdgeType
    interchange_station_code: str
    defunct_with_station_code: str | None = (
        None  # If this station code is present, this segment will no longer exist.
    )

    def __post_init__(self):
        if (
            len(self.station_code_pair) != 2
            or self.station_code_pair[0] == self.station_code_pair[1]
        ):
            raise ValueError("station_code_pair must be 2 different station codes.")
        if self.interchange_station_code not in self.station_code_pair:
            raise ValueError("station_code_pair must contain interchange_station_code.")


@dataclasses.dataclass(frozen=True)
class ConditionalInterchange:
    """A conditional interchange is a station that is positioned between different segments of the
    same line that are not directly connected to each other. For example, STC Sengkang is the
    conditional interchange for the Sengkang LRT East Loop and Sengkang LRT West Loop.

    A conditional interchange behaves as an interchange only when previous segment and next segment are
    of specific types as outlined in `edge_type_pairs`. For example, there will be an interchange transfer when
    moving from "bahar_east" to "bahar_west", but not from "bahar_west" to "bahar_east".

    Nearly all segments adjacent to a conditional interchange are non-sequential,
    except for BP6-BP7, JS6-JS7, JS7-JS8 which are sequential.
    """

    segments: tuple[ConditionalInterchangeSegment] = (
        ConditionalInterchangeSegment(
            ("BP5", "BP6"), EdgeType.bukit_panjang_main, "BP6"
        ),
        ConditionalInterchangeSegment(
            ("BP6", "BP13"), EdgeType.bukit_panjang_service_a, "BP6"
        ),
        ConditionalInterchangeSegment(
            ("BP6", "BP7"), EdgeType.bukit_panjang_service_b, "BP6"
        ),
        ConditionalInterchangeSegment(
            ("BP6", "BP14"), EdgeType.bukit_panjang_service_c, "BP6"
        ),
        #
        ConditionalInterchangeSegment(
            ("STC", "SE1"), EdgeType.sengkang_east_loop, "STC"
        ),
        ConditionalInterchangeSegment(
            ("STC", "SE5"), EdgeType.sengkang_east_loop, "STC"
        ),
        ConditionalInterchangeSegment(
            ("STC", "SW1"), EdgeType.sengkang_west_loop, "STC"
        ),
        ConditionalInterchangeSegment(
            ("STC", "SW2"), EdgeType.sengkang_west_loop, "STC", "SW1"
        ),
        ConditionalInterchangeSegment(
            ("STC", "SW4"), EdgeType.sengkang_west_loop, "STC", "SW2"
        ),
        ConditionalInterchangeSegment(
            ("STC", "SW8"), EdgeType.sengkang_west_loop, "STC"
        ),
        #
        ConditionalInterchangeSegment(
            ("PTC", "PE1"), EdgeType.punggol_east_loop, "PTC"
        ),
        ConditionalInterchangeSegment(
            ("PTC", "PE5"), EdgeType.punggol_east_loop, "PTC", "PE6"
        ),
        ConditionalInterchangeSegment(
            ("PTC", "PE6"), EdgeType.punggol_east_loop, "PTC", "PE7"
        ),
        ConditionalInterchangeSegment(
            ("PTC", "PE7"), EdgeType.punggol_east_loop, "PTC"
        ),
        ConditionalInterchangeSegment(
            ("PTC", "PW1"), EdgeType.punggol_west_loop, "PTC"
        ),
        ConditionalInterchangeSegment(
            ("PTC", "PW5"), EdgeType.punggol_west_loop, "PTC", "PW1"
        ),
        ConditionalInterchangeSegment(
            ("PTC", "PW7"), EdgeType.punggol_west_loop, "PTC"
        ),
        #
        ConditionalInterchangeSegment(("CC4", "CC5"), EdgeType.promenade_east, "CC4"),
        ConditionalInterchangeSegment(("CC3", "CC4"), EdgeType.promenade_west, "CC4"),
        ConditionalInterchangeSegment(("CC4", "CC34"), EdgeType.promenade_south, "CC4"),
        #
        ConditionalInterchangeSegment(("JS6", "JS7"), EdgeType.bahar_east, "JS7"),
        ConditionalInterchangeSegment(("JS7", "JW1"), EdgeType.bahar_west, "JS7"),
        ConditionalInterchangeSegment(("JS7", "JS8"), EdgeType.bahar_south, "JS7"),
    )

    # TODO change to dict that maps pairs to transfer durations.
    edge_type_pairs: frozenset[tuple[EdgeType, EdgeType]] = frozenset(
        (
            (EdgeType.punggol_west_loop, EdgeType.punggol_east_loop),
            (EdgeType.punggol_east_loop, EdgeType.punggol_west_loop),
            #
            (EdgeType.sengkang_west_loop, EdgeType.sengkang_east_loop),
            (EdgeType.sengkang_east_loop, EdgeType.sengkang_west_loop),
            #
            (EdgeType.bukit_panjang_service_a, EdgeType.bukit_panjang_service_b),
            (EdgeType.bukit_panjang_service_b, EdgeType.bukit_panjang_service_a),
            # Assume Service C always involves transfer at BP6.
            (EdgeType.bukit_panjang_service_c, EdgeType.bukit_panjang_main),
            (EdgeType.bukit_panjang_service_c, EdgeType.bukit_panjang_service_a),
            (EdgeType.bukit_panjang_service_c, EdgeType.bukit_panjang_service_b),
            (EdgeType.bukit_panjang_main, EdgeType.bukit_panjang_service_c),
            (EdgeType.bukit_panjang_service_a, EdgeType.bukit_panjang_service_c),
            (EdgeType.bukit_panjang_service_b, EdgeType.bukit_panjang_service_c),
            #
            (EdgeType.promenade_south, EdgeType.promenade_west),
            (EdgeType.promenade_west, EdgeType.promenade_south),
            (EdgeType.promenade_east, EdgeType.promenade_south),
            #
            (EdgeType.bahar_east, EdgeType.bahar_west),
            (EdgeType.bahar_west, EdgeType.bahar_south),
            (EdgeType.bahar_south, EdgeType.bahar_east),
        )
    )  # Order is important; (EdgeType.bahar_east, EdgeType.bahar_west) != (EdgeType.bahar_west, EdgeType.bahar_east)

    @classmethod
    def is_conditional_interchange_transfer(
        cls, previous_edge_type: str, next_edge_type: str
    ) -> bool:  # TODO this should return (bool, int) where int is transfer duration
        try:
            p, n = EdgeType[previous_edge_type], EdgeType[next_edge_type]
        except KeyError:
            return False
        return (p, n) in cls.edge_type_pairs
