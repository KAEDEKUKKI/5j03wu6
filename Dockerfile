# syntax=docker/dockerfile:1
FROM python:3.9.17-alpine3.18
WORKDIR /www
COPY ./www/requirements.txt /www/requirements.txt
RUN pip install -r requirements.txt
