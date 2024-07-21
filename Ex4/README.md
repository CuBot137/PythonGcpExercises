# PythonGcpExercises 4

This Cloud Function is triggered by messages from a Pub/Sub topic. It reads JSON messages from the Pub/Sub topic with the following schema:
{
  "fileName": "example.txt",
  "fileContent": "This is the content of the file."
}

Upon receiving a message, the function extracts the fileName and fileContent fields from the message and writes the content to a file in Google Cloud Storage.
 
### Deploy Command 
gcloud functions deploy bigquery_pubsub_storage_function --gen2 --runtime python312 --trigger-topic my-topic --allow-unauthenticated --entry-point=pubsub_storage_function --run-service-account=pub-sub-storage@function-project-423615.iam.gserviceaccount.com

### Trigger Command
gcloud pubsub topics publish my-topic --message '{"fileName": "This is the file name", "fileContent": "Test Data"}'