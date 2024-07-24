import functions_framework
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import logging


@functions_framework.cloud_event
def ex6_function(cloud_event):
    # Set up global logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    bq_client = bigquery.Client()
    dataset_id = "ex6_dataset"
    table_id = "ex6_table"
    bucket_name = cloud_event.data['bucket']
    destination_blob_name = cloud_event.data['name']
    source_uri = f'gs://{bucket_name}/{destination_blob_name}'

    check_if_dataset_exists(bq_client, dataset_id, logger)
    load_csv_from_storage_to_bigquery(bq_client, dataset_id, table_id, source_uri, logger)


def check_if_dataset_exists(bq_client, dataset_id, logger):
    try:
        bq_client.get_dataset(dataset_id)
        logger.info(f'Dataset {dataset_id} already exists') 
    except NotFound:
        logger.info(f"Dataset {dataset_id} not found")
        create_dataset(bq_client, dataset_id, logger)


def create_dataset(bq_client, dataset_id, logger):
    dataset = bigquery.Dataset(bq_client.dataset(dataset_id))
    dataset.location = "US"
    try:
        bq_client.create_dataset(dataset)
        logger.info(f'Dataset {dataset_id} created')
    except Exception as e:
        logger.error(f"Error creating dataset: {e}")


def load_csv_from_storage_to_bigquery(bq_client, dataset_id, table_id, source_uri, logger):
    try:
        table_ref = bq_client.dataset(dataset_id).table(table_id)
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            autodetect=True,
        )
        load_job = bq_client.load_table_from_uri(source_uri, table_ref, job_config=job_config)
        logger.info(f"Starting job {load_job.job_id}")
        # Waits for the job to complete
        load_job.result()  
        logger.info(f"Job {load_job.job_id} finished")

        table = bq_client.get_table(table_ref)
        logger.info(f"Loaded {table.num_rows} rows to {dataset_id}:{table_id}")
    except Exception as e:
        logger.error(f"Error loading CSV from storage to BigQuery: {e}")
