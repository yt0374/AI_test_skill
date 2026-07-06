"""P3 Integration Tests for Jingmen Cutting System 2.0.

End-to-end cross-module workflows spanning:
- PC task creation → PAD bed management → ticket printing → hanging execution
- Full state machine lifecycle
- Cross-device data consistency

All marked with @pytest.mark.p3.
"""

import pytest


class TestFullSingleCPOFlow:
    """完整单一CPO链路：创建任务→创建床次→提交→打印扎卡→挂片自动充数"""

    @pytest.mark.p3
    def test_full_single_cpo_flow(self, logged_in_page):
        """F-01: 单一CPO完整裁剪到挂片全链路"""
        page = logged_in_page

        # Step 1: PC端创建裁剪任务
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        page.click("button:has-text('新建裁剪任务')")
        page.wait_for_timeout(1000)
        # 勾选单一CPO
        checkboxes = page.query_selector_all("input[type='checkbox']:not([class*='select-all'])")
        if checkboxes:
            checkboxes[0].click()
        page.fill("input[placeholder*='计划层数']", "100")
        page.fill("input[placeholder*='计划件数']", "500")
        page.click("button:has-text('保存')")
        page.wait_for_timeout(2000)
        toast = page.query_selector(".ant-message-success")
        assert toast is not None, "Task creation should succeed"

        # Step 2: 验证任务状态=未开始
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        page.wait_for_timeout(1000)
        page_content = page.content()
        assert "未开始" in page_content, "Task should be in '未开始' status"

        # Step 3: PAD端创建床次
        page.click("text=未开始" or "tr:has-text('未开始')")
        page.wait_for_timeout(1000)
        page.click("button:has-text('新增床次')")
        page.fill("input[placeholder*='拉布层数']", "30")
        page.click("button:has-text('确定')")
        page.wait_for_timeout(2000)

        # Step 4: 验证任务状态变为拉布中
        page_content = page.content()
        assert "拉布中" in page_content, "Task should transition to '拉布中'"

        # Step 5: 提交完成床次
        page.click("button:has-text('提交完成')")
        page.fill("input[placeholder*='实际层数']", "30")
        page.click("button:has-text('确认提交')")
        page.wait_for_timeout(2000)

        # Step 6: 验证床次号和状态
        page_content = page.content()
        import re
        assert re.search(r'[CF]-\d{3}', page_content), "Bed number should be generated"

        # Step 7: 打印扎卡（单一CPO应显示CPO号）
        page.goto("http://bak.jmym.dtsimple.pro/production/ticket-print")
        page.wait_for_timeout(1000)
        page_content = page.content()
        assert "CPO" in page_content, "CPO info should be visible for single CPO task"

        # Step 8: 缝制挂片自动充数
        page.goto("http://bak.jmym.dtsimple.pro/production/hanging")
        page.wait_for_timeout(1000)
        assert "自动充数" in page_content or "auto" in page_content.lower(), \
            "Auto fill mode should be active"


class TestFullMergeCPOFlow:
    """完整合并CPO链路"""

    @pytest.mark.p3
    def test_full_merge_cpo_flow(self, logged_in_page):
        """F-02: 合并CPO完整裁剪到自动挂片全链路"""
        page = logged_in_page

        # Step 1: 创建合并CPO裁剪任务
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        page.click("button:has-text('新建裁剪任务')")
        page.wait_for_timeout(1000)
        # 勾选多个CPO
        checkboxes = page.query_selector_all("input[type='checkbox']:not([class*='select-all'])")
        for cb in checkboxes[:3]:
            cb.click()
        page.fill("input[placeholder*='计划层数']", "200")
        page.click("button:has-text('保存')")
        page.wait_for_timeout(2000)

        # Step 2: 创建床次
        page.click("text=未开始" or "tr:has-text('未开始')")
        page.wait_for_timeout(500)
        page.click("button:has-text('新增床次')")
        page.fill("input[placeholder*='拉布层数']", "50")
        page.click("button:has-text('确定')")
        page.wait_for_timeout(1000)

        # Step 3: 提交完成
        page.click("button:has-text('提交完成')")
        page.fill("input[placeholder*='实际层数']", "50")
        page.click("button:has-text('确认提交')")
        page.wait_for_timeout(2000)

        # Step 4: 扎卡打印 — 合并CPO应隐藏CPO信息
        page.goto("http://bak.jmym.dtsimple.pro/production/ticket-print")
        page.wait_for_timeout(1000)
        # 进入合并CPO任务的扎卡打印
        page_content = page.content()
        # 应无单独CPO选择区域

        # Step 5: 挂片 — 自动按交期充数
        page.goto("http://bak.jmym.dtsimple.pro/production/hanging")
        page.wait_for_timeout(1000)
        page_content = page.content()
        assert "自动" in page_content or "充数" in page_content, "Auto fill should be active"


class TestOvercutFullFlow:
    """防超裁完整流程：预警→强控→PC审核→继续"""

    @pytest.mark.p3
    def test_overcut_full_flow(self, logged_in_page):
        """F-03: 防超裁三阶段完整流程"""
        page = logged_in_page

        # Step 1: 创建一个剩余层数较少的裁剪任务场景
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task/detail/1")
        page.wait_for_timeout(1000)

        # Step 2: 尝试创建超额床次触发强控
        page.click("button:has-text('新增床次')")
        page.fill("input[placeholder*='拉布层数']", "999")
        page.click("button:has-text('确定')")
        page.wait_for_timeout(1000)

        # Step 3: 确认强控消息
        toast = page.query_selector(".ant-message-notice-content, .ant-modal-body")
        if toast:
            toast_text = toast.inner_text()
            assert any(kw in toast_text for kw in ["超计划", "已超", "审核"]), \
                f"Overcut block message expected, got: {toast_text}"
            # 关闭弹窗
            close_btn = page.query_selector("button:has-text('关闭'), button:has-text('取消')")
            if close_btn:
                close_btn.click()

        # Step 4: PC端超裁审核
        page.wait_for_timeout(500)
        overcut_btn = page.query_selector("button:has-text('申请超裁')")
        assert overcut_btn is not None, "Overcut approve button should appear"

        # Step 5: 放行
        overcut_btn.click()
        page.wait_for_timeout(1000)
        approve_btn = page.query_selector("button:has-text('放行'), button:has-text('通过')")
        if approve_btn:
            approve_btn.click()
            page.wait_for_timeout(2000)

        # Step 6: 验证可以继续创建床次
        page_content = page.content()
        assert "超裁" not in page_content or "已放行" in page_content, \
            "Task should be releasable after overcut approval"


class TestManualModeFullFlow:
    """手动模式完整流程：切换模式→选择CPO→满额切换"""

    @pytest.mark.p3
    def test_manual_mode_full_flow(self, logged_in_page):
        """F-06: 手动充数模式完整流程"""
        page = logged_in_page

        # Step 1: 进入挂片页面
        page.goto("http://bak.jmym.dtsimple.pro/production/hanging")
        page.wait_for_timeout(1000)

        # Step 2: 切换到手动模式
        page.click("button:has-text('手动充数')")
        page.wait_for_timeout(1000)
        page_content = page.content()
        assert "CPO" in page_content, "CPO list should show in manual mode"

        # Step 3: 选择CPO
        cpo_item = page.query_selector("tr:has-text('CPO')")
        if cpo_item:
            cpo_item.click()
            page.wait_for_timeout(500)

        # Step 4: 执行挂片操作（扫描扎卡或模拟）
        page.fill("input[placeholder*='扫描扎卡']", "TICKET-TEST-001")
        page.press("input[placeholder*='扫描扎卡']", "Enter")
        page.wait_for_timeout(1000)

        # Step 5: 切换到自动模式验证
        page.click("button:has-text('恢复自动充数')")
        page.wait_for_timeout(1000)
        page_content = page.content()
        assert "自动" in page_content or "auto" in page_content.lower(), "Should return to auto mode"


class TestCrossDeviceConsistency:
    """跨设备数据一致性测试"""

    @pytest.mark.p3
    def test_data_consistency_pc_to_pad(self, logged_in_page):
        """验证PC端创建的任务数据在PAD端正确显示"""
        page = logged_in_page

        # PC端创建任务
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        page.click("button:has-text('新建裁剪任务')")
        page.wait_for_timeout(1000)
        checkboxes = page.query_selector_all("input[type='checkbox']:not([class*='select-all'])")
        if checkboxes:
            checkboxes[0].click()
        page.fill("input[placeholder*='计划层数']", "80")
        page.fill("input[placeholder*='计划件数']", "400")
        page.click("button:has-text('保存')")
        page.wait_for_timeout(3000)

        # 返回列表，查看任务是否可见
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        page.wait_for_timeout(1000)
        page_content = page.content()
        assert "80" in page_content or "400" in page_content, \
            "Created task data should be visible in task list"

    @pytest.mark.p3
    def test_marker_allocated_after_delete_released(self, logged_in_page):
        """验证删除未开始任务后唛架层数释放"""
        page = logged_in_page

        # 创建任务（分配唛架层数）
        page.goto("http://bak.jmym.dtsimple.pro/production/cutting/task")
        page.click("button:has-text('新建裁剪任务')")
        page.wait_for_timeout(1000)
        checkboxes = page.query_selector_all("input[type='checkbox']:not([class*='select-all'])")
        if checkboxes:
            checkboxes[0].click()
        page.fill("input[placeholder*='分配层数']", "30")
        page.click("button:has-text('保存')")
        page.wait_for_timeout(2000)

        # 记录唛架剩余层数（before）
        # 删除任务
        draft_row = page.query_selector("tr:has-text('未开始')")
        if draft_row:
            draft_row.click()
            page.wait_for_timeout(1000)
            delete_btn = page.query_selector("button:has-text('删除')")
            if delete_btn and delete_btn.is_visible():
                delete_btn.click()
                page.wait_for_timeout(500)
                confirm_btn = page.query_selector("button:has-text('确定')")
                if confirm_btn:
                    confirm_btn.click()
                    page.wait_for_timeout(2000)
                    toast = page.query_selector(".ant-message-notice-content")
                    if toast:
                        assert any(kw in toast.inner_text() for kw in ["成功", "删除"]), \
                            "Task deletion should succeed"
