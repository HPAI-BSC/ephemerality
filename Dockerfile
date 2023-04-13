FROM python:3.9.15-slim

ADD ephemerality /src
ADD testing /test
ADD rest /rest
ADD scripts/ephemerality-cmd.py /
ADD requirements.txt /
ADD _version.py /
ADD setup.py /

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "rest.api:app", "--host", "0.0.0.0", "--port", "8080"]
