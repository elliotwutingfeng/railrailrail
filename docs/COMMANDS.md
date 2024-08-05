# Commands

## route

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

### Walking routes

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

### Past and future networks

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

## generate

> [!TIP]
> You do not need to do this if you already ran `make generate_config`.

Use `generate` to generate the station coordinates file and network config files for the route planner.

### Station Coordinates File

Generate a station `--coordinates` file (**station_coordinates.csv**).

```bash
poetry run python railrailrail/cli.py generate --coordinates
```

### Network Config File

Generate a `--network` config file with preset time durations for a given stage (e.g. `sklrt_east_loop`, `ccl_3`)

Run `generate --help` to get all possible options for `--network`.

```bash
poetry run python railrailrail/cli.py generate --help
poetry run python railrailrail/cli.py generate --network sklrt_east_loop
```
