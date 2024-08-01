# PythonGcpExercises 9

## Prerequisites
- Create a Google Cloud Account
- Create a Model on VertexAI with a training dataset
- Deploy Model to endpoint
- Enable API's: Cloud Function, Cloud Run, Cloud Build etc...

## Problem Statement
- Create a Google Cloud Function that will get a prediction back from a VertexAI Model 
- Call the function with a json data related to the model training dataset

## Solution
- Go to Model endpoint 
- Select "Sample Request" -> Python -> Follow the link [text](https://github.com/googleapis/python-aiplatform/blob/main/samples/snippets/prediction_service/predict_tabular_regression_sample.py)
- Add this function to your project
- Using Functions-Framework and Flask create a function that will take in a json payload
- Call the predict_tabular_regression_sample() function
- Return predictions

## Deploy Command
- gcloud functions deploy <function_name> --gen2 --runtime python312 --trigger-http --allow-unauthenticated --memory 512MB

## Example Result
- Predicted Values 0.3406739234924316
- Vertex AI predicts the likelyhood of a positive result.
- In my dataset we are predicting the gender
- 0 = male
- 1 = female
- The result is the probability of the student being female, positive result