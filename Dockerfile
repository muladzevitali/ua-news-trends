FROM python:3.9-slim

ENV DJANGO_SETTINGS_MODULE="config.settings"
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl libpq-dev --no-install-recommends
RUN useradd --create-home ua_app
RUN chown ua_app:ua_app -R  /tmp /app

USER ua_app

COPY --chown=ua_app:ua_app app/requirements.txt /app

ENV PYTHONUNBUFFERED="${PYTHONUNBUFFERED}" \
    PYTHONPATH="." \
    PATH="${PATH}:/home/ua_app/.local/bin" \
    USER="ua_app"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY --chown=ua_app:ua_app app /app
COPY --chown=ua_app:ua_app .env /app/.env
COPY --chown=ua_app:ua_app app-entrypoint.sh /
COPY --chown=ua_app:ua_app celery-entrypoint.sh /

RUN chmod u+x /app-entrypoint.sh
RUN chmod u+x /celery-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]