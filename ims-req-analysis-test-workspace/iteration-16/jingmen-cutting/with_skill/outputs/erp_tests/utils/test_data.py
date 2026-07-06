# =============================================================================
# test_data.py - 荆门鹰美环境测试数据常量
# 裁剪系统 2.0 Playwright 测试项目
# =============================================================================

# =============================================================================
# 环境配置
# =============================================================================
ENV_CONFIG = {
    "name": "荆门鹰美",
    "base_url": "http://bak.jmym.dtsimple.pro",
    "env_code": "jingmen",
}

# =============================================================================
# 测试用户
# =============================================================================
TEST_USERS = {
    "admin": {
        "username": "admin",
        "password": "ym5579",
        "role": "超级管理员",
        "description": "荆门鹰美管理员账号，无企业选择器",
    },
}

# =============================================================================
# 超时配置（毫秒）
# =============================================================================
TIMEOUTS = {
    "short": 3000,       # 快速等待（Toast 消失、动画）
    "medium": 10000,     # 中等等待（元素加载、表单提交反馈）
    "long": 30000,       # 长等待（大量数据加载、复杂操作）
    "page_load": 60000,  # 页面完整加载
}

# =============================================================================
# 页面路由
# =============================================================================
ROUTES = {
    "login": "/login",
    "dashboard": "/dashboard",
    "cutting_task": "/cutting/task",           # 裁剪任务列表
    "cutting_task_create": "/cutting/task/create",  # 创建裁剪任务
    "cutting_task_detail": "/cutting/task/detail",  # 裁剪任务详情
    "cutting_bed": "/cutting/bed",              # 床次管理
    "cutting_marker": "/cutting/marker",         # 唛架管理
    "cutting_ticket": "/cutting/ticket",         # 票号管理
    "pad_bed": "/pad/bed",                      # PAD端 床次创建
}

# =============================================================================
# 通用选择器
# =============================================================================
SELECTORS = {
    # ---- 登录页 ----
    "login": {
        "username_input": "input[placeholder*='用户名'], input[placeholder*='账号'], input[name='username']",
        "password_input": "input[placeholder*='密码'], input[name='password'], input[type='password']",
        "login_button": "button:has-text('登录'), button:has-text('登 录'), .ant-btn-primary",
    },

    # ---- 通用布局 ----
    "layout": {
        "sidebar": ".ant-layout-sider, .sidebar, nav",
        "header": ".ant-layout-header, header, .header",
        "breadcrumb": ".ant-breadcrumb, .breadcrumb",
        "content": ".ant-layout-content, .main-content, .content",
    },

    # ---- 通用按钮 ----
    "button": {
        "create": "button:has-text('新建'), button:has-text('创建'), button:has-text('新增'), [data-testid='btn-create']",
        "edit": "button:has-text('编辑'), button:has-text('修改'), [data-testid='btn-edit']",
        "delete": "button:has-text('删除'), [data-testid='btn-delete']",
        "save": "button:has-text('保存'), button:has-text('提交'), [data-testid='btn-save']",
        "cancel": "button:has-text('取消'), [data-testid='btn-cancel']",
        "confirm": "button:has-text('确定'), button:has-text('确认'), .ant-modal button.ant-btn-primary",
        "search": "button:has-text('查询'), button:has-text('搜索'), [data-testid='btn-search']",
        "reset": "button:has-text('重置'), [data-testid='btn-reset']",
        "export": "button:has-text('导出'), [data-testid='btn-export']",
        "print": "button:has-text('打印'), [data-testid='btn-print']",
    },

    # ---- 模态框 ----
    "modal": {
        "container": ".ant-modal, .el-dialog, [role='dialog']",
        "title": ".ant-modal-title, .el-dialog__title, [role='dialog'] h2",
        "confirm": ".ant-modal button.ant-btn-primary, .el-dialog button.el-button--primary",
        "cancel": ".ant-modal button:not(.ant-btn-primary), .el-dialog button:not(.el-button--primary)",
        "close": ".ant-modal-close, .el-dialog__close, [aria-label='Close']",
    },

    # ---- 表格 ----
    "table": {
        "container": ".ant-table, .el-table, table",
        "row": ".ant-table-row, .el-table__row",
        "header": ".ant-table-thead th, .el-table__header th",
        "cell": "td",
        "checkbox": "input[type='checkbox']",
        "pagination": ".ant-pagination, .el-pagination",
        "empty": ".ant-empty, .el-table__empty-text",
        "loading": ".ant-spin-spinning, .el-loading-mask",
    },

    # ---- 表单 ----
    "form": {
        "container": ".ant-form, form",
        "item": ".ant-form-item, .form-item",
        "label": ".ant-form-item-label label",
        "input": "input:not([type='checkbox']):not([type='radio'])",
        "select": ".ant-select, select",
        "date_picker": ".ant-picker, .ant-date-picker, input[placeholder*='日期']",
        "textarea": "textarea",
        "required_mark": ".ant-form-item-required, .required, [aria-required='true']",
    },

    # ---- Toast / 消息 ----
    "toast": {
        "success": ".ant-message-success, .ant-message .anticon-check-circle, .el-message--success",
        "error": ".ant-message-error, .ant-message .anticon-close-circle, .el-message--error",
        "warning": ".ant-message-warning, .ant-message .anticon-exclamation-circle, .el-message--warning",
        "info": ".ant-message-info, .ant-message .anticon-info-circle, .el-message--info",
        "container": ".ant-message, .ant-notification, .el-message, .el-notification",
    },

    # ---- 裁剪任务页专用 ----
    "cutting_task": {
        "task_table": ".ant-table-tbody",
        "task_row": ".ant-table-tbody tr.ant-table-row",
        "cpo_select_btn": "button:has-text('按CPO选择'), button:has-text('选择CPO'), [data-testid='cpo-select']",
        "cpo_search_input": "input[placeholder*='CPO'], input[placeholder*='订单号'], [data-testid='cpo-search']",
        "cpo_table": ".cpo-table .ant-table, [data-testid='cpo-table']",
        "cpo_checkbox_all": "thead input[type='checkbox'], [data-testid='cpo-select-all']",
        "cpo_checkbox_item": "tbody input[type='checkbox']",
        "merge_mode_toggle": "button:has-text('自动'), button:has-text('手动'), [data-testid='mode-toggle']",
        "marker_layer_input": "input[placeholder*='唛架层'], input[placeholder*='层数'], [data-testid='marker-layer']",
        "bed_number_input": "input[placeholder*='床次号'], input[placeholder*='床号'], [data-testid='bed-number']",
        "task_status": ".ant-tag, [data-testid='task-status']",
        "draft_status": ".ant-tag:has-text('草稿'), [data-testid='status-draft']",
        "pulling_status": ".ant-tag:has-text('拉布中'), [data-testid='status-pulling']",
        "completed_status": ".ant-tag:has-text('已完成'), [data-testid='status-completed']",
        "task_detail_link": "a:has-text('详情'), [data-testid='task-detail']",
    },

    # ---- 床次创建 (PAD端) 专用 ----
    "bed": {
        "create_form": ".bed-form, [data-testid='bed-form']",
        "roll_select": ".ant-select, [data-testid='roll-select']",
        "layer_input": "input[placeholder*='层'], input[placeholder*='层数'], [data-testid='layer-input']",
        "submit_button": "button:has-text('提交'), button:has-text('创建床次'), [data-testid='bed-submit']",
        "bed_list": ".bed-list, [data-testid='bed-list']",
        "bed_number_display": ".bed-number, [data-testid='bed-number']",
    },

    # ---- 超量裁剪专用 ----
    "overcut": {
        "warning_alert": ".ant-alert-warning, [data-testid='overcut-warning']",
        "block_alert": ".ant-alert-error, [data-testid='overcut-block']",
        "approve_button": "button:has-text('审批'), button:has-text('超裁审批'), [data-testid='overcut-approve']",
        "reason_input": "textarea[placeholder*='原因'], [data-testid='overcut-reason']",
    },

    # ---- 票号打印专用 ----
    "ticket": {
        "print_button": "button:has-text('打印票号'), button:has-text('打印'), [data-testid='ticket-print']",
        "merge_info": ".merge-info, [data-testid='merge-info']",
        "cpo_info": ".cpo-info, [data-testid='cpo-info']",
        "generic_ticket_btn": "button:has-text('通用票'), button:has-text('自动填充'), [data-testid='generic-ticket']",
        "specific_ticket_btn": "button:has-text('专用票'), button:has-text('指定票'), [data-testid='specific-ticket']",
    },

    # ---- 手动模式专用 ----
    "manual_mode": {
        "cpo_list": ".manual-cpo-list, [data-testid='manual-cpo-list']",
        "cpo_item": ".manual-cpo-item, [data-testid='manual-cpo-item']",
        "mode_switch_warning": ".ant-modal-confirm, [data-testid='mode-switch-warning']",
        "full_alert": ".ant-alert-warning:has-text('已满'), [data-testid='full-alert']",
    },
}

# =============================================================================
# 测试场景数据模板
# =============================================================================
TEST_SCENARIOS = {
    "single_cpo": {
        "cpo_code": "CPO-2026-0001",
        "order_qty": 500,
        "fabric_code": "FB-001",
        "color": "白色",
        "size_distribution": {"S": 100, "M": 150, "L": 150, "XL": 100},
    },
    "multi_cpo": {
        "cpo_codes": ["CPO-2026-0001", "CPO-2026-0002", "CPO-2026-0003"],
        "merge_mode": "auto",
        "merge_key": "same_date",  # 同日期合并
    },
    "overcut": {
        "threshold_warning_pct": 5,     # 超过预留 5% 警告
        "threshold_block_pct": 10,      # 超过预留 10% 阻止
        "approval_required": True,
    },
    "bed": {
        "default_layers_per_bed": 50,
        "max_beds_per_task": 999,
        "min_remaining_for_warning": 10,
    },
}

# =============================================================================
# 断言消息（中文）
# =============================================================================
MESSAGES = {
    "login_success": "登录成功，已进入系统主页",
    "login_fail": "登录失败：用户名或密码错误",
    "create_success": "裁剪任务创建成功",
    "create_fail": "裁剪任务创建失败",
    "delete_success": "删除成功",
    "save_success": "保存成功",
    "submit_success": "提交成功",
    "overcut_warning": "当前裁剪数量超过预留比例，请确认",
    "overcut_block": "裁剪数量超过允许上限，无法继续",
    "overcut_approve": "超裁审批已通过",
    "marker_insufficient": "唛架层数不足",
    "bed_created": "床次创建成功",
    "ticket_printed": "票号打印成功",
    "mode_switch_warning": "切换模式将清空当前选择，是否继续？",
    "full_alert": "所有CPO已分配完毕",
    "no_data": "暂无数据",
}
