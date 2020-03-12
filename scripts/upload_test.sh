#!/usr/bin/env bash
curl -X POST \
  http://localhost:5001/api/v1/fhir/ingest?user=my-user \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
    "resourceType": "Bundle",
    "type": "transaction",
    "entry": [
        {
            "resource": {
                "resourceType": "Patient",
                "identifier": [
                    {
                        "use": "usual",
                        "type": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": "76435-7"
                                }
                            ]
                        },
                        "value": "5a7dc54cf2f5f10100361927"
                    }
                ],
                "gender": "male",
                "birthDate": "1980-01-01",
                "managingOrganization": {
                    "reference": "Organization/Healthy"
                }
            }
        }
    ]
}
'