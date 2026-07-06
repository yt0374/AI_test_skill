# Traceability Report: 荆门新裁剪需求2.0

> 生成日期：2026-07-03
> 需求文档：D:\需求文档\荆门-新裁剪需求2.0.docx
> 测试环境：SIT → 荆门模拟生产 (bak.jmym.dtsimple.pro)

---

## Requirements-to-Tests Mapping

| Req ID | Requirement | Section | Test IDs | Count | Status |
|--------|-------------|---------|----------|:---:|:---:|
| F001 | 裁剪任务创建-多CPO合并 | PRD §1 | C-01, V-01, F-01 | 3 | DESIGNED |
| F002 | 裁剪任务创建-全选CPO | PRD §1 | C-03 | 1 | DESIGNED |
| F003 | 裁剪任务创建-智能合并 | PRD §1 | C-02 | 1 | DESIGNED |
| F004 | 唛架计划层数分配与递减 | PRD §1 | C-04, C-05, V-04, V-05 | 4 | DESIGNED |
| F005 | 唛架防超分配校验 | PRD §1 | V-02, V-03, F-01 | 3 | DESIGNED |
| F006 | 顶层裁剪任务管理(PC) | PRD §2 | C-06 | 1 | DESIGNED |
| F007 | 裁剪任务状态管理 | PRD §2 | U-01, U-02, U-03, X-01, X-02 | 5 | DESIGNED |
| F008 | 床次创建(PAD) | PRD §2 | C-07, V-12, V-13 | 3 | DESIGNED |
| F009 | 并发防超检验 | PRD §2 | V-08, V-09, P-01 | 3 | DESIGNED |
| F010 | 床次提交完成 | PRD §2 | C-08, C-09, V-14 | 3 | DESIGNED |
| F011 | 床次号生成与唯一性 | PRD §2 | V-06, V-07 | 2 | DESIGNED |
| F012 | 防超裁-软预警 | PRD §2 | V-10 | 1 | DESIGNED |
| F013 | 防超裁-强控禁止 | PRD §2 | V-11 | 1 | DESIGNED |
| F014 | 超裁审核(PC) | PRD §2 | C-10, C-11, P-02 | 3 | DESIGNED |
| F015 | 扎卡打印-合并CPO | PRD §3 | V-15, V-17, F-01 | 3 | DESIGNED |
| F016 | 扎卡打印-单一CPO | PRD §3 | V-16, V-18, F-02 | 3 | DESIGNED |
| F017 | 挂片匹配-合并CPO | PRD §4 | V-19, F-01 | 2 | DESIGNED |
| F018 | 挂片匹配-单一CPO | PRD §4 | V-20, V-21, F-02 | 3 | DESIGNED |
| F019 | 自动充数模式 | PRD §4 | V-22, F-07, F-02 | 3 | DESIGNED |
| F020 | 手动充数模式 | PRD §4 | V-23, V-24, F-05 | 3 | DESIGNED |
| F021 | 模式切换联动 | PRD §4 | F-04, F-06 | 2 | DESIGNED |
| **Total** | **21 requirements** | | **49 unique test IDs** | **54** | |

---

## PRD-to-Test Section Mapping

| PRD Section | Title | Test Case Range | Coverage |
|-------------|-------|-----------------|----------|
| §1 | 裁剪任务模块（新增CPO维度，支持合并） | C-01~C-05, V-01~V-05, U-01~U-03, X-01~X-02 | 15 tests |
| §2 | 床次任务与现场拉布模块 | C-06~C-11, V-06~V-14, P-01~P-02 | 19 tests |
| §3 | 扎卡打印模块（CPO关联规则） | V-15~V-18 | 4 tests |
| §4 | 缝制挂片模块（自动/手动充数） | V-19~V-24, F-04~F-07 | 10 tests |
| §1-4 | 端到端核心流程 | F-01~F-03 | 3 tests |

---

## Table-to-Test Mapping

| PRD Table | Content | Test IDs |
|-----------|---------|----------|
| Table 0 | 模块核心变更概览 | F-01~F-03 |
| Table 1 | 床次号示例 | V-06, V-07 |
| Table 2 | 状态流转定义 | U-01~U-03, X-01~X-02 |
| Table 3 | 扎卡CPO概览规则 | V-15, V-16 |
| Table 4 | 挂片匹配联动 | V-19, V-20, V-21 |
| Table 5 | 分扎计件规则 | V-17, V-18 |
| Table 6 | 自动充数规则 | V-19, V-20, V-22 |
| Table 7 | 模式切换规则 | F-04, F-06 |

---

## Uncovered Items

| Item | Reason | Impact | Recommendation |
|------|--------|:---:|------|
| 性能指标 | PRD未定义 | Low | 增加N-P-01(T-08)占位 |
| API接口定义 | PRD未提供 | Medium | 建议开发提供裁剪任务API规范 |
| 干燥房集成 | PRD未涉及裁剪与干燥房交互 | Medium | 确认裁剪→干燥房→挂片数据流 |
| 报表联动 | PRD未涉及 | Low | 裁剪日报表应考虑CPO维度 |

---

## Coverage Summary

| Metric | Value |
|--------|:---:|
| Total requirements | 21 |
| Requirements with tests | 21 (100%) |
| Total PRD paragraphs | 137 |
| Paragraphs mapped to tests | 137 (100%) |
| Total PRD tables | 8 |
| Tables mapped to tests | 8 (100%) |
| Total test cases | 63 |
| Data-driven variants | 24 |

---

## Quality Gate

| Gate | Status | Notes |
|------|:---:|------|
| 100% requirements covered | PASS | 21/21 |
| 100% tables covered | PASS | 8/8 |
| P0 <= 20% | PASS | 12.7% (8/63) |
| Cross-module tests present | PASS | P-01, P-02 |
| Data-driven tests present | PASS | 24 variants across 6 datasets |
| 13 clarification items logged | PASS | T-01~T-13 in test_cases.md |
| All boundary values have trio | PASS | 6 thresholds with -1/boundary/+1 |
| Environment order defined | PASS | SIT → jingmen |

**Overall: 8/8 gates passed — ready for execution.**
