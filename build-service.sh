#!/usr/bin/env bash
PROJECT_ID=${PROJECT_ID=$1}
docker build -t eu.gcr.io/${PROJECT_ID}/ingestion-service -f services/ingestion/Dockerfile .
docker push eu.gcr.io/${PROJECT_ID}/ingestion-service