# Configuration Guide

This document describes the config file formats used by railrailrail. By default, generated config files are saved to the `config/` folder, Contents in `config/` are gitignored. Pre-generated config files are available from the `config_examples/` folder.

There are 2 types of config files:

1) A single station coordinates file (CSV)
2) A network config file for each stage (TOML)

## Station Coordinates

[station_coordinates.csv](config_examples/station_coordinates.csv) maps stations to their latitude and longitude in decimal degrees. This includes both future and defunct stations.

## Network Config

Each network config file contains rail network [graph](https://en.wikipedia.org/wiki/Graph_theory) node and edge details for a given stage, stored in the [TOML](https://toml.io) format. For example, [network_nel.toml](config_examples/network_nel.toml) represents the rail network as of 20 June 2003, when the North East Line opened.

> [!TIP]
> For `[segments]`, `[transfers]`, and `[conditional_transfers]`, you can change any of the time durations (`duration`, `dwell_time_asc`, `dwell_time_desc`) to values in the range 0-3600 seconds inclusive.

### Schema

The current schema version is `1`. This number will be incremented if a forwards incompatible change is introduced to the network config file format.

```toml
schema = 1
```

### Stations

This section maps station codes (e.g. `BP1`) to station names (e.g. `Choa Chu Kang`).

```toml
[stations]
BP1 = "Choa Chu Kang"
BP2 = "South View"
BP3 = "Keat Hong"
...
```

### Segments

This section defines segments and their segment details. A segment is a connection between 2 stations with different names.
A segment can either be traversed by train (train segment), or by walking (walking segment).

Each segment key is formatted as `{station_code}-{another_station_code}` (2 different station codes separated by a minus sign).

A segment in the "opposite direction" should not be defined; do not add `BP2-BP1` if `BP1-BP2` is already defined.

A segment must have the following fields:

- `duration`: Travel time in seconds.
- `dwell_time_asc`: Dwell time when moving from the smaller station code
to the larger station code.
- `dwell_time_desc`: Dwell time when moving from the larger station code
to the smaller station code.

> [!NOTE]
> Dwell time is time spent in seconds waiting at station for passengers before train departure.
>
> Station codes are compared by splitting them into their line code, station number, and station number suffix (if any), and
> comparing their fields in that order.
> For example, NS3A -> ("NS", 3, "A"); string comparison for first field and third field, integer comparison for the second field.

```toml
[segments]
BP1-BP2 = {duration = 120, dwell_time_asc = 60, dwell_time_desc = 28}
BP2-BP3 = {duration = 60, dwell_time_asc = 28, dwell_time_desc = 28}
...
```

Walking segments are denoted by `mode = "walk"`. The dwell times are set to 0 as there is no need to wait for a train to depart when walking away from the station.

```toml
[segments]
...
CC2-NS25 = {duration = 420, mode = "walk", dwell_time_asc = 0, dwell_time_desc = 0}
...
```

Some segments have an **edge_type**. This is used for conditional interchange transfers. See the `[conditional transfers]` section below.

```toml
[segments]
...
CC3-CC4 = {duration = 180, edge_type = "promenade_west", dwell_time_asc = 28, dwell_time_desc = 45}
...
```

### Transfers

This section defines interchange transfers and their transfer details. An interchange transfer is a connection between
2 stations with the same name, but different station codes. Transfer details only contains the duration in seconds.

Unlike segments, transfers in both directions need to be specified (`BP1-NS4` and `NS4-BP1`). This may change in the
future.

```toml
[transfers]
BP1-NS4 = {duration = 420}
BP6-DT1 = {duration = 600}
CC1-NE6 = {duration = 480}
...
```

### Conditional Transfers

This section maps conditional interchange transfer sequences to their time duration in seconds.

A conditional interchange is a station that is positioned between different train segments of the
same line that are not directly connected to each other. For example, STC Sengkang is the
conditional interchange for the Sengkang LRT East Loop and Sengkang LRT West Loop.

A conditional interchange behaves as an interchange only when the `edge_type` of the
previous train segment and next train segment match any sequence in `conditional_transfers`.
When this happens, a conditional transfer occurs.

For example, there will be a conditional transfer when
moving from "bahar_east" to "bahar_west", but not from "bahar_west" to "bahar_east".

```toml
[conditional_transfers]
bahar_east.bahar_west = 360
bahar_south.bahar_east = 360
bahar_west.bahar_south = 360
...
```

### Non Linear Line Terminals

This section explicitly defines terminal station codes for certain line codes. This is a workaround for lines
where the terminal stations are tricky to determine lexicographically.

This includes looped lines like the Jurong Region Line and all LRT Lines, and the North South Line
before year 1989, where some East West Line stations used to be part of the North South Line.

The `1` is a placeholder for the TOML key-value format; it has no significant meaning.

```toml
[non_linear_line_terminals]
BP.BP1 = 1
BP.BP14 = 1
PE.PTC = 1
...
```

### Station Code Pseudonyms

This section maps pseudo station codes (e.g. JE0) to real station codes (e.g. JS3). Pseudo station codes
are used in lines that overlap with other lines like the Jurong Region Line East Branch (JE over JS),
and Circle Line Extension (CE over CC).

```toml
[station_code_pseudonyms]
CE0X = "CC6"
CE0Y = "CC5"
CE0Z = "CC4"
...
```
