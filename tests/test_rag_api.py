from fastapi.testclient import TestClient
from app.main import app

def test_rag_request_validation():
    client = TestClient(app)
    response = client.post("/rag/search", json={"query": ""})
    assert response.status_code == 422
