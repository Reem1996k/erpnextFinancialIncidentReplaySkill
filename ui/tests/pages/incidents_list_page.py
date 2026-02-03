from playwright.sync_api import Page


class IncidentsListPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        """Navigate directly to incidents list page"""
        self.page.goto("/incidents")

    def navigate_via_header(self):
        """Click 'Incidents' link in the top navigation bar"""
        self.page.get_by_role("link", name="Incidents").click()
        # Wait for navigation to complete
        self.page.wait_for_url("**/incidents", timeout=10000)

    def click_view_for_first_incident(self):
        """Click the 'View' button for the first incident in the list"""
        self.page.get_by_role("link", name="View").first.click()
        # Wait for navigation to incident detail page
        self.page.wait_for_url("**/incidents/*", timeout=10000)
