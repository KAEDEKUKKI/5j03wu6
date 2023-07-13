# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /www
COPY ./www/. /www/
RUN pip install -r requirements.txt
