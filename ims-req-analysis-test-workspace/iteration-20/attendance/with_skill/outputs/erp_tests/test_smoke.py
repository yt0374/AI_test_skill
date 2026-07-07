# erp_tests/test_smoke.py — P0 smoke tests for 考勤模块
"""P0 Smoke: core navigation, login, and critical CRUD operations.

Tests in this file must pass for every build. Failures block the build.
"""

import pytest
from conftest import navigate_to_hr_module
from pages.base_page import (
    AttendanceRegistrationPage,
    DailyAttendancePage,
    LeaveRegistrationPage,
    MonthlyAttendancePage,
)


@pytest.mark.p0
class TestSmokeNavigation:
    """P0: Verify all attendance pages load successfully."""

    def test_navigate_to_attendance_registration(self, logged_in_page):
        """F-01: Navigate to 考勤登记 page."""
        navigate_to_hr_module(logged_in_page, "考勤登记")
        logged_in_page.wait_for_selector(".ant-table", timeout=10_000)

    def test_navigate_to_daily_attendance(self, logged_in_page):
        """F-05: Navigate to 日考勤统计 page."""
        navigate_to_hr_module(logged_in_page, "日考勤统计")
        logged_in_page.wait_for_selector(".ant-table", timeout=10_000)

    def test_navigate_to_leave_registration(self, logged_in_page):
        """F-03: Navigate to 请假登记 page."""
        navigate_to_hr_module(logged_in_page, "请假登记")
        logged_in_page.wait_for_selector(".ant-table", timeout=10_000)

    def test_navigate_to_return_work(self, logged_in_page):
        """F-02: Navigate to 回工登记 page."""
        navigate_to_hr_module(logged_in_page, "回工登记")
        logged_in_page.wait_for_selector(".ant-table", timeout=10_000)

    def test_navigate_to_monthly_attendance(self, logged_in_page):
        """F-09: Navigate to 月考勤统计 page."""
        navigate_to_hr_module(logged_in_page, "月考勤统计")
        logged_in_page.wait_for_selector(".ant-table", timeout=10_000)


@pytest.mark.p0
class TestSmokeCRUD:
    """P0: Core create/read operations on key pages."""

    def test_attendance_query_today(self, logged_in_page):
        """C-04: Query today's attendance without errors."""
        navigate_to_hr_module(logged_in_page, "考勤登记")
        page = AttendanceRegistrationPage(logged_in_page)
        page.click_button("查询")

    def test_daily_attendance_query_today(self, logged_in_page):
        """F-05: Query today's daily attendance without errors."""
        navigate_to_hr_module(logged_in_page, "日考勤统计")
        page = DailyAttendancePage(logged_in_page)
        page.click_button("查询")

    def test_leave_registration_new_dialog(self, logged_in_page):
        """C-13: Click 新增 on 请假登记 opens edit dialog."""
        navigate_to_hr_module(logged_in_page, "请假登记")
        page = LeaveRegistrationPage(logged_in_page)
        page.click_button("新增")
        # Verify dialog opened
        logged_in_page.wait_for_selector(".ant-modal", timeout=5_000)

    def test_monthly_attendance_query(self, logged_in_page):
        """F-09: Query monthly attendance without errors."""
        navigate_to_hr_module(logged_in_page, "月考勤统计")
        page = MonthlyAttendancePage(logged_in_page)
        page.click_button("查询")
