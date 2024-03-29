FROM python:3.11-slim

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN alembic upgrade head

CMD uvicorn --factory app.main:create_app --host=0.0.0.0 --port=8000