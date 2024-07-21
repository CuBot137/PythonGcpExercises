# PythonGcpExercises 5

This Cloud Function is triggered by messages from a Pub/Sub topic. It reads JSON messages from the Pub/Sub topic with the following schema:
'{"nodeName": "exampleNode","timestamp": "2024-07-21T14:19:28.166194Z","uplink": 123.45,"downlink": 678.90}'

Upon receiving a message, the function extracts the nodeName, timestamp, uplink and downlink fields from the message and writes the content to a file in Google Cloud Storage.
 
### Deploy Command 
gcloud functions deploy ex5_function --gen2 --runtime python312 --trigger-topic my-topic --allow-unauthenticated --entry-point=ex5_function --run-service-account=vmo2-bigquery@festive-idea-426808-e6.iam.gserviceaccount.com --memory 512MB

### Trigger Command
gcloud pubsub topics publish my-topic --message '{"nodeName": "exampleNode","timestamp": "2024-07-21T14:19:28.166194Z","uplink": 123.45,"downlink": 678.90}'