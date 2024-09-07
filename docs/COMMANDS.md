# Commands

## route

Use `route` to get the fastest route between 2 stations.

Four arguments are required:

- `--start`: Origin station code. Example: **NS14**.
- `--end`: Destination station code. Example: **TE29**.
- `--coordinates-file`: Path to CSV file with location coordinates for every station. Example: [station_coordinates.csv](/config_examples/station_coordinates.csv)
- `--network-file`: Path to network config file with rail network [graph](https://en.wikipedia.org/wiki/Graph_theory) node and edge details. Example: [network_tel_4.toml](/config_examples/network_tel_4.toml)

```bash
poetry run python railrailrail/cli.py route --coordinates-file config/station_coordinates.csv --network-file config/network_tel_4.toml  --start NS14 --end TE29

# Start at NS14 Khatib
# Board train towards terminus NS28 Marina South Pier
# Alight at NS22 Orchard
# Transfer to TE14 Orchard
# Board train towards terminus TE29 Bayshore
# Alight at TE29 Bayshore
# Total duration: 62 minutes 11 seconds
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
# Total duration: 33 minutes 39 seconds
# Approximate path distance: 15.6 km, Haversine distance: 10.0 km, Circuity ratio: 1.6
```

### Past and future networks

Use a different `--network-file` to calculate fastest routes for both past and future versions of the network.

**Example:** EW1 Pasir Ris to NS16 Ang Mo Kio

EW1 Pasir Ris opened (1989).

```bash
poetry run python railrailrail/cli.py route --network-file config/network_phase_2a_2.toml --coordinates-file config/station_coordinates.csv --start EW1 --end NS16

# Start at EW1 Pasir Ris
# Board train towards terminus EW26 Lakeside
# Alight at EW13 City Hall
# Transfer to NS25 City Hall
# Board train towards terminus NS13 Yishun
# Alight at NS16 Ang Mo Kio
# Total duration: 53 minutes 37 seconds
# Approximate path distance: 27.7 km, Haversine distance: 11.1 km, Circuity ratio: 2.5
```

Cross Island Line 2 opened (est. 2032).

```bash
poetry run python railrailrail/cli.py route --network-file config/network_crl_2.toml --coordinates-file config/station_coordinates.csv --start EW1 --end NS16

# Start at EW1 Pasir Ris
# Transfer to CR5 Pasir Ris
# Board train towards terminus CR19 Jurong Lake District
# Alight at CR11 Ang Mo Kio
# Transfer to NS16 Ang Mo Kio
# Total duration: 25 minutes 22 seconds
# Approximate path distance: 11.8 km, Haversine distance: 11.1 km, Circuity ratio: 1.1
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
