import daft2bigquery

def execute_daft2bigquery(event, context):
    return daft2bigquery.ingest_pubsub(event, context)
