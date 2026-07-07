"""
Pytest conftest.py — Playwright fixtures for jingmen environment.
Jingmen (荆门鹰美) specific: admin/ym5579, no enterprise selector, direct login.
"""
import json
import os
import pytest
from pathlib import Path
from utils.test_data_loader import TestDataLoader

# --- Paths ---
PROJECT_ROOT = Path(__file__).parent
TEST_DATA_DIR = PROJECT_ROOT / "test_data"

# --- Jingmen environment config ---
JINGMEN_URL = "http://bak.jmym.dtsimple.pro"
JINGMEN_USER = "admin"
JINGMEN_PASSWORD = "ym5579"


@pytest.fixture(scope="session")
def test_data():
    """Load all test data from CSV file."""
    csv_path = PROJECT_ROOT.parent / "test_data.csv"
    return TestDataLoader(csv_path)


@pytest.fixture(scope="session")
def jingmen_url():
    return JINGMEN_URL


@pytest.fixture(scope="session")
def jingmen_credentials():
    return {"username": JINGMEN_USER, "password": JINGMEN_PASSWORD}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override browser context args for jingmen environment."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "zh-CN",
    }


@pytest.fixture(scope="session")
def context(browser, jingmen_credentials, jingmen_url):
    """Create browser context and log in to jingmen environment."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="zh-CN",
    )
    page = context.new_page()

    # Navigate and log in
    page.goto(jingmen_url, wait_until="domcontentloaded", timeout=30000)

    # Jingmen: direct login, no enterprise selector
    page.wait_for_selector("#form_item_username", timeout=15000)
    page.fill("#form_item_username", jingmen_credentials["username"])
    page.fill("#form_item_password", jingmen_credentials["password"])
    page.click(".ant-btn-primary")

    # Wait for sidebar to appear (login success indicator)
    page.wait_for_selector(".mts-layout-mix-sider-module__item", timeout=30000)

    yield context
    context.close()


@pytest.fixture
def page(context):
    """Create a new page for each test, already authenticated."""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def data_loader():
    """Load test data from CSV."""
    csv_path = PROJECT_ROOT.parent / "test_data.csv"
    loader = TestDataLoader(csv_path)
    return loader


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "p0: Smoke tests — must pass for every build")
    config.addinivalue_line("markers", "p1: Functional tests — core business flows")
    config.addinivalue_line("markers", "p2: Boundary tests — edge cases and validation")
    config.addinivalue_line("markers", "p3: Integration tests — cross-module workflows")
    config.addinivalue_line("markers", "flaky: Tests with known intermittent failures")
    config.addinivalue_line("markers", "quarantine: Tests isolated due to persistent failure")
