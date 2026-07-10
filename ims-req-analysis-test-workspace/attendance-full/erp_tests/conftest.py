"""IMS Attendance Module — Pytest Fixtures (Practical Edition)

Uses IMS hash-based SPA routing. Login with enterprise selector.
Auto-screenshots on failure saved to reports/screenshots/{datetime}/.
Post-test cleanup: deletes imported attendance records for the day.
"""
import json
import csv
import os
import pytest
from datetime import datetime

# === Session-level setup/cleanup ===

def pytest_sessionfinish(session, exitstatus):
    """Clean up test data after all tests complete."""
    try:
        from setup_test_data import cleanup_test_data
        cleanup_test_data()
        print("\n[cleanup] Test data cleaned up")
    except Exception as e:
        print(f"\n[cleanup] Cleanup failed: {e}")
from pathlib import Path
from playwright.sync_api import Page, Browser, BrowserContext

BASE_URL = "http://test.fj.dtsimple.pro"
TEST_DATA_DIR = Path(__file__).parent / "test_data"

# Screenshot directory: reports/screenshots/2026-07-08_173000/
_RUN_TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H%M%S")
SCREENSHOT_DIR = Path(__file__).parent.parent / "reports" / "screenshots" / _RUN_TIMESTAMP
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# IMS hash routes for attendance pages (verified on SIT 2026-07-08)
ATTENDANCE_ROUTES = {
    "考勤登记": "/#/personnel/workAttendance/detail",
    "回工登记": "/#/personnel/workAttendance/returningWork",
    "请假登记": "/#/personnel/workAttendance/leave",
    "日考勤统计": "/#/personnel/workAttendance/dailyReportNew",
    "月考勤统计": "/#/personnel/workAttendance/monthlyReport",
    "小组出勤表": "/#/personnel/workAttendance/teamAttendanceReport",
    "员工缺勤表": "/#/personnel/workAttendance/employeeAbsenceReport",
}


def load_json_dataset(name: str) -> dict:
    path = TEST_DATA_DIR / "test_data.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f).get(name, {})


def screenshot(page: Page, name: str) -> str:
    """Take a screenshot and return the file path."""
    safe_name = name.replace("/", "_").replace("\\", "_").replace(":", "_").replace(" ", "_")
    filepath = SCREENSHOT_DIR / f"{safe_name}.png"
    page.screenshot(path=str(filepath), full_page=True)
    return str(filepath)


# === Pytest Hooks ===

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Auto-screenshot on test failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = getattr(item, "_page", None)
        if page is None:
            # Try to get page from fixture
            try:
                page_fixture = item.funcargs.get("page")
                logged_in = item.funcargs.get("logged_in_page")
                page = logged_in or page_fixture
            except Exception:
                pass

        if page:
            try:
                test_name = item.nodeid.replace("::", "_").replace("/", "_")[-120:]
                screenshot(page, f"FAILED_{test_name}")
            except Exception:
                pass


# === Fixtures ===

@pytest.fixture(scope="session")
def run_timestamp() -> str:
    """Session-level timestamp for this test run."""
    return _RUN_TIMESTAMP


@pytest.fixture(scope="session")
def browser_context(browser: Browser) -> BrowserContext:
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="zh-CN",
    )
    yield context
    context.close()


@pytest.fixture
def page(browser_context: BrowserContext, request) -> Page:
    page = browser_context.new_page()
    page.set_default_timeout(30000)
    # Store reference for failure screenshot hook
    request.node._page = page
    yield page
    page.close()


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """Login to IMS SIT and return authenticated page."""
    username = os.environ.get("TEST_USERNAME", "admin")
    password = os.environ.get("TEST_PASSWORD", "metas2660")

    page.goto(f"{BASE_URL}/")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Already logged in (cookie/session)
    if "/home" in page.url:
        return page

    # Login form
    if "/login" in page.url:
        page.fill("#form_item_username", username)
        page.fill("#form_item_password", password)
        sel = page.locator(".ant-select")
        if sel.count() > 0:
            sel.first.click()
            page.wait_for_timeout(800)
            opts = page.locator(".ant-select-item-option-content")
            if opts.count() > 0:
                opts.first.click()
                page.wait_for_timeout(500)
        page.click(".ant-btn-primary")
        page.wait_for_timeout(5000)
        page.wait_for_load_state("networkidle")
        return page

    # Fallback: try login elements on current page
    username_input = page.locator("#form_item_username")
    if username_input.count() > 0:
        username_input.fill(username)
        page.locator("#form_item_password").fill(password)
        sel = page.locator(".ant-select")
        if sel.count() > 0:
            sel.first.click()
            page.wait_for_timeout(500)
            page.locator(".ant-select-item-option-content").first.click()
        page.locator(".ant-btn-primary").click()
        page.wait_for_timeout(5000)
        page.wait_for_load_state("networkidle")

    return page


# === Data-driven test fixtures ===

_dataset_cache: dict | None = None  # module-level: run pipeline only once
_cache_date: str = ""  # date of cached data — auto-invalidates daily

def _clear_dataset_cache():
    """Clear dataset cache to force re-extraction. Call after data changes."""
    global _dataset_cache
    _dataset_cache = None


@pytest.fixture
def test_dataset(logged_in_page: Page) -> dict:
    """Ensure SIT has attendance data, then return extracted dataset.

    Pipeline (runs ONCE per date):
      1. Extract existing → if >= 10 records, return directly
      2. Run 日考勤计算 in same session
      3. Re-extract
    """
    global _dataset_cache, _cache_date
    from datetime import datetime
    today = datetime.now().strftime("%Y%m%d")

    if _cache_date != today:
        _dataset_cache = None

    if _dataset_cache is not None:
        return _dataset_cache

    from utils.test_data_generator import generate_and_import
    _dataset_cache = generate_and_import(logged_in_page)
    _cache_date = today
    return _dataset_cache


@pytest.fixture
def normal_employee(test_dataset: dict) -> dict:
    """Return a real normal employee from SIT for data-driven tests."""
    emp = test_dataset.get("samples", {}).get("normal_employee")
    if emp:
        return emp
    pytest.skip("No normal employee data available in SIT")


@pytest.fixture
def late_employee(test_dataset: dict) -> dict:
    """Return a real late employee from SIT."""
    emp = test_dataset.get("samples", {}).get("late_employee")
    if emp:
        return emp
    pytest.skip("No late employee data available in SIT")


@pytest.fixture
def absent_employee(test_dataset: dict) -> dict:
    """Return a real absent employee from SIT."""
    emp = test_dataset.get("samples", {}).get("absent_employee")
    if emp:
        return emp
    pytest.skip("No absent employee data available in SIT")


@pytest.fixture
def missing_card_employee(test_dataset: dict) -> dict:
    """Return a real missing-card employee from SIT."""
    emp = test_dataset.get("samples", {}).get("missing_card_employee")
    if emp:
        return emp
    pytest.skip("No missing card employee data available in SIT")


@pytest.fixture
def navigate_to_attendance(logged_in_page: Page) -> Page:
    """Navigate to attendance pages by clicking sidebar via JS."""
    page = logged_in_page

    # Click HR module (index 11) via Vue router or sidebar
    page.evaluate("""() => {
        const items = document.querySelectorAll('.mts-layout-mix-sider-module__item');
        // Module order: 样衣0/销售1/采购2/仓库3/生产4/质检5/物流6/报表7/数据8/吊挂9/平板10/人事11/看板12/系统13
        const hrIdx = 11;
        if (items[hrIdx]) {
            items[hrIdx].style.display = 'block';
            items[hrIdx].style.visibility = 'visible';
            items[hrIdx].click();
        }
    }""")
    page.wait_for_timeout(3000)
    return page
