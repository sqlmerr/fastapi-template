run-dev:
	docker compose up

run-dev-build:
	docker compose up --build

stop:
	docker compose down

test:
	pytest -v -s

isort:
	poetry run isort .

format:
	poetry run ruff format .