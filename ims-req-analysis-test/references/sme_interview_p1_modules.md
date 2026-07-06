# SME Interview Questionnaire: P1 Priority Modules

> **Purpose:** Structured interview guide for business experts to fill knowledge gaps in 6 P1 modules.
> **Baseline:** These modules have ~70-75% coverage from existing documentation. Only ask about what we DON'T already know.
> **Instructions for interviewer:** Before each section, confirm the "Already Known" summary with the SME. If any point is incorrect, note it in the answer table. Then proceed with gap questions.

---

## Interview Logistics Reference

| Field | Notes |
|-------|-------|
| SME Name / Role | _______________ |
| Interview Date | _______________ |
| System Version Discussed | Standard / Jingmen / Cambodia / Other: _____ |
| Duration Estimate | 2-3 hours (6 modules, 20-25 min each) |

---

---

# 1. 销售 (Sales) -- Coverage: ~70%

## 1.1 What We Already Know (Confirm, Do NOT Re-ask)

- **State machine:** 草稿 -> 生效 -> 中止 -> 反中止 -> 生效. 生效 supports 变更 (ETA/warehouse date) and 拆分 (by color/size, generates draft child orders).
- **Cross-module chain:** Sales Order BOM -> Production Order -> Material calculation.
- **Pages identified:** 销售订单, 订单预排期, 订单排期表.
- **Menu structure:** Confirmed from module_texts.txt.

## 1.2 Targeted Gap Questions

### Pricing & Discounts

**Q1.** What pricing mechanisms exist on a sales order? Is there a base price list, and how are prices determined -- by customer contract, by style, by season, or a combination? Does the system support tiered/volume-based pricing?

**Q2.** What discount types are supported (percentage, fixed amount, per-item, per-order)? Can discounts stack (e.g., seasonal + customer loyalty)? Who has authority to override the calculated price?

### Multi-Currency

**Q3.** Does the sales module support multi-currency? If yes: where is the currency set (customer master, order header, or line item)? How are exchange rates sourced -- manual entry, rate table, or external feed? What happens to financial reports when exchange rates fluctuate between order creation and payment?

### Sales-to-Finance Integration

**Q4.** At what point does a sales order become visible to the finance/AR module -- upon creation (草稿), activation (生效), or shipment? Is there a credit check against the customer before order activation?

**Q5.** What financial documents or entries are generated from a sales order (invoice, delivery note, AR entry)? Is this automatic or manual? What information flows bidirectionally between Sales and Finance?

### Sales Order Change Management

**Q6.** After a sales order is 生效, what fields can be changed via the 变更 function? Are changes logged in an audit trail? Is there a version history for each sales order?

**Q7.** When an order is 拆分 (split), what happens to the original order's pricing, delivery dates, and references? Does the split trigger any notification to production planning?

## 1.3 Version Differences Probe

| Question | Notes |
|----------|-------|
| Do different client versions have different sales order approval workflows? | |
| Are there client-specific fields on the sales order (e.g., L/C number, forwarder, shipping terms)? | |
| Do any clients integrate sales orders with external ERP/finance systems differently? | |

## 1.4 Answer Recording Table

| Q# | SME Response | Key Rules Captured | Follow-up Needed? |
|----|-------------|-------------------|-------------------|
| Q1 | | | |
| Q2 | | | |
| Q3 | | | |
| Q4 | | | |
| Q5 | | | |
| Q6 | | | |
| Q7 | | | |

---

---

# 2. 采购 (Procurement) -- Coverage: ~75%

## 2.1 What We Already Know (Confirm, Do NOT Re-ask)

- **State machines:** 物料需求: 草稿 -> 审核中 -> 审核通过 (撤回送审, 反审核); 采购订单: 草稿 -> 生效 -> 确认到货 (locks receipt notices).
- **Pages identified:** 16 pages including 物料需求审核, 采购计划, 采购订单 (面料/辅料/现金 variants), 收货通知单, 退货通知单.
- **Cross-module chain:** Production Order -> Material Demand -> Demand Review -> Purchase Plan -> Purchase Order -> Receipt Notice -> Material Receipt -> Inventory.
- **Version differences:** 辅料收货: 荆门=先录后贴, 新基=无箱贴.
- **Receipt states:** 待收货 -> 已收货(临时库区) -> 已入库(立库库区).

## 2.2 Targeted Gap Questions

### Supplier Evaluation

**Q1.** Does the system track supplier performance metrics? If so, what metrics are captured (on-time delivery rate, quality pass rate, price variance, response time)? Where is this data visible -- supplier master, procurement dashboard, or separate evaluation page?

**Q2.** Is there a supplier qualification/approval workflow? Can unapproved suppliers be used on purchase orders? Is there an approved vendor list (AVL) that gates which suppliers can receive POs?

### Approval Hierarchy

**Q3.** What is the approval chain for purchase orders? Does it vary by order amount, material type (fabric vs. accessories vs. MRO), or supplier? What thresholds trigger different approval levels?

**Q4.** How does the 物料需求审核 (Material Requirement Review) approval relate to the 采购订单 approval -- are they independent, sequential, or can they be combined? Can a single approver approve both, or is segregation of duties enforced?

### Procurement Change Management

**Q5.** After a purchase order is 生效, what changes are allowed? Can quantity, price, delivery date, or supplier be modified? If so, does the change require re-approval?

**Q6.** How are price changes handled when a supplier delivers at a different price than the PO? Does the system support price tolerance (auto-accept if within X%), or is manual intervention always required?

### Receipt Flexibility

**Q7.** Can a single purchase order be received across multiple 收货通知单 (partial receipts)? What about over-receipt -- is there a tolerance percentage or is it strictly blocked? How does over/under receipt affect the PO status?

**Q8.** How does the 现金采购订单 (Cash PO) differ from standard POs in terms of workflow, approval, and financial integration?

## 2.3 Version Differences Probe

| Question | Notes |
|----------|-------|
| Do different clients have different PO approval hierarchies (e.g., by factory, by material category)? | |
| Is 辅料收货 mode (先录后贴 vs. 无箱贴 vs. other) configurable per client, or hardcoded? | |
| Do any clients use EDI or supplier portal for PO transmission and confirmation? | |

## 2.4 Answer Recording Table

| Q# | SME Response | Key Rules Captured | Follow-up Needed? |
|----|-------------|-------------------|-------------------|
| Q1 | | | |
| Q2 | | | |
| Q3 | | | |
| Q4 | | | |
| Q5 | | | |
| Q6 | | | |
| Q7 | | | |
| Q8 | | | |

---

---

# 3. 生产 (Production) -- Coverage: ~75%

## 3.1 What We Already Know (Confirm, Do NOT Re-ask)

- **State machines:** 生产订单: 草稿 -> 审核中 -> 生效 -> 已发布 -> 完成 (反发布/反生效). 缝制任务: 新增计划 -> 产前准备 -> 待缝制 -> 缝制中 -> 已完成 (换款/恢复). 备料: 未备料 <-> 已备料. 裁片: 待配套 <-> 已配套.
- **Pages identified:** 23 pages across 排程, 订单, 任务, 生产领料, 生产过程, 成品 sub-menus.
- **Device coverage:** PC (planning/orders), PAD (shop-floor tasks), PDA (picking), Industrial Tablet (hanging station).
- **Known rules:** Only editable in 草稿. Missing style name blocks 扎卡 tag generation. First process must be 挂片站. Preparations lock carriers.

## 3.2 Targeted Gap Questions

### Scheduling Algorithms

**Q1.** How does 车间预排程 (Workshop Pre-Scheduling) actually work? Is it a manual drag-and-drop tool, or does it auto-schedule based on rules (e.g., earliest due date, setup time minimization, priority)? What constraints does it consider (line capacity, material availability, delivery date)?

**Q2.** What is the relationship between 订单预排期 (Sales Order Pre-Scheduling) and 车间预排程? Is it a two-level scheduling hierarchy (rough-cut -> detailed)? What happens when the workshop schedule conflicts with the sales pre-schedule?

### Capacity Calculation

**Q3.** How is production line/group capacity defined and measured? Is it based on SAM (Standard Allowed Minutes), historical output, or manually entered daily targets? How is the 组别日产量负荷表 (Group Daily Output Load Table) calculated -- what formula or algorithm?

**Q4.** When a line is overloaded (demand exceeds capacity for a given period), how does the system surface this? Are there visual warnings on the scheduling pages? Can users manually override capacity limits?

### Material Completeness Check (物料齐套)

**Q5.** Before a production order can be 发布 (published/released), what material completeness checks occur? Is there an automated 齐套检查 (kit completeness check) that gates release? What is the exact rule -- all materials must be in stock, X% threshold, or critical-path materials only?

**Q6.** When materials are partially available, what actions can the production planner take? Can they release with shortage, reserve available materials for this order, or trigger emergency procurement?

### Production Progress & Exception Handling

**Q7.** How is a 缝制任务's 换款 (style change) operation different from a normal 缝制暂停? What system state changes occur -- are WIP materials tracked differently, is the production schedule automatically adjusted?

**Q8.** What happens when production exceeds the planned quantity (over-production)? Does the system allow it, block it, or require approval? How does over-production affect material consumption tracking?

## 3.3 Version Differences Probe

| Question | Notes |
|----------|-------|
| Do different client factories use different scheduling algorithms (e.g., make-to-order vs. make-to-stock)? | |
| Are 车间预排程 and 组别预排程 universally used, or do some clients skip them? | |
| Do any clients use automatic scheduling optimization vs. purely manual scheduling? | |

## 3.4 Answer Recording Table

| Q# | SME Response | Key Rules Captured | Follow-up Needed? |
|----|-------------|-------------------|-------------------|
| Q1 | | | |
| Q2 | | | |
| Q3 | | | |
| Q4 | | | |
| Q5 | | | |
| Q6 | | | |
| Q7 | | | |
| Q8 | | | |

---

---

# 4. 质检 (QC) -- Coverage: ~65%

## 4.1 What We Already Know (Confirm, Do NOT Re-ask)

- **State machine:** 待检验 -> 检验中 -> 已完成. Approval: 确认检验结果 (OK/NG/让步使用).
- **QC scoring formulas:** 100码 and 百平方码 modes -- full formulas known. 总扣分 > 可接受分数 = 不合格.
- **Pages identified:** 6 pages: 面料质检, 辅料质检, 成品质检, 缝制质检, 质检管理, 质检配置.
- **Version differences:** QC approval granularity (standard=whole-order, 荆门=material+color level). 荆门=full 缝制质检 workflow (巡检/首检/尾检). 荆门=LOT色 support.
- **Device support:** PC (config/review), PAD (shop-floor inspection), Industrial Tablet (hanging QC).

## 4.2 Targeted Gap Questions

### Defect Classification Taxonomy

**Q1.** What is the complete defect classification system? Is there a hierarchical taxonomy (e.g., Category -> Sub-category -> Defect Code)? Can you walk through an example: for fabric inspection, what are the top-level defect categories and typical sub-defects?

**Q2.** Does the defect classification differ by QC type (面料 vs. 辅料 vs. 成品 vs. 缝制)? Are there type-specific defect codes, or is it a unified taxonomy? Where is this taxonomy configured (is it the 质检配置 page)?

**Q3.** How is defect severity handled? Is there a severity level (critical/major/minor) per defect type, and does it affect the acceptance decision differently (e.g., one critical defect = auto-reject)?

### QC-to-Supplier Feedback

**Q4.** When a QC inspection fails (NG or 让步使用), what feedback goes back to the supplier? Is there a formal non-conformance report (NCR) or supplier corrective action request (SCAR) generated? Is quality performance tracked at the supplier level and does it affect future procurement decisions?

**Q5.** For 让步使用 (concession/use-as-is) decisions -- who can approve them? Is there a separate approval workflow distinct from the standard QC result confirmation? Are there limits on how many concessions a supplier can accumulate before being blocked?

### QC Configuration Details

**Q6.** On the 质检配置 page, how are QC standards (质检标准) defined? Is each standard a reusable template that can be assigned to multiple material types/suppliers? What happens when two different standards could apply to the same item -- what is the precedence rule?

**Q7.** How is the sampling method determined? The page field dictionary shows Fixed rate / AQL / 全检 options -- what AQL tables are used (ANSI/ASQ Z1.4, ISO 2859)? Is the sampling plan (sample size, accept/reject numbers) auto-calculated based on lot size and AQL level?

## 4.3 Version Differences Probe

| Question | Notes |
|----------|-------|
| Beyond 荆门's material+color approval, do any other clients have different QC approval models? | |
| Do different clients use different AQL standards (e.g., US vs. EU brands with different requirements)? | |
| For 成品质检, how is the process different between 荆门 (full workflow) and other versions (not mentioned in docs)? | |

## 4.4 Answer Recording Table

| Q# | SME Response | Key Rules Captured | Follow-up Needed? |
|----|-------------|-------------------|-------------------|
| Q1 | | | |
| Q2 | | | |
| Q3 | | | |
| Q4 | | | |
| Q5 | | | |
| Q6 | | | |
| Q7 | | | |

---

---

# 5. 报表 (Reports) -- Coverage: ~45%

## 5.1 What We Already Know (Confirm, Do NOT Re-ask)

- **Report inventory:** 50+ reports across 12 categories: 委外(1), 缝制(2), 采购(2), 财务(2), 裁剪&裁片(16), 吊挂(17), 样衣(7), 生产(14), 裁片仓(5), 面料仓(7), 辅料仓(4), 成品仓(4), 其他(2).
- **Common UI patterns:** All reports share date range filter, 车间/组别/款号/订单号 filters, and 查询/重置/导出/打印 buttons. Standard Ant Design Table + Pagination pattern confirmed.
- **Column structures:** Most report columns inferred from domain knowledge (see page_field_dictionary_05_09.md for full listing).
- **Report categories documented** with inferred column definitions for each report.

## 5.2 Targeted Gap Questions

### Report Aggregation Logic

**Q1.** For reports that show aggregated metrics (e.g., 生产全流程报表, 生产质量汇总表), how is the aggregation performed? Is it: (a) real-time query against transactional data, (b) pre-aggregated materialized views updated periodically, or (c) a data warehouse/OLAP cube? If periodic, what is the refresh frequency?

**Q2.** For cross-module reports like 采购跟踪表 (which tracks procurement AND production status), how is data joined across modules? Is there a unified data model or are these point-to-point integrations? What happens when source data in one module changes -- does the report reflect it immediately?

### Permission Scoping Per Report

**Q3.** Is report access controlled by user role? Can a user only see reports for their department (e.g., sewing supervisor sees only 缝制 reports, not 采购 reports)? Within a report, is the data automatically scoped to their organizational unit (their workshop, their group)?

**Q4.** Are there any reports that contain financially sensitive data (e.g., 应收报表, 应付报表, 物料采购明细表 with unit prices)? If so, is there fine-grained permission control -- can some roles see quantity but not price, or see summary but not detail?

### Export Constraints

**Q5.** What are the export capabilities for each report? Is there a row limit on exports (e.g., max 10,000 rows)? What export formats are supported (Excel, PDF, CSV)? Are there reports that CANNOT be exported due to data sensitivity?

**Q6.** For the many 裁剪&裁片 reports (16 reports in one sub-category) -- why so many variants? Are these client-specific customizations, or do they serve genuinely different analytical needs? Which ones are standard vs. custom?

### Report Customization

**Q7.** Can users create custom reports or modify existing ones? Is there a report builder, or are all reports hardcoded? Can users save their own filter presets?

## 5.3 Version Differences Probe

| Question | Notes |
|----------|-------|
| Which reports are standard (all clients get them) vs. client-specific customizations? | |
| Do different clients have different financial report formats (e.g., Chinese GAAP vs. IFRS requirements)? | |
| Are any reports localization-dependent (language, currency format, date format)? | |

## 5.4 Answer Recording Table

| Q# | SME Response | Key Rules Captured | Follow-up Needed? |
|----|-------------|-------------------|-------------------|
| Q1 | | | |
| Q2 | | | |
| Q3 | | | |
| Q4 | | | |
| Q5 | | | |
| Q6 | | | |
| Q7 | | | |

---

---

# 6. 数据/主数据 (Master Data) -- Coverage: ~55%

## 6.1 What We Already Know (Confirm, Do NOT Re-ask)

- **Pages identified:** 18 pages: 15 under 档案 (基础工序, 外购品, 基础面料, 基础辅料, 供应商, 客户, 品牌, 工厂日历, 作息安排, 港口管理, 单位转换, 基础制程, 送货工厂, 尺码管理, 报工系数) + 3 under 技术 (款号管理, 模板管理, 工艺要求).
- **Common CRUD pattern:** All pages follow 新建/编辑/删除/查询/重置/导出 pattern. Standard 编码/名称/状态/创建时间/操作 list columns.
- **Entity fields:** Detailed field lists for most entities (see page_field_dictionary_05_09.md).
- **Known validations:** Duplicate supplier code blocked ("编码重复，不允许保存"). Invalid style code format ("编码格式不正确"). Duplicate style code ("款号已存在").
- **Cross-module links:** 供应商->采购订单, 客户->销售订单, 基础面料/辅料->采购订单, 款号->生产订单+BOM.

## 6.2 Targeted Gap Questions

### Data Validation Rules (Formal, Complete)

**Q1.** What are the complete field validation rules for each master data entity? Specifically: (a) Which fields are mandatory vs. optional? (b) What are the format constraints (length limits, character restrictions, numeric ranges)? (c) Are there cross-field validation rules (e.g., "if supplier type is 面料, then default payment terms must be set")?

**Q2.** For codes/IDs (编码) across all master data entities -- is there a naming convention or pattern (e.g., SUP-xxxx for suppliers, FAB-xxxx for fabrics)? Can codes be changed after creation, or are they immutable?

### Cross-Module Data Dependencies

**Q3.** What are the referential integrity rules? If a supplier, customer, material, or style is already referenced by a transaction (PO, SO, production order), can it be deleted or deactivated? Is it a hard block or a soft warning?

**Q4.** When master data changes (e.g., supplier address, fabric specification, style BOM), do the changes cascade to existing transactions? Does a change to 基础面料 apply retroactively to open purchase orders, or only to new POs?

**Q5.** The 款号管理 (Style Management) page is the most complex master entity, linking to brand, customer, size group, routing, BOM, and process requirements. What is the exact creation sequence -- which dependencies must exist BEFORE a new style can be created? Can a style exist without a complete BOM?

### Import/Export Rules

**Q6.** What master data entities support bulk import (导入)? What format is required (Excel template, CSV)? Are there validation rules during import -- partial success allowed, or all-or-nothing? Is there a dry-run/preview mode before committing imports?

**Q7.** For entities that support 模板管理 (template management for import/export), what exactly do the templates contain? Are they just column headers, or do they include data validation rules, dropdown lists, and formula cells?

### Entity Lifecycle

**Q8.** What is the lifecycle of master data entities? Is there a concept of "draft" master data vs. "published/active"? Can master data changes go through an approval process, or are they effective immediately? Is there an audit trail for master data changes?

## 6.3 Version Differences Probe

| Question | Notes |
|----------|-------|
| Do different clients use different 编码 (code) schemes or formats? | |
| Is 单位转换 (Unit Conversion) pre-loaded with standard conversions, or does each client configure their own? | |
| Are any master data entities client-specific (e.g., some clients may not use 港口管理 or 送货工厂管理)? | |

## 6.4 Answer Recording Table

| Q# | SME Response | Key Rules Captured | Follow-up Needed? |
|----|-------------|-------------------|-------------------|
| Q1 | | | |
| Q2 | | | |
| Q3 | | | |
| Q4 | | | |
| Q5 | | | |
| Q6 | | | |
| Q7 | | | |
| Q8 | | | |

---

---

# Appendix A: Cross-Cutting Questions (Ask Last)

These apply across multiple modules. Ask them once and note which module(s) the answer affects.

**CC1.** 权限模型 (Permission Model): What is the granularity of the permission system? Is it role-based (RBAC) with predefined roles, or can permissions be assigned per-user, per-page, per-operation (CRUD)? Are there data-scoping permissions (e.g., "can only see POs for their own department")?

**CC2.** 审批流引擎 (Approval Workflow Engine): Is the approval workflow a generic engine configured per module, or are approvals hardcoded per entity type? Can clients customize approval chains (add/remove approvers, add conditions) without code changes?

**CC3.** 审计日志 (Audit Trail): Which entities have audit logging? Is it: all transactional entities (SO, PO, production order), master data changes, or both? What fields are logged (who, when, old value, new value)?

**CC4.** 并发控制 (Concurrency Control): What happens when two users edit the same entity simultaneously? Is it optimistic locking (last-save-wins with warning), pessimistic locking (first user locks the record), or something else?

**CC5.** 系统配置 (System Configuration Parameters): Beyond `st_auto_create_after_mpo_submit_enable`, what other system configuration parameters exist? Is there a central admin page listing all configurable parameters with descriptions and default values?

| CQ# | SME Response | Modules Affected | Follow-up Needed? |
|-----|-------------|-----------------|-------------------|
| CC1 | | | |
| CC2 | | | |
| CC3 | | | |
| CC4 | | | |
| CC5 | | | |

---

# Appendix B: Post-Interview Action Items

| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| 1 | Update erp_domain_knowledge.md with new state machines, rules, formulas from interview | | | |
| 2 | Update page_field_dictionary with confirmed/corrected field details | | | |
| 3 | Update knowledge_gap_analysis.md coverage percentages | | | |
| 4 | Generate revised test coverage matrix for updated domains | | | |
| 5 | Schedule follow-up interview if "Follow-up Needed?" is marked for any question | | | |
| 6 | Request access to live system for page capture (Strategy D) to verify interview findings | | | |

---

*Document version: 1.0 | Generated: 2026-06-30 | Based on: knowledge_gap_analysis.md v1, erp_domain_knowledge.md v1, page_field_dictionary_01_04.md v1, page_field_dictionary_05_09.md v1*
