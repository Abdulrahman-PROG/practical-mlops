import numpy as np
import onnxruntime as rt
from flask import Flask, request, jsonify

app = Flask(__name__)

session = rt.InferenceSession("model.onnx")
input_name = session.get_inputs()[0].name
CLASSES = ["setosa", "versicolor", "virginica"]


@app.route("/")
def index():
    return jsonify({"status": "ok", "model": "Iris ONNX Classifier v1", "runtime": "ONNX Runtime"})


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

    features = np.array([[data[f] for f in required]], dtype=np.float32)
    prediction = session.run(None, {input_name: features})[0][0]

    return jsonify({
        "prediction": CLASSES[int(prediction)],
        "runtime": "onnx",
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
