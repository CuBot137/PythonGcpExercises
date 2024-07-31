import requests
import json
import functions_framework
import flask
import logging


@functions_framework.http
def ex9_function(request: flask.Request):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    response = vertexai_endpoint_request()
    prediction = response['predictions']
    value = prediction[0]['value']
    logger.info(f"Prediction: {str(value)}")

    return str(value)
    



def vertexai_endpoint_request():
    endpoint_url = endpoint_url = "https://us-central1-aiplatform.googleapis.com/v1beta1/projects/storage-object-trigger/locations/us-central1/endpoints/1344216736630571008:predict"
    access_token = "ya29.a0AXooCgsz9O-QXRrTVqslA7Z_MR9nkx7iDqQfwHmRQH_Q1HgVgf7LXxl29qWUDKuI4fnKdKBLhL4wAkmd2Hw-Q9kRzW5wZW5CcAK316NcIRqL7peECoy9f_aH0KB7itHL9v2lsD0SrDBjsMcyR_fAjgUAjtSHaT9ciF5E7uKTSv8aCgYKAZwSARMSFQHGX2MiQkxZaS_0xx9VJQoj4H9rEQ0178"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "instances": [
            {
                "StudentID": "1001",
                "Age" : "16",
                "Ethnicity" : "1",
                "ParentalEducation" : "2",
                "StudyTimeWeekly" : "12.721150838053616",
                "Absences" : "13",
                "Tutoring" : "0",
                "ParentalSupport" : "0",
                "Extracurricular" : "0",
                "Sports" : "0",
                "Music" : "0",
                "Volunteering" : "1",
                "GPA" : "3.57347421032976",
                "GradeClass" : "4",
            }
        ]
    }
    response = requests.post(endpoint_url, headers=headers, data=json.dumps(data))
    return response.json()