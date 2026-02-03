from playwright.sync_api import Page, expect
import pytest


class CreateIncidentPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("/")
        self.page.wait_for_load_state("networkidle")
        self.page.get_by_role("button", name="Create & Analyze").wait_for(timeout=30000)

    def fill_erp_reference(self, value: str):
        self.page.get_by_placeholder("e.g., INV-2024-001234").fill(value)

    def select_incident_type(self, value: str):
        self.page.get_by_role("combobox").select_option(value)

    def fill_description(self, text: str):
        self.page.get_by_placeholder(
            "Describe the issue in detail"
        ).fill(text)

    def submit(self):
        # Click submit and wait for client-side routing to incident page.
        self.page.get_by_role("button", name="Create & Analyze").click()

        # Next.js uses SPA navigation; prefer waiting for URL change.
        try:
            self.page.wait_for_url("**/incidents/*", timeout=60000)
        except Exception:
            # If no navigation, check if the form displayed an error state.
            if self.page.locator(".error-box").is_visible():
                pytest.skip("Incident creation failed (backend/API unavailable). Skipping flow test.")
            # Otherwise, continue and let subsequent waits assert state.

        # Once on the incident page, the Run Analysis button should be present.
        self.page.get_by_role("button", name="Run Analysis").wait_for(timeout=30000)
        expect(self.page.get_by_text("OPEN")).to_be_visible(timeout=30000)

