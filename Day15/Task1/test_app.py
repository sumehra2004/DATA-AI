import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_form_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<form" in response.data

def test_form_submission(client):
    response = client.post("/", data={"name": "John"})
    assert response.status_code == 200
    assert b"Hello John" in response.data
