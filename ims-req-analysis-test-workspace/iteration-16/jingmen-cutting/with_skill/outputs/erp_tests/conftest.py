# =============================================================================
# conftest.py - 全局 Fixtures & 钩子
# 荆门鹰美裁剪系统 2.0 Playwright 测试项目
# =============================================================================

import json
import os
import csv
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext


# =============================================================================
# 项目路径常量
# =============================================================================
PROJECT_ROOT = Path(__file__).resolve().parent
TEST_DATA_DIR = PROJECT_ROOT / "test_data"
OUTPUTS_DIR = PROJECT_ROOT.parent / "outputs"
SCREENSHOTS_DIR = OUTPUTS_DIR / "screenshots"
TRACES_DIR = OUTPUTS_DIR / "traces"


# =============================================================================
# 命令行选项
# =============================================================================
def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="启用有头模式运行浏览器"
    )
    parser.addoption(
        "--slow-mo",
        type=int,
        default=0,
        help="每步操作间隔毫秒数（调试用）"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="http://bak.jmym.dtsimple.pro",
        help="被测系统基础 URL"
    )


# =============================================================================
# 会话级 Fixtures
# =============================================================================
@pytest.fixture(scope="session")
def browser(pytestconfig) -> Browser:
    """会话级浏览器实例 - 整个测试会话共享一个浏览器进程。"""
    headed = pytestconfig.getoption("--headed", default=False)
    slow_mo = pytestconfig.getoption("--slow-mo", default=0)

    with sync_playwright() as p:
        browser_instance = p.chromium.launch(
            headless=not headed,
            slow_mo=slow_mo,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ]
        )
        yield browser_instance
        browser_instance.close()


@pytest.fixture(scope="session")
def test_config() -> dict:
    """加载全局测试配置。"""
    config_path = TEST_DATA_DIR / "test_config.json"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


# =============================================================================
# 函数级 Fixtures
# =============================================================================
@pytest.fixture
def page(browser: Browser) -> Page:
    """每个测试函数获取独立页面，测试后自动关闭。"""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="zh-CN",
        timezone_id="Asia/Shanghai",
    )
    page_instance = context.new_page()
    page_instance.set_default_timeout(15000)
    yield page_instance
    context.close()


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """已登录页面 - 自动完成荆门鹰美环境登录。

    登录流程: 用户名 → 密码 → 点击登录（无企业选择器）
    """
    from utils.test_data import TEST_USERS, ENV_CONFIG, SELECTORS

    base_url = ENV_CONFIG["base_url"]
    username = TEST_USERS["admin"]["username"]
    password = TEST_USERS["admin"]["password"]

    page.goto(f"{base_url}/login", wait_until="domcontentloaded")
    page.wait_for_timeout(1000)

    # 填写用户名
    username_input = page.locator(SELECTORS["login"]["username_input"])
    if username_input.count() == 0:
        # 兜底策略：尝试常见选择器
        username_input = page.locator("input[placeholder*='用户名'], input[placeholder*='账号'], input[name='username'], input[type='text']").first
    username_input.wait_for(state="visible", timeout=10000)
    username_input.fill(username)

    # 填写密码
    password_input = page.locator(SELECTORS["login"]["password_input"])
    if password_input.count() == 0:
        password_input = page.locator("input[placeholder*='密码'], input[name='password'], input[type='password']").first
    password_input.wait_for(state="visible", timeout=5000)
    password_input.fill(password)

    # 点击登录按钮
    login_btn = page.locator(SELECTORS["login"]["login_button"])
    if login_btn.count() == 0:
        login_btn = page.locator("button:has-text('登录'), button:has-text('登 录'), .ant-btn-primary:has-text('登录'), button[type='submit']").first
    login_btn.click()

    # 等待登录完成并进入主页
    page.wait_for_url(f"{base_url}/**", timeout=15000)
    page.wait_for_timeout(2000)

    # 确认登录成功：页面应包含主布局元素
    assert page.locator(".ant-layout, .main-content, nav, header").first.is_visible(timeout=10000), \
        "登录失败：未能检测到主页布局元素"

    return page


@pytest.fixture
def screenshot_on_failure(request, page: Page):
    """测试失败时自动截图。"""
    yield
    if request.node.rep_call.failed:
        test_name = request.node.nodeid.replace("::", "_").replace("/", "_")
        screenshot_path = SCREENSHOTS_DIR / f"{test_name}.png"
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"\n[截图] 失败截图已保存: {screenshot_path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """钩子：收集测试结果状态用于 screenshot_on_failure。"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# =============================================================================
# 数据加载工具 Fixtures
# =============================================================================
@pytest.fixture
def load_json_data():
    """加载 test_data 目录下的 JSON 文件。

    用法:
        data = load_json_data("test_data.json")
        cpos = data["single_cpo"]["cpo_list"]
    """

    def _load(filename: str) -> dict:
        filepath = TEST_DATA_DIR / filename
        if not filepath.exists():
            raise FileNotFoundError(f"测试数据文件不存在: {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    return _load


@pytest.fixture
def load_csv_data():
    """加载 test_data 目录下的 CSV 文件。

    用法:
        rows = load_csv_data("cpo_list.csv")
        for row in rows:
            print(row["cpo_code"])
    """

    def _load(filename: str) -> list[dict]:
        filepath = TEST_DATA_DIR / filename
        if not filepath.exists():
            raise FileNotFoundError(f"测试数据文件不存在: {filepath}")
        with open(filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            return list(reader)

    return _load
