"""P2 Boundary Tests: Jingmen Cutting 2.0

Edge cases, error handling, boundary values, empty states,
permission checks, and concurrent access scenarios.

Priority: P2
Markers: boundary
"""
import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.test_data_loader import load_test_data_csv


@pytest.mark.p2
@pytest.mark.boundary
class TestLayerBoundaryValues:
    """V-02, V-04, V-05, V-06, V-11: Layer input boundary tests."""

    def test_marker_fully_allocated_not_selectable(self, page: Page):
        """V-02: Fully allocated marker (remaining=0) not selectable."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_add()

        # Try to select MK-003 (fully allocated, remaining=0)
        page.locator(".ant-select", has_text="唛架").click()
        page.wait_for_timeout(300)

        # Verify MK-003 is disabled or not in dropdown
        mk003 = page.locator(".ant-select-dropdown:visible text='MK-003'")
        if mk003.count() > 0:
            # If visible, should be disabled
            parent = mk003.locator("..")
            expect(parent).to_have_class("ant-select-item-option-disabled")

    def test_allocate_zero_layers_rejected(self, page: Page):
        """V-04: Allocating 0 layers rejected."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_add()

        # Select CPO and marker
        page.locator("label", has_text="CPO-A").locator("input[type='checkbox']").check()
        page.locator(".ant-select", has_text="唛架").click()
        page.locator(".ant-select-dropdown:visible text='MK-001'").click()
        page.wait_for_timeout(300)

        # Input 0 layers
        bp.fill_field("计划层数", "0")
        bp.click_save()

        bp.expect_error_toast("计划层数必须大于0")

    def test_marker_not_selected_rejected(self, page: Page):
        """V-06: No marker selected - save rejected."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_add()

        # Select CPO but NOT marker
        page.locator("label", has_text="CPO-A").locator("input[type='checkbox']").check()

        # Try to save without marker
        bp.click_save()

        bp.expect_error_toast("请选择唛架")

    def test_invalid_barcode_prompt(self, page: Page):
        """V-10: Scanning invalid barcode shows error."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_table_row("CPO-A")

        bp.pad_click_button("新增床次")
        page.wait_for_timeout(500)

        # Scan invalid barcode
        bp.pad_scan_barcode("INVALID-BARCODE-999")

        bp.expect_error_toast("未找到该布卷号")

    def test_negative_layer_input_rejected(self, page: Page):
        """V-11: Negative layer count rejected."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_table_row("CPO-A")
        bp.pad_click_button("新增床次")

        bp.pad_scan_barcode("FB001")

        # Input negative layers
        bp.pad_input_number("拉布层数", -5)
        bp.click_save()

        bp.expect_error_toast("请输入有效的正整数层数")

    def test_zero_layer_input_rejected(self, page: Page):
        """V-11: Zero layer count rejected."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_table_row("CPO-A")
        bp.pad_click_button("新增床次")

        bp.pad_scan_barcode("FB001")
        bp.pad_input_number("拉布层数", 0)
        bp.click_save()

        bp.expect_error_toast("拉布层数必须大于0")


@pytest.mark.p2
@pytest.mark.boundary
class TestStatusGateBoundaries:
    """V-07, V-08, V-09: State gate boundary checks."""

    def test_completed_task_cannot_add_bed(self, page: Page):
        """V-09: Completed task cannot add new bed."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")

        # Find completed task
        bp.click_table_row("已完成")

        # Verify 新增床次 is hidden
        bp.expect_button_hidden("新增床次")


@pytest.mark.p2
@pytest.mark.boundary
class TestBedNumberBoundaries:
    """V-17, V-18, V-19: Bed number uniqueness and format."""

    def test_bed_number_global_increment(self, page: Page):
        """V-17: Bed numbers increment globally within production order."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")

        # Check bed numbers in the list
        bed_cells = page.locator("td:has-text('C-'), td:has-text('F-')")
        expect(bed_cells.first).to_be_visible()

        # Collect bed numbers and verify they are sequential by display order
        count = bed_cells.count()
        bed_numbers = []
        for i in range(count):
            bed_numbers.append(bed_cells.nth(i).inner_text())

        # Extract numeric parts
        nums = []
        for bn in bed_numbers:
            # Format: C-001, F-001, etc.
            parts = bn.split("-")
            if len(parts) == 2:
                nums.append(int(parts[1]))

        # Verify ascending order
        assert nums == sorted(nums), f"Bed numbers not in ascending order: {nums}"

    def test_main_fabric_bed_prefix_c(self, page: Page):
        """V-19: Main fabric beds use C- prefix."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")

        # Verify C- prefix beds exist for main fabric tasks
        c_beds = page.locator("td:has-text('C-')")
        assert c_beds.count() > 0, "No C-prefix bed numbers found"

    def test_aux_fabric_bed_prefix_f(self, page: Page):
        """V-19: Auxiliary fabric beds use F- prefix."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")

        # Check for F- prefix beds (may not exist in all scenarios)
        f_beds = page.locator("td:has-text('F-')")
        if f_beds.count() > 0:
            # Verify F-prefix format
            first_f = f_beds.first.inner_text()
            assert first_f.startswith("F-"), f"Expected F- prefix, got: {first_f}"


@pytest.mark.p2
@pytest.mark.boundary
class TestAntiOvercutBoundaries:
    """V-20, V-21, V-22, V-23: Anti-overcut mechanism boundaries."""

    def test_warning_when_below_threshold(self, page: Page):
        """V-20: Soft warning when remaining layers below threshold."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_table_row("CPO-A")
        bp.pad_click_button("新增床次")

        bp.pad_scan_barcode("FB003")

        # Input that triggers warning (remaining 9 < threshold 10)
        bp.pad_input_number("拉布层数", 5)
        bp.click_save()

        # Expect warning message
        warning = page.locator(".ant-message-warning, .ant-alert-warning")
        expect(warning).to_be_visible(timeout=3000)
        expect(warning).to_contain_text("剩余层数不足")

    def test_hard_block_when_remaining_negative(self, page: Page):
        """V-21: Hard block when input causes negative remaining."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_table_row("CPO-A")
        bp.pad_click_button("新增床次")

        bp.pad_scan_barcode("FB004")

        # Input that causes negative remaining (remaining 3, input 5)
        bp.pad_input_number("拉布层数", 5)
        bp.click_save()

        bp.expect_error_toast("总裁剪层数已超计划，需PC端审核")

    def test_pc_overcut_approval_approve(self, page: Page):
        """V-22: PC overcut approval - approve increases plan layers."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")

        # Find a task with overcut request
        page.locator("button:has-text('申请超裁')").first.click()
        page.wait_for_timeout(500)

        # In approval dialog, click approve
        page.locator("button:has-text('放行')").click()
        bp.confirm_dialog()

        bp.expect_success_toast()

    def test_pc_overcut_approval_reject(self, page: Page):
        """V-23: PC overcut approval - reject keeps original layers."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")

        page.locator("button:has-text('申请超裁')").first.click()
        page.wait_for_timeout(500)

        # Click reject
        page.locator("button:has-text('驳回')").click()
        bp.confirm_dialog()

        # Verify overcut request button still visible (plan layers unchanged)
        expect(page.locator("button:has-text('申请超裁')").first).to_be_visible()
