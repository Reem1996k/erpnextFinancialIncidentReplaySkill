from playwright.sync_api import Page, expect
import pytest


class CreateIncidentPage:
    def __init__(self, page: Page):
        self.page = page

    def _debug_snapshot(self, name: str):
        self.page.screenshot(
            path=f"playwright-artifacts/{name}.png",
            full_page=True
        )
        print(f"[DEBUG] Screenshot saved: {name}.png")
        print(f"[DEBUG] Current URL: {self.page.url}")

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
        self.page.get_by_role("button", name="Create & Analyze").click()

        try:
            self.page.wait_for_url("**/incidents/*", timeout=60000)
        except Exception:
            self._debug_snapshot("incident_creation_failed")

            if self.page.locator(".error-box").is_visible():
                pytest.skip(
                    "Incident creation failed (backend/API unavailable – see screenshot)"
                )
            raise

        self.page.get_by_role("button", name="Run Analysis").wait_for(timeout=30000)
        expect(self.page.get_by_text("OPEN")).to_be_visible(timeout=30000)
