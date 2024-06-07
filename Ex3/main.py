import base64
import functions_framework
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@functions_framework.cloud_event
def pubsub_function(cloud_event):
    message = base64.b64decode(cloud_event.data.get('message', {}).get('data', '')).decode('utf-8')
    event_id = cloud_event['id']
    event_type = cloud_event['type']

    print(f'New Event: id ={event_id}, event_type ={event_type}')
    print(f'Data = {message}')
    logger.info(message)
