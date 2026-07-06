"""Quarantine: Flaky tests isolated due to intermittent failures.

These tests have known issues with timing, environment dependencies,
or external service instability. They are skipped by default and
reviewed weekly.

Quarantine Rules:
- Tests in this file MUST have @pytest.mark.skip with a reason
- Reason must include date quarantined and failure pattern
- Weekly review: un-skip fixed tests, remove those fixed >2 weeks
- Before re-enabling: run 10x consecutively, must pass 10/10

Markers: quarantine
"""
import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


@pytest.mark.quarantine
class TestQuarantinedFlaky:
    """Quarantined tests — review weekly."""

    @pytest.mark.skip(reason="[2026-07-03] Intermittent timeout on slow CI; PAD modal render delay >5s")
    def test_bed_submission_large_layer_count(self, page: Page):
        """C-08 (quarantine variant): Bed submission with large layer count.

        Known issue: PAD submit modal occasionally takes >5s to render
        when layer count is large, causing timeout in CI environment.
        """
        bp = BasePage(page)
        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_table_row("CPO-A")

        page.locator("text=拉布中").first.click()
        bp.pad_click_button("提交完成")
        bp.pad_input_number("实际层数", "100")
        bp.confirm_dialog()
        bp.expect_success_toast()

    @pytest.mark.skip(reason="[2026-07-03] Smart merge dialog not always triggered; depends on CPO data state")
    def test_smart_merge_all_same_delivery(self, page: Page):
        """C-04 (quarantine variant): Smart merge when ALL CPOs share same delivery.

        Known issue: When all CPOs have same delivery date, the merge dialog
        behavior is inconsistent — sometimes groups all, sometimes shows empty.
        """
        bp = BasePage(page)
        bp.navigate_to_module("生产")
        bp.click_third_menu("裁剪任务")
        bp.click_add()

        page.locator("button:has-text('智能合并')").click()
        page.wait_for_timeout(1000)

        dialog = page.locator(".ant-modal:visible")
        expect(dialog).to_be_visible()

    @pytest.mark.skip(reason="[2026-07-03] Manual-to-auto switch CPO reselection inconsistent on Jingmen env")
    def test_manual_to_auto_cpo_preservation(self, page: Page):
        """F-12 (quarantine variant): Manual->Auto preserves correct CPO state.

        Known issue: After manual hanging of CPO-D (far delivery), switching
        back to auto does not always reselect the nearest-unfilled CPO.
        """
        bp = BasePage(page)
        bp.navigate_to_module("吊挂")
        bp.click_third_menu("缝制挂片")
        bp.pad_click_button("手动充数")
        page.locator(".cpo-item", has_text="CPO-D").click()
        bp.pad_scan_barcode("TAG-GEN-005")
        bp.pad_click_button("恢复自动充数")
        page.wait_for_timeout(1000)
        auto_cpo = page.locator(".assigned-cpo, [class*='current-cpo']")
        expect(auto_cpo).to_be_visible()
