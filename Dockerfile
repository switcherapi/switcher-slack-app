FROM python:3.10.4-slim-bullseye

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .