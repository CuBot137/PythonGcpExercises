import functions_framework
import logging
import json
from google.cloud import storage, bigquery
from google.cloud.exceptions import NotFound
import base64

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@functions_framework.cloud_event
def ex5_function(cloud_event):
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)    

    message_data = cloud_event.data.get('message', {}).get('data', '')
    logger.info(f"Received message data: {message_data}")

    if not message_data:
        logger.error("No data found in the Pub/Sub message")
        return

    try:
        message = base64.b64decode(message_data).decode('utf-8')
        logger.info(f"Decoded message: {message}")

        message_json = json.loads(message)
        logger.info(f"Message JSON: {message_json}")
    except (base64.binascii.Error, UnicodeDecodeError) as e:
        logger.error(f"Error decoding message data: {e}")
        return
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON: {e}")
        return

    node_name = message_json.get('nodeName')
    timestamp = message_json.get('timestamp')
    uplink = message_json.get('uplink')
    downlink = message_json.get('downlink')

    if None in [node_name, timestamp, uplink, downlink]:
        logger.error(f'Missing one or more required keys in the message data.\nnodeName: {node_name}, timestamp: {timestamp}, uplink: {uplink}, downlink: {downlink}')
        return

    bq_client = bigquery.Client()
    storage_client = storage.Client()

    bucket_name = 'ex5_bucket'
    dataset_id = 'ex5_dataset'
    table_id = 'ex5_table'
    destination_blob_name = f'{node_name}-{timestamp}.json'

    # Create the bucket if it doesn't exist
    check_if_bucket_exists(storage_client, bucket_name)
    json_file = create_json_file(message_json, node_name, timestamp)
    upload_to_gcs(storage_client, json_file, bucket_name, destination_blob_name)

    # Create the dataset and table if they don't exist
    check_if_dataset_exists(bq_client, dataset_id)
    check_if_table_exists(bq_client, dataset_id, table_id)

    # Load data into BigQuery
    filtered_data = filter_data(message_json)
    load_data_to_bigquery(bq_client, dataset_id, table_id, filtered_data)

def check_if_bucket_exists(storage_client, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        logger.info(f'Bucket {bucket_name} already exists.')
    except NotFound:
        bucket = storage_client.create_bucket(bucket_name)
        logger.info(f'Bucket {bucket_name} created.')

def create_json_file(data, node_name, timestamp):
    file_name = f'{node_name}-{timestamp}.json'
    with open(file_name, 'w') as f:
        json.dump(data, f)
    return file_name

def upload_to_gcs(storage_client, file, bucket_name, destination_blob_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(file)
        logger.info(f'File {file} uploaded to {bucket_name} as {destination_blob_name}.')
    except Exception as e:
        logger.error(f"An unexpected error occurred while uploading to GCS: {e}")

def check_if_dataset_exists(bq_client, dataset_id):
    try:
        dataset_ref = bigquery.DatasetReference(bq_client.project, dataset_id)
        bq_client.get_dataset(dataset_ref)
        logger.info(f'Dataset {dataset_id} already exists.')
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = 'US'
        bq_client.create_dataset(dataset, exists_ok=True)
        logger.info(f'Dataset {dataset_id} created.')

def check_if_table_exists(bq_client, dataset_id, table_id):
    table_ref = bq_client.dataset(dataset_id).table(table_id)
    try:
        bq_client.get_table(table_ref)
        logger.info(f'Table {table_id} already exists.')
    except NotFound:
        schema = [
            bigquery.SchemaField("nodeName", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("uplink", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("downlink", "FLOAT", mode="REQUIRED")
        ]
        table = bigquery.Table(table_ref, schema=schema)
        bq_client.create_table(table)
        logger.info(f'Table {table_id} created.')

def filter_data(data):
    # Only include the fields that are defined in the BigQuery schema
    allowed_fields = {"nodeName", "timestamp", "uplink", "downlink"}
    return {key: data[key] for key in allowed_fields if key in data}

def load_data_to_bigquery(bq_client, dataset_id, table_id, data):
    try:
        table_ref = bq_client.dataset(dataset_id).table(table_id)
        rows_to_insert = [data]
        errors = bq_client.insert_rows_json(table_ref, rows_to_insert)
        if errors:
            logger.error(f"Errors occurred while inserting rows: {errors}")
        else:
            logger.info(f"Data inserted into {dataset_id}.{table_id} successfully.")
    except Exception as e:
        logger.error(f"An unexpected error occurred while inserting rows: {e}")
