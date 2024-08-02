generate_config:
	poetry run python railrailrail/cli.py generate --coordinates --path config/station_coordinates.csv
	poetry run python railrailrail/cli.py generate --network all --path config

generate_config_examples:
	poetry run python railrailrail/cli.py generate --coordinates --path config_examples/station_coordinates.csv
	poetry run python railrailrail/cli.py generate --network all --path config_examples

markdown_lint:
	markdownlint --disable MD013 MD033 MD041 --fix . --ignore CODE_OF_CONDUCT.md

ruff_lint:
	poetry run ruff format
	poetry run ruff check --fix

ruff_check:
	poetry run ruff check

ruff_format_check:
	poetry run ruff format --check

install:
	poetry install

update:
	poetry lock
	poetry install

test: ruff_format_check ruff_check
	poetry run pytest -vv --cov=./ --cov-report html
