"""Pytest configuration for UI tests"""
import pytest
from playwright.sync_api import Page


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, pytestconfig):
    """Configure browser context with base URL"""
    return {
        **browser_context_args,
        "base_url": pytestconfig.getini("base_url") or "http://localhost:3000",
    }


@pytest.fixture
def page(page: Page):
    """Page fixture that uses base_url from configuration"""
    return page
