FROM python:3.13-alpine

ENV APP_HOME=/home/app
RUN addgroup -S app \
    && adduser -S app -G app

COPY requirements.txt $APP_HOME

WORKDIR $APP_HOME

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY /src .

RUN chown -R app:app "$APP_HOME"
USER app