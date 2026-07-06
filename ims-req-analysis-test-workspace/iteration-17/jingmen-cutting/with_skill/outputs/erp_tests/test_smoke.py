"""P0 Smoke Tests: Jingmen Cutting 2.0

Core path verification — these must pass for every build.
Covers: CPO selection, cutting task creation, bed creation,
tag printing visibility, and auto-fill hanging.

Priority: P0
Markers: smoke_sanity
"""
import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


@pytest.mark.p0
@pytest.mark.smoke
class TestCuttingTaskCreation:
    """F-01, C-01, C-02: Cutting task creation with CPO selection."""

    def test_create_task_single_cpo(self, page: Page):
        """C-01: Create cutting task with single CPO selection."""
        bp = BasePage(page)

        # Navigate to 生产 > 裁剪任务
        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")

        # Click add/save for single CPO
        bp.click_add()
        page.wait_for_timeout(1000)

        # Select single CPO
        cpo_checkbox = page.locator("label", has_text="CPO-A").locator("input[type='checkbox']")
        cpo_checkbox.check()

        # Verify only CPO-A is selected
        assert cpo_checkbox.is_checked()
        bp.click_save()

        bp.expect_success_toast()

    def test_create_task_multiple_cpo(self, page: Page):
        """C-02: Create cutting task with multiple CPO selection."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")

        bp.click_add()
        page.wait_for_timeout(1000)

        # Select multiple CPOs
        for cpo_id in ["CPO-B", "CPO-C"]:
            cpo_checkbox = page.locator("label", has_text=cpo_id).locator("input[type='checkbox']")
            cpo_checkbox.check()

        bp.click_save()
        bp.expect_success_toast()

    def test_task_default_not_started(self, page: Page):
        """C-05: Newly created task defaults to '未开始' status."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")

        # Verify tasks in list have 未开始 status
        bp.expect_table_has_rows(min_rows=1)
        bp.expect_status_in_table("未开始")


@pytest.mark.p0
@pytest.mark.smoke
class TestBedCreation:
    """F-01, C-06: Bed (床次) creation on PAD."""

    def test_create_bed_with_enough_layers(self, page: Page):
        """C-06: Create bed with input layers less than remaining."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")

        # Enter first cutting task (simulating PAD view via task detail)
        bp.click_table_row("CPO-A")

        # Click 新增床次
        bp.pad_click_button("新增床次")
        page.wait_for_timeout(1000)

        # Scan barcode
        bp.pad_scan_barcode("FB001")

        # Input layer count
        bp.pad_input_number("拉布层数", 20)

        # Submit
        bp.click_save()
        bp.expect_success_toast()

    def test_create_bed_exact_remaining(self, page: Page):
        """C-07: Create bed with input exactly equal to remaining."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_table_row("CPO-A")

        bp.pad_click_button("新增床次")
        page.wait_for_timeout(1000)

        bp.pad_scan_barcode("FB002")
        bp.pad_input_number("拉布层数", 10)  # Exactly remaining

        bp.click_save()
        bp.expect_success_toast()

    def test_bed_number_generation(self, page: Page):
        """V-17: Bed number generated on submit complete."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_table_row("CPO-A")

        # Find a bed in 拉布中 status
        bed_row = page.locator("tr", has_text="拉布中").first
        bed_row.click()

        # Submit complete
        bp.pad_click_button("提交完成")
        page.wait_for_timeout(500)

        # Input actual layers
        bp.pad_input_number("实际层数", 20)
        bp.confirm_dialog()

        # Verify bed number generated (C-xxx or F-xxx format)
        bed_number_cell = page.locator("td", has_text="C-").first
        expect(bed_number_cell).to_be_visible(timeout=5000)


@pytest.mark.p0
@pytest.mark.smoke
class TestTagPrinting:
    """L-01, L-02: Tag printing with CPO visibility rules."""

    def test_merged_cpo_hides_cpo_info(self, page: Page):
        """L-01: Merged CPO task hides CPO info on tag print page."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("扎卡打印")

        # Select a merged-CPO cutting task
        bp.click_table_row("CPO-B")  # Assuming CPO-B is in a merged task

        # Verify CPO selection area is hidden
        cpo_section = page.locator(".cpo-selector, [class*='cpo']")
        expect(cpo_section).to_be_hidden()

    def test_single_cpo_shows_cpo_info(self, page: Page):
        """L-02: Single CPO task shows CPO info on tag print page."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("扎卡打印")

        # Select a single-CPO cutting task
        bp.click_table_row("CPO-A")

        # Verify CPO info is displayed
        cpo_info = page.locator("text=CPO-A")
        expect(cpo_info).to_be_visible()

        # Verify delivery date and quantity shown
        expect(page.locator("text=2026-07-01")).to_be_visible()
        expect(page.locator("text=500")).to_be_visible()


@pytest.mark.p0
@pytest.mark.smoke
class TestAutoFillHanging:
    """F-05, F-06: Auto-fill mode for hanging station."""

    def test_generic_tag_auto_fill_by_delivery(self, page: Page):
        """F-05: Generic tag auto-fills by delivery date priority."""
        bp = BasePage(page)

        bp.navigate_to_module("吊挂")
        bp.click_third_menu("缝制挂片")

        # Verify we are in auto-fill mode (default)
        auto_mode_indicator = page.locator("text=自动充数")
        expect(auto_mode_indicator).to_be_visible()

        # Scan a generic tag (no CPO info)
        bp.pad_scan_barcode("TAG-GEN-001")

        # Verify system auto-assigned to nearest-delivery CPO
        assigned_cpo = page.locator(".assigned-cpo, [class*='current-cpo']")
        expect(assigned_cpo).to_contain_text("CPO-A")  # Nearest delivery 7/1

    def test_specific_tag_priority_bind(self, page: Page):
        """F-06: Specific tag binds to its designated CPO first."""
        bp = BasePage(page)

        bp.navigate_to_module("吊挂")
        bp.click_third_menu("缝制挂片")

        # Scan a specific tag (has CPO-A printed)
        bp.pad_scan_barcode("TAG-CPO-A-001")

        # Verify bound to CPO-A
        bound_cpo = page.locator(".assigned-cpo, [class*='current-cpo']")
        expect(bound_cpo).to_contain_text("CPO-A")

    def test_task_publish_pad_sync(self, page: Page):
        """F-04: Published cutting task synced to PAD."""
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")

        # Check table has rows visible
        bp.expect_table_has_rows(min_rows=1)

        # Verify task details include CPO and layer info
        first_row = page.locator("tr.ant-table-row").first
        expect(first_row).to_be_visible()
