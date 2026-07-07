# ERP Knowledge Gap Analysis & Supplement Guide

This document maps knowledge coverage across 14 IMS modules and provides a practical
supplement strategy for each gap. Since no complete PRD exists, supplements rely on
existing materials, structured observation, and targeted SME interviews.

---

## 1. Coverage Heatmap

| # | Module | module_texts | 知识库文档 | Domain Knowledge | Overall | Priority |
|---|--------|-------------|-----------|-----------------|---------|----------|
| 1 | 样衣 | ❌ 缺 | ❌ 缺 | ❌ 缺 | 🔴 0% | P0 |
| 2 | 销售 | ✅ | ⚠️ 间接 | ⚠️ 中 | 🟡 70% | P1 |
| 3 | 采购 | ✅ | ⚠️ 间接 | ⚠️ 中 | 🟡 75% | P1 |
| 4 | 仓库/WMS | ✅ | ✅ 6份 | ✅ 详 | 🟢 95% | P2 |
| 5 | 生产/MES | ✅ | ⚠️ 间接 | ⚠️ 中 | 🟡 75% | P1 |
| 6 | 质检/QC | ✅ | ⚠️ 间接 | ⚠️ 中 | 🟡 65% | P1 |
| 7 | 物流 | ❌ 空壳 | ❌ 缺 | ❌ 浅 | 🔴 5% | P0 |
| 8 | 报表 | ✅ | ❌ 缺 | ❌ 缺 | 🟠 45% | P1 |
| 9 | 数据/主数据 | ✅ | ❌ 缺 | ❌ 浅 | 🟠 55% | P1 |
| 10 | 吊挂 | ✅ | ✅ 4份 | ⚠️ 中 | 🟢 90% | P2 |
| 11 | 平板/PAD | ❌ 缺 | ❌ 缺 | ❌ 浅 | 🔴 15% | P2 |
| 12 | 人事 | ❌ 缺 | ❌ 缺 | ❌ 缺 | 🔴 0% | P2 |
| 13 | 看板 | ❌ 缺 | ❌ 缺 | ❌ 缺 | 🔴 0% | P2 |
| 14 | 系统/Admin | ❌ 缺 | ❌ 缺 | ❌ 浅 | 🔴 10% | P2 |

---

## 2. Missing Knowledge Dimensions (Across All Modules)

Even for well-covered modules like WMS, these dimensions are absent:

| 维度 | 当前状态 | 为什么重要 |
|------|---------|-----------|
| **PRD/需求背景** | 全模块缺失 | 知道"为什么这样设计"才能设计正确的测试场景 |
| **后端业务逻辑** | 仅从UI推断 | UI校验只是冰山一角，后端逻辑才是核心 |
| **版本差异矩阵** | 仅荆门/柬埔寨/标准 3 个点 | 400+工厂客户，版本差异是回归测试的核心 |
| **API接口契约** | 全模块缺失 | 自动化测试和集成测试的基础 |
| **权限模型** | 仅角色名称列表 | 不知道谁能做什么，安全测试无法覆盖 |
| **性能SLA** | 仅功能说明书中的全局指标 | 各模块差异化的性能要求是负载测试依据 |
| **数据约束规则** | 散落在各文档 | 缺少集中的数据字典：字段类型、长度、枚举值、默认值 |
| **异常处理策略** | 仅部分错误消息 | 超时、并发、降级、回滚策略不明确 |

---

## 3. 补充策略（按信息来源分类）

### 策略 A：从现有资料交叉提取（立即可做）

已有机遇：12份知识库文档 + module_texts.txt 中包含了很多未被 system 化提取的信息。

| 可补充项 | 方法 | 来源 |
|---------|------|------|
| **页面字段字典** | 逐模块解析 module_texts.txt，提取每个页面的字段名、按钮名、下拉选项 | module_texts.txt |
| **菜单完整树** | 从 module_texts.txt 每个模块节中提取完整的三级菜单结构 | module_texts.txt |
| **隐含业务规则** | 从操作手册的"注意事项"、"约束条件"段落中提取规则 | 操作手册 .docx |
| **隐含状态机** | 从操作手册的操作步骤中推断实体生命周期 | 操作手册 .docx |
| **错误消息汇总** | 搜索所有文档中的"提示"、"错误"、"不允许"关键词 | 全部文档 |

### 策略 B：从 module_texts.txt 深度挖掘

module_texts.txt 是页面捕捉数据，包含大量未提取的信息：

```markdown
提取清单：
□ 每个页面的所有可交互元素（按钮、输入框、下拉框、表格列）
□ 页面间的导航关系（从哪个页面可以跳转到哪个页面）
□ 列表页的筛选条件字段和筛选项
□ 表单的必填字段（标*的）vs 可选字段
□ 表格的操作按钮（编辑/删除/查看/审批等）
□ 页面上的状态标签和徽章（如"已审核"、"待处理"）
□ 数字格式（金额、数量、百分比、日期的显示格式）
□ 面包屑导航路径
```

### 策略 C：结构化 SME 访谈模板

当无文档可查时，用以下模板访谈业务专家：

```markdown
## [模块名] 业务逻辑访谈模板

### 实体与生命周期
- 这个模块管理哪些核心业务实体？（如：销售订单、采购计划）
- 每个实体有哪些状态？状态之间怎样流转？（画状态机）
- 什么事件/操作触发状态变化？
- 哪些状态变化是不可逆的？

### 业务规则
- 哪些操作需要审批？审批层级是怎样的？
- 有哪些金额/数量/时间的阈值规则？
- 有哪些数据关联约束？（A存在才能创建B）
- 有哪些重复/冲突检查规则？

### 版本差异
- 这个功能在哪些客户版本中不同？
- 差异点具体是什么？（字段不同？流程不同？）
- 客户定制化程度如何？哪些是可配置的？

### 异常处理
- 操作失败时用户看到什么？
- 有没有超时/重试机制？
- 并发操作如何处理？（两人同时编辑同一订单）

### 集成点
- 这个模块和哪些外部系统交互？
- 数据是实时同步还是批量同步？
- 同步失败时的降级策略是什么？
```

### 策略 D：操作捕捉指南

如果没有文档，通过实际操作捕捉页面数据来补充：

```markdown
## 页面数据捕捉清单

对每个功能页面，记录：
□ 完整URL路径
□ 页面标题和面包屑
□ 所有表单字段（名称、类型、是否必填、默认值、placeholder）
□ 所有按钮（名称、位置、触发后的行为）
□ 表格列定义（列名、排序、筛选）
□ 下拉框选项（完整枚举值）
□ 所有可见的状态值和对应颜色/图标
□ 正常操作流程（完整录屏）
□ 异常操作流程（输入非法值后的反应）
□ 每个操作的响应时间（粗略计时）

工具：浏览器DevTools + 录屏 + module_texts.txt 追加
```

### 策略 E：从 module_texts.txt 推断业务规则

即使没文档，页面结构也能推断规则：

| 页面特征 | 可推断的规则 |
|---------|------------|
| 审批按钮存在 | 需要审批流程 |
| 状态字段有颜色变化 | 状态机存在，每种颜色对应一个状态 |
| 字段旁边有"*" | 该字段必填 |
| 表格操作列有多按钮 | 同一实体有多种操作 |
| 筛选条件有日期范围 | 数据按日期组织，可能需要性能分页 |
| 详情页有"操作日志"标签 | 操作需要审计追踪 |
| 按钮灰显/隐藏 | 存在基于状态/权限的操作限制 |
| 弹出确认对话框 | 操作需要二次确认 |

---

## 4. 按模块的补充优先级和具体行动

### P0 — 盲区模块（立即可做的低成本补充）

| 模块 | 已知信息 | 立即可补充 | 需要访谈/捕捉 |
|------|---------|-----------|-------------|
| **物流** | module_texts 仅"半成品收货通知单" | 从功能说明书 §2.6 提取供应链协同流程 | 物流与仓库/财务的交接点、运单管理、发货状态机 |
| **样衣** | 模块在侧边栏存在，但无任何文档 | 从功能说明书推断样衣到生产的转换 | 完整的样衣管理流程、样衣BOM、样衣审批 |

### P1 — 部分覆盖模块（从现有资料深度提取）

| 模块 | 主要缺口 | 补充方法 |
|------|---------|---------|
| **销售** | 定价规则、折扣、多币种、与财务对接 | 策略E(从module_texts推断) + 策略C(访谈) |
| **采购** | 供应商评估、采购审批层级、采购变更 | 策略A(从操作手册提取) + 策略B(module_texts挖掘) |
| **生产** | 排程算法、产能计算、物料齐套检查 | 策略A + 策略C |
| **质检** | 缺陷分类体系、供应商质量反馈、质检配置 | 策略A + 策略C |
| **报表** | 报表聚合逻辑、权限范围、导出限制 | 策略B(从module_texts报表页提取) |
| **数据/主数据** | 数据校验规则、导入导出规则、数据依赖 | 策略B + 策略E |

### P2 — 已较好覆盖（持续完善）

| 模块 | 当前状态 | 可增强方向 |
|------|---------|-----------|
| **仓库/WMS** | 95%覆盖 | 补充硬件交互细节(AGV/立库)、多仓库调度策略 |
| **吊挂** | 90%覆盖 | 补充不同产线类型的配置差异、硬件故障恢复 |
| **平板/PAD** | 15%覆盖 | 补充离线模式、同步策略、PAD特定UI规则 |
| **人事** | 0%覆盖 | 如需要：访谈 + 页面捕捉 |
| **看板** | 0%覆盖 | 如需要：确定KPI指标 + 权限范围 |
| **系统/Admin** | 10%覆盖 | 如需要：权限矩阵 + 系统配置参数清单 |

---

## 5. 版本差异矩阵（当前已知 vs 需补充）

| 维度 | 当前已知 | 需补充 |
|------|---------|--------|
| **QC审批粒度** | 标准:全单; 荆门:物料+颜色级 | 柬埔寨、际华、泰富等客户差异 |
| **辅料收货模式** | 荆门:先录后贴; 新基:无箱贴 | 其他客户使用哪种？先贴后录谁用？ |
| **LOT色** | 仅荆门有此功能 | 其他客户是否需要？为什么？ |
| **缝制质检** | 荆门:完整三类型; 柬埔寨:吊挂QC | 标准版？其他客户？ |
| **成品质检** | 仅荆门有完整流程 | 其他版本的成品检验如何做？ |
| **质检扣分类型** | 荆门:100码+百平方码 | 其他客户用哪种？ |
| **WMS策略** | 飞雁工厂:开箱任务 | 其他工厂的开箱流程？ |
| **吊挂系统** | 详细覆盖但仅柬埔寨手册 | 其他工厂的吊挂配置差异？ |
| **系统配置参数** | 仅 `st_auto_create_after_mpo_submit_enable` | 完整的系统配置项清单？ |

---

## 6. 建议的补充节奏

```
Week 1-2: 策略A+B — 从现有资料深度提取（零成本，立即可做）
  ├── 为每个模块生成页面字段字典
  ├── 提取所有错误消息和提示文本
  └── 重建完整菜单树

Week 3-4: 策略E — 从 module_texts 推断业务规则
  ├── 识别所有状态机（从状态标签颜色推断）
  ├── 识别所有必填字段和约束
  └── 生成初步的数据字典

Week 5-8: 策略C — 结构化 SME 访谈（需要业务方配合）
  ├── 按 P0→P1→P2 顺序访谈
  ├── 重点：业务逻辑、异常处理、版本差异
  └── 每次访谈后更新 erp_domain_knowledge.md

Ongoing: 策略D — 操作捕捉（需要系统访问权限）
  ├── 对盲区模块（物流、样衣）做完整页面捕捉
  ├── 追加到 module_texts.txt
  └── 更新 skill 中的模块清单
```


---

# 附录A: 知识库完整度评估



## Executive Summary

The IMS ERP testing skill knowledge base covers **14 modules** with highly uneven depth. Five modules (仓库, 生产, 吊挂, 采购, 数据) achieve 75%+ completeness thanks to official documentation, feature XMind extractions, and live system captures. Five modules (样衣, 看板, 平板, 物流, 系统) remain at 25% or below -- three of which have essentially zero coverage (样衣, 看板, 平板). The biggest systemic gap is the **complete absence of field-level page data** for modules 01-04 and 10-14 in the page field dictionary, meaning Playwright script generation cannot reliably locate DOM elements for these modules.

**Aggregate KB completeness: 51%** (weighted average across all 14 modules and 8 dimensions).

---

## Assessment Matrix

| # | Module | Menu Structure | State Machines | Business Rules | Error Messages | Field/Page Details | Feature Points | Cross-Module Flows | Overall Rating |
|---|--------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 样衣 (Sample) | NONE | NONE | NONE | 0 | NONE | NONE | NONE | **5%** |
| 2 | 销售 (Sales) | LIVE | YES | PARTIAL | 0 | PARTIAL | NONE | YES | **55%** |
| 3 | 采购 (Purchasing) | LIVE | YES | YES | 10 | PARTIAL | YES | YES | **80%** |
| 4 | 仓库 (Warehouse) | LIVE | YES | YES | 22 | PARTIAL | PARTIAL | YES | **85%** |
| 5 | 生产 (Production) | STATIC | YES | YES | 15 | PARTIAL | YES | YES | **82%** |
| 6 | 质检 (Quality) | LIVE | YES | YES | 2 | YES | NONE | YES | **75%** |
| 7 | 物流 (Logistics) | LIVE | PARTIAL | PARTIAL | 0 | YES | NONE | YES | **35%** |
| 8 | 报表 (Reports) | LIVE | NONE* | PARTIAL | 0 | YES | YES | YES | **70%** |
| 9 | 数据 (Master Data) | LIVE | PARTIAL | YES | 15 | YES | YES | YES | **78%** |
| 10 | 吊挂 (Hanging) | STATIC | YES | YES | 10 | YES | PARTIAL | YES | **78%** |
| 11 | 平板 (Tablet) | LIVE | NONE | NONE | 5 | NONE | NONE | NONE | **10%** |
| 12 | 人事 (HR) | LIVE | NONE | PARTIAL | 0 | NONE | NONE | NONE | **25%** |
| 13 | 看板 (Dashboard) | NONE | NONE | NONE | 0 | NONE | NONE | NONE | **2%** |
| 14 | 系统 (System) | LIVE | NONE* | PARTIAL | 1 | NONE | NONE | NONE | **20%** |

> *NONE* = Not applicable (read-only reports have no state machines; system admin config has no business state flow).
> `*` for 报表 and 系统 indicates "NONE/NOT APPLICABLE" -- these modules don't have traditional business state machines.

---

## Module-by-Module Detailed Assessment

### 01 -- 样衣 (Sample) -- 5%

**Strengths:** Module exists in the sidebar (`gm.样衣#1`). Seven dedicated reports in the 报表 module (办单全流程跟踪表, 采购物料跟踪表, etc.) indicate a significant business area.

**Gaps (critical):** Zero menu structure. Zero state machine data. Zero business rules. Zero field/page data. No module_texts.txt section. No official documentation. No live system capture. No feature-point documents.

**Impact:** Cannot generate Playwright scripts for any sample garment page. Cannot write P0 test cases. The 7 report names hint at a workflow involving 办单 (sample orders), 采购物料 (procurement tracking), but no details exist.

**Data sources examined:** Sidebar entry in module_texts.txt (all 9 captured sections show `gm.样衣#1`). Report names in 报表 module.

---

### 02 -- 销售 (Sales) -- 55%

**Strengths:**
- Menu: 3 items captured live (销售订单, 订单预排期, 订单排期表)
- State machine: Fully documented (草稿→生效→中止→反中止, 变更, 拆分)
- Cross-module: Sales Order → Material Requirements + Production Order chain defined
- Role: `gm.销售#1` (Tier 1, primary operator)

**Gaps (critical):**
- Zero error messages catalogued
- Zero field-level page data (all fields/buttons/filters marked [GAP] in page_field_dictionary.md)
- No feature-point document (no XMind extraction for sales)
- Missing business rules: pricing, discounts, multi-currency, sales returns/refunds, change/cancel operations
- No live page capture with field details for any of the 3 pages

**Impact:** Can design state-machine test scenarios but cannot write Playwright selectors. The sales module drives all downstream workflows (purchasing + production), making this gap particularly damaging to end-to-end test coverage.

---

### 03 -- 采购 (Purchasing) -- 80%

**Strengths:**
- Menu: 17 items captured live with full hierarchy
- State machines: Material Requirements (草稿→审核中→审核通过) and Purchase Order (草稿→生效→确认到货) fully documented
- Business rules: Demand-driven workflow, fabric/accessory split, cash PO exception, extra receipt types for fabric all documented
- Feature points: feature_procurement_picking.md covers fabric picking, accessory picking, PDA cut-parts outsource, external purchase
- Cross-module: Production→Material Demand→Purchase Plan→Purchase Order→Receipt flows documented
- One live captured page: 备货辅料需求通知单 with fields, columns, buttons, statuses
- Role: `gm.采购#2` (Tier 2, elevated)

**Gaps:**
- ~10 error messages catalogued but most are from the picking subdomain, not core purchasing
- Field/page details: PARTIAL -- only 1 of 17 pages has live field data; 5 have domain knowledge labels but no actual fields
- Missing: supplier evaluation criteria, purchase approval hierarchy/workflow, purchase order change management
- No dedicated feature document for core purchase order lifecycle (picking document covers the picking subdomain)

---

### 04 -- 仓库 (Warehouse) -- 85%

**Strengths:**
- Menu: 43 items captured live (largest menu of any module) with full hierarchy in 12 categories
- State machines: 6 distinct state machines documented (WMS Material, Carrier, 备料, 裁片配套, 开箱任务, 叫箱需求单)
- Business rules: Comprehensive -- 6 segregated inventory types, formulas (可用库存, 开箱), box type allocation thresholds, locking rules
- Error messages: 22 messages catalogued (most of any module) -- covering material receipt, carrier binding, unboxing, preparation
- Cross-module: Full Purchasing→WMS receipt→Inventory and WMS→Production picking flows
- Base knowledge: 6 official WMS documents sourced
- Role: `gm.仓库#1` (Tier 1)

**Gaps:**
- Field/page details: PARTIAL -- domain knowledge exists for 9 pages but zero actual field-level data in page_field_dictionary.md
- Feature points: PARTIAL -- no dedicated warehouse feature XMind extraction; picking doc overlaps but doesn't cover core WMS
- Missing: AGV/立体仓库 hardware interaction details, multi-warehouse dispatch strategy, inventory reconciliation processes

---

### 05 -- 生产 (Production) -- 82%

**Strengths:**
- Menu: 29 pages (STATIC from module_texts hierarchy, no live capture) across 6 categories
- State machines: Production Order (7 states, hard rollback) and Sewing Task (5 states with 换款/暂停/恢复) fully documented
- Business rules: Physical garment sequence (松布→裁剪→缝制→尾整), two-level scheduling, review gate, washing separate, picking by material type
- Error messages: ~15 messages from feature_production_offline.md covering production order validation, color/size, import, marker management, offline task assignment, proxy reporting, workstation config
- Feature points: feature_production_offline.md is the most comprehensive feature document (covers production orders, offline module, proxy reporting, workstation configuration, ~357 lines of detailed test scenarios)
- Cross-module: Sales BOM→Production Order→Material calculation→Picking→WMS chain; production→款号 generation; offline task→sewing task→reports sync
- ~13 system configuration keys documented
- Role: `gm.生产#3` (highest Tier 3, elevated permissions)

**Gaps:**
- Menu: STATIC only -- no live system capture for production module pages
- Field/page details: PARTIAL -- domain knowledge labels exist for 6 pages but actual field/button data is from feature doc extraction, not live capture
- Missing: 排程算法 (scheduling algorithm), 产能计算 (capacity calculation), 物料齐套检查 (material kitting check) logic
- No live captured page with field/column/button details for production pages

---

### 06 -- 质检 (Quality) -- 75%

**Strengths:**
- Menu: 5 items captured live
- State machine: 待检验→检验中→已完成 documented
- Business rules: 4 inspection types with scope mapping, global QC configuration, scoring formulas (100码 and 百平方码), pass/fail thresholds
- Field/page details: YES -- page_field_dictionary.md has detailed field names, types, required indicators, buttons, filter fields, status labels, tabs, and sub-tables for all 6 QC pages (the most complete field documentation of any module)
- Cross-module: Receipt→QC→Warehouse stock quality status documented
- Version differences: Standard/Jingmen/Cambodia differences for QC documented
- Role: `gm.质检#1`

**Gaps:**
- Only 2 error messages catalogued (formula-based pass/fail criteria)
- No feature-point document (no XMind extraction for QC)
- Missing: defect classification system details, supplier quality feedback loop, AQL sampling configuration values
- State machine lacks detail on 让步使用 (concession) flow

---

### 07 -- 物流 (Logistics) -- 35%

**Strengths:**
- Menu: 1 item captured live (半成品收货通知单)
- Cross-module: Production outsourcing→Logistics receipt→Warehouse inbound documented
- Field/page details: YES -- surprisingly detailed field definitions for 半成品收货通知单 in page_field_dictionary.md (list columns, form fields, filter fields, buttons, status labels)
- State machine: PARTIAL (待收货→部分收货→已收货 inferred)
- Role: `gm.物流#1`

**Gaps:**
- Only 1 page in the entire module ("empty shell" per knowledge_gap_analysis.md)
- Zero error messages catalogued
- Zero business rules beyond the single receipt flow
- No feature-point document
- Missing: shipping management, transportation tracking, delivery confirmation, carrier integration
- Real logistics likely happens in 成品仓库 sub-module of Warehouse, not this module

---

### 08 -- 报表 (Reports) -- 70%

**Strengths:**
- Menu: 81 items captured live (largest page count), organized in 14 categories
- Field/page details: YES -- page_field_dictionary.md has detailed report structures, common filter patterns, common button patterns, and per-category column definitions for 50+ reports
- Feature points: YES -- feature_style_reports.md covers currency formatting (千位符), department/workshop/group cascade filtering, cutting daily output report field update logic, export column customization across 12 reports
- 3 live captured report pages (物料采购明细表, 物料收货明细表, 裁剪日产量报表) with full field/column/button data
- Cross-module: Reads from ALL modules (cross-cutting)
- Role: `gm.报表#1`

**Gaps:**
- State machines: NONE/NOT APPLICABLE (reports are read-only)
- Zero error messages catalogued
- Business rules: PARTIAL -- export formatting and filter cascading documented, but report aggregation logic, permission scoping for report data, and export size limits are missing
- 50+ reports have column inference but no live capture for most

---

### 09 -- 数据 (Master Data) -- 78%

**Strengths:**
- Menu: 17 items captured live in 2 categories (档案 + 技术)
- Business rules: YES -- archives vs technical split, 款号→模板→工艺要求 hierarchy, style-mode config (1 vs 2), uniqueness rules, color/size merge logic, tab-level permission control
- Error messages: ~15 from feature_style_reports.md covering style creation, import validation, copy operations, process import, material validation
- Field/page details: YES -- page_field_dictionary.md has detailed field names, types, required indicators, buttons, validation rules for all 18 master data pages
- Feature points: YES -- feature_style_reports.md covers style management comprehensively (~393 lines)
- Cross-module: Foundational -- all transactional modules consume master data
- Role: `gm.数据#1`

**Gaps:**
- State machines: PARTIAL -- 款号 has 草稿→生效 but supplier, customer, brand, process, and other entities lack state machine documentation
- Missing: data import/export rules (file format, size limits), data dependency constraints across master data entities
- Feature doc covers style management but not the other 17 master data pages

---

### 10 -- 吊挂 (Hanging) -- 78%

**Strengths:**
- Menu: 4 items (STATIC from module_texts, no live capture) in 2 categories
- State machines: YES -- sewing task state machine (产前准备→待缝制→缝制中→已完成) with 换款→暂停→恢复 cycle
- Business rules: Production station required, 过站不回流, rework reason mandatory, QC rework rate on rework station
- Error messages: ~10 from error catalog and domain knowledge (station validation, rework, 衣架更换, 站位管理)
- Field/page details: YES -- page_field_dictionary.md has detailed field names, types, sub-tables for all 4 hanging config pages (流水线配置, 扫码终端配置, 分拣MES配置, 分拣下位配置)
- Cross-module: Production→Hanging line execution→Reports fully documented
- Base knowledge: 2 official hanging system documents sourced
- Role: `gm.吊挂#1`

**Gaps:**
- Menu: STATIC only -- no live capture
- Feature points: PARTIAL -- no dedicated hanging feature XMind; feature_production_offline.md covers related production tasks but not hanging-specific features
- Missing: Different line type configuration differences, hardware fault recovery procedures, hanging system PLC integration

---

### 11 -- 平板 (Tablet) -- 10%

**Strengths:**
- Menu: 1 item captured live (缝制管理（PAD）)
- ~5 error messages from error catalog (PAD-related: 挂片超挂, 色码切换, 站位管理, 衣架更换, 工序编排)
- Role: `gm.平板#1`

**Gaps:**
- Only 1 page visible in menu -- the tablet module likely has many more screens not exposed via PC menu
- Zero state machine data specific to tablet UI
- Zero business rules specific to tablet
- Zero field/page data (no tablet screens captured)
- No feature-point document
- No cross-module flow documentation
- Missing: offline mode behavior, sync strategy, tablet-specific UI rules, device hardware requirements
- per knowledge_gap_analysis.md: coverage = 15%

---

### 12 -- 人事 (HR) -- 25%

**Strengths:**
- Menu: 19 items captured live (员工档案 through 工资项设置)
- Business rules: PARTIAL -- employee ID conventions (6-digit numeric, 100xxx=Chinese, 101xxx+=Khmer), visa/passport expiry global alerts
- Cross-module: Global notifications (visa/passport expiry) appear in all modules
- Role: `gm.人事#1`

**Gaps:**
- Zero state machine data
- Zero error messages catalogued
- Zero field/page data for any of the 19 HR pages
- No feature-point document
- Missing: attendance calculation logic, payroll calculation, piece-rate wage computation, leave balance rules, shift scheduling constraints
- per knowledge_gap_analysis.md: coverage = 0%

---

### 13 -- 看板 (Dashboard) -- 2%

**Strengths:**
- Module exists in sidebar (`gm.看板#1`)
- No other data available in any source

**Gaps (critical):**
- Zero menu structure
- Zero state machine data (not applicable -- dashboards are read-only)
- Zero business rules
- Zero error messages
- Zero field/page data
- No feature-point document
- No live system capture
- No module_texts.txt section
- No official documentation
- per knowledge_gap_analysis.md: coverage = 0%

---

### 14 -- 系统 (System) -- 20%

**Strengths:**
- Menu: 18 items captured live (部门管理 through 操作日志)
- Business rules: PARTIAL -- role-based access control tier model (#1/#2/#3) documented; role isolation and global visibility inferred
- 1 error message (新增用户确认 dialog)
- Role: `gm.系统#1`

**Gaps:**
- State machines: NONE/NOT APPLICABLE (system admin config)
- Zero field/page data for any of the 18 system pages
- No feature-point document
- No cross-module flow documentation (system is infrastructure, not business flow)
- Missing: full permission matrix (who can do what per role per module), system configuration parameter catalog (only ~13 keys documented across all feature docs), audit log format, data dictionary completeness, import/export template definitions
- per knowledge_gap_analysis.md: coverage = 10%

---

## Completeness Ranking (Descending)

| Rank | Module | Rating | Tier |
|------|--------|:------:|------|
| 1 | 仓库 (Warehouse) | 85% | GREEN |
| 2 | 生产 (Production) | 82% | GREEN |
| 3 | 采购 (Purchasing) | 80% | GREEN |
| 4 | 数据 (Master Data) | 78% | GREEN |
| 5 | 吊挂 (Hanging) | 78% | GREEN |
| 6 | 质检 (Quality) | 75% | YELLOW |
| 7 | 报表 (Reports) | 70% | YELLOW |
| 8 | 销售 (Sales) | 55% | YELLOW |
| 9 | 物流 (Logistics) | 35% | RED |
| 10 | 人事 (HR) | 25% | RED |
| 11 | 系统 (System) | 20% | RED |
| 12 | 平板 (Tablet) | 10% | RED |
| 13 | 样衣 (Sample) | 5% | RED |
| 14 | 看板 (Dashboard) | 2% | RED |

**Rating scale:** GREEN >= 75% | YELLOW 50-74% | RED < 50%

---

## Top 5 Highest-Impact Gaps

### Gap 1: Sales module has zero field-level page data (IMPACT: CRITICAL)

The sales module is the **origin of all downstream workflows**. Every manufacturing order, purchase plan, and material requirement traces back to a sales order. Despite having a documented state machine and cross-module flows, the KB has:

- Zero error messages catalogued
- Zero field names, button names, or filter fields for any of the 3 sales pages
- No live page capture with DOM-relevant selectors
- No feature-point document for sales order management

**Consequence:** Playwright scripts cannot be generated for sales order creation, scheduling, splitting, or status transitions. E2E test chains that start with "create a sales order" are blocked at the first step.

**Recommended action:** Live-capture the 销售订单 page (list + detail + edit views) using Strategy D. This is the single highest-ROI data collection task.

---

### Gap 2: Field/page data systematically absent for production pages (IMPACT: CRITICAL)

While production has excellent domain documentation (state machines, business rules, feature-point extraction, error messages), **zero production pages have live-captured field data**. All production field entries in page_field_dictionary.md are marked [GAP]. The 29-page production menu is entirely STATIC (from module_texts.txt hierarchy, not live capture).

**Consequence:** Playwright selectors cannot target production order forms, sewing task cards, offline task assignments, or any of the 29 production pages. This blocks the most test-heavy module in the system.

**Recommended action:** Live-capture the 生产订单 page (creation + edit + tab navigation). This is the central production entity linking sales, material requirements, picking, and WMS.

---

### Gap 3: 样衣 (Sample) module is a complete blind spot (IMPACT: HIGH)

The sample garment module has zero coverage across all 8 dimensions. Seven dedicated reports exist in the 报表 module, confirming this is a significant business area. The entire sample-to-production conversion workflow is undocumented.

**Consequence:** Cannot test sample order management, sample BOM, sample approval, or the sample-to-production handoff. This gap affects pre-production quality assurance workflows.

**Recommended action:** SME interview (Strategy C) to document the sample order lifecycle, followed by live page capture (Strategy D).

---

### Gap 4: No live system capture for production, hanging, or data modules (IMPACT: HIGH)

Three GREEN/YELLOW-rated modules (生产 @82%, 吊挂 @78%) and one GREEN-rated module (数据 @78%) rely entirely on STATIC menu hierarchies from module_texts.txt. The live_system_menu_tree.md has captures for 10 modules but **not** for 生产, 吊挂, or the full hierarchy of 数据. This means:

- Menu structure may be incomplete or outdated
- No breadcrumb paths are verified
- No page-level IDs (`gm.页面名#N`) are captured

**Consequence:** Page navigation paths in Playwright scripts may be incorrect. The 生产 module's 29 pages represent the largest untested surface area.

**Recommended action:** Complete live system capture sessions for 生产, 吊挂, and 数据 modules, appending to live_system_menu_tree.md.

---

### Gap 5: Error message coverage is heavily skewed toward WMS (IMPACT: MEDIUM)

Of the ~95 error messages catalogued across the entire KB:

| Module | Error Messages |
|--------|:---:|
| 仓库 (WMS) | 22 (23%) |
| 生产 (Production) | 15 (16%) |
| 数据 (Master Data) | 15 (16%) |
| 采购 (Purchasing) | 10 (11%) |
| 吊挂 (Hanging) | 10 (11%) |
| 平板 (Tablet) | 5 (5%) |
| 质检 (Quality) | 2 (2%) |
| 系统 (System) | 1 (1%) |
| 销售 (Sales) | **0** |
| 物流 (Logistics) | **0** |
| 报表 (Reports) | **0** |
| 人事 (HR) | **0** |
| 样衣 (Sample) | **0** |
| 看板 (Dashboard) | **0** |

Seven modules have zero error messages catalogued. Error messages are critical for negative-testing Playwright scripts (asserting correct error text appears after invalid input).

**Consequence:** Negative test cases cannot verify error message text for 7 modules. Playwright `.toHaveText()` assertions will have nothing to match against.

**Recommended action:** Extract error messages systematically from the 7 official WMS/hanging documents that have not yet been fully mined. For modules with no official docs, use live system page interaction (submit empty forms, enter invalid values) to capture error messages.

---

## Dimension-Level Summary

| Dimension | Coverage | Notes |
|-----------|:---:|-------|
| Menu Structure | 79% | 11/14 have LIVE or STATIC; 3 have NONE (样衣, 看板, 平板 partial) |
| State Machines | 57% | 7 have YES, 2 have PARTIAL, 5 have NONE/NOT APPLICABLE |
| Business Rules | 54% | 7 have YES, 4 have PARTIAL, 3 have NONE |
| Error Messages | ~95 total | Heavily skewed to WMS (22) and Production (15); 7 modules have 0 |
| Field/Page Details | 43% | 6 have YES, 3 have PARTIAL, 5 have NONE |
| Feature Points (XMind) | 36% | 3 have YES, 2 have PARTIAL, 9 have NONE |
| Cross-Module Flows | 64% | 9 have YES, 5 have NONE |

---

## Data Source Utilization

| Source File | Modules Covered | Unique Value |
|-------------|:---:|-------|
| consolidated_domain_knowledge.md | ALL (1-14) | State machines, top rules, cross-module flows, ID conventions |
| error_messages_catalog.md | 4, 5, 9, 10, 11 | 95 error/confirmation/prompt messages from 7 docx sources |
| implicit_business_rules.md | 1-9 | 71 inferred rules from module_texts.txt menu hierarchies |
| live_system_menu_tree.md | 2, 3, 4, 6, 7, 8, 9, 11, 12, 14 | Live-captured menus for 10 modules + 4 captured pages with full field data |
| page_field_dictionary.md | 1-9 | Detailed field definitions for modules 5-9; PARTIAL/GAP for 1-4 |
| knowledge_gap_analysis.md | ALL (1-14) | Coverage heatmap, supplement strategies, SME interview templates |
| feature_production_offline.md | 5 | Production orders, offline tasks, workstation config, proxy reporting |
| feature_procurement_picking.md | 3, 4 | Fabric/accessory picking, cut-parts outsource, external purchase, PDA outbound |
| feature_style_reports.md | 8, 9 | Style management, report formatting, export customization, CPO deletion |
| module_texts.txt | 1-9 | Navigation text for 9 modules (modules 10-14 have no section) |

---

## Recommended Remediation Sequence

### Phase 1 (Week 1-2): Critical GAPs -- Enable E2E Test Script Generation

1. **Live-capture sales order pages** (销售订单 create/edit/list/detail) -- unblocks sales→production→purchasing E2E chains
2. **Live-capture production order pages** (生产订单 create/edit/tabs) -- unblocks the most test-heavy module
3. **Live-capture 生产, 吊挂, 数据 module menus** -- fills STATIC→LIVE gaps for 3 GREEN modules

### Phase 2 (Week 3-4): Fill Blind Spots

4. **SME interview for 样衣 module** -- document sample order lifecycle and sample-to-production conversion
5. **Error message extraction sprint** -- mine remaining official docs; live-capture errors for sales, logistics, HR
6. **Feature-point extraction for sales and QC** -- create feature_sales.md and feature_quality.md from available XMind files

### Phase 3 (Week 5-8): Depth and Completeness

7. **Field-level capture for all 采购 pages** -- only 1 of 17 pages has live field data
8. **Field-level capture for all 仓库 pages** -- the largest module (43 pages) has zero live field data
9. **System configuration parameter catalog** -- expand from ~13 known keys to full system config inventory
10. **Permission matrix documentation** -- map role tiers (#1/#2/#3) to specific CRUD+approve permissions per module

---

## Appendix: Source Documents Referenced

| # | File | Lines/Size | Type |
|---|------|:---:|------|
| 1 | references/consolidated_domain_knowledge.md | 482 lines | Core reference (merged from live + static + docs) |
| 2 | references/error_messages_catalog.md | 342 lines | Core reference (7 docx sources) |
| 3 | references/implicit_business_rules.md | 798 lines | Core reference (71 rules from module_texts) |
| 4 | references/live_system_menu_tree.md | 297 lines | Core reference (live capture 2026-07-01) |
| 5 | references/page_field_dictionary.md | 2890 lines | Core reference (modules 1-9, partial for 1-4) |
| 6 | references/knowledge_gap_analysis.md | 223 lines | Core reference (coverage heatmap, strategies) |
| 7 | references/feature_production_offline.md | 357 lines | Feature doc (production + offline) |
| 8 | references/feature_procurement_picking.md | 635 lines | Feature doc (picking + outsource + external purchase) |
| 9 | references/feature_style_reports.md | 393 lines | Feature doc (style management + reports) |
| 10 | C:\Users\yanta\Documents\ERP-test\module_texts.txt | ~450K chars | Live data (9 module sections, headers scanned) |


---

# 附录B: 补充方案



## 执行优先级

| 优先级 | 缺口 | 当前 | 目标 | 提升 | 预计工时 |
|--------|------|:---:|:---:|:---:|:---:|
| P0 | 销售零字段数据 | 55% | 85% | +30% | 4h |
| P0 | 生产页面字段全 [GAP] | 82% | 92% | +10% | 3h |
| P1 | 7 模块零错误消息 | 50% | 75% | +25% | 2h |
| P1 | 实时字段仅 4/14 模块 | 43% | 65% | +22% | 5h |
| P2 | 样衣完全盲区 | 5% | 40% | +35% | 3h |

---

## P0-1: 销售模块字段补全

### 现状
销售是最上游模块（订单驱动一切），但页面字段、按钮、筛选器数据完全空白。
唯一的数据来源是 module_texts.txt 中 "01_销售模块" 的导航文本。

### 目标页面（按业务价值排序）

| 页面 | 路径 | 优先级 | 原因 |
|------|------|:---:|------|
| 销售订单 | 销售→订单→销售订单 | 🔴 | 最核心页面，所有下游流程入口 |
| 订单预排期 | 销售→排期→订单预排期 | 🟡 | 排期规则入口 |
| 订单排期表 | 销售→排期→订单排期表 | 🟢 | 排期结果展示 |

### 每页面捕获项（10 项清单）

1. 所有表单字段（label + type + required + placeholder）
2. 所有表格列头（含排序/筛选标识）
3. 所有按钮（文本 + 位置 + 可见条件）
4. 所有下拉选项（完整枚举值）
5. 所有 Tab 页签名称
6. 所有筛选条件字段 + 筛选项
7. 所有状态标签（文字 + 颜色）
8. 面包屑导航路径
9. 操作按钮的权限可见性（哪些角色可见）
10. 截图（标注字段位置）

### 执行方式

```bash
# 使用已有系统权限，浏览器 DevTools 手动捕获
# 1. 登录 http://test.fj.dtsimple.pro
# 2. 打开 DevTools → Elements 面板
# 3. 导航到目标页面
# 4. 逐项记录到模板中
# 5. 截图保存到 captured/ 目录
```

### 预期产出

- `captured/01_销售_销售订单_field_data.md` — 完整字段字典
- 更新 `page_field_dictionary.md` 销售章节
- 更新 `live_system_menu_tree.md` 标注 [CAPTURED]

### 预期覆盖率提升

销售模块：55% → 85%（+30%）

---

## P0-2: 生产模块字段补全

### 现状
生产模块有最强的领域文档（状态机/业务规则/功能点均完整），但 29 个页面零实时字段数据。

### 目标页面（按业务价值排序，Top 8）

| 页面 | 路径 | 优先级 |
|------|------|:---:|
| 生产订单 | 生产→订单→生产订单 | 🔴 |
| 生产订单审核 | 生产→订单→生产订单审核 | 🔴 |
| 车间预排程 | 生产→排程→车间预排程 | 🔴 |
| 生产排程表 | 生产→排程→生产排程表 | 🟡 |
| 缝制任务 | 生产→任务→缝制任务 | 🟡 |
| 裁剪任务 | 生产→任务→裁剪任务 | 🟡 |
| 松布任务 | 生产→任务→松布任务 | 🟢 |
| 委外管理 | 生产→任务→委外管理 | 🟢 |

### 特别关注

生产订单有 11 个 Tab 页签（基本资料/颜色尺码/部位尺寸/工艺要求/生产工序/物料信息/配料说明/吊牌管理/唛架管理/装箱/操作日志），每个 Tab 的字段都需单独记录。

### 预期覆盖率提升

生产模块：82% → 92%（+10%）

---

## P1-3: 错误消息补全（7 模块零消息）

### 现状
error_messages_catalog.md 有 ~95 条消息，但：
- WMS（仓库）占 22 条
- 销售/采购/生产/质检/物流/报表/数据/吊挂/平板/人事/看板/系统 — 12 个模块零或极少

### 补充方法

**方法 A：从已有文档反向提取（零成本，立即可做）**
- 搜索 12 份知识库文档中的 "提示"/"错误"/"不允许"/"无法"/"请" 关键词
- 从 XMind 功能点中提取校验规则对应的错误消息

**方法 B：实时系统操作触发（需系统权限）**
- 在目标页面故意输入非法值
- 记录系统返回的错误提示文本
- 每个页面至少触发 3 种错误：必填缺失、格式错误、业务规则违反

### 目标模块

| 优先级 | 模块 | 最低目标 |
|:---:|------|------|
| P0 | 销售 | 8 条 |
| P0 | 生产 | 10 条 |
| P1 | 采购 | 6 条 |
| P1 | 质检 | 5 条 |
| P2 | 数据 | 5 条 |
| P2 | 报表 | 3 条 |

### 预期覆盖率提升

错误消息维度：50% → 75%（+25%，新增 ~37 条）

---

## P1-4: 实时字段批量扩充

### 现状
14 模块中仅仓库/采购/生产（组别日产量负荷表）/报表（缝制小组产量表）4 个模块有实时页面字段数据。

### 策略：分层捕获

**Layer 1 — 每个模块首页（14 页面，~2h）**
- 每个模块点击第一个子菜单项
- 快速记录：表单字段名 + 表格列头 + 按钮文本
- 快速模式：只记录名称，不记录类型/必填/默认值

**Layer 2 — 核心页面深度捕获（~3h）**
- 在 Layer 1 基础上，对 8 个核心页面做完整 10 项捕获
- 目标页面：销售订单/采购订单/生产订单/物料需求审核/质检配置/盘点单管理/款号管理/流水线配置

### 预期覆盖率提升

页面字段维度：43% → 65%（+22%）

---

## P2-5: 样衣模块破冰

### 现状
完全盲区（5%）。但 7 个报表确认其存在，24 个子菜单项已在实时系统中发现。

### 破冰策略

```
Step 1: 菜单发现（已完成 ✅）
  24 个子菜单项已在 live_system_menu_tree.md 中

Step 2: 首屏捕获（P2, ~1h）
  点击每个子菜单 → 截图 → 记录页面标题和 URL
  目标：确认哪些页面可访问，哪些需要权限

Step 3: 核心流程识别（P2, ~1h）  
  基于页面名称推断业务流程：
  样衣资料 → 工艺撰写 → 技术协作 → 物料需求 → 采购合同 → 入库 → 出库
  向 SME 确认流程准确性

Step 4: 字段补全（后续迭代）
  对 3-5 个核心页面做完整字段捕获
```

### 预期覆盖率提升

样衣模块：5% → 40%（+35%）

---

## 执行路线图

```
Week 1 (4h)  ████ P0-1 销售字段补全 (3页)
              ███  P0-2 生产字段补全 (8页)

Week 2 (5h)  █████ P1-4 Layer 1 批量首页捕获 (14页)
              ██   P1-3 方法A 文档反向提取错误消息

Week 3 (3h)  ███  P1-4 Layer 2 核心页面深度捕获 (8页)
              ██   P1-3 方法B 实时系统触发错误消息

Week 4 (3h)  ██   P2-5 样衣首屏 + 流程确认
              █    P1-3 收尾：合并到 error_messages_catalog.md
```

### 完成后预期

| 指标 | 当前 | 目标 |
|------|:---:|:---:|
| 总体完整度 | 51% | **75%** |
| 销售 | 55% | 85% |
| 生产 | 82% | 92% |
| 页面字段维度 | 43% | 65% |
| 错误消息维度 | 50% | 75% |
| 样衣 | 5% | 40% |
| 🟢 模块数 | 5 | **9** |
| 🔴 模块数 | 6 | **3** |
