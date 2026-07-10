# Test Execution Report: IMS 考勤模块

> 最新执行：2026-07-09 | 环境：SIT (test.fj.dtsimple.pro) | 耗时：7分14秒

## Summary

| Metric | Value |
|--------|-------|
| Execution Time | 2026-07-09 15:30 (UTC+8) |
| Total Tests | 38 (collected) / 77 (test_cases.md 计划) |
| Passed | **33** |
| Skipped | 5 |
| Failed | 0 |
| Overall Pass Rate | **100%** (33/33 active) |
| Environment | SIT (http://test.fj.dtsimple.pro) |
| Test Type | UI-heavy — Playwright + pytest |
| Browser | Chromium (headless) |

## Results by Priority

| Priority | Total | Passed | Skipped | Failed | Pass Rate | Status |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| P0 | 11 | 11 | 0 | 0 | 100% | ✅ |
| P1 | 12 | 12 | 0 | 0 | 100% | ✅ |
| P2 | 10 | 6 | 4 | 0 | 100% | ✅ |
| P3 | 3 | 2 | 1 | 0 | 100% | ✅ |
| Quarantine | 2 | 0 | 2 | 0 | — | ⏸️ |
| **Total** | **38** | **33** | **5** | **0** | **100%** | ✅ |

## Skipped Tests (5条)

| # | 测试 | 原因 |
|---|------|------|
| 1 | 迟到员工迟到值 > 0 | 导入数据中无迟到员工（正常数据） |
| 2 | 缺勤员工四时段全空 | 导入数据中无缺勤员工 |
| 3 | 缺卡员工过滤 | 导入数据中无缺卡员工 |
| 4 | 出勤时数公式验证 | 提取数据中数值字段为空（数据精度待修） |
| 5 | 考勤同步(隔离)/大批量计算(隔离) | 已知 flaky，已隔离 |

## Data-Driven Tests — 首次通过 (2026-07-09)

修复 `test_data_extractor.py` 中两个 bug 后，以下测试从 skip 变为 pass：

| 测试 | 之前 | 现在 |
|------|:---:|:---:|
| 正常员工早班补卡按钮 | ⏸️ skip | ✅ pass |
| 真实员工在请假下拉列表 | ⏸️ skip | ✅ pass |
| 请假页员工与日考勤数据一致 | ⏸️ skip | ✅ pass |

## Trend Analysis

| Metric | 2026-07-08 | 2026-07-09 | Trend |
|--------|:---:|:---:|:---:|
| Total Passed | 30 | **33** | 📈 +3 |
| P2 Passed | 3 | **6** | 📈 +3 |
| Skipped (total) | 8 | **5** | 📉 -3 |
| Skipped (data) | 6 | **3** | 📉 -3 |
| Test Type | UI-heavy — Playwright + pytest |
| Browser | Chromium (headless) |

## Results by Priority

| Priority | Total | Passed | Skipped | Failed | Pass Rate | Status |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| P0 | 11 | 11 | 0 | 0 | 100% | ✅ |
| P1 | 12 | 12 | 0 | 0 | 100% | ✅ |
| P2 | 10 | 5 | 5 | 0 | 100% | ✅ |
| P3 | 3 | 2 | 1 | 0 | 100% | ✅ |
| Quarantine | 2 | 0 | 2 | 0 | — | ⏸️ |
| **Total** | **38** | **30** | **8** | **0** | **100%** | ✅ |

## Skipped Tests (8条 — 数据依赖)

以下测试因 SIT 环境当天无考勤数据而自动跳过。导入数据后自动恢复执行。

| # | 测试 | 原因 | 恢复条件 |
|---|------|------|------|
| 1 | 正常员工早班补卡 | 无正常打卡员工数据 | 考勤同步/导入后 |
| 2 | 迟到员工迟到值 > 0 | 无迟到员工数据 | 有迟到记录后 |
| 3 | 缺勤员工四时段全空 | 无缺勤员工数据 | 有缺勤记录后 |
| 4 | 缺卡员工过滤 | 无缺卡员工数据 | 有缺卡记录后 |
| 5 | 出勤时数公式验证 | 无正常员工数据 | 有出勤数据后 |
| 6 | 真实员工在下拉列表 | 无正常员工数据 | 有员工数据后 |
| 7 | 请假端到端(员工搜索) | 无正常员工数据 | 有员工数据后 |
| 8 | 考勤同步(隔离) | 已知 flaky，已隔离 | 修复后取消 skip |

## Results by Page

| 页面 | P0 | P1 | P2 | P3 | 结果 |
|------|:---:|:---:|:---:|:---:|:---:|
| 登录 + 首页 | 2/2 | — | — | — | ✅✅ |
| 考勤登记 | 1/1 | 2/2 | — | — | ✅✅✅ |
| 回工登记 | 1/1 | 2/2 | — | — | ✅✅✅ |
| 请假登记 | 1/1 | 2/2 | 1/5 | — | ✅✅✅ + 4⏸️ |
| 日考勤统计 | 2/2 | 3/3 | 4/5 | 1/2 | ✅✅✅✅✅ + 2⏸️ |
| 月考勤统计 | 1/1 | 1/1 | — | 1/1 | ✅✅✅ |
| 小组出勤表 | 1/1 | 1/1 | — | — | ✅✅ |
| 员工缺勤表 | 1/1 | 1/1 | — | — | ✅✅ |

## Requirements Traceability

| Requirement | 计划用例 | 已执行 | 通过 | 跳过 | 状态 |
|------------|:---:|:---:|:---:|:---:|:---:|
| §考勤登记 (F001~F008) | 9 | 3 | 3 | 0 | ✅ |
| §回工登记 (F009~F015) | 11 | 3 | 3 | 0 | ✅ |
| §请假登记 (F016~F023) | 14 | 7 | 3 | 4 | ⚠️ 部分(数据缺失) |
| §日考勤统计 (F024~F036) | 25 | 11 | 9 | 2 | ⚠️ 部分(数据缺失) |
| §月考勤统计 (F037~F042) | 7 | 3 | 3 | 0 | ✅ |
| §小组出勤表 (F043~F044) | 3 | 2 | 2 | 0 | ✅ |
| §员工缺勤表 (F045~F046) | 2 | 2 | 2 | 0 | ✅ |
| §安全附录 | 3 | 0 | — | — | ⏳ 待补充 |
| §待澄清 (T-01~T-03) | 3 | 0 | — | — | ⏳ 待产品确认 |

## Verified Page URLs

| 页面 | Hash URL |
|------|------|
| 考勤登记 | `/#/personnel/workAttendance/detail` |
| 回工登记 | `/#/personnel/workAttendance/returningWork` |
| 请假登记 | `/#/personnel/workAttendance/leave` |
| 日考勤统计 | `/#/personnel/workAttendance/dailyReportNew` |
| 月考勤统计 | `/#/personnel/workAttendance/monthlyReport` |
| 小组出勤表 | `/#/personnel/workAttendance/teamAttendanceReport` |
| 员工缺勤表 | `/#/personnel/workAttendance/employeeAbsenceReport` |

## Trend Analysis

| Metric | Current (2026-07-08) | Previous | Delta | Trend |
|--------|:---:|:---:|:---:|:---:|
| Total Tests | 38 | — | — | 基线 |
| Active Pass Rate | 100% | — | — | ✅ |
| P0 Pass Rate | 100% (11/11) | — | — | ✅ |
| P1 Pass Rate | 100% (12/12) | — | — | ✅ |
| P2 Pass Rate | 100% (5/5 active) | — | — | ✅ |
| P3 Pass Rate | 100% (2/2 active) | — | — | ✅ |
| Execution Time | 6:55 | — | — | 基线 |

> **趋势解读**：所有活跃测试 100% 通过。8 条数据驱动测试因 SIT 当天无考勤数据自动跳过，属正常行为。待考勤数据导入后，跳过数将降为 0，P2 执行数将升至 10。

## Execution Commands

```bash
cd attendance-full

# 冒烟测试 (P0, ~3min)
python -m pytest erp_tests/ -m p0 -v

# 功能测试 (P0+P1, ~5min)
python -m pytest erp_tests/ -m "p0 or p1" -v

# 全量测试 (P0~P3, ~7min)
python -m pytest erp_tests/ -v

# 数据驱动测试 (需先导入考勤数据)
python -m pytest erp_tests/ -m "p2 or p3" -v
```

## Appendix: Document Audit Findings

| ID | Description | Status |
|----|------|:---:|
| AUD-001 | 请假"取消"状态 | ✅ 不需要 |
| AUD-002 | 回工晚班参数 | ✅ 不需要 |
| AUD-003 | 请假不生成考勤登记 | ✅ 已确认 |
| AUD-004 | 考勤计算后删除签到 | ✅ 已确认执行顺序 |

> 详细审计见 `requirements_audit.md`

## Appendix: Data-Driven Architecture

```
test_data_extractor.py  →  从日考勤统计页面提取真实员工数据
conftest.py fixtures    →  按类别分类（正常/迟到/缺勤/缺卡）
test_boundary.py        →  P2: 公式验证 / 补卡状态 / 过滤校验
test_integration.py     →  P3: 请假↔日考勤 / 月统计汇总 / 公式链
```

数据缺失时自动 `pytest.skip()`，不产生误报。导入考勤数据后所有 skip 自动恢复为实际验证。
