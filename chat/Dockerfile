FROM python:3.6-alpine

RUN mkdir /srv/chatapp
WORKDIR /srv/chatapp

COPY ./requirements.txt /srv/chatapp/requirements.txt

RUN cd /srv/chatapp \
    && pip install -r requirements.txt \
    && rm requirements.txt