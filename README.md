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

## Requirements

- Python 3.12+
- [Python Poetry](https://python-poetry.org)

## Setup

Install dependencies and generate network configuration files.

```bash
make install
make generate_all
```

## Usage

```bash
poetry run python railrailrail/cli.py route --walk --network now --start NS14 --end TE29
poetry run python railrailrail/cli.py route --walk --network crl_2 --start CR14 --end TE31
poetry run python railrailrail/cli.py route --walk --network future --start CR14 --end CC18
```

## Future Developments

Johor Bahru-Singapore Rapid Transit System (RTS) Link

- RTS Woodlands North
- RTS Bukit Chagar

CRL Phase 3

- CR20
- CR21/JS12 Jurong Pier
- CR22
- CR23
- CR24/EW30 Gul Circle

Seletar Line

- ???

## References

- TransitLink
  - [MRT/LRT Journey Information](https://www.transitlink.com.sg/eservice/eguide/rail_idx.php)
- SMRT
  - [SMRT Journey Planner](https://journey.smrt.com.sg)
- SBS Transit
  - [Travel Time](https://www.sbstransit.com.sg/travel-time)
- Thomson-East Coast Line (TEL) Dwell times by u/xavierang2
  - [Reddit post](https://www.reddit.com/r/singapore/comments/z6i58u/some_observations_about_the_thomsoneast_coast)
  - [Timetable](https://docs.google.com/document/d/1LO1lB0jptt8UJnlUYUd3KxYqSmKoyvIauf6DNYVlb5w)
- Singapore Train Station Coordinates
  - [GitHub Repo](https://github.com/elliotwutingfeng/singapore_train_station_coordinates)
