FROM python:3.9.15

ADD src /src
ADD test /test
ADD ephemerality.py /
ADD requirements.txt /
ADD _version.py /
ADD setup.py /

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "ephemerality.py"]
