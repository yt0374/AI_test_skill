# erp_tests/utils/test_data.py
"""Static test data constants for 考勤模块 tests."""

# SIT environment
SIT = {
    "url": "http://test.fj.dtsimple.pro",
    "username": "admin",
    "password": "metas2660",
    "enterprise": "最佳智造",
}

# Attendance type values
ATTENDANCE_TYPES = {
    "正常": "正常",
    "出差": "出差",
    "回工": "回工",
    "病假": "病假",
    "事假": "事假",
    "特殊假": "特殊假",
    "年假": "年假",
}

# Attendance sources
ATTENDANCE_SOURCES = {
    "考勤机": "考勤机",
    "补卡": "补卡",
    "导入": "导入",
    "系统": "系统",
}

# Return work duration
RETURN_WORK_DURATIONS = ["全天", "上午", "下午"]

# Leave durations
LEAVE_DURATIONS = ["全天", "上午", "下午"]

# Reissue types
REISSUE_TYPES = ["正常", "出差"]

# Attendance anomaly
ATTENDANCE_ANOMALIES = ["正常", "没上班", "缺卡"]

# Date types
DATE_TYPES = ["工作日", "周末", "节假日"]

# Status values
RETURN_WORK_STATUSES = ["草稿", "生效"]
LEAVE_STATUSES = ["草稿", "审批中", "生效", "关闭", "取消"]

# HR module navigation paths (SIT environment)
HR_MENU_ITEMS = [
    "员工档案", "工资预支", "在职月工资",
    "请假登记", "回工登记", "考勤登记",
    "日考勤统计", "月考勤统计",
    "小组出勤表", "员工缺勤表", "月考勤统计表",
    "计件登记", "日计件统计", "月计件统计",
    "班次设置", "假类设置", "节假日设置",
    "工资汇率设置", "工资项设置",
]

# Expected error messages (from PRD)
ERROR_MESSAGES = {
    "no_selection": "没有选择记录",
    "please_select": "请选择记录。",
    "same_date_required": "请选择相同日期。",
    "same_shift_required": "请选择相同班次。",
    "choose_period": "请选择考勤时段。",
    "enter_time": "请输入选中考勤时段的补卡时间。",
    "confirm_delete": "是否确认删除？",
    "employee_not_found": "工号不存在。",
    "no_return_employees": "没有登记员工，不能生效。",
    "choose_return_employees": "请选择回工员工。",
    "leave_overlap": "请假时间范围内存在其他请假。",
    "date_out_of_range": "起始日期不可超出3个月前或大于今天。",
    "employees_exceed_500": "员工已经超出500人。",
    "ret_work_date_confirm": "回工日期小于今日，反生效会影响已有考勤统计，是否继续？",
    "leave_date_confirm": "开始时间小于今日，反生效会影响已有考勤统计，是否继续？",
}

# Rounding test data for overtime hours (0.5h rounding)
OVERTIME_ROUNDING = [
    (1.149, 1.0),    # 1.149 -> 1H
    (1.15, 1.5),     # 1.15 -> 1.5H
    (1.649, 1.5),    # 1.649 -> 1.5H
    (1.65, 2.0),     # 1.65 -> 2H
    (1.85, 2.0),     # 1.85 -> 2H
    (0.749, 0.5),    # 0.749 -> 0.5H
    (0.25, 0.0),     # 0.25 -> 0H
]

# Boundary test values for length constraints
LENGTH_BOUNDARIES = {
    "工号": {"max": 20, "tests": [(20, True), (21, False)]},
    "事由": {"max": 200, "tests": [(200, True), (201, False)]},
    "考勤机": {"max": 20, "tests": [(20, True), (21, False)]},
}
