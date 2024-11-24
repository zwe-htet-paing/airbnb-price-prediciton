from pathlib import Path

import model


def read_text(file):
    test_directory = Path(__file__).parent

    with open(test_directory / file, 'rt', encoding='utf-8') as f_in:
        return f_in.read().strip()


def test_base64_decode():
    base64_input = read_text('data.b64')

    actual_result = model.base64_decode(base64_input)
    expected_result = {
    "input_data": {
            "room_type": "Entire home/apt",
            "neighbourhood": "SIXTH WARD",
            "latitude": 42.65222,
            "longitude": -73.76724,
            "minimum_nights": 2,
            "number_of_reviews": 302,
            "reviews_per_month": 2.53,
            "availability_365": 253
        },
        "input_id": 123
    }

    assert actual_result == expected_result


def test_prepare_features():
    model_service = model.ModelService(None)

    input_data = {
        "room_type": "Entire home/apt",
        "neighbourhood": "SIXTH WARD",
        "latitude": 42.65222,
        "longitude": -73.76724,
        "minimum_nights": 2,
        "number_of_reviews": 302,
        "reviews_per_month": 2.53,
        "availability_365": 253
    }

    actual_features = model_service.prepare_features(input_data)

    expected_fetures = {
        "room_type": "Entire home/apt",
        "neighbourhood": "SIXTH WARD",
        "latitude": 42.65222,
        "longitude": -73.76724,
        "minimum_nights": 2,
        "number_of_reviews": 302,
        "reviews_per_month": 2.53,
        "availability_365": 253
    }

    assert actual_features == expected_fetures


class ModelMock:
    def __init__(self, value):
        self.value = value

    def predict(self, X):
        n = len(X)
        return [self.value] * n


def test_predict():
    model_mock = ModelMock(10.0)
    model_service = model.ModelService(model_mock)

    features = {
        "room_type": "Entire home/apt",
        "neighbourhood": "SIXTH WARD",
        "latitude": 42.65222,
        "longitude": -73.76724,
        "minimum_nights": 2,
        "number_of_reviews": 302,
        "reviews_per_month": 2.53,
        "availability_365": 253
    }

    actual_prediction = model_service.predict(features)
    expected_prediction = 10.0

    assert actual_prediction == expected_prediction


def test_lambda_handler():
    model_mock = ModelMock(10.0)
    model_version = 'Test123'
    model_service = model.ModelService(model_mock, model_version)

    base64_input = read_text('data.b64')

    event = {
        "Records": [
            {
                "kinesis": {
                    "data": base64_input,
                },
            }
        ]
    }

    actual_predictions = model_service.lambda_handler(event)
    expected_predictions = {
        'predictions': [
            {
                'model': 'price_prediction_model',
                'version': model_version,
                'prediction': {
                    'price': 10.0,
                    'input_id': 123
                },
            }
        ]
    }

    assert actual_predictions == expected_predictions