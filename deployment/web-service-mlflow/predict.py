import os
import pickle
import numpy as np

import mlflow
from flask import Flask, request, jsonify


TRACKING_URL = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(TRACKING_URL)

# RUN_ID = os.getenv('RUN_ID')
RUN_ID = "7b5744464f544451aee4a9308d1971ad"

logged_model = f'runs:/{RUN_ID}/models'
model = mlflow.pyfunc.load_model(logged_model)

with open("preprocessor.b", 'rb') as f_in:
    dv = pickle.load(f_in)

def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
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