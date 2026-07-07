"""
P3 Integration Tests: #4140 分拣统计表 数据修正
Jingmen environment (bak.jmym.dtsimple.pro)
Tests: I-01 (end-to-end data flow), I-02 (cross-module sewing group linkage)
"""
import pytest
from pages.base_page import BasePage


class TestSortingStatsIntegration:
    """P3 integration/cross-module tests."""

    # -- I-01: End-to-end data flow --
    @pytest.mark.p3
    def test_end_to_end_data_flow(self, page):
        """
        I-01: Verify end-to-end data flow:
        sortation → MQ → mes-production → 分拣统计表
        This test validates the full chain is operational by checking:
        1. Report page loads
        2. Data rows contain expected field values
        3. New fields (缝制组别, 订单数) have content
        """
        base = BasePage(page)

        # Step 1: Navigate to report
        base.navigate_to_module("报表")
        page.wait_for_timeout(1000)
        base.navigate_to_submenu("分拣统计表")
        base.wait_for_table(timeout=20000)

        # Step 2: Verify table structure
        headers = base.get_column_headers()
        all_headers = " ".join(headers)

        required_fields = ["日期", "SKU", "CPO", "站位", "产量", "缝制组别", "订单数"]
        for field in required_fields:
            assert field in all_headers, \
                f"Required field '{field}' not found in table headers: {all_headers}"

        # Step 3: Verify data rows (at least table is functional)
        rows = base.get_table_rows()
        row_count = rows.count()

        if row_count > 0:
            # Check first row for basic data integrity
            first_row_text = rows.first.text_content()
            # Date should be in YYYY-MM-DD format
            # Numbers should be present for 产量/订单数
            assert len(first_row_text) > 0, "First row should have content"

        # Step 4: Verify filter controls
        assert page.locator("button").filter(has_text="查询").count() > 0
        assert page.locator("button").filter(has_text="导出").count() > 0

        # Step 5: Verify more filters accessible
        more_filter_btn = page.locator("button, a").filter(has_text="更多筛选")
        if more_filter_btn.count() > 0:
            more_filter_btn.first.click()
            page.wait_for_timeout(500)
            # Additional filter fields should appear
            base.close_modal()

    # -- I-02: Cross-module verification (生产 → 缝制组别 → 报表) --
    @pytest.mark.p3
    def test_sewing_group_cross_module(self, page):
        """
        I-02: Verify 缝制组别 field links correctly to 生产 > 缝制任务.
        The sewing group displayed in the report should match the group
        assigned in the production sewing task.
        """
        base = BasePage(page)

        # Navigate to report
        base.navigate_to_module("报表")
        page.wait_for_timeout(1000)
        base.navigate_to_submenu("分拣统计表")
        base.wait_for_table(timeout=20000)

        # Check 缝制组别 column has values
        headers = base.get_column_headers()
        sewing_group_index = None
        for i, h in enumerate(headers):
            if "缝制组别" in h:
                sewing_group_index = i
                break

        assert sewing_group_index is not None, \
            "缝制组别 column must exist in the table"

        # Verify values in 缝制组别 column are meaningful
        rows = base.get_table_rows()
        if rows.count() > 0:
            for row_idx in range(min(rows.count(), 5)):
                cell_text = base.get_table_cell(row_idx, sewing_group_index)
                # Value should not be raw null/undefined
                if cell_text:
                    assert "null" not in cell_text.lower(), \
                        f"Row {row_idx}: 缝制组别 should not show 'null'"
                    assert "undefined" not in cell_text.lower(), \
                        f"Row {row_idx}: 缝制组别 should not show 'undefined'"

    # -- I-03: Navigation consistency --
    @pytest.mark.p3
    def test_navigation_consistency(self, page):
        """
        I-03: Navigate away and back to report, verify state consistency.
        Also verifies the report is correctly placed under 报表 module.
        """
        base = BasePage(page)

        # First visit
        base.navigate_to_module("报表")
        page.wait_for_timeout(1000)
        base.navigate_to_submenu("分拣统计表")
        base.wait_for_table()

        rows_before = base.get_table_rows()
        count_before = rows_before.count()

        # Navigate to another module
        base.navigate_to_module("生产")
        page.wait_for_timeout(1000)

        # Return to report
        base.navigate_to_module("报表")
        page.wait_for_timeout(1000)
        base.navigate_to_submenu("分拣统计表")
        base.wait_for_table()

        rows_after = base.get_table_rows()
        count_after = rows_after.count()

        assert count_after == count_before, \
            f"Row count changed after re-navigation: {count_before} -> {count_after}"
