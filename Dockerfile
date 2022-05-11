FROM python:3.8.6

ADD src /src
ADD test /test
ADD calculate_ephemerality.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "calculate_ephemerality.py"]
