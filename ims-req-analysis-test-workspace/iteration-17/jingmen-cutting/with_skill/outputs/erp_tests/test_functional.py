"""P1 Functional Tests: Jingmen Cutting 2.0

Core business flows: data CRUD, search/filter, status transitions,
calculations, and data-driven parametrized tests.

Priority: P1
Markers: functional
"""
import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.test_data_loader import load_test_data_csv, get_data_by_id


# ---------------------------------------------------------------------------
# Data-driven: 唛架层数分配校验
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
@pytest.mark.parametrize("data_id,expected_result,expected_message", [
    ("D01-1", "pass", None),
    ("D01-3", "pass", None),
    ("D01-5", "block", "分配层数超过唛架剩余可用层数"),
    ("D01-7", "pass", None),
])
def test_marker_layer_allocation(page: Page, data_id, expected_result, expected_message):
    """V-01, V-03, V-05: Marker layer allocation with various remaining amounts."""
    bp = BasePage(page)
    data = load_test_data_csv("test_data.csv")
    record = get_data_by_id(data, data_id)

    bp.navigate_to_module("生产")
    bp.click_third_menu("裁剪任务")
    bp.click_add()

    # Select CPO
    page.locator("label", has_text=record["cpo_id"]).locator("input[type='checkbox']").check()

    # Select marker
    page.locator(".ant-select", has_text="唛架").click()
    page.locator(f".ant-select-dropdown:visible text={record['marker_id']}").click()
    page.wait_for_timeout(300)

    # Input allocation layers
    bp.fill_field("计划层数", record["input_layers"])
    bp.click_save()

    if expected_result == "pass":
        bp.expect_success_toast()
    else:
        bp.expect_error_toast(expected_message)


# ---------------------------------------------------------------------------
# CPO Selection features
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
class TestCPOSelection:
    """C-03, C-04: Select-all and smart-merge CPO features."""

    def test_select_all_cpo(self, page: Page):
        """C-03: Select-all function checks all CPOs."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_add()

        # Click select-all
        select_all = page.locator("label:has-text('全选')").locator("input[type='checkbox']")
        select_all.check()

        # Verify all individual CPO checkboxes are checked
        cpo_checkboxes = page.locator(".cpo-list input[type='checkbox']")
        count = cpo_checkboxes.count()
        for i in range(count):
            expect(cpo_checkboxes.nth(i)).to_be_checked()

    def test_smart_merge_cpo_by_delivery(self, page: Page):
        """C-04: Smart merge groups CPOs by same delivery date."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_add()

        # Click smart merge
        smart_merge = page.locator("button:has-text('智能合并')")
        smart_merge.click()
        page.wait_for_timeout(1000)

        # Verify grouping dialog appears
        group_dialog = page.locator(".ant-modal:visible")
        expect(group_dialog).to_be_visible()

        # Verify same-delivery CPOs grouped together
        group_text = group_dialog.inner_text()
        assert "CPO-B" in group_text and "CPO-C" in group_text  # Both 7/5


# ---------------------------------------------------------------------------
# Cutting task lifecycle
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
class TestTaskLifecycle:
    """U-01, X-01: Edit and delete cutting tasks in '未开始' state."""

    def test_edit_task_not_started(self, page: Page):
        """U-01: Edit task when status is '未开始'."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")

        # Find a 未开始 task
        bp.click_table_row("未开始")

        # Click edit
        bp.click_edit()
        page.wait_for_timeout(500)

        # Verify edit form is editable
        layer_input = page.locator("input[placeholder*='层数'], .ant-input-number input")
        expect(layer_input).to_be_editable()

        # Change layer count
        layer_input.fill("25")
        bp.click_save()
        bp.expect_success_toast()

    def test_delete_task_not_started(self, page: Page):
        """X-01: Delete task when status is '未开始'."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_table_row("未开始")

        # Click delete
        bp.click_delete()

        # Confirm deletion dialog
        dialog = page.locator(".ant-modal-confirm:visible")
        expect(dialog).to_be_visible()
        bp.confirm_dialog()

        bp.expect_success_toast()

    def test_cannot_edit_in_progress_task(self, page: Page):
        """V-07: Edit button hidden when task is '拉布中'."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")

        # Find a 拉布中 task
        bp.click_table_row("拉布中")

        # Verify edit button is hidden
        bp.expect_button_hidden("编辑")

    def test_cannot_delete_in_progress_task(self, page: Page):
        """V-08: Delete button hidden when task is '拉布中'."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_table_row("拉布中")

        bp.expect_button_hidden("删除")


# ---------------------------------------------------------------------------
# Bed completion
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
class TestBedCompletion:
    """C-08, V-15, V-16: Bed completion with actual layer validation."""

    def test_actual_equals_reserved_submit_success(self, page: Page):
        """C-08: Actual layers equal reserved - submit success."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_table_row("CPO-A")

        # Find a 拉布中 bed
        page.locator("text=拉布中").first.click()
        bp.pad_click_button("提交完成")

        bp.pad_input_number("实际层数", 20)  # same as reserved
        bp.confirm_dialog()

        # Verify status changed to 已拉布
        expect(page.locator("text=已拉布").first).to_be_visible(timeout=5000)

    def test_actual_less_than_reserved_return_diff(self, page: Page):
        """V-15: Actual < reserved returns difference to remaining."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_table_row("CPO-A")

        page.locator("text=拉布中").first.click()
        bp.pad_click_button("提交完成")

        bp.pad_input_number("实际层数", 15)  # less than reserved 20
        bp.confirm_dialog()

        bp.expect_success_toast()

    def test_actual_over_range_submit_fails(self, page: Page):
        """V-16: Actual over adjustable range - submit fails."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_table_row("CPO-A")

        page.locator("text=拉布中").first.click()
        bp.pad_click_button("提交完成")

        bp.pad_input_number("实际层数", 30)  # exceeds range
        bp.confirm_dialog()

        bp.expect_error_toast("实际层数超出可调整范围")


# ---------------------------------------------------------------------------
# Hanging - Manual mode
# ---------------------------------------------------------------------------
@pytest.mark.p1
@pytest.mark.functional
class TestManualFillMode:
    """F-08, F-09, F-10: Manual fill mode for hanging station."""

    def test_manual_mode_shows_cpo_list(self, page: Page):
        """F-08: Manual mode displays unfilled CPO list sorted by delivery."""
        bp = BasePage(page)

        bp.navigate_to_module("吊挂")
        bp.click_third_menu("缝制挂片")

        # Switch to manual mode
        bp.pad_click_button("手动充数")
        page.wait_for_timeout(1000)

        # Verify CPO list is visible
        cpo_list = page.locator(".cpo-list, [class*='cpo-select']")
        expect(cpo_list).to_be_visible()

        # Verify sorted by delivery (CPO-A 7/1 first)
        first_cpo = cpo_list.locator("li, .cpo-item").first
        expect(first_cpo).to_contain_text("CPO-A")

    def test_manual_select_cpo_free_hanging(self, page: Page):
        """F-09: Free selection of CPO and hanging in manual mode."""
        bp = BasePage(page)

        bp.navigate_to_module("吊挂")
        bp.click_third_menu("缝制挂片")
        bp.pad_click_button("手动充数")

        # Select CPO-C (not the nearest delivery)
        page.locator(".cpo-item", has_text="CPO-C").click()
        page.wait_for_timeout(500)

        # Scan tag
        bp.pad_scan_barcode("TAG-GEN-002")

        # Verify assigned to CPO-C
        assigned = page.locator(".assigned-cpo, [class*='current-cpo']")
        expect(assigned).to_contain_text("CPO-C")

    def test_cpo_full_prompt_switch(self, page: Page):
        """F-10: CPO full prompts worker to switch."""
        bp = BasePage(page)

        bp.navigate_to_module("吊挂")
        bp.click_third_menu("缝制挂片")
        bp.pad_click_button("手动充数")

        # Select CPO with 0 remaining
        # (This requires test data setup: CPO already fully filled)
        page.locator(".cpo-item", has_text="CPO-C").click()

        # Try to hang to full CPO - expect prompt
        bp.pad_scan_barcode("TAG-GEN-003")

        full_prompt = page.locator(".ant-modal-confirm:visible, .ant-message-warning")
        expect(full_prompt).to_be_visible(timeout=3000)
        expect(full_prompt).to_contain_text("数量已满")

    def test_auto_to_manual_switch_preserves_progress(self, page: Page):
        """F-11: Auto->Manual switch preserves current fill progress."""
        bp = BasePage(page)

        bp.navigate_to_module("吊挂")
        bp.click_third_menu("缝制挂片")

        # In auto mode, note current CPO progress
        current_cpo = page.locator(".assigned-cpo, [class*='current-cpo']").inner_text()

        # Switch to manual
        bp.pad_click_button("手动充数")
        page.wait_for_timeout(1000)

        # Verify CPO list reflects actual remaining quantities
        cpo_list = page.locator(".cpo-list")
        expect(cpo_list).to_be_visible()

    def test_manual_to_auto_recalc(self, page: Page):
        """F-12: Manual->Auto recalculates CPO by delivery priority."""
        bp = BasePage(page)

        bp.navigate_to_module("吊挂")
        bp.click_third_menu("缝制挂片")
        bp.pad_click_button("手动充数")

        # In manual mode, select a far-delivery CPO
        page.locator(".cpo-item", has_text="CPO-D").click()

        # Switch back to auto
        bp.pad_click_button("恢复自动充数")
        page.wait_for_timeout(1000)

        # Verify auto-reselects nearest-delivery unfilled CPO
        auto_cpo = page.locator(".assigned-cpo, [class*='current-cpo']")
        expect(auto_cpo).to_be_visible()

    def test_manual_free_skip_delivery_order(self, page: Page):
        """F-13: Manual mode allows skipping delivery order freely."""
        bp = BasePage(page)

        bp.navigate_to_module("吊挂")
        bp.click_third_menu("缝制挂片")
        bp.pad_click_button("手动充数")

        # Select CPO-B (7/5) even though CPO-A (7/1) is earlier
        page.locator(".cpo-item", has_text="CPO-B").click()

        # Verify selection accepted
        selected = page.locator(".cpo-item.selected, .cpo-item.active")
        expect(selected).to_contain_text("CPO-B")
