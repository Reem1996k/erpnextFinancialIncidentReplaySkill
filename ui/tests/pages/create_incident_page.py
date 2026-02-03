from playwright.sync_api import Page, expect


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
        # Click submit and wait for navigation to complete
        with self.page.expect_navigation(url="**/incidents/*", timeout=20000):
            self.page.get_by_role("button", name="Create & Analyze").click()

