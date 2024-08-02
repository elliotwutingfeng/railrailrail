<div align="center">
  <h3 align="center">railrailrail</h3>
  <img src="images/train.svg" alt="Train" width="200" height="200">

  <p align="center">
  Route planner for all stages of the Singapore MRT/LRT rail network (1987-2040+).
  </p>

  <p align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python"/></a>
  </p>

  <p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/SOURCE_CODE_LICENSE-Apache--2.0-GREEN?style=for-the-badge" alt="Apache-2.0 license"/></a>
  <a href="LICENSE-DATASET"><img src="https://img.shields.io/badge/DATASET_LICENSE-SODL--1.0%20AND%20ODbL--1.0-GREEN?style=for-the-badge" alt="SODL-1.0 and ODbL-1.0 License"/></a>
  </p>
</div>

railrailrail finds fastest routes between any 2 stations on the Singapore MRT/LRT rail network. It supports all known past and future stages of the network (1987-2040+).

## Features

- Preset configurations for all known stages of the MRT/LRT network, in the [TOML](https://toml.io) file format.
- Customize every station-to-station travel time, interchange transfer time, and station dwell time, by editing the TOML config file directly.
- Handle conditional transfers such as at JS7 Bahar Junction, or the Circle Line Extension; can be modified via TOML config files.
- Optionally enable walking routes between nearby stations; can be modified via TOML config files.
- Find the circuity ratio of a fastest route. The circuity ratio is the total distance travelled divided by the great-circle distance between origin station and destination station. Smaller circuity ratio implies a more direct (efficient) route.

## Requirements

- Python 3.12+
- [Python Poetry](https://python-poetry.org)
- GNU Make

Works natively on a POSIX environment like Linux/macOS. Windows users should use the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install).

## Setup

Install dependencies.

```bash
make install
```

Then generate a coordinates file (station_coordinates.csv), and network config files for all stages.
These files will be saved to the `config/` folder.

```bash
make generate_config
```

## Commands

### route

Use `route` to get the fastest route between 2 stations.

Four arguments are required:

- `--start`: Origin station code. Example: **NS14**.
- `--end`: Destination station code. Example: **TE29**.
- `--coordinates-file`: Path to CSV file with location coordinates for every station. Example: [station_coordinates.csv](config_examples/station_coordinates.csv)
- `--network-file`: Path to network config file with rail network [graph](https://en.wikipedia.org/wiki/Graph_theory) node and edge details. Example: [network_tel_4.toml](config_examples/network_tel_4.toml)

```bash
poetry run python railrailrail/cli.py route --coordinates-file config/station_coordinates.csv --network-file config/network_tel_4.toml  --start NS14 --end TE29

# Start at NS14 Khatib
# Board train towards terminus NS28 Marina South Pier
# Alight at NS22 Orchard
# Transfer to TE14 Orchard
# Board train towards terminus TE29 Bayshore
# Alight at TE29 Bayshore
# Total duration: 73 minutes 41 seconds
# Approximate path distance: 29.7 km, Haversine distance: 16.8 km, Circuity ratio: 1.8
```

#### Walking routes

Walking routes can be enabled with the optional `--walk` flag. These routes are taken from the [LTA Walking Train Map (WTM)](https://www.lta.gov.sg/content/dam/ltagov/who_we_are/statistics_and_publications/pdf/connect_nov_2018_fa_12nov.pdf)

```bash
poetry run python railrailrail/cli.py route --walk --coordinates-file config/station_coordinates.csv --network-file config/network_tel_4.toml  --start DT13 --end TE29

# Start at DT13 Rochor
# Board train towards terminus DT35 Expo
# Alight at DT17 Downtown
# Walk to TE20 Marina Bay
# Board train towards terminus TE29 Bayshore
# Alight at TE29 Bayshore
# Total duration: 38 minutes 44 seconds
# Approximate path distance: 15.6 km, Haversine distance: 10.0 km, Circuity ratio: 1.6
```

#### Past and future networks

Use a different `--network-file` to calculate fastest routes for both past and future versions of the network.

**Example:** EW1 Pasir Ris to NS17 Bishan

EW22 Dover opened.

```bash
poetry run python railrailrail/cli.py route --network-file config/network_dover.toml --coordinates-file config/station_coordinates.csv --start EW1 --end NS17

# Start at EW1 Pasir Ris
# Board train towards terminus EW27 Boon Lay
# Alight at EW13 City Hall
# Transfer to NS25 City Hall
# Board train towards terminus NS1 Jurong East
# Alight at NS17 Bishan
# Total duration: 67 minutes 26 seconds
# Approximate path distance: 25.6 km, Haversine distance: 11.5 km, Circuity ratio: 2.2
```

Circle Line Stage 4 and Stage 5 opened.

```bash
poetry run python railrailrail/cli.py route --network-file config/network_ccl_4_and_ccl_5.toml --coordinates-file config/station_coordinates.csv --start EW1 --end NS17

# Start at EW1 Pasir Ris
# Board train towards terminus EW29 Joo Koon
# Alight at EW8 Paya Lebar
# Transfer to CC9 Paya Lebar
# Board train towards terminus CC29 HarbourFront
# Alight at CC15 Bishan
# Transfer to NS17 Bishan
# Total duration: 47 minutes 27 seconds
# Approximate path distance: 19.0 km, Haversine distance: 11.5 km, Circuity ratio: 1.7
```

Cross Island Line 2 opened.

```bash
poetry run python railrailrail/cli.py route --network-file config/network_crl_2.toml --coordinates-file config/station_coordinates.csv --start EW1 --end NS17

# Start at EW1 Pasir Ris
# Transfer to CR5 Pasir Ris
# Board train towards terminus CR19 Jurong Lake District
# Alight at CR11 Ang Mo Kio
# Transfer to NS16 Ang Mo Kio
# Board train towards terminus NS28 Marina South Pier
# Alight at NS17 Bishan
# Total duration: 40 minutes 7 seconds
# Approximate path distance: 13.9 km, Haversine distance: 11.5 km, Circuity ratio: 1.2
```

### generate

> [!TIP]
> You do not need to do this if you already ran `make generate_config` in the Setup section.

Use `generate` to generate the station coordinates file and network config files for the route planner.

#### Station Coordinates File

Generate a station `--coordinates` file (**station_coordinates.csv**).

```bash
poetry run python railrailrail/cli.py generate --coordinates
```

#### Network Config File

Generate a `--network` config file with preset time durations for a given stage (e.g. `sklrt_east_loop`, `ccl_3`)

Run `generate --help` to get all possible arguments for `--network`.

```bash
poetry run python railrailrail/cli.py generate --help
poetry run python railrailrail/cli.py generate --network sklrt_east_loop
```

## Customization

The generated network config files (ending with `.toml`) and the station coordinates file (**station_coordinates.csv**) in the `config`
folder can be customized. See [CONFIG.md](CONFIG.md).

## Future stages

These stages are tentative and subject to detailed planning.

### CRL Phase 3

<https://www.straitstimes.com/singapore/possible-interchanges-in-king-albert-park-clementi-jurong-pier-gul-circle-for-cross-island>

- CR20
- CR21/JS12 Jurong Pier
- CR22
- CR23
- CR24/EW30 Gul Circle

## Issues

- The preset travel durations between adjacent stations are based on estimates provided by SMRT/SBS Transit which may or may not factor in time spent at station waiting for passengers to board/disembark (dwell time). The estimates also generally have wide 1 minute margin of error, so either 61 seconds or 179 seconds can count as an estimated 2 minutes.
- The approximate path distance metric treats adjacent stations as being connected directly by their great-circle distance. Real paths between adjacent stations are not "straight lines", so the actual path distance should be higher. Actual rail path data will be included in the future.

## License

Source code is under Apache-2.0. Most of the dataset is under the Singapore Open Data Licence version 1.0, while some of the coordinate
data are under Open Data Commons Open Database License (ODbL).

See [LICENSE](LICENSE) and [LICENSE-DATASET](LICENSE-DATASET).

## References

- TransitLink
  - [MRT/LRT Journey Information](https://www.transitlink.com.sg/eservice/eguide/rail_idx.php)
- SMRT
  - [SMRT Journey Planner](https://journey.smrt.com.sg)
- SBS Transit
  - [Travel Time](https://www.sbstransit.com.sg/travel-time)
- Thomson-East Coast Line (TEL) Dwell times by u/xavierang2 on Reddit
  - [Reddit post](https://www.reddit.com/r/singapore/comments/z6i58u/some_observations_about_the_thomsoneast_coast)
  - [Timetable](https://docs.google.com/document/d/1LO1lB0jptt8UJnlUYUd3KxYqSmKoyvIauf6DNYVlb5w)
- Measured interchange transfer times by a deleted user on Reddit
  - [Reddit post](https://www.reddit.com/r/singapore/comments/10wkygf/mrt_map_with_transfer_timing)
  - [Timetable](https://docs.google.com/spreadsheets/d/1e-Tuf6rHBFsgsuFN7XqbFL8ec_vdRjQw)
- Singapore Train Station Coordinates
  - [GitHub Repo](https://github.com/elliotwutingfeng/singapore_train_station_coordinates)
