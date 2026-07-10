"""IMS Attendance — Static Test Data Constants"""

# SIT Environment
SIT_BASE_URL = "http://test.fj.dtsimple.pro"

# Default User Credentials (override via env vars)
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "metas2660"

# Page Paths
PATH_ATTENDANCE_REGISTRATION = "/attendance/registration"
PATH_RETURN_WORK = "/attendance/return-work"
PATH_LEAVE_REGISTRATION = "/attendance/leave-registration"
PATH_DAILY_STATISTICS = "/attendance/daily-statistics"
PATH_MONTHLY_STATISTICS = "/attendance/monthly-statistics"
PATH_GROUP_ATTENDANCE = "/attendance/group-attendance"
PATH_EMPLOYEE_ABSENCE = "/attendance/employee-absence"

# Attendance Types
ATTENDANCE_TYPES = ["正常", "出差", "回工", "病假", "事假", "特殊假", "年假"]
ATTENDANCE_SOURCES = ["考勤机", "补卡", "导入", "系统"]
ATTENDANCE_EXCEPTIONS = ["正常", "没上班", "缺卡"]
DATE_TYPES = ["工作日", "周末", "节假日"]

# Leave Durations
LEAVE_DURATIONS = ["全天", "上午", "下午"]
RETURN_WORK_DURATIONS = ["全天", "上午", "下午"]

# Shift Periods (for batch mend card)
SHIFT_PERIODS = [
    "早班上班时间", "早班下班时间",
    "午班上班时间", "午班下班时间",
    "晚班上班时间", "晚班下班时间",
]

# Field Lengths
MAX_REASON_LENGTH = 200
MAX_EMPLOYEE_ID_LENGTH = 20
MAX_MACHINE_ID_LENGTH = 20

# Date Range Limits
MAX_QUERY_SPAN_DAYS = 90       # 3 months for attendance queries
MAX_LEAVE_QUERY_SPAN_DAYS = 365 # 1 year for leave queries
MAX_MONTHLY_QUERY_YEARS = 3     # 3 years for monthly statistics
MAX_GROUP_ATTENDANCE_ROWS = 400
MAX_MONTHLY_PRINT_EMPLOYEES = 500

# Overtime Rounding
OVERTIME_ROUNDING_UNIT = 0.5
