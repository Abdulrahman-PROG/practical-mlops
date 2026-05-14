import pickle
import numpy as np
from sklearn.linear_model import LinearRegression

# Simple dataset: [size_sqft, bedrooms] -> price
X = np.array([
    [600, 1], [800, 2], [1000, 2], [1200, 3],
    [1500, 3], [1800, 4], [2000, 4], [2500, 5],
])
y = np.array([150000, 200000, 240000, 280000,
              340000, 400000, 450000, 560000])

model = LinearRegression()
model.fit(X, y)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved to model.pkl")
