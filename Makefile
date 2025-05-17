.PHONY: install format lint

install:
	poetry install --sync

format:
	poetry run ruff check --fix-only .
	poetry run ruff format .

lint:
	poetry run ruff check .
	poetry run ruff format --diff .
	poetry run mypy .
