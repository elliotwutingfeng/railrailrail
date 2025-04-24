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
  <a href="LICENSE-DATASET.md"><img src="https://img.shields.io/badge/DATASET_LICENSE-SODL--1.0-GREEN?style=for-the-badge" alt="SODL-1.0 License"/></a>
  </p>
</div>

railrailrail finds fastest routes between any 2 stations on the Singapore MRT/LRT rail network. It supports all known past and future stages of the network (1987-2040+).

## Features

- Preset configurations for all known stages of the MRT/LRT network, in the [TOML](https://toml.io) file format.
- Customize every station-to-station travel time, interchange transfer time, and station dwell time, by editing the TOML config file directly.
- Optionally enable walking routes between nearby stations.
- Find the circuity ratio of a fastest route. The circuity ratio is the total distance travelled divided by the [great-circle (haversine) distance](https://en.wikipedia.org/wiki/Great-circle_distance) between origin station and destination station. Smaller circuity ratio implies a more direct and efficient route.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv) 0.6.16+
- GNU Make

Works natively on a POSIX/UNIX-like environment like Linux/macOS. Windows users should use the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install).

## Setup

Install dependencies. Then generate a coordinates file (station_coordinates.csv), and network config files for all stages.
These files will be saved to the `config/` folder.

```bash
make install
make generate_config
```

## Basic Usage

Now lets find the fastest route between Pasir Ris and Hougang in 2003.

```bash
uv run python railrailrail/cli.py route --network-file config/network_nel.toml --coordinates-file config/station_coordinates.csv --start EW1 --end NE14

# Start at EW1 Pasir Ris
# Board train towards terminus EW27 Boon Lay
# Alight at EW13 City Hall
# Transfer to NS25 City Hall
# Board train towards terminus NS1 Jurong East
# Alight at NS24 Dhoby Ghaut
# Transfer to NE6 Dhoby Ghaut
# Board train towards terminus NE17 Punggol
# Alight at NE14 Hougang
# Total duration: 61 minutes 28 seconds
# Approximate path distance: 28.1 km, Haversine distance: 6.3 km, Circuity ratio: 4.4
```

In 2024.

```bash
uv run python railrailrail/cli.py route --network-file config/network_tel_4.toml --coordinates-file config/station_coordinates.csv --start EW1 --end NE14

# Start at EW1 Pasir Ris
# Board train towards terminus EW33 Tuas Link
# Alight at EW8 Paya Lebar
# Transfer to CC9 Paya Lebar
# Board train towards terminus CC29 HarbourFront
# Alight at CC13 Serangoon
# Transfer to NE12 Serangoon
# Board train towards terminus NE17 Punggol
# Alight at NE14 Hougang
# Total duration: 49 minutes 26 seconds
# Approximate path distance: 19.6 km, Haversine distance: 6.3 km, Circuity ratio: 3.1
```

In 2030.

```bash
uv run python railrailrail/cli.py route --network-file config/network_crl_1.toml --coordinates-file config/station_coordinates.csv --start EW1 --end NE14

# Start at EW1 Pasir Ris
# Transfer to CR5 Pasir Ris
# Board train towards terminus CR13 Bright Hill
# Alight at CR8 Hougang
# Transfer to NE14 Hougang
# Total duration: 13 minutes 41 seconds
# Approximate path distance: 7.3 km, Haversine distance: 6.3 km, Circuity ratio: 1.1
```

## Customization

The generated network config files (ending with `.toml`) and the station coordinates file (**station_coordinates.csv**) in the `config`
folder can be customized. See [CONFIG.md](docs/CONFIG.md).

## Commands

See [COMMANDS.md](docs/COMMANDS.md).

## Misc

See [MISC.md](docs/MISC.md).

## Analysis

A Jupyter notebook for analysing the route planner output is available at [analysis.ipynb](analysis/analysis.ipynb).

## License

Source code is under Apache-2.0. Most of the datasets are under the Singapore Open Data Licence version 1.0.

See [LICENSE](LICENSE) and [LICENSE-DATASET.md](LICENSE-DATASET.md).

## References

- Train Spotters from YouTube
  - [Link](docs/TRAIN_SPOTTERS.md)
- Measured interchange transfer times by a deleted user on Reddit
  - [Reddit post](https://www.reddit.com/r/singapore/comments/10wkygf/mrt_map_with_transfer_timing)
  - [Timetable](https://docs.google.com/spreadsheets/d/1e-Tuf6rHBFsgsuFN7XqbFL8ec_vdRjQw)
- TransitLink
  - [MRT/LRT Journey Information](https://www.transitlink.com.sg/eservice/eguide/rail_idx.php)
- SMRT
  - [SMRT Journey Planner](https://journey.smrt.com.sg)
- SBS Transit
  - [Travel Time](https://www.sbstransit.com.sg/travel-time)
- Singapore Train Station Coordinates
  - [GitHub Repo](https://github.com/elliotwutingfeng/singapore_train_station_coordinates)
