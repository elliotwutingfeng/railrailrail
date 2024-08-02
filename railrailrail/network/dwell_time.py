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

from railrailrail.network.station import Station


class DwellTime:
    """Standard dwell time presets.

    Reference: https://www.railengineer.co.uk/an-international-metro-review
    """

    non_interchange = 28
    interchange = 45
    terminal = 60

    @classmethod
    def get_dwell_time(
        cls,
        terminal_station_codes: set[str],
        interchange_station_codes: set[str],
        current_station: str,
        next_station: str,
    ) -> tuple[int, int]:
        """Assign dwell time based on whether origin station is a non-interchange, interchange or terminus.

        Args:
            terminal_station_codes (set[str]): Station codes belonging to terminals.
            interchange_station_codes (set[str]): Station codes belonging to interchanges.
            current_station (str): Current station code.
            next_station (str): Next station code.

        Returns:
            tuple[int, int]: Direction-specific dwell times; in ascending and in descending order of station codes.
        """
        is_ascending: bool = Station.to_station_code_components(
            current_station
        ) < Station.to_station_code_components(next_station)
        smaller = current_station if is_ascending else next_station
        larger = next_station if is_ascending else current_station

        dwell_time_asc = cls.non_interchange
        dwell_time_desc = cls.non_interchange

        # Check if station is interchange.
        if smaller in interchange_station_codes:
            dwell_time_asc = max(dwell_time_asc, cls.interchange)
        if larger in interchange_station_codes:
            dwell_time_desc = max(dwell_time_desc, cls.interchange)

        # Check if station is terminal.
        if smaller in terminal_station_codes:
            dwell_time_asc = max(dwell_time_asc, cls.terminal)
        if larger in terminal_station_codes:
            dwell_time_desc = max(dwell_time_desc, cls.terminal)

        return dwell_time_asc, dwell_time_desc
