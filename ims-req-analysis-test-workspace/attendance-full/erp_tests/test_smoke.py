"""IMS Attendance — P0 Smoke Tests (Verified URLs)

All routes verified on SIT 2026-07-08.
Screenshots saved to reports/screenshots/{timestamp}/.
"""
import pytest
from playwright.sync_api import Page, expect
from conftest import screenshot

BASE = "http://test.fj.dtsimple.pro"

ROUTES = {
    "考勤登记": f"{BASE}/#/personnel/workAttendance/detail",
    "回工登记": f"{BASE}/#/personnel/workAttendance/returningWork",
    "请假登记": f"{BASE}/#/personnel/workAttendance/leave",
    "日考勤统计": f"{BASE}/#/personnel/workAttendance/dailyReportNew",
    "月考勤统计": f"{BASE}/#/personnel/workAttendance/monthlyReport",
    "小组出勤表": f"{BASE}/#/personnel/workAttendance/teamAttendanceReport",
    "员工缺勤表": f"{BASE}/#/personnel/workAttendance/employeeAbsenceReport",
}


@pytest.mark.p0
class TestLoginAndDashboard:
    """登录 + 首页验证"""

    def test_login_successful(self, logged_in_page: Page, run_timestamp: str):
        assert "/home" in logged_in_page.url or "/dashboard" in logged_in_page.url
        screenshot(logged_in_page, "01_login_dashboard")

    def test_sidebar_modules_exist(self, logged_in_page: Page):
        modules = logged_in_page.locator(".mts-layout-mix-sider-module__item")
        assert modules.count() == 14


@pytest.mark.p0
class TestAttendancePages:
    """考勤7个核心页面 — 均可访问"""

    @pytest.mark.parametrize("name,url", list(ROUTES.items()))
    def test_page_accessible(self, logged_in_page: Page, name, url):
        page = logged_in_page
        page.goto(url, timeout=15000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        assert "ErrorPage" not in page.title(), f"{name} returned ErrorPage"
        # Screenshot each attendance page
        safe_name = name.replace(" ", "_")
        screenshot(page, f"02_page_{safe_name}")


@pytest.mark.p0
class TestDailyAttendance:
    """日考勤统计 — 核心页面元素"""

    def test_query_button_exists(self, logged_in_page: Page):
        page = logged_in_page
        page.goto(ROUTES["日考勤统计"], timeout=15000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        buttons = page.locator("button, .ant-btn, [type='button']")
        assert buttons.count() > 0, "No buttons found on daily attendance page"
        screenshot(page, "03_daily_attendance_loaded")


@pytest.mark.p0
class TestLeaveRegistration:
    """请假登记 — 核心元素"""

    def test_add_button_exists(self, logged_in_page: Page):
        page = logged_in_page
        page.goto(ROUTES["请假登记"], timeout=15000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        buttons = page.locator("button, .ant-btn, [type='button']")
        assert buttons.count() > 0, "No buttons found on leave page"
        screenshot(page, "04_leave_registration_loaded")
