"""
Root conftest.py for pytest configuration
"""
import pytest
import subprocess
import time
import requests
from playwright.sync_api import sync_playwright


# Global variable to store server process
_server_process = None


def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "api: API tests")
    config.addinivalue_line("markers", "bdd: BDD tests")
    config.addinivalue_line("markers", "ui: UI tests")


@pytest.fixture(scope="session", autouse=True)
def start_server():
    """Start FastAPI server for testing"""
    global _server_process

    # Start the server
    _server_process = subprocess.Popen(
        ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to be ready
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("\nServer started successfully")
                break
        except requests.exceptions.ConnectionError:
            if i == max_retries - 1:
                _server_process.kill()
                raise Exception("Server failed to start")
            time.sleep(1)

    yield

    # Cleanup
    if _server_process:
        _server_process.terminate()
        _server_process.wait()
        print("\nServer stopped")


@pytest.fixture(scope="session")
def playwright_instance():
    """Create Playwright instance"""
    with sync_playwright() as p:
        yield p
