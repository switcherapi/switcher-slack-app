# ---------- Base ----------
FROM python:slim AS base

# Upgrade all packages to latest
RUN echo 'deb http://deb.debian.org/debian bullseye-backports main' >> /etc/apt/sources.list
RUN apt-get update && apt-get -y --no-install-recommends upgrade && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

# ---------- Build ----------
FROM base AS builder

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .