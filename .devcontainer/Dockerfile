FROM python:3.14-alpine

#  Update pip and install dependencies and tools
RUN pip install --upgrade pip && \
    pip install pipenv && \
    apk update && \
        apk add --no-cache \
        make \
        git