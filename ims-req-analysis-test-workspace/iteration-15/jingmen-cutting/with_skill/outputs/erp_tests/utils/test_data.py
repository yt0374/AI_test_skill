"""
Static test data constants for 荆门新裁剪需求2.0 tests.

Derived from test_data_inventory.md and consolidated_domain_knowledge.md.
Environment: jingmen (bak.jmym.dtsimple.pro)
"""

# =============================================================
# Environment Configuration
# =============================================================

JINGMEN_URL = "http://bak.jmym.dtsimple.pro"
JINGMEN_CREDENTIALS = {"username": "admin", "password": "ym5579"}
JINGMEN_PAGE_TITLE = "首页 - 麦塔西智能制造协同平台"

# =============================================================
# Test CPO Data
# =============================================================

CPO_DATA = [
    {"code": "CPO-A", "qty": 500, "date": "2026-07-01", "priority": "紧急"},
    {"code": "CPO-B", "qty": 300, "date": "2026-07-05", "priority": "正常"},
    {"code": "CPO-C", "qty": 200, "date": "2026-07-02", "priority": "正常"},
    {"code": "CPO-D", "qty": 100, "date": "2026-07-01", "priority": "紧急"},
    {"code": "CPO-E", "qty": 50,  "date": "2026-07-10", "priority": "低"},
]

# =============================================================
# Test Marker Data
# =============================================================

MARKER_DATA = [
    {"id": "M-001", "total_layers": 100, "style": "款号A"},
    {"id": "M-002", "total_layers": 50,  "style": "款号B"},
    {"id": "M-003", "total_layers": 200, "style": "款号C"},
]

# =============================================================
# Test Bed Data
# =============================================================

BED_DATA = [
    {"roll_no": "FAB-001", "input_layers": 20, "actual_layers": 20, "group": "组A"},
    {"roll_no": "FAB-002", "input_layers": 15, "actual_layers": 14, "group": "组A"},
    {"roll_no": "FAB-003", "input_layers": 10, "actual_layers": 10, "group": "组B"},
    {"roll_no": "FAB-004", "input_layers": 5,  "actual_layers": 5,  "group": "组B"},
    {"roll_no": "FAB-005", "input_layers": 50, "actual_layers": 50, "group": "组A"},
]

# =============================================================
# Anti-Overcut Thresholds
# =============================================================

WARNING_THRESHOLD = 10    # Soft warning threshold (default)
FORCE_CONTROL_LIMIT = 0   # Force control when remaining < 0

# =============================================================
# Task Status Values
# =============================================================

TASK_STATUS = {
    "NOT_STARTED": "未开始",
    "IN_PROGRESS": "拉布中",
    "COMPLETED": "已完成",
}

BED_STATUS = {
    "IN_PROGRESS": "拉布中",
    "COMPLETED": "已拉布",
}

# =============================================================
# Bed Number Prefixes
# =============================================================

BED_PREFIX_MAIN = "C"    # 主布床次
BED_PREFIX_AUX = "F"     # 辅布床次

# =============================================================
# Expected Messages
# =============================================================

MESSAGES = {
    "SELECT_CPO_REQUIRED": "请至少选择一个CPO",
    "MARKER_FULL": "唛架剩余层数不足，可用层数为0",
    "MARKER_OVER_ALLOCATED": "分配层数超出唛架剩余可用层数",
    "LAYERS_INSUFFICIENT": "剩余层数不足",
    "WARNING_THRESHOLD": "剩余层数不足10层，请注意控制",
    "FORCE_CONTROL": "总裁剪层数已超计划，需PC端审核",
    "ACTUAL_EXCEEDS_RANGE": "实际层数超出可调整范围",
    "CPO_FULL": "数量已满，请切换其他 CPO",
    "CREATE_SUCCESS": "创建成功",
    "SUBMIT_SUCCESS": "提交成功",
    "OVERCUT_APPROVED": "放行",
    "OVERCUT_REJECTED": "驳回",
}

# =============================================================
# Page URLs (jingmen environment)
# =============================================================

PAGE_URLS = {
    "login": "/login",
    "production_cutting_task": "/production/cutting-task",
    "production_tag_print": "/production/tag-print",
    "production_hanging_station": "/production/hanging-station",
    "production_bed_task": "/production/bed-task",
}
