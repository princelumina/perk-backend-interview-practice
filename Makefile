.PHONY: run lint

run:
	uv run fastapi dev app/main.py

lint:
	@uv run ruff check --select I --fix
	@uv run ruff check --fix