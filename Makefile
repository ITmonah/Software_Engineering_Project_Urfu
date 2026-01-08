lint:
	ruff check .
	black --check .

format:
	black .
	ruff check . --fix
