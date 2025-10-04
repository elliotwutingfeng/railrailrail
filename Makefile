generate_config:
	uv run python src/railrailrail/cli.py generate --coordinates --path config/station_coordinates.csv
	uv run python src/railrailrail/cli.py generate --network all --path config

generate_config_examples:
	uv run python src/railrailrail/cli.py generate --coordinates --path config_examples/station_coordinates.csv
	uv run python src/railrailrail/cli.py generate --network all --path config_examples

markdown_lint:
	markdownlint --disable MD013 MD033 MD041 --fix . --ignore CODE_OF_CONDUCT.md

ruff_check:
	uv run ruff check
	uv run ruff format --check

ruff_format:
	uv run ruff check --fix
	uv run ruff format

install:
	uv sync --locked --all-extras --dev
	uv run pre-commit install

update:
	uv lock --upgrade
	uv sync --all-groups

test: ruff_check
	uv run pytest -vv --cov=./ --cov-report html --cov-report=lcov --cov-branch -n auto
