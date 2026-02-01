"""
Integration Test Configuration

This conftest provides fixtures for REAL integration tests:
- No mocks
- Real database (SQLite test DB)
- Real AI client (Anthropic Claude)
- Real ERP client (ERPNext via ngrok)

These tests validate end-to-end behavior including external dependencies.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file BEFORE importing app
backend_dir = Path(__file__).parent.parent.parent
env_path = backend_dir / ".env"
load_dotenv(dotenv_path=env_path)

from app.main import app
from app.db.database import Base
from app.api.incidents import get_db as incidents_get_db
from app.api.analysis import get_db as analysis_get_db


# =========================
# Test Database Setup
# =========================

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="function")
def db_session():
    """
    Creates a clean database session for each test.
    
    This is NOT mocked - it's a real SQLite database.
    We clean it up after each test to ensure isolation.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# =========================
# FastAPI TestClient
# =========================

@pytest.fixture(scope="function")
def client(db_session):
    """
    FastAPI TestClient with real database.
    
    NO MOCKS:
    - AI client uses real Anthropic API
    - ERP client uses real ERPNext instance
    - Only database is overridden for test isolation
    
    This validates real integration behavior.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Override both get_db functions (incidents.py and analysis.py)
    app.dependency_overrides[incidents_get_db] = override_get_db
    app.dependency_overrides[analysis_get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

@pytest.fixture(scope="session", autouse=True)
def validate_integration_environment():
    required_vars = [
        "ERPNEXT_BASE_URL",
        "ERPNEXT_API_KEY",
        "ERPNEXT_API_SECRET",
        "ANTHROPIC_API_KEY",
        "AI_ENABLED"
    ]

    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        pytest.skip(
            "Missing integration environment variables: "
            + ", ".join(missing)
        )

    if os.getenv("AI_ENABLED", "").lower() not in ("true", "1", "yes", "on"):
        pytest.skip("AI_ENABLED must be true for integration tests")

