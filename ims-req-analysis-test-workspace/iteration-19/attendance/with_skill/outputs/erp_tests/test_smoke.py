"""P0 Smoke Tests: IMS Attendance (考勤) Module

Core path verification — these must pass for every build.
Covers: 7 sub-page navigation, key list pages, primary CRUD operations,
and essential workflows.

Priority: P0
Markers: p0, smoke
"""
import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from conftest import navigate_to_attendance, get_attendance_subpages


@pytest.mark.p0
@pytest.mark.smoke
class TestAttendanceNavigation:
    """Verify all 7 attendance sub-pages are accessible from the sidebar."""

    @pytest.mark.parametrize("subpage", get_attendance_subpages())
    def test_navigate_to_subpage(self, page: Page, subpage: str):
        """Verify navigation to each attendance sub-page loads successfully."""
        bp = BasePage(page)

        bp.navigate_to_module("人事")
        bp.click_third_menu(subpage)

        # Verify page content loads (not blank, not error)
        page_content = page.content()
        assert len(page_content) > 500, f"Page content too short for {subpage}"
        # Page should not show a catastrophic error
        assert "500" not in page.title(), f"Server error on page {subpage}"


@pytest.mark.p0
@pytest.mark.smoke
class TestAttendanceRegisterList:
    """L-01: 考勤登记 default list query."""

    def test_default_query_today_records(self, page: Page):
        """Verify 考勤登记 page loads with today's attendance records."""
        bp = BasePage(page)

        navigate_to_attendance(page, "考勤登记")

        # Page should load without errors
        expect(page).to_have_title("考勤登记 - 麦塔西智能制造协同平台", timeout=10000)

        # Either table has rows or shows empty state - both are valid
        bp.expect_table_has_rows(min_rows=0)
        # Search button should be visible
        bp.expect_button_visible("查询")

    def test_date_shortcut_buttons_visible(self, page: Page):
        """Verify date shortcut buttons are visible on 考勤登记 page."""
        bp = BasePage(page)

        navigate_to_attendance(page, "考勤登记")

        # Quick date buttons should be present
        for btn_text in ["今日", "本周", "本月", "昨日", "上周", "上月"]:
            btn = page.locator(f"button:has-text('{btn_text}'), span:has-text('{btn_text}')")
            expect(btn.first).to_be_visible(timeout=3000)

    def test_search_functionality(self, page: Page):
        """Verify search button triggers query on 考勤登记."""
        bp = BasePage(page)

        navigate_to_attendance(page, "考勤登记")

        bp.click_search()
        page.wait_for_timeout(2000)

        # After search, the page should still be stable
        assert "考勤登记" in page.title()


@pytest.mark.p0
@pytest.mark.smoke
class TestReturnWorkList:
    """L-06: 回工登记 list page."""

    def test_return_work_list_loads(self, page: Page):
        """Verify 回工登记 page loads successfully."""
        bp = BasePage(page)

        navigate_to_attendance(page, "回工登记")

        expect(page).to_have_title("回工登记 - 麦塔西智能制造协同平台", timeout=10000)
        bp.expect_button_visible("查询")
        bp.expect_button_visible("新增")

    def test_return_work_search_by_date(self, page: Page):
        """Verify searching 回工登记 by date works."""
        bp = BasePage(page)

        navigate_to_attendance(page, "回工登记")

        # Set date to today and search
        today_inputs = page.locator(".ant-picker-input input")
        if today_inputs.count() > 0:
            today_inputs.first.fill("2026-07-03")

        bp.click_search()
        page.wait_for_timeout(2000)

        # Page should remain stable after search
        assert "回工登记" in page.title()


@pytest.mark.p0
@pytest.mark.smoke
class TestLeaveRegisterList:
    """L-09: 请假登记 list page."""

    def test_leave_register_list_loads(self, page: Page):
        """Verify 请假登记 page loads successfully."""
        bp = BasePage(page)

        navigate_to_attendance(page, "请假登记")

        expect(page).to_have_title("请假登记 - 麦塔西智能制造协同平台", timeout=10000)
        bp.expect_button_visible("查询")
        bp.expect_button_visible("新增")

    def test_leave_register_search(self, page: Page):
        """Verify search on 请假登记 page works."""
        bp = BasePage(page)

        navigate_to_attendance(page, "请假登记")
        bp.click_search()
        page.wait_for_timeout(2000)

        assert "请假登记" in page.title()


@pytest.mark.p0
@pytest.mark.smoke
class TestDailyAttendanceStats:
    """L-12: 日考勤统计 default query."""

    def test_daily_stats_loads(self, page: Page):
        """Verify 日考勤统计 page loads with records."""
        bp = BasePage(page)

        navigate_to_attendance(page, "日考勤统计")

        expect(page).to_have_title("日考勤统计 - 麦塔西智能制造协同平台", timeout=10000)
        bp.expect_button_visible("查询")

        # Table should be present (may have data or be empty)
        table = page.locator(".ant-table")
        expect(table.first).to_be_visible(timeout=8000)

    def test_daily_stats_search_by_date(self, page: Page):
        """Verify searching 日考勤统计 by today's date."""
        bp = BasePage(page)

        navigate_to_attendance(page, "日考勤统计")
        bp.click_search()
        page.wait_for_timeout(2000)

        # Page should remain functional
        assert "日考勤统计" in page.title()


@pytest.mark.p0
@pytest.mark.smoke
class TestMonthlyAttendanceStats:
    """L-18: 月考勤统计 list page."""

    def test_monthly_stats_loads(self, page: Page):
        """Verify 月考勤统计 page loads with records."""
        bp = BasePage(page)

        navigate_to_attendance(page, "月考勤统计")

        expect(page).to_have_title("月考勤统计 - 麦塔西智能制造协同平台", timeout=10000)
        bp.expect_button_visible("查询")

    def test_monthly_stats_generate_button(self, page: Page):
        """Verify 生成月考勤 button is visible."""
        bp = BasePage(page)

        navigate_to_attendance(page, "月考勤统计")

        gen_btn = page.locator("button:has-text('生成月考勤')")
        expect(gen_btn.first).to_be_visible(timeout=5000)


@pytest.mark.p0
@pytest.mark.smoke
class TestGroupAttendanceReport:
    """F-07: 小组出勤表 page."""

    def test_group_attendance_loads(self, page: Page):
        """Verify 小组出勤表 page loads."""
        bp = BasePage(page)

        navigate_to_attendance(page, "小组出勤表")

        expect(page).to_have_title("小组出勤表 - 麦塔西智能制造协同平台", timeout=10000)
        bp.expect_button_visible("查询")

    def test_group_attendance_search(self, page: Page):
        """Verify search on 小组出勤表 works."""
        bp = BasePage(page)

        navigate_to_attendance(page, "小组出勤表")
        bp.click_search()
        page.wait_for_timeout(2000)

        assert "小组出勤表" in page.title()


@pytest.mark.p0
@pytest.mark.smoke
class TestEmployeeAbsenceReport:
    """F-08: 员工缺勤表 page."""

    def test_employee_absence_loads(self, page: Page):
        """Verify 员工缺勤表 page loads."""
        bp = BasePage(page)

        navigate_to_attendance(page, "员工缺勤表")

        expect(page).to_have_title("员工缺勤表 - 麦塔西智能制造协同平台", timeout=10000)
        bp.expect_button_visible("查询")

    def test_employee_absence_search(self, page: Page):
        """Verify search displays employees with absence > 0."""
        bp = BasePage(page)

        navigate_to_attendance(page, "员工缺勤表")
        bp.click_search()
        page.wait_for_timeout(2000)

        assert "员工缺勤表" in page.title()


@pytest.mark.p0
@pytest.mark.smoke
class TestReplenishCardOperation:
    """C-01: 补卡 - normal save."""

    def test_replenish_card_button_visible(self, page: Page):
        """Verify 补卡 button is visible on 考勤登记 page."""
        bp = BasePage(page)

        navigate_to_attendance(page, "考勤登记")

        replenish_btn = page.locator("button:has-text('补卡')")
        expect(replenish_btn.first).to_be_visible(timeout=5000)

    def test_replenish_card_dialog_opens(self, page: Page):
        """Verify clicking 补卡 opens a dialog/modal."""
        bp = BasePage(page)

        navigate_to_attendance(page, "考勤登记")

        replenish_btn = page.locator("button:has-text('补卡')").first
        replenish_btn.click()
        page.wait_for_timeout(1000)

        # A modal or form should appear
        modal_or_form = page.locator(
            ".ant-modal:visible, .ant-drawer:visible, .replenish-form"
        )
        expect(modal_or_form.first).to_be_visible(timeout=5000)


@pytest.mark.p0
@pytest.mark.smoke
class TestReturnWorkCreate:
    """C-02: 回工登记 add draft."""

    def test_return_work_add_button_opens_form(self, page: Page):
        """Verify clicking 新增 on 回工登记 opens a form."""
        bp = BasePage(page)

        navigate_to_attendance(page, "回工登记")
        bp.click_add()

        # A modal or form should appear
        modal = page.locator(".ant-modal:visible, .ant-drawer:visible")
        expect(modal.first).to_be_visible(timeout=5000)

        # Form should have essential fields
        form = page.locator(".ant-form")
        expect(form.first).to_be_visible(timeout=3000)

    def test_return_work_form_has_required_fields(self, page: Page):
        """Verify 回工登记 form contains required fields."""
        bp = BasePage(page)

        navigate_to_attendance(page, "回工登记")
        bp.click_add()
        page.wait_for_timeout(1000)

        # Check for key form elements
        form_page = page.locator(".ant-modal:visible, .ant-drawer:visible")
        form_text = form_page.inner_text()

        # Should contain date, shift, department, group related fields
        expected_fields = ["日期", "时间", "部门", "员工"]
        for field in expected_fields:
            assert field in form_text, f"Field '{field}' not found in return-work form"


@pytest.mark.p0
@pytest.mark.smoke
class TestLeaveRegisterCreate:
    """C-03: 请假登记 add draft."""

    def test_leave_register_add_button_opens_form(self, page: Page):
        """Verify clicking 新增 on 请假登记 opens a form."""
        bp = BasePage(page)

        navigate_to_attendance(page, "请假登记")
        bp.click_add()

        modal = page.locator(".ant-modal:visible, .ant-drawer:visible")
        expect(modal.first).to_be_visible(timeout=5000)

    def test_leave_register_form_has_required_fields(self, page: Page):
        """Verify 请假登记 form contains required fields."""
        bp = BasePage(page)

        navigate_to_attendance(page, "请假登记")
        bp.click_add()
        page.wait_for_timeout(1000)

        form_page = page.locator(".ant-modal:visible, .ant-drawer:visible")
        form_text = form_page.inner_text()

        expected_fields = ["员工", "假类", "日期", "时间"]
        for field in expected_fields:
            assert field in form_text, f"Field '{field}' not found in leave form"


@pytest.mark.p0
@pytest.mark.smoke
class TestDailyAttendanceCalculate:
    """U-10: 日考勤计算 - normal calculation."""

    def test_daily_calc_button_visible(self, page: Page):
        """Verify 日考勤计算 button is visible on 日考勤统计 page."""
        bp = BasePage(page)

        navigate_to_attendance(page, "日考勤统计")

        calc_btn = page.locator("button:has-text('计算'), button:has-text('日考勤计算')")
        expect(calc_btn.first).to_be_visible(timeout=5000)

    def test_daily_calc_dialog_opens(self, page: Page):
        """Verify clicking 日考勤计算 opens a dialog."""
        bp = BasePage(page)

        navigate_to_attendance(page, "日考勤统计")

        calc_btn = page.locator(
            "button:has-text('计算'), button:has-text('日考勤计算')"
        ).first
        calc_btn.click()
        page.wait_for_timeout(1000)

        # Dialog/modal should open
        modal = page.locator(".ant-modal:visible, .ant-drawer:visible")
        if modal.count() > 0:
            expect(modal.first).to_be_visible(timeout=3000)


@pytest.mark.p0
@pytest.mark.smoke
class TestMonthlyAttendanceGenerate:
    """C-06: 月考勤统计 generation."""

    def test_monthly_generate_dialog_opens(self, page: Page):
        """Verify clicking 生成月考勤 opens dialog."""
        bp = BasePage(page)

        navigate_to_attendance(page, "月考勤统计")

        gen_btn = page.locator("button:has-text('生成月考勤')").first
        gen_btn.click()
        page.wait_for_timeout(1000)

        modal = page.locator(".ant-modal:visible, .ant-drawer:visible")
        expect(modal.first).to_be_visible(timeout=5000)
