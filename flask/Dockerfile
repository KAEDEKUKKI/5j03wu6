FROM python:3.9.17-alpine3.18
WORKDIR /www
COPY ./requirements.txt /www/requirements.txt
RUN pip install -r requirements.txt
RUN pip install wtforms