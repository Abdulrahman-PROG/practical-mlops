import pickle
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)


@app.route("/")
def index():
    return jsonify({
        "message": "Housing Price Prediction API",
        "usage": "POST /predict with JSON: {size_sqft: int, bedrooms: int}"
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    size = data.get("size_sqft")
    bedrooms = data.get("bedrooms")

    if size is None or bedrooms is None:
        return jsonify({"error": "size_sqft and bedrooms are required"}), 400

    features = np.array([[size, bedrooms]])
    price = model.predict(features)[0]
    return jsonify({"predicted_price": round(float(price), 2)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
