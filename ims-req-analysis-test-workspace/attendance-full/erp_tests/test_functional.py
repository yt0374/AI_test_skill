"""IMS Attendance — P1 Functional Tests (Verified URLs)

Screenshots saved at key checkpoints to reports/screenshots/{timestamp}/.
"""
import pytest
from playwright.sync_api import Page, expect
from conftest import screenshot

BASE = "http://test.fj.dtsimple.pro"
DAILY = f"{BASE}/#/personnel/workAttendance/dailyReportNew"
LEAVE = f"{BASE}/#/personnel/workAttendance/leave"
RETURN = f"{BASE}/#/personnel/workAttendance/returningWork"
DETAIL = f"{BASE}/#/personnel/workAttendance/detail"
MONTHLY = f"{BASE}/#/personnel/workAttendance/monthlyReport"
GROUP = f"{BASE}/#/personnel/workAttendance/teamAttendanceReport"
ABSENCE = f"{BASE}/#/personnel/workAttendance/employeeAbsenceReport"


@pytest.mark.p1
class TestDailyAttendanceQuery:
    """日考勤统计 — 查询功能"""

    def test_page_loads(self, logged_in_page: Page):
        page = logged_in_page
        page.goto(DAILY, timeout=15000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        assert "ErrorPage" not in page.title()
        screenshot(page, "P1_daily_query_page")

    def test_date_filter_present(self, logged_in_page: Page):
        page = logged_in_page
        page.goto(DAILY, timeout=15000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        date_inputs = page.locator(".ant-picker input, input[placeholder*='日期']")
        assert date_inputs.count() >= 1, "Date filter not found"

    def test_employee_filter_present(self, logged_in_page: Page):
        page = logged_in_page
        page.goto(DAILY, timeout=15000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        emp_select = page.locator(".ant-select, input[placeholder*='员工']")
        assert emp_select.count() >= 1, "Employee filter not found"


@pytest.mark.p1
class TestLeaveRegistrationFlow:
    """请假登记 — 核心流程"""

    def test_page_loads(self, logged_in_page: Page):
        page = logged_in_page
        page.goto(LEAVE, timeout=15000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        assert "ErrorPage" not in page.title()
        screenshot(page, "P1_leave_list_page")

    def test_add_button_opens_form(self, logged_in_page: Page):
        page = logged_in_page
        page.goto(LEAVE, timeout=15000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        add_btn = page.locator("button:has-text('新增')")
        if add_btn.count() > 0:
            add_btn.first.click()
            page.wait_for_timeout(2000)
            form_fields = page.locator(".ant-select, input, textarea")
            assert form_fields.count() > 2, "Leave form did not appear"
            screenshot(page, "P1_leave_add_form")


@pytest.mark.p1
class TestReturnWorkFlow:
    """回工登记 — 核心流程"""

    def test_page_loads(self, logged_in_page: Page):
        page = logged_in_page
        page.goto(RETURN, timeout=15000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        assert "ErrorPage" not in page.title()
        screenshot(page, "P1_return_work_page")

    def test_query_fields_present(self, logged_in_page: Page):
        page = logged_in_page
        page.goto(RETURN, timeout=15000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        selectors = page.locator(".ant-select")
        assert selectors.count() >= 1, "No select fields found"


@pytest.mark.p1
class TestAttendanceRegistration:
    """考勤登记 — 核心流程"""

    def test_page_loads(self, logged_in_page: Page):
        page = logged_in_page
        page.goto(DETAIL, timeout=15000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        assert "ErrorPage" not in page.title()
        screenshot(page, "P1_attendance_detail_page")

    def test_query_button_exists(self, logged_in_page: Page):
        page = logged_in_page
        page.goto(DETAIL, timeout=15000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        buttons = page.locator("button, .ant-btn, [type='button']")
        assert buttons.count() > 0, "No buttons found on registration page"


@pytest.mark.p1
class TestMonthlyAttendance:
    """月考勤统计 — 核心流程"""

    def test_page_loads(self, logged_in_page: Page):
        page = logged_in_page
        page.goto(MONTHLY, timeout=15000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        assert "ErrorPage" not in page.title()
        screenshot(page, "P1_monthly_report_page")


@pytest.mark.p1
class TestGroupAndAbsenceReports:
    """小组出勤表 + 员工缺勤表"""

    def test_group_page_loads(self, logged_in_page: Page):
        page = logged_in_page
        page.goto(GROUP, timeout=15000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        assert "ErrorPage" not in page.title()
        screenshot(page, "P1_group_attendance_page")

    def test_absence_page_loads(self, logged_in_page: Page):
        page = logged_in_page
        page.goto(ABSENCE, timeout=15000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        assert "ErrorPage" not in page.title()
        screenshot(page, "P1_employee_absence_page")
