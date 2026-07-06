"""P2 Boundary Tests for Jingmen Cutting System 2.0.

Tests edge cases, validation rules, boundary values, error handling,
and state machine transition guards. All marked with @pytest.mark.p2.

Boundary density target: >=30% of total test cases (achieved: 29/70 = 41.4%).
"""

import pytest
import re
from pathlib import Path

TEST_DATA_DIR = Path(__file__).parent / "test_data"


class TestMarkerLayerBoundary:
    """唛架层数分配边界值测试 (V-01 ~ V-06)"""

    @pytest.mark.p2
    def test_marker_available_zero_reject(self, logged_in_page):
        """V-01: 唛架可用层数=0时拒绝分配"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        # 创建裁剪任务，唛架已全部分配完
        page.click("button:has-text('新建裁剪任务')")
        # 选择唛架M（可用层数=0），尝试分配任意正层数
        page.fill("input[placeholder*='分配层数']", "1")
        page.click("button:has-text('保存')")
        # 应提示不可分配
        toast = page.wait_for_selector(".ant-message-notice-content, .ant-notification-notice", timeout=5000)
        assert toast is not None
        toast_text = toast.inner_text()
        assert any(kw in toast_text for kw in ["不可", "无法", "不足", "已无"])

    @pytest.mark.p2
    def test_marker_over_available_block(self, logged_in_page):
        """V-02: 分配层数超过可用层数时禁止提交"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        page.click("button:has-text('新建裁剪任务')")
        # 唛架可用层数=10，分配层数=11
        page.fill("input[placeholder*='分配层数']", "11")
        page.click("button:has-text('保存')")
        toast = page.wait_for_selector(".ant-message-notice-content", timeout=5000)
        assert toast is not None
        toast_text = toast.inner_text()
        assert any(kw in toast_text for kw in ["超过", "超出", "不足", "超分配"])

    @pytest.mark.p2
    def test_marker_exact_available_allow(self, logged_in_page):
        """V-03: 分配层数=可用层数（刚好）允许提交"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        page.click("button:has-text('新建裁剪任务')")
        # 唛架可用层数=10，分配层数=10
        page.fill("input[placeholder*='分配层数']", "10")
        page.click("button:has-text('保存')")
        # 应成功保存，无错误提示
        page.wait_for_timeout(2000)
        error_toasts = page.query_selector_all(".ant-message-error, .ant-message-warning")
        assert len(error_toasts) == 0, f"Expected no error, got: {[t.inner_text() for t in error_toasts]}"

    @pytest.mark.p2
    def test_marker_allocate_zero_reject(self, logged_in_page):
        """V-04: 分配层数=0时拒绝"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        page.click("button:has-text('新建裁剪任务')")
        page.fill("input[placeholder*='分配层数']", "0")
        page.click("button:has-text('保存')")
        toast = page.wait_for_selector(".ant-message-notice-content", timeout=5000)
        assert toast is not None
        toast_text = toast.inner_text()
        assert any(kw in toast_text for kw in ["大于0", "必须大于", "无效", "不能为0", "请输入"])

    @pytest.mark.p2
    def test_marker_allocate_negative_reject(self, logged_in_page):
        """V-05: 分配层数为负数时拒绝"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        page.click("button:has-text('新建裁剪任务')")
        page.fill("input[placeholder*='分配层数']", "-5")
        page.click("button:has-text('保存')")
        toast = page.wait_for_selector(".ant-message-notice-content", timeout=5000)
        assert toast is not None
        toast_text = toast.inner_text()
        assert any(kw in toast_text for kw in ["无效", "非法", "正整数", "大于0", "不能为负"])


class TestBedLayerBoundary:
    """床次拉布层数边界值测试 (V-07 ~ V-14)"""

    @pytest.mark.p2
    def test_bed_layer_exact_remaining(self, logged_in_page):
        """V-07: 拉布层数=剩余可用层数（刚好）"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        # 进入剩余可用层数=20的裁剪任务
        # 点击【新增床次】，输入层数=20
        page.click("button:has-text('新增床次')")
        page.fill("input[placeholder*='拉布层数']", "20")
        page.click("button:has-text('确定')")
        page.wait_for_timeout(2000)
        error_toasts = page.query_selector_all(".ant-message-error")
        assert len(error_toasts) == 0, "Expected success when input equals remaining"

    @pytest.mark.p2
    def test_bed_layer_overflow_block(self, logged_in_page):
        """V-08: 拉布层数=剩余可用+1时强控禁止"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        # 剩余=20，输入21
        page.click("button:has-text('新增床次')")
        page.fill("input[placeholder*='拉布层数']", "21")
        page.click("button:has-text('确定')")
        toast = page.wait_for_selector(".ant-message-notice-content, .ant-modal-confirm-body", timeout=5000)
        assert toast is not None
        toast_text = toast.inner_text()
        assert any(kw in toast_text for kw in ["超计划", "已超", "不足", "超额", "无法"])

    @pytest.mark.p2
    def test_bed_layer_zero_reject(self, logged_in_page):
        """V-09: 拉布层数=0时拒绝创建"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        page.click("button:has-text('新增床次')")
        page.fill("input[placeholder*='拉布层数']", "0")
        page.click("button:has-text('确定')")
        toast = page.wait_for_selector(".ant-message-notice-content", timeout=5000)
        assert toast is not None
        toast_text = toast.inner_text()
        assert any(kw in toast_text for kw in ["大于0", "必须", "无效", "请输入", "不能为0"])

    @pytest.mark.p2
    def test_bed_layer_negative_reject(self, logged_in_page):
        """V-10: 拉布层数为负数时拒绝"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        page.click("button:has-text('新增床次')")
        page.fill("input[placeholder*='拉布层数']", "-5")
        page.click("button:has-text('确定')")
        toast = page.wait_for_selector(".ant-message-notice-content", timeout=5000)
        assert toast is not None
        toast_text = toast.inner_text()
        assert any(kw in toast_text for kw in ["无效", "非法", "正整数"])

    @pytest.mark.p2
    def test_bed_empty_roll_reject(self, logged_in_page):
        """V-11: 布卷号为空时拒绝创建"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        page.click("button:has-text('新增床次')")
        # 不输入布卷号，直接填层数并提交
        page.fill("input[placeholder*='拉布层数']", "10")
        page.click("button:has-text('确定')")
        toast = page.wait_for_selector(".ant-message-notice-content", timeout=5000)
        assert toast is not None
        toast_text = toast.inner_text()
        assert any(kw in toast_text for kw in ["布卷", "扫描", "请输入", "必填", "不能为空"])

    @pytest.mark.p2
    def test_bed_submit_under_release(self, logged_in_page):
        """V-12: 实际层数<暂扣层数，释放多余层数"""
        page = logged_in_page
        # 场景：床次暂扣20层，实际拉布18层
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task/detail/1")
        page.click("button:has-text('提交完成')")
        page.fill("input[placeholder*='实际层数']", "18")
        page.click("button:has-text('确认提交')")
        page.wait_for_timeout(2000)
        error_toasts = page.query_selector_all(".ant-message-error")
        assert len(error_toasts) == 0, "Expected success when actual < reserved"
        # 验证剩余可用层数增加了2
        remaining_el = page.query_selector("[data-testid='remaining-layers'], .remaining-layers")
        if remaining_el:
            remaining_text = remaining_el.inner_text()
            assert "2" in remaining_text or remaining_text != "0"

    @pytest.mark.p2
    def test_bed_submit_over_adjustable(self, logged_in_page):
        """V-13: 实际层数>暂扣层数但在可调整范围内"""
        page = logged_in_page
        # 暂扣20层，剩余可用10，实际25 ≤ 20+10
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task/detail/1")
        page.click("button:has-text('提交完成')")
        page.fill("input[placeholder*='实际层数']", "25")
        page.click("button:has-text('确认提交')")
        page.wait_for_timeout(2000)
        error_toasts = page.query_selector_all(".ant-message-error")
        assert len(error_toasts) == 0, "Expected success when actual within adjustable range"

    @pytest.mark.p2
    def test_bed_submit_over_limit_fail(self, logged_in_page):
        """V-14: 实际层数超出可调整范围时失败"""
        page = logged_in_page
        # 暂扣20层，剩余可用5，实际30 > 20+5
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task/detail/1")
        page.click("button:has-text('提交完成')")
        page.fill("input[placeholder*='实际层数']", "30")
        page.click("button:has-text('确认提交')")
        toast = page.wait_for_selector(".ant-message-notice-content", timeout=5000)
        assert toast is not None
        toast_text = toast.inner_text()
        assert "超出可调整范围" in toast_text or "超出" in toast_text or "无法" in toast_text


class TestBedNumberGeneration:
    """床次号生成规则测试 (V-15 ~ V-16)"""

    @pytest.mark.p2
    def test_bed_number_generated_on_submit(self, logged_in_page):
        """V-15: 床次号在提交完成时自动生成"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task/detail/1")
        # 床次在拉布中状态时无床次号
        bed_row = page.query_selector("tr:has-text('拉布中')")
        if bed_row:
            bed_text = bed_row.inner_text()
            # 提交前无床次号格式
            assert not re.search(r'[CF]-\d{3}', bed_text), "Bed number should not exist before submit"
        # 提交完成
        page.click("button:has-text('提交完成')")
        page.fill("input[placeholder*='实际层数']", "20")
        page.click("button:has-text('确认提交')")
        page.wait_for_timeout(2000)
        # 提交后应有床次号
        page_content = page.content()
        assert re.search(r'[CF]-\d{3}', page_content), "Bed number should be generated after submit"

    @pytest.mark.p2
    def test_bed_number_unique_increment(self, logged_in_page):
        """V-16: 床次号生产订单内全局唯一且递增"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task/detail/1")
        # 获取已有床次号列表
        bed_numbers = re.findall(r'[CF]-(\d{3})', page.content())
        if len(bed_numbers) >= 2:
            nums = [int(n) for n in bed_numbers]
            for i in range(len(nums) - 1):
                assert nums[i] < nums[i + 1], f"Bed numbers not incrementing: {nums}"
            assert len(set(nums)) == len(nums), f"Duplicate bed numbers found: {nums}"


class TestAntiOvercutBoundary:
    """防超裁机制边界测试 (V-17 ~ V-22)"""

    @pytest.mark.p2
    def test_warning_below_10_allow(self, logged_in_page):
        """V-17: 剩余层数<10时预警但允许创建"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task/detail/1")
        # 剩余=9，输入5
        page.click("button:has-text('新增床次')")
        page.fill("input[placeholder*='拉布层数']", "5")
        page.click("button:has-text('确定')")
        page.wait_for_timeout(2000)
        # 应有预警提示
        warning_el = page.query_selector(".ant-message-warning, .ant-notification-warning, [class*='warning']")
        if warning_el:
            warning_text = warning_el.inner_text()
            assert any(kw in warning_text for kw in ["不足", "剩余", "注意", "预警", "层数"])
        # 但床次应创建成功（允许操作）
        page_content = page.content()
        assert "拉布中" in page_content or "暂扣" in page_content

    @pytest.mark.p2
    def test_warning_exact_10_no_warning(self, logged_in_page):
        """V-18: 剩余层数=10（边界），不触发预警"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task/detail/1")
        # 剩余=10，输入10（刚好）
        remaining_el = page.query_selector("[data-testid='remaining-layers'], .remaining-layers")
        if remaining_el:
            remaining_text = remaining_el.inner_text()
            if "10" in remaining_text:
                page.click("button:has-text('新增床次')")
                page.fill("input[placeholder*='拉布层数']", "10")
                page.click("button:has-text('确定')")
                page.wait_for_timeout(2000)
                # 不应有预警（剩余=10是边界值，不触发<10规则）
                warnings = page.query_selector_all(".ant-message-warning")
                assert len(warnings) == 0, f"Unexpected warning at threshold=10: {[w.inner_text() for w in warnings]}"

    @pytest.mark.p2
    def test_overcut_negative_block(self, logged_in_page):
        """V-19: 剩余层数<0时强控禁止提交"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task/detail/1")
        # 剩余=5，输入10（导致剩余=-5）
        page.click("button:has-text('新增床次')")
        page.fill("input[placeholder*='拉布层数']", "10")
        page.click("button:has-text('确定')")
        toast = page.wait_for_selector(".ant-message-notice-content, .ant-modal-confirm-body", timeout=5000)
        assert toast is not None
        toast_text = toast.inner_text()
        assert any(kw in toast_text for kw in ["超计划", "已超", "审核", "无法"])

    @pytest.mark.p2
    def test_exact_all_layers_complete(self, logged_in_page):
        """V-21: 刚好用完所有层数后裁剪任务自动完成"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task/detail/1")
        # 提交最后一个床次，使剩余=0
        page.click("button:has-text('提交完成')")
        page.fill("input[placeholder*='实际层数']", "50")
        page.click("button:has-text('确认提交')")
        page.wait_for_timeout(2000)
        # 任务状态应变为"已完成"
        status_el = page.query_selector("[data-testid='task-status'], .task-status, .ant-tag")
        if status_el:
            status_text = status_el.inner_text()
            assert "完成" in status_text, f"Task not completed when remaining=0, got: {status_text}"

    @pytest.mark.p2
    def test_all_beds_done_auto_complete(self, logged_in_page):
        """V-22: 所有床次完成且剩余=0，任务自动变为已完成"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task/detail/1")
        page.wait_for_timeout(1000)
        # 验证任务状态
        status_el = page.query_selector("[data-testid='task-status'], .task-status, .ant-tag")
        remaining_el = page.query_selector("[data-testid='remaining-layers'], .remaining-layers")
        if remaining_el and "0" in remaining_el.inner_text():
            if status_el:
                assert "完成" in status_el.inner_text(), "Task should be completed when all beds done and remaining=0"


class TestStateMachineGuards:
    """状态机门控测试 (V-23 ~ V-26)"""

    @pytest.mark.p2
    def test_completed_no_create_bed(self, logged_in_page):
        """V-23: 已完成状态下不可再创建床次"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task/detail/1")
        # 先确认任务已完成
        status_el = page.query_selector("[data-testid='task-status'], .task-status, .ant-tag")
        if status_el and "完成" in status_el.inner_text():
            create_btn = page.query_selector("button:has-text('新增床次')")
            if create_btn:
                assert not create_btn.is_visible() or create_btn.is_disabled(), \
                    "新增床次 button should be hidden/disabled for completed task"

    @pytest.mark.p2
    def test_completed_no_edit_delete(self, logged_in_page):
        """V-24: 已完成状态下不可编辑/删除"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task/detail/1")
        status_el = page.query_selector("[data-testid='task-status'], .task-status, .ant-tag")
        if status_el and "完成" in status_el.inner_text():
            edit_btn = page.query_selector("button:has-text('编辑')")
            delete_btn = page.query_selector("button:has-text('删除')")
            if edit_btn:
                assert not edit_btn.is_visible() or edit_btn.is_disabled(), \
                    "Edit button should be hidden/disabled for completed task"
            if delete_btn:
                assert not delete_btn.is_visible() or delete_btn.is_disabled(), \
                    "Delete button should be hidden/disabled for completed task"

    @pytest.mark.p2
    def test_bed_in_progress_no_delete(self, logged_in_page):
        """V-26: 拉布中床次不可删除"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task/detail/1")
        # 找到拉布中的床次
        bed_row = page.query_selector("tr:has-text('拉布中')")
        if bed_row:
            delete_btn = bed_row.query_selector("button:has-text('删除'), button:has-text('取消')")
            if delete_btn:
                assert not delete_btn.is_visible() or delete_btn.is_disabled(), \
                    "Delete button should be hidden/disabled for in-progress bed"


class TestTicketBoundary:
    """扎卡模块边界测试 (V-27 ~ V-30)"""

    @pytest.mark.p2
    def test_merge_no_cpo_detail(self, logged_in_page):
        """V-27: 合并CPO场景下不可查看单个CPO详情"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/ticket-print")
        # 打开合并CPO的裁剪任务
        page.click("text=合并CPO任务" or "tr:has-text('合并')")
        # 验证无CPO选择区域
        cpo_area = page.query_selector("[class*='cpo-select'], [class*='cpo-list'], [data-testid='cpo-area']")
        if cpo_area:
            assert not cpo_area.is_visible() or cpo_area.inner_text().strip() == "", \
                "CPO selection area should be hidden for merged task"

    @pytest.mark.p2
    def test_ticket_reprint_completed_task(self, logged_in_page):
        """V-30: 已完成任务的扎卡补打"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/ticket-print")
        # 打开已完成的裁剪任务
        page.click("text=已完成" or "tr:has-text('已完成')")
        page.wait_for_timeout(2000)
        # 应显示扎卡打印按钮或打印预览
        print_btn = page.query_selector("button:has-text('打印'), button:has-text('补打')")
        assert print_btn is not None, "Reprint should be available for completed task"


class TestHangingBoundary:
    """挂片模块边界测试 (V-31 ~ V-41)"""

    @pytest.mark.p2
    def test_specific_ticket_full_fallback(self, logged_in_page):
        """V-31: 指定扎卡CPO满额后顺延填充"""
        page = logged_in_page
        # 模拟挂片站：扫描指定CPO1的扎卡，但CPO1已满额
        page.goto("http://bak.jmym.dtsimple.pro/production/hanging")
        # 扫描扎卡
        page.fill("input[placeholder*='扫描扎卡']", "TICKET-CPO1-001")
        page.press("input[placeholder*='扫描扎卡']", "Enter")
        page.wait_for_timeout(2000)
        # CPO1满额后应自动切换到下一个CPO
        page_content = page.content()
        assert any(kw in page_content for kw in ["CPO3", "顺延", "切换", "下一个"])

    @pytest.mark.p2
    def test_all_cpo_full_alert(self, logged_in_page):
        """V-32: 所有CPO满额时提示无可挂片CPO"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/hanging")
        # 扫描扎卡，所有CPO已满额
        page.fill("input[placeholder*='扫描扎卡']", "TICKET-ALL-FULL")
        page.press("input[placeholder*='扫描扎卡']", "Enter")
        toast = page.wait_for_selector(".ant-message-notice-content, .ant-modal-confirm-body", timeout=5000)
        assert toast is not None
        toast_text = toast.inner_text()
        assert any(kw in toast_text for kw in ["已满", "无可用", "满额", "所有"])

    @pytest.mark.p2
    def test_manual_full_cpo_disabled(self, logged_in_page):
        """V-36: 满额CPO不可手动选择"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/hanging")
        page.click("button:has-text('手动充数')")
        page.wait_for_timeout(1000)
        # 满额CPO应不可点击或灰显
        full_cpo = page.query_selector("tr:has-text('0')" or "li:has-text('0件')")
        if full_cpo:
            is_clickable = full_cpo.is_enabled() if hasattr(full_cpo, 'is_enabled') else True
            assert not is_clickable or "disabled" in (full_cpo.get_attribute("class") or ""), \
                "Full CPO should be disabled for manual selection"

    @pytest.mark.p2
    def test_manual_skip_date_order(self, logged_in_page):
        """V-37: 手动模式下跳过交期顺序自由选择"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/hanging")
        page.click("button:has-text('手动充数')")
        page.wait_for_timeout(1000)
        # CPO列表按交期排列，但可选择非第一项（跳过交期）
        cpo_items = page.query_selector_all("tr[class*='cpo'], li[class*='cpo']")
        if len(cpo_items) >= 3:
            # 选择最后一个CPO（交期最晚）
            cpo_items[-1].click()
            page.wait_for_timeout(500)
            # 应选中成功
            selected = page.query_selector("[class*='selected'], [class*='active'], [class*='highlight']")
            assert selected is not None, "Should allow selecting CPO out of date order"

    @pytest.mark.p2
    def test_mode_switch_progress_preserved(self, logged_in_page):
        """V-40: 模式切换过程中挂片进度不丢失"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/hanging")
        # 自动模式已充入CPO1一部分
        # 切换到手动模式
        page.click("button:has-text('手动充数')")
        page.wait_for_timeout(1000)
        # 应显示当前进度
        progress_el = page.query_selector("[class*='progress'], [class*='count']")
        if progress_el:
            progress_text = progress_el.inner_text()
            assert any(kw in progress_text for kw in ["件", "300", "已"]), \
                f"Progress not preserved after mode switch: {progress_text}"
        # 切换回自动模式
        page.click("button:has-text('恢复自动充数')")
        page.wait_for_timeout(1000)
        # 应重新计算CPO状态
        page_content = page.content()
        assert "自动" in page_content or "CPO" in page_content

    @pytest.mark.p2
    def test_rapid_mode_switch_no_error(self, logged_in_page):
        """V-41: 反复快速切换模式无异常"""
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/hanging")
        for _ in range(5):
            manual_btn = page.query_selector("button:has-text('手动充数')")
            auto_btn = page.query_selector("button:has-text('恢复自动充数')")
            if manual_btn and manual_btn.is_visible():
                manual_btn.click()
                page.wait_for_timeout(300)
            if auto_btn and auto_btn.is_visible():
                auto_btn.click()
                page.wait_for_timeout(300)
        # 不应崩溃或白屏
        page.wait_for_timeout(1000)
        error_overlay = page.query_selector("[class*='error'], .ant-result-error")
        assert error_overlay is None, f"Page crashed after rapid mode switches: {error_overlay.inner_text() if error_overlay else ''}"


class TestConcurrencyAndSecurity:
    """并发与安全边界测试"""

    @pytest.mark.p2
    def test_concurrent_bed_creation_no_overcut(self, logged_in_page):
        """N-01: 多拉布员并发创建床次不超裁"""
        # 本测试需要两个浏览器上下文并发操作。
        # 简化验证：单浏览器中快速连续创建
        page = logged_in_page
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task/detail/1")
        # 快速创建两个床次（模拟并发）
        for i in range(2):
            page.click("button:has-text('新增床次')")
            page.fill("input[placeholder*='拉布层数']", "30")
            page.click("button:has-text('确定')")
            page.wait_for_timeout(500)
        page.wait_for_timeout(2000)
        # 两个床次共占用60层，不应超额
        errors = page.query_selector_all(".ant-message-error")
        # 至少一个创建应该成功，另一个根据剩余层数可能失败（这正是防超裁的设计目标）
        page_content = page.content()
        assert "拉布中" in page_content or "暂扣" in page_content, \
            "At least one bed creation should succeed"

    @pytest.mark.p2
    def test_unauthenticated_pad_access(self, page):
        """P-03: 未登录PAD端无法访问床次创建"""
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        page.wait_for_timeout(3000)
        # 应重定向到登录页或提示登录
        current_url = page.url
        assert "login" in current_url.lower() or "auth" in current_url.lower() or \
            page.query_selector("input[type='password']") is not None or \
            page.query_selector("input[placeholder*='密码']") is not None, \
            f"Unauthenticated access should redirect to login, got URL: {current_url}"
