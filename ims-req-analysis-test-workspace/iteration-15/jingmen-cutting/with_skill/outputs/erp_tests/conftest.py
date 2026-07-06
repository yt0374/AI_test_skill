"""
Pytest configuration for 荆门新裁剪需求2.0 Playwright automation tests.

Environment order: SIT → jingmen (模拟生产 bak.jmym.dtsimple.pro)
"""
import pytest
import json
from pathlib import Path

# =============================================================
# Test Data Fixtures
# =============================================================

def load_test_data():
    """Load test_data.json from the test_data directory."""
    data_path = Path(__file__).parent / "test_data" / "test_data.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_env_config(env: str = "jingmen"):
    """Load environment-specific configuration."""
    env_path = Path(__file__).parent.parent.parent.parent.parent / "environments" / f"{env}.json"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            return json.load(f)
    # Fallback to jingmen defaults
    return {
        "url": "http://bak.jmym.dtsimple.pro",
        "credentials": {"username": "admin", "password": "ym5579"},
        "type": "customer"
    }


@pytest.fixture(scope="session")
def test_data():
    """Session-scoped fixture for all test datasets."""
    return load_test_data()


@pytest.fixture(scope="session")
def env_config():
    """Session-scoped fixture for environment configuration."""
    return load_env_config("jingmen")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, env_config):
    """Configure browser context with environment-specific settings."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "zh-CN",
    }


@pytest.fixture(scope="session")
def base_url(env_config):
    """Base URL from environment config."""
    return env_config.get("url", "http://bak.jmym.dtsimple.pro")


@pytest.fixture(scope="session")
def credentials(env_config):
    """Login credentials from environment config."""
    return env_config.get("credentials", {"username": "admin", "password": "ym5579"})


@pytest.fixture(scope="session")
def logged_in_page(browser, base_url, credentials):
    """Session-scoped fixture: login once, reuse across tests."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="zh-CN"
    )
    page = context.new_page()

    # Navigate to login page
    page.goto(f"{base_url}/login", wait_until="networkidle")

    # Fill login form (jingmen: no enterprise selector)
    page.fill("#form_item_username", credentials["username"])
    page.fill("#form_item_password", credentials["password"])
    page.click(".ant-btn-primary")

    # Wait for dashboard/home page
    page.wait_for_url(f"{base_url}/**", timeout=15000)
    page.wait_for_load_state("networkidle")

    yield page

    context.close()


@pytest.fixture(scope="function")
def cutting_task_page(logged_in_page, base_url):
    """Navigate to the cutting task page on PC."""
    page = logged_in_page
    # Navigate via sidebar: 生产 > 裁剪任务
    # Note: actual selectors depend on jingmen environment UI structure
    page.goto(f"{base_url}/production/cutting-task", wait_until="networkidle")
    yield page


# =============================================================
# Pytest Configuration
# =============================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "p0: Smoke tests - must pass for every build")
    config.addinivalue_line("markers", "p1: Functional tests - core business flows")
    config.addinivalue_line("markers", "p2: Boundary tests - edge cases and validation")
    config.addinivalue_line("markers", "p3: Integration tests - cross-module workflows")
    config.addinivalue_line("markers", "flaky: Tests with known intermittent failures")
    config.addinivalue_line("markers", "quarantine: Tests isolated due to persistent failure")
    config.addinivalue_line("markers", "pc: PC端 browser tests")
    config.addinivalue_line("markers", "pad: PAD端 tablet tests (emulated viewport)")
    config.addinivalue_line("markers", "sit: SIT environment tests")
    config.addinivalue_line("markers", "jingmen: 荆门 customer environment tests")


def pytest_collection_modifyitems(config, items):
    """Add markers based on test path/module."""
    for item in items:
        if "smoke" in str(item.fspath):
            item.add_marker(pytest.mark.p0)
        if "functional" in str(item.fspath):
            item.add_marker(pytest.mark.p1)
        if "boundary" in str(item.fspath):
            item.add_marker(pytest.mark.p2)
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.p3)


# =============================================================
# Playwright-specific fixtures
# =============================================================

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch arguments."""
    return {
        **browser_type_launch_args,
        "headless": True,
        "slow_mo": 100,  # Slow down operations for visibility
    }
