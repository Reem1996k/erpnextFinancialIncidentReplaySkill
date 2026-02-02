import pytest
from tests.pages.create_incident_page import CreateIncidentPage
from tests.pages.incident_page import IncidentPage
from tests.pages.incidents_list_page import IncidentsListPage


@pytest.mark.e2e
def test_incident_full_flow(page):
    """Complete E2E test: Create incident -> Analyze -> View from list"""
    create_page = CreateIncidentPage(page)
    incident_page = IncidentPage(page)
    list_page = IncidentsListPage(page)

    # Step 1: Open create incident page and fill form
    create_page.open()
    create_page.fill_erp_reference("ACC-SINV-2026-00009")
    create_page.select_incident_type("payment_mismatch")
    create_page.fill_description(
        "Customer claims invoice amount is higher than agreed"
    )
    
    # Step 2: Submit form (handles analyzing state and navigation)
    create_page.submit()

    # Step 3: Verify incident page shows OPEN status
    incident_page.expect_status("OPEN")

    # Step 4: Run analysis
    incident_page.run_analysis()

    # Step 5: Verify analyzing state (status still OPEN, analyzing indicator visible)
    incident_page.expect_analyzing()

    # Step 6: Wait for AI analysis to complete
    incident_page.wait_for_resolved()

    # Step 7: Verify analysis results are displayed
    incident_page.expect_confidence()
    incident_page.expect_summary()
    
    # Step 8: Navigate to incidents list via header
    list_page.navigate_via_header()
    
    # Step 9: Click View to return to incident details
    list_page.click_view_for_first_incident()
    
    # Step 10: Verify status is still RESOLVED after navigation
    incident_page.expect_status("RESOLVED")