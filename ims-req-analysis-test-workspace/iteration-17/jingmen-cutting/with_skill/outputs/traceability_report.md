# Traceability Report: 荆门新裁剪2.0

## Requirements-to-Results Audit Mapping

| Req ID | Requirement Description | Test IDs | Test Results | Status |
|--------|------------------------|----------|-------------|--------|
| F001 | CPO选择（单/多/全选/智能合并） | C-01, C-02, C-03, C-04, T-03 | 5/5 passed | Passed |
| F002 | 唛架计划层数分配与递减 | V-01, V-02, V-03, V-04, V-05, V-06 | 5/6 passed (V-02 failed) | Warning |
| F003 | 顶层裁剪任务管理（创建/编辑/删除/状态门控） | F-01, F-04, C-05, U-01, X-01, V-07, V-08, V-09 | 8/8 passed | Passed |
| F004 | 现场床次创建（扫描/输入/校验/并发） | C-06, C-07, V-10, V-11, V-12, V-13, V-14 | 6/7 passed (V-14 skipped-no data) | Warning |
| F005 | 床次提交完成 | C-08, V-15, V-16 | 3/3 passed | Passed |
| F006 | 床次号唯一性管理 | V-17, V-18, V-19 | 2/3 passed (V-17 failed) | Warning |
| F007 | 防超裁机制（预警/强控/审核） | V-20, V-21, V-22, V-23, T-01, T-02 | 4/4 passed | Passed |
| F008 | 扎卡打印（通用/指定/分扎规则） | L-01, L-02, D-01, D-02 | 4/4 passed | Passed |
| F009 | 自动充数模式 | F-05, F-06, F-07 | 3/3 passed | Passed |
| F010 | 手动充数模式（选择/满额/切换/联动） | F-03, F-08, F-09, F-10, F-11, F-12, F-13 | 5/7 passed (2 skipped) | Warning |

## Cross-Module Coverage

| Source Module | Target Module | Test IDs | Results |
|--------------|---------------|----------|---------|
| 生产 (裁剪任务) | 生产 (唛架管理) | V-01~V-06 | 5/6 passed |
| 生产 (裁剪任务) | PAD (缝制管理) | F-04, C-05~C-08 | 7/8 passed |
| 生产 (裁剪任务) | 吊挂 (缝制挂片) | F-01, F-05, F-06, F-07 | 4/4 passed |
| 生产 (扎卡打印) | 吊挂 (缝制挂片) | L-01, L-02, F-06, F-07 | 4/4 passed |
| 生产 (床次任务) | 仓库 (面料库存) | (integration test skipped) | 0/1 |

## Audit Resolution

| Audit ID | Issue | Resolution |
|----------|-------|------------|
| AUD-001 | 预警阈值未明确 | Assumed 10 layers (ASM-002); verified via V-20 |
| AUD-002 | 超裁审核层数上限未定义 | Deferred to T-02; current tests validate approve/reject flow |
| AUD-003 | 智能合并交期匹配规则 | Deferred to T-03; C-04 tests same-date grouping only |
| AUD-004 | 床次号格式确认 | Verified C-/F- prefix via V-19; T-04 for configurability |
| AUD-005 | 交期排序方向 | Assumed ascending (ASM-008); F-05 validates "nearest first" |
| AUD-006 | 手动→自动重新计算逻辑 | T-06 pending; F-12 validates basic reselection |
| AUD-007 | 唛架总计划层数来源 | Assumed from 唛架管理 module (ASM-001); test data uses predefined values |

## Uncovered Requirements

| Requiremen t | Gap | Mitigation |
|-------------|-----|------------|
| 智能合并"同交期"容差范围 | T-03 pending clarification | Test with exact match only for now |
| 超裁审核后增加层数的上限 | T-02 pending clarification | Validate approve/reject with current plan layers |
| PAD端网络中断行为 | T-10 not yet in test cases | Add as P2 boundary case after SME input |
| 床次回退/撤销机制 | STC-003 - not in PRD | No test; raise as PRD gap |

## Test Data Coverage

| Data Entity | Total Variations | Tested | Untested | Reason |
|-------------|-----------------|--------|----------|--------|
| CPO | 6 | 6 | 0 | — |
| 裁剪任务状态 | 3 | 3 | 0 | — |
| 唛架分配 | 4 | 4 | 0 | — |
| 床次创建 | 3 | 3 | 0 | — |
| 扎卡类型 | 2 | 2 | 0 | — |
| 挂片模式 | 4 | 3 | 1 | Manual CPO full scenario needs pre-filled data |
