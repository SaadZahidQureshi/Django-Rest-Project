FROM python:3.10-slim

RUN apt-get update && apt-get install -y build-essential gcc gdal-bin libgdal-dev postgresql-client libpq-dev

ENV PYTHONDONOTWRITEBYTECODE = 1
ENV PYTHONUNBUFFERED = 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/