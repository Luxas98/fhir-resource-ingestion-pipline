FHIR Ingestion pipeline
=======================

1. api accepting fhir resources
2. fhir to avro transformation
3. pulsar message system
4. service processing avro messages to files
5. minio storage service

## Pre requirements

see: https://cloud.google.com/community/tutorials/managing-gcp-projects-with-terraform

load variables from the tutorial into `setup-infra.sh`

TF_VAR_org_id=<YOUR-ORG-ID>
TF_VAR_billing_account=<YOUR-BILLING-ACCOUNT>

and provide terraform admin credentials into `tf-admin.json`

## Build and push

./build-api.sh <project_id>

./build-service.sh <project_id> 


## Deployment

./setup-infra.sh <project_name>

kubectl -n minio get secrets minio-secret -o json | jq -r .data.MINIO_SECRET_KEY | base64 -d

>> update ingestion-deployment.yaml and fhir-api-deployment.yaml with proper <project_id> in image section


kustomize build deployments/manifests/ | kubectl apply -f -


## Development

#### Pulsar

```bash
    pulsar-admin persistent delete persistent://public/default/fhir-ingestion --force
```