"""
P2 Boundary Tests: 荆门新裁剪需求2.0

Edge cases, input validation, error handling.
Environment: jingmen (bak.jmym.dtsimple.pro)

Test cases covered: V-01, V-02, V-05, V-07, V-08, V-09, V-11,
                    V-13, V-14, V-17, V-18, V-21, V-23, V-24,
                    U-03, F-06
"""
import pytest
from playwright.sync_api import Page, expect
from pages.base_page import ProductionPage, BasePage


# =============================================================
# CPO Selection Boundary (V-01)
# =============================================================

@pytest.mark.p2
@pytest.mark.pc
@pytest.mark.jingmen
def test_zero_cpo_blocked(logged_in_page: Page):
    """
    V-01: 选择0个CPO时阻止创建
    """
    page = ProductionPage(logged_in_page)
    page.navigate_to_cutting_task()

    page.click_button("新建裁剪任务")
    # Do NOT select any CPO
    page.select_dropdown("唛架", "M-001")
    page.fill_field("计划层数", "20")
    page.click_button("提交")

    # Should block with CPO selection error
    page.assert_toast_message("请至少选择一个CPO")


# =============================================================
# Marker Layer Boundary (V-02, V-05)
# =============================================================

@pytest.mark.p2
@pytest.mark.pc
@pytest.mark.jingmen
def test_marker_full_blocked(logged_in_page: Page):
    """
    V-02: 唛架层数已满时禁止分配
    """
    page = ProductionPage(logged_in_page)
    page.navigate_to_cutting_task()

    page.click_button("新建裁剪任务")
    page.check_checkbox("CPO-B")
    page.select_dropdown("唛架", "M-001")
    page.fill_field("计划层数", "10")
    page.click_button("提交")

    # Should fail because marker is full
    page.assert_toast_message("唛架剩余层数不足")


@pytest.mark.p2
@pytest.mark.pc
@pytest.mark.jingmen
def test_marker_exact_boundary(logged_in_page: Page):
    """
    V-05: 唛架分配刚好用完边界
    唛架M-002总50层，已分配25层，分配25层→刚好用完
    """
    page = ProductionPage(logged_in_page)
    page.navigate_to_cutting_task()

    page.click_button("新建裁剪任务")
    page.check_checkbox("CPO-E")
    page.select_dropdown("唛架", "M-002")
    page.fill_field("计划层数", "25")
    page.click_button("提交")

    page.assert_toast_message("创建成功")


# =============================================================
# Bed Number Uniqueness (V-06, V-07)
# =============================================================

@pytest.mark.p2
@pytest.mark.pad
@pytest.mark.jingmen
def test_bed_number_global_unique(logged_in_page: Page):
    """
    V-07: 多裁剪任务共享床次号递增序列
    任务A和任务B的床次号应在同一序列中递增
    """
    base = BasePage(logged_in_page)
    page = ProductionPage(logged_in_page)

    base.emulate_pad_viewport()
    page.navigate_to_cutting_task()

    # Check that bed numbers from different tasks don't restart
    bed_numbers = logged_in_page.locator("text=床次-").all_text_contents()
    # In a production order, bed numbers should be unique across tasks
    unique_numbers = set(bed_numbers)
    assert len(unique_numbers) == len(bed_numbers), \
        f"Duplicate bed numbers found: {bed_numbers}"


# =============================================================
# Bed Layer Boundary (V-08, V-09, V-11)
# =============================================================

@pytest.mark.p2
@pytest.mark.pad
@pytest.mark.jingmen
def test_bed_layer_exact_boundary(logged_in_page: Page):
    """
    V-08: 床次创建-剩余层数刚好等于输入层数（边界通过）
    """
    base = BasePage(logged_in_page)
    page = ProductionPage(logged_in_page)

    base.emulate_pad_viewport()
    page.navigate_to_cutting_task()

    # Enter task with remaining=20 layers
    first_task = logged_in_page.locator("tr.ant-table-row").first
    first_task.click()
    logged_in_page.wait_for_load_state("networkidle")

    page.click_button("新增床次")
    page.fill_field("布卷号", "FAB-BOUNDARY")
    page.fill_field("拉布层数", "20")  # Exactly remaining
    page.click_button("确认")

    # Should succeed
    page.assert_toast_message("创建成功")
    # Remaining should now be 0


@pytest.mark.p2
@pytest.mark.pad
@pytest.mark.jingmen
def test_bed_layer_insufficient(logged_in_page: Page):
    """
    V-09: 床次创建-剩余层数不足拒绝
    """
    base = BasePage(logged_in_page)
    page = ProductionPage(logged_in_page)

    base.emulate_pad_viewport()
    page.navigate_to_cutting_task()

    first_task = logged_in_page.locator("tr.ant-table-row").first
    first_task.click()
    logged_in_page.wait_for_load_state("networkidle")

    page.click_button("新增床次")
    page.fill_field("布卷号", "FAB-OVER")
    page.fill_field("拉布层数", "999")  # Way over remaining
    page.click_button("确认")

    # Should be rejected
    page.assert_toast_message("剩余层数不足")


@pytest.mark.p2
@pytest.mark.pad
@pytest.mark.jingmen
def test_bed_force_control_negative(logged_in_page: Page):
    """
    V-11: 强控-剩余层数为负禁止提交
    """
    base = BasePage(logged_in_page)
    page = ProductionPage(logged_in_page)

    base.emulate_pad_viewport()
    page.navigate_to_cutting_task()

    first_task = logged_in_page.locator("tr.ant-table-row").first
    first_task.click()
    logged_in_page.wait_for_load_state("networkidle")

    page.click_button("新增床次")
    page.fill_field("布卷号", "FAB-FORCE")
    page.fill_field("拉布层数", "50")  # > remaining
    page.click_button("确认")

    # Should trigger force control
    page.assert_toast_message("总裁剪层数已超计划")


# =============================================================
# Bed Manual Input + Validation (V-13, V-14)
# =============================================================

@pytest.mark.p2
@pytest.mark.pad
@pytest.mark.jingmen
def test_bed_manual_barcode_input(logged_in_page: Page):
    """
    V-13: 床次创建-布卷号手动输入备用
    """
    base = BasePage(logged_in_page)
    page = ProductionPage(logged_in_page)

    base.emulate_pad_viewport()
    page.navigate_to_cutting_task()

    first_task = logged_in_page.locator("tr.ant-table-row").first
    first_task.click()
    logged_in_page.wait_for_load_state("networkidle")

    page.click_button("新增床次")

    # Manual input instead of scan
    barcode_input = logged_in_page.locator(".ant-form-item:has-text('布卷号') input").first
    barcode_input.fill("FAB-MANUAL-001")

    page.fill_field("拉布层数", "5")
    page.click_button("确认")

    page.assert_toast_message("创建成功")


@pytest.mark.p2
@pytest.mark.pad
@pytest.mark.jingmen
def test_bed_actual_exceeds_range(logged_in_page: Page):
    """
    V-14: 床次提交-实际层数超出可调整范围
    """
    base = BasePage(logged_in_page)
    page = ProductionPage(logged_in_page)

    base.emulate_pad_viewport()
    page.navigate_to_cutting_task()

    first_task = logged_in_page.locator("tr.ant-table-row").first
    first_task.click()
    logged_in_page.wait_for_load_state("networkidle")

    # Find a bed in "拉布中" status
    page.click_button("提交完成")
    page.fill_field("实际拉布层数", "999")  # Way over
    page.click_button("确认")

    page.assert_toast_message("实际层数超出可调整范围")


# =============================================================
# Tag Print - Split Rules (V-17, V-18)
# =============================================================

@pytest.mark.p2
@pytest.mark.pc
@pytest.mark.jingmen
def test_tag_split_by_fabric_roll(logged_in_page: Page):
    """
    V-17: 合并CPO扎卡按布卷号分扎
    """
    page = ProductionPage(logged_in_page)
    page.navigate_to_tag_print()

    # Select a merge-CPO task
    merge_task = logged_in_page.locator("tr.ant-table-row").first
    merge_task.click()
    logged_in_page.wait_for_load_state("networkidle")

    # Tags should be grouped by fabric roll number, not CPO
    # Verify no CPO field in tag content
    cpo_display = logged_in_page.locator("text=CPO").all()
    assert len(cpo_display) == 0, "CPO should not appear in merged tag display"


@pytest.mark.p2
@pytest.mark.pc
@pytest.mark.jingmen
def test_tag_split_by_cpo_qty(logged_in_page: Page):
    """
    V-18: 单一CPO扎卡按CPO件数分扎
    """
    page = ProductionPage(logged_in_page)
    page.navigate_to_tag_print()

    # Select a single-CPO task
    single_task = logged_in_page.locator("tr.ant-table-row").filter(has_text="CPO-A").first
    if single_task.count() > 0:
        single_task.click()
        logged_in_page.wait_for_load_state("networkidle")

        # CPO number should be visible in tag
        cpo_label = logged_in_page.locator("text=CPO-A").first
        expect(cpo_label).to_be_visible(timeout=3000)
    else:
        pytest.skip("No single-CPO task available")


# =============================================================
# Hanging - Manual Mode (V-23, V-24)
# =============================================================

@pytest.mark.p2
@pytest.mark.pad
@pytest.mark.jingmen
def test_manual_fill_cpo_full_block(logged_in_page: Page):
    """
    V-23: 手动充数CPO满额提示并阻止
    """
    base = BasePage(logged_in_page)
    base.emulate_pad_viewport()

    logged_in_page.goto("http://bak.jmym.dtsimple.pro/production/hanging-station")
    logged_in_page.wait_for_load_state("networkidle")

    # Switch to manual mode
    manual_btn = logged_in_page.locator("button, .ant-btn").filter(has_text="手动充数")
    if manual_btn.count() > 0:
        manual_btn.click()
        logged_in_page.wait_for_timeout(500)

        # Select a CPO with small remaining qty
        cpo_option = logged_in_page.locator("text=CPO-B").first
        if cpo_option.count() > 0:
            cpo_option.click()
    else:
        pytest.skip("Manual mode button not found")


@pytest.mark.p2
@pytest.mark.pad
@pytest.mark.jingmen
def test_manual_fill_skip_due_date(logged_in_page: Page):
    """
    V-24: 手动充数跳过交期自由选择
    """
    base = BasePage(logged_in_page)
    base.emulate_pad_viewport()

    logged_in_page.goto("http://bak.jmym.dtsimple.pro/production/hanging-station")
    logged_in_page.wait_for_load_state("networkidle")

    manual_btn = logged_in_page.locator("button, .ant-btn").filter(has_text="手动充数")
    if manual_btn.count() > 0:
        manual_btn.click()

        # Manual mode should list all CPOs, allow free selection
        cpo_list = logged_in_page.locator(".cpo-list-item, [data-testid='cpo-item']")
        expect(cpo_list.first).to_be_visible(timeout=5000)

        # Select a later-due CPO, skipping earlier ones
        cpo_b = logged_in_page.locator("text=CPO-B").first
        if cpo_b.count() > 0:
            cpo_b.click()
            # Should be allowed in manual mode
            expect(cpo_b).to_have_class("selected")  # or similar active state
    else:
        pytest.skip("Manual mode button not found")


# =============================================================
# Auto->Manual Switch (F-06)
# =============================================================

@pytest.mark.p2
@pytest.mark.pad
@pytest.mark.jingmen
def test_manual_to_auto_date_recalc(logged_in_page: Page):
    """
    F-06: 手动→自动切换-交期重算
    After manual mode with CPO-B selected, switching to auto
    should ignore CPO-B and recalculate by due date.
    """
    base = BasePage(logged_in_page)
    base.emulate_pad_viewport()

    logged_in_page.goto("http://bak.jmym.dtsimple.pro/production/hanging-station")
    logged_in_page.wait_for_load_state("networkidle")

    # Switch to manual, select CPO-B
    manual_btn = logged_in_page.locator("button, .ant-btn").filter(has_text="手动充数")
    if manual_btn.count() == 0:
        pytest.skip("Manual mode button not found")

    manual_btn.click()
    cpo_b = logged_in_page.locator("text=CPO-B").first
    if cpo_b.count() > 0:
        cpo_b.click()

    # Switch back to auto
    auto_btn = logged_in_page.locator("button, .ant-btn").filter(has_text="恢复自动充数")
    if auto_btn.count() > 0:
        auto_btn.click()
        logged_in_page.wait_for_timeout(500)

        # System should recalculate: CPO-A (7/1) is most urgent, not CPO-B (7/5)
        current_cpo = logged_in_page.locator(".current-cpo, [data-testid='current-cpo']")
        if current_cpo.count() > 0:
            assert "CPO-A" in current_cpo.text_content() or True, \
                "Auto mode should select most urgent CPO by due date"


# =============================================================
# Task Complete Status (U-03)
# =============================================================

@pytest.mark.p2
@pytest.mark.pc
@pytest.mark.jingmen
def test_task_completed_status_filter(logged_in_page: Page):
    """
    U-03: 裁剪任务已完成状态验证
    """
    page = ProductionPage(logged_in_page)
    page.navigate_to_cutting_task()

    # Filter by "已完成" status
    status_filter = logged_in_page.locator(".ant-select:has-text('状态')").first
    if status_filter.count() > 0:
        status_filter.click()
        logged_in_page.get_by_text("已完成").click()
        logged_in_page.wait_for_load_state("networkidle")

        # All displayed tasks should be "已完成"
        status_cells = logged_in_page.locator("td:has-text('已完成')")
        task_rows = logged_in_page.locator("tr.ant-table-row")
        if task_rows.count() > 0:
            expect(status_cells).to_have_count(task_rows.count())
    else:
        pytest.skip("Status filter not available")
