"""
Pytest configuration for Jingmen Cutting 2.0 E2E tests.

Environment: jingmen (bak.jmym.dtsimple.pro)
Login: admin / ym5579 (direct login, no enterprise selector)
"""
import pytest
import json
import csv
from pathlib import Path
from playwright.sync_api import Page, Browser, BrowserContext, expect


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
TEST_DATA_DIR = Path(__file__).parent / "test_data"
OUTPUT_DIR = Path(__file__).parent.parent  # outputs/


# ---------------------------------------------------------------------------
# Browser fixture (session-scoped)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def browser():
    """Launch a persistent browser for the test session."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"],
            slow_mo=100,  # 100ms delay for visual debugging
        )
        yield browser
        browser.close()


# ---------------------------------------------------------------------------
# Context + Page fixtures (function-scoped)
# ---------------------------------------------------------------------------
@pytest.fixture
def context(browser: Browser):
    """Create a new browser context with viewport for each test."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="zh-CN",
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext):
    """Create a new page and perform login."""
    page = context.new_page()
    yield page
    page.close()


# ---------------------------------------------------------------------------
# Login fixture (auto-use for all tests)
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def login(page: Page):
    """Login to Jingmen ERP before each test.

    Jingmen environment: direct login, no enterprise selector.
    URL: http://bak.jmym.dtsimple.pro
    Credentials: admin / ym5579
    """
    page.goto("http://bak.jmym.dtsimple.pro", wait_until="domcontentloaded")

    # Fill username
    username_input = page.locator("#form_item_username")
    username_input.wait_for(state="visible", timeout=10000)
    username_input.fill("admin")

    # Fill password
    password_input = page.locator("#form_item_password")
    password_input.fill("ym5579")

    # Click login button
    login_btn = page.locator(".ant-btn-primary")
    login_btn.click()

    # Wait for dashboard to load
    page.wait_for_url("**/dashboard**", timeout=15000)
    expect(page).to_have_title("首页 - 麦塔西智能制造协同平台")

    yield


# ---------------------------------------------------------------------------
# Test data loader fixture
# ---------------------------------------------------------------------------
@pytest.fixture
def load_csv():
    """Load test data from CSV file.

    Returns a dict keyed by data_id for easy lookup.
    """
    def _load(filename: str) -> list[dict]:
        filepath = TEST_DATA_DIR / filename
        if not filepath.exists():
            filepath = OUTPUT_DIR / filename  # fallback to outputs/
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    return _load


@pytest.fixture
def load_json():
    """Load test data from JSON file."""
    def _load(filename: str) -> dict:
        filepath = TEST_DATA_DIR / filename
        if not filepath.exists():
            filepath = OUTPUT_DIR / filename
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return _load


# ---------------------------------------------------------------------------
# Navigation helpers
# ---------------------------------------------------------------------------
def navigate_to_production(page: Page, submenu: str = None):
    """Navigate to 生产 module and optionally a sub-menu page.

    Jingmen uses simple module names (e.g., '生产' not 'gm.生产#3').
    Sub-menus open via .third-menu panel.
    """
    # Click 生产 in sidebar
    production = page.locator(".mts-layout-mix-sider-module__item", has_text="生产")
    production.click()
    page.wait_for_timeout(500)

    if submenu:
        # Open sub-menu in .third-menu panel
        submenu_item = page.locator(".third-menu .menu-item", has_text=submenu)
        submenu_item.click()
        page.wait_for_timeout(500)


def navigate_via_third_menu(page: Page, module: str, *menu_path: str):
    """Navigate through Jingmen's .third-menu panel system.

    Args:
        page: Playwright page
        module: Sidebar module name (e.g., '生产')
        *menu_path: Menu path items to click in order
    """
    # Click module in sidebar
    sidebar = page.locator(".mts-layout-mix-sider-module__item", has_text=module)
    sidebar.click()
    page.wait_for_timeout(800)

    # Navigate through third-menu levels
    for item in menu_path:
        menu_item = page.locator(".third-menu", has_text=item)
        menu_item.click()
        page.wait_for_timeout(500)
