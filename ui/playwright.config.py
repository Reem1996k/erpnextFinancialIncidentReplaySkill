from playwright.sync_api import Playwright

BASE_URL = "https://lichenlike-kellee-autocratically.ngrok-free.dev"

def pytest_configure(config):
    config.option.base_url = BASE_URL
