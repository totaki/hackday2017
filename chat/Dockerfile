FROM python:3.6-alpine

RUN mkdir /srv/chatapp
WORKDIR /srv/chatapp

COPY ./requirements.txt /srv/chatapp/requirements.txt
COPY . /srv/chatapp

RUN cd /srv/chatapp \
    && pip install -r requirements.txt \
    && rm requirements.txt \
    && python -m compileall -b . \
    && find . -name "*.py" -type f -print0 | xargs -0 /bin/rm -f

CMD ["python3", "main.pyc"]