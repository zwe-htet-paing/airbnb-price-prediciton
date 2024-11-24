import os
import json
import boto3
import base64

kinesis_client = boto3.client('kinesis')

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'airbnb_predictions')

# RUN_ID = os.getenv('RUN_ID')

# logged_model = f's3://mlflow-models-alexey/1/{RUN_ID}/artifacts/model'
# # logged_model = f'runs:/{RUN_ID}/model'
# model = mlflow.pyfunc.load_model(logged_model)

TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'

def prepare_features(input_data):
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

def predict(features):
    # pred = model.predict(features)
    # return float(pred[0])
    return 100.0

def lambda_handler(event, context):
    # print(json.dumps(event))
    predictions_events = []
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        airbnb_event = json.loads(decoded_data)
        # print(airbnb_event)

        input_data = airbnb_event['input_data']
        input_id = airbnb_event['input_id']

        features = prepare_features(input_data)
        prediction = predict(features)

        prediciton_event = {
            'model': 'price_prediction_model',
            'version': '1',
            'prediction': {
                'price': prediction,
                'input_id': input_id
            }
        }

        if not TEST_RUN:
            kinesis_client.put_record(
                StreamName=PREDICTIONS_STREAM_NAME,
                Data=json.dumps(prediciton_event),
                PartitionKey=str(input_id)
            )
        predictions_events.append(prediciton_event)

    return {
        'predictions': predictions_events
    }
