# PythonGcpExercises 2

This is a Google Cloud Function that is triggered every minute by Google Cloud Scheduler
When the function is called, the current time is logged

### Test Function Locally
cd into Ex2
functions-framework --target cronFunction

### Deploy Command
gcloud functions deploy cronFucntion --gen2 --runtime=python312 --entry-point=cronFunction --trigger-http --allow-unauthenticated