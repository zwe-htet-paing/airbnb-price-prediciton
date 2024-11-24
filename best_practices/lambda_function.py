import os
import model



PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'airbnb_predictions')
# RUN_ID = os.getenv('RUN_ID')
TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'

model_service = model.init()

def lambda_handler(event, context):
    return model_service.lambda_handler(event)