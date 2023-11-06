import pytest
from flask import json
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_add(client):
    response = client.post(
        "/add",
        data=json.dumps({"a": 5, "b": 3}),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.get_json() == {"result": 8}


def test_subtract(client):
    response = client.post(
        "/subtract",
        data=json.dumps({"a": 5, "b": 3}),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.get_json() == {"result": 2}
