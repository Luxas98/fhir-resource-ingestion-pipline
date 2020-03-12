#!/usr/bin/env bash
PROJECT_ID=${PROJECT_ID=$1}
docker build -t eu.gcr.io/${PROJECT_ID}/ingestion-api -f flaskapp/Dockerfile .
docker push eu.gcr.io/${PROJECT_ID}/ingestion-api