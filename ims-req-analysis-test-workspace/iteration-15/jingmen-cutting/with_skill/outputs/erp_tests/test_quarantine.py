"""
Quarantined / Flaky tests: 荆门新裁剪需求2.0

Tests that have been identified as flaky and are isolated for investigation.
These tests are skipped by default in CI.

Flaky Test Strategy:
1. Retry: Run failed tests with --reruns 2 --reruns-delay 5
2. Identification: Tests failing >30% of runs over 1 week → quarantine
3. Quarantine: Move to this file with @pytest.mark.skip
4. Weekly review: Review quarantined tests every Monday
"""
import pytest
from playwright.sync_api import Page


@pytest.mark.quarantine
@pytest.mark.skip(reason="Under investigation - intermittent timeout on bed creation")
@pytest.mark.p2
@pytest.mark.pad
@pytest.mark.jingmen
def test_quarantine_bed_creation_slow_network(logged_in_page: Page):
    """
    [QUARANTINED] Bed creation under slow network conditions.

    Original test: V-13
    Failure rate: ~40%
    Root cause: Network timing dependency on PAD sync
    Investigation: Check if backend response time > 5s causes timeout
    """
    from pages.base_page import ProductionPage, BasePage

    base = BasePage(logged_in_page)
    page = ProductionPage(logged_in_page)

    base.emulate_pad_viewport()
    page.navigate_to_cutting_task()

    first_task = logged_in_page.locator("tr.ant-table-row").first
    first_task.click()
    logged_in_page.wait_for_load_state("networkidle")

    page.click_button("新增床次")
    page.fill_field("布卷号", "FAB-SLOW-001")
    page.fill_field("拉布层数", "5")
    page.click_button("确认")

    # Increased timeout for slow network
    logged_in_page.wait_for_timeout(10000)
    page.assert_toast_message("创建成功")


@pytest.mark.quarantine
@pytest.mark.skip(reason="Under investigation - race condition in concurrent test")
@pytest.mark.p3
@pytest.mark.jingmen
def test_quarantine_concurrent_bed_race(browser, base_url, credentials):
    """
    [QUARANTINED] Concurrent bed creation race condition.

    Original test: P-01
    Failure rate: ~50%
    Root cause: Race condition when two beds claim last available layers
    Investigation: Check backend locking mechanism
    """
    # Same as P-01 but with retry analysis
    pass
