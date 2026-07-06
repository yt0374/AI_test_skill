"""
Pytest configuration for IMS Attendance (考勤) module E2E tests.

Environment: SIT (test.fj.dtsimple.pro)
Enterprise: 最佳智造
Module: 人事 > 考勤 (7 sub-pages)
Login: admin / admin123 (SIT credentials)
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
    """Launch a persistent Chromium browser for the test session."""
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
    """Create a new browser context with Chinese locale for each test."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="zh-CN",
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext):
    """Create a new page for each test."""
    page = context.new_page()
    yield page
    page.close()


# ---------------------------------------------------------------------------
# Login fixture (auto-use for all tests)
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def login(page: Page):
    """Login to SIT IMS ERP before each test.

    Environment: test.fj.dtsimple.pro
    Enterprise: 最佳智造
    Credentials: admin / admin123

    Login flow: URL -> username -> password -> click login ->
                select enterprise (if shown) -> wait for dashboard.
    """
    SIT_URL = "http://test.fj.dtsimple.pro"
    SIT_USERNAME = "admin"
    SIT_PASSWORD = "admin123"
    ENTERPRISE_NAME = "最佳智造"

    page.goto(SIT_URL, wait_until="domcontentloaded")

    # Fill username
    username_input = page.locator("#form_item_username")
    username_input.wait_for(state="visible", timeout=15000)
    username_input.fill(SIT_USERNAME)

    # Fill password
    password_input = page.locator("#form_item_password")
    password_input.fill(SIT_PASSWORD)

    # Click login button
    login_btn = page.locator(".ant-btn-primary")
    login_btn.click()

    # Check for enterprise selector (SIT environment shows enterprise list after login)
    try:
        enterprise_modal = page.locator(".ant-modal:visible, .enterprise-selector")
        enterprise_modal.wait_for(state="visible", timeout=5000)
        # Click the enterprise row
        enterprise_item = page.locator(
            f".ant-modal:visible tr:has-text('{ENTERPRISE_NAME}'), "
            f".enterprise-item:has-text('{ENTERPRISE_NAME}')"
        )
        enterprise_item.first.click()
        # Click confirm/enter button
        confirm_btn = page.locator(
            ".ant-modal:visible button:has-text('确定'), "
            ".ant-modal:visible button:has-text('进入')"
        )
        confirm_btn.click()
    except Exception:
        # No enterprise selector — direct login (already on dashboard)
        pass

    # Wait for dashboard to load
    page.wait_for_url("**/dashboard**", timeout=20000)
    expect(page).to_have_title("首页 - 麦塔西智能制造协同平台", timeout=15000)

    yield


# ---------------------------------------------------------------------------
# Test data loader fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def load_csv():
    """Load test data from CSV file.

    Returns a callable that takes a filename and returns list[dict].
    Searches erp_tests/test_data/ first, then outputs/.
    """
    def _load(filename: str) -> list[dict]:
        filepath = TEST_DATA_DIR / filename
        if not filepath.exists():
            filepath = OUTPUT_DIR / filename  # fallback to outputs/
        if not filepath.exists():
            raise FileNotFoundError(f"Test data file not found: {filename}")
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    return _load


@pytest.fixture
def load_json():
    """Load test data from JSON file.

    Returns a callable that takes a filename and returns dict.
    """
    def _load(filename: str) -> dict:
        filepath = TEST_DATA_DIR / filename
        if not filepath.exists():
            filepath = OUTPUT_DIR / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Test data file not found: {filename}")
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return _load


# ---------------------------------------------------------------------------
# Navigation helpers for attendance module
# ---------------------------------------------------------------------------
def navigate_to_attendance(page: Page, submenu: str = None):
    """Navigate to 人事 > 考勤 module, optionally to a specific sub-page.

    Args:
        page: Playwright page
        submenu: Sub-page name (one of the 7 attendance sub-pages):
                  考勤登记, 回工登记, 请假登记, 日考勤统计,
                  月考勤统计, 小组出勤表, 员工缺勤表
    """
    # Click 人事 in sidebar
    hr_module = page.locator(".mts-layout-mix-sider-module__item", has_text="人事")
    hr_module.click()
    page.wait_for_timeout(800)

    if submenu:
        # Click sub-menu in .third-menu panel
        submenu_item = page.locator(".third-menu .menu-item", has_text=submenu)
        submenu_item.click()
        page.wait_for_timeout(800)


def get_attendance_subpages():
    """Return the list of 7 attendance sub-pages for parametrized navigation tests."""
    return [
        "考勤登记",
        "回工登记",
        "请假登记",
        "日考勤统计",
        "月考勤统计",
        "小组出勤表",
        "员工缺勤表",
    ]
