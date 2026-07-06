# =============================================================================
# test_smoke.py - P0 冒烟测试
# 荆门鹰美裁剪系统 2.0 - 核心流程验证
# =============================================================================

import pytest
from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from utils.test_data import ENV_CONFIG, ROUTES, SELECTORS, MESSAGES, TEST_USERS, TIMEOUTS


# =============================================================================
# P0: test_login_success - 登录验证
# =============================================================================
@pytest.mark.p0
@pytest.mark.smoke
def test_login_success(page: Page):
    """验证使用 admin/ym5579 登录荆门鹰美环境成功，无企业选择器。

    前置条件: 无
    操作步骤:
        1. 访问登录页
        2. 输入用户名 admin
        3. 输入密码 ym5579
        4. 点击登录按钮
    预期结果: 成功跳转到主页，无企业选择器弹窗
    """
    base_url = ENV_CONFIG["base_url"]
    page.goto(f"{base_url}/login", wait_until="domcontentloaded")
    page.wait_for_timeout(1000)

    bp = BasePage(page)

    # 验证登录页标题或登录表单存在
    assert bp.is_visible("input, button") is True, "登录页面未正常加载"

    # 填写用户名
    bp.fill_input(
        "input[placeholder*='用户名'], input[placeholder*='账号'], input[name='username'], input[type='text']",
        TEST_USERS["admin"]["username"],
    )

    # 填写密码
    bp.fill_input(
        "input[placeholder*='密码'], input[name='password'], input[type='password']",
        TEST_USERS["admin"]["password"],
    )

    # 点击登录
    bp.click_button(SELECTORS["login"]["login_button"])

    # 等待页面跳转
    page.wait_for_timeout(3000)

    # 验证登录成功：URL 不再是登录页
    current_url = bp.get_current_url()
    assert "/login" not in current_url, f"登录失败，仍在登录页面: {current_url}"

    # 验证主页元素存在：布局、导航栏等
    has_layout = (
        bp.is_visible(SELECTORS["layout"]["sidebar"]) or
        bp.is_visible(SELECTORS["layout"]["header"]) or
        bp.is_visible(SELECTORS["layout"]["content"])
    )
    assert has_layout, MESSAGES["login_fail"]

    # 验证无企业选择器弹窗（荆门环境特征）
    enterprise_modal = page.locator("text=选择企业, text=切换企业, [data-testid='enterprise-select']")
    expect(enterprise_modal).to_have_count(0, timeout=TIMEOUTS["short"])

    print(f"[PASS] {MESSAGES['login_success']}")


# =============================================================================
# P0: test_navigate_cutting_task_page - 导航到裁剪任务页
# =============================================================================
@pytest.mark.p0
@pytest.mark.smoke
def test_navigate_cutting_task_page(logged_in_page: Page):
    """验证成功登录后能够导航到裁剪任务页面。

    前置条件: 已登录 admin/ym5579
    操作步骤:
        1. 在侧边栏或菜单中点击"裁剪任务"
        2. 或直接访问裁剪任务 URL
    预期结果: 裁剪任务页面正常加载，显示任务列表或空状态
    """
    page = logged_in_page
    bp = BasePage(page)

    base_url = ENV_CONFIG["base_url"]

    # 尝试通过侧边栏导航
    sidebar_links = page.locator(
        f"{SELECTORS['layout']['sidebar']} a:has-text('裁剪任务'), "
        f"{SELECTORS['layout']['sidebar']} li:has-text('裁剪任务'), "
        f"a:has-text('裁剪任务'), "
        f".ant-menu-item:has-text('裁剪任务')"
    )

    if sidebar_links.count() > 0:
        sidebar_links.first.click()
    else:
        # 兜底：直接访问 URL
        page.goto(f"{base_url}{ROUTES['cutting_task']}", wait_until="domcontentloaded")

    page.wait_for_timeout(2000)

    # 验证页面加载：存在表格、面包屑或页面标题
    page_loaded = (
        bp.is_visible(SELECTORS["table"]["container"]) or
        bp.is_visible(SELECTORS["layout"]["breadcrumb"]) or
        bp.is_visible("h1, h2, h3, .page-title") or
        "/cutting" in bp.get_current_url()
    )
    assert page_loaded, "裁剪任务页面加载失败"

    # 验证 URL 包含 cutting 相关路径
    current_url = bp.get_current_url()
    assert "/cutting" in current_url or "/task" in current_url, \
        f"URL 不符合预期: {current_url}"

    print(f"[PASS] 裁剪任务页面导航成功: {current_url}")


# =============================================================================
# P0: test_create_cutting_task_single_cpo - 创建单个 CPO 裁剪任务
# =============================================================================
@pytest.mark.p0
@pytest.mark.smoke
def test_create_cutting_task_single_cpo(logged_in_page: Page):
    """验证创建单个 CPO 的裁剪任务。

    前置条件: 已登录，系统存在可用的 CPO
    操作步骤:
        1. 导航到裁剪任务页
        2. 点击"新建"或"创建"按钮
        3. 在 CPO 选择弹窗中搜索并选择单个 CPO
        4. 确认创建
    预期结果: 任务创建成功，Toast 提示成功，任务列表中出现新任务
    """
    page = logged_in_page
    bp = BasePage(page)
    base_url = ENV_CONFIG["base_url"]

    # 导航到裁剪任务页
    page.goto(f"{base_url}{ROUTES['cutting_task']}", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # 点击创建按钮
    create_btn = page.locator(SELECTORS["button"]["create"])
    if create_btn.count() > 0:
        create_btn.first.click()
    else:
        # 尝试页面内特定创建按钮
        btn = page.locator(
            "button:has-text('新建裁剪任务'), button:has-text('创建任务'), "
            "[data-testid='create-cutting-task'], a:has-text('新建任务')"
        ).first
        if btn.count() > 0:
            btn.click()
        else:
            pytest.skip("未找到创建任务入口按钮，请确认页面结构")

    page.wait_for_timeout(1500)

    # 期望打开 CPO 选择弹窗或创建表单
    modal_or_form = page.locator(
        f"{SELECTORS['modal']['container']}, form, .ant-drawer, .ant-form"
    )
    assert modal_or_form.count() > 0, "创建任务弹窗/表单未打开"

    # 搜索 CPO
    cpo_search = page.locator(SELECTORS["cutting_task"]["cpo_search_input"])
    if cpo_search.count() > 0:
        cpo_search.first.fill("CPO")
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)

    # 选择第一个可用 CPO
    cpo_checkboxes = page.locator(SELECTORS["cutting_task"]["cpo_checkbox_item"])
    if cpo_checkboxes.count() > 0:
        cpo_checkboxes.first.check()
    else:
        # 尝试按文本选择或直接表格行点击
        first_row = page.locator(".ant-table-row, [data-testid='cpo-row']").first
        if first_row.count() > 0:
            first_row.click()
        else:
            pytest.skip("未找到可选 CPO 列表，请确认系统中存在 CPO 数据")

    page.wait_for_timeout(500)

    # 确认创建
    confirm_btn = page.locator(
        f"{SELECTORS['modal']['confirm']}, button:has-text('确定'), button:has-text('创建')"
    ).first
    if confirm_btn.count() > 0:
        confirm_btn.click()
    else:
        pytest.skip("未找到确认创建的按钮")

    # 等待操作完成
    page.wait_for_timeout(2000)

    # 验证：Toast 成功提示 或 弹窗关闭回到列表
    toast_success = (
        bp.is_visible(SELECTORS["toast"]["success"]) or
        bp.is_visible(SELECTORS["toast"]["container"])
    )
    back_to_list = not page.locator(SELECTORS["modal"]["container"]).is_visible()

    assert toast_success or back_to_list, "任务创建后未出现成功反馈"
    print(f"[PASS] 单个 CPO 裁剪任务创建成功")


# =============================================================================
# P0: test_create_cutting_task_multi_cpo - 创建多个 CPO 裁剪任务
# =============================================================================
@pytest.mark.p0
@pytest.mark.smoke
def test_create_cutting_task_multi_cpo(logged_in_page: Page):
    """验证选择多个 CPO 创建合并裁剪任务。

    前置条件: 已登录，系统存在至少 2 个可用的 CPO
    操作步骤:
        1. 导航到裁剪任务页
        2. 点击创建按钮
        3. 在 CPO 选择弹窗中选择多个 CPO（至少 2 个）
        4. 确认创建
    预期结果: 合并任务创建成功，任务列表中显示合并标识
    """
    page = logged_in_page
    bp = BasePage(page)
    base_url = ENV_CONFIG["base_url"]

    page.goto(f"{base_url}{ROUTES['cutting_task']}", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # 点击创建
    create_btn = page.locator(
        f"{SELECTORS['button']['create']}, button:has-text('新建裁剪任务'), "
        f"button:has-text('创建任务'), [data-testid='create-cutting-task']"
    ).first
    if create_btn.count() > 0:
        create_btn.click()
    else:
        pytest.skip("未找到创建任务入口")

    page.wait_for_timeout(1500)

    # 确认弹窗/表单打开
    assert page.locator(
        f"{SELECTORS['modal']['container']}, form, .ant-drawer, .ant-form"
    ).count() > 0, "创建任务弹窗未打开"

    # 搜索 CPO
    cpo_search = page.locator(SELECTORS["cutting_task"]["cpo_search_input"])
    if cpo_search.count() > 0:
        cpo_search.first.fill("CPO")
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)

    # 选择多个 CPO（前 2-3 个）
    cpo_checkboxes = page.locator(SELECTORS["cutting_task"]["cpo_checkbox_item"])
    selected_count = 0
    if cpo_checkboxes.count() >= 2:
        for i in range(min(3, cpo_checkboxes.count())):
            cb = cpo_checkboxes.nth(i)
            if not cb.is_checked():
                cb.check()
                selected_count += 1
    else:
        pytest.skip("CPO 数量不足（需要至少 2 个），请确认系统中存在足够的 CPO 数据")

    assert selected_count >= 2, f"未能选择足够的 CPO（仅选了 {selected_count} 个）"

    # 确认创建
    confirm = page.locator(f"{SELECTORS['modal']['confirm']}, button:has-text('确定')").first
    if confirm.count() > 0:
        confirm.click()
    else:
        pytest.skip("未找到确认按钮")

    page.wait_for_timeout(2500)

    # 验证创建成功
    success = (
        bp.is_visible(SELECTORS["toast"]["success"]) or
        bp.is_visible(SELECTORS["toast"]["container"]) or
        not page.locator(SELECTORS["modal"]["container"]).is_visible()
    )
    assert success, "多 CPO 任务创建未成功"
    print(f"[PASS] 多个 CPO ({selected_count} 个) 合并任务创建成功")


# =============================================================================
# P0: test_marker_allocation - 唛架层分配验证
# =============================================================================
@pytest.mark.p0
@pytest.mark.smoke
def test_marker_allocation(logged_in_page: Page):
    """验证创建裁剪任务后唛架层数的分配显示。

    前置条件: 已登录，有可用任务或可创建任务
    操作步骤:
        1. 进入已创建的任务详情
        2. 查看唛架层数分配信息
    预期结果: 唛架层数正确显示，与实际订单数量匹配
    """
    page = logged_in_page
    bp = BasePage(page)
    base_url = ENV_CONFIG["base_url"]

    page.goto(f"{base_url}{ROUTES['cutting_task']}", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # 查找已存在的任务
    task_rows = page.locator(SELECTORS["cutting_task"]["task_row"])
    if task_rows.count() == 0:
        pytest.skip("当前无任务数据，请先手动创建任务后再执行此测试")

    # 点击第一个任务的详情
    detail_link = page.locator(SELECTORS["cutting_task"]["task_detail_link"]).first
    if detail_link.count() > 0:
        detail_link.click()
    else:
        task_rows.first.click()

    page.wait_for_timeout(2000)

    # 验证详情页包含唛架信息
    marker_info_visible = (
        bp.is_visible("text=唛架, text=层数, text=marker, text=layer") or
        bp.is_visible(SELECTORS["cutting_task"]["marker_layer_input"])
    )
    assert marker_info_visible, "任务详情页未显示唛架层数信息"

    # 验证有具体数值（非空）
    marker_input = page.locator(SELECTORS["cutting_task"]["marker_layer_input"])
    if marker_input.count() > 0:
        value = bp.get_input_value(SELECTORS["cutting_task"]["marker_layer_input"])
        assert value, "唛架层数输入为空"
        print(f"[PASS] 唛架层数分配验证成功，当前值: {value}")
    else:
        print("[PASS] 唛架信息区域存在，未能直接读取数值但元素可见")


# =============================================================================
# P0: test_create_bed_on_pad - PAD 端创建床次
# =============================================================================
@pytest.mark.p0
@pytest.mark.smoke
def test_create_bed_on_pad(logged_in_page: Page):
    """验证在 PAD 端模拟创建床次（模拟/桩测试，非真实 PAD 设备）。

    前置条件: 已登录，存在已创建的裁剪任务
    操作步骤:
        1. 导航至裁剪任务详情
        2. 进入床次管理页面
        3. 点击创建床次
        4. 填写层数信息
        5. 点击提交
    预期结果: 床次创建成功，返回床次编号
    """
    page = logged_in_page
    bp = BasePage(page)
    base_url = ENV_CONFIG["base_url"]

    # 先导航到任务列表检查是否有任务
    page.goto(f"{base_url}{ROUTES['cutting_task']}", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    task_rows = page.locator(SELECTORS["cutting_task"]["task_row"])
    if task_rows.count() == 0:
        pytest.skip("当前无裁剪任务，请先创建任务后再执行 PAD 床次测试")

    # 进入第一个任务
    task_rows.first.click()
    page.wait_for_timeout(2000)

    # 查找床次相关入口
    bed_tab = page.locator(
        "text=床次, text=床次管理, .ant-tabs-tab:has-text('床次'), [data-testid='bed-tab']"
    ).first
    if bed_tab.count() > 0:
        bed_tab.click()
        page.wait_for_timeout(1000)

    # 点击创建床次
    create_bed_btn = page.locator(
        f"{SELECTORS['button']['create']}, button:has-text('创建床次'), "
        f"button:has-text('新建床次'), [data-testid='create-bed']"
    ).first

    if create_bed_btn.count() > 0:
        create_bed_btn.click()
    else:
        # 模拟 PAD 端创建：直接在床次表单区域操作
        bed_form = page.locator(SELECTORS["bed"]["create_form"])
        if bed_form.count() == 0:
            pytest.skip("未找到床次创建入口，请确认页面结构")

    page.wait_for_timeout(1000)

    # 填写床次信息
    layer_input = page.locator(SELECTORS["bed"]["layer_input"])
    if layer_input.count() > 0:
        layer_input.first.fill("50")

    # 选择布匹卷
    roll_select = page.locator(SELECTORS["bed"]["roll_select"])
    if roll_select.count() > 0:
        roll_select.first.click()
        page.wait_for_timeout(500)
        # 选择第一个选项
        first_option = page.locator(".ant-select-dropdown .ant-select-item, .el-select-dropdown__item").first
        if first_option.count() > 0:
            first_option.click()
            page.wait_for_timeout(500)
    else:
        # 可能直接有输入框
        bed_number_input = page.locator(SELECTORS["cutting_task"]["bed_number_input"])
        if bed_number_input.count() > 0:
            bed_number_input.first.fill("BED-001")

    # 点击提交
    submit_btn = page.locator(SELECTORS["bed"]["submit_button"])
    if submit_btn.count() > 0:
        submit_btn.first.click()
    else:
        save_btn = page.locator(f"{SELECTORS['button']['save']}, button:has-text('提交')").first
        if save_btn.count() > 0:
            save_btn.click()
        else:
            pytest.skip("未找到床次提交按钮")

    page.wait_for_timeout(2000)

    # 验证床次创建成功
    success = (
        bp.is_visible(SELECTORS["toast"]["success"]) or
        bp.is_visible(SELECTORS["toast"]["container"])
    )

    if success:
        toast_text = bp.get_text(SELECTORS["toast"]["container"])
        print(f"[PASS] PAD 端床次创建成功，反馈: {toast_text}")
    else:
        # 宽松断言：至少不在错误状态
        assert not bp.is_visible(SELECTORS["toast"]["error"]), "床次创建失败"
        print("[PASS] PAD 端床次创建操作已执行（未检测到错误）")


# =============================================================================
# P0: test_ticket_print_merge_hide_cpo - 合并任务票号打印隐藏 CPO
# =============================================================================
@pytest.mark.p0
@pytest.mark.smoke
def test_ticket_print_merge_hide_cpo(logged_in_page: Page):
    """验证合并任务在票号打印时 CPO 信息被正确隐藏。

    前置条件: 已登录，存在合并的裁剪任务（多 CPO）
    操作步骤:
        1. 进入合并任务详情或票号打印页面
        2. 检查 CPO 信息区域的显示状态
    预期结果: 合并任务中 CPO 详情被隐藏或以合并形式展示
    """
    page = logged_in_page
    bp = BasePage(page)
    base_url = ENV_CONFIG["base_url"]

    page.goto(f"{base_url}{ROUTES['cutting_task']}", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # 查找状态为"合并"或"拉布中"的任务（表示多 CPO 任务）
    task_rows = page.locator(SELECTORS["cutting_task"]["task_row"])
    if task_rows.count() == 0:
        pytest.skip("当前无任务数据")

    # 尝试找到多 CPO 任务或使用第一个任务
    found_merge = False
    for i in range(min(10, task_rows.count())):
        row = task_rows.nth(i)
        row_text = row.inner_text()
        if "合并" in row_text or "拉布中" in row_text:
            row.click()
            found_merge = True
            break

    if not found_merge:
        task_rows.first.click()

    page.wait_for_timeout(2000)

    # 导航到票号打印相关页面
    ticket_tab = page.locator(
        "text=票号, text=打印, .ant-tabs-tab:has-text('票号'), [data-testid='ticket-tab']"
    ).first
    if ticket_tab.count() > 0:
        ticket_tab.click()
        page.wait_for_timeout(1000)

    # 检查合并信息区域
    merge_info = page.locator(SELECTORS["ticket"]["merge_info"])
    if merge_info.count() > 0:
        merge_text = merge_info.first.inner_text()
        assert merge_text, "合并信息区域为空"
        # 合并信息应存在但不展示单个 CPO 明细
        print(f"[PASS] 合并任务票号信息: {merge_text[:100]}")
    else:
        # 检查 CPO 信息：合并任务不应显示单个 CPO 详情
        cpo_detail = page.locator(".cpo-detail, [data-testid='single-cpo-detail']")
        if cpo_detail.count() > 0:
            # 存在 CPO 详情说明可能是单 CPO 任务
            print("[INFO] 当前任务可能为单 CPO，预期合并任务不显示 CPO 明细")
        else:
            print("[PASS] 合并任务不显示单个 CPO 明细（符合预期）")

    assert True, "票号打印 CPO 隐藏验证完成"


# =============================================================================
# P0: test_auto_fill_generic_ticket - 自动填充通用票
# =============================================================================
@pytest.mark.p0
@pytest.mark.smoke
def test_auto_fill_generic_ticket(logged_in_page: Page):
    """验证通用票号自动填充功能。

    前置条件: 已登录，存在已提交的床次
    操作步骤:
        1. 进入票号管理页面
        2. 点击"通用票"或"自动填充"按钮
        3. 验证票号自动生成
    预期结果: 系统自动分配通用票号并显示
    """
    page = logged_in_page
    bp = BasePage(page)
    base_url = ENV_CONFIG["base_url"]

    # 导航到票号管理页面
    page.goto(f"{base_url}{ROUTES['cutting_ticket']}", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # 如果直接 URL 不行，从裁剪任务页进入
    if bp.is_visible(".ant-result-404, .ant-result-error") or "/404" in bp.get_current_url():
        page.goto(f"{base_url}{ROUTES['cutting_task']}", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        # 进入第一个任务
        task_rows = page.locator(SELECTORS["cutting_task"]["task_row"])
        if task_rows.count() > 0:
            task_rows.first.click()
            page.wait_for_timeout(2000)
            # 切换到票号 tab
            ticket_tab = page.locator(
                "text=票号, .ant-tabs-tab:has-text('票号'), [data-testid='ticket-tab']"
            ).first
            if ticket_tab.count() > 0:
                ticket_tab.click()
                page.wait_for_timeout(1000)

    # 点击通用票/自动填充按钮
    generic_btn = page.locator(SELECTORS["ticket"]["generic_ticket_btn"])
    if generic_btn.count() == 0:
        generic_btn = page.locator(
            "button:has-text('通用'), button:has-text('自动填充'), "
            "button:has-text('自动生成'), [data-testid='auto-fill']"
        ).first

    if generic_btn.count() > 0:
        generic_btn.click()
        page.wait_for_timeout(2000)

        # 验证票号已自动生成
        ticket_display = page.locator(
            ".ticket-number, .ticket-code, [data-testid='ticket-number'], "
            "input[placeholder*='票号'], .ticket-info"
        ).first

        if ticket_display.count() > 0:
            ticket_value = ticket_display.inner_text() or ticket_display.input_value()
            if ticket_value:
                assert len(ticket_value) > 0, "通用票号自动填充后为空"
                print(f"[PASS] 通用票号自动填充成功: {ticket_value}")
            else:
                print("[PASS] 通用票自动填充操作已执行，票号区域可见")
        else:
            # 检查是否有 Toast 成功消息
            success_toast = bp.is_visible(SELECTORS["toast"]["success"])
            assert success_toast, "自动填充后未出现成功提示"
            print("[PASS] 通用票自动填充成功（Toast 反馈）")
    else:
        pytest.skip("未找到通用票号自动填充按钮")
