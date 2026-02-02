"""
Smoke Test: Critical User Path

Validates:
1. Application loads
2. User can create an incident
3. Incident page opens successfully
4. Basic incident data is visible

Does NOT validate:
- AI analysis results
- Deep data validation
- Error scenarios
"""
import pytest
from tests.pages.create_incident_page import CreateIncidentPage
from tests.pages.incident_page import IncidentPage


@pytest.mark.smoke
def test_create_incident_smoke(page):
    """
    SMOKE: Verify critical path - create incident and navigate to incident page
    
    Minimal assertions, fast execution, happy path only
    """
    create_page = CreateIncidentPage(page)
    incident_page = IncidentPage(page)

    # Step 1: Load application
    create_page.open()

    # Step 2: Fill minimal required fields
    create_page.fill_erp_reference("SMOKE-INV-2026-00001")
    create_page.select_incident_type("payment_mismatch")
    create_page.fill_description("Smoke test incident")

    # Step 3: Submit and navigate
    create_page.submit()

    # Step 4: Verify incident page loaded with OPEN status
    incident_page.expect_status("OPEN", timeout=10000)

    # SMOKE TEST STOPS HERE
    # No deep analysis validation, no AI checks
