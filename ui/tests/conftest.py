import os
import pytest

@pytest.fixture(autouse=True)
def handle_ngrok_warning(page):
    if "ngrok-free.dev" in (os.getenv("APP_URL") or ""):
        try:
            page.get_by_role("button", name="Visit Site").click(timeout=5000)
        except:
            pass
