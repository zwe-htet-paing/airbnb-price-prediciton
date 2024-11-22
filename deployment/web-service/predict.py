import pickle

from flask import Flask, request, jsonify

with open('lin_reg.bin', 'rb') as f_in:
    (dv, model) = pickle.load(f_in)

def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    return float(preds[0])


app = Flask('airbnb-prices-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    data = request.get_json()

    # features = prepare_features(ride)
    pred = predict(data)

    result = {
        'price': pred
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)