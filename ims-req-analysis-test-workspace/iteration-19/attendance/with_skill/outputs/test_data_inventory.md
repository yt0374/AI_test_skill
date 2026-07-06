# Test Data Inventory: 考勤模块

> 数据来源：module_texts.txt + 考勤.md需求文档 | 日期：2026-07-03

---

## 1. Users/Roles

| Role | Pattern | Use in Testing |
|------|---------|---------------|
| gm.人事#1 | Primary HR operator | HR模块全部页面可访问 |

---

## 2. Entity Types & Variations

### 2.1 Employee Status
| Variation | Description | Required for |
|-----------|-------------|-------------|
| 在职 | Active employee | 正常考勤/请假/回工 |
| 离职(近3月) | Resigned within 3 months | 考勤登记/日考勤统计员工查询范围 |
| 离职(超3月) | Resigned >3 months | 不可见（不在查询范围） |
| 孕期 | Within pregnancy period | 孕期差异化签到/签退时间 |
| 哺乳期 | Within lactation period | 哺乳期差异化签到/签退时间 |

### 2.2 Attendance Type
| Variation | Code | Use in Testing |
|-----------|------|---------------|
| 正常 | Normal | 考勤机同步/导入/补卡产生 |
| 出差 | Business Trip | 补卡时可选 |
| 回工 | Return-to-Work | 回工登记生效时系统生成 |
| 病假 | Sick Leave | 请假登记生效时系统生成 |
| 事假 | Personal Leave | 请假登记生效时系统生成 |
| 特殊假 | Special Leave | 请假登记生效时系统生成 |
| 年假 | Annual Leave | 请假登记生效时系统生成 |
| 拓展假类1~6 | Custom Leave Types | 默认不启用，按客户配置 |

### 2.3 Attendance Source
| Variation | Code | Required for |
|-----------|------|-------------|
| 考勤机 | Machine | 同步功能 |
| 补卡 | Reissue | 补卡操作 |
| 导入 | Import | Excel/TXT导入 |
| 系统 | System | 回工/请假自动生成 |

### 2.4 Shift Types (for calculation testing)
| Variation | Shifts | Required for |
|-----------|--------|-------------|
| 一班制 | 早班 only | 基本考勤计算 |
| 二班制 | 早班+午班 | 正常班次计算 |
| 三班制 | 早班+午班+晚班 | 加班计算 |

### 2.5 Date Type
| Variation | Description | Required for |
|-----------|-------------|-------------|
| 工作日 | Workday | 正班时数计算 |
| 周末 | Weekend | 周末加班时数计算 |
| 节假日 | Holiday | 节假日加班时数计算 |

### 2.6 Attendance Anomaly
| Variation | Description | Required for |
|-----------|-------------|-------------|
| 正常 | Normal | 正常打卡 |
| 没上班 | No show | 工作日全天无打卡且未请假 |
| 缺卡 | Missing punch | 部分打卡缺失 |

### 2.7 Leave Type
| Variation | Properties | Required for |
|-----------|-----------|-------------|
| 年假 | 计薪比例=1 | 带薪假计算 |
| 病假 | 计薪比例可配置 | 带薪假计算 |
| 事假 | 计薪比例=0（通常） | 无薪假计算 |
| 特殊假 | 计薪比例可配置 | 带薪假计算 |
| 拓展假类 | 计薪比例可配置 | 自定义假类计算 |

### 2.8 Return-to-Work Duration
| Variation | Start Time | End Time |
|-----------|-----------|----------|
| 全天 | 默认早班上班时间 | 默认午班下班时间 |
| 上午 | 默认早班上班时间 | 默认早班下班时间 |
| 下午 | 默认午班上班时间 | 默认午班下班时间 |

---

## 3. Real Test Data References

### 3.1 Employee IDs (from module_texts.txt)
| ID Pattern | Example | Name Pattern |
|-----------|---------|-------------|
| 100xxx (Chinese) | 100072 | CHEN FEIMAN |
| 101xxx (Khmer) | 101035 | Mixed |
| 108xxx (Khmer) | 108481 | Khmer names |

### 3.2 Organizational Units
Based on the HR menu structure, the organization uses:
- 部门 (Department) - from 部门管理 in 系统 module
- 组别 (Group) - subordinate to department

### 3.3 Test Data Dimensions for Boundary Testing

| Dimension | Values | Tests |
|-----------|--------|-------|
| 考勤日期范围 | 跨度1天/1月/3月/3月+1天 | V-01, V-02 |
| 员工数(回工) | 0/1/N | V-11, V-12 |
| 员工数(月考勤表) | 1/500/501 | V-27, V-28 |
| 加班0.5h四舍五入 | 1.149/1.15/1.649/1.85 | V-21~V-24 |
| 工时<起计时长 | 起计-1min/起计/起计+1min | V-25, V-26 |
| 迟到<免计时长 | 免计-1min/免计/免计+1min | V-29, V-30 |
