import pytest
from app.main import app
from starlette.testclient import TestClient

USER_NAME = "meli"
QUESTION = "quien es zara?"

@pytest.fixture
def test_client():
    client = TestClient(app)
    return client

def test_generate_answer(test_client):
    response = test_client.post(
            f"/askme?user_name={USER_NAME}&question={QUESTION}")
    assert response.status_code == 200