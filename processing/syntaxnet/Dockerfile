FROM tensorflow/syntaxnet

ADD . /opt/tensorflow/syntaxnet

RUN pip install -r requirements

CMD ["python", "main.py"]
EXPOSE 9999