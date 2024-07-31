import functions_framework
from google.cloud import aiplatform
from typing import Dict
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import logging



functions_framework.http
def ex9_function(cloud_event):
    logging.basicConfig(level=logging.INFO)
    global logger 
    logger = logging.getLogger(__name__)
    logger.info(f"Cloud event: {cloud_event}")
    example_1 = {
        "StudentID": "1001",
        "Age" : "16",
        "Ethnicity" : "1",
        "ParentalEducation" : "2",
        "StudyTimeWeekly" : "12.721150838053616",
        "Absences" : "13",
        "Tutoring" : "1",
        "ParentalSupport" : "1",
        "Extracurricular" : "1",
        "Sports" : "1",
        "Music" : "1",
        "Volunteering" : "1",
        "GPA" : "3.57347421032976",
        "GradeClass" : "4",
    }

    project_id = "storage-object-trigger"
    endpoint_id = "1344216736630571008"
    location = "us-central1"
    instance_dict = example_1
    api_endpoint = "us-central1-aiplatform.googleapis.com"
    try:
        result = predict_tabular_classification_sample(project_id, endpoint_id, location, instance_dict, api_endpoint)
        return result
    except Exception as e:
        logger.error(f"Error: {e}")
    logger.info("Prediction completed")




# Code copied from https://github.com/googleapis/python-aiplatform/blob/main/samples/snippets/prediction_service/predict_tabular_classification_sample.py
# Changed print to logger.info
def predict_tabular_classification_sample(
    project: str,
    endpoint_id: str,
    instance_dict: Dict,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # for more info on the instance schema, please use get_model_sample.py
    # and look at the yaml found in instance_schema_uri
    instance = json_format.ParseDict(instance_dict, Value())
    instances = [instance]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    logger.info("response")
    logger.info(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/tabular_classification_1.0.0.yaml for the format of the predictions.
    predictions = response.predictions
    for prediction in predictions:
        logger.info(" prediction:", dict(prediction))