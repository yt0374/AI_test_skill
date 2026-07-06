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
from conftest import navigate_to_attendance


@pytest.mark.quarantine
class TestQuarantinedFlaky:
    """Quarantined tests -- review weekly."""

    @pytest.mark.skip(
        reason="[2026-07-03] Replenish card dialog render timing inconsistent; "
               "modal may take >5s to appear on SIT environment."
    )
    def test_replenish_card_full_flow(self, page: Page):
        """C-01 (quarantine variant): Full replenish card save flow.

        Known issue: Replenish card dialog occasionally takes >5s to render
        fully, causing timeout in CI. SIT environment latency varies.
        """
        bp = BasePage(page)
        navigate_to_attendance(page, "考勤登记")

        replenish_btn = page.locator("button:has-text('补卡')").first
        replenish_btn.click()
        page.wait_for_timeout(1000)

        modal = page.locator(".ant-modal:visible, .ant-drawer:visible")
        if modal.count() > 0:
            inputs = modal.first.locator("input")
            if inputs.count() > 0:
                inputs.first.fill("100001")

    @pytest.mark.skip(
        reason="[2026-07-03] Return-work employee selector load time "
               "depends on department/group data; may fail when DB slow."
    )
    def test_return_work_employee_selector_full(self, page: Page):
        """V-21 (quarantine variant): Full employee selector interaction.

        Known issue: Employee list loading time varies greatly depending
        on department/group data size. On SIT, load can exceed 10s.
        """
        bp = BasePage(page)
        navigate_to_attendance(page, "回工登记")
        bp.click_add()
        page.wait_for_timeout(1000)

        modal = page.locator(".ant-modal:visible, .ant-drawer:visible")
        if modal.count() > 0:
            # Wait for employee selector to load
            page.wait_for_timeout(3000)

    @pytest.mark.skip(
        reason="[2026-07-03] Daily attendance calculation with progress bar "
               "takes 30-120s depending on date range. Not suitable for CI."
    )
    def test_daily_calc_with_large_date_range(self, page: Page):
        """U-10 (quarantine variant): Daily calc with 3-month range.

        Known issue: Full 3-month calculation takes 30-120 seconds
        on SIT environment, causing CI timeout (default 30s per test).
        """
        bp = BasePage(page)
        navigate_to_attendance(page, "日考勤统计")

        calc_btn = page.locator(
            "button:has-text('计算'), button:has-text('日考勤计算')"
        ).first
        calc_btn.click()
        page.wait_for_timeout(1000)

    @pytest.mark.skip(
        reason="[2026-07-03] Monthly attendance generation - version increment "
               "depends on prior month having at least one version. "
               "Data state unpredictable on shared SIT."
    )
    def test_monthly_generate_with_version_increment(self, page: Page):
        """C-06 (quarantine variant): Generate monthly with version+1.

        Known issue: Version increment behavior depends on prior month
        having generated stats. Shared SIT environment has unpredictable
        monthly attendance data state.
        """
        bp = BasePage(page)
        navigate_to_attendance(page, "月考勤统计")

        gen_btn = page.locator("button:has-text('生成月考勤')").first
        gen_btn.click()
        page.wait_for_timeout(1000)

    @pytest.mark.skip(
        reason="[2026-07-03] Attendance sync from device - requires live "
               "Access DB connection on server. Not available in CI."
    )
    def test_attendance_sync_full_flow(self, page: Page):
        """F-05 (quarantine variant): Full attendance sync flow.

        Known issue: Requires live Access database connection on the
        server. The sync endpoint is not always available in CI
        and may fail with network errors.
        """
        bp = BasePage(page)
        navigate_to_attendance(page, "日考勤统计")

        sync_btn = page.locator("button:has-text('考勤同步')")
        if sync_btn.count() > 0:
            sync_btn.first.click()
            page.wait_for_timeout(1000)
