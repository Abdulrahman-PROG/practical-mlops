import pickle
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

CLASSES = ["setosa", "versicolor", "virginica"]

EXAMPLES = [
    {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2, "expected": "setosa"},
    {"sepal_length": 6.7, "sepal_width": 3.0, "petal_length": 5.2, "petal_width": 2.3, "expected": "virginica"},
    {"sepal_length": 5.9, "sepal_width": 3.0, "petal_length": 4.2, "petal_width": 1.5, "expected": "versicolor"},
]


@app.route("/")
def index():
    return jsonify({
        "message": "Iris Classifier API",
        "endpoints": {
            "GET  /": "This help message",
            "GET  /examples": "Sample inputs you can use to test the model",
            "GET  /metadata": "Model information and feature descriptions",
            "POST /predict": "Classify an iris flower — send JSON with sepal_length, sepal_width, petal_length, petal_width",
        }
    })


@app.route("/examples")
def examples():
    return jsonify({
        "description": "Copy any of these into POST /predict to test the model",
        "examples": EXAMPLES
    })


@app.route("/metadata")
def metadata():
    return jsonify({
        "model": "Logistic Regression",
        "library": "scikit-learn",
        "dataset": "Iris (Fisher, 1936)",
        "classes": CLASSES,
        "features": {
            "sepal_length": "Sepal length in cm",
            "sepal_width": "Sepal width in cm",
            "petal_length": "Petal length in cm",
            "petal_width": "Petal width in cm",
        },
        "accuracy": "~97% on Iris dataset",
        "version": "1.0.0",
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    required = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    features = np.array([[data[f] for f in required]])
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    return jsonify({
        "prediction": CLASSES[prediction],
        "confidence": round(float(probabilities[prediction]), 4),
        "probabilities": {cls: round(float(prob), 4) for cls, prob in zip(CLASSES, probabilities)},
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
