import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

iris = load_iris()
model = LogisticRegression(max_iter=200)
model.fit(iris.data, iris.target)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved.")
