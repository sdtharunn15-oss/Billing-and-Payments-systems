import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200