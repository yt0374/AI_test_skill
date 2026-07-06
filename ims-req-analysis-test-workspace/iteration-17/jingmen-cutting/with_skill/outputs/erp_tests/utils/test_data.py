"""Static test data constants for Jingmen Cutting 2.0 tests.

These constants are used when CSV data is not required
(e.g., hardcoded expected values, environment config).
"""
from dataclasses import dataclass
from typing import Optional


# ---- Environment ----
JINGMEN_URL = "http://bak.jmym.dtsimple.pro"
JINGMEN_USERNAME = "admin"
JINGMEN_PASSWORD = "ym5579"
PAGE_TITLE = "首页 - 麦塔西智能制造协同平台"

# ---- Module Names (Jingmen uses simple names) ----
MODULE_PRODUCTION = "生产"
MODULE_HANGING = "吊挂"
MODULE_WAREHOUSE = "仓库"

# ---- CPO Test Data ----
CPO_A = {"id": "CPO-A", "delivery_date": "2026-07-01", "quantity": 500}
CPO_B = {"id": "CPO-B", "delivery_date": "2026-07-05", "quantity": 300}
CPO_C = {"id": "CPO-C", "delivery_date": "2026-07-02", "quantity": 200}
CPO_D = {"id": "CPO-D", "delivery_date": "2026-07-10", "quantity": 400}

# ---- Marker (唛架) Test Data ----
MARKER_MK001 = {"id": "MK-001", "total_layers": 100}
MARKER_MK002 = {"id": "MK-002", "total_layers": 80}
MARKER_MK003 = {"id": "MK-003", "total_layers": 50}
MARKER_MK004 = {"id": "MK-004", "total_layers": 30}

# ---- Status Values ----
TASK_STATUS_NOT_STARTED = "未开始"
TASK_STATUS_IN_PROGRESS = "拉布中"
TASK_STATUS_COMPLETED = "已完成"

BED_STATUS_LAYING = "拉布中"
BED_STATUS_COMPLETED = "已拉布"

# ---- Error Messages (expected) ----
MSG_OVER_ALLOCATION = "分配层数超过唛架剩余可用层数"
MSG_ZERO_LAYERS = "计划层数必须大于0"
MSG_INVALID_BARCODE = "未找到该布卷号"
MSG_INVALID_LAYERS = "请输入有效的正整数层数"
MSG_OVER_CUT_WARNING = "剩余层数不足"
MSG_OVER_CUT_BLOCK = "总裁剪层数已超计划，需PC端审核"
MSG_CPO_FULL = "数量已满，请切换其他CPO"
MSG_ACTUAL_OVER_RANGE = "实际层数超出可调整范围"

# ---- Warning Threshold ----
DEFAULT_WARNING_THRESHOLD = 10
