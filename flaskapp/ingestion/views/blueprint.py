from flask import Blueprint

ingestion = Blueprint('ingestion', __name__, url_prefix='/ingest')
