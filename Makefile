generate_all:
	poetry run python railrailrail/cli.py generate --coordinates
	poetry run python railrailrail/cli.py generate --network all

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
	poetry lock
	poetry install

test: ruff_format_check ruff_check
	poetry run pytest -vv --cov=./ --cov-report html
