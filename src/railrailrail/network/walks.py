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


class WalksMeta(type):
    """Walking routes and their estimated durations between some stations.

    From [LTA Walking Train Map (WTM)](https://www.lta.gov.sg/content/dam/ltagov/who_we_are/statistics_and_publications/pdf/connect_nov_2018_fa_12nov.pdf)
    """

    __routes: tuple[tuple[str, str, int], ...] = (
        ("Bras Basah", "Bencoolen", 120),
        ("Dhoby Ghaut", "Bencoolen", 300),
        ("Esplanade", "City Hall", 300),
        ("Marina Bay", "Downtown", 300),
        ("Rochor", "Jalan Besar", 300),
        ("Telok Ayer", "Raffles Place", 300),
        ("Shenton Way", "Downtown", 360),
        ("Bras Basah", "City Hall", 420),
        ("Downtown", "Raffles Place", 420),
        ("Maxwell", "Tanjong Pagar", 480),
        ("Telok Ayer", "Tanjong Pagar", 480),
        ("Jalan Besar", "Bugis", 540),
        ("Rochor", "Bencoolen", 540),
        ("Boon Keng", "Bendemeer", 600),
        ("Bras Basah", "Bugis", 600),
        ("Chinatown", "Maxwell", 600),
        ("Clarke Quay", "Raffles Place", 600),
        ("Fort Canning", "Clarke Quay", 600),
        ("Little India", "Jalan Besar", 600),
        ("Shenton Way", "Tanjong Pagar", 600),
        ("Chinatown", "Raffles Place", 660),
        ("Maxwell", "Telok Ayer", 660),
        ("Esplanade", "Bugis", 720),
        ("Shenton Way", "Raffles Place", 720),
    )

    def __new__(cls, name, bases, dct):
        pairs: set[tuple[str, str]] = set()
        for station_name_1, station_name_2, duration in cls.__routes:
            if (
                station_name_1 == station_name_2
                or not isinstance(station_name_1, str)
                or not isinstance(station_name_2, str)
                or type(duration) is not int
                or duration <= 0
            ):
                raise AttributeError(
                    f"Route must be between 2 different names with a positive duration. Got {station_name_1}, {station_name_2}, {duration}"
                )  # pragma: no cover
            pair = (
                (station_name_1, station_name_2)
                if station_name_1 < station_name_2
                else (station_name_2, station_name_1)
            )
            if pair in pairs:
                raise AttributeError(
                    f"Duplicate route not allowed: {station_name_1}, {station_name_2}"
                )  # pragma: no cover
            pairs.add(pair)
        cls.routes = cls.__routes  # pyrefly: ignore
        return super().__new__(cls, name, bases, dct)


class Walks(metaclass=WalksMeta):
    pass
