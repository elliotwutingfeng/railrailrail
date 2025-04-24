generate_config:
	uv run python railrailrail/cli.py generate --coordinates --path config/station_coordinates.csv
	uv run python railrailrail/cli.py generate --network all --path config

generate_config_examples:
	uv run python railrailrail/cli.py generate --coordinates --path config_examples/station_coordinates.csv
	uv run python railrailrail/cli.py generate --network all --path config_examples

markdown_lint:
	markdownlint --disable MD013 MD033 MD041 --fix . --ignore CODE_OF_CONDUCT.md

ruff_lint:
	uv run ruff format
	uv run ruff check --fix

ruff_check:
	uv run ruff check

ruff_format_check:
	uv run ruff format --check

install:
	uv sync --locked --all-extras --dev

update:
	uv lock --upgrade

upgrade: update install

test: ruff_format_check ruff_check
	uv run pytest -vv --cov=./ --cov-report html --cov-branch -n auto
