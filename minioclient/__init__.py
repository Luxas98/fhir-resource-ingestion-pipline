import os
import io
from minio import Minio
from minio.error import (ResponseError, NoSuchBucket)
from gcloudlogging.logger import create_logger

minio_host = os.environ.get('MINIO_HOST')
minion_access_key = os.environ.get('MINIO_ACCESS_KEY', "minioadmin")
minion_secret_key = os.environ.get('MINIO_SECRET_KEY', "minioadmin")

DEBUG = os.environ.get('DEBUG', False)
log = create_logger()


def _get_storage_client():
    if hasattr(_get_storage_client, 'client'):
        return _get_storage_client.client

    _get_storage_client.client = Minio(minio_host, access_key=minion_access_key,
                                       secret_key=minion_secret_key,
                                       secure=False, region='europe-west4')
    return _get_storage_client.client


def _getio_length(stream):
    pos = stream.tell()
    stream.seek(0, os.SEEK_END)
    length = stream.tell()
    stream.seek(pos)
    return length


def _bytesiocovert(stream):
    return io.BytesIO(stream.read().encode('utf-8'))


def upload_file(file_stream, filename, app_name, metadata, compress=False):
    log.info(f'Uploading file {filename} to {app_name}',
             extra={'_filename': filename, 'app': app_name})

    client = _get_storage_client()
    file_stream = _bytesiocovert(file_stream)
    stream_length = _getio_length(file_stream)
    result = ""
    try:
        exists = client.bucket_exists(app_name)
        if not exists:
            client.make_bucket(app_name, 'europe-west4')

        result = client.put_object(app_name, filename, file_stream,
                                   stream_length,
                                   content_type="application/octet-stream",
                                   metadata=metadata)
    except ResponseError as e:
        log.error(e, extra={'_filename': filename, 'app': app_name})
        # TODO: notify user that upload failed
        # Reraise the error for now
        raise e

    return result


def list_all_files(user_id, folder, app_name):
    client = _get_storage_client()

    prefix = os.path.join(*[str(user_id), folder])
    try:
        return client.list_objects(app_name, prefix=prefix)
    except NoSuchBucket as e:
        log.warning(e, extra={'app': app_name, '_filename': folder, 'user': user_id})
        return []


def list_files(user_id, folder, app_name):
    try:
        return [f.object_name.encode('utf-8') for f in
            list_all_files(user_id, folder, app_name)]
    except NoSuchBucket as e:
        log.warning(e, extra={'user': user_id, 'app': app_name, '_filename': folder})
        return []


def get_file(filename, app_name):
    client = _get_storage_client()
    try:
        return client.get_object(app_name, filename).data  # TODO: .stream() -> maybe more efficient if we pass streams around?
    except NoSuchBucket as e:
        log.warning(e, extra={'app': app_name, '_filename': filename})
        return ""
