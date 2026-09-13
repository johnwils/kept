.PHONY: install test lint fmt web daemon demo-reset fixtures

install:
	uv sync --extra dev
	uv run pre-commit install

test:
	uv run pytest -q

lint:
	uv run ruff check src tests
	uv run ruff format --check src tests

fmt:
	uv run ruff check --fix src tests
	uv run ruff format src tests

web:
	uv run kept web

daemon:
	uv run kept daemon

demo-reset:
	rm -rf data .kept
	mkdir -p data
	@echo "state cleared — dashboard and daemon will start empty"

fixtures:
	@echo "Run scripts/capture-fixtures.sh on the Mac that is logged into Bee."
	@echo "See docs/FIXTURES.md"
