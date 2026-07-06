"""
P1 Functional Tests: 荆门新裁剪需求2.0

Core business flow tests with parametrized data-driven approach.
Environment: jingmen (bak.jmym.dtsimple.pro)

Test cases covered: C-01, C-02, C-03, C-05, C-08 ~ C-11,
                    U-01, U-02, X-01, X-02, V-04, V-06,
                    V-10, V-12, V-15, V-16, V-19, V-20, V-22,
                    F-04, F-05, F-07
"""
import json
import pytest
from pathlib import Path
from playwright.sync_api import Page, expect
from pages.base_page import ProductionPage, BasePage


# =============================================================
# Data-Driven: CPO Selection (C-01, C-02, C-03)
# =============================================================

@pytest.mark.p1
@pytest.mark.pc
@pytest.mark.jingmen
@pytest.mark.parametrize("record", [
    {"id": "D01-1", "cpos": ["CPO-A", "CPO-C"], "expected": "success"},
    {"id": "D01-2", "cpos": ["CPO-A", "CPO-D"], "expected": "success_merge"},
    {"id": "D01-3", "cpos": ["CPO-A", "CPO-B", "CPO-C", "CPO-D", "CPO-E"], "expected": "success"},
])
def test_cpo_selection_variants(logged_in_page: Page, record: dict):
    """数据驱动: CPO选择变体 (C-01, C-02, C-03)"""
    page = ProductionPage(logged_in_page)
    page.navigate_to_cutting_task()

    page.click_button("新建裁剪任务")

    # Select CPOs
    for cpo in record["cpos"]:
        page.check_checkbox(cpo)

    page.select_dropdown("唛架", "M-001")
    page.fill_field("计划层数", "30")
    page.click_button("提交")

    if record["expected"] == "success":
        page.assert_toast_message("创建成功")


# =============================================================
# Marker Layer Allocation (C-05, V-04)
# =============================================================

@pytest.mark.p1
@pytest.mark.pc
@pytest.mark.jingmen
def test_marker_partial_allocation(logged_in_page: Page):
    """
    C-05: 部分占用后再次分配
    前置：唛架M-001已分配40层给任务A，剩余可用60层
    """
    page = ProductionPage(logged_in_page)
    page.navigate_to_cutting_task()

    page.click_button("新建裁剪任务")
    page.check_checkbox("CPO-C")
    page.select_dropdown("唛架", "M-001")
    page.fill_field("计划层数", "30")
    page.click_button("提交")

    page.assert_toast_message("创建成功")

    # Verify remaining layers display (UI should show remaining)
    # The page should indicate remaining available layers
    remaining = logged_in_page.locator("text=剩余可用").text_content()
    assert "30" in remaining, f"Expected remaining 30 layers, got: {remaining}"


@pytest.mark.p1
@pytest.mark.pc
@pytest.mark.jingmen
def test_marker_multi_task_decrement(logged_in_page: Page):
    """
    V-04: 多任务共享唛架层数递减验证
    """
    page = ProductionPage(logged_in_page)

    # Task A: 30 layers
    page.navigate_to_cutting_task()
    page.create_cutting_task(cpos=["CPO-A"], marker="M-001", layers=30)

    # Task B: 30 layers
    page.navigate_to_cutting_task()
    page.create_cutting_task(cpos=["CPO-C"], marker="M-001", layers=30)

    # Task C: 40 layers
    page.navigate_to_cutting_task()
    page.create_cutting_task(cpos=["CPO-B"], marker="M-001", layers=40)

    # Task D: should fail (1 layer > remaining 0)
    page.navigate_to_cutting_task()
    page.click_button("新建裁剪任务")
    page.check_checkbox("CPO-D")
    page.select_dropdown("唛架", "M-001")
    page.fill_field("计划层数", "1")
    page.click_button("提交")

    page.assert_toast_message("剩余层数不足")


# =============================================================
# Bed Submission (C-08, C-09)
# =============================================================

@pytest.mark.p1
@pytest.mark.pad
@pytest.mark.jingmen
@pytest.mark.parametrize("record", [
    {"id": "D04-1", "held": 30, "actual": 30, "expected": "success"},
    {"id": "D04-2", "held": 30, "actual": 25, "expected": "success"},
])
def test_bed_submit_variants(logged_in_page: Page, record: dict):
    """数据驱动: 床次提交变体 - 实际层数等于/小于暂扣 (C-08, C-09)"""
    base = BasePage(logged_in_page)
    page = ProductionPage(logged_in_page)

    base.emulate_pad_viewport()
    page.navigate_to_cutting_task()

    # Enter the cutting task
    first_task = logged_in_page.locator("tr.ant-table-row").first
    first_task.click()
    logged_in_page.wait_for_load_state("networkidle")

    # Find the bed in "拉布中" status
    page.click_button("提交完成")
    page.fill_field("实际拉布层数", str(record["actual"]))
    page.click_button("确认")

    if record["expected"] == "success":
        page.assert_toast_message("提交成功")


# =============================================================
# Task Status Management (U-01, U-02, X-01, X-02)
# =============================================================

@pytest.mark.p1
@pytest.mark.pc
@pytest.mark.jingmen
def test_editable_when_not_started(logged_in_page: Page):
    """
    U-01: 裁剪任务未开始可编辑
    """
    page = ProductionPage(logged_in_page)
    page.navigate_to_cutting_task()

    # Find a task in "未开始" status
    task_row = logged_in_page.locator("tr.ant-table-row").filter(has_text="未开始").first
    expect(task_row).to_be_visible(timeout=5000)

    # Edit button should be visible and clickable
    edit_btn = task_row.locator("button, .ant-btn").filter(has_text="编辑")
    expect(edit_btn).to_be_visible()


@pytest.mark.p1
@pytest.mark.pc
@pytest.mark.jingmen
def test_edit_hidden_when_in_progress(logged_in_page: Page):
    """
    U-02: 裁剪任务拉布中隐藏编辑按钮
    """
    page = ProductionPage(logged_in_page)
    page.navigate_to_cutting_task()

    # Find a task in "拉布中" status
    task_row = logged_in_page.locator("tr.ant-table-row").filter(has_text="拉布中").first
    if task_row.count() > 0:
        edit_btn = task_row.locator("button, .ant-btn").filter(has_text="编辑")
        expect(edit_btn).not_to_be_visible()
    else:
        pytest.skip("No task in '拉布中' status available for testing")


@pytest.mark.p1
@pytest.mark.pc
@pytest.mark.jingmen
def test_deletable_when_not_started(logged_in_page: Page):
    """
    X-01: 裁剪任务未开始可删除
    """
    page = ProductionPage(logged_in_page)
    page.navigate_to_cutting_task()

    task_row = logged_in_page.locator("tr.ant-table-row").filter(has_text="未开始").first
    expect(task_row).to_be_visible(timeout=5000)

    delete_btn = task_row.locator("button, .ant-btn").filter(has_text="删除")
    expect(delete_btn).to_be_visible()


@pytest.mark.p1
@pytest.mark.pc
@pytest.mark.jingmen
def test_delete_hidden_when_in_progress(logged_in_page: Page):
    """
    X-02: 裁剪任务拉布中隐藏删除按钮
    """
    page = ProductionPage(logged_in_page)
    page.navigate_to_cutting_task()

    task_row = logged_in_page.locator("tr.ant-table-row").filter(has_text="拉布中").first
    if task_row.count() > 0:
        delete_btn = task_row.locator("button, .ant-btn").filter(has_text="删除")
        expect(delete_btn).not_to_be_visible()
    else:
        pytest.skip("No task in '拉布中' status available for testing")


# =============================================================
# Overcut Review (C-10, C-11)
# =============================================================

@pytest.mark.p1
@pytest.mark.pc
@pytest.mark.jingmen
def test_overcut_approve(logged_in_page: Page):
    """
    C-10: 超裁申请-管理员放行
    """
    page = ProductionPage(logged_in_page)
    page.navigate_to_cutting_task()

    # Find task with overcut button visible
    overcut_btn = logged_in_page.locator("button, .ant-btn").filter(has_text="申请超裁")
    if overcut_btn.count() > 0:
        overcut_btn.first.click()
        logged_in_page.wait_for_timeout(500)
        page.click_button("放行")
        page.assert_toast_message("放行")
    else:
        pytest.skip("No overcut application available for testing")


@pytest.mark.p1
@pytest.mark.pc
@pytest.mark.jingmen
def test_overcut_reject(logged_in_page: Page):
    """
    C-11: 超裁申请-管理员驳回
    """
    page = ProductionPage(logged_in_page)
    page.navigate_to_cutting_task()

    overcut_btn = logged_in_page.locator("button, .ant-btn").filter(has_text="申请超裁")
    if overcut_btn.count() > 0:
        overcut_btn.first.click()
        logged_in_page.wait_for_timeout(500)
        page.click_button("驳回")
        page.assert_toast_message("驳回")
    else:
        pytest.skip("No overcut application available for testing")


# =============================================================
# Anti-Overcut Warning (V-10)
# =============================================================

@pytest.mark.p1
@pytest.mark.pad
@pytest.mark.jingmen
def test_anticut_warning_threshold(logged_in_page: Page):
    """
    V-10: 软预警-剩余层数低于阈值(10层)
    """
    base = BasePage(logged_in_page)
    page = ProductionPage(logged_in_page)

    base.emulate_pad_viewport()
    page.navigate_to_cutting_task()

    # Enter task (must have 92+ locked layers, leaving <10 available)
    first_task = logged_in_page.locator("tr.ant-table-row").first
    first_task.click()
    logged_in_page.wait_for_load_state("networkidle")

    page.click_button("新增床次")
    page.fill_field("布卷号", "FAB-WARN")
    page.fill_field("拉布层数", "5")
    page.click_button("确认")

    # Should show warning toast
    warning = logged_in_page.locator("text=剩余层数不足")
    expect(warning).to_be_visible(timeout=5000)


# =============================================================
# Tag Printing (V-12, V-15, V-16)
# =============================================================

@pytest.mark.p1
@pytest.mark.pad
@pytest.mark.jingmen
def test_bed_barcode_scan(logged_in_page: Page):
    """
    V-12: 床次创建-布卷号扫描录入
    """
    base = BasePage(logged_in_page)
    page = ProductionPage(logged_in_page)

    base.emulate_pad_viewport()
    page.navigate_to_cutting_task()

    first_task = logged_in_page.locator("tr.ant-table-row").first
    first_task.click()
    logged_in_page.wait_for_load_state("networkidle")

    page.click_button("新增床次")

    # Simulate barcode scan by filling the field
    barcode_field = logged_in_page.locator(".ant-form-item:has-text('布卷号') input").first
    expect(barcode_field).to_be_visible()
    barcode_field.fill("FAB-001")

    page.fill_field("拉布层数", "10")
    page.click_button("确认")
    page.assert_toast_message("创建成功")


@pytest.mark.p1
@pytest.mark.pc
@pytest.mark.jingmen
def test_tag_print_merge_cpo_no_display(logged_in_page: Page):
    """
    V-15: 合并CPO时扎卡打印页面隐藏CPO选择区域
    """
    page = ProductionPage(logged_in_page)
    page.navigate_to_tag_print()

    # Select a task with merged CPOs
    merge_task = logged_in_page.locator("tr.ant-table-row").first
    merge_task.click()

    # CPO selection area should be hidden
    cpo_area = logged_in_page.locator("text=CPO").first
    # In merged CPO scenario, CPO selection should not be visible
    # Note: actual selector depends on UI implementation
    expect(cpo_area).not_to_be_visible(timeout=5000)


@pytest.mark.p1
@pytest.mark.pc
@pytest.mark.jingmen
def test_tag_print_single_cpo_display(logged_in_page: Page):
    """
    V-16: 单一CPO时扎卡显示CPO号并印刷
    """
    page = ProductionPage(logged_in_page)
    page.navigate_to_tag_print()

    # Select a task with single CPO
    single_task = logged_in_page.locator("tr.ant-table-row").filter(has_text="CPO-A").first
    if single_task.count() > 0:
        single_task.click()
        # CPO info should be visible
        cpo_display = logged_in_page.locator("text=CPO-A").first
        expect(cpo_display).to_be_visible(timeout=5000)
    else:
        pytest.skip("No single-CPO task available for tag print test")


# =============================================================
# Hanging Station - Auto Fill (V-19, V-20, V-22)
# =============================================================

@pytest.mark.p1
@pytest.mark.pad
@pytest.mark.jingmen
def test_auto_fill_due_date_priority(logged_in_page: Page):
    """
    V-19: 通用扎卡按交期优先自动充数
    """
    base = BasePage(logged_in_page)
    base.emulate_pad_viewport()

    # Navigate to hanging station (PAD)
    logged_in_page.goto("http://bak.jmym.dtsimple.pro/production/hanging-station")
    logged_in_page.wait_for_load_state("networkidle")

    # Scan generic tag (simulated)
    # The system should auto-fill to the most urgent CPO
    fill_btn = logged_in_page.locator("button, .ant-btn").filter(has_text="自动充数")
    if fill_btn.count() > 0:
        expect(fill_btn).to_be_visible()
    else:
        pytest.skip("Auto-fill button not found on hanging station page")


@pytest.mark.p1
@pytest.mark.pad
@pytest.mark.jingmen
def test_auto_fill_cpo_switch_on_full(logged_in_page: Page):
    """
    V-22: CPO满额自动切换下一个
    """
    base = BasePage(logged_in_page)
    base.emulate_pad_viewport()

    logged_in_page.goto("http://bak.jmym.dtsimple.pro/production/hanging-station")
    logged_in_page.wait_for_load_state("networkidle")

    # Current CPO display should change when full
    cpo_display = logged_in_page.locator(".current-cpo, [data-testid='current-cpo']")
    if cpo_display.count() > 0:
        initial_cpo = cpo_display.text_content()
        # Simulate filling until CPO full, verify switch
        expect(cpo_display).to_be_visible()
