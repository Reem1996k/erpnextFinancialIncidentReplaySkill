"""Pytest configuration for UI tests"""
import os
import pytest
from playwright.sync_api import Page


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context with base URL (CI / Local compatible)"""
    return {
        **browser_context_args,
        "baseURL": os.getenv("APP_URL", "http://localhost:3000"),
    }


@pytest.fixture
def page(page: Page):
    return page
