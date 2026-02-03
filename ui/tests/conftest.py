import os
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    context = dict(browser_context_args)

    # ✅ Skip NGROK warning page
    if os.getenv("APP_URL"):
        context["extra_http_headers"] = {
            "ngrok-skip-browser-warning": "true"
        }

    return context
