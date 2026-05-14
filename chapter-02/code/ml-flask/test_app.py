import pytest
import subprocess
import sys
from app import app


@pytest.fixture(scope="session", autouse=True)
def train_model():
    subprocess.run([sys.executable, "train.py"], check=True)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "predicted_price" not in response.get_json()


def test_predict(client):
    response = client.post("/predict", json={"size_sqft": 1200, "bedrooms": 3})
    assert response.status_code == 200
    data = response.get_json()
    assert "predicted_price" in data
    assert data["predicted_price"] > 0


def test_predict_missing_fields(client):
    response = client.post("/predict", json={"size_sqft": 1000})
    assert response.status_code == 400
