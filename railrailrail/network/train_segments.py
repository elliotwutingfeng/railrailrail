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

from railrailrail.network.station import SingaporeStation


class TrainSegmentsMeta(type):
    """Duration presets for all train segments, which includes future train segments (e.g. NS3 -> NS3A),
    defunct train segments, and soon-to-be-defunct train segments (e.g. BP6 -> BP14, NS3 -> NS4).

    A train segment is an edge between any 2 adjacent stations traversed via train; not a transfer and not a walking route.
    The two stations almost always have the same line code, except for "EW15-NS26" before EWL opening.
    """

    __train_segments: tuple = (
        ("BP1-BP2", ("duration", 85)),
        ("BP2-BP3", ("duration", 50)),
        ("BP3-BP4", ("duration", 60)),
        ("BP4-BP5", ("duration", 60)),
        ("BP5-BP6", ("duration", 90)),
        ("BP6-BP7", ("duration", 60)),
        ("BP6-BP13", ("duration", 70)),
        ("BP6-BP14", ("duration", 120)),  # defunct
        ("BP7-BP8", ("duration", 85)),
        ("BP8-BP9", ("duration", 60)),
        ("BP9-BP10", ("duration", 105)),
        ("BP10-BP11", ("duration", 60)),
        ("BP11-BP12", ("duration", 80)),
        ("BP12-BP13", ("duration", 60)),
        ("CC1-CC2", ("duration", 85)),
        ("CC2-CC3", ("duration", 85)),
        ("CC3-CC4", ("duration", 110)),
        ("CC4-CC5", ("duration", 105)),
        ("CC4-CC34", ("duration", 115)),
        ("CC5-CC6", ("duration", 120)),
        ("CC6-CC7", ("duration", 85)),
        ("CC7-CC8", ("duration", 85)),
        ("CC8-CC9", ("duration", 115)),
        ("CC9-CC10", ("duration", 100)),
        ("CC10-CC11", ("duration", 100)),
        ("CC11-CC12", ("duration", 110)),
        ("CC12-CC13", ("duration", 125)),
        ("CC13-CC14", ("duration", 100)),
        ("CC14-CC15", ("duration", 135)),
        ("CC15-CC16", ("duration", 130)),
        ("CC16-CC17", ("duration", 100)),
        ("CC17-CC18", ("duration", 110)),  # future
        ("CC17-CC19", ("duration", 245)),
        ("CC18-CC19", ("duration", 175)),  # future
        ("CC19-CC20", ("duration", 100)),
        ("CC20-CC21", ("duration", 125)),
        ("CC21-CC22", ("duration", 95)),
        ("CC22-CC23", ("duration", 90)),
        ("CC23-CC24", ("duration", 90)),
        ("CC24-CC25", ("duration", 120)),
        ("CC25-CC26", ("duration", 105)),
        ("CC26-CC27", ("duration", 115)),
        ("CC27-CC28", ("duration", 90)),
        ("CC28-CC29", ("duration", 195)),
        ("CC29-CC30", ("duration", 110)),  # future
        ("CC30-CC31", ("duration", 95)),  # future
        ("CC31-CC32", ("duration", 115)),  # future
        ("CC32-CC33", ("duration", 105)),  # future
        ("CC33-CC34", ("duration", 110)),
        ("CE0X-CE0Y", ("duration", 120)),
        ("CE0Y-CE0Z", ("duration", 105)),
        ("CE0Z-CE1", ("duration", 115)),
        ("CE1-CE2", ("duration", 110)),
        ("CG-CG1", ("duration", 135)),
        ("CG1-CG2", ("duration", 255)),
        ("CP1-CP2", ("duration", 240)),  # future
        ("CP2-CP3", ("duration", 360)),  # future
        ("CP3-CP4", ("duration", 240)),  # future
        ("CR1-CR2", ("duration", 240)),  # future
        ("CR2-CR3", ("duration", 270)),  # future
        ("CR3-CR4", ("duration", 120)),  # future
        ("CR4-CR5", ("duration", 120)),  # future
        ("CR5-CR6", ("duration", 120)),  # future
        ("CR6-CR7", ("duration", 480)),  # future
        ("CR7-CR8", ("duration", 120)),  # future
        ("CR8-CR9", ("duration", 240)),  # future
        ("CR9-CR10", ("duration", 180)),  # future
        ("CR10-CR11", ("duration", 180)),  # future
        ("CR11-CR12", ("duration", 120)),  # future
        ("CR12-CR13", ("duration", 180)),  # future
        ("CR13-CR14", ("duration", 540)),  # future
        ("CR14-CR15", ("duration", 180)),  # future
        ("CR15-CR16", ("duration", 120)),  # future
        ("CR16-CR17", ("duration", 240)),  # future
        ("CR17-CR18", ("duration", 120)),  # future
        ("CR18-CR19", ("duration", 300)),  # future
        ("DT-DT1", ("duration", 245)),  # future
        ("DT1-DT2", ("duration", 85)),
        ("DT2-DT3", ("duration", 75)),
        ("DT3-DT4", ("duration", 75)),  # future
        ("DT3-DT5", ("duration", 175)),
        ("DT4-DT5", ("duration", 120)),  # future
        ("DT5-DT6", ("duration", 90)),
        ("DT6-DT7", ("duration", 105)),
        ("DT7-DT8", ("duration", 90)),
        ("DT8-DT9", ("duration", 80)),
        ("DT9-DT10", ("duration", 90)),
        ("DT10-DT11", ("duration", 105)),
        ("DT11-DT12", ("duration", 105)),
        ("DT12-DT13", ("duration", 55)),
        ("DT13-DT14", ("duration", 70)),
        ("DT14-DT15", ("duration", 80)),
        ("DT15-DT16", ("duration", 95)),
        ("DT16-DT17", ("duration", 70)),
        ("DT17-DT18", ("duration", 60)),
        ("DT18-DT19", ("duration", 55)),
        ("DT19-DT20", ("duration", 105)),
        ("DT20-DT21", ("duration", 75)),
        ("DT21-DT22", ("duration", 70)),
        ("DT22-DT23", ("duration", 90)),
        ("DT23-DT24", ("duration", 100)),
        ("DT24-DT25", ("duration", 125)),
        ("DT25-DT26", ("duration", 75)),
        ("DT26-DT27", ("duration", 80)),
        ("DT27-DT28", ("duration", 90)),
        ("DT28-DT29", ("duration", 80)),
        ("DT29-DT30", ("duration", 110)),
        ("DT30-DT31", ("duration", 115)),
        ("DT31-DT32", ("duration", 100)),
        ("DT32-DT33", ("duration", 100)),
        ("DT33-DT34", ("duration", 160)),
        ("DT34-DT35", ("duration", 75)),
        ("DT35-DT36", ("duration", 70)),  # future
        ("DT36-DT37", ("duration", 95)),  # future
        ("EW1-EW2", ("duration", 150)),
        ("EW2-EW3", ("duration", 105)),
        ("EW3-EW4", ("duration", 150)),
        ("EW4-EW5", ("duration", 125)),
        ("EW5-EW6", ("duration", 140)),
        ("EW6-EW7", ("duration", 85)),
        ("EW7-EW8", ("duration", 85)),
        ("EW8-EW9", ("duration", 95)),
        ("EW9-EW10", ("duration", 100)),
        ("EW10-EW11", ("duration", 85)),
        ("EW11-EW12", ("duration", 85)),
        ("EW12-EW13", ("duration", 85)),
        ("EW13-EW14", ("duration", 90)),
        ("EW14-EW15", ("duration", 105)),
        ("EW15-EW16", ("duration", 85)),
        (
            "EW15-NS26",
            ("duration", 105),
        ),  # defunct. Same as EW14-EW15. Only used before EWL opening.
        ("EW16-EW17", ("duration", 130)),
        ("EW17-EW18", ("duration", 105)),
        ("EW18-EW19", ("duration", 100)),
        ("EW19-EW20", ("duration", 90)),
        ("EW20-EW21", ("duration", 90)),
        ("EW21-EW22", ("duration", 105)),
        ("EW21-EW23", ("duration", 300)),  # defunct
        ("EW22-EW23", ("duration", 120)),
        ("EW23-EW24", ("duration", 260)),
        ("EW24-EW25", ("duration", 105)),
        ("EW25-EW26", ("duration", 110)),
        ("EW26-EW27", ("duration", 145)),
        ("EW27-EW28", ("duration", 80)),
        ("EW28-EW29", ("duration", 170)),
        ("EW29-EW30", ("duration", 150)),
        ("EW30-EW31", ("duration", 125)),
        ("EW31-EW32", ("duration", 95)),
        ("EW32-EW33", ("duration", 105)),
        ("JE0-JE1", ("duration", 100)),  # future
        ("JE1-JE2", ("duration", 80)),  # future
        ("JE2-JE3", ("duration", 85)),  # future
        ("JE3-JE4", ("duration", 80)),  # future
        ("JE4-JE5", ("duration", 85)),  # future
        ("JE5-JE6", ("duration", 90)),  # future
        ("JE6-JE7", ("duration", 80)),  # future
        ("JS1-JS2", ("duration", 90)),  # future
        ("JS2-JS3", ("duration", 140)),  # future
        ("JS3-JS4", ("duration", 100)),  # future
        ("JS4-JS5", ("duration", 125)),  # future
        ("JS5-JS6", ("duration", 85)),  # future
        ("JS6-JS7", ("duration", 80)),  # future
        ("JS7-JS8", ("duration", 95)),  # future
        ("JS7-JW1", ("duration", 75)),  # future
        ("JS8-JS9", ("duration", 85)),  # future
        ("JS9-JS10", ("duration", 85)),  # future
        ("JS10-JS11", ("duration", 85)),  # future
        ("JS11-JS12", ("duration", 75)),  # future
        ("JW1-JW2", ("duration", 85)),  # future
        ("JW2-JW3", ("duration", 80)),  # future
        ("JW3-JW4", ("duration", 90)),  # future
        ("JW4-JW5", ("duration", 80)),  # future
        ("NE1-NE3", ("duration", 170)),
        ("NE3-NE4", ("duration", 75)),
        ("NE4-NE5", ("duration", 70)),
        ("NE5-NE6", ("duration", 115)),
        ("NE6-NE7", ("duration", 90)),
        ("NE7-NE8", ("duration", 80)),
        ("NE8-NE9", ("duration", 95)),
        ("NE9-NE10", ("duration", 125)),
        ("NE10-NE11", ("duration", 80)),
        ("NE10-NE12", ("duration", 190)),  # defunct
        ("NE11-NE12", ("duration", 100)),
        ("NE12-NE13", ("duration", 130)),
        ("NE13-NE14", ("duration", 120)),
        ("NE14-NE15", ("duration", 105)),
        ("NE14-NE16", ("duration", 215)),  # defunct
        ("NE15-NE16", ("duration", 90)),
        ("NE16-NE17", ("duration", 130)),
        ("NE17-NE18", ("duration", 115)),  # future
        ("NS1-NS2", ("duration", 225)),
        ("NS2-NS3", ("duration", 95)),
        ("NS3-NS3A", ("duration", 120)),  # future
        ("NS3-NS4", ("duration", 205)),
        ("NS3A-NS4", ("duration", 135)),  # future
        ("NS4-NS5", ("duration", 120)),
        ("NS5-NS6", ("duration", 140)),  # future
        ("NS5-NS7", ("duration", 250)),
        ("NS6-NS7", ("duration", 155)),  # future
        ("NS7-NS8", ("duration", 125)),
        ("NS8-NS9", ("duration", 125)),
        ("NS9-NS10", ("duration", 135)),
        ("NS10-NS11", ("duration", 150)),
        ("NS11-NS12", ("duration", 110)),
        ("NS11-NS13", ("duration", 240)),  # defunct
        ("NS12-NS13", ("duration", 120)),
        ("NS13-NS14", ("duration", 105)),
        ("NS14-NS15", ("duration", 300)),
        ("NS15-NS16", ("duration", 115)),
        ("NS16-NS17", ("duration", 160)),
        ("NS17-NS18", ("duration", 95)),
        ("NS18-NS19", ("duration", 95)),
        ("NS19-NS20", ("duration", 110)),
        ("NS20-NS21", ("duration", 100)),
        ("NS21-NS22", ("duration", 110)),
        ("NS22-NS23", ("duration", 100)),
        ("NS23-NS24", ("duration", 75)),
        ("NS24-NS25", ("duration", 85)),
        ("NS25-NS26", ("duration", 100)),
        ("NS26-NS27", ("duration", 90)),
        ("NS27-NS28", ("duration", 115)),
        ("PE1-PE2", ("duration", 55)),
        ("PE2-PE3", ("duration", 60)),
        ("PE3-PE4", ("duration", 60)),
        ("PE4-PE5", ("duration", 75)),
        ("PE5-PE6", ("duration", 55)),
        ("PE6-PE7", ("duration", 55)),
        ("PTC-PE1", ("duration", 120)),
        ("PTC-PE5", ("duration", 210)),  # defunct
        ("PTC-PE6", ("duration", 180)),  # defunct
        ("PTC-PE7", ("duration", 135)),
        ("PTC-PW1", ("duration", 90)),
        ("PTC-PW5", ("duration", 270)),  # defunct
        ("PTC-PW7", ("duration", 145)),
        ("PW1-PW2", ("duration", 50)),  # future
        ("PW1-PW3", ("duration", 125)),
        ("PW1-PW5", ("duration", 265)),  # defunct
        ("PW2-PW3", ("duration", 65)),  # future
        ("PW3-PW4", ("duration", 70)),
        ("PW3-PW5", ("duration", 140)),  # defunct
        ("PW4-PW5", ("duration", 60)),
        ("PW5-PW6", ("duration", 50)),
        ("PW6-PW7", ("duration", 55)),
        ("SE1-SE2", ("duration", 75)),
        ("SE2-SE3", ("duration", 55)),
        ("SE3-SE4", ("duration", 70)),
        ("SE4-SE5", ("duration", 90)),
        ("STC-SE1", ("duration", 100)),
        ("STC-SE5", ("duration", 150)),
        ("STC-SW1", ("duration", 125)),
        ("STC-SW2", ("duration", 190)),  # defunct
        ("STC-SW4", ("duration", 355)),  # defunct
        ("STC-SW8", ("duration", 155)),
        ("SW1-SW2", ("duration", 55)),
        ("SW2-SW3", ("duration", 75)),
        ("SW2-SW4", ("duration", 165)),  # defunct
        ("SW3-SW4", ("duration", 80)),
        ("SW4-SW5", ("duration", 75)),
        ("SW5-SW6", ("duration", 65)),
        ("SW6-SW7", ("duration", 70)),
        ("SW7-SW8", ("duration", 65)),
        ("TE1-TE2", ("duration", 125)),
        ("TE2-TE3", ("duration", 105)),
        ("TE3-TE4", ("duration", 250)),
        ("TE4-TE4A", ("duration", 110)),  # future
        ("TE4-TE5", ("duration", 160)),
        ("TE4A-TE5", ("duration", 105)),  # future
        ("TE5-TE6", ("duration", 125)),
        ("TE6-TE7", ("duration", 95)),
        ("TE7-TE8", ("duration", 115)),
        ("TE8-TE9", ("duration", 165)),
        ("TE9-TE10", ("duration", 105)),  # future
        ("TE9-TE11", ("duration", 185)),
        ("TE10-TE11", ("duration", 120)),  # future
        ("TE11-TE12", ("duration", 135)),
        ("TE12-TE13", ("duration", 75)),
        ("TE13-TE14", ("duration", 95)),
        ("TE14-TE15", ("duration", 105)),
        ("TE15-TE16", ("duration", 70)),
        ("TE16-TE17", ("duration", 90)),
        ("TE17-TE18", ("duration", 60)),
        ("TE18-TE19", ("duration", 75)),
        ("TE19-TE20", ("duration", 65)),
        ("TE20-TE21", ("duration", 95)),  # future
        ("TE20-TE22", ("duration", 130)),
        ("TE21-TE22", ("duration", 75)),  # future
        ("TE22-TE22A", ("duration", 120)),  # future
        ("TE22-TE23", ("duration", 195)),
        ("TE22A-TE23", ("duration", 90)),  # future
        ("TE23-TE24", ("duration", 115)),
        ("TE24-TE25", ("duration", 115)),
        ("TE25-TE26", ("duration", 100)),
        ("TE26-TE27", ("duration", 95)),
        ("TE27-TE28", ("duration", 125)),
        ("TE28-TE29", ("duration", 125)),
        ("TE29-TE30", ("duration", 90)),  # future
        ("TE30-TE31", ("duration", 95)),  # future
        ("TE31-TE32", ("duration", 290)),  # future
        ("TE32-TE33", ("duration", 185)),  # future
        ("TE33-TE34", ("duration", 250)),  # future
        ("TE34-TE35", ("duration", 145)),  # future
    )

    def __new__(cls, name, bases, dct):
        cls.train_segments = dict()
        pairs: set[tuple[str, str]] = set()
        for segment, *details in cls.__train_segments:
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
            SingaporeStation.to_station_code_components(
                station_code_1
            )  # Raises ValueError if invalid.
            SingaporeStation.to_station_code_components(
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
            cls.train_segments[segment] = segment_details

        return super().__new__(cls, name, bases, dct)


class TrainSegments(metaclass=TrainSegmentsMeta):
    pass
