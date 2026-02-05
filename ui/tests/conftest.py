import os
import pytest
import time


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    context = dict(browser_context_args)

    base_url = os.getenv("APP_URL") or "http://localhost:3000"

    context["base_url"] = base_url
    context["extra_http_headers"] = {
        "ngrok-skip-browser-warning": "true"
    }

    return context