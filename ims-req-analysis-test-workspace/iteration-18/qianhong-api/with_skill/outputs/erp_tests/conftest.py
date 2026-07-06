"""
IMS ERP API Test Fixtures - conftest.py
Provides: api_client (httpx sync), auth token, test data loading
"""
import os
import json
import pytest
import httpx
from pathlib import Path

BASE_URL = os.getenv("IMS_BASE_URL", "http://test.fj.dtsimple.pro/api/ims-open-api")
TEST_USERNAME = os.getenv("IMS_TEST_USERNAME", "admin")
TEST_PASSWORD = os.getenv("IMS_TEST_PASSWORD", "IMS@2026")

TEST_DATA_DIR = Path(__file__).parent / "test_data"


@pytest.fixture(scope="session")
def base_url():
    """Base URL for IMS API."""
    return BASE_URL


@pytest.fixture(scope="session")
def auth_token(base_url):
    """Get Bearer token once per test session."""
    with httpx.Client(timeout=30) as client:
        resp = client.post(
            f"{base_url}/api/ims-open-api/public/auth/authorization",
            json={"username": TEST_USERNAME, "password": TEST_PASSWORD},
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("code") == 0:
                return data.get("data", "")
        pytest.fail(f"Failed to get auth token: {resp.status_code} {resp.text}")
    return None


@pytest.fixture
def api_client(base_url, auth_token):
    """Httpx client with auth headers."""
    with httpx.Client(
        base_url=base_url,
        timeout=30,
        headers={
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json;charset=utf-8",
        },
    ) as client:
        yield client


@pytest.fixture
def unauth_client(base_url):
    """Httpx client without auth headers."""
    with httpx.Client(
        base_url=base_url,
        timeout=30,
        headers={"Content-Type": "application/json;charset=utf-8"},
    ) as client:
        yield client


@pytest.fixture
def load_test_data():
    """Load test data from JSON file."""

    def _load(filename):
        path = TEST_DATA_DIR / filename
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    return _load
