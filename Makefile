run-dev:
	poetry run uvicorn --factory app.main:create_app --reload

test:
	poetry run pytest -v -s

isort:
	poetry run isort .