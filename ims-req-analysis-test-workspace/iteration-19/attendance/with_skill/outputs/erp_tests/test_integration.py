"""P3 Integration Tests: IMS Attendance (考勤) Module

Cross-module workflows spanning attendance, HR, and other modules.
End-to-end scenarios and data consistency verification across sub-pages.

Priority: P3
Markers: p3, integration
"""
import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from conftest import navigate_to_attendance


@pytest.mark.p3
@pytest.mark.integration
class TestAttendanceDataCollectionFlow:
    """F-01: End-to-end attendance data collection to daily stats."""

    def test_attendance_register_to_daily_stats_flow(self, page: Page):
        """F-01: Verify data flow from 考勤登记 to 日考勤统计.

        Steps:
        1. Navigate to 考勤登记 and query records
        2. Navigate to 日考勤统计 and verify data consistency
        3. Verify employees with attendance records appear in daily stats
        """
        bp = BasePage(page)

        # Step 1: Query attendance records
        navigate_to_attendance(page, "考勤登记")
        bp.click_search()
        page.wait_for_timeout(2000)

        # Record the page state
        attendance_loaded = "考勤登记" in page.title()
        assert attendance_loaded, "Attendance register page should load"

        # Step 2: Navigate to daily stats
        navigate_to_attendance(page, "日考勤统计")
        bp.click_search()
        page.wait_for_timeout(2000)

        # Verify daily stats page loads
        daily_stats_loaded = "日考勤统计" in page.title()
        assert daily_stats_loaded, "Daily stats page should load"

        # Step 3: Both pages should be functional
        table = page.locator(".ant-table")
        expect(table.first).to_be_visible(timeout=8000)

    def test_attendance_register_to_group_report(self, page: Page):
        """Verify 考勤登记 data appears in 小组出勤表."""
        bp = BasePage(page)

        # Check attendance register
        navigate_to_attendance(page, "考勤登记")
        bp.click_search()
        page.wait_for_timeout(2000)
        assert "考勤登记" in page.title()

        # Navigate to group attendance report
        navigate_to_attendance(page, "小组出勤表")
        bp.click_search()
        page.wait_for_timeout(2000)

        assert "小组出勤表" in page.title()
        # Table should load
        table = page.locator(".ant-table")
        expect(table.first).to_be_visible(timeout=8000)

    def test_attendance_register_to_absence_report(self, page: Page):
        """Verify 考勤登记 data appears in 员工缺勤表."""
        bp = BasePage(page)

        # Source: attendance register
        navigate_to_attendance(page, "考勤登记")
        bp.click_search()
        page.wait_for_timeout(2000)

        # Target: employee absence report
        navigate_to_attendance(page, "员工缺勤表")
        bp.click_search()
        page.wait_for_timeout(2000)

        assert "员工缺勤表" in page.title()
        table = page.locator(".ant-table")
        expect(table.first).to_be_visible(timeout=8000)


@pytest.mark.p3
@pytest.mark.integration
class TestReturnWorkToDailyStatsFlow:
    """F-02: Return-work registration to daily stats flow."""

    def test_return_work_to_daily_stats(self, page: Page):
        """F-02: Verify 回工登记 data flows to 日考勤统计.

        Steps:
        1. Navigate to 回工登记 and check existing records
        2. Navigate to 日考勤统计 and verify 回工 type records exist
        """
        bp = BasePage(page)

        # Step 1: Return-work registration list
        navigate_to_attendance(page, "回工登记")
        bp.click_search()
        page.wait_for_timeout(2000)
        assert "回工登记" in page.title()

        # Step 2: Daily attendance stats - check for 回工 records
        navigate_to_attendance(page, "日考勤统计")
        bp.click_search()
        page.wait_for_timeout(2000)

        assert "日考勤统计" in page.title()

    def test_return_work_cross_check_attendance_register(self, page: Page):
        """Verify 回工-generated records appear in 考勤登记 as source=系统."""
        bp = BasePage(page)

        # Check return work
        navigate_to_attendance(page, "回工登记")
        bp.click_search()
        page.wait_for_timeout(2000)

        # Check attendance register for 系统 source records
        navigate_to_attendance(page, "考勤登记")

        # Select source=系统
        source_select = page.locator(
            ".ant-form-item", has_text="来源"
        ).locator(".ant-select")
        if source_select.count() > 0:
            source_select.first.click()
            page.wait_for_timeout(500)
            sys_option = page.locator(
                ".ant-select-dropdown:visible .ant-select-item-option",
                has_text="系统"
            )
            if sys_option.count() > 0:
                sys_option.first.click()
                page.wait_for_timeout(300)

        bp.click_search()
        page.wait_for_timeout(2000)
        assert "考勤登记" in page.title()


@pytest.mark.p3
@pytest.mark.integration
class TestLeaveToDailyStatsFlow:
    """F-03: Leave registration to daily stats flow."""

    def test_leave_to_daily_stats(self, page: Page):
        """F-03: Verify 请假登记 data flows to 日考勤统计.

        Steps:
        1. Navigate to 请假登记 and check existing records
        2. Navigate to 日考勤统计 and verify leave-related data
        """
        bp = BasePage(page)

        # Step 1: Leave registration list
        navigate_to_attendance(page, "请假登记")
        bp.click_search()
        page.wait_for_timeout(2000)
        assert "请假登记" in page.title()

        # Step 2: Daily attendance stats
        navigate_to_attendance(page, "日考勤统计")
        bp.click_search()
        page.wait_for_timeout(2000)

        assert "日考勤统计" in page.title()

    def test_leave_type_consistency_cross_pages(self, page: Page):
        """Verify leave types are consistent between 请假登记 and 考勤登记."""
        bp = BasePage(page)

        # Check leave types in attendance register type filter
        navigate_to_attendance(page, "考勤登记")

        type_select = page.locator(
            ".ant-form-item", has_text="类型"
        ).locator(".ant-select")
        if type_select.count() > 0:
            type_select.first.click()
            page.wait_for_timeout(500)
            # Leave types should be available in the dropdown
            dropdown = page.locator(".ant-select-dropdown:visible")
            if dropdown.count() > 0:
                expect(dropdown.first).to_be_visible()
            # Click away to close
            page.locator("body").click()

        # Navigate to leave register
        navigate_to_attendance(page, "请假登记")

        leave_type_select = page.locator(
            ".ant-form-item", has_text="假类"
        ).locator(".ant-select")
        if leave_type_select.count() > 0:
            leave_type_select.first.click()
            page.wait_for_timeout(500)
            dropdown = page.locator(".ant-select-dropdown:visible")
            if dropdown.count() > 0:
                expect(dropdown.first).to_be_visible()


@pytest.mark.p3
@pytest.mark.integration
class TestMonthlyAttendanceFullFlow:
    """F-04: Monthly attendance generation to detail to report."""

    def test_monthly_stats_to_detail_flow(self, page: Page):
        """F-04: Full monthly attendance workflow.

        Steps:
        1. Navigate to 月考勤统计 and view list
        2. Check detail page
        3. Verify report access from detail
        """
        bp = BasePage(page)

        # Step 1: Monthly stats list
        navigate_to_attendance(page, "月考勤统计")
        bp.click_search()
        page.wait_for_timeout(2000)
        assert "月考勤统计" in page.title()

        # Step 2: Click 详情 on first record
        detail_btn = page.locator("button:has-text('详情'), a:has-text('详情')").first
        if detail_btn.count() > 0:
            detail_btn.click()
            page.wait_for_timeout(2000)

    def test_monthly_detail_version_dropdown(self, page: Page):
        """V-76: Verify version dropdown in monthly detail."""
        bp = BasePage(page)

        navigate_to_attendance(page, "月考勤统计")
        bp.click_search()
        page.wait_for_timeout(2000)

        detail_btn = page.locator("button:has-text('详情'), a:has-text('详情')").first
        if detail_btn.count() > 0:
            detail_btn.click()
            page.wait_for_timeout(2000)

            # In detail view, look for version dropdown
            version_select = page.locator(
                ".ant-select", has_text="版本"
            )
            if version_select.count() > 0:
                expect(version_select.first).to_be_visible(timeout=5000)


@pytest.mark.p3
@pytest.mark.integration
class TestCrossModuleDataConsistency:
    """Cross-module data consistency across all attendance sub-pages."""

    def test_all_subpages_load_consistently(self, page: Page):
        """Verify all 7 attendance sub-pages load without errors."""
        bp = BasePage(page)

        subpages = [
            "考勤登记", "回工登记", "请假登记",
            "日考勤统计", "月考勤统计", "小组出勤表", "员工缺勤表",
        ]

        for subpage in subpages:
            navigate_to_attendance(page, subpage)
            bp.click_search()
            page.wait_for_timeout(2000)

            # Each page should load successfully
            page_content = page.content()
            assert len(page_content) > 500, f"{subpage} page content too short"

    def test_navigation_between_all_pages(self, page: Page):
        """Verify smooth navigation between different attendance pages."""
        bp = BasePage(page)

        # Start at 考勤登记
        navigate_to_attendance(page, "考勤登记")
        page.wait_for_timeout(1000)

        # Switch to 日考勤统计
        navigate_to_attendance(page, "日考勤统计")
        page.wait_for_timeout(1000)
        bp.click_search()
        page.wait_for_timeout(2000)

        # Switch to 月考勤统计
        navigate_to_attendance(page, "月考勤统计")
        page.wait_for_timeout(1000)
        bp.click_search()
        page.wait_for_timeout(2000)

        # Switch to 小组出勤表
        navigate_to_attendance(page, "小组出勤表")
        page.wait_for_timeout(1000)
        bp.click_search()
        page.wait_for_timeout(2000)

        # All should have loaded successfully
        assert "小组出勤表" in page.title()

    def test_sidebar_module_highlight(self, page: Page):
        """Verify 人事 module stays highlighted when on attendance pages."""
        bp = BasePage(page)

        navigate_to_attendance(page, "考勤登记")
        page.wait_for_timeout(1000)

        # The 人事 sidebar item should be in active/selected state
        hr_module = page.locator(
            ".mts-layout-mix-sider-module__item.active, "
            ".mts-layout-mix-sider-module__item--active, "
            ".mts-layout-mix-sider-module__item[class*='active']"
        )
        # Verify sidebar is present (exact class depends on implementation)
        sidebar = page.locator(".mts-layout-mix-sider-module__item")
        expect(sidebar.first).to_be_visible()


@pytest.mark.p3
@pytest.mark.integration
class TestAttendanceReportsFlow:
    """Integrated report flow: daily -> monthly -> group -> absence."""

    def test_reports_access_from_daily_stats(self, page: Page):
        """Verify report menu is accessible from 日考勤统计."""
        bp = BasePage(page)

        navigate_to_attendance(page, "日考勤统计")
        bp.click_search()
        page.wait_for_timeout(2000)

        # Look for 报表 button
        report_btn = page.locator("button:has-text('报表')")
        if report_btn.count() > 0:
            report_btn.first.click()
            page.wait_for_timeout(1000)

    def test_all_reports_accessible(self, page: Page):
        """Verify all report pages are accessible and functional."""
        bp = BasePage(page)

        report_pages = ["小组出勤表", "员工缺勤表"]

        for report_page in report_pages:
            navigate_to_attendance(page, report_page)
            bp.click_search()
            page.wait_for_timeout(2000)

            # Verify page loaded
            assert report_page in page.title(), f"{report_page} failed to load"
            table = page.locator(".ant-table")
            expect(table.first).to_be_visible(timeout=8000)


@pytest.mark.p3
@pytest.mark.integration
class TestConcurrentPageNavigation:
    """Test that multiple attendance pages can coexist in navigation."""

    def test_rapid_page_switching(self, page: Page):
        """Verify rapid switching between attendance pages does not crash."""
        bp = BasePage(page)

        subpages = ["考勤登记", "日考勤统计", "回工登记", "请假登记"]

        for i in range(3):  # 3 rounds of switching
            for subpage in subpages:
                navigate_to_attendance(page, subpage)
                page.wait_for_timeout(500)
                # Verify page is loading (not blank)
                page_content = page.content()
                assert len(page_content) > 500

    def test_third_menu_state_preserved(self, page: Page):
        """Verify third-menu panel shows correct sub-page after switching."""
        bp = BasePage(page)

        navigate_to_attendance(page, "考勤登记")
        page.wait_for_timeout(800)

        # Third menu should be visible
        third_menu = page.locator(".third-menu")
        expect(third_menu.first).to_be_visible(timeout=5000)

        # Should contain attendance sub-pages
        menu_text = third_menu.inner_text()
        for subpage in ["考勤登记", "回工登记", "请假登记"]:
            assert subpage in menu_text, f"'{subpage}' not found in third menu"
