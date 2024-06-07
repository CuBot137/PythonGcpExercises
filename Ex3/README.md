# PythonGcpExercises 3

This is a Google Cloud Function that is triggered by a PubSub message.
This function reads the PubSub message and logs it.

### Deploy Command 
gcloud functions deploy pubsub_function --gen2 --runtime python312 --trigger-topic my-topic --allow-unauthenticated --entry-point=pubsub_function