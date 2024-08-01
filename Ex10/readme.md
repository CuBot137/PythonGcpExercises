## Set up Service Account
- gcloud iam service-accounts create my-service-account --display-name "My Service Account"
- gcloud projects add-iam-policy-binding [PROJECT_ID] --member "serviceAccount:my-service-account@[PROJECT_ID].iam.gserviceaccount.com" --role "roles/storage.objectViewer"
- gcloud iam service-accounts keys create key.json --iam-account my-service-account@exercise-9-431213.iam.gserviceaccount.com


## API Call
- http://127.0.0.1:5000/download/ex_9_bucket/Student_performance_data%20_.csv

