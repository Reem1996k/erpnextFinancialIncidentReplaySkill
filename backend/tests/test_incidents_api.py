"""
Write a pytest test for POST /incidents.

Test steps:
- Use FastAPI TestClient
- Send valid incident payload
- Assert status code is 201
- Assert response contains:
  - id
  - erp_reference
  - status == "OPEN"

"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base
from app.db.models import Incident


# Create test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


from app.api.incidents import get_db
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup():
    """Clean up test database after each test."""
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_incident_success():
    """Test successful creation of a new incident."""
    payload = {
        "erp_reference": "ERR-001",
        "incident_type": "Financial_Discrepancy",
        "description": "Test incident description"
    }
    
    response = client.post("/incidents/", json=payload)
    
    # Assert status code is 201
    assert response.status_code == 201
    
    # Parse response
    data = response.json()
    
    # Assert response contains required fields
    assert "id" in data
    assert data["erp_reference"] == "ERR-001"
    assert data["status"] == "OPEN"
    assert data["incident_type"] == "Financial_Discrepancy"
    assert data["description"] == "Test incident description"
    assert "created_at" in data


def test_create_incident_missing_fields():
    """Test incident creation with missing required fields."""
    payload = {
        "erp_reference": "ERR-002"
    }
    
    response = client.post("/incidents/", json=payload)
    
    # Should fail validation (422 Unprocessable Entity)
    assert response.status_code == 422


def test_get_incident_success():
    """Test successful retrieval of an incident by ID."""
    # First, create an incident
    payload = {
        "erp_reference": "ERR-003",
        "incident_type": "Audit_Finding",
        "description": "Test GET endpoint"
    }
    
    create_response = client.post("/incidents/", json=payload)
    assert create_response.status_code == 201
    created_data = create_response.json()
    incident_id = created_data["id"]
    
    # Now fetch the incident
    get_response = client.get(f"/incidents/{incident_id}")
    
    # Assert status code is 200
    assert get_response.status_code == 200
    
    # Parse response
    data = get_response.json()
    
    # Assert returned data matches created data
    assert data["id"] == incident_id
    assert data["erp_reference"] == "ERR-003"
    assert data["status"] == "OPEN"
    assert data["incident_type"] == "Audit_Finding"
    assert data["description"] == "Test GET endpoint"


def test_get_incident_not_found():
    """Test retrieval of non-existent incident."""
    # Try to fetch an incident that doesn't exist
    response = client.get("/incidents/9999")
    
    # Assert status code is 404
    assert response.status_code == 404
    
    # Assert error message is present
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_replay_incident_success():
    """Test successful replay of an incident."""
    # First, create an incident
    payload = {
        "erp_reference": "ERR-004",
        "incident_type": "Pricing_Issue",
        "description": "Test replay endpoint"
    }
    
    create_response = client.post("/incidents/", json=payload)
    assert create_response.status_code == 201
    created_data = create_response.json()
    incident_id = created_data["id"]
    
    # Call replay endpoint
    replay_response = client.post(f"/incidents/{incident_id}/replay")
    
    # Assert status code is 200
    assert replay_response.status_code == 200
    
    # Parse response
    data = replay_response.json()
    
    # Assert status is ANALYZED
    assert data["status"] == "ANALYZED"
    
    # Assert replay fields are populated
    assert data["replay_summary"] is not None
    assert "exceeds expected amount" in data["replay_summary"].lower()
    assert "15.0%" in data["replay_summary"]
    assert data["replay_details"] is not None
    assert data["replay_conclusion"] is not None
    assert data["replayed_at"] is not None


def test_replay_incident_not_found():
    """Test replay of non-existent incident."""
    # Try to replay an incident that doesn't exist
    response = client.post("/incidents/9999/replay")
    
    # Assert status code is 404
    assert response.status_code == 404
    
    # Assert error message is present
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()

