# ---------- Base ----------
FROM python:3.10.4-slim-bullseye AS base

LABEL COMPANY="Trackerforce"
LABEL MAINTAINER="trackerforce.project@gmail.com"
LABEL APPLICATION="Switcher Slack App"

# Upgrade all packages to latest
RUN echo 'deb http://deb.debian.org/debian bullseye-backports main' >> /etc/apt/sources.list
RUN apt-get update && apt-get -y --no-install-recommends upgrade && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

# ---------- Build ----------
FROM base AS builder

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .