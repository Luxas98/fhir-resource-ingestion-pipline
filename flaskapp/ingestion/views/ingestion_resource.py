import json
import os
from collections import defaultdict
from time import time
from uuid import uuid4
from flask.views import MethodView
from flask import request, jsonify
from flaskapp.extensions.api import api
from flaskapp.ingestion.views.blueprint import ingestion
from flaskapp.logger import logger as log
from apimessages.status import ResponseGenerator
import pulsarclient
from minioclient import list_files, get_file

from time import sleep

project_id = os.environ.get('PROJECT_ID', 'default')
app_name = f"{project_id}-fhir-data"

service_name = 'fhir-api'  # TODO: from env or kubectl?
fhir_ingestion_topic_name = os.environ.get("TOPIC_NAME", "fhir-ingestion-test")

publisher = pulsarclient.publisher(
    fhir_ingestion_topic_name, schema=pulsarclient.fastavro_schema
)


class FHIRPredictAPI(MethodView):
    def post(self, _version):
        ingestion_id = request.args.get('ingestion_id', str(uuid4()))
        user_id = request.args.get('user')

        responses = ResponseGenerator(app_name, user_id, "", service_name, "")

        if not user_id:
            return jsonify(responses.missing_parameter('user'))

        fhir_data_bundles = request.get_data()
        if not fhir_data_bundles:
            return jsonify(responses.missing_parameter('body'))

        try:
            fhir_data_bundles = json.loads(fhir_data_bundles)
            if not fhir_data_bundles:
                jsonify(responses.missing_parameter("body"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            log.error(f"Failed to parse data: {fhir_data_bundles} {e}")
            return jsonify(
                responses.error(
                    f"Could not decode JSON body, invalid JSON structure, received data structure: {fhir_data_bundles}"
                )
            )
        log.info('Data received')
        ingestion_time = int(time())
        patient_id = ""
        if isinstance(fhir_data_bundles, list):
            for bundle in fhir_data_bundles:
                patient_id = self._process_bundle(
                    user_id, ingestion_id, ingestion_time, bundle
                )

        if isinstance(fhir_data_bundles, dict):
            patient_id = self._process_bundle(
                user_id, ingestion_id, ingestion_time, fhir_data_bundles
            )

        ingestion_status = self._are_data_ingested(app_name, user_id,
                                                   ingestion_id, ingestion_time,
                                                   patient_id
                                                   )
        counter = 0
        while not ingestion_status.get("data") or counter < 10:
            sleep(0.2)
            log.info('Waiting for data in GCS')
            ingestion_status = self._are_data_ingested(
                app_name, user_id, ingestion_id, ingestion_time, patient_id
            )
            counter += 1

        log.info(f"Ingestion {ingestion_status}")
        return jsonify(ingestion_status)

    def _process_bundle(self, user_id, ingestion_id, ingestion_time, bundle):
        if 'entry' not in bundle:
            return 'Missing "entry" value in bundle'

        if len(bundle['entry']) == 0:
            return 'Empty "entry" value in bundle'

        fhir_data = (entry['resource'] for entry in bundle['entry'])
        patient_id = None
        fhir_bundle = defaultdict(list)

        try:
            for resource_data in fhir_data:
                if 'resourceType' not in resource_data:
                    return 'Missing "resourceType" in bundle entry'

                if not patient_id:
                    patient_id = self._get_patient_id(resource_data)

                resource_type = resource_data['resourceType']
                fhir_bundle[resource_type].append(resource_data)
        except KeyError:
            # fhir_data is generator so the error is raised on call not on assigment
            return 'Missing "resource" value in bundle entry'

        log.info(
            f'Publishing patient for ingestion: ${fhir_bundle}',
            extra={
                "patient_id": patient_id,
                "ingestion_id": ingestion_id,
                "ingestion_time": ingestion_time,
                "user_id": user_id
            }
        )

        pulsarclient.publish(
            publisher,
            fhir_bundle,
            meta={
                "patient_id": f"{patient_id}",
                "ingestion_id": f"{ingestion_id}",
                "ingestion_time": f"{ingestion_time}",
                "user_id": f"{user_id}",
                "app_name": f"{app_name}"
            }
        )

        return patient_id

    def _get_patient_id(self, resource):
        resource_type = resource['resourceType']
        if resource_type == 'Patient':
            try:
                id = resource['id']
                return id
            except KeyError:
                pass

            try:
                id = [
                    identifier['value'] for identifier in resource['identifier']
                    if identifier['use'] == 'usual'
                ][-1]
                return id
            except KeyError:
                pass

        # { "subject" : { "reference": "Patient/123" }
        # { "subject" : { "refernece": "urn:uuid:75f4051c-91aa-4101-abdc-d0eb10c0f446"}
        try:
            return resource['patient'].split('/')[-1]
        except KeyError:
            pass

        try:
            return resource['patient'].split(':')[-1]
        except KeyError:
            pass

        try:
            return resource['subject']['reference'].split('/')[-1]
        except KeyError:
            pass

        try:
            return resource['subject']['reference'].split(':')[-1]
        except KeyError:
            pass

        log.warning('No patient id found, generating new one: {id}')
        return str(uuid4())

    def _are_data_ingested(
            self, app_name, user_id, ingestion_id, ingestion_time, patient_id
    ):
        data = {}
        ingested_files = list_files(
            user_id, f'{patient_id}/{ingestion_time}/ingested/', app_name
        )

        for pfile in ingested_files:
            data[patient_id] = json.loads(get_file(pfile, app_name))

        return {
            'id': ingestion_id,
            'user': user_id,
            'data': data,
            # 'status': current_statuses
        }


ingestion_view = FHIRPredictAPI.as_view('ingestion')

api.add_url_rule(
    ingestion.url_prefix,
    view_func=ingestion_view,
    methods=['POST'],
)

api.add_url_rule(
    ingestion.url_prefix + '/',
    view_func=ingestion_view,
    methods=['POST'],
)
