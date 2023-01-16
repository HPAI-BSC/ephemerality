FROM python:3.9.15-slim

ADD src /src
ADD test /test
ADD rest /rest
ADD ephemerality.py /
ADD requirements.txt /
ADD _version.py /
ADD setup.py /

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "rest.api:app", "--host", "0.0.0.0", "--port", "8080"]
