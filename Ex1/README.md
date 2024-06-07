# PythonGcpExercises 1

This is a Google Cloud Function that is triggered by HTTP requests.
GET, POST, DELETE are handled. Other requests will trigger a 'Unknown method', 405 response

### Test Function Locally
cd into Ex1
functions-framework --target http_handler

### Deploy Command
gcloud functions deploy http_handler --gen2 --runtime python310 --trigger-http --allow-unauthenticated