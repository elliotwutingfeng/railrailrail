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


class TransfersMeta(type):
    """Duration presets for transfers, which includes defunct and future interchanges.

    Estimates based on walking time + waiting time (5 min for MRT / 6 min for LRT).

    As a simplification, treat transfer time in both directions as equal.
    TODO: Update in the future when more direction-specific transfer time is available.

    Estimated transfer time for future interchanges:

    - elevated/elevated -> 7 min
    - underground/underground -> 9 min
    - underground/elevated -> 12 min
    """

    __interchange_transfers: tuple[tuple[str, int]] = (
        ("Ang Mo Kio", 600),
        ("Bayfront", 360),
        ("Bishan", 480),
        ("Boon Lay", 600),
        ("Botanic Gardens", 480),
        ("Bright Hill", 540),
        ("Bugis", 540),
        ("Bukit Panjang", 600),
        ("Buona Vista", 480),
        ("Caldecott", 540),
        ("Changi Airport Terminal 5", 540),
        ("Chinatown", 420),
        ("Choa Chu Kang", 420),
        ("City Hall", 360),
        ("Clementi", 480),
        ("Dhoby Ghaut", 480),
        ("Expo", 480),
        ("HarbourFront", 420),
        ("Hougang", 540),
        ("Jurong East", 420),
        ("King Albert Park", 540),
        ("Little India", 480),
        ("MacPherson", 360),
        ("Marina Bay", 600),
        ("Newton", 540),
        ("Nicoll Highway", 360),  # Interchange for ccl_e
        ("Orchard", 480),
        ("Outram Park", 480),
        ("Pasir Ris", 480),
        ("Paya Lebar", 480),
        ("Promenade", 420),
        ("Punggol", 420),
        ("Raffles Place", 360),
        ("Riviera", 480),
        ("Sengkang", 420),
        ("Serangoon", 480),
        ("Stadium", 360),  # Interchange for ccl_e
        ("Stevens", 420),
        ("Sungei Bedok", 540),
        ("Sungei Kadut", 480),
        ("Tampines", 720),
        ("Tanah Merah", 420),
        ("Tengah", 360),
        ("Woodlands", 540),
    )

    def __new__(cls, name, bases, dct):
        cls.interchange_transfers = {
            station_name: duration
            for station_name, duration in cls.__interchange_transfers
        }
        if len(cls.interchange_transfers) != len(cls.__interchange_transfers):
            raise AttributeError(
                "Duplicate station names are not allowed."
            )  # pragma: no cover
        if any(duration <= 0 for duration in cls.interchange_transfers.values()):
            raise AttributeError(
                "Transfer duration must be positive."
            )  # pragma: no cover

        return super().__new__(cls, name, bases, dct)


class Transfers(metaclass=TransfersMeta):
    pass
