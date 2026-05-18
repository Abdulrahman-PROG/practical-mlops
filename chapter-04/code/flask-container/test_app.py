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
    with app.test_client() as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "healthy"


def test_index_returns_ok(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_predict_valid(client):
    r = client.post("/predict", json={
        "sepal_length": 5.1, "sepal_width": 3.5,
        "petal_length": 1.4, "petal_width": 0.2,
    })
    assert r.status_code == 200
    data = r.get_json()
    assert "prediction" in data
    assert "confidence" in data
    assert data["prediction"] in ["setosa", "versicolor", "virginica"]


def test_predict_missing_fields(client):
    r = client.post("/predict", json={"sepal_length": 5.1})
    assert r.status_code == 400


def test_predict_returns_json(client):
    r = client.post("/predict", json={
        "sepal_length": 6.7, "sepal_width": 3.0,
        "petal_length": 5.2, "petal_width": 2.3,
    })
    assert r.content_type == "application/json"
