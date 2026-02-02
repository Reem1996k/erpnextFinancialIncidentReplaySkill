from playwright.sync_api import Page, expect
import re


class IncidentPage:
    def __init__(self, page: Page):
        self.page = page

    def expect_status(self, status: str, timeout: int = 10000):
        """Verify the incident status badge shows the expected status"""
        expect(
            self.page.get_by_text(status)
        ).to_be_visible(timeout=timeout)

    def run_analysis(self):
        """Click the Run Analysis button"""
        self.page.get_by_role("button", name="Run Analysis").click()

    def expect_analyzing(self):
        """Wait for analyzing state: 'Analyzing...' text visible"""
        # Wait for analyzing indicator to appear
        expect(
            self.page.get_by_text("Analyzing...")
        ).to_be_visible(timeout=10000)

    def wait_for_resolved(self):
        """Wait for analysis to complete and status to change to RESOLVED"""
        expect(
            self.page.get_by_text("RESOLVED")
        ).to_be_visible(timeout=60000)

    def expect_confidence(self):
        """Verify confidence score is visible (contains % symbol)"""
        # Match percentage like "97%" but not text containing "%"
        expect(
            self.page.get_by_text(re.compile(r'^\d+%$'))
        ).to_be_visible()

    def expect_summary(self):
        """Verify analysis summary section is visible"""
        expect(self.page.get_by_text("ANALYSIS SUMMARY")).to_be_visible()
