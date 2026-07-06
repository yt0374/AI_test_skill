# 荆门新裁剪需求2.0 - Playwright自动化测试脚本

import pytest
import re
import time
from datetime import datetime, timedelta
from playwright.sync_api import Page, expect, BrowserContext


# ============================================================
# 全局配置与测试数据
# ============================================================

BASE_URL = "http://ims-test.example.com"  # 替换为实际测试环境URL
PC_USER = "test_cutting_manager"
PC_PASS = "test123"
PAD_USER = "test_cutting_worker"
PAD_PASS = "test123"

# 测试数据
TEST_ORDER = "SO-JM-2026-001"
TEST_MARKER = "M-001"  # 唛架M，总层数100
TEST_CPOS = {
    "CPO1": {"qty": 500, "delivery": "2026-07-01"},
    "CPO2": {"qty": 300, "delivery": "2026-07-05"},
    "CPO3": {"qty": 200, "delivery": "2026-07-02"},
    "CPO4": {"qty": 400, "delivery": "2026-07-01"},
}

THRESHOLD = 10  # 预警阈值


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture(scope="session")
def browser_context(browser):
    """创建浏览器上下文"""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="zh-CN"
    )
    yield context
    context.close()


@pytest.fixture
def pc_page(browser_context: BrowserContext) -> Page:
    """PC端页面 - 裁剪管理员"""
    page = browser_context.new_page()
    page.goto(f"{BASE_URL}/login")
    page.fill("#username", PC_USER)
    page.fill("#password", PC_PASS)
    page.click("button[type='submit']")
    page.wait_for_url(f"{BASE_URL}/dashboard")
    return page


@pytest.fixture
def pad_page(browser_context: BrowserContext) -> Page:
    """PAD端页面 - 拉布员/挂片员工"""
    page = browser_context.new_page()
    page.set_viewport_size({"width": 1024, "height": 768})
    page.goto(f"{BASE_URL}/pad/login")
    page.fill("#username", PAD_USER)
    page.fill("#password", PAD_PASS)
    page.click("button[type='submit']")
    page.wait_for_url(f"{BASE_URL}/pad/home")
    return page


# ============================================================
# 模块1：裁剪任务测试
# ============================================================

class TestCuttingTask:
    """裁剪任务模块测试"""

    # --- P0 测试 ---

    def test_create_single_cpo_cutting_task(self, pc_page: Page):
        """TC-CUT-P0-001: 创建单一CPO裁剪任务"""
        pc_page.goto(f"{BASE_URL}/cutting/task/new")
        pc_page.wait_for_selector("#cpo-select-area")

        # 选择CPO1
        pc_page.check("input[name='cpo'][value='CPO1']")

        # 验证仅CPO1被选中
        assert pc_page.is_checked("input[name='cpo'][value='CPO1']")
        assert not pc_page.is_checked("input[name='cpo'][value='CPO2']")

        # 选择唛架
        pc_page.select_option("#marker-select", TEST_MARKER)

        # 输入分配层数
        pc_page.fill("#allocated-layers", "40")

        # 提交
        pc_page.click("#btn-submit")

        # 验证成功提示
        expect(pc_page.locator(".success-toast")).to_be_visible(timeout=5000)
        assert "创建成功" in pc_page.locator(".success-toast").inner_text()

        # 验证唛架剩余层数
        pc_page.goto(f"{BASE_URL}/cutting/marker/{TEST_MARKER}")
        remaining = pc_page.locator("#remaining-layers").input_value()
        assert remaining == "60"

    def test_create_merged_cpo_cutting_task(self, pc_page: Page):
        """TC-CUT-P0-002: 创建合并CPO裁剪任务"""
        pc_page.goto(f"{BASE_URL}/cutting/task/new")

        # 多选CPO
        pc_page.check("input[name='cpo'][value='CPO1']")
        pc_page.check("input[name='cpo'][value='CPO2']")
        pc_page.check("input[name='cpo'][value='CPO3']")

        pc_page.select_option("#marker-select", TEST_MARKER)
        pc_page.fill("#allocated-layers", "80")
        pc_page.click("#btn-submit")

        expect(pc_page.locator(".success-toast")).to_be_visible(timeout=5000)

        # 验证剩余层数
        pc_page.goto(f"{BASE_URL}/cutting/marker/{TEST_MARKER}")
        remaining = pc_page.locator("#remaining-layers").input_value()
        assert remaining == "20"

    def test_marker_layer_overflow_prevention(self, pc_page: Page):
        """TC-CUT-P0-003: 唛架层数防超分配-超额禁止"""
        # 假设已分配90层(剩余10层)
        pc_page.goto(f"{BASE_URL}/cutting/task/new")

        pc_page.check("input[name='cpo'][value='CPO4']")
        pc_page.select_option("#marker-select", TEST_MARKER)
        pc_page.fill("#allocated-layers", "15")
        pc_page.click("#btn-submit")

        # 验证拦截
        expect(pc_page.locator(".error-toast")).to_be_visible(timeout=5000)
        error_msg = pc_page.locator(".error-toast").inner_text()
        assert "超" in error_msg or "超出" in error_msg or "不足" in error_msg

    def test_marker_layer_boundary_fill(self, pc_page: Page):
        """TC-CUT-P0-004: 唛架层数刚好满额"""
        pc_page.goto(f"{BASE_URL}/cutting/task/new")

        pc_page.check("input[name='cpo'][value='CPO4']")
        pc_page.select_option("#marker-select", TEST_MARKER)
        pc_page.fill("#allocated-layers", "10")
        pc_page.click("#btn-submit")

        expect(pc_page.locator(".success-toast")).to_be_visible(timeout=5000)

        pc_page.goto(f"{BASE_URL}/cutting/marker/{TEST_MARKER}")
        remaining = pc_page.locator("#remaining-layers").input_value()
        assert remaining == "0"

    def test_select_all_cpos(self, pc_page: Page):
        """TC-CUT-P0-005: 全选CPO功能"""
        pc_page.goto(f"{BASE_URL}/cutting/task/new")

        # 点击全选
        pc_page.click("#btn-select-all-cpo")

        # 验证所有CPO被选中
        for cpo_name in ["CPO1", "CPO2", "CPO3", "CPO4"]:
            assert pc_page.is_checked(f"input[name='cpo'][value='{cpo_name}']"), f"{cpo_name}未选中"

        # 验证总量
        total_qty = pc_page.locator("#total-order-qty").inner_text()
        assert "800" in total_qty

    def test_marker_sequential_allocation(self, pc_page: Page):
        """TC-CUT-P0-006: 唛架层数递减校验-多任务串行"""
        # 任务A: 30层
        pc_page.goto(f"{BASE_URL}/cutting/task/new")
        pc_page.check("input[name='cpo'][value='CPO1']")
        pc_page.select_option("#marker-select", TEST_MARKER)
        pc_page.fill("#allocated-layers", "30")
        pc_page.click("#btn-submit")
        expect(pc_page.locator(".success-toast")).to_be_visible()

        # 任务B: 40层
        pc_page.goto(f"{BASE_URL}/cutting/task/new")
        pc_page.check("input[name='cpo'][value='CPO2']")
        pc_page.select_option("#marker-select", TEST_MARKER)
        pc_page.fill("#allocated-layers", "40")
        pc_page.click("#btn-submit")
        expect(pc_page.locator(".success-toast")).to_be_visible()

        # 任务C: 30层
        pc_page.goto(f"{BASE_URL}/cutting/task/new")
        pc_page.check("input[name='cpo'][value='CPO3']")
        pc_page.select_option("#marker-select", TEST_MARKER)
        pc_page.fill("#allocated-layers", "30")
        pc_page.click("#btn-submit")
        expect(pc_page.locator(".success-toast")).to_be_visible()

        # 任务D: 尝试10层 - 应被拒绝
        pc_page.goto(f"{BASE_URL}/cutting/task/new")
        pc_page.check("input[name='cpo'][value='CPO4']")
        pc_page.select_option("#marker-select", TEST_MARKER)
        pc_page.fill("#allocated-layers", "10")
        pc_page.click("#btn-submit")
        expect(pc_page.locator(".error-toast")).to_be_visible()

    # --- P1 测试 ---

    def test_smart_merge_same_delivery(self, pc_page: Page):
        """TC-CUT-P1-001: 智能合并-同交期CPO自动归组"""
        pc_page.goto(f"{BASE_URL}/cutting/task/new")

        # 点击智能合并
        pc_page.click("#btn-smart-merge")

        # 验证合并分组 - CPO1和CPO4同交期7/1应为一组
        groups = pc_page.locator(".cpo-merge-group")
        group_count = groups.count()

        # 应至少有一个组包含CPO1和CPO4
        group_texts = groups.all_inner_texts()
        merged_found = False
        for text in group_texts:
            if "CPO1" in text and "CPO4" in text:
                merged_found = True
        assert merged_found, "CPO1和CPO4未智能合并到同一组"

    def test_smart_merge_no_same_delivery(self, pc_page: Page):
        """TC-CUT-P1-002: 智能合并-无同交期场景"""
        # 需要准备3个CPO均不同交期的订单数据
        pc_page.goto(f"{BASE_URL}/cutting/task/new?order=SO-DIFF-DELIVERY")
        pc_page.click("#btn-smart-merge")

        groups = pc_page.locator(".cpo-merge-group")
        assert groups.count() == 3, "3个不同交期CPO应分为3组"

    def test_task_only_includes_selected_cpo_qty(self, pc_page: Page):
        """TC-CUT-P1-004: 裁剪任务仅含选中CPO的订单数量"""
        pc_page.goto(f"{BASE_URL}/cutting/task/new")

        pc_page.check("input[name='cpo'][value='CPO1']")
        # 不选CPO2

        selected_qty = pc_page.locator("#selected-cpo-total-qty").inner_text()
        assert "500" in selected_qty
        assert "300" not in selected_qty

    # --- P2 测试 ---

    def test_no_cpo_selected_validation(self, pc_page: Page):
        """TC-CUT-P2-001: 不选择CPO时提交"""
        pc_page.goto(f"{BASE_URL}/cutting/task/new")
        pc_page.select_option("#marker-select", TEST_MARKER)
        pc_page.fill("#allocated-layers", "10")
        pc_page.click("#btn-submit")

        expect(pc_page.locator(".validation-error")).to_be_visible()
        error_text = pc_page.locator(".validation-error").inner_text()
        assert "选择" in error_text or "CPO" in error_text

    def test_marker_list_filters_used_up(self, pc_page: Page):
        """TC-CUT-P2-005: 唛架列表过滤-仅显示有剩余层数的"""
        pc_page.goto(f"{BASE_URL}/cutting/task/new")

        options = pc_page.locator("#marker-select option")
        option_texts = options.all_inner_texts()

        # 验证剩余0层的唛架不在列表中或标注不可用
        for text in option_texts:
            assert "0层" not in text or "disabled" in text.lower(), f"唛架{text}剩余0层但仍可选"


# ============================================================
# 模块2：床次任务与现场拉布测试
# ============================================================

class TestBedTask:
    """床次任务模块测试"""

    # --- P0 测试 ---

    def test_create_bed_basic_flow(self, pad_page: Page):
        """TC-BED-P0-001: 创建床次-基本流程"""
        # 进入裁剪任务
        pad_page.goto(f"{BASE_URL}/pad/cutting/tasks")
        pad_page.click(f"text={TEST_ORDER}")

        # 点击新增床次
        pad_page.click("#btn-new-bed")

        # 扫描布卷号
        pad_page.fill("#fabric-roll", "BR-2026-001")
        # 或使用扫描输入模拟
        # pad_page.fill("#fabric-roll-scan", "BR0001")

        # 输入拉布层数
        pad_page.fill("#layer-count", "30")

        # 确认创建
        pad_page.click("#btn-confirm-bed")

        # 验证成功
        expect(pad_page.locator(".bed-created-toast")).to_be_visible(timeout=5000)

        # 验证状态
        bed_status = pad_page.locator(".bed-status").inner_text()
        assert "拉布中" in bed_status

        # 验证剩余层数
        remaining = pad_page.locator("#remaining-layers").inner_text()
        assert "70" in remaining

    def test_bed_submit_complete(self, pad_page: Page):
        """TC-BED-P0-002: 床次提交完成-基本流程"""
        # 假设已有床次001在拉布中状态
        pad_page.goto(f"{BASE_URL}/pad/cutting/beds")

        # 找到拉布中的床次
        pad_page.click(".bed-row[data-status='spreading'] #btn-submit-complete")

        # 录入实际层数
        pad_page.fill("#actual-layers", "30")
        pad_page.click("#btn-confirm-complete")

        # 验证成功
        expect(pad_page.locator(".submit-success-toast")).to_be_visible(timeout=5000)
        expect(pad_page.locator(".bed-number")).not_to_be_empty()

    def test_anti_overcut_hard_block(self, pad_page: Page):
        """TC-BED-P0-003: 防超裁-强控禁止提交"""
        # 前置：已锁定80层，暂扣15层，剩余5层
        # 先确保任务状态
        pad_page.goto(f"{BASE_URL}/pad/cutting/tasks")
        pad_page.click(f"text={TEST_ORDER}")

        pad_page.click("#btn-new-bed")
        pad_page.fill("#fabric-roll", "BR-TEST-OVERCUT")
        pad_page.fill("#layer-count", "10")
        pad_page.click("#btn-confirm-bed")

        # 验证拒绝
        expect(pad_page.locator(".overcut-blocked-toast")).to_be_visible(timeout=5000)
        block_msg = pad_page.locator(".overcut-blocked-toast").inner_text()
        assert "超" in block_msg and ("计划" in block_msg or "审核" in block_msg)

    def test_task_status_transition_unstarted_to_spreading(self, pad_page: Page):
        """TC-BED-P0-006: 裁剪任务状态流转-未开始到拉布中"""
        # 假设任务A状态=未开始
        pad_page.goto(f"{BASE_URL}/pad/cutting/tasks")
        status_before = pad_page.locator(f"tr[data-task='task-unstarted'] .task-status").inner_text()
        assert "未开始" in status_before

        # 创建第一个床次
        pad_page.click("tr[data-task='task-unstarted']")
        pad_page.click("#btn-new-bed")
        pad_page.fill("#fabric-roll", "BR-STATUS-TEST")
        pad_page.fill("#layer-count", "10")
        pad_page.click("#btn-confirm-bed")

        # 验证状态变化
        pad_page.goto(f"{BASE_URL}/pad/cutting/tasks")
        status_after = pad_page.locator(f"tr[data-task='task-unstarted'] .task-status").inner_text()
        assert "拉布中" in status_after

    def test_edit_button_hidden_when_spreading(self, pc_page: Page):
        """TC-BED-P0-007: 裁剪任务编辑控制-拉布中不可编辑"""
        pc_page.goto(f"{BASE_URL}/cutting/tasks")

        # 找到拉布中状态的任务
        spreading_task = pc_page.locator("tr[data-status='spreading']").first
        spreading_task.click()

        # 验证编辑/删除按钮不可见
        expect(pc_page.locator("#btn-edit-task")).not_to_be_visible()
        expect(pc_page.locator("#btn-delete-task")).not_to_be_visible()

    # --- P1 测试 ---

    def test_concurrent_bed_creation(self, pad_page: Page):
        """TC-BED-P1-001: 多小组并发创建床次（模拟单PAD验证逻辑）"""
        pad_page.goto(f"{BASE_URL}/pad/cutting/tasks")
        pad_page.click(f"text={TEST_ORDER}")

        # 模拟：使用API查询实时剩余可用层数
        # 从UI读取当前剩余层数
        initial_remaining = int(pad_page.locator("#remaining-layers").inner_text())

        # 小组1创建35层
        pad_page.click("#btn-new-bed")
        pad_page.fill("#fabric-roll", "BR-CONCURRENT-1")
        pad_page.fill("#layer-count", "35")
        pad_page.click("#btn-confirm-bed")

        # 小组2创建35层
        pad_page.click("#btn-new-bed")
        pad_page.fill("#fabric-roll", "BR-CONCURRENT-2")
        pad_page.fill("#layer-count", "35")
        pad_page.click("#btn-confirm-bed")

        # 小组3尝试创建35层 - 应拦截
        pad_page.click("#btn-new-bed")
        pad_page.fill("#fabric-roll", "BR-CONCURRENT-3")
        pad_page.fill("#layer-count", "35")
        pad_page.click("#btn-confirm-bed")

        if initial_remaining >= 105:
            # 如果总层数足够，3个都应成功
            expect(pad_page.locator(".bed-created-toast")).to_be_visible()
        else:
            # 第3个应被拦截
            expect(pad_page.locator(".overcut-blocked-toast")).to_be_visible()

    def test_bed_submit_layer_validation(self, pad_page: Page):
        """TC-BED-P1-003: 床次提交完成-层数校验"""
        # 床次暂扣30层，剩余10层
        pad_page.goto(f"{BASE_URL}/pad/cutting/beds")
        pad_page.click(".bed-row[data-status='spreading'][data-hold='30'] #btn-submit-complete")

        # 尝试提交超出可调整范围的实际层数
        pad_page.fill("#actual-layers", "45")  # 30暂扣 + 10剩余 = 40上限, 45超出
        pad_page.click("#btn-confirm-complete")

        expect(pad_page.locator(".overcut-blocked-toast")).to_be_visible()
        error_text = pad_page.locator(".overcut-blocked-toast").inner_text()
        assert "超出" in error_text or "范围" in error_text

    def test_bed_list_sorted_by_bed_number(self, pad_page: Page):
        """TC-BED-P1-006: 床次列表按床次号升序"""
        pad_page.goto(f"{BASE_URL}/pad/cutting/beds")

        bed_numbers = pad_page.locator(".bed-number").all_inner_texts()
        # 验证升序
        numbers = [n.replace("床次-", "").replace("C-", "").replace("F-", "") for n in bed_numbers]
        for i in range(len(numbers) - 1):
            assert int(numbers[i]) <= int(numbers[i + 1]), f"床次号未按升序排列: {numbers[i]} > {numbers[i+1]}"

    def test_bed_number_generated_on_submit(self, pad_page: Page):
        """TC-BED-P1-007: 床次号生成时机-提交时非创建时"""
        pad_page.goto(f"{BASE_URL}/pad/cutting/tasks")
        pad_page.click(f"text={TEST_ORDER}")

        # 创建新床次
        pad_page.click("#btn-new-bed")
        pad_page.fill("#fabric-roll", "BR-NUMBER-TEST")
        pad_page.fill("#layer-count", "10")
        pad_page.click("#btn-confirm-bed")

        # 检查床次号是否为空（创建时不生成）
        bed_number_elem = pad_page.locator(".bed-row:last-child .bed-number")
        bed_number = bed_number_elem.inner_text() if bed_number_elem.is_visible() else ""
        assert bed_number == "" or bed_number == "-", "创建时不应有床次号"

        # 提交完成
        pad_page.click(".bed-row:last-child #btn-submit-complete")
        pad_page.fill("#actual-layers", "10")
        pad_page.click("#btn-confirm-complete")

        # 验证床次号已生成
        expect(pad_page.locator(".bed-row:last-child .bed-number")).not_to_be_empty()
        final_number = pad_page.locator(".bed-row:last-child .bed-number").inner_text()
        assert "床次-" in final_number or "C-" in final_number or "F-" in final_number

    # --- P2 测试 ---

    def test_anti_overcut_warning_threshold(self, pad_page: Page):
        """TC-BED-P2-001: 防超裁预警-剩余层数低于阈值"""
        # 需要配置任务总层数100，已使用91层
        pad_page.goto(f"{BASE_URL}/pad/cutting/tasks")
        pad_page.click(f"text=SO-THRESHOLD-TEST")

        pad_page.click("#btn-new-bed")
        pad_page.fill("#fabric-roll", "BR-THRESHOLD")
        pad_page.fill("#layer-count", "5")
        pad_page.click("#btn-confirm-bed")

        # 应弹出预警提示
        expect(pad_page.locator(".warning-toast")).to_be_visible(timeout=5000)
        warning = pad_page.locator(".warning-toast").inner_text()
        assert "不足" in warning or f"{THRESHOLD}" in warning

    def test_delete_task_when_unstarted(self, pc_page: Page):
        """TC-BED-P2-004: 未开始状态可删除裁剪任务"""
        pc_page.goto(f"{BASE_URL}/cutting/tasks")

        # 找到未开始的任务
        unstarted_task = pc_page.locator("tr[data-status='unstarted']").first
        task_name = unstarted_task.locator(".task-name").inner_text()
        unstarted_task.click()

        pc_page.click("#btn-delete-task")
        pc_page.click("#btn-confirm-delete")

        expect(pc_page.locator(".success-toast")).to_be_visible()
        # 验证任务已不在列表中
        pc_page.goto(f"{BASE_URL}/cutting/tasks")
        expect(pc_page.locator(f"text={task_name}")).not_to_be_visible()


# ============================================================
# 模块3：扎卡打印测试
# ============================================================

class TestCardPrinting:
    """扎卡打印模块测试"""

    def test_merged_cpo_hide_cpo_info(self, pc_page: Page):
        """TC-CARD-P0-001: 合并CPO-扎卡打印隐藏CPO信息"""
        pc_page.goto(f"{BASE_URL}/cutting/card/print")

        # 选择合并CPO的裁剪任务
        pc_page.click("tr[data-cpo-type='merged']")

        # 验证CPO选择区域不显示
        expect(pc_page.locator("#cpo-select-area")).not_to_be_visible()

        # 验证扎卡预览无CPO号
        card_preview = pc_page.locator("#card-preview").inner_text()
        assert "CPO" not in card_preview, "合并CPO扎卡不应显示CPO号"

    def test_single_cpo_show_cpo_info(self, pc_page: Page):
        """TC-CARD-P0-002: 单一CPO-扎卡打印显示CPO信息"""
        pc_page.goto(f"{BASE_URL}/cutting/card/print")

        # 选择单一CPO的裁剪任务
        pc_page.click("tr[data-cpo-type='single']")

        # 验证CPO信息显示
        expect(pc_page.locator("#cpo-info-area")).to_be_visible()
        cpo_info = pc_page.locator("#cpo-info-area").inner_text()
        assert "CPO1" in cpo_info
        assert "500" in cpo_info

        # 验证扎卡预览含CPO号
        card_preview = pc_page.locator("#card-preview").inner_text()
        assert "CPO1" in card_preview

    def test_merged_cpo_card_no_cpo_field(self, pc_page: Page):
        """TC-CARD-P1-001: 合并CPO-分扎计件不记录CPO"""
        pc_page.goto(f"{BASE_URL}/cutting/card/print")
        pc_page.click("tr[data-cpo-type='merged']")
        pc_page.fill("#print-count", "10")
        pc_page.click("#btn-print")

        # 验证打印记录
        pc_page.goto(f"{BASE_URL}/cutting/card/records")
        records = pc_page.locator(".card-record").all_inner_texts()
        for record in records:
            assert "CPO" not in record, "合并CPO扎卡记录不应含有CPO字段"

    def test_print_count_validation(self, pc_page: Page):
        """TC-CARD-P2-003: 扎卡打印数量校验"""
        pc_page.goto(f"{BASE_URL}/cutting/card/print")
        pc_page.click("tr[data-cpo-type='single']")
        pc_page.fill("#print-count", "1000")  # 超过订单总量
        pc_page.click("#btn-print")

        expect(pc_page.locator(".validation-error")).to_be_visible()


# ============================================================
# 模块4：缝制挂片测试
# ============================================================

class TestHangingOperation:
    """缝制挂片模块测试"""

    def test_auto_fill_merged_cpo_by_delivery(self, pad_page: Page):
        """TC-HANG-P0-001: 自动充数+合并CPO-按交期自动分配"""
        pad_page.goto(f"{BASE_URL}/pad/hanging")

        # 扫描通用扎卡
        pad_page.fill("#scan-card", "MERGE-CARD-001")
        pad_page.press("#scan-card", "Enter")

        # 验证系统自动选择交期最近的CPO
        active_cpo = pad_page.locator("#active-cpo").inner_text()
        assert "CPO1" in active_cpo, f"应自动选择交期最近的CPO1，实际选择了{active_cpo}"
        assert "7/1" in active_cpo

    def test_auto_fill_single_cpo_priority(self, pad_page: Page):
        """TC-HANG-P0-002: 自动充数+单一CPO-优先分配指定CPO"""
        pad_page.goto(f"{BASE_URL}/pad/hanging")

        # 扫描指定CPO1扎卡
        pad_page.fill("#scan-card", "CPO1-CARD-001")
        pad_page.press("#scan-card", "Enter")

        # 验证强制绑定CPO1
        active_cpo = pad_page.locator("#active-cpo").inner_text()
        assert "CPO1" in active_cpo

        # 尝试切换CPO应被限制（自动模式）
        # pad_page.click("#btn-manual-mode") -> 先切手动才允许

    def test_manual_fill_select_cpo(self, pad_page: Page):
        """TC-HANG-P0-003: 手动充数-选择CPO挂片"""
        pad_page.goto(f"{BASE_URL}/pad/hanging")

        # 切换到手动模式
        pad_page.click("#btn-manual-mode")

        # 查看CPO列表
        expect(pad_page.locator("#cpo-list")).to_be_visible()

        # 选择CPO2（非交期最近）
        pad_page.click("tr[data-cpo='CPO2']")

        # 验证选中
        expect(pad_page.locator("tr[data-cpo='CPO2'].selected")).to_be_visible()

        # 开始挂片
        pad_page.fill("#scan-card", "MANUAL-CARD-001")
        pad_page.press("#scan-card", "Enter")

        # 验证充入CPO2
        cpo2_qty_after = pad_page.locator("tr[data-cpo='CPO2'] .remaining-qty").inner_text()
        assert cpo2_qty_after != "300"  # 数量应减少

    def test_manual_cpo_full_block(self, pad_page: Page):
        """TC-HANG-P0-004: 手动充数-CPO满额禁止继续"""
        pad_page.goto(f"{BASE_URL}/pad/hanging")
        pad_page.click("#btn-manual-mode")

        # 选择即将满额的CPO
        pad_page.click("tr[data-cpo='CPO2'][data-remaining='0']")

        # 尝试挂片
        pad_page.fill("#scan-card", "FULL-CPO-TEST")
        pad_page.press("#scan-card", "Enter")

        # 验证满额提示
        expect(pad_page.locator(".cpo-full-toast")).to_be_visible(timeout=5000)
        full_msg = pad_page.locator(".cpo-full-toast").inner_text()
        assert "满" in full_msg or "切换" in full_msg

    def test_manual_switch_cpo_after_full(self, pad_page: Page):
        """TC-HANG-P0-005: 手动充数-满额后切换CPO"""
        pad_page.goto(f"{BASE_URL}/pad/hanging")
        pad_page.click("#btn-manual-mode")

        # CPO2已满额，切换CPO1
        pad_page.click("tr[data-cpo='CPO1']")
        pad_page.fill("#scan-card", "SWITCH-CPO-TEST")
        pad_page.press("#scan-card", "Enter")

        # 验证成功挂片到CPO1
        expect(pad_page.locator(".hanging-success-toast")).to_be_visible()
        active = pad_page.locator("#active-cpo").inner_text()
        assert "CPO1" in active

    def test_manual_cpo_list_sorted_by_delivery(self, pad_page: Page):
        """TC-HANG-P1-001: 手动模式CPO列表显示-按交期排序"""
        pad_page.goto(f"{BASE_URL}/pad/hanging")
        pad_page.click("#btn-manual-mode")

        # 获取CPO列表顺序
        cpo_rows = pad_page.locator("#cpo-list tr[data-cpo]")
        cpo_deliveries = []
        for i in range(cpo_rows.count()):
            delivery_text = cpo_rows.nth(i).locator(".cpo-delivery").inner_text()
            cpo_deliveries.append(delivery_text)

        # 验证交期是升序的
        dates = []
        for d in cpo_deliveries:
            match = re.search(r'(\d+)/(\d+)', d)
            if match:
                dates.append(datetime(2026, int(match.group(1)), int(match.group(2))))
        for i in range(len(dates) - 1):
            assert dates[i] <= dates[i + 1], f"CPO列表未按交期排序: {dates[i]} > {dates[i+1]}"

    def test_manual_free_selection_ignore_delivery(self, pad_page: Page):
        """TC-HANG-P1-003: 手动模式自由选择-无视交期"""
        pad_page.goto(f"{BASE_URL}/pad/hanging")
        pad_page.click("#btn-manual-mode")

        # 选择交期最晚的CPO
        latest_cpo = pad_page.locator("#cpo-list tr[data-cpo]").last
        latest_cpo.click()

        # 应能成功选择，无限制提示
        expect(pad_page.locator("tr[data-cpo].selected")).to_be_visible()

    def test_auto_to_manual_mode_switch(self, pad_page: Page):
        """TC-HANG-P1-004: 自动→手动模式切换"""
        pad_page.goto(f"{BASE_URL}/pad/hanging")

        # 当前在自动模式
        current_progress = pad_page.locator("#total-hung-qty").inner_text()

        # 切换到手动
        pad_page.click("#btn-manual-mode")

        # 验证切换成功
        expect(pad_page.locator(".mode-switch-toast")).to_be_visible()
        expect(pad_page.locator("#cpo-list")).to_be_visible()

    def test_manual_to_auto_mode_switch(self, pad_page: Page):
        """TC-HANG-P1-005: 手动→自动模式切换"""
        pad_page.goto(f"{BASE_URL}/pad/hanging")
        pad_page.click("#btn-manual-mode")

        # 切换回自动
        pad_page.click("#btn-auto-mode")

        # 验证切换成功并自动选择CPO
        expect(pad_page.locator(".mode-switch-toast")).to_be_visible()
        expect(pad_page.locator("#active-cpo")).not_to_be_empty()

    def test_manual_only_show_unfilled_cpos(self, pad_page: Page):
        """TC-HANG-P2-002: 手动模式-仅显示未满额CPO"""
        pad_page.goto(f"{BASE_URL}/pad/hanging")
        pad_page.click("#btn-manual-mode")

        # 验证所有显示的CPO剩余量>0
        cpo_rows = pad_page.locator("#cpo-list tr[data-cpo]")
        for i in range(cpo_rows.count()):
            remaining_text = cpo_rows.nth(i).locator(".remaining-qty").inner_text()
            remaining = int(re.search(r'\d+', remaining_text).group())
            assert remaining > 0, f"列表中显示了满额CPO: {remaining=}"


# ============================================================
# 模块5：超裁审核测试
# ============================================================

class TestOvercutAudit:
    """超裁审核模块测试"""

    def test_overcut_trigger_audit_button(self, pc_page: Page):
        """TC-OVR-P0-001: 超裁触发-PC端审核按钮出现"""
        # 模拟已触发超裁的裁剪任务
        pc_page.goto(f"{BASE_URL}/cutting/tasks")
        pc_page.click("tr[data-has-overcut='true']")

        # 验证审核按钮
        expect(pc_page.locator("#btn-apply-overcut")).to_be_visible()

    def test_overcut_audit_approve(self, pc_page: Page):
        """TC-OVR-P0-002: 超裁审核-放行流程"""
        pc_page.goto(f"{BASE_URL}/cutting/tasks")
        pc_page.click("tr[data-has-overcut='true']")
        pc_page.click("#btn-apply-overcut")

        # 审核页面
        expect(pc_page.locator("#overcut-audit-dialog")).to_be_visible()

        # 放行 - 增加计划层数
        pc_page.fill("#additional-layers", "20")
        pc_page.click("#btn-approve")

        expect(pc_page.locator(".success-toast")).to_be_visible()

        # 验证计划层数已更新
        new_plan_layers = pc_page.locator("#plan-layers").inner_text()
        assert "120" in new_plan_layers

    def test_overcut_audit_reject(self, pc_page: Page):
        """TC-OVR-P1-001: 超裁审核-驳回流程"""
        pc_page.goto(f"{BASE_URL}/cutting/tasks")
        pc_page.click("tr[data-has-overcut='true']")
        pc_page.click("#btn-apply-overcut")

        pc_page.click("#btn-reject")
        pc_page.fill("#reject-reason", "请调整层数，优先完成已有任务")
        pc_page.click("#btn-confirm-reject")

        expect(pc_page.locator(".success-toast")).to_be_visible()
        # 验证审核按钮消失
        expect(pc_page.locator("#btn-apply-overcut")).not_to_be_visible()

    def test_overcut_pad_prompt_accuracy(self, pad_page: Page):
        """TC-OVR-P1-002: 超裁触发后PAD端提示准确"""
        pad_page.goto(f"{BASE_URL}/pad/cutting/tasks")
        pad_page.click(f"text={TEST_ORDER}")

        pad_page.click("#btn-new-bed")
        pad_page.fill("#fabric-roll", "BR-OVERTEST")
        pad_page.fill("#layer-count", "999")  # 远超计划
        pad_page.click("#btn-confirm-bed")

        expect(pad_page.locator(".overcut-blocked-toast")).to_be_visible()
        msg = pad_page.locator(".overcut-blocked-toast").inner_text()
        assert "超" in msg and "计划" in msg and ("审核" in msg or "PC" in msg)


# ============================================================
# 端到端集成测试
# ============================================================

class TestEndToEnd:
    """端到端集成测试"""

    def test_e2e_single_cpo_full_flow(self, pc_page: Page, pad_page: Page):
        """TC-E2E-P0-001: 完整流程-单一CPO端到端"""
        # Step 1: PC创建单一CPO裁剪任务
        pc_page.goto(f"{BASE_URL}/cutting/task/new")
        pc_page.check("input[name='cpo'][value='CPO1']")
        pc_page.select_option("#marker-select", TEST_MARKER)
        pc_page.fill("#allocated-layers", "60")
        pc_page.click("#btn-submit")
        expect(pc_page.locator(".success-toast")).to_be_visible()

        # Step 2: PAD创建床次-001
        pad_page.goto(f"{BASE_URL}/pad/cutting/tasks")
        pad_page.click(f"text={TEST_ORDER}")
        pad_page.click("#btn-new-bed")
        pad_page.fill("#fabric-roll", "BR-E2E-001")
        pad_page.fill("#layer-count", "30")
        pad_page.click("#btn-confirm-bed")
        pad_page.click("#btn-submit-complete")
        pad_page.fill("#actual-layers", "30")
        pad_page.click("#btn-confirm-complete")
        expect(pad_page.locator(".submit-success-toast")).to_be_visible()
        assert "床次-001" in pad_page.locator(".bed-number").inner_text()

        # Step 3: PAD创建床次-002
        pad_page.click("#btn-new-bed")
        pad_page.fill("#fabric-roll", "BR-E2E-002")
        pad_page.fill("#layer-count", "30")
        pad_page.click("#btn-confirm-bed")
        pad_page.click("#btn-submit-complete")
        pad_page.fill("#actual-layers", "30")
        pad_page.click("#btn-confirm-complete")

        # Step 4: 验证裁剪任务完成
        pc_page.goto(f"{BASE_URL}/cutting/tasks")
        status = pc_page.locator(f"tr[data-task='CPO1-{TEST_ORDER}'] .task-status").inner_text()
        assert "已完成" in status

        # Step 5: 扎卡打印（应显示CPO1）
        pc_page.goto(f"{BASE_URL}/cutting/card/print")
        pc_page.click(f"tr[data-task='CPO1-{TEST_ORDER}']")
        card_preview = pc_page.locator("#card-preview").inner_text()
        assert "CPO1" in card_preview

        # Step 6: 挂片-自动充入CPO1
        pad_page.goto(f"{BASE_URL}/pad/hanging")
        pad_page.fill("#scan-card", "CPO1-CARD-E2E")
        pad_page.press("#scan-card", "Enter")
        active_cpo = pad_page.locator("#active-cpo").inner_text()
        assert "CPO1" in active_cpo

    def test_e2e_merged_cpo_full_flow(self, pc_page: Page, pad_page: Page):
        """TC-E2E-P0-002: 完整流程-合并CPO端到端"""
        # Step 1: PC智能合并创建裁剪任务
        pc_page.goto(f"{BASE_URL}/cutting/task/new")
        pc_page.click("#btn-smart-merge")
        # 确认合并组
        pc_page.click(".cpo-merge-group:first-child #btn-use-group")
        pc_page.select_option("#marker-select", TEST_MARKER)
        pc_page.fill("#allocated-layers", "80")
        pc_page.click("#btn-submit")
        expect(pc_page.locator(".success-toast")).to_be_visible()

        # Step 2: PAD拉布
        pad_page.goto(f"{BASE_URL}/pad/cutting/tasks")
        pad_page.click("tr[data-cpo-type='merged']")
        pad_page.click("#btn-new-bed")
        pad_page.fill("#fabric-roll", "BR-MERGED-E2E")
        pad_page.fill("#layer-count", "40")
        pad_page.click("#btn-confirm-bed")
        pad_page.click("#btn-submit-complete")
        pad_page.fill("#actual-layers", "40")
        pad_page.click("#btn-confirm-complete")

        # Step 3: 扎卡打印-验证无CPO号
        pc_page.goto(f"{BASE_URL}/cutting/card/print")
        pc_page.click("tr[data-cpo-type='merged']")
        card_preview = pc_page.locator("#card-preview").inner_text()
        assert "CPO" not in card_preview

        # Step 4: 挂片-自动按交期分配
        pad_page.goto(f"{BASE_URL}/pad/hanging")
        pad_page.fill("#scan-card", "MERGE-CARD-E2E")
        pad_page.press("#scan-card", "Enter")
        active_cpo = pad_page.locator("#active-cpo").inner_text()
        assert "CPO1" in active_cpo  # 交期7/1最近


# ============================================================
# 数据驱动测试
# ============================================================

@pytest.mark.parametrize("allocated,expected_result", [
    (0, "reject"),
    (-1, "reject"),
    (1, "success"),
    (50, "success"),
    (100, "success"),
    (101, "reject"),
])
def test_marker_layer_boundary_values(pc_page: Page, allocated, expected_result):
    """数据驱动: 唛架层数边界值测试"""
    pc_page.goto(f"{BASE_URL}/cutting/task/new")
    pc_page.check("input[name='cpo'][value='CPO1']")
    pc_page.select_option("#marker-select", TEST_MARKER)

    pc_page.fill("#allocated-layers", str(allocated))
    pc_page.click("#btn-submit")

    if expected_result == "success":
        expect(pc_page.locator(".success-toast")).to_be_visible(timeout=5000)
    else:
        expect(pc_page.locator(".error-toast, .validation-error")).to_be_visible(timeout=5000)


@pytest.mark.parametrize("scenario,cpo_list,expected_behavior", [
    ("single_cpo", ["CPO1"], "show_cpo"),
    ("merged_cpo", ["CPO1", "CPO2", "CPO3"], "hide_cpo"),
])
def test_card_printing_cpo_display_rule(pc_page: Page, scenario, cpo_list, expected_behavior):
    """数据驱动: 扎卡打印CPO显示规则"""
    # 先创建对应场景的裁剪任务
    pc_page.goto(f"{BASE_URL}/cutting/task/new")
    for cpo in cpo_list:
        pc_page.check(f"input[name='cpo'][value='{cpo}']")
    pc_page.select_option("#marker-select", TEST_MARKER)
    pc_page.fill("#allocated-layers", "50")
    pc_page.click("#btn-submit")
    expect(pc_page.locator(".success-toast")).to_be_visible()

    # 进入扎卡打印
    pc_page.goto(f"{BASE_URL}/cutting/card/print")
    pc_page.click("tr.cutting-task-row:last-child")

    if expected_behavior == "show_cpo":
        expect(pc_page.locator("#cpo-info-area")).to_be_visible()
        assert "CPO" in pc_page.locator("#card-preview").inner_text()
    else:
        expect(pc_page.locator("#cpo-select-area")).not_to_be_visible()
        assert "CPO" not in pc_page.locator("#card-preview").inner_text()


# ============================================================
# 并发测试辅助方法
# ============================================================

def simulate_concurrent_bed_creation(pages: list[Page], task_url: str, layers: list[int]) -> list[bool]:
    """
    模拟多页面并发创建床次
    返回每个操作是否成功
    """
    results = []

    # 同时导航到任务页面
    for i, page in enumerate(pages):
        page.goto(task_url)
        page.click("#btn-new-bed")
        page.fill("#fabric-roll", f"BR-CONCURRENT-{i}")
        page.fill("#layer-count", str(layers[i]))

    # 近乎同时点击确认
    for page in pages:
        page.click("#btn-confirm-bed")

    # 收集结果
    for page in pages:
        time.sleep(1)
        if page.locator(".bed-created-toast").is_visible():
            results.append(True)
        else:
            results.append(False)

    return results


# ============================================================
# 运行配置
# ============================================================

if __name__ == "__main__":
    # 运行所有测试
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--html=test_report.html",
        "--self-contained-html",
        "-n", "auto",  # 并行运行
    ])
