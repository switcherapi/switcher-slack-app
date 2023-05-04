# ---------- Base ----------
FROM python:3.10.11-alpine AS base

COPY requirements.txt /app/requirements.txt

# ---------- Build ----------
FROM base AS builder

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .