import base64
import json

from daft2bigquery import bigquery, daft


def ingest_pubsub(event, context):
    if '@type' in event and event['@type'] == 'type.googleapis.com/google.pubsub.v1.PubsubMessage':
        data = str(base64.b64decode(event['data']), 'utf-8')
        event = json.loads(data)

    housing = daft.DaftResults(event)
    bq = bigquery.BigQuery(event)
    results = housing.get_listings_as_rows()
    results = filter(lambda x: x is not None, results)
    bq.insert_listings(results)
