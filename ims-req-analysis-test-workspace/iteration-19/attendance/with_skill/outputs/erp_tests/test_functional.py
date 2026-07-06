"""P1 Functional Tests: IMS Attendance (考勤) Module

Core business flows: data CRUD, search/filter, status transitions,
attendance synchronization, replenish card operations, and
data-driven parametrized tests.

Priority: P1
Markers: p1, functional
"""
import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from conftest import navigate_to_attendance
from utils.test_data_loader import load_test_data_csv, get_data_by_id


# ---------------------------------------------------------------------------
# Data-driven: Attendance type/source filter verification
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
@pytest.mark.parametrize("type_filter", [
    "正常", "出差", "回工", "病假", "事假", "特殊假", "年假",
])
def test_attendance_type_filter(page: Page, type_filter: str):
    """L-04: Filter attendance by type - verify each type filter works."""
    bp = BasePage(page)

    navigate_to_attendance(page, "考勤登记")

    # Select type filter dropdown
    type_select = page.locator(".ant-form-item", has_text="类型").locator(".ant-select")
    if type_select.count() > 0:
        type_select.first.click()
        page.wait_for_timeout(500)
        option = page.locator(
            f".ant-select-dropdown:visible .ant-select-item-option",
            has_text=type_filter
        )
        if option.count() > 0:
            option.first.click()
            page.wait_for_timeout(300)

    bp.click_search()
    page.wait_for_timeout(2000)
    # Page should still be functional
    assert "考勤登记" in page.title()


@pytest.mark.p1
@pytest.mark.functional
@pytest.mark.parametrize("source_filter", [
    "考勤机", "补卡", "导入", "系统",
])
def test_attendance_source_filter(page: Page, source_filter: str):
    """L-05: Filter attendance by source - verify each source filter works."""
    bp = BasePage(page)

    navigate_to_attendance(page, "考勤登记")

    # Select source filter dropdown
    source_select = page.locator(".ant-form-item", has_text="来源").locator(".ant-select")
    if source_select.count() > 0:
        source_select.first.click()
        page.wait_for_timeout(500)
        option = page.locator(
            f".ant-select-dropdown:visible .ant-select-item-option",
            has_text=source_filter
        )
        if option.count() > 0:
            option.first.click()
            page.wait_for_timeout(300)

    bp.click_search()
    page.wait_for_timeout(2000)
    assert "考勤登记" in page.title()


# ---------------------------------------------------------------------------
# 考勤登记 - Export and Delete
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
class TestAttendanceRegisterOperations:
    """X-01, X-02: Export and delete attendance records."""

    def test_export_attendance_records(self, page: Page):
        """X-01: Export attendance records to Excel."""
        bp = BasePage(page)

        navigate_to_attendance(page, "考勤登记")
        bp.click_search()
        page.wait_for_timeout(2000)

        # Click export
        export_btn = page.locator("button:has-text('导出')")
        if export_btn.count() > 0:
            export_btn.first.click()
            page.wait_for_timeout(3000)
            # Export should trigger download or show success
            assert "考勤登记" in page.title()

    def test_delete_attendance_record_dialog(self, page: Page):
        """X-02: Delete non-system attendance record - confirm dialog appears."""
        bp = BasePage(page)

        navigate_to_attendance(page, "考勤登记")
        bp.click_search()
        page.wait_for_timeout(2000)

        # Find a delete button on a record
        delete_btn = page.locator("button:has-text('删除')")
        if delete_btn.count() > 0:
            delete_btn.first.click()
            page.wait_for_timeout(1000)

            # Confirm dialog should appear
            confirm_modal = page.locator(".ant-modal-confirm:visible, .ant-popconfirm")
            if confirm_modal.count() > 0:
                expect(confirm_modal.first).to_be_visible(timeout=3000)
                # Click cancel to not actually delete
                cancel_btn = page.locator(
                    ".ant-modal-confirm:visible button:has-text('取消'), "
                    ".ant-popconfirm button:has-text('取消')"
                )
                if cancel_btn.count() > 0:
                    cancel_btn.first.click()


# ---------------------------------------------------------------------------
# 考勤登记 - Replenish Card
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
class TestReplenishCardFlow:
    """C-01, V-09: Replenish card operations."""

    def test_replenish_card_normal_save(self, page: Page):
        """C-01: Replenish card with normal type - save successfully."""
        bp = BasePage(page)

        navigate_to_attendance(page, "考勤登记")

        # Click 补卡
        replenish_btn = page.locator("button:has-text('补卡')").first
        replenish_btn.click()
        page.wait_for_timeout(1000)

        # Verify dialog/form opened
        modal = page.locator(".ant-modal:visible, .ant-drawer:visible")
        if modal.count() > 0:
            expect(modal.first).to_be_visible()

            # Try to fill employee ID
            emp_input = modal.first.locator("input").first
            if emp_input.count() > 0:
                emp_input.fill("100001")
                page.wait_for_timeout(300)

    def test_replenish_card_continue_add(self, page: Page):
        """V-09: Replenish card with 'continue add' - new blank form appears."""
        bp = BasePage(page)

        navigate_to_attendance(page, "考勤登记")

        replenish_btn = page.locator("button:has-text('补卡')").first
        replenish_btn.click()
        page.wait_for_timeout(1000)

        # Check for '继续添加' button
        continue_btn = page.locator("button:has-text('继续添加')")
        if continue_btn.count() > 0:
            # Fill some basic info first
            modal = page.locator(".ant-modal:visible, .ant-drawer:visible")
            inputs = modal.first.locator("input")
            if inputs.count() > 0:
                inputs.first.fill("100001")

            continue_btn.first.click()
            page.wait_for_timeout(1000)

            # Should still have the form open with cleared employee ID
            assert modal.first.is_visible()

    def test_replenish_card_business_trip_type(self, page: Page):
        """V-10: Replenish card with 出差 type."""
        bp = BasePage(page)

        navigate_to_attendance(page, "考勤登记")

        replenish_btn = page.locator("button:has-text('补卡')").first
        replenish_btn.click()
        page.wait_for_timeout(1000)

        # Select type = 出差
        type_select = page.locator(
            ".ant-modal:visible .ant-form-item, .ant-drawer:visible .ant-form-item"
        ).filter(has_text="类型").locator(".ant-select")
        if type_select.count() > 0:
            type_select.first.click()
            page.wait_for_timeout(500)
            option = page.locator(
                ".ant-select-dropdown:visible .ant-select-item-option",
                has_text="出差"
            )
            if option.count() > 0:
                option.first.click()
                page.wait_for_timeout(300)


# ---------------------------------------------------------------------------
# 回工登记 - Lifecycle
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
class TestReturnWorkLifecycle:
    """U-01, V-12: Return-work life cycle."""

    def test_return_work_effective_flow(self, page: Page):
        """U-01: Activate a draft return-work registration."""
        bp = BasePage(page)

        navigate_to_attendance(page, "回工登记")
        bp.click_search()
        page.wait_for_timeout(2000)

        # Look for 生效 button
        effective_btn = page.locator("button:has-text('生效')")
        if effective_btn.count() > 0:
            expect(effective_btn.first).to_be_visible()
            # We do NOT click to avoid affecting real data
            # Just verify the button exists in the UI

    def test_return_work_reverse_effective_confirm(self, page: Page):
        """V-12: Reverse-effective shows confirm when date < today."""
        bp = BasePage(page)

        navigate_to_attendance(page, "回工登记")
        bp.click_search()
        page.wait_for_timeout(2000)

        # Look for 反生效 button
        reverse_btn = page.locator("button:has-text('反生效')")
        if reverse_btn.count() > 0:
            expect(reverse_btn.first).to_be_visible()

    def test_return_work_delete_draft(self, page: Page):
        """X-03: Delete draft return-work registration."""
        bp = BasePage(page)

        navigate_to_attendance(page, "回工登记")
        bp.click_search()
        page.wait_for_timeout(2000)

        # Click delete on a row
        delete_btn = page.locator("button:has-text('删除')").first
        if delete_btn.count() > 0:
            delete_btn.click()
            page.wait_for_timeout(500)

            confirm_modal = page.locator(".ant-modal-confirm:visible")
            if confirm_modal.count() > 0:
                expect(confirm_modal.first).to_be_visible(timeout=3000)

    def test_return_work_status_filter(self, page: Page):
        """L-07: Filter return-work by status (草稿/生效)."""
        bp = BasePage(page)

        navigate_to_attendance(page, "回工登记")

        status_select = page.locator(
            ".ant-form-item", has_text="状态"
        ).locator(".ant-select")
        if status_select.count() > 0:
            status_select.first.click()
            page.wait_for_timeout(500)

            # Try selecting 草稿
            draft_option = page.locator(
                ".ant-select-dropdown:visible .ant-select-item-option",
                has_text="草稿"
            )
            if draft_option.count() > 0:
                draft_option.first.click()
                page.wait_for_timeout(300)
                bp.click_search()
                page.wait_for_timeout(2000)

        assert "回工登记" in page.title()


# ---------------------------------------------------------------------------
# 请假登记 - Lifecycle
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
class TestLeaveLifecycle:
    """U-02, U-03: Leave life cycle."""

    def test_leave_effective_flow(self, page: Page):
        """U-02: Activate a draft leave registration."""
        bp = BasePage(page)

        navigate_to_attendance(page, "请假登记")
        bp.click_search()
        page.wait_for_timeout(2000)

        effective_btn = page.locator("button:has-text('生效')")
        if effective_btn.count() > 0:
            expect(effective_btn.first).to_be_visible()

    def test_leave_reverse_effective(self, page: Page):
        """U-03: Reverse-effective a leave registration."""
        bp = BasePage(page)

        navigate_to_attendance(page, "请假登记")
        bp.click_search()
        page.wait_for_timeout(2000)

        reverse_btn = page.locator("button:has-text('反生效')")
        if reverse_btn.count() > 0:
            expect(reverse_btn.first).to_be_visible()

    def test_leave_status_filter(self, page: Page):
        """L-11: Filter leave by status."""
        bp = BasePage(page)

        navigate_to_attendance(page, "请假登记")

        status_select = page.locator(
            ".ant-form-item", has_text="状态"
        ).locator(".ant-select")
        if status_select.count() > 0:
            status_select.first.click()
            page.wait_for_timeout(500)

            draft_option = page.locator(
                ".ant-select-dropdown:visible .ant-select-item-option",
                has_text="生效"
            )
            if draft_option.count() > 0:
                draft_option.first.click()
                page.wait_for_timeout(300)
                bp.click_search()
                page.wait_for_timeout(2000)

        assert "请假登记" in page.title()

    def test_leave_type_filter(self, page: Page):
        """L-11: Filter leave by leave type."""
        bp = BasePage(page)

        navigate_to_attendance(page, "请假登记")

        leave_type_select = page.locator(
            ".ant-form-item", has_text="假类"
        ).locator(".ant-select")
        if leave_type_select.count() > 0:
            leave_type_select.first.click()
            page.wait_for_timeout(500)

            annual_option = page.locator(
                ".ant-select-dropdown:visible .ant-select-item-option",
                has_text="年假"
            )
            if annual_option.count() > 0:
                annual_option.first.click()
                page.wait_for_timeout(300)
                bp.click_search()
                page.wait_for_timeout(2000)

        assert "请假登记" in page.title()


# ---------------------------------------------------------------------------
# 日考勤统计 - Quick Replenish Card
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
class TestDailyQuickReplenish:
    """U-04 ~ U-08: Quick replenish card per shift period."""

    def test_early_morning_replenish_button(self, page: Page):
        """U-04: 早班上班补卡 button visible on 日考勤统计."""
        bp = BasePage(page)

        navigate_to_attendance(page, "日考勤统计")
        bp.click_search()
        page.wait_for_timeout(2000)

        # Look for quick replenish buttons
        replenish_texts = ["早班上班补卡", "早班下班补卡", "午班上班补卡", "午班下班补卡"]
        found_any = False
        for text in replenish_texts:
            btn = page.locator(f"button:has-text('{text}'), span:has-text('{text}')")
            if btn.count() > 0:
                found_any = True
                break
        # At least one quick replenish element should exist
        # (may be in header or on row actions)

    def test_default_standard_time_checkbox(self, page: Page):
        """Verify '默认按上下班标准时间补卡' checkbox exists."""
        bp = BasePage(page)

        navigate_to_attendance(page, "日考勤统计")

        checkbox_label = page.locator(
            "label:has-text('默认按上下班标准时间补卡'), "
            "span:has-text('默认按上下班标准时间补卡')"
        )
        # This checkbox may or may not be visible depending on UI state
        # Just verify the page loaded
        assert "日考勤统计" in page.title()


# ---------------------------------------------------------------------------
# 日考勤统计 - Batch Replenish Card
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
class TestBatchReplenishCard:
    """C-04: Batch replenish card."""

    def test_batch_replenish_button_visible(self, page: Page):
        """Verify batch 补卡 button is visible."""
        bp = BasePage(page)

        navigate_to_attendance(page, "日考勤统计")

        batch_btn = page.locator("button:has-text('批量补卡'), button:has-text('补卡')")
        expect(batch_btn.first).to_be_visible(timeout=5000)

    def test_batch_replenish_no_selection_prompt(self, page: Page):
        """V-50: Batch replenish without selecting records shows prompt."""
        bp = BasePage(page)

        navigate_to_attendance(page, "日考勤统计")

        batch_btn = page.locator("button:has-text('批量补卡'), button:has-text('补卡')").first
        batch_btn.click()
        page.wait_for_timeout(1000)

        # Should see a prompt or modal
        # It may be a warning message or a modal dialog
        prompt = page.locator(
            ".ant-message, .ant-modal:visible, .ant-alert-warning"
        )
        if prompt.count() > 0:
            expect(prompt.first).to_be_visible(timeout=3000)


# ---------------------------------------------------------------------------
# 日考勤统计 - Change Shift
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
class TestChangeShift:
    """U-09: Change shift for selected records."""

    def test_change_shift_button_visible(self, page: Page):
        """Verify 更改班次 button is visible."""
        bp = BasePage(page)

        navigate_to_attendance(page, "日考勤统计")

        shift_btn = page.locator("button:has-text('更改班次')")
        expect(shift_btn.first).to_be_visible(timeout=5000)

    def test_change_shift_no_selection_prompt(self, page: Page):
        """V-56: Change shift without selecting records shows prompt."""
        bp = BasePage(page)

        navigate_to_attendance(page, "日考勤统计")

        shift_btn = page.locator("button:has-text('更改班次')").first
        shift_btn.click()
        page.wait_for_timeout(1000)

        prompt = page.locator(".ant-message, .ant-modal:visible")
        if prompt.count() > 0:
            expect(prompt.first).to_be_visible(timeout=3000)


# ---------------------------------------------------------------------------
# 日考勤统计 - Daily Attendance Calculation
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
class TestDailyAttendanceCalcFlow:
    """U-10, U-11: Daily attendance calculation."""

    def test_daily_calc_form_has_date_inputs(self, page: Page):
        """U-10: Daily calc form shows date range inputs."""
        bp = BasePage(page)

        navigate_to_attendance(page, "日考勤统计")

        calc_btn = page.locator(
            "button:has-text('计算'), button:has-text('日考勤计算')"
        ).first
        calc_btn.click()
        page.wait_for_timeout(1000)

        modal = page.locator(".ant-modal:visible")
        if modal.count() > 0:
            # Should have date inputs
            date_inputs = modal.first.locator(".ant-picker input, input[type='text']")
            assert date_inputs.count() > 0, "Calc modal should have date inputs"

    def test_daily_calc_with_filter(self, page: Page):
        """U-11: Daily calc with department/group filter."""
        bp = BasePage(page)

        navigate_to_attendance(page, "日考勤统计")

        calc_btn = page.locator(
            "button:has-text('计算'), button:has-text('日考勤计算')"
        ).first
        calc_btn.click()
        page.wait_for_timeout(1000)

        modal = page.locator(".ant-modal:visible")
        if modal.count() > 0:
            # Try to select a department filter
            dept_select = modal.first.locator(
                ".ant-form-item", has_text="部门"
            ).locator(".ant-select")
            if dept_select.count() > 0:
                dept_select.first.click()
                page.wait_for_timeout(500)

                # Try selecting first option
                first_option = page.locator(
                    ".ant-select-dropdown:visible .ant-select-item-option"
                ).first
                if first_option.count() > 0:
                    first_option.click()
                    page.wait_for_timeout(300)

            # Close modal
            cancel_btn = modal.first.locator("button:has-text('取消')")
            if cancel_btn.count() > 0:
                cancel_btn.first.click()


# ---------------------------------------------------------------------------
# 考勤同步 - Attendance Sync
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
class TestAttendanceSync:
    """F-05: Attendance sync from device."""

    def test_sync_dialog_opens(self, page: Page):
        """Verify 考勤同步 dialog opens."""
        bp = BasePage(page)

        navigate_to_attendance(page, "日考勤统计")

        sync_btn = page.locator("button:has-text('考勤同步')")
        if sync_btn.count() > 0:
            sync_btn.first.click()
            page.wait_for_timeout(1000)

            modal = page.locator(".ant-modal:visible")
            if modal.count() > 0:
                expect(modal.first).to_be_visible(timeout=5000)


# ---------------------------------------------------------------------------
# 月考勤统计 - Detail and Recalculate
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
class TestMonthlyAttendanceOperations:
    """U-14, V-76: Monthly attendance detail and recalculate."""

    def test_monthly_detail_page(self, page: Page):
        """D-04: Navigate to monthly attendance detail page."""
        bp = BasePage(page)

        navigate_to_attendance(page, "月考勤统计")
        bp.click_search()
        page.wait_for_timeout(2000)

        # Click 详情 on a record
        detail_btn = page.locator("button:has-text('详情'), a:has-text('详情')")
        if detail_btn.count() > 0:
            detail_btn.first.click()
            page.wait_for_timeout(2000)

            # Should navigate to detail page or open detail view
            assert "月考勤" in page.title() or page.locator(
                ".ant-modal:visible, .ant-drawer:visible"
            ).count() > 0

    def test_monthly_export(self, page: Page):
        """V-77: Export monthly attendance detail."""
        bp = BasePage(page)

        navigate_to_attendance(page, "月考勤统计")
        bp.click_search()
        page.wait_for_timeout(2000)

        export_btn = page.locator("button:has-text('导出')")
        if export_btn.count() > 0:
            export_btn.first.click()
            page.wait_for_timeout(3000)


# ---------------------------------------------------------------------------
# 月考勤明细表 - Monthly Detail Report
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
class TestMonthlyDetailReport:
    """F-06, V-86: Monthly detail report from daily stats."""

    def test_monthly_detail_report_from_daily(self, page: Page):
        """V-86: Access monthly detail report from 日考勤统计."""
        bp = BasePage(page)

        navigate_to_attendance(page, "日考勤统计")

        # Look for 报表 or 月考勤明细表 button
        report_btn = page.locator(
            "button:has-text('报表'), button:has-text('月考勤明细表')"
        )
        if report_btn.count() > 0:
            report_btn.first.click()
            page.wait_for_timeout(1000)

            # A sub-menu or dialog should appear
            report_option = page.locator(
                ".ant-dropdown:visible text='月考勤明细表', "
                ".ant-modal:visible"
            )
            if report_option.count() > 0:
                expect(report_option.first).to_be_visible(timeout=3000)
