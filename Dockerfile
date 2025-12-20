FROM python:3.14-alpine

ENV APP_HOME=/home/app
RUN addgroup -S app \
    && adduser -S app -G app

COPY Pipfile Pipfile.lock $APP_HOME

WORKDIR $APP_HOME

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --deploy --system --ignore-pipfile && \
    pip uninstall -y pipenv

COPY /src .

RUN chown -R app:app "$APP_HOME"
USER app