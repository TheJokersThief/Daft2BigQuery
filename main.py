from daft2bigquery import bigquery, daft


def execute_daft2bigquery(event, context):
    housing = daft.DaftResults(event)
    bq = bigquery.BigQuery(event)
    results = housing.get_listings_as_rows()
    bq.insert_listings(results)
