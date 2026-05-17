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
    r = client.get("/")
    assert r.status_code == 200
    assert "endpoints" in r.get_json()


def test_examples(client):
    r = client.get("/examples")
    assert r.status_code == 200
    data = r.get_json()
    assert "examples" in data
    assert len(data["examples"]) == 3


def test_metadata(client):
    r = client.get("/metadata")
    assert r.status_code == 200
    data = r.get_json()
    assert "model" in data
    assert "features" in data
    assert "classes" in data


def test_predict_setosa(client):
    r = client.post("/predict", json={
        "sepal_length": 5.1, "sepal_width": 3.5,
        "petal_length": 1.4, "petal_width": 0.2
    })
    assert r.status_code == 200
    assert r.get_json()["prediction"] == "setosa"


def test_predict_missing_fields(client):
    r = client.post("/predict", json={"sepal_length": 5.1})
    assert r.status_code == 400
