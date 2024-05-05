run-dev:
	docker compose up

run-dev-build:
	docker compose up --build

stop:
	docker compose down

test:
	docker compose exec app pytest -v -s

isort:
	poetry run isort .

format:
	poetry run ruff format .