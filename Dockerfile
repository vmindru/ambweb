FROM python:3.7-alpine

RUN apk add gcc musl-dev mariadb-dev mariadb-client

RUN pip install --upgrade pip

WORKDIR /code
COPY requirements.ini ./
RUN pip install -r ./requirements.ini
RUN mkdir /var/log/AMB
