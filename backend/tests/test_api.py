from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_replay_customer_returns_schema():
    r = client.get("/replay/customer/CUST-0001")
    assert r.status_code == 200
    data = r.json()

    assert data["scope"]["type"] == "customer"
    assert data["scope"]["customer_id"] == "CUST-0001"
    assert "summary" in data
    assert "timeline" in data
    assert "findings" in data
    assert "control_gaps" in data
    assert "conclusion" in data
