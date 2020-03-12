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
        },
        {
            "resource": {
                "resourceType": "Observation",
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8480-6"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/5a7dc54cf2f5f10100361927"
                },
                "effectiveDateTime": "2010-09-12T12:16:17+00:00",
                "valueQuantity": {
                    "value": 120,
                    "system": "http://unitsofmeasure.org",
                    "code": "mm[Hg]"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8893-0"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/5a7dc54cf2f5f10100361927"
                },
                "effectiveDateTime": "2010-09-12T12:16:17+00:00",
                "valueQuantity": {
                    "value": 61,
                    "system": "http://unitsofmeasure.org",
                    "code": "/min"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "59408-5"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/5a7dc54cf2f5f10100361927"
                },
                "effectiveDateTime": "2010-09-12T12:16:17+00:00",
                "valueQuantity": {
                    "value": 96,
                    "system": "http://unitsofmeasure.org",
                    "code": "%"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "9279-1"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/5a7dc54cf2f5f10100361927"
                },
                "effectiveDateTime": "2010-09-12T12:16:17+00:00",
                "valueQuantity": {
                    "value": 18,
                    "system": "http://unitsofmeasure.org",
                    "code": "/min"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8302-2"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/5a7dc54cf2f5f10100361927"
                },
                "effectiveDateTime": "2010-09-12T12:16:17+00:00",
                "valueQuantity": {
                    "value": 175,
                    "system": "http://unitsofmeasure.org",
                    "code": "cm"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "29463-7"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/5a7dc54cf2f5f10100361927"
                },
                "effectiveDateTime": "2010-09-12T12:16:17+00:00",
                "valueQuantity": {
                    "value": 76,
                    "system": "http://unitsofmeasure.org",
                    "code": "kg"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8480-6"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/5a7dc54cf2f5f10100361927"
                },
                "effectiveDateTime": "2010-09-12T12:16:17+00:00",
                "valueQuantity": {
                    "value": 120,
                    "system": "http://unitsofmeasure.org",
                    "code": "mm[Hg]"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8462-4"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/5a7dc54cf2f5f10100361927"
                },
                "effectiveDateTime": "2010-09-12T12:16:17+00:00",
                "valueQuantity": {
                    "value": 80,
                    "system": "http://unitsofmeasure.org",
                    "code": "mm[Hg]"
                }
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "status": "final",
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "35088-4"
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/5a7dc54cf2f5f10100361927"
                },
                "effectiveDateTime": "2010-09-12T12:16:17+00:00",
                "valueQuantity": {
                    "value": 1,
                    "system": "http://unitsofmeasure.org",
                    "code": "{score}"
                }
            }
        }
    ]
}
'
