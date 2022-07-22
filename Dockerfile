FROM python:3.11.0b3-slim

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .