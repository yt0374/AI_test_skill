"""Static test data constants for IMS Attendance (考勤) tests.

These constants are used when CSV data is not required
(e.g., hardcoded expected values, environment config, module names).
"""
from dataclasses import dataclass
from typing import Optional


# ---- Environment ----
SIT_URL = "http://test.fj.dtsimple.pro"
SIT_USERNAME = "admin"
SIT_PASSWORD = "admin123"
ENTERPRISE_NAME = "最佳智造"
PAGE_TITLE = "首页 - 麦塔西智能制造协同平台"

# ---- Module Names ----
MODULE_HR = "人事"
MODULE_ATTENDANCE = "考勤"

# ---- 7 Attendance Sub-Pages ----
SUBPAGE_ATTENDANCE_REGISTER = "考勤登记"      # Attendance registration
SUBPAGE_RETURN_WORK = "回工登记"               # Return-to-work registration
SUBPAGE_LEAVE_REGISTER = "请假登记"            # Leave registration
SUBPAGE_DAILY_STATS = "日考勤统计"             # Daily attendance statistics
SUBPAGE_MONTHLY_STATS = "月考勤统计"           # Monthly attendance statistics
SUBPAGE_GROUP_ATTENDANCE = "小组出勤表"        # Group attendance report
SUBPAGE_EMPLOYEE_ABSENCE = "员工缺勤表"        # Employee absence report

ALL_ATTENDANCE_SUBPAGES = [
    SUBPAGE_ATTENDANCE_REGISTER,
    SUBPAGE_RETURN_WORK,
    SUBPAGE_LEAVE_REGISTER,
    SUBPAGE_DAILY_STATS,
    SUBPAGE_MONTHLY_STATS,
    SUBPAGE_GROUP_ATTENDANCE,
    SUBPAGE_EMPLOYEE_ABSENCE,
]

# ---- Shift Types ----
SHIFT_EARLY = "早班"       # Morning shift
SHIFT_NOON = "午班"        # Afternoon shift
SHIFT_NIGHT = "晚班"       # Night shift (overtime)

# ---- Attendance Record Types ----
TYPE_NORMAL = "正常"
TYPE_BUSINESS_TRIP = "出差"
TYPE_RETURN_WORK = "回工"
TYPE_SICK_LEAVE = "病假"
TYPE_PERSONAL_LEAVE = "事假"
TYPE_SPECIAL_LEAVE = "特殊假"
TYPE_ANNUAL_LEAVE = "年假"
ALL_TYPES = [
    TYPE_NORMAL, TYPE_BUSINESS_TRIP, TYPE_RETURN_WORK,
    TYPE_SICK_LEAVE, TYPE_PERSONAL_LEAVE, TYPE_SPECIAL_LEAVE,
    TYPE_ANNUAL_LEAVE,
]

# ---- Attendance Record Sources ----
SOURCE_MACHINE = "考勤机"
SOURCE_REPLENISH = "补卡"
SOURCE_IMPORT = "导入"
SOURCE_SYSTEM = "系统"
ALL_SOURCES = [SOURCE_MACHINE, SOURCE_REPLENISH, SOURCE_IMPORT, SOURCE_SYSTEM]

# ---- Status Values ----
STATUS_DRAFT = "草稿"
STATUS_EFFECTIVE = "生效"
STATUS_APPROVING = "审批中"
STATUS_CLOSED = "关闭"
STATUS_CANCELLED = "取消"

# ---- Attendance Anomaly Types ----
ANOMALY_NORMAL = "正常"
ANOMALY_ABSENT = "没上班"
ANOMALY_MISSING_CARD = "缺卡"

# ---- Return-to-Work Duration Types ----
DURATION_FULL_DAY = "全天"
DURATION_MORNING = "上午"
DURATION_AFTERNOON = "下午"

# ---- Leave Duration Types ----
LEAVE_FULL_DAY = "全天"
LEAVE_MORNING = "上午"
LEAVE_AFTERNOON = "下午"

# ---- Date Type ----
DATE_TYPE_WORKDAY = "工作日"
DATE_TYPE_WEEKEND = "周末"
DATE_TYPE_HOLIDAY = "节假日"

# ---- HR Status ----
HR_STATUS_ACTIVE = "在职"
HR_STATUS_LEFT = "离职"

# ---- Replenish Card Types ----
REPLENISH_NORMAL = "正常"
REPLENISH_BUSINESS_TRIP = "出差"

# ---- Standard Time Defaults (approximate, set by system) ----
DEFAULT_EARLY_START = "08:00"
DEFAULT_EARLY_END = "12:00"
DEFAULT_NOON_START = "13:30"
DEFAULT_NOON_END = "17:30"
DEFAULT_NIGHT_START = "18:30"
DEFAULT_NIGHT_END = "21:30"

# ---- Boundary Values ----
MAX_DATE_RANGE_DAYS = 90          # 3 months for attendance queries
MAX_LEAVE_RANGE_DAYS = 365        # 1 year for leave queries
MAX_EMPLOYEES_MONTHLY = 500       # Max employees for monthly detail report
MAX_GROUPS_ATTENDANCE = 400       # Max groups for group attendance report
MAX_EMPLOYEE_ID_LENGTH = 20       # Max employee ID character length
MAX_REASON_LENGTH = 200           # Max reason/remarks character length
MAX_YEAR_RANGE = 3                # Max year range for queries

# ---- Calculation Boundaries ----
ROUNDING_HALF_HOUR_THRESHOLD = 0.25  # 0.25h threshold for 0.5h rounding

# ---- Error Messages (expected) ----
MSG_EMPLOYEE_NOT_FOUND = "工号不存在。"
MSG_NO_RECORD_SELECTED = "没有选择记录"
MSG_NO_EMPLOYEE_REGISTERED = "没有登记员工，不能生效。"
MSG_DATE_BEFORE_TODAY_RETURN = "回工日期小于今日，反生效会影响已有考勤统计，是否继续？"
MSG_DATE_BEFORE_TODAY_LEAVE = "开始时间小于今日，反生效会影响已有考勤统计，是否继续？"
MSG_SELECT_SAME_DATE = "请选择相同日期。"
MSG_SELECT_SAME_SHIFT = "请选择相同班次。"
MSG_SELECT_TIME_PERIOD = "请选择考勤时段。"
MSG_ENTER_REPLENISH_TIME = "请输入选中考勤时段的补卡时间。"
MSG_LEAVE_OVERLAP = "请假时间范围内存在其他请假。"
MSG_EMPLOYEES_EXCEED_500 = "员工已经超出500人。"
MSG_DATE_OUT_OF_RANGE = "起始日期不可超出3个月前或大于今天。"
MSG_CONFIRM_DELETE = "是否确认删除？"
MSG_PLEASE_SELECT_RECORD = "请选择记录。"
MSG_PLEASE_SELECT_EMPLOYEE = "请选择回工员工。"
MSG_PLAN_LAYERS_MUST_POSITIVE = "计划层数必须大于0"
