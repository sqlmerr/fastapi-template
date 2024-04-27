#!/bin/sh

alembic upgrade head

uvicorn --factory app.main:create_app --host=0.0.0.0 --port=8000