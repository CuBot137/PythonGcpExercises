## Problem Statement
- Stores some files in cloud storage manually
- Write code which exposes REST endpoint which accepts bucket name and object ID as query/path parameters, gets the file from GCS and returns downloadable file as response
- Create a docker image and deploy in Cloud Run
- Use service account with necessary permissions to read data from GCS

## Set up Service Account
- gcloud iam service-accounts create my-service-account --display-name "My Service Account"
- gcloud projects add-iam-policy-binding [PROJECT_ID] --member "serviceAccount:my-service-account@[PROJECT_ID].iam.gserviceaccount.com" --role "roles/storage.objectViewer"
- gcloud iam service-accounts keys create key.json --iam-account my-service-account@exercise-9-431213.iam.gserviceaccount.com


## Local API Call
- http://127.0.0.1:5000/download/ex_9_bucket/Student_performance_data%20_.csv

## Docker
- docker build -t ex10 .  
- docker run -p 8081:8081 ex10 
- docker tag ex10 gcr.io/exercise-9-431213/ex10:ex10
- docker push gcr.io/exercise-9-431213/ex10:ex10   

## Deploy Command 
gcloud run deploy my-flask-app \
  --image gcr.io/<project-id>/<app_name> \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
