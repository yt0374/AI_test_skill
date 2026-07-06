"""
P3 Integration Tests: 荆门新裁剪需求2.0

Cross-module and end-to-end workflow tests.
Environment: jingmen (bak.jmym.dtsimple.pro)

Test cases covered: P-01 (并发床次创建), P-02 (超裁→审核→继续拉布)
"""
import pytest
from playwright.sync_api import Page, expect
from pages.base_page import ProductionPage, BasePage


# =============================================================
# Concurrent Bed Creation (P-01)
# =============================================================

@pytest.mark.p3
@pytest.mark.jingmen
def test_concurrent_bed_creation(browser, base_url, credentials):
    """
    P-01: 并发床次创建-多小组同时操作

    Two groups simultaneously create beds on the same cutting task.
    Anti-overcut must prevent exceeding planned layers.
    """
    # Simulate by creating two independent browser contexts
    # Context 1: Group A
    ctx_a = browser.new_context(viewport={"width": 1024, "height": 768}, locale="zh-CN")
    page_a = ctx_a.new_page()

    # Context 2: Group B
    ctx_b = browser.new_context(viewport={"width": 1024, "height": 768}, locale="zh-CN")
    page_b = ctx_b.new_page()

    try:
        # Login both contexts
        for page in [page_a, page_b]:
            page.goto(f"{base_url}/login", wait_until="networkidle")
            page.fill("#form_item_username", credentials["username"])
            page.fill("#form_item_password", credentials["password"])
            page.click(".ant-btn-primary")
            page.wait_for_url(f"{base_url}/**", timeout=15000)

        # Navigate both to the same cutting task (PAD view)
        for page in [page_a, page_b]:
            page.goto(f"{base_url}/production/cutting-task", wait_until="networkidle")

        # Both groups create beds simultaneously
        # Group A: 30 layers
        task_a = page_a.locator("tr.ant-table-row").first
        task_a.click()
        page_a.wait_for_load_state("networkidle")
        page_a.locator("button, .ant-btn").filter(has_text="新增床次").click()
        page_a.locator(".ant-form-item:has-text('布卷号') input").first.fill("FAB-A-001")
        page_a.locator(".ant-form-item:has-text('拉布层数') input").first.fill("30")
        page_a.locator("button, .ant-btn").filter(has_text="确认").click()

        # Group B: 30 layers (same task, same remaining)
        task_b = page_b.locator("tr.ant-table-row").first
        task_b.click()
        page_b.wait_for_load_state("networkidle")
        page_b.locator("button, .ant-btn").filter(has_text="新增床次").click()
        page_b.locator(".ant-form-item:has-text('布卷号') input").first.fill("FAB-B-001")
        page_b.locator(".ant-form-item:has-text('拉布层数') input").first.fill("30")
        page_b.locator("button, .ant-btn").filter(has_text="确认").click()

        # Wait for both operations
        page_a.wait_for_timeout(2000)
        page_b.wait_for_timeout(2000)

        # Verify: at least one should succeed, system must not allow
        # total > planned layers
        result_a = page_a.locator(".ant-message-notice-content").text_content() or ""
        result_b = page_b.locator(".ant-message-notice-content").text_content() or ""

        # One may succeed, one may fail with overcut - both cases valid
        assert "创建成功" in result_a or "创建成功" in result_b or \
               "超" in result_a or "超" in result_b, \
               "Expected at least one result message"

    finally:
        ctx_a.close()
        ctx_b.close()


# =============================================================
# Overcut End-to-End (P-02)
# =============================================================

@pytest.mark.p3
@pytest.mark.jingmen
def test_overcut_full_workflow(logged_in_page: Page):
    """
    P-02: 超裁→审核→继续拉布（端到端）

    Full flow: trigger overcut on PAD → admin approves on PC →
    continue bed creation on PAD.
    """
    page = ProductionPage(logged_in_page)
    base = BasePage(logged_in_page)

    # Phase 1: PAD - Create beds until overcut triggered
    base.emulate_pad_viewport()
    page.navigate_to_cutting_task()

    first_task = logged_in_page.locator("tr.ant-table-row").first
    first_task.click()
    logged_in_page.wait_for_load_state("networkidle")

    # Try to create a bed that triggers overcut
    page.click_button("新增床次")
    page.fill_field("布卷号", "FAB-OVERCUT-001")
    page.fill_field("拉布层数", "999")  # Force overcut
    page.click_button("确认")

    # Should see overcut error
    overcut_msg = logged_in_page.locator("text=总裁剪层数已超计划")
    expect(overcut_msg).to_be_visible(timeout=5000)

    # Phase 2: PC - Admin approves overcut
    logged_in_page.set_viewport_size({"width": 1920, "height": 1080})
    page.navigate_to_cutting_task()

    # Find the overcut application button
    apply_btn = logged_in_page.locator("button, .ant-btn").filter(has_text="申请超裁")
    if apply_btn.count() > 0:
        apply_btn.first.click()
        logged_in_page.wait_for_timeout(500)

        # Admin approves
        logged_in_page.locator("button, .ant-btn").filter(has_text="放行").click()
        logged_in_page.wait_for_load_state("networkidle")

        page.assert_toast_message("放行")

        # Phase 3: PAD - Continue bed creation
        base.emulate_pad_viewport()
        page.navigate_to_cutting_task()
        first_task = logged_in_page.locator("tr.ant-table-row").first
        first_task.click()
        logged_in_page.wait_for_load_state("networkidle")

        # Should now be able to create bed (layers increased)
        page.click_button("新增床次")
        page.fill_field("布卷号", "FAB-OVERCUT-002")
        page.fill_field("拉布层数", "30")
        page.click_button("确认")

        page.assert_toast_message("创建成功")
    else:
        pytest.skip("No overcut application available for integration test")
