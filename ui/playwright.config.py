import os
from playwright.sync_api import Playwright

def pytest_configure(config):
    base_url = os.getenv(
        "APP_URL",
        "http://localhost:3000"  # fallback ללוקאל
    )
    config.base_url = base_url

