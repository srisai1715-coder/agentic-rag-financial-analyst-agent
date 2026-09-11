from fastapi.testclient import TestClient
from app.main import app

def test_agent_request_validation():
    client = TestClient(app)
    response = client.post("/agent/ask", json={"query": ""})
    assert response.status_code == 422
