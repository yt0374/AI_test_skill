# erp_tests/conftest.py — Playwright + pytest fixtures for 考勤模块
"""Shared fixtures: browser, login, test data loading."""

import json
import csv
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, Browser

BASE_DIR = Path(__file__).parent
TEST_DATA_DIR = BASE_DIR / "test_data"

# SIT environment config
SIT_URL = "http://test.fj.dtsimple.pro"
SIT_USER = "admin"
SIT_PASS = "metas2660"
SIT_ENTERPRISE = "最佳智造"
LOGIN_TIMEOUT = 30_000  # ms


@pytest.fixture(scope="session")
def browser():
    """Session-scoped browser instance."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser: Browser) -> Page:
    """Function-scoped page with clean context."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="zh-CN",
    )
    page = context.new_page()
    page.set_default_timeout(15_000)
    yield page
    context.close()


@pytest.fixture(scope="function")
def logged_in_page(page: Page) -> Page:
    """Page pre-authenticated as gm.人事#1 on SIT."""
    page.goto(SIT_URL, timeout=LOGIN_TIMEOUT)
    page.fill("#form_item_username", SIT_USER)
    page.fill("#form_item_password", SIT_PASS)
    # Select enterprise
    page.click(".ant-select")  # enterprise selector
    page.click(f".ant-select-item-option-content:has-text('{SIT_ENTERPRISE}')")
    page.click(".ant-btn-primary")
    page.wait_for_url("**/home**", timeout=LOGIN_TIMEOUT)
    return page


@pytest.fixture(scope="session")
def test_data() -> dict:
    """Load test_data.json as dict."""
    data_file = TEST_DATA_DIR / "test_data.json"
    if data_file.exists():
        return json.loads(data_file.read_text(encoding="utf-8"))
    return {}


def load_csv_data(filename: str) -> list[dict]:
    """Load CSV test data file."""
    path = TEST_DATA_DIR / filename
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def navigate_to_hr_module(page: Page, sub_module: str):
    """Navigate to人事 sub-module page.

    sub_module options:
      - 考勤登记, 回工登记, 请假登记
      - 日考勤统计, 月考勤统计
      - 小组出勤表, 员工缺勤表
    """
    # Click 人事 in sidebar
    page.click('.mts-layout-mix-sider-module__item:has-text("人事")')
    page.wait_for_timeout(500)
    # Click sub-menu - SIT uses .third-menu
    page.click(f'.third-menu:has-text("{sub_module}")')
    page.wait_for_load_state("networkidle")
