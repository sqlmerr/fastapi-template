#!/bin/sh

alembic upgrade head
python -m app

uvicorn --factory app.main:create_app --host=0.0.0.0 --port=8000