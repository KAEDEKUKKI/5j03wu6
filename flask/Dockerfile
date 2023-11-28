FROM python:3.9.17-alpine3.18

ENV TZ="Asia/Taipei"

WORKDIR /www
COPY ./requirements.txt /www/requirements.txt

RUN pip install -r requirements.txt