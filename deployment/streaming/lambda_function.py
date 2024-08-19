import os
import json
import boto3
import base64

import mlflow

kinesis_client = boto3.client('kinesis')

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'airbnb_predictions')


RUN_ID = os.getenv('RUN_ID')

logged_model = f's3://mlflow-models-alexey/1/{RUN_ID}/artifacts/model'
# logged_model = f'runs:/{RUN_ID}/model'
model = mlflow.pyfunc.load_model(logged_model)


TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'


def predict(features):
    pred = model.predict(features)
    return float(pred[0])


def lambda_handler(event, context):
    # print(json.dumps(event))
    
    predictions_events = []
    
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        event = json.loads(decoded_data)

        # print(event)
        features = event['features']
        id_ = event['id_']
    
        prediction = predict(features)
    
        prediction_event = {
            'model': 'airbnb_price_prediction_model',
            'version': '123',
            'prediction': {
                'feature_duration': prediction,
                'id_': id_   
            }
        }

        if not TEST_RUN:
            kinesis_client.put_record(
                StreamName=PREDICTIONS_STREAM_NAME,
                Data=json.dumps(prediction_event),
                PartitionKey=str(id_)
            )
        
        predictions_events.append(prediction_event)


    return {
        'predictions': predictions_events
    }