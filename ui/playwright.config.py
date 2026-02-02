from playwright.sync_api import Playwright

BASE_URL = "http://localhost:3000"

def pytest_configure(config):
    config.option.base_url = BASE_URL
