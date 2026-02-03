"""
Feature Test: Incident Page Refresh

Tests that the incident page can be refreshed via browser reload.
Verifies that data persists correctly after page reload.
"""
import pytest
from tests.pages.create_incident_page import CreateIncidentPage
from tests.pages.incident_page import IncidentPage


@pytest.mark.feature
def test_page_reload_preserves_open_status(page):
    """
    FEATURE: Verify browser reload preserves incident data
    
    Test flow:
    1. Create a new incident
    2. Navigate to incident details page
    3. Verify initial status is visible
    4. Reload the page (browser refresh)
    5. Verify status remains visible after reload
    """
    create_page = CreateIncidentPage(page)
    incident_page = IncidentPage(page)

    # Step 1: Create incident and navigate to details page
    create_page.open()
    create_page.fill_erp_reference("RELOAD-TEST-2026-00001")
    create_page.select_incident_type("invoice_discrepancy")
    create_page.fill_description("Test incident for page reload functionality")
    create_page.submit()

    # Step 2: Verify initial page load - status should be OPEN
    incident_page.expect_status("OPEN")

    # Step 3: Reload the page (browser refresh)
    page.reload(wait_until="networkidle")

    # Step 4: Verify status is still visible after reload
    incident_page.expect_status("OPEN")


@pytest.mark.feature
def test_page_reload_preserves_resolved_status(page):
    """
    FEATURE: Verify page reload preserves RESOLVED status
    
    Test flow:
    1. Create incident
    2. Run analysis and wait for RESOLVED status
    3. Reload the page
    4. Verify RESOLVED status persists after reload
    """
    create_page = CreateIncidentPage(page)
    incident_page = IncidentPage(page)

    # Step 1: Create incident
    create_page.open()
    create_page.fill_erp_reference("ACC-SINV-2026-00003")
    create_page.select_incident_type("payment_mismatch")
    create_page.fill_description("Test page reload with resolved incident")
    create_page.submit()

    # Step 2: Run analysis and wait for resolution
    incident_page.expect_status("OPEN")
    incident_page.run_analysis()
    incident_page.wait_for_resolved()

    # Step 3: Reload the page
    page.reload(wait_until="networkidle")

    # Step 4: Verify RESOLVED status is preserved
    incident_page.expect_status("RESOLVED")
