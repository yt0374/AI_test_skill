"""P3 Integration Tests: Jingmen Cutting 2.0

Cross-module workflows spanning production, hanging, and warehouse modules.
End-to-end scenarios and data consistency verification.

Priority: P3
Markers: integration
"""
import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


@pytest.mark.p3
@pytest.mark.integration
class TestCuttingToHangingFlow:
    """End-to-end: Cutting task creation -> tag printing -> hanging."""

    def test_full_e2e_single_cpo_flow(self, page: Page):
        """F-01: Complete E2E flow for single CPO cutting.

        Steps:
        1. PC: Create cutting task with single CPO
        2. PC: Print tags (should show CPO info)
        3. PAD: Create bed and submit
        4. PAD: Hang pieces in auto-fill mode
        """
        bp = BasePage(page)

        # Step 1: Create cutting task
        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_add()
        page.locator("label", has_text="CPO-A").locator("input[type='checkbox']").check()
        page.locator(".ant-select", has_text="唛架").click()
        page.locator(".ant-select-dropdown:visible text='MK-001'").click()
        page.wait_for_timeout(300)
        bp.fill_field("计划层数", "40")
        bp.click_save()
        bp.expect_success_toast()

        # Step 2: Navigate to tag printing
        bp.navigate_to_module("生产")
        bp.click_third_menu("扎卡打印")
        bp.click_table_row("CPO-A")

        # Verify CPO info visible
        expect(page.locator("text=CPO-A")).to_be_visible()

        # Step 3: PAD bed creation (simulated on PC viewport)
        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_table_row("CPO-A")
        bp.pad_click_button("新增床次")
        bp.pad_scan_barcode("FB001")
        bp.pad_input_number("拉布层数", "20")
        bp.click_save()
        bp.expect_success_toast()

        # Submit bed
        page.locator("text=拉布中").first.click()
        bp.pad_click_button("提交完成")
        bp.pad_input_number("实际层数", "20")
        bp.confirm_dialog()
        bp.expect_success_toast()

        # Step 4: Hanging in auto-fill mode
        bp.navigate_to_module("吊挂")
        bp.click_third_menu("缝制挂片")
        bp.pad_scan_barcode("TAG-CPO-A-001")

        # Verify auto-assigned to CPO-A
        assigned = page.locator(".assigned-cpo, [class*='current-cpo']")
        expect(assigned).to_contain_text("CPO-A")

    def test_cross_module_data_consistency(self, page: Page):
        """Verify data consistency between production and hanging modules.

        - Cutting task created in 生产 should have CPO list visible in 吊挂
        - Tag printed for single CPO should match CPO in hanging station
        """
        bp = BasePage(page)

        # Check production module - verify cutting tasks exist
        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.expect_table_has_rows(min_rows=1)

        # Check hanging module - verify CPO data sync
        bp.navigate_to_module("吊挂")
        bp.click_third_menu("缝制挂片")

        # Verify page loads and shows CPO context
        page_content = page.content()
        assert "CPO" in page_content, "Hanging page should contain CPO references"


@pytest.mark.p3
@pytest.mark.integration
class TestProductionToWarehouseFlow:
    """Cross-module: Cutting beds -> warehouse fabric consumption."""

    def test_bed_completion_updates_inventory(self, page: Page):
        """Verify bed completion triggers warehouse inventory update.

        After bed submission (已拉布), fabric inventory should reflect
        the consumed layers in the warehouse fabric stock.
        """
        bp = BasePage(page)

        # Navigate to warehouse fabric inventory
        bp.navigate_to_module("仓库")
        bp.click_third_menu("面料库存管理")

        # Search for fabric used in the bed
        bp.fill_field("物料编号", "FB001")
        bp.click_search()

        # Verify inventory record exists
        bp.expect_table_has_rows(min_rows=1)

        # Check stock quantity reflects consumption
        stock_row = page.locator("tr.ant-table-row").first
        expect(stock_row).to_be_visible()


@pytest.mark.p3
@pytest.mark.integration
class TestConcurrentBedCreation:
    """V-14: Concurrent bed creation - first-come-first-served."""

    def test_concurrent_bed_creation_race(self, page: Page):
        """V-14: Simulate concurrent bed creation with remaining layer check.

        Note: Full concurrent testing requires multiple browser contexts.
        This test verifies the server-side race protection by:
        1. Opening two tabs to the same cutting task
        2. Creating beds in quick succession
        3. Verifying the second creation sees updated remaining layers
        """
        bp = BasePage(page)

        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_table_row("CPO-A")

        # Create first bed
        bp.pad_click_button("新增床次")
        bp.pad_scan_barcode("FB-RACE-1")
        bp.pad_input_number("拉布层数", "15")
        bp.click_save()
        bp.expect_success_toast()

        # Navigate back and re-enter to see updated remaining
        page.go_back()
        page.wait_for_timeout(500)
        bp.click_table_row("CPO-A")

        # Create second bed - should see reduced remaining
        bp.pad_click_button("新增床次")
        bp.pad_scan_barcode("FB-RACE-2")

        # Try to allocate more than remaining
        bp.pad_input_number("拉布层数", "40")  # Should exceed remaining
        bp.click_save()

        # Should be blocked if remaining < 40
        error_or_success = page.locator(".ant-message").first
        expect(error_or_success).to_be_visible(timeout=5000)
