from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_intent_validation():
    r = client.post("/payments/intents", json={"amount": 0})
    assert r.status_code == 422
