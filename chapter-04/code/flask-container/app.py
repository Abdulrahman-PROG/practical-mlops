from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

CLASSES = ["setosa", "versicolor", "virginica"]


@app.route("/")
def index():
    return jsonify({"status": "ok", "model": "Iris Classifier v1"})


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    required = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    features = np.array([[data[f] for f in required]])
    prediction = int(model.predict(features)[0])
    confidence = float(model.predict_proba(features)[0][prediction])

    return jsonify({
        "prediction": CLASSES[prediction],
        "confidence": round(confidence, 4),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
