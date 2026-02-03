"""Health check test to verify frontend and backend are accessible"""
import pytest
import requests
from playwright.sync_api import expect


def test_backend_health():
    """Verify backend API is accessible"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        assert response.status_code == 200, f"Backend returned status {response.status_code}"
        print("✓ Backend is running")
    except requests.exceptions.ConnectionError:
        pytest.fail("Backend is not running. Start it with: cd backend && uvicorn app.main:app --reload")
    except requests.exceptions.Timeout:
        pytest.fail("Backend connection timeout")


def test_frontend_accessible(page):
    """Verify frontend is accessible"""
    try:
        page.goto("/", timeout=10000)
        expect(page).to_have_title("Financial Incident Replay - Enterprise Platform")
        print("✓ Frontend is running")
    except Exception as e:
        pytest.fail(f"Frontend is not accessible: {e}\nStart it with: cd ui && npm run dev")
