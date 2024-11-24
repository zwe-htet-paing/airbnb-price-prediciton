import os
import json
import boto3
import base64

import mlflow

def get_model_location(run_id):
    model_location = os.getenv('MODEL_LOCATION')

    if model_location is not None:
        return model_location

    model_bucket = os.getenv('MODEL_BUCKET', 'mlflow-models-alexey')
    experiment_id = os.getenv('MLFLOW_EXPERIMENT_ID', '1')

    model_location = f's3://{model_bucket}/{experiment_id}/{run_id}/artifacts/model'
    return model_location

def load_model(run_id):
    # model_path = get_model_location(run_id)
    model_path = f'runs:/{run_id}/model'
    model = mlflow.pyfunc.load_model(model_path)
    return model


def base64_decode(encoded_data):
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    airbnb_event = json.loads(decoded_data)
    return airbnb_event

class ModelService:
    def __init__(self, model, model_version=None, callbacks=None):
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []

    def prepare_features(self,input_data):
        features = {}
        features['room_type'] = input_data['room_type']
        features['neighbourhood'] = input_data['neighbourhood']
        features['latitude'] = input_data['latitude']
        features['longitude'] = input_data['longitude']
        features['minimum_nights'] = input_data['minimum_nights']
        features['number_of_reviews'] = input_data['number_of_reviews']
        features['reviews_per_month'] = input_data['reviews_per_month']
        features['availability_365'] = input_data['availability_365']

        return features

    def predict(self, features):
        pred = self.model.predict(features)
        return float(pred[0])

    
    def lambda_handler(self, event):
    
        # print(json.dumps(event))
        predictions_events = []
        for record in event['Records']:
            encoded_data = record['kinesis']['data']
            airbnb_event = base64_decode(encoded_data)

            input_data = airbnb_event['input_data']
            input_id = airbnb_event['input_id']

            features = self.prepare_features(input_data)
            prediction = self.predict(features)

            prediction_event = {
                'model': 'price_prediction_model',
                'version': self.model_version,
                'prediction': {
                    'price': prediction,
                    'input_id': input_id
                }
            }
            
            for callback in self.callbacks:
                callback(prediction_event)

            predictions_events.append(prediction_event)

        return {
            'predictions': predictions_events
        }
        

class KinesisCallback:
    def __init__(self, kinesis_client, prediction_stream_name):
        self.kinesis_client = kinesis_client
        self.prediction_stream_name = prediction_stream_name

    def put_record(self, prediction_event):
        input_id = prediction_event['prediction']['input_id']

        self.kinesis_client.put_record(
            StreamName=self.prediction_stream_name,
            Data=json.dumps(prediction_event),
            PartitionKey=str(input_id),
        )

def create_kinesis_client():
    endpoint_url = os.getenv('KINESIS_ENDPOINT_URL')

    if endpoint_url is None:
        return boto3.client('kinesis')

    return boto3.client('kinesis', endpoint_url=endpoint_url)


def init(prediction_stream_name: str, run_id: str, test_run: bool):
    model = load_model(run_id)

    callbacks = []

    if not test_run:
        kinesis_client = create_kinesis_client()
        kinesis_callback = KinesisCallback(kinesis_client, prediction_stream_name)
        callbacks.append(kinesis_callback.put_record)

    model_service = ModelService(model=model, model_version=run_id, callbacks=callbacks)

    return model_service