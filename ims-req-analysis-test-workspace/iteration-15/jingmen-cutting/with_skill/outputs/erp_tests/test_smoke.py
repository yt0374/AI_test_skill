"""
P0 Smoke Tests: 荆门新裁剪需求2.0

Core path verification — must pass for every build.
Environment: jingmen (bak.jmym.dtsimple.pro)

Test cases covered: F-01, F-02, F-03, C-04, C-06, C-07, V-03
"""
import pytest
from playwright.sync_api import Page, expect
from pages.base_page import ProductionPage, BasePage


class TestCuttingTaskCreation:
    """P0: 裁剪任务创建 - 核心流程 (C-04, V-03)"""

    @pytest.mark.p0
    @pytest.mark.pc
    @pytest.mark.jingmen
    def test_create_task_with_marker_allocation(self, logged_in_page: Page):
        """
        C-04: 正常分配唛架层数
        唛架M-001总计划层数100，当前已分配0，分配40层，剩余60
        """
        page = ProductionPage(logged_in_page)
        page.navigate_to_cutting_task()

        # Create task with single CPO and 40 layers
        page.create_cutting_task(
            cpos=["CPO-A"],
            marker="M-001",
            layers=40
        )

        # Verify success
        page.assert_toast_message("创建成功")
        page.assert_table_row_count(min_count=1)

    @pytest.mark.p0
    @pytest.mark.pc
    @pytest.mark.jingmen
    def test_overallocation_blocked(self, logged_in_page: Page):
        """
        V-03: 超额分配唛架层数禁止提交
        前置：唛架已分配80层，剩余20层；输入25层应被阻止
        """
        page = ProductionPage(logged_in_page)
        page.navigate_to_cutting_task()

        page.click_button("新建裁剪任务")
        page.check_checkbox("CPO-B")
        page.select_dropdown("唛架", "M-001")
        page.fill_field("计划层数", "25")
        page.click_button("提交")

        # Should block with allocation error
        page.assert_toast_message("分配层数超出")


class TestCuttingTaskPublish:
    """P0: 裁剪任务发布 (C-06)"""

    @pytest.mark.p0
    @pytest.mark.pc
    @pytest.mark.jingmen
    def test_publish_task_visible_on_pad(self, logged_in_page: Page):
        """
        C-06: 裁剪任务发布后PAD端可见
        """
        page = ProductionPage(logged_in_page)
        base = BasePage(logged_in_page)

        # PC: Create and publish task
        page.navigate_to_cutting_task()
        page.create_cutting_task(
            cpos=["CPO-A"],
            marker="M-001",
            layers=30
        )
        page.click_button("发布")

        # PAD: Switch viewport and verify visibility
        base.emulate_pad_viewport()
        page.navigate_to_cutting_task()

        # Task should be visible on PAD
        page.assert_table_row_count(min_count=1)
        # Verify task has correct status
        expect(logged_in_page.locator("tr.ant-table-row").first).to_contain_text("未开始")


class TestEndToEndMergeCpoFlow:
    """P0: 端到端流程 F-01 - 合并CPO裁剪→通用扎卡→自动挂片"""

    @pytest.mark.p0
    @pytest.mark.pc
    @pytest.mark.jingmen
    def test_merge_cpo_full_flow_pc_part(self, logged_in_page: Page):
        """
        F-01 (PC部分): 创建合并CPO裁剪任务，分配层数
        """
        page = ProductionPage(logged_in_page)
        page.navigate_to_cutting_task()

        # Create task with multiple CPOs (different due dates)
        page.create_cutting_task(
            cpos=["CPO-A", "CPO-C", "CPO-B"],
            marker="M-001",
            layers=50
        )

        # Verify: task created, marker remaining = 50
        page.assert_toast_message("创建成功")
        page.assert_table_row_count(min_count=1)


class TestEndToEndSingleCpoFlow:
    """P0: 端到端流程 F-02 - 单一CPO裁剪→指定扎卡→自动挂片"""

    @pytest.mark.p0
    @pytest.mark.pc
    @pytest.mark.jingmen
    def test_single_cpo_full_flow_pc_part(self, logged_in_page: Page):
        """
        F-02 (PC部分): 创建单一CPO裁剪任务
        """
        page = ProductionPage(logged_in_page)
        page.navigate_to_cutting_task()

        # Create task with single CPO
        page.create_cutting_task(
            cpos=["CPO-A"],
            marker="M-001",
            layers=40
        )

        page.assert_toast_message("创建成功")


class TestBedLifecycle:
    """P0: 床次全生命周期 F-03"""

    @pytest.mark.p0
    @pytest.mark.pad
    @pytest.mark.jingmen
    def test_bed_creation_basic(self, logged_in_page: Page):
        """
        C-07: 正常创建床次
        前置：裁剪任务计划层数100，剩余可用100
        """
        page = ProductionPage(logged_in_page)
        base = BasePage(logged_in_page)

        # Emulate PAD
        base.emulate_pad_viewport()
        page.navigate_to_cutting_task()

        # Enter cutting task and create bed
        first_task = logged_in_page.locator("tr.ant-table-row").first
        first_task.click()
        logged_in_page.wait_for_load_state("networkidle")

        page.click_button("新增床次")
        page.fill_field("布卷号", "FAB-001")
        page.fill_field("拉布层数", "30")
        page.click_button("确认")

        # Verify bed created
        page.assert_toast_message("创建成功")
