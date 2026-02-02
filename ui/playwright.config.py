import os

def pytest_configure(config):
    config.option.base_url = os.getenv("BASE_URL")