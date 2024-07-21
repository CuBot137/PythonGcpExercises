import functions_framework
import logging
import base64
import json
from google.cloud import storage
from datetime import datetime
import os
import google.cloud.logging

# Set up credentials for local testing
credentials_path = 'Ex5/function-project-423615-c4079e58fea3.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

# Instantiates a Cloud Logging client and integrates it with the logging module
client = google.cloud.logging.Client()
client.setup_logging()

# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@functions_framework.cloud_event
def pubsub_storage_function(event):
    try:
        # Decode the Pub/Sub message
        message_data = event.data.get('message', {}).get('data', '')
        logger.info(f"Received message data: {message_data}")

        if not message_data:
            raise ValueError("No data found in the Pub/Sub message")

        message = base64.b64decode(message_data).decode('utf-8')
        logger.info(f"Decoded message: {message}")

        message_json = json.loads(message)
        logger.info(f"Message JSON: {message_json}")

        # Extract properties
        nodeName = message_json.get('nodeName')
        tempTimeStamp = message_json.get('timeStamp')
        uplink = message_json.get('uplink')
        downlink = message_json.get('downlink')  # Correct spelling here

        logger.info(f"Extracted properties - nodeName: {nodeName} ({type(nodeName)}), timeStamp: {tempTimeStamp} ({type(tempTimeStamp)}), uplink: {uplink} ({type(uplink)}), downlink: {downlink} ({type(downlink)})")

        # Validate properties
        if nodeName is None:
            raise ValueError("nodeName is None")
        if tempTimeStamp is None:
            raise ValueError("timeStamp is None")
        if uplink is None:
            raise ValueError("uplink is None")
        if downlink is None:
            raise ValueError("downlink is None")

        timeStamp = datetime.strptime(tempTimeStamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        logger.info(f"Parsed timeStamp: {timeStamp}")

        # Generate file name and file content
        file_name = f"{nodeName}-{timeStamp}.json"
        file_content = json.dumps(message_json)

        # Write the file to Google Cloud Storage
        storage_client = storage.Client()
        bucket_name = 'ex4-storage'
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(file_content)
        logger.info(f"File {file_name} uploaded to bucket {bucket_name}")

    except Exception as e:
        logger.error(f'Error processing event: {e}', exc_info=True)




# import functions_framework
# import logging
# import base64
# import json
# from google.cloud import storage
# from datetime import datetime
# import os


# # Set up credentials for local testing
# credentials_path = 'Ex5/function-project-423615-c4079e58fea3.json'
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# @functions_framework.cloud_event
# def pubsub_storage_function(event):
#     try:
#         # Decode the Pub/Sub message
#         message_data = event.data.get('message', {}).get('data', '')
#         logger.info(f"Received message data: {message_data}")

#         if not message_data:
#             raise ValueError("No data found in the Pub/Sub message")

#         message = base64.b64decode(message_data).decode('utf-8')
#         logger.info(f"Decoded message: {message}")

#         message_json = json.loads(message)
#         logger.info(f"Message JSON: {message_json}")

#         # Extract properties
#         nodeName = message_json.get('nodeName')
#         tempTimeStamp = message_json.get('timeStamp')
#         uplink = message_json.get('uplink')
#         downlink = message_json.get('downlink')  # Correct spelling here

#         logger.info(f"Extracted properties - nodeName: {nodeName} ({type(nodeName)}), timeStamp: {tempTimeStamp} ({type(tempTimeStamp)}), uplink: {uplink} ({type(uplink)}), downlink: {downlink} ({type(downlink)})")

#         # Validate properties
#         if nodeName is None:
#             raise ValueError("nodeName is None")
#         if tempTimeStamp is None:
#             raise ValueError("timeStamp is None")
#         if uplink is None:
#             raise ValueError("uplink is None")
#         if downlink is None:
#             raise ValueError("downlink is None")

#         timeStamp = datetime.strptime(tempTimeStamp, '%Y-%m-%dT%H:%M:%S.%fZ')
#         logger.info(f"Parsed timeStamp: {timeStamp}")

#         # Generate file name and file content
#         file_name = f"{nodeName}-{timeStamp}.json"
#         file_content = json.dumps(message_json)

#         # Write the file to Google Cloud Storage
#         storage_client = storage.Client()
#         bucket_name = 'ex4-storage'
#         bucket = storage_client.bucket(bucket_name)
#         blob = bucket.blob(file_name)
#         blob.upload_from_string(file_content)
#         logger.info(f"File {file_name} uploaded to bucket {bucket_name}")

#     except Exception as e:
#         logger.error(f'Error processing event: {e}', exc_info=True)
