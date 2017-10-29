FROM python:3.6-alpine

RUN mkdir /srv/processing
WORKDIR /srv/processing

COPY ./requirements.txt /srv/processing/requirements.txt

RUN cd /srv/chatapp \
    && pip install -r requirements.txt \
    && rm requirements.txt

RUN python -c "import nltk;nltk.download('punct')"

CMD ["python", "main.py"]
EXPOSE 9000