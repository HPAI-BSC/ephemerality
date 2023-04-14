FROM python:3.9.15-slim
ARG test=false

ADD ephemerality /ephemerality
ADD ephemerality.egg-info /ephemerality.egg-info
ADD rest /rest
ADD scripts /scripts
ADD testing /testing
ADD _version.py /
ADD README.md /
ADD setup.py /

RUN if [ $test = true ] ; then pip install --no-cache-dir --upgrade -e .[test] ; else pip install --no-cache-dir --upgrade .; fi

ENTRYPOINT ["uvicorn", "scripts.ephemerality-api:app", "--host", "0.0.0.0", "--port", "8080"]
