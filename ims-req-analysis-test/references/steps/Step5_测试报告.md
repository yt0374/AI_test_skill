# Step 5: 测试报告

> 承接 Step 4（pytest_results.json）| 产出：report + traceability + exec_log + defects

---

## 5.1 报告产出

| 文件 | 格式 | 受众 |
|------|:---:|------|
| `test_report.md` | Markdown 摘要 | 业务干系人 |
| `traceability_report.md` | Markdown 追溯 | 审计/合规 |
| `TEST_EXECUTION_LOG.md` | Markdown 记录 | 持续追踪 |
| `pytest_results.json` | JSON | CI 集成 |
| `defects/` | Markdown | 开发团队 |

## 5.2 报告结构

```markdown
# 测试执行报告
## 摘要（通过率/耗时/总数）
## 优先级分布（P0~P3）
## 模块分布
## 失败详情（根因+建议）
## 需求追溯（需求→用例→结果）
## 趋势分析（历史对比）
## 缺陷清单
```

## 5.3 趋势分析（MANDATORY）

| 首次执行 | 有历史数据 |
|------|------|
| 占位符 + "首次执行，下次运行后可用" | 真实delta + Improving/Watch/Action分析 |

## 5.4 缺陷模板（承接失败用例）

```markdown
## BUG-001: [标题]
| 严重度 | 模块 | 构建 | 环境 |
### 复现步骤
### 期望 vs 实际
### 附件
```

## 5.5 执行记录（自动追加）

每次执行自动生成/更新 `TEST_EXECUTION_LOG.md`：

| 字段 | 说明 |
|------|------|
| 执行摘要 | 总数/已执行/通过/失败/通过率/结论 |
| 环境记录 | 环境/日期/结果/说明 |
| 用例明细 | 用例ID/环境/结果/说明 |
| 待修复项 | 问题/修复方案/优先级 |

首次执行→创建文件。后续→追加条目+更新摘要。

## 5.6 产出清单

| 文件 | → 流向 |
|------|:---:|
| `test_report.md` | → Step 6 |
| `traceability_report.md` | → 审计 |
| `TEST_EXECUTION_LOG.md` | → 持续追踪 |
| `defects/` | → 开发团队 |
