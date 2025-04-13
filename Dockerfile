FROM python:3.11-alpine3.18

ENV PYTHONUNBUFFERED=1

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    python3-dev \
    build-base

RUN python3 -m ensurepip && pip3 install --upgrade pip setuptools wheel

WORKDIR /opt/backend

COPY ./requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

RUN apk del gcc musl-dev libffi-dev python3-dev build-base

COPY hash_fixture_passwords.py /opt/backend/

COPY ./docker-entrypoint.sh /usr/local/bin/entrypoint
RUN ["chmod", "+x", "/usr/local/bin/entrypoint"]

EXPOSE 8000

ENTRYPOINT /usr/local/bin/entrypoint
