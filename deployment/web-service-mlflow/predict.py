import os
import numpy as np

import mlflow
from flask import Flask, request, jsonify


TRACKING_URL = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(TRACKING_URL)

# RUN_ID = os.getenv('RUN_ID')
RUN_ID = "1936d050006746eeaa60c76db167d18c"
logged_model = f'runs:/{RUN_ID}/model'

# Load model
model = mlflow.sklearn.load_model(logged_model)

def predict(features):
    preds = model.predict(features)
    result = np.power(10, preds[0])
    
    return float(result)


app = Flask('airbna-price-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    data = request.get_json()

    pred = predict(data)

    result = {
        'price': pred,
        'model_version': RUN_ID
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)