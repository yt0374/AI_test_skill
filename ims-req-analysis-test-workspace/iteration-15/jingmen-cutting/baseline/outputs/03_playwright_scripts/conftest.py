# 荆门新裁剪需求2.0 - Playwright测试配置

import pytest
from playwright.sync_api import Browser, Playwright


def pytest_addoption(parser):
    """添加自定义命令行选项"""
    parser.addoption("--base-url", action="store", default="http://ims-test.example.com",
                     help="测试环境基础URL")
    parser.addoption("--pc-user", action="store", default="test_cutting_manager",
                     help="PC端测试账号")
    parser.addoption("--pc-pass", action="store", default="test123",
                     help="PC端测试密码")
    parser.addoption("--pad-user", action="store", default="test_cutting_worker",
                     help="PAD端测试账号")
    parser.addoption("--pad-pass", action="store", default="test123",
                     help="PAD端测试密码")
    parser.addoption("--headless", action="store_true", default=False,
                     help="无头模式运行")


def pytest_configure(config):
    """配置测试元数据"""
    config._metadata = {
        "项目": "荆门新裁剪需求2.0",
        "版本": "V1.0",
        "测试环境": config.getoption("--base-url"),
        "PC用户": config.getoption("--pc-user"),
        "PAD用户": config.getoption("--pad-user"),
    }


@pytest.fixture(scope="session")
def browser(playwright: Playwright, request) -> Browser:
    """创建浏览器实例"""
    headless = request.config.getoption("--headless")
    browser = playwright.chromium.launch(
        headless=headless,
        args=["--start-maximized"]
    )
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def base_url(request) -> str:
    """基础URL"""
    return request.config.getoption("--base-url")


def pytest_html_report_title(report):
    """自定义HTML报告标题"""
    report.title = "荆门新裁剪需求2.0 - 自动化测试报告"


def pytest_html_results_table_header(cells):
    """自定义HTML报告表头"""
    cells.insert(2, "<th>模块</th>")
    cells.insert(3, "<th>优先级</th>")
    cells.pop()


def pytest_html_results_table_row(report, cells):
    """自定义HTML报告行"""
    # 从测试名称提取模块
    if hasattr(report, "nodeid"):
        nodeid = report.nodeid
        if "TestCuttingTask" in nodeid:
            module = "裁剪任务"
        elif "TestBedTask" in nodeid:
            module = "床次任务"
        elif "TestCardPrinting" in nodeid:
            module = "扎卡打印"
        elif "TestHangingOperation" in nodeid:
            module = "缝制挂片"
        elif "TestOvercutAudit" in nodeid:
            module = "超裁审核"
        elif "TestEndToEnd" in nodeid:
            module = "端到端集成"
        else:
            module = "通用"
        cells.insert(2, f"<td>{module}</td>")

        if "p0" in nodeid.lower():
            priority = "P0"
        elif "p1" in nodeid.lower():
            priority = "P1"
        elif "p2" in nodeid.lower():
            priority = "P2"
        else:
            priority = "P3"
        cells.insert(3, f"<td>{priority}</td>")

    cells.pop()
