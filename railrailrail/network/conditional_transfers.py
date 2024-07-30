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

import immutabledict


@dataclasses.dataclass(frozen=True)
class ConditionalTransfersSegment:
    station_code_pair: tuple[str, str]
    edge_type: str
    interchange_station_code: str
    defunct_with_station_code: str | None = (
        None  # If this station code is present, this segment will no longer exist.
    )

    def __post_init__(self):
        if not self.edge_type:
            raise ValueError("edge_type must be a non-empty string.")
        if (
            len(self.station_code_pair) != 2
            or self.station_code_pair[0] == self.station_code_pair[1]
        ):
            raise ValueError("station_code_pair must be 2 different station codes.")
        if self.interchange_station_code not in self.station_code_pair:
            raise ValueError("station_code_pair must contain interchange_station_code.")


@dataclasses.dataclass(frozen=True)
class ConditionalTransfers:
    """A conditional interchange is a station that is positioned between different train segments of the
    same line that are not directly connected to each other. For example, STC Sengkang is the
    conditional interchange for the Sengkang LRT East Loop and Sengkang LRT West Loop.

    A conditional interchange behaves as an interchange only when the `edge_type` of the
    previous train segment and next train segment match any sequence in `conditional_transfers`.
    When this happens, a conditional transfer occurs.

    For example, there will be a conditional transfer when
    moving from "bahar_east" to "bahar_west", but not from "bahar_west" to "bahar_east".

    Nearly all train segments adjacent to a conditional interchange are non-sequential, like JS7-JW1,
    except for BP6-BP7, JS6-JS7, JS7-JS8 which are sequential.
    """

    conditional_transfer_segments: tuple[ConditionalTransfersSegment] = (
        ConditionalTransfersSegment(("BP5", "BP6"), "bukit_panjang_main", "BP6"),
        ConditionalTransfersSegment(("BP6", "BP13"), "bukit_panjang_service_a", "BP6"),
        ConditionalTransfersSegment(("BP6", "BP7"), "bukit_panjang_service_b", "BP6"),
        ConditionalTransfersSegment(("BP6", "BP14"), "bukit_panjang_service_c", "BP6"),
        #
        ConditionalTransfersSegment(("STC", "SE1"), "sengkang_east_loop", "STC"),
        ConditionalTransfersSegment(("STC", "SE5"), "sengkang_east_loop", "STC"),
        ConditionalTransfersSegment(("STC", "SW1"), "sengkang_west_loop", "STC"),
        ConditionalTransfersSegment(("STC", "SW2"), "sengkang_west_loop", "STC", "SW1"),
        ConditionalTransfersSegment(("STC", "SW4"), "sengkang_west_loop", "STC", "SW2"),
        ConditionalTransfersSegment(("STC", "SW8"), "sengkang_west_loop", "STC"),
        #
        ConditionalTransfersSegment(("PTC", "PE1"), "punggol_east_loop", "PTC"),
        ConditionalTransfersSegment(("PTC", "PE5"), "punggol_east_loop", "PTC", "PE6"),
        ConditionalTransfersSegment(("PTC", "PE6"), "punggol_east_loop", "PTC", "PE7"),
        ConditionalTransfersSegment(("PTC", "PE7"), "punggol_east_loop", "PTC"),
        ConditionalTransfersSegment(("PTC", "PW1"), "punggol_west_loop", "PTC"),
        ConditionalTransfersSegment(("PTC", "PW5"), "punggol_west_loop", "PTC", "PW1"),
        ConditionalTransfersSegment(("PTC", "PW7"), "punggol_west_loop", "PTC"),
        #
        ConditionalTransfersSegment(("CC4", "CC5"), "promenade_east", "CC4"),
        ConditionalTransfersSegment(("CC3", "CC4"), "promenade_west", "CC4"),
        ConditionalTransfersSegment(("CC4", "CC34"), "promenade_south", "CC4"),
        #
        ConditionalTransfersSegment(("JS6", "JS7"), "bahar_east", "JS7"),
        ConditionalTransfersSegment(("JS7", "JW1"), "bahar_west", "JS7"),
        ConditionalTransfersSegment(("JS7", "JS8"), "bahar_south", "JS7"),
    )

    # Transfers at all possible conditional interchanges, including defunct and future conditional interchanges.
    #
    # TODO: Update in the future when more direction-specific transfer time is available.
    #
    conditional_transfers: immutabledict.immutabledict[
        str, immutabledict.immutabledict[str, int]
    ] = immutabledict.immutabledict(
        {
            "punggol_west_loop": immutabledict.immutabledict(
                {"punggol_east_loop": 360}
            ),
            "punggol_east_loop": immutabledict.immutabledict(
                {"punggol_west_loop": 360}
            ),
            #
            "sengkang_west_loop": immutabledict.immutabledict(
                {"sengkang_east_loop": 360}
            ),
            "sengkang_east_loop": immutabledict.immutabledict(
                {"sengkang_west_loop": 360}
            ),
            #
            "bukit_panjang_service_a": immutabledict.immutabledict(
                {
                    "bukit_panjang_service_b": 420,
                    "bukit_panjang_service_c": 420,
                }
            ),
            "bukit_panjang_service_b": immutabledict.immutabledict(
                {
                    "bukit_panjang_service_a": 420,
                    "bukit_panjang_service_c": 420,
                }
            ),
            "bukit_panjang_service_c": immutabledict.immutabledict(
                {
                    "bukit_panjang_main": 420,
                    "bukit_panjang_service_a": 420,
                    "bukit_panjang_service_b": 420,
                }
            ),  # Assume Service C always involves transfer at BP6.
            "bukit_panjang_main": immutabledict.immutabledict(
                {"bukit_panjang_service_c": 420}
            ),
            #
            "promenade_south": immutabledict.immutabledict({"promenade_west": 420}),
            "promenade_west": immutabledict.immutabledict({"promenade_south": 420}),
            "promenade_east": immutabledict.immutabledict({"promenade_south": 420}),
            #
            "bahar_east": immutabledict.immutabledict({"bahar_west": 360}),
            "bahar_west": immutabledict.immutabledict({"bahar_south": 360}),
            "bahar_south": immutabledict.immutabledict({"bahar_east": 360}),
        }
    )  # Order is important; bahar_east -> bahar_west != bahar_west -> bahar_east
