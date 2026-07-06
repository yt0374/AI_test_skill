# IMS ERP Knowledge Base Completeness Audit Report

> **Generated:** 2026-07-02
> **Source documents analyzed:** 9 reference files, 3 feature docs, 1 live data file
> **Method:** Cross-referencing all available sources against 8 assessment dimensions per module

---

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
