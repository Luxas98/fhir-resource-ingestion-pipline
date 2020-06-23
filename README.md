FHIR Ingestion pipeline
=======================

This is an example Flask API ingesting JSON (FHIR) bundles, 
storing them in GCS using minio client, publishing message into Pulsar MQ and 
service which processes JSON (FHIR) files and transforming them into avro format.

1. api accepting fhir resources
2. fhir to avro transformation
3. minio storage service
4. pulsar message system
5. service processing avro messages to files

## Pre requirements

see: https://cloud.google.com/community/tutorials/managing-gcp-projects-with-terraform

load variables from the tutorial into `setup-infra.sh`
```bash
TF_VAR_org_id=<YOUR-ORG-ID>
TF_VAR_billing_account=<YOUR-BILLING-ACCOUNT>
```



and provide terraform admin credentials into `tf-admin.json`

## Build and push
```bash
./build-api.sh <project_id>
./build-service.sh <project_id>
```

## Deployment
```bash
./setup-infra.sh <project_name>

kubectl -n minio get secrets minio-secret -o json | jq -r .data.MINIO_SECRET_KEY | base64 -d

#update ingestion-deployment.yaml and fhir-api-deployment.yaml with proper <project_id> in image section
kustomize build deployments/manifests/ | kubectl apply -f -
```







## Development

#### Pulsar

```bash
    pulsar-admin persistent delete persistent://public/default/fhir-ingestion --force
```