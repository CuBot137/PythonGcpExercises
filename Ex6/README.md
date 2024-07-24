# PythonGcpExercises 5
This Cloud Function is triggered by a csv file being uploaded to a Cloud Storage Bucket. When the csv is uploaded to a Cloud Storage Bucket the funciton will be triggered and write the csv to Cloud BigQuery
 
### Deploy Command 
gcloud functions deploy ex6_function --gen2 --runtime python312 --trigger-bucket gs://ex6_bucket --entry-point=ex6_function --run-service-account=ex6-358@storage-object-trigger.iam.gserviceaccount.com --memory 512MB

### Trigger 
Upload CSV to Cloud Storage via the console