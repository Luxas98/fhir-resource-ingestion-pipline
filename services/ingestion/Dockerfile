FROM python:3.6-stretch
RUN apt-get update
RUN pip install --upgrade pip

WORKDIR /app
COPY pulsarclient pulsarclient
COPY gcloudlogging gcloudlogging
COPY minioclient minioclient
COPY services/ingestion/requirements.txt requirements.txt
COPY services/ingestion/src/ingestion.py ingestion.py
COPY fhirfastavro fhirfastavro
COPY fhirfastavro/schema schema

RUN pip install -r requirements.txt

RUN mkdir -p /etc/secrets
COPY deployments/terraform/credentials.json /etc/secrets/gcs-secret.json

# use -u so the stdout is sent to docker logs
CMD ["python", "-u", "ingestion.py"]
#CMD [ "while true; do sleep 30; done;;" ]