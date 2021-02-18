from daft2bigquery import ingest_pubsub

def execute_daft2bigquery(event, context):
    return ingest_pubsub(event, context)
