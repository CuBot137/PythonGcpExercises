from typing import Dict

from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import functions_framework
import flask
import logging 


@functions_framework.http
def ex9_function(request: flask.Request):
    logging.basicConfig(level=logging.INFO)
    global logger
    logger = logging.getLogger(__name__)

    try:
        # get_json() turns json payload into a dictionary
        request_json = request.get_json()
    except Exception as e:
        logger.error(f"Error loading JSON from request: {e}")
        return "Error loading JSON from request", 500

    instance_data = request_json.get('instance_data')
    if not instance_data:
        return "missing instance data in request", 400

    values_list = predict_tabular_regression_sample("storage-object-trigger","1344216736630571008", instance_data, "us-central1", "us-central1-aiplatform.googleapis.com")
    values_string = ', '.join(str(i) for i in values_list)
    logger.info(f"Predicted Values: {values_string}")
    return f"Predicted Values {values_string}"


def predict_tabular_regression_sample(
    project: str,
    endpoint_id: str,
    instance_dict: Dict,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    try:
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
        logger.info(f"Deployed_model_id:{response.deployed_model_id}")
        # See gs://google-cloud-aiplatform/schema/predict/prediction/tabular_regression_1.0.0.yaml for the format of the predictions.
        predictions = response.predictions
        values = []
        for prediction in predictions:
            prediction_dict = dict(prediction)
            value = prediction_dict.get('value','N/A')
            values.append(value)
        return values

    except Exception as e:
        logger.info(f"Prediction request to AI Platform failed: {e}")