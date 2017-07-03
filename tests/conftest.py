# content of conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption("--access_token", action="store", default="",
        help="access_token parameter")
    parser.addoption("--url", action="store",
            default="https://www.melown.com/cloud/backend/api",
            help="Server URL")
    parser.addoption("--app_id", action="store",
            default="com.melown.mario-web-console",
            help="Application ID")

@pytest.fixture
def access_token(request):
    return request.config.getoption("--access_token")

@pytest.fixture
def url(request):
    return request.config.getoption("--url")

@pytest.fixture
def app_id(request):
    return request.config.getoption("--app_id")
