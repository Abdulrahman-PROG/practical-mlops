import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

iris = load_iris()
model = LogisticRegression(max_iter=200)
model.fit(iris.data, iris.target)

initial_type = [("float_input", FloatTensorType([None, 4]))]
onnx_model = convert_sklearn(model, initial_types=initial_type)

with open("model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

print("ONNX model saved to model.onnx")
