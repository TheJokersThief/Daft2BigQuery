from google.cloud import bigquery


class BigQuery():
    def __init__(self, event):
        self.table_id = event['bq_table_id']
        self.client = bigquery.Client()

    def insert_listings(self, listings):
        errors = self.client.insert_rows_json(
            self.table_id, listings
        )
        if errors == []:
            print("New rows have been added.")
        else:
            print("Encountered errors while inserting rows: {}".format(errors))
            raise Exception(errors)
        