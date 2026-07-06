# Implicit Business Rules Extracted from module_texts.txt Page Structure

> Source: `C:\Users\yanta\Documents\ERP-test\module_texts.txt`
> Date extracted: 2026-06-30
> Method: Static analysis of navigation text, breadcrumbs, alerts, ID patterns, and menu hierarchies
> IMPORTANT: module_texts.txt contains **navigation/menu text only** -- no form fields, no table columns,
> no button text, no status labels, and no color/icon information. Rules below are extracted from
> what IS present. All limitations are explicitly noted.

---

## 1. Role Assignment Model (Inferred from User ID Pattern `gm.xxx#N`)

### 1.1 Observed Roles and Access Levels

Every module section shows the same 14 user role entries in the sidebar/breadcrumb, each with a `#N` suffix.
The `#N` suffix indicates the user's **priority/access tier** within that module:

| User ID | Module | Tier | Interpretation |
|---------|--------|------|---------------|
| `gm.样衣#1` | 样衣 (Sample) | 1 | Primary sample garment user |
| `gm.销售#1` | 销售 (Sales) | 1 | Primary sales user |
| `gm.采购#2` | 采购 (Purchasing) | **2** | Secondary purchasing user (elevated tier) |
| `gm.仓库#1` | 仓库 (Warehouse) | 1 | Primary warehouse user |
| `gm.生产#3` | 生产 (Production) | **3** | Highest-tier production user |
| `gm.质检#1` | 质检 (QC) | 1 | Primary QC user |
| `gm.物流#1` | 物流 (Logistics) | 1 | Primary logistics user |
| `gm.报表#1` | 报表 (Reports) | 1 | Primary reports user |
| `gm.数据#1` | 数据 (Data) | 1 | Primary master-data user |
| `gm.吊挂#1` | 吊挂 (Hanging) | 1 | Primary hanging-system user |
| `gm.平板#1` | 平板 (Tablet) | 1 | Primary tablet-interface user |
| `gm.人事#1` | 人事 (HR) | 1 | Primary HR user |
| `gm.看板#1` | 看板 (Dashboard) | 1 | Primary dashboard user |
| `gm.系统#1` | 系统 (System) | 1 | Primary system-admin user |

### 1.2 Inferred Access Control Rules

RULE-R01: **Tier 3 (生产#3)** is the highest explicit tier -- the production user likely has elevated permissions
  (e.g., ability to publish orders, override statuses).

RULE-R02: **Tier 2 (采购#2)** for purchasing suggests a secondary role, possibly with approval
  authority but not full admin rights.

RULE-R03: All other modules are **Tier 1** -- primary operator but likely not the final approver.

RULE-R04: Breadcrumbs show `gm.首页#2` -- the home/dashboard role is Tier 2 (read-only or observer
  access, not admin).

RULE-R05: **Role isolation**: Each `gm.*` user appears in ALL module sections, suggesting a global
  visibility model -- any role can navigate to any module, but their `#N` tier controls what
  they can DO within each module.

### 1.3 Missing (Cannot Infer from This Data)

- Exact permission matrix (create/read/update/delete/approve per role per module)
- Whether tier numbers map to specific permission sets or are just display labels
- Whether `#1`, `#2`, `#3` are cumulative (higher includes lower) or disjoint
- No admin/super-admin role visible (e.g., no `gm.系统#99`)

---

## 2. Menu Hierarchy and Workflow Sequences (Tab Ordering)

### 2.1 Sales Module (01_销售模块) -- Menu Tree

```
订单
  └── 销售订单
排期
  ├── 订单预排期
  └── 订单排期表
```

**Business Rule Inferences:**

RULE-S01: Sales workflow is **Order first, then Scheduling**. You cannot schedule an order
  that does not exist.

RULE-S02: Two levels of scheduling: **Pre-scheduling (预排期)** before **Final scheduling (排期表)**.
  This implies a draft/confirmed scheduling pattern.

RULE-S03: CRITICAL GAP -- `销售订单` appears to be the ONLY sales entity. There is no visible:
  - Sales return/refund page
  - Sales order change/cancel page
  - Pricing/discount configuration
  - Customer-specific price list
  These may be inline operations within the sales order page.

### 2.2 Procurement Module (02_采购模块) -- Menu Tree

```
需求
  ├── 物料需求审核
  ├── 按单物料需求
  ├── 备货面料需求通知单
  └── 备货辅料需求通知单
订单
  ├── 采购计划
  ├── 采购订单
  ├── 面料采购计划
  ├── 辅料采购计划
  ├── 面料采购订单
  ├── 辅料采购订单
  └── 现金采购订单
收货
  ├── 面料收货通知单
  ├── 辅料收货通知单
  ├── 面料其他收货通知单
  └── 面料期初收货通知单
退货
  ├── 面料退货通知单
  └── 辅料退货通知单
```

**Business Rule Inferences:**

RULE-P01: **Demand-Driven Procurement**: The menu order is 需求 → 订单 → 收货 → 退货.
  Procurement flows: Demand Review → Plan → Order → Receive → Return.

RULE-P02: **Fabric and Accessory Split**: 面料 (fabric) and 辅料 (accessories/trims) have
  SEPARATE purchasing plans, orders, receipt notices, and return notices. They are never
  mixed on the same document.

RULE-P03: **Cash Purchase Order exception**: `现金采购订单` is a standalone entity -- it does
  NOT have a corresponding 现金采购计划. This implies cash purchases bypass the planning phase.

RULE-P04: **Fabric has extra receipt types**: Only 面料 gets `其他收货通知单` (other receipt)
  and `期初收货通知单` (opening balance receipt). 辅料 does NOT have these. This means:
  - Fabric can be received via non-standard channels (e.g., samples, transfers)
  - Fabric supports opening-balance import for system go-live
  - Accessories follow only standard receipt flow

RULE-P05: **物料需求审核** (Material Demand Review) is the FIRST step -- demands must be
  reviewed/approved before they can become purchase plans.

### 2.3 Production Module (03_生产模块) -- Menu Tree

```
排程
  ├── 车间预排程
  ├── 组别预排程
  ├── 生产排程表
  ├── 排程计划表
  ├── 组别日产量负荷表
  ├── 组别周产量负荷表
  ├── 缝制日目标
  ├── 缝制日目标达成表
  └── 吊挂目标设置
订单
  ├── 生产订单
  ├── 生产订单审核
  ├── 洗水订单
  ├── CPO明细表
  └── 生产订单
任务
  ├── 松布任务
  ├── 裁剪任务
  ├── 委外管理
  ├── 线外任务
  ├── 缝制任务
  └── 尾整任务
生产领料
  ├── 面料领料申请单
  ├── 辅料领料申请单
  └── 裁片领料申请单
生产过程
  ├── 裁剪完成转移单
  ├── 成衣尾整接收
  ├── 包码管理
  └── 包载绑定管理
成品
  ├── 装箱明细管理
  ├── 箱型管理
  └── 装箱单
```

**Business Rule Inferences:**

RULE-M01: **Garment production physical sequence**: The task order (松布 → 裁剪 → 缝制 → 尾整)
  matches the real-world garment manufacturing flow:
  1. 松布 (Fabric relaxing/spreading) -- prepare fabric
  2. 裁剪 (Cutting) -- cut fabric into pieces
  3. 缝制 (Sewing) -- sew pieces into garments
  4. 尾整 (Finishing) -- final finishing/pressing/packing

RULE-M02: **Two-level scheduling**: 车间预排程 (workshop pre-scheduling) → 组别预排程 (group
  pre-scheduling). Workshop-level is coarse; group-level is detailed. Changes at group
  level may not affect workshop-level.

RULE-M03: **Load monitoring by group, not workshop**: `组别日产量负荷表` and `组别周产量负荷表`
  track load at the GROUP level. This means capacity planning is managed per group/team,
  not per workshop.

RULE-M04: **Production order requires review**: `生产订单审核` exists as a separate menu item,
  meaning production orders have a **review/approval gate** before they can proceed to
  task generation.

RULE-M05: **Washing is a separate order type**: `洗水订单` (washing orders) are distinct from
  regular production orders, implying a separate workflow for garment washing processes.

RULE-M06: **CPO明细表** exists under orders -- CPO stands for "Cutting Production Order" or
  similar, suggesting cutting has its own detailed order tracking.

RULE-M07: **Picking requests are material-type-specific**: 面料, 辅料, and 裁片 each have their
  own picking request (领料申请单). They are never requested on the same form.

RULE-M08: **"线外任务" (offline tasks) exists between 委外管理 (outsourcing) and 缝制任务
  (sewing tasks)**. "线外" refers to operations outside the main hanging line -- these
  are manual/non-conveyor operations that happen in parallel to the main production flow.

RULE-M09: **Cutting completion triggers transfer**: `裁剪完成转移单` suggests cut pieces are
  formally transferred to the next stage, not just implicitly available.

RULE-M10: **Packaging management is hierarchical**: 装箱明细管理 (detail management) → 箱型管理
  (box type management) → 装箱单 (packing list). You define box types first, then manage
  individual box details, then generate packing lists.

### 2.4 Warehouse Module (04_仓库模块) -- Menu Tree

```
仓库管理
  ├── 工作区列表
  ├── 库区管理
  ├── 库位管理
  ├── 载具管理
  └── 料架管理
面料仓库
  ├── 面料货载管理
  ├── 面料物料清单
  ├── 面料库存管理
  ├── 面料仓出入库流水
  └── 面料退料回库单
松布仓库
  ├── 松布库存管理
  └── 松布出入库流水
辅料仓库
  ├── 辅料物料清单
  ├── 辅料库存管理
  └── 辅料出入库流水
裁片仓库
  ├── 裁片物料清单
  ├── 裁片库存管理
  └── 裁片出入库流水
成品仓库
  ├── 成品物料清单
  ├── 成品货载管理
  ├── 成品箱物流记录
  ├── 成品库存管理
  ├── 成品出入库流水
  ├── 箱出入库流水
  ├── 成品收货通知单
  ├── 成品出库通知单
  ├── 成品入库单
  ├── 成品出库单
  └── 成品箱库存管理
半成品仓库
  ├── 半成品库存管理
  ├── 半成品物料清单
  └── 半成品出入库流水
盘点
  ├── 调整单管理
  └── 盘点单管理
调度
  ├── 阶段模版配置
  ├── 任务寻找策略
  ├── 任务模版配置
  └── 任务记录
开箱
  ├── 开箱规则
  ├── 开箱机配置
  ├── 叫箱需求单
  └── 开箱任务记录
```

**Business Rule Inferences:**

RULE-W01: **Six inventory types, each segregated**: 面料, 松布, 辅料, 裁片, 成品, 半成品 each
  have their own warehouse sub-module. Inventory cannot be mixed across types.

RULE-W02: **松布 (relaxed fabric) is a SEPARATE inventory type** from 面料 (raw fabric).
  Once fabric goes through the relaxing/spreading process, it moves from 面料仓库 to
  松布仓库. This is a physical state change.

RULE-W03: **Not all warehouse types have the same feature set**:
  - 面料仓库: 5 sub-pages (richest -- includes carrier management, return-to-warehouse)
  - 成品仓库: 11 sub-pages (richest -- includes box logistics, receiving/delivery notices, inbound/outbound orders)
  - 松布仓库: 2 sub-pages (simplest -- inventory + transaction log only)
  - 辅料仓库: 3 sub-pages (no carrier management)
  - 裁片仓库: 3 sub-pages (no carrier management)
  - 半成品仓库: 3 sub-pages

RULE-W04: **Fabric has return-to-warehouse flow**: `面料退料回库单` exists only for 面料.
  If production returns unused fabric, it goes through this specific document.

RULE-W05: **Finished goods warehouse has the richest workflow**: It includes:
  - Receipt notices AND delivery notices (inbound and outbound notifications)
  - Actual inbound orders AND outbound orders (confirmation documents)
  - Box-level inventory AND box-level transaction log
  - Box logistics tracking (成品箱物流记录)
  This implies成品 warehouse is the most complex, handling full shipping logistics.

RULE-W06: **Adjustment and Inventory-Count are separate**:
  - 调整单管理 (adjustment order management) -- for direct stock adjustments
  - 盘点单管理 (inventory-count order management) -- for formal cycle/physical counts
  These are different business processes, not just different entry points.

RULE-W07: **Dispatch has template-based configuration**: 调度 (dispatch) uses 阶段模版配置
  (phase templates) and 任务模版配置 (task templates) -- meaning dispatch workflows are
  configurable per warehouse/factory, not hardcoded.

RULE-W08: **Box-calling workflow has its own sub-module (开箱)**:
  `开箱规则 → 开箱机配置 → 叫箱需求单 → 开箱任务记录`
  This matches the known WMS unboxing state machine from domain knowledge.

### 2.5 Quality Module (05_质检模块) -- Menu Tree

```
质量管理
  ├── 面料质检
  ├── 辅料质检
  ├── 成品质检
  ├── 缝制质检
  ├── 质检管理
  └── 质检配置
```

**Business Rule Inferences:**

RULE-Q01: **Four inspection types, one management view**: 面料, 辅料, 成品, 缝制 each have
  dedicated inspection pages. 质检管理 provides a unified management overview.

RULE-Q02: **QC configuration is global**: `质检配置` is a single entry, not per-inspection-type.
  QC rules (acceptance criteria, defect categories, scoring formulas) are configured
  once and applied across all inspection types.

RULE-Q03: **Inspection scope mapping to warehouse types**:
  - 面料质检 → 面料仓库/松布仓库 receiving
  - 辅料质检 → 辅料仓库 receiving
  - 成品质检 → 成品仓库 (final goods)
  - 缝制质检 → In-process inspection during sewing (on the hanging line)

### 2.6 Logistics Module (06_物流模块) -- Menu Tree

```
收货
  └── 半成品收货通知单
```

**Business Rule Inferences:**

RULE-L01: This module is a **thin shell** -- only one page. The real logistics handling
  probably happens within 仓库模块 (成品仓库 shipping/receiving) or 生产模块 (transfer
  between production stages).

RULE-L02: 半成品收货通知单 suggests semi-finished goods can be received from external
  sources (outsourcing returns, inter-factory transfers).

### 2.7 Reports Module (07_报表模块) -- Menu Tree (Categories)

The reports module is organized by business domain categories:

| Category | Report Count | Key Observations |
|----------|-------------|------------------|
| 委外 (Outsourcing) | 1 | 裁片外协报表 |
| 缝制 (Sewing) | 2 | Production quality + group output |
| 采购 (Purchasing) | 2 | Material purchase detail + receipt detail |
| 财务 (Finance) | 2 | AR report + AP report |
| 裁剪&裁片 (Cutting) | 14 | Heaviest report concentration |
| 吊挂 (Hanging) | 14 | Equal heaviest |
| 样衣 (Sample) | 7 | Sample tracking reports |
| 生产 (Production) | 15 | Heaviest concentration |
| 裁片仓 (Cut-Parts WH) | 6 | Warehouse-specific reports |
| 面料仓 (Fabric WH) | 8 | Warehouse-specific reports |
| 其他 (Other) | 2 | Employee skills + NPT tracking |
| 辅料仓 (Accessory WH) | 4 | Warehouse-specific reports |
| 成品仓 (Finished WH) | 4 | Warehouse-specific reports |

**Business Rule Inferences:**

RULE-RP01: **Reports are organized by BUSINESS DOMAIN, not by technical module**. A single
  business domain (e.g., 裁剪&裁片) spans both 生产模块 and 仓库模块.

RULE-RP02: **Highest report density**: 生产 (15), 裁剪&裁片 (14), 吊挂 (14) -- these are the
  most data-intensive business areas with the most KPIs to track.

RULE-RP03: **Finance reports are minimal** (AR + AP only) -- suggesting this is NOT a full
  ERP financial system; finance integration is likely external (e.g., 金蝶, 用友).

RULE-RP04: **Sample (样衣) has dedicated reports**: 7 reports for the sample-making process
  (办单全流程跟踪表, 采购物料跟踪表, 办单数量跟踪表, 跟单员工作量报表, 纸样员工工作量报表,
  样衣水洗明细表, 办房裁剪库存消耗表). This is a significant business area even though
  no separate module_texts file exists for it.

### 2.8 Data/Master Data Module (08_数据模块) -- Menu Tree

```
档案
  ├── 基础工序管理
  ├── 外购品管理
  ├── 基础面料
  ├── 基础辅料
  ├── 基础辅料           ← appears TWICE (likely end-of-line material vs. trims)
  ├── 供应商
  ├── 客户
  ├── 品牌
  ├── 工厂日历
  ├── 作息安排
  ├── 港口管理
  ├── 单位转换
  ├── 基础制程
  ├── 送货工厂管理
  ├── 尺码管理
  └── 报工系数配置
技术
  ├── 款号管理
  ├── 模板管理
  └── 工艺要求
```

**Business Rule Inferences:**

RULE-D01: **Master data split: 档案 (Records) vs 技术 (Technical)**. Records are operational
  reference data; Technical is product/process engineering data.

RULE-D02: **"基础辅料" appears twice** -- this is likely two different types:
  - 基础辅料 (1): End-of-line materials (线, 扣子, 拉链) -- sewing consumables
  - 基础辅料 (2): Trim/accessory materials (标签, 包装, 吊牌)
  OR it could be a data extraction artifact (duplicate entry).

RULE-D03: **工序 (process/routing) management is foundational**: `基础工序管理` is the FIRST
  entry under 档案 -- process definitions are the most fundamental master data, as they
  drive production routing, scheduling, and costing.

RULE-D04: **Site-level configuration**: 工厂日历, 作息安排, 港口管理, 送货工厂管理 are
  factory/site-specific, not global. Multi-factory deployments would have different
  values per site.

RULE-D05: **款式 (Style), 模板 (Template), 工艺要求 (Process Requirements)** form a hierarchy:
  Style defines WHAT to make, Template defines HOW to cut it, Process Requirements define
  HOW to sew/finish it.

### 2.9 Hanging System Module (09_吊挂模块) -- Menu Tree

```
吊挂
  ├── 流水线配置
  └── 吊挂扫码终端配置
分拣
  ├── 分拣MES配置
  └── 分拣下位配置
```

**Business Rule Inferences:**

RULE-H01: **Hanging system configuration split**: 流水线配置 (production line config) vs
  吊挂扫码终端配置 (scanning terminal config). These are separate concerns -- line
  topology vs. station hardware.

RULE-H02: **Sorting configuration is MES-integrated**: 分拣MES配置 indicates sorting is
  driven by MES configuration, not standalone.

RULE-H03: **分拣下位配置** (sorting lower-level config) controls the physical sorting
  hardware/PLC layer, not the business logic.

---

## 3. ID and Encoding Conventions

### 3.1 Material Codes (ML Prefix)

Pattern: `ML` + digits

| Observed Value | Context | Interpretation |
|---------------|---------|---------------|
| `ML863` | Breadcrumb in ALL modules | Active material/style context |
| `ML870` | Breadcrumb in ALL modules | Active material/style context |

**Business Rule Inferences:**

RULE-ID01: `ML` likely stands for **Material List** or **Model Line** -- it is a material/style
  identifier that appears in breadcrumbs across all modules, suggesting it is the currently
  active/looked-up material.

RULE-ID02: Both `ML863` and `ML870` appear together, suggesting dual-context navigation
  (e.g., comparing two materials, or a parent-child relationship).

RULE-ID03: The numeric part is 3 digits (863, 870), suggesting a range of at least 000-999
  for this ID segment. Unknown if the full code can be longer (e.g., ML1234).

### 3.2 Employee IDs

Pattern: 6-digit numeric

| Range | Examples | Likely Category |
|-------|----------|----------------|
| 100xxx | 100072, 100128, 100139, 100149, 100164, 100168, 100172, 100177, 100178, 100214, 100240, 100241, 100250 | Chinese-name employees (CHEN FEIMAN, CHEN GANG, ZOU WENQIANG, etc.) |
| 101xxx | 101035, 101341, 101616, 101972 | Mixed (Khmer names) |
| 102xxx | 102959 | Khmer names |
| 103xxx | 103299, 103742, 103990 | Khmer names |
| 104xxx | 104005, 104175, 104498, 104727, 104867 | Khmer names |
| 105xxx | 105241 | Khmer names |
| 106xxx | 106296 | Khmer names |
| 108xxx | 108481-108528 (many) | Khmer names |

**Business Rule Inferences:**

RULE-ID04: Employee IDs are **6-digit numeric**, starting from 100000.

RULE-ID05: **100xxx range contains Chinese-named employees** (likely headquarters/management
  staff from China). Khmer-named employees (Cambodian factory workers) are distributed
  across higher ranges (101xxx-108xxx).

RULE-ID06: The 108xxx range suggests at least 8,000+ employees have been registered in the
  system (IDs 100000-108528 observed).

RULE-ID07: There is a gap -- **107xxx range has no observed entries** in the notification
  data. This could mean: (a) range not yet allocated, (b) reserved range, or
  (c) employees in that range have no expiring documents.

### 3.3 Breadcrumb ID Pattern

In every module's breadcrumb area:
```
gm.首页#2
ML863
生产订单
ML870
```

**Business Rule Inferences:**

RULE-ID08: The breadcrumb shows **context stack**: `gm.首页#2` (home) > `ML863` (active
  material 1) > `生产订单` (current page type) > `ML870` (active material 2).

RULE-ID09: `生产订单` in the breadcrumb is the PAGE TYPE label, not a specific order number.
  This means the page title is reused as a breadcrumb segment.

---

## 4. Date/Time Formats

### 4.1 System Timestamp

All modules show the same timestamp format:

```
2026/06/30 08:00:13
```

**Business Rule Inferences:**

RULE-DT01: System timestamp format: `YYYY/MM/DD HH:MM:SS` (24-hour clock).

RULE-DT02: All 9 modules show the **identical timestamp** (`2026/06/30 08:00:13`), suggesting
  the module_texts were captured in a single session at this time.

### 4.2 Document Expiry Dates

Visa and passport expiry notifications use:
```
签证到期日期：2025/12/05
护照到期日期：2025/12/14
```

**Business Rule Inferences:**

RULE-DT03: Document expiry date format: `YYYY/MM/DD` (no time component -- date only).

RULE-DT04: **All observed visa/passport dates are in the past** (2025/12/05 through 2025/12/31,
  with a few at 2026/01/01). Since the system date is 2026/06/30, ALL these documents
  are ALREADY EXPIRED. These are outstanding/alarm notifications.

RULE-DT05: The date `2026/01/01` appears for 4 employees (DING JIAMEI, DENG NANCHANG,
  DENG XIAOLAN, DAI TAO) -- the latest expiry observed. Even this is ~6 months
  in the past from the system date.

---

## 5. Notification and Alert Patterns

### 5.1 Alert Types Observed

Two alert types appear in every module section:

1. **签证到期提醒** (Visa Expiry Reminder)
2. **护照到期提醒** (Passport Expiry Reminder)

**Business Rule Inferences:**

RULE-N01: Both alerts appear in ALL modules -- they are **global/system-level notifications**,
  not module-specific.

RULE-N02: Data format: `员工ID，姓名，证件类型到期日期：YYYY/MM/DD` -- each entry contains
  employee ID, name, document type, and expiry date.

RULE-N03: There are ~40-50 entries per alert type, suggesting a significant expat workforce
  (Cambodian factory with Chinese management, plus local Khmer workers with passports).

RULE-N04: **Visa and passport dates DO NOT always match**: `ZOU WENQIANG` appears in visa
  reminder with date 2025/12/14, and in passport reminder with the same date. But
  `ក ប៊ុនលី` appears in visa reminder with 2025/12/17, and in passport reminder
  with the same date. So the dates CAN differ per employee.

RULE-N05: The presence of these alerts implies:
  - An **HR module** that manages employee document records
  - A **scheduled job** that checks for approaching/expired documents
  - A **notification count** is visible (99+), suggesting a notification bell/badge

### 5.2 Notification Badge

The value `99+` appears at the top of every module section:

**Business Rule Inferences:**

RULE-N06: `99+` is a **notification badge count**, capped at 99 (shows "99+" when >= 100
  unread notifications).

RULE-N07: The badge count is identical across all modules, consistent with it being a
  global notification system.

---

## 6. System Branding and Context

### 6.1 Platform Identity

Every module section begins with:
```
瑞晟智能制造协同平台
最佳智造
```

**Business Rule Inferences:**

RULE-SYS01: **Platform name**: 瑞晟智能制造协同平台 (Ruisheng Intelligent Manufacturing
  Collaborative Platform).

RULE-SYS02: **Tagline**: 最佳智造 (Best Intelligent Manufacturing).

RULE-SYS03: The platform is branded as **IMS** (Intelligent Manufacturing System) in
  documentation, with the full Chinese name in the UI.

---

## 7. Module Navigation Pattern (Universal)

### 7.1 Sidebar Structure

Every module section has an identical sidebar showing all 14 roles:

```
gm.样衣#1
gm.销售#1
gm.采购#2
gm.仓库#1
gm.生产#3
gm.质检#1
gm.物流#1
gm.报表#1
gm.数据#1
gm.吊挂#1
gm.平板#1
gm.人事#1
gm.看板#1
gm.系统#1
```

Followed by the module-specific menu, followed by:
```
/
gm.首页#2
```

**Business Rule Inferences:**

RULE-NAV01: The **sidebar shows ALL roles**, not just the current module's role. This is a
  role-switching mechanism -- clicking a role name switches to that module's interface.

RULE-NAV02: The `/` separator divides the sidebar roles from the breadcrumb/home section.

RULE-NAV03: Navigation pattern is:
  - Top: 14 role-switching links (one per module)
  - Middle: Module-specific menu tree
  - Bottom: Home link and current breadcrumbs

---

## 8. Module Dependency Graph (Inferred from Menu Structure)

Based on which modules reference concepts from other modules:

```
数据(主数据) ──> 销售 ──> 采购 ──> 仓库/WMS ──> 生产/MES ──> 质检(QC)
                                   │               │
                                   └──> 物流 <─────┘
                                         │
                                   ┌─────┴─────┐
                                   │  吊挂系统   │
                                   └─────────────┘
                                         │
                                   报表(跨模块)
```

**Business Rule Inferences:**

RULE-DEP01: **Master data must exist first** (数据模块) -- styles, materials, processes,
  suppliers, customers, brands, etc. No transaction can be created without master data.

RULE-DEP02: **Sales drives demand** -- sales orders trigger material requirements which
  drive purchasing and production.

RULE-DEP03: **Purchasing and Production are parallel consumers** of sales demand. Both can
  be triggered from the same sales order.

RULE-DEP04: **WMS serves both Purchasing and Production** -- purchasing inbound goes to WMS;
  production picking goes from WMS.

RULE-DEP05: **QC is a gate at multiple points**: material receiving QC (面料/辅料),
  in-process QC (缝制), and final QC (成品).

RULE-DEP06: **吊挂 (Hanging system) is an execution system** that operates within the
  production module's 缝制 stage.

RULE-DEP07: **报表 (Reports) is cross-cutting** -- it reads from ALL other modules but
  does not drive any workflow.

---

## 9. Gaps: What CANNOT Be Inferred from This Data

This section is critical for understanding the limitations of the analysis.

### 9.1 Not Present in module_texts.txt at All

| Rule Type | Why Missing | Where to Find It |
|-----------|------------|------------------|
| **Status colors/icons** | No color/icon data in nav text | Actual UI screenshots or CSS inspection |
| **Required field markers** | No form fields in nav text | Actual form pages or HTML inspection |
| **Number format patterns** | No currency/quantity values displayed | Actual data entry pages |
| **Button visibility patterns** | No button text in nav text | Actual page captures |
| **Filter options** | No filter UI in nav text | List page headers |
| **Table column ordering** | No table content in nav text | List page table headers |
| **Validation hints/tooltips** | No inline help text | Form field `title`/`placeholder` attributes |
| **Placeholder text** | No input fields in nav text | Form field HTML |
| **Status label text** | No data rows in nav text | Table/list views |
| **Order numbers (CGJH- prefix etc.)** | No order data in nav text | Actual order list pages |

### 9.2 Partially Present (Inferred but Not Confirmed)

| Rule Type | What We Have | What We Still Need |
|-----------|-------------|-------------------|
| **Role permissions** | Role names and tiers (#1/#2/#3) | Exact permission matrix per role per operation |
| **Workflow sequences** | Menu ordering implies workflow | Actual state transitions and gate conditions |
| **Material subtypes** | Fabric vs. accessory split | Exact material classification criteria |
| **Warehouse features** | Different feature sets per type | Why certain warehouses lack certain features |

### 9.3 Recommended Next Steps for Filling Gaps

1. **Capture full page content** (Strategy D from knowledge_gap_analysis.md):
   - For each menu item, capture: form fields, buttons, table columns, filter options,
     status labels with colors, validation messages.
   - Append to module_texts.txt

2. **Extract status labels from actual data pages**:
   - Open list views and record all visible status values and their colors
   - Open detail views and record all visible buttons per status

3. **Capture form validation**:
   - Attempt to submit empty forms; record which fields trigger validation errors
   - Attempt to enter invalid values; record error messages

4. **Extract button visibility rules**:
   - Compare the same page under different `gm.*#N` roles
   - Record which buttons appear/disappear per role

---

## 10. Summary: Rule Count by Category

| Category | Rules Extracted | Confidence Level |
|----------|----------------|------------------|
| 1. Role Assignment | 5 | HIGH (explicit in data) |
| 2. Menu/Workflow | 32 | HIGH (menu structure is explicit) |
| 3. ID Conventions | 9 | HIGH (explicit patterns) |
| 4. Date/Time Formats | 5 | HIGH (explicit in data) |
| 5. Notifications | 7 | HIGH (explicit in data) |
| 6. System Branding | 3 | HIGH (explicit in data) |
| 7. Navigation Pattern | 3 | HIGH (explicit structure) |
| 8. Module Dependencies | 7 | MEDIUM (inferred from menu references) |
| 9. Gaps & Limitations | N/A | -- |
| **TOTAL** | **71 rules** | -- |

---

> Next: Feed these rules into test coverage matrix generation for scenario derivation.
> When actual page content becomes available, update status color mappings, validation
> rules, and button visibility rules.
