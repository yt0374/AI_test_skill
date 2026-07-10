---
name: ims-req-analysis-test
description: >-
  ERP需求分析与测试全生命周期：需求分析→生成测试用例→Playwright自动化脚本和执行→测试报告。
  专为瑞晟IMS智能制造协同平台设计，内置官方文档知识库（状态机、业务规则、计算公式、错误消息、跨模块数据流）。
  当用户提到以下任一内容时必须使用此skill：瑞晟、IMS、智能制造协同平台、module_texts、ERP测试、ERP需求分析、
  测试用例生成、测试计划、测试执行、测试报告、Playwright自动化、数据驱动测试、销售/采购/生产/仓库/质检/吊挂/物流/
  报表/数据模块分析、业务流程测试、状态机测试、P0/P1/P2/P3测试用例、pytest测试脚本。任何涉及瑞晟ERP模块的
  需求分析或测试工作都应触发此skill。
---

# IMS ERP 需求分析与测试生成

为 **瑞晟智能制造协同平台** 提供完整测试生命周期：
**需求分析 → 生成测试用例 → Playwright自动化脚本和执行 → 测试报告**

## Core Principle: Data-Driven Testing

ERP 系统是数据密集型的 — 同一业务逻辑适用于大量不同实体。单一数据点测试是不够的，因此**测试数据是一等交付物**。每个阶段都从 ERP 系统中提取、编目和利用真实数据。

## System Context

- **数据源**: `module_texts.txt`（项目根目录或 `Documents/ERP-test/`）— 页面结构、实体实例、数据模式。**始终先读这个文件。**
- **环境配置**: `environments/` 目录 — SIT/UAT/xinji/jingmen/ajn 五环境 URL、选择器、模块名。默认 `sit` 环境。
- **设备终端**: PC（管理功能）、PAD（平板触控）、PDA（扫码）、工业平板（工位固定）。详见 `references/consolidated_domain_knowledge.md`。
- **领域知识**: 主参考 `references/consolidated_domain_knowledge.md`（状态机、校验规则、计算公式），模块详情见 `references/feature_*.md`，字段定位器见 `references/page_field_dictionary.md`。

**参考文件加载策略（按需）：**

| 场景 | 加载文件 |
|------|---------|
| **始终加载** | `consolidated_domain_knowledge.md` |
| UI 流程 | `功能测试用例验收标准.md` + `测试用例模版.md` |
| API 规格 | `接口自动化测试用例验收标准.md` |
| 客户定制 | `customer_variants.md` + `environments/{name}.json` |
| 特定模块 | `feature_{module}.md`（如存在） |
| **UI 自动化** | `ims_ui_automation_patterns.md` — Ant Design/IMS 交互坑点 |
| Light 模式 | 仅始终加载的3个文件 |

## When to Use

- 描述了 ERP 的业务需求或功能需求
- 要求"需求分析"或"生成测试用例"
- 提供了 PRD、规格文档或用户故事
- 要为特定 ERP 模块制定测试计划
- 要创建 Playwright 自动化测试脚本

## Step 0: Requirement Classification

| Type | Signals | Strategy |
|:---:|------|------|
| **新增** | New module/API, no "change/optimize" keywords | Full 6-step lifecycle |
| **变更** | "调整/改为/新增字段/优化逻辑" | Change impact analysis + regression, output `change_impact.md` |
| **存量** | "补充XX模块用例", no standalone doc | Baseline gap fill, cross-reference `mainline_baseline.md` |

详见 `references/steps/Step0_需求分类.md`

---

## Complete Workflow

```
Input (Doc/Conversation)
  │
  ├─[1] 需求分析 → requirements_spec.md + requirements_audit.md + test_data_inventory.md
  ├─[2] 测试用例 → test_cases.md (8章统一文档) + test_coverage_matrix.md + test_data.csv/json
  ├─[3] 自动化   → erp_tests/ (Playwright+pytest) + pytest.ini + run_tests.sh/ps1
  └─[4] 测试报告 → test_report.md + traceability_report.md + defects/
```

---

# 1. 需求分析

## 1.1 提取需求

从输入中提取：**功能点(F-xx)**、**业务规则(R-xx)**、**数据流转**、**角色/参与者**、**前置/后置条件**、**边界/异常场景**。

## 1.2 文档质量审计（必做）

真实需求文档常有错误，在传播到测试用例前主动识别：

- **API/接口问题**: 字段名冲突、数据类型不匹配、占位符/复用字段名
- **枚举问题**: 基数不匹配、缺失空值处理、未定义枚举值
- **结构问题**: 缺失回调字段、不完整状态转换、未定义错误场景

输出 `requirements_audit.md`（Critical Issues / Warnings / Assumptions 三表格式）。

## 1.3 状态机分析

对需求中涉及的每个实体，识别生命周期状态和合法转换。**每个状态转换 = 一个测试用例**（合法→P1，非法→P2）。

参考 `references/consolidated_domain_knowledge.md` 中已编目的状态机。

## 1.4 测试数据编目

扫描 `module_texts.txt` 提取实体数据：Users(`gm.模块名#N`)、Materials(`ML`前缀码)、Customers、Warehouse Types、Status Values、Date/Time Formats、ID Conventions。

输出 `test_data_inventory.md`：每个实体类型识别变化维度并编目。

## 1.5 输出: `requirements_spec.md`

```markdown
# Requirements Specification: [Feature/Module]
## 1. Overview + Business Context
## 2. Functional Points (F001, F002...)
## 3. Business Rules (R001, R002...)
## 4. Data Flow (with ASCII diagrams)
## 5. Cross-Module Dependencies
## 6. Data Entities & Variations (ref test_data_inventory.md)
## 7. Edge Cases & Constraints
```

---

# 2. 生成测试用例

## 2.1 优先级框架

| 优先级 | 范围 | 阻塞条件 |
|:---:|------|------|
| **P0** | 页面加载、导航、关键 CRUD | 任一失败 = 构建阻塞 |
| **P1** | 主要业务流、状态转换、计算验证 | 100% 通过（SIT） |
| **P2** | 边界值、输入校验、错误处理、权限 | ≥90% 通过 |
| **P3** | 跨模块集成、数据一致性 | 有跨模块依赖时必做 |

## 2.2 核心策略

- **状态机驱动**: 合法转换→P1，非法转换→P2
- **公式边界**: ≥30% 总用例数为边界测试 (V-前缀)，每功能点≥5个
- **数据变化维度**: 对每个需求问"什么数据条件会改变结果？"→映射到 test_data_inventory.md 中的变化维度
- **数据驱动格式**: 同一逻辑+多数据行→参数化表格

输出 `test_coverage_matrix.md`（需求×测试追溯 + 数据变化覆盖）。

## 2.3 统一测试用例文档

按 `references/测试用例模版.md` 的 8 章标准生成 **一个** `test_cases.md`，涵盖功能+API：

| 前缀 | 含义 | 前缀 | 含义 |
|------|------|------|------|
| F- | 核心流程 | V- | 校验/边界 |
| C-/U-/X- | 创建/更新/删除 | L-/D- | 列表/详情 |
| **A-** | **API 接口测试** | P-/N-/T- | 权限/非功能/待澄清 |

**含 API 规格时**: 在文档中嵌入 YAML block（`kind: api_pytest`），可被 `generate_pytest.py` 直接提取执行。

## 2.4 外部测试数据

生成 `test_data.json`（自动化用，结构化）和 `test_data.csv`（业务评审用，扁平格式）。

---

# 3. Playwright 自动化脚本和执行

## 3.1 项目结构

```
erp_tests/
├── conftest.py              # Fixtures: browser, login, data loading
├── test_smoke.py            # P0 tests
├── test_functional.py       # P1 parametrized tests
├── test_boundary.py         # P2 boundary tests
├── test_integration.py      # P3 integration tests
├── test_api.py              # API tests (when API specs exist)
├── test_quarantine.py       # Quarantined flaky tests
├── pages/base_page.py       # Page Object Model
├── utils/
│   ├── test_data_loader.py  # CSV/JSON loading
│   └── test_data.py         # Static constants
├── test_data/               # External JSON/CSV datasets
└── README.md
```

## 3.2 技术要求

- `pytest` + `playwright` (sync_api) + `@pytest.mark.parametrize` + 外部数据文件
- `conftest.py`: browser/auth/data-loading fixtures + JSON data loader
- `pytest.ini`: `--reruns 2 --reruns-delay 5` + p0/p1/p2/p3/flaky/quarantine markers
- `run_tests.sh` + `run_tests.ps1`: smoke/functional/full/integration/complete 五种模式

## 3.3 Flaky Test 策略（必做）

1. `pytest.ini` 含 `--reruns 2 --reruns-delay 5`
2. `erp_tests/test_quarantine.py` 含 `@pytest.mark.skip` 隔离模板
3. `README.md` 含 `## Flaky Test Strategy` 章节

## 3.4 执行环境顺序

```
SIT (测试环境) → 客户验证 (UAT优先 → 模拟生产 bak.*) → 上线
```

| 阶段 | 环境 | 用例范围 | 通过标准 |
|:---:|------|------|------|
| 1 | SIT | P0+P1 全量 | 100% P0, ≥95% P1 |
| 2 | 客户验证 | P0+P1+P2（含差异用例） | 100% P0+P1, ≥90% P2 |
| 3 | 上线 | P0~P3 全量 | 100% P0+P1, ≥85% P2+P3 |

客户差异从 `references/customer_variants.md` 读取，公共模块在 SIT 覆盖。

详见 `references/steps/Step4_测试执行.md`

---

# 4. 测试报告

## 4.1 报告产出

| 文件 | 内容 |
|------|------|
| `test_report.md` | 可读摘要（概要+按优先级结果+失败分析+趋势分析） |
| `test_report.html` | 交互式浏览器报告（含图表） |
| `traceability_report.md` | 需求→结果审计映射 |
| `pytest_results.json` | 结构化执行结果 |
| `defects/` | 缺陷工单（含复现步骤+预期vs实际+截图） |

## 4.2 趋势分析（必做）

即使首次执行也要包含 Trend Analysis 章节（无历史数据时标注"首次执行"）。
有历史数据时计算真实增量，附解读（Improving/Watch/Action）。

---

## Quick Output Modes

Skill 自动检测文档类型并调整产出密度：

| 模式 | 触发词 | 用例编号 | 脚本 | 目标文件数 |
|------|--------|:---:|:---:|:---:|
| **Full** | "完整测试方案","全套" | F/C/V/L/D/A/P/N | 全量 erp_tests/ | ≤22 |
| **Smoke** | "冒烟测试","P0 only" | P0 only | test_smoke.py | ≤8 |
| **API** | "API测试","接口测试" | A-xx + schema | test_api.py | ≤12 |
| **Cases** | "只要测试用例" | 全部 | 跳过 | ≤8 |
| **Report** | "测试报告" | — | — | ≤4 |
| **Module** | "只看XX模块" | 限定范围 | 限定范围 | 按比例 |

**文件数控制**: Light 模式≤12文件，跳过 test_report.html / test_quarantine.py / test_data.json（CSV足够时）。

---

## Output Summary

| 阶段 | 核心产出 |
|:---:|------|
| 1. 需求分析 | `requirements_spec.md` + `requirements_audit.md` + `test_data_inventory.md` |
| 2. 测试用例 | `test_cases.md` + `test_coverage_matrix.md` + `test_data.csv/json` |
| 3. 自动化 | `erp_tests/` + `pytest.ini` + `run_tests.sh/ps1` + `pytest_results.json` |
| 4. 报告 | `test_report.md` + `traceability_report.md` + `defects/` |

## Key Principles

- **提取，不要凭空编造**测试数据 — 从捕获页面拉取真实实体名
- **每个状态转换 = 一个测试用例** — 合法→P1，非法→P2
- **每个公式阈值 = 一个边界测试** — 精确阈值、阈值±1、零值、极值
- **每条错误消息 = 一个预期结果** — 使用领域知识中的精确中文消息
- **数据变化是 ERP 测试质量的关键** — 覆盖所有数据维度
- **P3 不可跳过** — 有跨模块依赖时必须做
- **注意设备特定行为** — PC/PAD/PDA/工业平板
- 如果找不到 `module_texts.txt`，请用户提供位置

## Test Data Lifecycle (setup → test → cleanup)

所有自动化测试遵循统一的 **运行前检查 → 执行 → 运行后清理** 三步流水线，确保测试数据唯一性和环境清洁。**此规范适用于所有 IMS 系统模块**（销售、采购、生产、仓库、质检、吊挂、物流、报表、数据等），不限于特定模块。

### 三步流水线

```
┌─ setup (运行前检查与准备) ─────────────────────────────────────┐
│  1. 清理旧数据: 按业务唯一键删除目标模块已有测试数据           │
│  2. 生成测试数据: 新建数据 (非模板复制)，无残留行              │
│  3. 导入/创建: 通过 UI 或 API 将测试数据写入系统               │
│  4. 前置计算/审批: 触发模块所需的预处理流程（如计算、审核等）  │
└──────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─ pytest erp_tests/ ──────────────────────────────────────────┐
│  5. test_dataset fixture: 提取数据 → 分类 → 缓存             │
│  6. 全量测试执行 (P0~P3)                                     │
└──────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─ pytest_sessionfinish hook ───────────────────────────────────┐
│  7. 自动清理: 删除本次导入/创建的所有测试数据                  │
└──────────────────────────────────────────────────────────────┘
```

### 关键原则

| 原则 | 实现 |
|------|------|
| **业务唯一性** | 导入前按模块业务唯一键删除已有记录 |
| **数据干净** | 程序化新建数据 (如 `openpyxl.Workbook()`)，不复制模板 |
| **自然交互** | 按钮启用后才点击，不 force-click；等待异步任务完成 |
| **会话一致** | 数据准备和提取在同一 Playwright 会话 |
| **测试后清理** | `pytest_sessionfinish` hook 自动执行清理 |

### 实现文件

| 文件 | 职责 |
|------|------|
| `setup_test_data.py` | Pre-test: 清理→生成→导入→前置流程触发 |
| `conftest.py::pytest_sessionfinish` | Post-test: 自动清理本次测试数据 |
| `erp_tests/utils/test_data_extractor.py` | 数据提取+分类+缓存 |
| `erp_tests/utils/test_data_generator.py` | 测试数据生成+前置计算 |

### conftest 钩子模板

```python
# conftest.py
def pytest_sessionfinish(session, exitstatus):
    """测试完成后自动清理本次测试数据"""
    from setup_test_data import cleanup_test_data
    cleanup_test_data()
```

| 陷阱 | 表现 | 解决 |
|------|------|------|
| Ant Design 表格 td 比 th 多一列 | 数据提取永远返回 0 | `cells = cells[len(cells)-len(headers):]` |
| 按钮选择器 `.ant-btn-primary` 误匹配 | 点击了弹窗按钮而非查询按钮 | 遍历 `button:visible` + 文本匹配 |
| DatePicker 是 readonly input | `fill()` 超时 | `fill(value, force=True)` |
| Excel 导入字段列映射错位 | 预览报错/按钮 disabled | 确认字段列顺序与系统导入模板一致 |
| 异步任务进度不在预期容器 | 轮询永远找不到完成标记 | 搜索 `body` 全文 |
