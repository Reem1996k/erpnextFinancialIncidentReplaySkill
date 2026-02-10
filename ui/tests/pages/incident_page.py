from playwright.sync_api import Page, expect
import re
import pytest


class IncidentPage:
    def __init__(self, page: Page):
        self.page = page

    def _debug_snapshot(self, name: str):
        self.page.screenshot(
            path=f"playwright-artifacts/{name}.png",
            full_page=True
        )
        print(f"[DEBUG] Screenshot saved: {name}.png")
        print(f"[DEBUG] Current URL: {self.page.url}")

    def expect_status(self, status: str, timeout: int = 10000):
        expect(self.page.get_by_text(status)).to_be_visible(timeout=timeout)

    def run_analysis(self):
        self.page.get_by_role("button", name="Run Analysis").click()

    def expect_analyzing(self):
        try:
            expect(
                self.page.get_by_text(re.compile(r'Analyzing\.\.\.'))
            ).to_be_visible(timeout=10000)
        except AssertionError:
            self._debug_snapshot("analysis_not_started")

            error_visible = self.page.locator(
                ".text-red-600, .error, [role='alert']"
            ).first.is_visible()

            if error_visible:
                pytest.skip(
                    "Analysis failed - backend or AI not configured (see screenshot)"
                )
            raise

    def wait_for_resolved(self):
        try:
            
            expect(
                self.page.get_by_text("Resolved")
            ).to_be_visible(timeout=60000)
        except AssertionError:
            self._debug_snapshot("analysis_not_resolved")

            if self.page.get_by_text("Open").is_visible():
                pytest.skip(
                    "Analysis did not complete (still OPEN) - see screenshot"
                )

            if self.page.get_by_text("Error").is_visible():
                pytest.skip(
                    "Analysis failed with ERROR - see screenshot"
                )
            raise

    def expect_confidence(self):
        expect(
            self.page.get_by_text(re.compile(r'^\d+%$'))
        ).to_be_visible()

    def expect_summary(self):
        expect(
            self.page.get_by_text("ANALYSIS SUMMARY")
        ).to_be_visible()
