FROM python:3.9.18-slim

ENV TZ="Asia/Taipei"

WORKDIR /www
COPY ./requirements.txt /www/requirements.txt

RUN pip install -r requirements.txt