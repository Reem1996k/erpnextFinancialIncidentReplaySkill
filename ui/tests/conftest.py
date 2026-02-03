"""Pytest configuration for UI tests"""
import os
import pytest
from playwright.sync_api import Page


"""Pytest configuration for UI tests"""
import os
import pytest

def pytest_configure(config):
    # pytest-base-url plugin
    config.option.base_url = os.getenv(
        "APP_URL",
        "http://localhost:3000"
    )


@pytest.fixture
def page(page: Page):
    return page
