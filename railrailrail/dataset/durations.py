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

from railrailrail.dataset.station import Station


class DurationsMeta(type):
    """Standard duration presets."""

    # All possible rail segments between any 2 adjacent stations on the same line.
    # This includes segments that have yet to exist (e.g. NS3 -> NS3A),
    # and segments that no longer exist or will be removed in the future (e.g. BP6 -> BP14, NS3 -> NS4).
    __segments: tuple = (
        ("BP1-BP2", ("duration", 120)),
        ("BP2-BP3", ("duration", 60)),
        ("BP3-BP4", ("duration", 120)),
        ("BP4-BP5", ("duration", 60)),
        ("BP5-BP6", ("duration", 60)),
        ("BP6-BP7", ("duration", 60)),
        ("BP6-BP13", ("duration", 120)),
        ("BP6-BP14", ("duration", 60)),
        ("BP7-BP8", ("duration", 120)),
        ("BP8-BP9", ("duration", 60)),
        ("BP9-BP10", ("duration", 120)),
        ("BP10-BP11", ("duration", 60)),
        ("BP11-BP12", ("duration", 60)),
        ("BP12-BP13", ("duration", 120)),
        ("CC1-CC2", ("duration", 180)),
        ("CC2-CC3", ("duration", 180)),
        ("CC3-CC4", ("duration", 180)),
        ("CC4-CC5", ("duration", 360)),
        ("CC4-CC34", ("duration", 180)),
        ("CC5-CC6", ("duration", 120)),
        ("CC6-CC7", ("duration", 120)),
        ("CC7-CC8", ("duration", 120)),
        ("CC8-CC9", ("duration", 120)),
        ("CC9-CC10", ("duration", 120)),
        ("CC10-CC11", ("duration", 120)),
        ("CC11-CC12", ("duration", 120)),
        ("CC12-CC13", ("duration", 120)),
        ("CC13-CC14", ("duration", 120)),
        ("CC14-CC15", ("duration", 120)),
        ("CC15-CC16", ("duration", 120)),
        ("CC16-CC17", ("duration", 120)),
        ("CC17-CC18", ("duration", 120)),
        ("CC17-CC19", ("duration", 300)),
        ("CC18-CC19", ("duration", 240)),
        ("CC19-CC20", ("duration", 120)),
        ("CC20-CC21", ("duration", 120)),
        ("CC21-CC22", ("duration", 120)),
        ("CC22-CC23", ("duration", 120)),
        ("CC23-CC24", ("duration", 120)),
        ("CC24-CC25", ("duration", 120)),
        ("CC25-CC26", ("duration", 120)),
        ("CC26-CC27", ("duration", 120)),
        ("CC27-CC28", ("duration", 120)),
        ("CC28-CC29", ("duration", 120)),
        ("CC29-CC30", ("duration", 120)),
        ("CC30-CC31", ("duration", 60)),
        ("CC31-CC32", ("duration", 60)),
        ("CC32-CC33", ("duration", 60)),
        ("CC33-CC34", ("duration", 120)),
        ("CC33-DT17", ("duration", 300)),
        ("CE0X-CE0Y", ("duration", 120)),
        ("CE0Y-CE0Z", ("duration", 360)),
        ("CE0Z-CE1", ("duration", 180)),
        ("CE1-CE2", ("duration", 120)),
        ("CG-CG1", ("duration", 180)),
        ("CG1-CG2", ("duration", 240)),
        ("CP1-CP2", ("duration", 240)),
        ("CP2-CP3", ("duration", 360)),
        ("CP3-CP4", ("duration", 240)),
        ("CR1-CR2", ("duration", 240)),
        ("CR2-CR3", ("duration", 360)),
        ("CR3-CR4", ("duration", 180)),
        ("CR4-CR5", ("duration", 180)),
        ("CR5-CR6", ("duration", 120)),
        ("CR6-CR7", ("duration", 480)),
        ("CR7-CR8", ("duration", 120)),
        ("CR8-CR9", ("duration", 240)),
        ("CR9-CR10", ("duration", 180)),
        ("CR10-CR11", ("duration", 180)),
        ("CR11-CR12", ("duration", 120)),
        ("CR12-CR13", ("duration", 180)),
        ("CR13-CR14", ("duration", 540)),
        ("CR14-CR15", ("duration", 180)),
        ("CR15-CR16", ("duration", 120)),
        ("CR16-CR17", ("duration", 240)),
        ("CR17-CR18", ("duration", 120)),
        ("CR18-CR19", ("duration", 300)),
        ("DT-DT1", ("duration", 420)),
        ("DT1-DT2", ("duration", 120)),
        ("DT2-DT3", ("duration", 120)),
        ("DT3-DT4", ("duration", 120)),
        ("DT3-DT5", ("duration", 180)),
        ("DT4-DT5", ("duration", 180)),
        ("DT5-DT6", ("duration", 120)),
        ("DT6-DT7", ("duration", 120)),
        ("DT7-DT8", ("duration", 120)),
        ("DT8-DT9", ("duration", 120)),
        ("DT9-DT10", ("duration", 120)),
        ("DT10-DT11", ("duration", 120)),
        ("DT11-DT12", ("duration", 180)),
        ("DT12-DT13", ("duration", 60)),
        ("DT13-DT14", ("duration", 120)),
        ("DT14-DT15", ("duration", 120)),
        ("DT15-DT16", ("duration", 120)),
        ("DT16-DT17", ("duration", 120)),
        ("DT17-DT18", ("duration", 60)),
        ("DT18-DT19", ("duration", 120)),
        ("DT19-DT20", ("duration", 120)),
        ("DT20-DT21", ("duration", 120)),
        ("DT21-DT22", ("duration", 60)),
        ("DT22-DT23", ("duration", 120)),
        ("DT23-DT24", ("duration", 120)),
        ("DT24-DT25", ("duration", 120)),
        ("DT25-DT26", ("duration", 120)),
        ("DT26-DT27", ("duration", 120)),
        ("DT27-DT28", ("duration", 120)),
        ("DT28-DT29", ("duration", 120)),
        ("DT29-DT30", ("duration", 120)),
        ("DT30-DT31", ("duration", 180)),
        ("DT31-DT32", ("duration", 120)),
        ("DT32-DT33", ("duration", 120)),
        ("DT33-DT34", ("duration", 180)),
        ("DT34-DT35", ("duration", 120)),
        ("DT35-DT36", ("duration", 60)),
        ("DT36-DT37", ("duration", 120)),
        ("EW1-EW2", ("duration", 180)),
        ("EW2-EW3", ("duration", 180)),
        ("EW3-EW4", ("duration", 180)),
        ("EW4-EW5", ("duration", 180)),
        ("EW5-EW6", ("duration", 180)),
        ("EW6-EW7", ("duration", 180)),
        ("EW7-EW8", ("duration", 120)),
        ("EW8-EW9", ("duration", 120)),
        ("EW9-EW10", ("duration", 180)),
        ("EW10-EW11", ("duration", 120)),
        ("EW11-EW12", ("duration", 180)),
        ("EW12-EW13", ("duration", 120)),
        ("EW13-EW14", ("duration", 120)),
        ("EW14-EW15", ("duration", 120)),
        ("EW15-EW16", ("duration", 120)),
        ("EW16-EW17", ("duration", 180)),
        ("EW17-EW18", ("duration", 180)),
        ("EW18-EW19", ("duration", 120)),
        ("EW19-EW20", ("duration", 180)),
        ("EW20-EW21", ("duration", 120)),
        ("EW21-EW22", ("duration", 180)),
        ("EW21-EW23", ("duration", 300)),
        ("EW22-EW23", ("duration", 120)),
        ("EW23-EW24", ("duration", 300)),
        ("EW24-EW25", ("duration", 120)),
        ("EW25-EW26", ("duration", 180)),
        ("EW26-EW27", ("duration", 120)),
        ("EW27-EW28", ("duration", 180)),
        ("EW28-EW29", ("duration", 180)),
        ("EW29-EW30", ("duration", 240)),
        ("EW30-EW31", ("duration", 120)),
        ("EW31-EW32", ("duration", 120)),
        ("EW32-EW33", ("duration", 120)),
        ("JE0-JE1", ("duration", 180)),
        ("JE1-JE2", ("duration", 120)),
        ("JE2-JE3", ("duration", 120)),
        ("JE3-JE4", ("duration", 180)),
        ("JE4-JE5", ("duration", 120)),
        ("JE5-JE6", ("duration", 120)),
        ("JE6-JE7", ("duration", 120)),
        ("JS1-JS2", ("duration", 120)),
        ("JS2-JS3", ("duration", 240)),
        ("JS3-JS4", ("duration", 120)),
        ("JS4-JS5", ("duration", 180)),
        ("JS5-JS6", ("duration", 120)),
        ("JS6-JS7", ("duration", 120)),
        ("JS7-JS8", ("duration", 120)),
        ("JS7-JW1", ("duration", 120)),
        ("JS8-JS9", ("duration", 120)),
        ("JS9-JS10", ("duration", 120)),
        ("JS10-JS11", ("duration", 120)),
        ("JS11-JS12", ("duration", 120)),
        ("JW1-JW2", ("duration", 120)),
        ("JW2-JW3", ("duration", 120)),
        ("JW3-JW4", ("duration", 120)),
        ("JW4-JW5", ("duration", 120)),
        ("NE1-NE3", ("duration", 240)),
        ("NE3-NE4", ("duration", 60)),
        ("NE4-NE5", ("duration", 120)),
        ("NE5-NE6", ("duration", 180)),
        ("NE6-NE7", ("duration", 60)),
        ("NE7-NE8", ("duration", 60)),
        ("NE8-NE9", ("duration", 120)),
        ("NE9-NE10", ("duration", 180)),
        ("NE10-NE11", ("duration", 60)),
        ("NE10-NE12", ("duration", 180)),
        ("NE11-NE12", ("duration", 120)),
        ("NE12-NE13", ("duration", 180)),
        ("NE13-NE14", ("duration", 120)),
        ("NE14-NE15", ("duration", 120)),
        ("NE14-NE16", ("duration", 240)),
        ("NE15-NE16", ("duration", 120)),
        ("NE16-NE17", ("duration", 180)),
        ("NE17-NE18", ("duration", 180)),
        ("NS1-NS2", ("duration", 180)),
        ("NS2-NS3", ("duration", 180)),
        ("NS3-NS3A", ("duration", 120)),
        ("NS3-NS4", ("duration", 240)),
        ("NS3A-NS4", ("duration", 120)),
        ("NS4-NS5", ("duration", 120)),
        ("NS5-NS6", ("duration", 180)),
        ("NS5-NS7", ("duration", 300)),
        ("NS6-NS7", ("duration", 120)),
        ("NS7-NS8", ("duration", 180)),
        ("NS8-NS9", ("duration", 180)),
        ("NS9-NS10", ("duration", 180)),
        ("NS10-NS11", ("duration", 180)),
        ("NS11-NS12", ("duration", 180)),
        ("NS11-NS13", ("duration", 300)),
        ("NS12-NS13", ("duration", 180)),
        ("NS13-NS14", ("duration", 120)),
        ("NS14-NS15", ("duration", 300)),
        ("NS15-NS16", ("duration", 180)),
        ("NS16-NS17", ("duration", 240)),
        ("NS17-NS18", ("duration", 120)),
        ("NS18-NS19", ("duration", 120)),
        ("NS19-NS20", ("duration", 180)),
        ("NS20-NS21", ("duration", 120)),
        ("NS21-NS22", ("duration", 180)),
        ("NS22-NS23", ("duration", 120)),
        ("NS23-NS24", ("duration", 120)),
        ("NS24-NS25", ("duration", 180)),
        ("NS25-NS26", ("duration", 120)),
        ("NS26-NS27", ("duration", 120)),
        ("NS27-NS28", ("duration", 120)),
        ("PE1-PE2", ("duration", 60)),
        ("PE2-PE3", ("duration", 60)),
        ("PE3-PE4", ("duration", 60)),
        ("PE4-PE5", ("duration", 60)),
        ("PE5-PE6", ("duration", 60)),
        ("PE6-PE7", ("duration", 60)),
        ("PTC-PE1", ("duration", 180)),
        ("PTC-PE5", ("duration", 240)),
        ("PTC-PE6", ("duration", 180)),
        ("PTC-PE7", ("duration", 120)),
        ("PTC-PW1", ("duration", 120)),
        ("PTC-PW5", ("duration", 300)),
        ("PTC-PW7", ("duration", 180)),
        ("PW1-PW2", ("duration", 60)),
        ("PW1-PW3", ("duration", 120)),
        ("PW1-PW5", ("duration", 240)),
        ("PW2-PW3", ("duration", 60)),
        ("PW3-PW4", ("duration", 60)),
        ("PW3-PW5", ("duration", 120)),
        ("PW4-PW5", ("duration", 60)),
        ("PW5-PW6", ("duration", 60)),
        ("PW6-PW7", ("duration", 60)),
        ("SE1-SE2", ("duration", 60)),
        ("SE2-SE3", ("duration", 60)),
        ("SE3-SE4", ("duration", 60)),
        ("SE4-SE5", ("duration", 120)),
        ("STC-SE1", ("duration", 120)),
        ("STC-SE5", ("duration", 180)),
        ("STC-SW1", ("duration", 120)),
        ("STC-SW2", ("duration", 180)),
        ("STC-SW4", ("duration", 300)),
        ("STC-SW8", ("duration", 180)),
        ("SW1-SW2", ("duration", 60)),
        ("SW2-SW3", ("duration", 60)),
        ("SW2-SW4", ("duration", 120)),
        ("SW3-SW4", ("duration", 60)),
        ("SW4-SW5", ("duration", 60)),
        ("SW5-SW6", ("duration", 60)),
        ("SW6-SW7", ("duration", 60)),
        ("SW7-SW8", ("duration", 60)),
        ("TE1-TE2", ("duration", 120)),
        ("TE2-TE3", ("duration", 120)),
        ("TE3-TE4", ("duration", 300)),
        ("TE4-TE4A", ("duration", 120)),
        ("TE4-TE5", ("duration", 180)),
        ("TE4A-TE5", ("duration", 120)),
        ("TE5-TE6", ("duration", 180)),
        ("TE6-TE7", ("duration", 120)),
        ("TE7-TE8", ("duration", 120)),
        ("TE8-TE9", ("duration", 180)),
        ("TE9-TE10", ("duration", 120)),
        ("TE9-TE11", ("duration", 240)),
        ("TE10-TE11", ("duration", 120)),
        ("TE11-TE12", ("duration", 180)),
        ("TE12-TE13", ("duration", 60)),
        ("TE13-TE14", ("duration", 120)),
        ("TE14-TE15", ("duration", 120)),
        ("TE15-TE16", ("duration", 120)),
        ("TE16-TE17", ("duration", 120)),
        ("TE17-TE18", ("duration", 120)),
        ("TE18-TE19", ("duration", 60)),
        ("TE19-TE20", ("duration", 120)),
        ("TE20-TE21", ("duration", 120)),
        ("TE20-TE22", ("duration", 180)),
        ("TE21-TE22", ("duration", 60)),
        ("TE22-TE22A", ("duration", 120)),
        ("TE22-TE23", ("duration", 240)),
        ("TE22A-TE23", ("duration", 120)),
        ("TE23-TE24", ("duration", 120)),
        ("TE24-TE25", ("duration", 180)),
        ("TE25-TE26", ("duration", 60)),
        ("TE26-TE27", ("duration", 120)),
        ("TE27-TE28", ("duration", 120)),
        ("TE28-TE29", ("duration", 120)),
        ("TE29-TE30", ("duration", 60)),
        ("TE30-TE31", ("duration", 60)),
        ("TE31-TE32", ("duration", 600)),
        ("TE32-TE33", ("duration", 180)),
        ("TE33-TE34", ("duration", 240)),
        ("TE34-TE35", ("duration", 180)),
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
        ("Clementi", 720),
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
        ("Pasir Ris", 720),
        ("Paya Lebar", 480),
        ("Promenade", 420),
        ("Punggol", 420),
        ("Raffles Place", 360),
        ("Riviera", 720),
        ("Sengkang", 420),
        ("Serangoon", 480),
        ("Stadium", 360),  # Interchange for ccl_e
        ("Stevens", 420),
        ("Sungei Bedok", 540),
        ("Sungei Kadut", 720),
        ("Tampines", 720),
        ("Tanah Merah", 420),
        ("Tengah", 360),
        ("Woodlands", 540),
    )

    # Transfers at all possible conditional interchanges, including defunct and future conditional interchanges.
    #
    # As a simplification, treat transfer time in both directions as equal.
    # TODO: Update in the future when more direction-specific transfer time is available.
    #
    __conditional_interchange_transfers: tuple = (
        ("Bahar Junction", 360),
        ("Bukit Panjang", 420),
        ("Promenade", 420),
        ("Punggol", 360),
        ("Sengkang", 360),
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
            Station.to_station_code_components(
                station_code_1
            )  # Raises ValueError if invalid.
            Station.to_station_code_components(
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
            if type(segment_details.get("duration", None)) is not int:
                raise AttributeError(
                    "Segment duration must be int."
                )  # pragma: no cover
            cls.segments[segment] = segment_details

        cls.interchange_transfers = {
            station_name: duration
            for station_name, duration in cls.__interchange_transfers
        }
        if len(cls.interchange_transfers) != len(cls.__interchange_transfers):
            raise AttributeError(
                "Duplicate station names are not allowed."
            )  # pragma: no cover

        cls.conditional_interchange_transfers = {
            station_name: duration
            for station_name, duration in cls.__conditional_interchange_transfers
        }
        if len(cls.conditional_interchange_transfers) != len(
            cls.__conditional_interchange_transfers
        ):
            raise AttributeError(
                "Duplicate station names are not allowed."
            )  # pragma: no cover

        return super().__new__(cls, name, bases, dct)


class Durations(metaclass=DurationsMeta):
    pass
