import os
from collections import defaultdict

from gcloudlogging.logger import create_logger
from gcloudlogging.errors import error_handler
from gcloudlogging.profiling import conditional_decorator
import io
from minioclient import upload_file
import pulsarclient
from fhirfastavro import avroutil
import fastavro

project_id = os.environ.get('PROJECT_ID', 'default')
INSTANCE_ID = os.environ.get("INSTANCE_ID", "instance-1")
PROFILING = os.environ.get('PROFILING', False)

profile = None
if PROFILING:
    from line_profiler import LineProfiler
    profile = LineProfiler()

fhir_ingestion_topic_name = os.environ.get("TOPIC_NAME", "fhir-ingestion-test")
fhir_ingestion_subscription_name = os.environ.get(
    "SUB_NAME", f"{fhir_ingestion_topic_name}-sub"
)

log = create_logger()

def remove_none(obj):
  if isinstance(obj, (list, tuple, set)):
    return type(obj)(remove_none(x) for x in obj if x is not None)
  elif isinstance(obj, dict):
    return type(obj)((remove_none(k), remove_none(v))
      for k, v in obj.items() if k is not None and v is not None)
  else:
    return obj


@error_handler
@conditional_decorator(profile, PROFILING)
def ingestion_callback(message):
    data, metadata = pulsarclient.callback_info(message)

    user_id = metadata['user_id']
    patient_id = metadata['patient_id']
    ingestion_time = metadata['ingestion_time']
    app = metadata['app_name']
    log.info(f'DEBUG: {type(data["Patient"][0]["id"])} {data["Patient"][0]["id"]}')
    log.info(f'Received patient data: {type(data)}')
    log.info(f'Received patient data: {data["Patient"]}')
    # bundle = {
    #     'resourceType': 'Bundle',
    #     'type': 'transaction',
    #     'entry': []
    # }
    # for entry in data:
    #     bundle['entry'].append(entry)

    # sanitize_null
    sanitized_data = defaultdict(list)
    for resourceType, resources in data.items():
        if resources:
            for resource in resources:
                # TODO: hack to remove None, till I figure how to make null pass validation in avro
                new_resource = remove_none(resource)
                sanitized_data[resourceType].append(new_resource)

    log.info(sanitized_data)

    fastavro_schema = avroutil.get_bundle_schema()
    fastavro_schema = pulsarclient.AvroSchema(schema_definition=fastavro_schema,
                                              schema_name=fastavro_schema[
                                                  'name'])

    fastavro.validate(sanitized_data, fastavro_schema)
    buffer = io.BytesIO()
    fastavro.schemaless_writer(buffer, fastavro_schema, sanitized_data)
    buffer.seek(0)

    upload_file(
        buffer,
        f"{user_id}/{patient_id}/{ingestion_time}/ingested/bundle.avro",
        app, {}
    )

    if PROFILING:
        profile.print_stats()


pulsarclient.subscribe(
    topic_name=fhir_ingestion_topic_name,
    subscription_name=fhir_ingestion_topic_name,
    callback=ingestion_callback,
    schema=pulsarclient.fastavro_schema
)