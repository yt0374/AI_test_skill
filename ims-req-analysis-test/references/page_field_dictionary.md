# IMS Page Field Dictionary -- Modules 01-04

> **Source:** `C:\Users\yanta\Documents\ERP-test\module_texts.txt`
> **Extraction Date:** 2026-06-30
> **Status:** PARTIAL -- Source file contains only menu/page names and navigation structure.
> Detailed field names, button names, filter fields, tab names, required indicators,
> dropdown options, and status labels are **NOT present** in the source file and must be
> supplemented via page capture (Strategy D) or SME interview (Strategy C) as outlined in
> `knowledge_gap_analysis.md`.
>
> **Legend for coverage indicators:**
> - [OK] = Information present in source file
> - [DK] = Cross-referenced from `erp_domain_knowledge.md`
> - [GAP] = Not available; needs supplementation
> - [INFER] = Inferred from page name / domain conventions

---

## 01_销售 (Sales)

Coverage: Menu structure [OK] | Fields/Buttons/Filters/Tabs [GAP] | Status labels [DK]

### Menu Category: 订单 (Orders)

#### Page: 销售订单 (Sales Order)
- **Source line:** 36-37
- **Domain Knowledge [DK]:** State machine: 草稿 -> 生效 -> 中止 -> 反中止 -> 生效. 生效 supports 变更 (modify ETA/warehouse date) and 拆分 (split by color/size qty, creates Draft child orders). Only editable in 草稿.
- **Fields:** [GAP -- not in source]
- **Buttons:** [GAP -- not in source]
- **Filters:** [GAP -- not in source]
- **Tabs:** [GAP -- not in source]
- **Status Labels [DK]:** 草稿 (Draft), 生效 (Active), 中止 (Suspended)
- **Required Fields:** [GAP -- not in source]

### Menu Category: 排期 (Scheduling)

#### Page: 订单预排期 (Order Pre-Scheduling)
- **Source line:** 39
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 订单排期表 (Order Schedule Table)
- **Source line:** 40
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

---

## 02_采购 (Purchasing)

Coverage: Menu structure [OK] | Fields/Buttons/Filters/Tabs [GAP] | Status labels [DK]

### Menu Category: 需求 (Requirements)

#### Page: 物料需求审核 (Material Requirement Review)
- **Source line:** 86
- **Domain Knowledge [DK]:** State machine for 物料需求: 草稿 -> 提交审核 -> 审核中 -> 审核通过 (available for PO). 审核中 supports 撤回送审 -> 草稿. 审核通过 supports 反审核 (only if no PO created yet).
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels [DK]:** 草稿, 审核中, 审核通过
- **Required Fields:** [GAP]

#### Page: 按单物料需求 (Per-Order Material Requirements)
- **Source line:** 87
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 备货面料需求通知单 (Stock-up Fabric Requirement Notice)
- **Source line:** 88
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 备货辅料需求通知单 (Stock-up Accessory Requirement Notice)
- **Source line:** 89
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 订单 (Orders)

#### Page: 采购计划 (Purchase Plan)
- **Source line:** 91
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 采购订单 (Purchase Order)
- **Source line:** 92
- **Domain Knowledge [DK]:** State machine: 草稿 -> 生效. 生效 -> 确认到货 (locks receipt notices). 草稿 supports 删除 (only in 草稿).
- **Cross-module [DK]:** Production Order -> Material Demand -> Demand Review -> Purchase Plan -> Purchase Order -> Receipt Notice -> Material Receipt -> Inventory
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels [DK]:** 草稿, 生效
- **Required Fields:** [GAP]

#### Page: 面料采购计划 (Fabric Purchase Plan)
- **Source line:** 93
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 辅料采购计划 (Accessory Purchase Plan)
- **Source line:** 94
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 面料采购订单 (Fabric Purchase Order)
- **Source line:** 95
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels [DK]:** 草稿, 生效 (same state machine as 采购订单)
- **Required Fields:** [GAP]

#### Page: 辅料采购订单 (Accessory Purchase Order)
- **Source line:** 96
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels [DK]:** 草稿, 生效
- **Required Fields:** [GAP]

#### Page: 现金采购订单 (Cash Purchase Order)
- **Source line:** 97
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 收货 (Receiving)

#### Page: 面料收货通知单 (Fabric Receipt Notice)
- **Source line:** 99
- **Domain Knowledge [DK]:** State flow: 待收货 -> PDA物料收货 -> 已收货(临时库区) -> PDA货载上架 -> 已入库(立库库区). Duplicate receipt blocked. Delete only allowed in 待收货.
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels [DK]:** 待收货, 已收货, 已入库
- **Required Fields:** [GAP]

#### Page: 辅料收货通知单 (Accessory Receipt Notice)
- **Source line:** 100
- **Version differences [DK]:** 荆门: 先录后贴; 新基: 无箱贴; Standard: all 3 modes
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels [DK]:** 待收货, 已收货, 已入库
- **Required Fields:** [GAP]

#### Page: 面料其他收货通知单 (Fabric Other Receipt Notice)
- **Source line:** 101
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 面料期初收货通知单 (Fabric Opening Receipt Notice)
- **Source line:** 102
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 退货 (Returns)

#### Page: 面料退货通知单 (Fabric Return Notice)
- **Source line:** 104
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 辅料退货通知单 (Accessory Return Notice)
- **Source line:** 105
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

---

## 03_生产 (Production)

Coverage: Menu structure [OK] | Fields/Buttons/Filters/Tabs [GAP] | Status labels [DK]

### Menu Category: 排程 (Scheduling)

#### Page: 车间预排程 (Workshop Pre-Scheduling)
- **Source line:** 151
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 组别预排程 (Group Pre-Scheduling)
- **Source line:** 152
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 生产排程表 (Production Schedule Table)
- **Source line:** 153
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 排程计划表 (Schedule Plan Table)
- **Source line:** 154
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 组别日产量负荷表 (Group Daily Output Load Table)
- **Source line:** 155
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 组别周产量负荷表 (Group Weekly Output Load Table)
- **Source line:** 156
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 缝制日目标 (Sewing Daily Target)
- **Source line:** 157
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 缝制日目标达成表 (Sewing Daily Target Achievement Table)
- **Source line:** 158
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 吊挂目标设置 (Hanging Target Setting)
- **Source line:** 159
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 订单 (Orders)

#### Page: 生产订单 (Production Order)
- **Source lines:** 161, 165 (appears twice in menu)
- **Domain Knowledge [DK]:** State machine: 草稿 -> 提交审核 -> 审核中 -> 通过 (back to edit flow) / 驳回 (editing). 草稿 -> 生效 -> 发布 -> 已发布. 已发布 -> 反发布 -> 生效 -> 反生效 -> 草稿. 已发布 -> 完成 / 发起领料. Only editable in 草稿.
- **Cross-module [DK]:** Sales Order BOM -> Production Order -> Material calculation. Published PO -> Picking Request -> Cloth Loosening (if 松布作业=是).
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels [DK]:** 草稿, 审核中, 生效, 已发布, 完成
- **Required Fields:** [GAP]
- **Device [DK]:** PC for creation; PAD/PDA for shop floor execution

#### Page: 生产订单审核 (Production Order Review)
- **Source line:** 162
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels [DK]:** 审核中 (related to 生产订单 state machine)
- **Required Fields:** [GAP]

#### Page: 洗水订单 (Washing Order)
- **Source line:** 163
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: CPO明细表 (CPO Detail Table)
- **Source line:** 164
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 任务 (Tasks)

#### Page: 松布任务 (Cloth Loosening Task)
- **Source line:** 167
- **Device [DK]:** PAD
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 裁剪任务 (Cutting Task)
- **Source line:** 168
- **Device [DK]:** PAD
- **Domain Knowledge [DK]:** Cutting tasks cannot generate 扎卡 tags if style name is missing
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 委外管理 (Outsourcing Management)
- **Source line:** 169
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 线外任务 (Offline Task)
- **Source line:** 170
- **Device [DK]:** PAD
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 缝制任务 (Sewing Task)
- **Source line:** 171
- **Domain Knowledge [DK]:** State machine: 新增缝制计划 -> 产前准备 -> 提交 -> 待缝制 -> 挂片成功 -> 缝制中 -> 缝制完成 -> 已完成. 缝制中 supports: 换款 -> 缝制暂停 -> 恢复 -> 缝制中.
- **Device [DK]:** PAD/Industrial Tablet
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels [DK]:** 产前准备, 待缝制, 缝制中, 缝制暂停, 已完成
- **Required Fields:** [GAP]

#### Page: 尾整任务 (Finishing Task)
- **Source line:** 172
- **Device [DK]:** PAD
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 生产领料 (Production Picking)

#### Page: 面料领料申请单 (Fabric Picking Request)
- **Source line:** 174
- **Domain Knowledge [DK]:** Preparation binding state machine: 未备料 -> 备料绑定 -> 已备料 -> 备料解绑 -> 未备料. Locked carriers block: 载具收货, 货载绑定, 货载解绑, 物料合载. Error: "该载具已备料，无法使用当前功能，请先备货解绑"
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels [DK]:** 未备料, 已备料
- **Required Fields:** [GAP]

#### Page: 辅料领料申请单 (Accessory Picking Request)
- **Source line:** 175
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 裁片领料申请单 (Cut Parts Picking Request)
- **Source line:** 176
- **Domain Knowledge [DK]:** Cut parts matching: 待配套 -> 配套绑定 -> 已配套 -> 配套解绑 -> 待配套
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels [DK]:** 待配套, 已配套
- **Required Fields:** [GAP]

### Menu Category: 生产过程 (Production Process)

#### Page: 裁剪完成转移单 (Cutting Completion Transfer)
- **Source line:** 178
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 成衣尾整接收 (Garment Finishing Receipt)
- **Source line:** 179
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 包码管理 (Package Code Management)
- **Source line:** 180
- **Cross-module [DK]:** Hanging -> Finishing: 缝制下线 -> Package codes -> Finishing tasks
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 包载绑定管理 (Package-Carrier Binding Management)
- **Source line:** 181
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 成品 (Finished Goods)

#### Page: 装箱明细管理 (Boxing Detail Management)
- **Source line:** 183
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 箱型管理 (Box Type Management)
- **Source line:** 184
- **Domain Knowledge [DK]:** Box type location allocation: same tray same type qty <= 1.2上限 -> 1.2货位; 1.2上限 < qty <= 1.65上限 -> 1.65货位; qty > 1.65上限 -> Block: "成品纸箱数量超过上限数"; mixed types -> always 1.65货位
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 装箱单 (Packing List)
- **Source line:** 185
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

---

## 04_仓库 (Warehouse/WMS)

Coverage: Menu structure [OK] | Fields/Buttons/Filters/Tabs [GAP] | Status labels [DK]

### Menu Category: 仓库管理 (Warehouse Management)

#### Page: 仓库管理 (Warehouse Management)
- **Source line:** 231
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 工作区列表 (Work Area List)
- **Source line:** 232
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 库区管理 (Warehouse Zone Management)

#### Page: 库区管理 (Zone Management)
- **Source line:** 234
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Top-Level Pages (No Parent Category)

#### Page: 库位管理 (Location Management)
- **Source line:** 235
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 载具管理 (Carrier Management)
- **Source line:** 236
- **Domain Knowledge [DK]:** Carrier state machine: 初始状态 -> 货载上架 -> 已上架 -> 货载下架 -> 已下架 -> 货载上架 -> 已上架 (cycle). Shelving non-initial carrier blocked. Empty carrier shelving bound carrier blocked. Query temp-zone via 货载下架 cannot be queried -- only 立库 materials visible.
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels [DK]:** 初始状态, 已上架, 已下架
- **Required Fields:** [GAP]

#### Page: 料架管理 (Rack Management)
- **Source line:** 237
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 面料仓库 (Fabric Warehouse)

#### Page: 面料货载管理 (Fabric Cargo Management)
- **Source line:** 239
- **Device [DK]:** PDA (barcode scanning)
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 面料物料清单 (Fabric BOM)
- **Source line:** 240
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 面料库存管理 (Fabric Inventory Management)
- **Source line:** 241
- **Domain Knowledge [DK]:** Formula: 可用库存 = 当前库存 - 已分配数量 - 安全库存. 80% rule: 可下单最大数量 = floor(库存数量 * 0.80). Partial outbound NOT supported for fabric.
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 面料仓出入库流水 (Fabric Warehouse In/Out Transaction Log)
- **Source line:** 242
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 面料退料回库单 (Fabric Return-to-Warehouse Order)
- **Source line:** 243
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 松布仓库 (Cloth Loosening Warehouse)

#### Page: 松布库存管理 (Cloth Loosening Inventory Management)
- **Source line:** 245
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 松布出入库流水 (Cloth Loosening In/Out Transaction Log)
- **Source line:** 246
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 辅料仓库 (Accessory Warehouse)

#### Page: 辅料物料清单 (Accessory BOM)
- **Source line:** 248
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 辅料库存管理 (Accessory Inventory Management)
- **Source line:** 249
- **Domain Knowledge [DK]:** Partial outbound SUPPORTED for accessories (unlike fabric/cut parts which are full outbound only)
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 辅料出入库流水 (Accessory In/Out Transaction Log)
- **Source line:** 250
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 裁片仓库 (Cut Parts Warehouse)

#### Page: 裁片物料清单 (Cut Parts BOM)
- **Source line:** 252
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 裁片库存管理 (Cut Parts Inventory Management)
- **Source line:** 253
- **Domain Knowledge [DK]:** Partial outbound NOT supported for cut parts (full outbound only)
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 裁片出入库流水 (Cut Parts In/Out Transaction Log)
- **Source line:** 254
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 成品仓库 (Finished Goods Warehouse)

#### Page: 成品物料清单 (Finished Goods BOM)
- **Source line:** 256
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 成品货载管理 (Finished Goods Cargo Management)
- **Source line:** 257
- **Device [DK]:** PDA
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 成品箱物流记录 (Finished Goods Box Logistics Record)
- **Source line:** 258
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 成品库存管理 (Finished Goods Inventory Management)
- **Source line:** 259
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 成品出入库流水 (Finished Goods In/Out Transaction Log)
- **Source line:** 260
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 箱出入库流水 (Box In/Out Transaction Log)
- **Source line:** 261
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 成品收货通知单 (Finished Goods Receipt Notice)
- **Source line:** 262
- **Cross-module [DK]:** Production -> WMS: Finished goods -> Receipt Notice -> Box Calling -> Unboxing -> Delivery
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 成品出库通知单 (Finished Goods Outbound Notice)
- **Source line:** 263
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 成品入库单 (Finished Goods Inbound Order)
- **Source line:** 264
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 成品出库单 (Finished Goods Outbound Order)
- **Source line:** 265
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 成品箱库存管理 (Finished Goods Box Inventory Management)
- **Source line:** 266
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 半成品仓库 (Semi-Finished Goods Warehouse)

#### Page: 半成品库存管理 (Semi-Finished Inventory Management)
- **Source line:** 268
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 半成品物料清单 (Semi-Finished BOM)
- **Source line:** 269
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 半成品出入库流水 (Semi-Finished In/Out Transaction Log)
- **Source line:** 270
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 盘点 (Inventory Counting)

#### Page: 调整单管理 (Adjustment Order Management)
- **Source line:** 272
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 盘点单管理 (Count Sheet Management)
- **Source line:** 273
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 调度 (Dispatch)

#### Page: 阶段模版配置 (Stage Template Configuration)
- **Source line:** 275
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 任务寻找策略 (Task Search Strategy)
- **Source line:** 276
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 任务模版配置 (Task Template Configuration)
- **Source line:** 277
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 任务记录 (Task Records)
- **Source line:** 278
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

### Menu Category: 开箱 (Unboxing)

#### Page: 开箱规则 (Unboxing Rules)
- **Source line:** 280
- **Domain Knowledge [DK]:** Formulas -- 订单需求箱数 = sum of box qty for given packing list + box type under receipt notice; 已叫箱数 = sum of 叫箱需求数 from all demand orders; 已派送箱数 = sum of 送货箱数; 剩余可叫箱数 = 需求箱数 - 已叫箱数; 建议叫箱数 = 包装完成数 - 已叫箱数 (if negative -> 0); 本次开箱数(default) = 叫箱数 - 已下发开箱数; 可派送数量 = 叫箱数 - 送箱数
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 开箱机配置 (Unboxing Machine Configuration)
- **Source line:** 281
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels:** [GAP]
- **Required Fields:** [GAP]

#### Page: 叫箱需求单 (Box Call Demand Order)
- **Source line:** 282
- **Domain Knowledge [DK]:** State machine: 待完成 -> 已完成 (送箱数 >= 叫箱数, or 手动完成). Depts: only 尾整工段 depts. Error: "已超额叫箱" (exceed 剩余可叫箱数 without permission). With permission: must select "超额叫箱的原因".
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels [DK]:** 待完成, 已完成
- **Required Fields:** [GAP]

#### Page: 开箱任务记录 (Unboxing Task Records)
- **Source line:** 283
- **Domain Knowledge [DK]:** State machine: 初始化 -> 下发 -> 执行中 -> 完成 -> 已完成. 初始化/执行中 -> 取消 -> 已取消. 初始化/执行中 -> 异常 -> 重试.
- **Fields:** [GAP]
- **Buttons:** [GAP]
- **Filters:** [GAP]
- **Tabs:** [GAP]
- **Status Labels [DK]:** 初始化, 执行中, 已完成, 已取消, 异常
- **Required Fields:** [GAP]

---

## Summary Statistics

| Module | Total Pages | With Domain Knowledge [DK] | Fields/Buttons/Filters/Tabs [GAP] |
|--------|------------|---------------------------|----------------------------------|
| 01_销售 | 3 | 1 (销售订单) | 3 |
| 02_采购 | 16 | 5 | 16 |
| 03_生产 | 23 | 6 | 23 |
| 04_仓库 | 35 | 9 | 35 |
| **Total** | **77** | **21** | **77** |

## Supplementation Priority (for field-level detail)

1. **销售订单** -- Highest priority. Core entity linking Sales->Production chain.
2. **生产订单** -- Core entity linking Production->Picking->WMS chain.
3. **采购订单** -- Core entity linking Purchasing->WMS chain.
4. **面料收货通知单 / 辅料收货通知单** -- Core WMS entry points.
5. **成品收货通知单 / 成品出库通知单** -- Core finished goods flow.
6. **叫箱需求单 / 开箱任务记录** -- Complex formulas and state machine.
7. **面料领料申请单 / 裁片领料申请单** -- Picking with binding/locking rules.

## Next Steps

To complete this dictionary with actual field-level detail:
- **Strategy B:** Re-examine module_texts.txt for any page detail beyond menu names (unlikely based on current file structure)
- **Strategy D:** Perform live page capture for priority pages (see list above) using browser DevTools
- **Strategy C:** Interview SMEs with the structured template from `knowledge_gap_analysis.md`
- **Cross-reference:** Check 12 official IMS documents for any page schema/field definitions

> Entries marked [INFERRED] are derived from domain knowledge, test case logic, and standard ERP patterns.
> Entries marked [CONFIRMED] are directly observed in source texts.

---

## 05. 质检模块 (Quality Control / QC)

### Module Overview

| Attribute | Value |
|-----------|-------|
| Module ID | 05 |
| Module Name (CN) | 质检 |
| Module Name (EN) | Quality Control / QC |
| Top-Level Menu | 质量管理 |
| Sub-Menu Count | 6 pages |
| Device Support | PC (config/review), PAD (shop-floor inspection), Industrial Tablet (hanging QC) |

### Menu Hierarchy

```
质量管理/
  ├── 面料质检          (Fabric QC)
  ├── 辅料质检          (Accessories QC)
  ├── 成品质检          (Finished Goods QC)
  ├── 缝制质检          (Sewing QC)
  ├── 质检管理          (QC Management)
  └── 质检配置          (QC Configuration)
```

---

### 05.01 面料质检 (Fabric QC Inspection)

[CONFIRMED] Page name from module_texts.txt. Documentation from erp_domain_knowledge.md sections 1.12, 2.2, 7.

#### List Page - Columns (Table Headers)

| Column ID | Field Name (CN) | Field Name (EN) | Type | Notes |
|-----------|-----------------|-----------------|------|-------|
| inspection_no | 检验单号 | Inspection No | text | Auto-generated |
| inspection_date | 检验日期 | Inspection Date | date | |
| supplier_code | 供应商编码 | Supplier Code | text | |
| supplier_name | 供应商名称 | Supplier Name | text | |
| material_code | 物料编码 | Material Code | text | |
| material_name | 物料名称 | Material Name | text | |
| lot_no | 批号 | Lot No | text | [INFERRED] |
| color | 颜色 | Color | text | [INFERRED] |
| quantity | 检验数量 | Inspection Qty | number | |
| yardage | 实际码数 | Actual Yardage | number | QC scoring input |
| width | 实际封度 | Actual Width | number | QC scoring input (百平方码 mode) |
| score_method | 扣分方式 | Deduction Method | select | Options: 100码, 百平方码 |
| total_deduction | 总扣分 | Total Deduction | number | Calculated |
| acceptable_score | 可接受分数 | Acceptable Score | number | Calculated via formula |
| defect_rate | 次损率 | Defect Rate | percentage | Calculated |
| result | 检验结果 | Inspection Result | status | OK / NG / 让步使用 |
| inspector | 检验员 | Inspector | text | |
| status | 状态 | Status | status | See State Machine below |

#### Form Fields (Inspection Detail / Execute)

| Field ID | Field Name (CN) | Required | Type | Notes |
|----------|-----------------|----------|------|-------|
| inspection_no | 检验单号 | Y | text | Read-only, auto-generated |
| receipt_notice_no | 收货通知单号 | Y | text | Links to procurement receipt |
| material_code | 物料编码 | Y | text | Select from received materials |
| material_name | 物料名称 | N | text | Auto-populated |
| lot_no | 批号 | Y | text | |
| color | 颜色 | Y | text | |
| inspection_qty | 检验数量 | Y | number | |
| yardage | 实际码数 | Y | number | Required for QC scoring |
| width | 实际封度 | N | number | Required for 百平方码 mode |
| score_method | 扣分方式 | Y | select | 100码 / 百平方码 |
| defect_points | 疵点记录 | N | textarea | Per-defect entry |
| deduction_per_defect | 扣分配置 | Y | number | Deduction points per defect |
| total_deduction | 总扣分 | N | number | Auto-calculated |
| acceptable_score | 可接受分数 | N | number | Auto-calculated |
| result | 检验结论 | Y | select | OK / NG / 让步使用 |

#### Filter / Search Fields

| Field | Type | Notes |
|-------|------|-------|
| 检验单号 | text | |
| 检验日期范围 | date range | |
| 供应商 | select/text | |
| 物料编码 | text | |
| 批号 | text | |
| 检验结果 | select | OK / NG / 让步使用 |
| 状态 | select | 待检验 / 检验中 / 已完成 |

#### Buttons

| Button Name (CN) | Action | Notes |
|------------------|--------|-------|
| 新建 | Create | Generate inspection sheet (auto from receipt) |
| 开始检验 | Start Inspection | Status: 待检验 -> 检验中 |
| 录入检验结果 | Enter Results | Input defect data |
| 确认检验结果 | Confirm Results | Approve OK/NG/让步使用 |
| 打印报告 | Print Report | QC report output |
| 导出 | Export | Excel/PDF export |

#### State Machine

```
待检验 (Awaiting Inspection)
  --[开始检验]--> 检验中 (Inspecting)
  --[完成检验]--> 已完成 (Completed)
  --[确认检验结果]--> result set: OK / NG / 让步使用
```

#### Status Labels

| Status | Display Text | Color/Indicator |
|--------|-------------|-----------------|
| PENDING | 待检验 | Orange/Warning |
| INSPECTING | 检验中 | Blue/Processing |
| COMPLETED | 已完成 | Green/Success |
| OK | 合格 | Green/Success |
| NG | 不合格 | Red/Error |
| CONCESSION | 让步使用 | Yellow/Warning |

#### QC Scoring Formulas [CONFIRMED from erp_domain_knowledge.md]

| Mode | Acceptable Score Formula | Defect Rate Formula |
|------|-------------------------|---------------------|
| 100码 | (实际码数 x 扣分配置) / 100 | (总扣分 x 0.25 x 100) / 实际码数 |
| 百平方码 | (实际码数 x 实际封度 x 扣分配置) / 100 / 36 | (总扣分 x 0.25 x 100 x 36) / 实际码数 / 实际封度 |

| Rule | Condition |
|------|-----------|
| 通过 (Pass) | 总扣分 <= 可接受分数 |
| 不合格 (Fail) | 总扣分 > 可接受分数 |

#### Location Differences

| Feature | Standard | Jingmen | Cambodia |
|---------|----------|---------|----------|
| Approval Granularity | Whole-order | Material+color level OK/NG/让步使用 | Not specified |
| Scoring Modes | Both | Both | Not specified |
| LOT色 | No | Yes | No |

---

### 05.02 辅料质检 (Accessories QC Inspection)

[CONFIRMED] Page name from module_texts.txt. Same QC flow as 面料质检, adapted for accessories.

#### List Page - Columns (Table Headers)

| Column ID | Field Name (CN) | Notes |
|-----------|-----------------|-------|
| inspection_no | 检验单号 | Auto-generated |
| inspection_date | 检验日期 | |
| supplier_code | 供应商编码 | |
| supplier_name | 供应商名称 | |
| material_code | 物料编码 | |
| material_name | 物料名称 | |
| lot_no | 批号 | |
| quantity | 检验数量 | |
| result | 检验结果 | OK / NG / 让步使用 |
| inspector | 检验员 | |
| status | 状态 | 待检验 / 检验中 / 已完成 |

#### Form Fields

| Field ID | Field Name (CN) | Required | Type |
|----------|-----------------|----------|------|
| inspection_no | 检验单号 | Y | text |
| receipt_notice_no | 收货通知单号 | Y | text |
| material_code | 物料编码 | Y | text |
| material_name | 物料名称 | N | text |
| lot_no | 批号 | Y | text |
| inspection_qty | 检验数量 | Y | number |
| sampling_rate | 抽检比例 | Y | number/percent |
| defect_qty | 不良数 | N | number |
| result | 检验结论 | Y | select: OK / NG / 让步使用 |
| remark | 备注 | N | textarea |

#### Filter / Search Fields

Same as 面料质检.

#### Buttons

Same as 面料质检.

---

### 05.03 成品质检 (Finished Goods QC Inspection)

[CONFIRMED] Page name from module_texts.txt. QC for finished garments.

#### List Page - Columns (Table Headers)

| Column ID | Field Name (CN) | Notes |
|-----------|-----------------|-------|
| inspection_no | 检验单号 | Auto-generated |
| inspection_date | 检验日期 | |
| production_order_no | 生产订单号 | Links to production |
| style_no | 款号 | |
| style_name | 款名 | |
| color | 颜色 | |
| size | 尺码 | |
| quantity | 检验数量 | |
| defect_qty | 不良数 | |
| defect_rate | 不良率 | Calculated |
| defect_type | 缺陷类型 | [INFERRED] |
| result | 检验结果 | OK / NG / 让步使用 |
| inspector | 检验员 | |
| status | 状态 | 待检验 / 检验中 / 已完成 |

#### Form Fields

| Field ID | Field Name (CN) | Required | Type |
|----------|-----------------|----------|------|
| inspection_no | 检验单号 | Y | text |
| production_order_no | 生产订单号 | Y | text |
| style_no | 款号 | Y | text |
| color | 颜色 | Y | text |
| size | 尺码 | Y | text |
| inspection_qty | 检验数量 | Y | number |
| defect_qty | 不良数 | N | number |
| defect_desc | 缺陷描述 | N | textarea |
| result | 检验结论 | Y | select: OK / NG / 让步使用 |
| remark | 备注 | N | textarea |

#### Filter / Search Fields

| Field | Type |
|-------|------|
| 检验单号 | text |
| 检验日期范围 | date range |
| 生产订单号 | text |
| 款号 | text |
| 检验结果 | select |
| 状态 | select |

#### Buttons

Same pattern as 05.01, plus: 标记不合格 (Mark as NG), 选择处理方式 (Select Disposition).

---

### 05.04 缝制质检 (Sewing QC Inspection)

[CONFIRMED] Page name from module_texts.txt. In-line QC during sewing process.

#### List Page - Columns (Table Headers)

| Column ID | Field Name (CN) | Notes |
|-----------|-----------------|-------|
| inspection_no | 检验单号 | |
| inspection_date | 检验日期 | |
| production_order_no | 生产订单号 | |
| sewing_line | 缝制组别 | Sewing group/line |
| process_name | 工序名称 | |
| operator | 操作工 | |
| quantity | 检验数量 | |
| defect_qty | 不良数 | |
| defect_type | 缺陷类型 | [INFERRED] |
| rework_flag | 是否返工 | Yes/No |
| result | 检验结果 | |
| inspector | 检验员 | |
| station_type | 检验站类型 | [INFERRED] 巡检/首检/尾检/二道检 |

#### Location/Version Differences

| Location | Sewing QC Type |
|----------|---------------|
| Standard | Not fully documented |
| Jingmen | Full 3-type workflow (巡检/首检/尾检) |
| Cambodia | Hanging-system QC |

---

### 05.05 质检管理 (QC Management)

[CONFIRMED] Page name from module_texts.txt. Management dashboard for all QC activities.

#### List Page - Columns (Table Headers)

| Column ID | Field Name (CN) | Notes |
|-----------|-----------------|-------|
| inspection_no | 检验单号 | Across all QC types |
| qc_type | 质检类型 | 面料/辅料/成品/缝制 |
| inspection_date | 检验日期 | |
| related_order | 关联单据 | Order/Receipt notice |
| supplier_name | 供应商 | |
| total_qty | 检验总数 | |
| pass_qty | 合格数 | |
| ng_qty | 不合格数 | |
| concession_qty | 让步接收数 | |
| pass_rate | 合格率 | Calculated |
| result | 处理结果 | |
| inspector | 检验员 | |
| status | 状态 | |

#### Filter / Search Fields

| Field | Type |
|-------|------|
| 质检类型 | select: 面料/辅料/成品/缝制 |
| 检验日期范围 | date range |
| 供应商 | select |
| 检验结果 | select |
| 检验员 | select |
| 状态 | select |

#### Buttons

| Button Name (CN) | Action |
|------------------|--------|
| 查询 | Search |
| 不合格处理 | Handle NG items |
| 导出报表 | Export report |
| 打印 | Print |

#### Tabs (if applicable)

| Tab Name | Content |
|----------|---------|
| 面料质检 | Fabric QC records |
| 辅料质检 | Accessories QC records |
| 成品质检 | Finished goods QC records |
| 缝制质检 | Sewing QC records |

---

### 05.06 质检配置 (QC Configuration)

[CONFIRMED] Page name from module_texts.txt. Configuration of QC standards and parameters.

#### Form Fields

| Field ID | Field Name (CN) | Required | Type | Notes |
|----------|-----------------|----------|------|-------|
| qc_standard | 质检标准 | Y | text | Standard name |
| qc_type | 适用质检类型 | Y | select | 面料/辅料/成品/缝制 |
| material_category | 适用物料类别 | N | select | |
| sampling_method | 抽检方式 | Y | select | Fixed rate / AQL / 全检 |
| sampling_rate | 抽检比例 | N | number | Percentage |
| aql_level | AQL等级 | N | select | [INFERRED] AQL levels |
| acceptable_defect_level | 可接受缺陷水平 | Y | number | |
| score_method | 扣分方式 | Y | select | 100码 / 百平方码 |
| deduction_config | 扣分配置 | Y | number | Points per defect type |
| defect_category | 缺陷分类 | N | textarea | Defect category definitions |
| is_active | 是否启用 | Y | boolean | Enable/Disable |

#### List Page - Columns

| Column | Notes |
|--------|-------|
| 质检标准名称 | |
| 适用类型 | |
| 抽检方式 | |
| 抽检比例 | |
| 是否启用 | |
| 创建时间 | |
| 操作 | Edit/Delete/Enable/Disable |

#### Filter / Search Fields

| Field | Type |
|-------|------|
| 质检标准名称 | text |
| 适用类型 | select |
| 是否启用 | select |

#### Buttons

| Button Name (CN) | Action |
|------------------|--------|
| 新建 | Create new QC standard |
| 编辑 | Edit QC standard |
| 删除 | Delete (with confirmation) |
| 启用/停用 | Toggle active status |

---

## 06. 物流模块 (Logistics)

### Module Overview

| Attribute | Value |
|-----------|-------|
| Module ID | 06 |
| Module Name (CN) | 物流 |
| Module Name (EN) | Logistics |
| Top-Level Menu | 收货 |
| Sub-Menu Count | 1 page |
| Coverage | Minimal - "empty shell" per knowledge gap analysis |

### Menu Hierarchy

```
收货/
  └── 半成品收货通知单    (Semi-Finished Goods Receipt Notice)
```

---

### 06.01 半成品收货通知单 (Semi-Finished Goods Receipt Notice)

[CONFIRMED] Page name from module_texts.txt. Only page in this module. Receives semi-finished goods from external processing (委外) or upstream production stages.

#### List Page - Columns (Table Headers)

| Column ID | Field Name (CN) | Field Name (EN) | Type | Notes |
|-----------|-----------------|-----------------|------|-------|
| receipt_no | 通知单号 | Notice No | text | Auto-generated |
| receipt_date | 通知日期 | Notice Date | date | |
| supplier_code | 供应商编码 | Supplier Code | text | External processor |
| supplier_name | 供应商名称 | Supplier Name | text | |
| production_order_no | 生产订单号 | Production Order No | text | |
| style_no | 款号 | Style No | text | |
| style_name | 款名 | Style Name | text | [INFERRED] |
| color | 颜色 | Color | text | [INFERRED] |
| size | 尺码 | Size | text | [INFERRED] |
| notice_qty | 通知数量 | Notice Qty | number | |
| received_qty | 已收数量 | Received Qty | number | |
| remaining_qty | 未收数量 | Remaining Qty | number | Calculated: notice_qty - received_qty |
| unit | 单位 | Unit | text | |
| status | 状态 | Status | status | See State below |
| create_time | 创建时间 | Create Time | datetime | |
| update_time | 更新时间 | Update Time | datetime | |

#### Form Fields (Create/Edit)

| Field ID | Field Name (CN) | Required | Type | Notes |
|----------|-----------------|----------|------|-------|
| receipt_no | 通知单号 | Y | text | Auto-generated |
| receipt_date | 通知日期 | Y | date | Default: today |
| supplier_code | 供应商编码 | Y | select | External processor |
| supplier_name | 供应商名称 | N | text | Auto-populated |
| production_order_no | 生产订单号 | Y | text | Links to production |
| style_no | 款号 | N | text | Auto-populated from order |
| material_code | 物料编码 | Y | text | Semi-finished material code |
| material_name | 物料名称 | N | text | Auto-populated |
| color | 颜色 | Y | text | |
| size | 尺码 | Y | text | |
| notice_qty | 通知数量 | Y | number | Must be > 0 |
| unit | 单位 | Y | select | |
| expected_arrival_date | 预计到货日期 | N | date | |
| remark | 备注 | N | textarea | |

#### Filter / Search Fields

| Field | Type | Notes |
|-------|------|-------|
| 通知单号 | text | |
| 通知日期范围 | date range | |
| 供应商 | select/text | |
| 生产订单号 | text | |
| 款号 | text | |
| 状态 | select | 待收货 / 部分收货 / 已收货 |
| 物料编码 | text | |

#### Buttons

| Button Name (CN) | Action | Notes |
|------------------|--------|-------|
| 新建 | Create | Create new receipt notice |
| 编辑 | Edit | Edit existing notice (only 待收货) |
| 删除 | Delete | With confirmation (only 待收货) |
| 确认收货 | Confirm Receipt | Triggers receipt processing |
| 查询 | Search | Filter list |
| 重置 | Reset | Clear filters |
| 导出 | Export | Export list to Excel |

#### State Machine [INFERRED from test_cases.md and ERP patterns]

```
待收货 (Awaiting Receipt)
  --[部分收货]--> 部分收货 (Partial Receipt)
  --[全部收货]--> 已收货 (Fully Received)
部分收货
  --[继续收货]--> 部分收货 (updated qty)
  --[全部收货]--> 已收货
已收货
  --[关联仓库入库]--> triggers WMS receipt
```

#### Status Labels

| Status | Display Text | Color/Indicator | Notes |
|--------|-------------|-----------------|-------|
| PENDING | 待收货 | Orange/Warning | Awaiting receipt |
| PARTIAL | 部分收货 | Blue/Processing | Partially received |
| COMPLETED | 已收货 | Green/Success | Fully received |

#### Cross-Module Integration

| From | To | Data Flow |
|------|----|-----------|
| 生产委外 | 物流.半成品收货通知单 | Outsourcing sends semi-finished goods back |
| 物流.半成品收货通知单 | 仓库.半成品入库 | Receipt triggers WMS inbound for semi-finished warehouse |

---

## 07. 报表模块 (Reports)

### Module Overview

| Attribute | Value |
|-----------|-------|
| Module ID | 07 |
| Module Name (CN) | 报表 |
| Module Name (EN) | Reports |
| Report Count | 50+ across 12 categories |
| Common Features | Date range filter, Export (Excel/PDF), Chart visualization |

### Report Categories and Sub-Categories

```
报表/
├── 委外/
│   └── 裁片外协报表
├── 缝制/
│   ├── 生产质量报表
│   └── 缝制小组产量表
├── 采购/
│   ├── 物料采购明细表
│   └── 物料收货明细表
├── 财务/
│   ├── 应收报表
│   └── 应付报表
├── 裁剪&裁片/
│   ├── 裁剪日产量报表
│   ├── 验片产量报表
│   ├── 拉布日产量表
│   ├── 裁剪日产量明细报表V2
│   ├── 裁剪日产量明细统计表
│   ├── 裁剪日产量明细表-演示2
│   ├── 裁剪日产量明细报表
│   ├── 裁剪员工实时报工表
│   ├── 裁剪床次日产量报表
│   ├── 验片日产量表
│   ├── 裁片质检报表
│   ├── 裁剪验片员工日产量报表
│   ├── 拉布员工实时报表
│   ├── 裁剪员工实时报表
│   └── 裁剪产量汇总表
├── 吊挂/
│   ├── 员工考勤报表
│   ├── 巡检站质检统计报表
│   ├── 二道检质检报表
│   ├── 首检报告汇总表
│   ├── 质检全流程明细表
│   ├── 尾检报告汇总表
│   ├── 工序产量汇总表
│   ├── 日产量报表
│   ├── 生产订单产量汇总表
│   ├── 生产质量汇总表
│   ├── 生产质量明细表
│   ├── 员工实时报工表
│   ├── 小组日质检明细表
│   ├── 车间月质检汇总表
│   ├── 款号质量统计表
│   ├── 成衣质检日报表
│   └── 专站返工日报表
├── 样衣/
│   ├── 办单全流程跟踪表
│   ├── 采购物料跟踪表
│   ├── 办单数量跟踪表
│   ├── 跟单员工作量报表
│   ├── 纸样员工工作量报表
│   ├── 样衣水洗明细表
│   └── 办房裁剪库存消耗表
├── 生产/
│   ├── 生产全流程报表
│   ├── 采购跟踪表
│   ├── 分拣统计表
│   ├── 线外员工实时报工表
│   ├── 线外工序完工表
│   ├── 线外工序完工表V2
│   ├── 水洗日产量报表
│   ├── 尾整日产量报表
│   ├── 尾整员工实时报工表
│   ├── 分拣日产量报表
│   ├── 分拣晾干明细表
│   ├── 分拣库存表
│   ├── 装箱明细表
│   └── 员工实时手工报工表
├── 裁片仓报表/
│   ├── 裁片库存层级报表
│   ├── 裁片仓上下架报表
│   ├── 裁片仓出入库报表
│   ├── 裁片仓库存报表
│   └── 裁片齐套报表
├── 面料仓报表/
│   ├── 面料质检报表
│   ├── 面料库存层级查询
│   ├── 面料仓上下架报表
│   ├── 面料仓出入库报表
│   ├── 面料仓库存报表
│   ├── 面料收货通知单报表
│   └── 面料消耗表
├── 辅料仓报表/
│   ├── 辅料库存层级查询
│   ├── 辅料仓上下架报表
│   ├── 辅料仓出入库报表
│   └── 辅料消耗表
├── 成品仓报表/
│   ├── MD to A 箱查询表
│   ├── 成品库存层级报表
│   ├── 成品仓DO库存报表
│   └── 成品仓CPO明细表
└── 其他/
    ├── 员工技能报表
    └── NPT跟进模块
```

---

### Common Filter/Search Fields (Applicable to Most Reports)

All report pages share a common filter panel pattern:

| Field | Type | Notes |
|-------|------|-------|
| 日期范围 | date range | Start date / End date, default varies by report |
| 车间/工厂 | select | Filter by workshop/factory |
| 组别 | select | Filter by group/line |
| 款号 | text | Filter by style number |
| 生产订单号 | text | Filter by production order |
| 供应商 | select | Applicable to procurement/QC reports |
| 客户 | select | Applicable to sales reports |

### Common Buttons (Applicable to Most Reports)

| Button Name (CN) | Action |
|------------------|--------|
| 查询 | Execute search with filters |
| 重置 | Reset all filters to default |
| 导出 | Export to Excel/PDF |
| 打印 | Print report |
| 刷新 | Refresh data |

### Common Columns (Recurring Across Reports)

| Column Name (CN) | Appears In |
|------------------|-----------|
| 订单号/生产订单号 | All production-related reports |
| 款号/款名 | Garment-level reports |
| 颜色/尺码 | Detail-level reports |
| 车间/组别 | Production/scheduling reports |
| 日期 | All time-series reports |
| 数量 | All quantity reports |
| 员工/操作工 | Operator productivity reports |
| 工序名称 | Process-level reports |
| 状态 | Status-tracking reports |

---

### 07.01 委外 Reports

#### 裁片外协报表 (Cut Parts Outsourcing Report)

| Attribute | Value |
|-----------|-------|
| Category | 委外 |
| Type | Tabular |
| Filters | 日期范围, 供应商, 款号, 生产订单号 |

**Columns [INFERRED from domain]:**

| Column | Notes |
|--------|-------|
| 外协单号 | Outsourcing order number |
| 供应商名称 | External processor |
| 款号 | Style number |
| 裁片名称 | Cut part name |
| 外发数量 | Quantity sent out |
| 收回数量 | Quantity returned |
| 在途数量 | In-transit quantity |
| 外发日期 | Send-out date |
| 预计收回日期 | Expected return date |
| 实际收回日期 | Actual return date |
| 状态 | 待发/外发中/已收回 |

---

### 07.02 缝制 Reports

#### 生产质量报表 (Production Quality Report)

| Attribute | Value |
|-----------|-------|
| Category | 缝制 |
| Type | Tabular + Chart |
| Filters | 日期范围, 车间, 组别, 款号 |

**Columns:**

| Column | Notes |
|--------|-------|
| 日期 | |
| 车间/组别 | |
| 款号 | |
| 总产量 | Total output |
| 合格数量 | Pass qty |
| 不合格数量 | NG qty |
| 合格率 | Pass rate % |
| 主要缺陷类型 | Top defect category |

#### 缝制小组产量表 (Sewing Group Output Table)

| Attribute | Value |
|-----------|-------|
| Category | 缝制 |
| Type | Tabular + Chart |
| Filters | 日期范围, 组别, 款号 |

**Columns:**

| Column | Notes |
|--------|-------|
| 日期 | |
| 组别 | Group/Line |
| 款号 | |
| 目标产量 | Target output |
| 实际产量 | Actual output |
| 达成率 | Achievement rate % |
| 在制品数量 | WIP qty |
| 效率 | Efficiency % |

---

### 07.03 采购 Reports

#### 物料采购明细表 (Material Purchase Detail)

| Attribute | Value |
|-----------|-------|
| Category | 采购 |
| Filters | 日期范围, 供应商, 物料类型(面料/辅料) |

**Columns:**

| Column | Notes |
|--------|-------|
| 采购订单号 | |
| 下单日期 | |
| 供应商名称 | |
| 物料编码 | |
| 物料名称 | |
| 规格 | |
| 颜色 | |
| 采购数量 | |
| 单价 | |
| 金额 | |
| 已收数量 | |
| 未收数量 | |
| 预计到货日期 | |
| 状态 | |

#### 物料收货明细表 (Material Receipt Detail)

| Attribute | Value |
|-----------|-------|
| Category | 采购 |
| Filters | 日期范围, 供应商, 物料类型 |

**Columns:**

| Column | Notes |
|--------|-------|
| 收货通知单号 | |
| 收货日期 | |
| 采购订单号 | |
| 供应商名称 | |
| 物料编码 | |
| 物料名称 | |
| 收货数量 | |
| 质检结果 | OK/NG/让步使用 |
| 入库数量 | |
| 仓库/库位 | |

---

### 07.04 财务 Reports

#### 应收报表 (Accounts Receivable)

| Attribute | Value |
|-----------|-------|
| Category | 财务 |
| Filters | 日期范围, 客户 |

**Columns:**

| Column | Notes |
|--------|-------|
| 客户名称 | |
| 销售订单号 | |
| 订单日期 | |
| 订单金额 | |
| 已收金额 | |
| 应收余额 | |
| 账期 | |
| 逾期天数 | |

#### 应付报表 (Accounts Payable)

| Attribute | Value |
|-----------|-------|
| Category | 财务 |
| Filters | 日期范围, 供应商 |

**Columns:**

| Column | Notes |
|--------|-------|
| 供应商名称 | |
| 采购订单号 | |
| 订单日期 | |
| 订单金额 | |
| 已付金额 | |
| 应付余额 | |
| 账期 | |
| 逾期天数 | |

---

### 07.05 裁剪&裁片 Reports (16 reports)

Common filters across all 裁剪 reports: 日期范围, 车间, 组别, 款号, 床次

**Recurring columns across 裁剪 reports:**

| Column | Appears In |
|--------|-----------|
| 日期 | All |
| 员工/操作工 | 员工实时/日产量 reports |
| 款号/款名 | All |
| 床次 | 裁剪床次 reports |
| 拉布层数 | 拉布 reports |
| 裁剪数量 | 裁剪 reports |
| 验片数量 | 验片 reports |
| 合格/不合格 | QC reports |
| 工序 | Process-level reports |
| 报工时间 | Real-time report reports |
| 产量 | All output reports |
| 效率 | Performance reports |

---

### 07.06 吊挂 Reports (17 reports)

Common filters: 日期范围, 车间, 吊挂线/组别, 款号

**Key report-specific columns:**

| Report | Key Columns |
|--------|------------|
| 员工考勤报表 | 员工, 日期, 上班时间, 下班时间, 工时, 考勤状态 |
| 巡检站质检统计报表 | 巡检站, 日期, 检验数, 合格数, 不合格数, 合格率 |
| 二道检质检报表 | 二道检站, 日期, 检验数, NG数, 返工数 |
| 首检报告汇总表 | 款号, 首检日期, 首检结果, 问题描述 |
| 质检全流程明细表 | 订单号, 款号, 工序, 巡检/首检/尾检结果, 缺陷描述 |
| 尾检报告汇总表 | 款号, 尾检日期, 检验数, NG数, 合格率 |
| 工序产量汇总表 | 工序名称, 日期, 计划产量, 实际产量, 达成率 |
| 日产量报表 | 日期, 组别, 款号, 目标, 实际, 达成率 |
| 生产订单产量汇总表 | 订单号, 款号, 总产量, 完成率 |
| 生产质量汇总表 | 日期, 组别, 合格数, NG数, 合格率 |
| 生产质量明细表 | 日期, 组别, 款号, 工序, 缺陷类型, 数量 |
| 员工实时报工表 | 员工, 工序, 开始时间, 结束时间, 产量, 效率 |
| 小组日质检明细表 | 日期, 组别, 款号, 检验类型, 检验数, 合格数, NG数 |
| 车间月质检汇总表 | 月份, 车间, 检验总数, 合格数, NG数, 合格率 |
| 款号质量统计表 | 款号, 总检验数, 合格数, NG数, 合格率, 主要缺陷 |
| 成衣质检日报表 | 日期, 款号, 检验数, 合格数, NG数, 缺陷类型 |
| 专站返工日报表 | 日期, 站别, 返工数, 返工原因, 返工率 |

---

### 07.07 样衣 Reports (7 reports)

Common filters: 日期范围, 样衣编号/办单号, 跟单员

**Key report-specific columns:**

| Report | Key Columns |
|--------|------------|
| 办单全流程跟踪表 | 办单号, 款号, 当前状态, 开始日期, 各节点完成日期, 负责人 |
| 采购物料跟踪表 | 办单号, 物料编码, 物料名称, 采购数量, 已到数量, 预计到货日期, 状态 |
| 办单数量跟踪表 | 办单号, 款号, 计划数量, 已完成数量, 在制数量 |
| 跟单员工作量报表 | 跟单员, 负责办单数, 进行中, 已完成, 逾期数 |
| 纸样员工工作量报表 | 纸样员, 款号数, 完成数, 进行中 |
| 样衣水洗明细表 | 办单号, 款号, 水洗类型, 水洗日期, 结果 |
| 办房裁剪库存消耗表 | 物料编码, 物料名称, 期初库存, 消耗量, 期末库存 |

---

### 07.08 生产 Reports (14 reports)

Common filters: 日期范围, 车间, 组别, 款号, 生产订单号

**Key report-specific columns:**

| Report | Key Columns |
|--------|------------|
| 生产全流程报表 | 订单号, 款号, 裁剪状态, 缝制状态, 尾整状态, 当前工序, 完成率 |
| 采购跟踪表 | 订单号, 物料编码, 采购状态, 到货状态, 预计到货日期 |
| 分拣统计表 | 日期, 分拣组, 分拣数量, 合格数, NG数 |
| 线外员工实时报工表 | 员工, 工序, 开始时间, 结束时间, 产量 |
| 线外工序完工表 | 订单号, 工序名称, 计划数量, 完成数量, 完成日期 |
| 线外工序完工表V2 | Same as above, enhanced version |
| 水洗日产量报表 | 日期, 水洗类型, 数量, 合格数 |
| 尾整日产量报表 | 日期, 尾整组, 款号, 产量 |
| 尾整员工实时报工表 | 员工, 工序, 开始时间, 产量 |
| 分拣日产量报表 | 日期, 分拣组, 产量 |
| 分拣晾干明细表 | 日期, 款号, 数量, 晾干状态 |
| 分拣库存表 | 款号, 分拣库存数量, 库位 |
| 装箱明细表 | 装箱单号, 款号, 箱号, 颜色, 尺码, 数量, 总箱数 |
| 员工实时手工报工表 | 员工, 工序, 手工报工数量, 报工时间 |

---

### 07.09 裁片仓报表 (5 reports)

| Report | Key Columns |
|--------|------------|
| 裁片库存层级报表 | 仓库, 库区, 库位, 款号, 裁片名称, 库存数量 |
| 裁片仓上下架报表 | 日期, 裁片, 上架数量, 下架数量, 操作人, 载具号 |
| 裁片仓出入库报表 | 日期, 单据号, 裁片, 入库数量, 出库数量, 结存 |
| 裁片仓库存报表 | 裁片编码, 裁片名称, 款号, 库存数量, 可用数量, 已分配数量 |
| 裁片齐套报表 | 款号, 订单号, 所需裁片数, 已齐套数, 缺失裁片, 齐套率 |

---

### 07.10 面料仓报表 (7 reports)

| Report | Key Columns |
|--------|------------|
| 面料质检报表 | 检验单号, 物料编码, 供应商, 检验结果, 合格率 |
| 面料库存层级查询 | 仓库, 库区, 库位, 物料编码, 批号, 库存数量 |
| 面料仓上下架报表 | 日期, 物料, 载具号, 上架/下架数量, 操作人 |
| 面料仓出入库报表 | 日期, 单据号, 物料, 入库数量, 出库数量, 结存 |
| 面料仓库存报表 | 物料编码, 物料名称, 批号, 颜色, 库存数量, 可用数量 |
| 面料收货通知单报表 | 通知单号, 供应商, 物料, 通知数量, 已收数量 |
| 面料消耗表 | 物料编码, 款号, 订单号, 消耗数量, 日期 |

---

### 07.11 辅料仓报表 (4 reports)

| Report | Key Columns |
|--------|------------|
| 辅料库存层级查询 | 仓库, 库区, 库位, 物料编码, 库存数量 |
| 辅料仓上下架报表 | 日期, 物料, 载具号, 上架/下架数量 |
| 辅料仓出入库报表 | 日期, 单据号, 物料, 入库/出库数量, 结存 |
| 辅料消耗表 | 物料编码, 款号, 订单号, 消耗数量 |

---

### 07.12 成品仓报表 (4 reports)

| Report | Key Columns |
|--------|------------|
| MD to A 箱查询表 | 箱号, MD箱号, A箱号, 款号, 颜色, 尺码, 数量 |
| 成品库存层级报表 | 仓库, 库区, 库位, 款号, 箱号, 库存数量 |
| 成品仓DO库存报表 | DO单号, 款号, 箱号, 库存数量 |
| 成品仓CPO明细表 | CPO单号, 款号, 颜色, 尺码, 数量, 箱数 |

---

### 07.13 其他 Reports (2 reports)

| Report | Key Columns |
|--------|------------|
| 员工技能报表 | 员工姓名, 工号, 技能类型, 技能等级, 认证日期, 有效期 |
| NPT跟进模块 | 订单号, 款号, NPT目标, 实际NPT, 偏差, 责任人 |

---

## 08. 数据模块 (Master Data)

### Module Overview

| Attribute | Value |
|-----------|-------|
| Module ID | 08 |
| Module Name (CN) | 数据 |
| Module Name (EN) | Master Data |
| Top-Level Categories | 档案 (Archives), 技术 (Technical) |
| Sub-Menu Count | 18 pages |
| Primary Function | CRUD for all foundational/master data entities |

### Menu Hierarchy

```
├── 档案/
│   ├── 基础工序管理      (Basic Process Management)
│   ├── 外购品管理        (Purchased Item Management)
│   ├── 基础面料          (Basic Fabric)
│   ├── 基础辅料          (Basic Accessories)
│   ├── 供应商            (Suppliers)
│   ├── 客户              (Customers)
│   ├── 品牌              (Brands)
│   ├── 工厂日历          (Factory Calendar)
│   ├── 作息安排          (Work Schedule)
│   ├── 港口管理          (Port Management)
│   ├── 单位转换          (Unit Conversion)
│   ├── 基础制程          (Basic Routing/Process Chain)
│   ├── 送货工厂管理      (Delivery Factory Management)
│   ├── 尺码管理          (Size Management)
│   └── 报工系数配置      (Work Reporting Coefficient Config)
└── 技术/
    ├── 款号管理          (Style Management)
    ├── 模板管理          (Template Management)
    └── 工艺要求          (Process Requirements)
```

---

### Common Master Data Page Pattern

All master data pages follow the standard CRUD pattern:

**List Page Columns:** ID/编码, 名称, 状态/启用标识, 创建时间, 更新时间, 操作

**Form Fields:** Entity-specific fields (see below)

**Common Filter/Search Fields:** 编码, 名称, 状态

**Common Buttons:** 新建, 编辑, 删除, 查询, 重置, 导出, 导入

---

### 08.01 基础工序管理 (Basic Process Management)

Manages standard manufacturing operations/processes.

#### List Page - Columns

| Column | Type | Notes |
|--------|------|-------|
| 工序编码 | text | Process code |
| 工序名称 | text | Process name |
| 工序类型 | select | [INFERRED] 裁剪/缝制/尾整/水洗/质检 |
| 标准工时(SAM) | number | Standard Allowed Minutes |
| 工种 | select | [INFERRED] Job category |
| 适用车间 | select | Applicable workshop |
| 是否启用 | boolean | Active/Inactive |
| 创建时间 | datetime | |
| 操作 | actions | Edit/Delete |

#### Form Fields

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| 工序编码 | Y | text | Unique |
| 工序名称 | Y | text | |
| 工序类型 | Y | select | 裁剪/缝制/尾整/水洗/质检 |
| 标准工时(SAM) | N | number | Minutes |
| 工种 | N | select | |
| 适用车间 | N | select | |
| 备注 | N | textarea | |
| 是否启用 | Y | boolean | Default: true |

---

### 08.02 外购品管理 (Purchased Item Management)

Manages externally purchased items that are not fabric/accessories.

#### List Page - Columns

| Column | Type |
|--------|------|
| 外购品编码 | text |
| 外购品名称 | text |
| 规格 | text |
| 单位 | text |
| 供应商 | select |
| 是否启用 | boolean |
| 创建时间 | datetime |
| 操作 | Edit/Delete |

#### Form Fields

| Field | Required | Type |
|-------|----------|------|
| 外购品编码 | Y | text |
| 外购品名称 | Y | text |
| 规格 | N | text |
| 单位 | Y | select |
| 供应商 | N | select |
| 备注 | N | textarea |

---

### 08.03 基础面料 (Basic Fabric)

Manages fabric master data. Used as the base for purchasing and inventory.

#### List Page - Columns

| Column | Type | Notes |
|--------|------|-------|
| 面料编码 | text | Unique fabric code |
| 面料名称 | text | Fabric name |
| 规格/门幅 | text | Width specification [INFERRED] |
| 成分 | text | Composition [INFERRED] |
| 重量/克重 | text | Weight [INFERRED] |
| 颜色列表 | text | Associated colors [INFERRED] |
| 默认单位 | text | |
| 供应商 | select | |
| 是否启用 | boolean | |
| 创建时间 | datetime | |
| 操作 | actions | Edit/Delete |

#### Form Fields

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| 面料编码 | Y | text | Unique, alphanumeric |
| 面料名称 | Y | text | |
| 规格/门幅 | N | text | Width in cm/inch |
| 成分 | N | text | e.g., 100% Cotton |
| 克重 | N | text | GSM or oz |
| 颜色 | N | text/multi | Color list |
| 默认单位 | Y | select | 米/码/公斤 |
| 默认供应商 | N | select | |
| 备注 | N | textarea | |

---

### 08.04 基础辅料 (Basic Accessories)

Manages accessories/trims (buttons, zippers, labels, etc.).

#### List Page - Columns

Same structure as 08.03 基础面料, with 辅料编码/辅料名称.

#### Form Fields

| Field | Required | Type |
|-------|----------|------|
| 辅料编码 | Y | text |
| 辅料名称 | Y | text |
| 辅料类型 | Y | select [INFERRED]: 拉链/纽扣/标签/线/衬/其他 |
| 规格 | N | text |
| 颜色 | N | text |
| 默认单位 | Y | select: 个/套/米/卷 |
| 默认供应商 | N | select |
| 备注 | N | textarea |

---

### 08.05 供应商 (Supplier Management)

Manages supplier/vendor master data.

#### List Page - Columns

| Column | Type | Notes |
|--------|------|-------|
| 供应商编码 | text | Unique supplier code |
| 供应商名称 | text | Supplier name |
| 供应商类型 | select | [INFERRED] 面料/辅料/外购品/综合 |
| 联系人 | text | Contact person |
| 联系电话 | text | Phone number |
| 地址 | text | Address |
| 结算币种 | select | [INFERRED] CNY/USD/etc |
| 付款条件 | text | Payment terms [INFERRED] |
| 是否启用 | boolean | Active/Inactive |
| 创建时间 | datetime | |
| 操作 | actions | Edit/Delete |

#### Form Fields

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| 供应商编码 | Y | text | Unique |
| 供应商名称 | Y | text | |
| 供应商类型 | Y | select | |
| 联系人 | N | text | |
| 联系电话 | N | text | |
| 邮箱 | N | text | Email |
| 地址 | N | textarea | |
| 结算币种 | N | select | |
| 付款条件 | N | text | |
| 备注 | N | textarea | |

#### Validation [INFERRED from test_cases.md TC-DAT-013]

| Rule | Error Message |
|------|--------------|
| Duplicate supplier code | 编码重复，不允许保存 |
| Supplier name empty | 供应商名称为必填 |

---

### 08.06 客户 (Customer Management)

Manages customer/buyer master data.

#### List Page - Columns

| Column | Type |
|--------|------|
| 客户编码 | text |
| 客户名称 | text |
| 客户类型 | select [INFERRED]: 品牌商/代理商/其他 |
| 品牌 | select (from 08.07) |
| 联系人 | text |
| 联系电话 | text |
| 地址 | text |
| 是否启用 | boolean |
| 创建时间 | datetime |
| 操作 | Edit/Delete |

#### Form Fields

| Field | Required | Type |
|-------|----------|------|
| 客户编码 | Y | text |
| 客户名称 | Y | text |
| 客户类型 | N | select |
| 品牌 | N | select |
| 联系人 | N | text |
| 联系电话 | N | text |
| 邮箱 | N | text |
| 地址 | N | textarea |
| 备注 | N | textarea |

---

### 08.07 品牌 (Brand Management)

Manages brand master data.

#### List Page - Columns

| Column | Type |
|--------|------|
| 品牌编码 | text |
| 品牌名称 | text |
| 所属客户 | select |
| 是否启用 | boolean |
| 创建时间 | datetime |
| 操作 | Edit/Delete |

#### Form Fields

| Field | Required | Type |
|-------|----------|------|
| 品牌编码 | Y | text |
| 品牌名称 | Y | text |
| 所属客户 | N | select |
| 备注 | N | textarea |

---

### 08.08 工厂日历 (Factory Calendar)

Manages factory working/non-working day calendar.

#### List Page - Columns

| Column | Type |
|--------|------|
| 日期 | date |
| 日期类型 | select: 工作日/休息日/节假日 |
| 班次 | select [INFERRED]: 白班/夜班/全天 |
| 备注 | text |

#### Form Fields

| Field | Required | Type |
|-------|----------|------|
| 日期范围 | Y | date range |
| 日期类型 | Y | select: 工作日/休息日/节假日 |
| 班次 | N | select |
| 备注 | N | text |

#### Buttons

| Button | Action |
|--------|--------|
| 批量设置 | Batch set date range |
| 导入 | Import calendar |
| 导出 | Export calendar |

---

### 08.09 作息安排 (Work Schedule)

Manages shift/work hour schedules.

#### List Page - Columns

| Column | Type |
|--------|------|
| 作息名称 | text |
| 班次 | select |
| 上班时间 | time |
| 下班时间 | time |
| 休息开始 | time |
| 休息结束 | time |
| 有效工时 | number (hours) |
| 是否启用 | boolean |
| 操作 | Edit/Delete |

#### Form Fields

| Field | Required | Type |
|-------|----------|------|
| 作息名称 | Y | text |
| 班次 | Y | select |
| 上班时间 | Y | time |
| 下班时间 | Y | time |
| 休息开始 | N | time |
| 休息结束 | N | time |
| 有效工时 | N | number |

---

### 08.10 港口管理 (Port Management)

Manages port/shipping destination data.

#### List Page - Columns

| Column | Type |
|--------|------|
| 港口编码 | text |
| 港口名称 | text |
| 国家/地区 | text [INFERRED] |
| 是否启用 | boolean |
| 操作 | Edit/Delete |

#### Form Fields

| Field | Required | Type |
|-------|----------|------|
| 港口编码 | Y | text |
| 港口名称 | Y | text |
| 国家/地区 | N | text |
| 备注 | N | textarea |

---

### 08.11 单位转换 (Unit Conversion)

Manages unit conversion rates between measurement units.

#### List Page - Columns

| Column | Type |
|--------|------|
| 源单位 | text |
| 目标单位 | text |
| 转换系数 | number |
| 适用物料类型 | select [INFERRED] |
| 是否启用 | boolean |
| 操作 | Edit/Delete |

#### Form Fields

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| 源单位 | Y | select | 米/码/公斤/磅/个/套/卷 |
| 目标单位 | Y | select | |
| 转换系数 | Y | number | Multiplication factor |
| 适用物料类型 | N | select | |
| 备注 | N | textarea | |

---

### 08.12 基础制程 (Basic Routing/Process Chain)

Manages standard routing/process chains for garment manufacturing.

#### List Page - Columns

| Column | Type |
|--------|------|
| 制程编码 | text |
| 制程名称 | text |
| 适用款型 | select [INFERRED] |
| 工序数量 | number |
| 总标准工时 | number |
| 是否启用 | boolean |
| 操作 | Edit/Delete |

#### Form Fields

| Field | Required | Type |
|-------|----------|------|
| 制程编码 | Y | text |
| 制程名称 | Y | text |
| 适用款型 | N | select |
| 工序列表 | Y | multi-select table (select from 08.01) |
| 工序顺序 | Y | number (auto from order) |
| 标准工时 | N | number |
| 备注 | N | textarea |

---

### 08.13 送货工厂管理 (Delivery Factory Management)

Manages delivery destination factories.

#### List Page - Columns

| Column | Type |
|--------|------|
| 工厂编码 | text |
| 工厂名称 | text |
| 地址 | text |
| 联系人 | text |
| 联系电话 | text |
| 是否启用 | boolean |
| 操作 | Edit/Delete |

---

### 08.14 尺码管理 (Size Management)

Manages size groups and individual size definitions.

#### List Page - Columns

| Column | Type |
|--------|------|
| 尺码组编码 | text |
| 尺码组名称 | text |
| 尺码列表 | text (e.g., S/M/L/XL) |
| 是否启用 | boolean |
| 创建时间 | datetime |
| 操作 | Edit/Delete |

#### Form Fields

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| 尺码组编码 | Y | text | e.g., SZ-GROUP-001 |
| 尺码组名称 | Y | text | e.g., Standard, Asian |
| 尺码明细 | Y | multi-row | |

**尺码明细 sub-table:**

| Column | Required | Type |
|--------|----------|------|
| 尺码编码 | Y | text (S/M/L/XL/XXL) |
| 尺码名称 | Y | text |
| 排序 | Y | number |
| 尺码参考值 | N | text | [INFERRED] e.g., chest/bust measurement |

---

### 08.15 报工系数配置 (Work Reporting Coefficient Config)

Manages coefficients used for adjusting work reporting calculations.

#### List Page - Columns

| Column | Type |
|--------|------|
| 系数编码 | text |
| 系数名称 | text |
| 适用工序/工种 | select |
| 系数值 | number |
| 适用条件 | text |
| 是否启用 | boolean |
| 操作 | Edit/Delete |

#### Form Fields

| Field | Required | Type |
|-------|----------|------|
| 系数编码 | Y | text |
| 系数名称 | Y | text |
| 适用工序 | N | select (from 08.01) |
| 适用工种 | N | select |
| 系数值 | Y | number (default: 1.0) |
| 适用条件 | N | textarea |
| 备注 | N | textarea |

---

### 08.16 款号管理 (Style Management)

[Technical category] Manages garment style/master definitions. Core entity linked to BOM and production.

#### List Page - Columns

| Column | Type | Notes |
|--------|------|-------|
| 款号 | text | Style number, unique |
| 款名 | text | Style name |
| 品牌 | select | From 08.07 |
| 客户 | select | From 08.06 |
| 尺码组 | select | From 08.14 |
| 制程 | select | From 08.12 |
| 产品类型 | select | [INFERRED] 上装/下装/连衣裙/外套 |
| 是否启用 | boolean | |
| 创建时间 | datetime | |
| 操作 | Edit/Delete |

#### Form Fields

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| 款号 | Y | text | Unique style identifier |
| 款名 | Y | text | Style name |
| 品牌 | Y | select | |
| 客户 | Y | select | |
| 尺码组 | Y | select | Size range |
| 制程 | Y | select | Routing/process chain |
| 产品类型 | N | select | |
| 产品图片 | N | file/image | Upload [INFERRED] |
| 工艺要求 | N | select | From 08.18 |
| BOM物料清单 | N | sub-table | Bill of materials [INFERRED] |
| 备注 | N | textarea | |

#### Validation [INFERRED from test_cases.md TC-DAT-014]

| Rule | Error Message |
|------|--------------|
| Invalid style code format | 编码格式不正确 |
| Duplicate style code | 款号已存在 |
| Missing required field | 款号为必填 / 款名为必填 |

---

### 08.17 模板管理 (Template Management)

[Technical category] Manages document/excel templates used for import/export and reporting.

#### List Page - Columns

| Column | Type |
|--------|------|
| 模板编码 | text |
| 模板名称 | text |
| 模板类型 | select [INFERRED]: 导入/导出/打印 |
| 适用模块 | select |
| 文件名 | text |
| 上传时间 | datetime |
| 上传人 | text |
| 是否启用 | boolean |
| 操作 | Download/Edit/Delete |

#### Form Fields

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| 模板编码 | Y | text | |
| 模板名称 | Y | text | |
| 模板类型 | Y | select | 导入模板/导出模板/打印模板 |
| 适用模块 | Y | select | Module scope |
| 模板文件 | Y | file | Upload .xlsx/.docx |
| 备注 | N | textarea | |

---

### 08.18 工艺要求 (Process Requirements)

[Technical category] Manages process requirement specifications for styles.

#### List Page - Columns

| Column | Type |
|--------|------|
| 工艺编码 | text |
| 工艺名称 | text |
| 适用产品类型 | select |
| 工艺描述 | text |
| 标准工时 | number |
| 所需设备 | text [INFERRED] |
| 是否启用 | boolean |
| 创建时间 | datetime |
| 操作 | Edit/Delete |

#### Form Fields

| Field | Required | Type |
|-------|----------|------|
| 工艺编码 | Y | text |
| 工艺名称 | Y | text |
| 适用产品类型 | N | select |
| 工艺描述 | Y | textarea |
| 标准工时 | N | number |
| 所需设备/工具 | N | text |
| 注意事项 | N | textarea |
| 附件 | N | file [INFERRED] |
| 备注 | N | textarea |

---

## 09. 吊挂模块 (Hanging System)

### Module Overview

| Attribute | Value |
|-----------|-------|
| Module ID | 09 |
| Module Name (CN) | 吊挂 |
| Module Name (EN) | Hanging System |
| Top-Level Categories | 吊挂, 分拣 |
| Sub-Menu Count | 4 pages |
| Device Support | PC (config), Industrial Tablet (station operations) |
| Coverage | 90% per knowledge gap analysis |

### Menu Hierarchy

```
├── 吊挂/
│   ├── 流水线配置          (Production Line Configuration)
│   └── 吊挂扫码终端配置    (Hanging Scanner Terminal Configuration)
└── 分拣/
    ├── 分拣MES配置         (Sorting MES Configuration)
    └── 分拣下位配置        (Sorting Lower-Level Configuration)
```

### Domain Knowledge [CONFIRMED from erp_domain_knowledge.md]

| Rule | Details |
|------|---------|
| 产量工序 | Must designate at least one process as 产量工序, otherwise prevented |
| 过站工序不回流 | When checked, hangers skip already-passed processes |
| 返工原因 | Each reworked process must have a reason recorded |
| QC返工率 | Recorded on rework STATION, not inspection station |
| 缝制任务状态 | 新增缝制计划 → 产前准备 → 待缝制 → 缝制中 → 已完成 |
| 换款 | 缝制中 → 换款 → 缝制暂停 → 恢复 → 缝制中 |
| 第一工序 | Must be 挂片站 (Piece Hanging Station) |

---

### 09.01 流水线配置 (Production Line Configuration)

[CONFIRMED] Page name from module_texts.txt. Configures hanging production lines.

#### List Page - Columns

| Column ID | Field Name (CN) | Type | Notes |
|-----------|-----------------|------|-------|
| line_code | 流水线编码 | text | Unique line identifier |
| line_name | 流水线名称 | text | |
| workshop | 所属车间 | select | |
| line_type | 线体类型 | select | [INFERRED] 主吊挂线/分拣线/返工线 |
| station_count | 站位数 | number | Number of stations |
| current_style | 当前款号 | text | Active style on line |
| status | 状态 | status | 空闲/运行中/暂停/维护 |
| is_enabled | 是否启用 | boolean | |
| create_time | 创建时间 | datetime | |
| 操作 | Actions | | Edit/Delete/Preview |

#### Form Fields (Create/Edit)

| Field ID | Field Name (CN) | Required | Type | Notes |
|----------|-----------------|----------|------|-------|
| line_code | 流水线编码 | Y | text | Unique |
| line_name | 流水线名称 | Y | text | |
| workshop | 所属车间 | Y | select | |
| line_type | 线体类型 | Y | select | |
| station_list | 站点配置 | Y | sub-table | Station configuration |

**Station Configuration Sub-Table:**

| Column | Required | Type | Notes |
|--------|----------|------|-------|
| 站点序号 | Y | number | Order in line |
| 站点名称 | Y | text | Station name |
| 站点类型 | Y | select | 挂片站/普通站/全能工站/质检站/产量站 |
| 绑定工序 | N | select | From 基础工序管理 |
| 是否产量工序 | Y | boolean | [From domain rule] At least one required |
| 过站不回流 | N | boolean | Skip already-passed processes |
| 工位数量 | N | number | Seats per station |
| IP地址 | N | text | Terminal IP [INFERRED] |
| 端口 | N | number | Terminal port [INFERRED] |

#### Filter / Search Fields

| Field | Type |
|-------|------|
| 流水线编码 | text |
| 流水线名称 | text |
| 所属车间 | select |
| 线体类型 | select |
| 状态 | select |

#### Buttons

| Button Name (CN) | Action |
|------------------|--------|
| 新建 | Create new line |
| 编辑 | Edit line config |
| 删除 | Delete (with confirmation) |
| 复制 | Copy existing line config [INFERRED] |
| 预览 | Preview line layout |
| 启用/停用 | Toggle active status |

#### Status Labels

| Status | Display Text | Notes |
|--------|-------------|-------|
| IDLE | 空闲 | Line available, no style assigned |
| RUNNING | 运行中 | Active production |
| PAUSED | 暂停 | Style change or maintenance |
| MAINTENANCE | 维护 | Under maintenance |

---

### 09.02 吊挂扫码终端配置 (Hanging Scanner Terminal Configuration)

[CONFIRMED] Page name from module_texts.txt. Configures barcode/RFID scanner terminals at hanging stations.

#### List Page - Columns

| Column ID | Field Name (CN) | Type | Notes |
|-----------|-----------------|------|-------|
| terminal_code | 终端编码 | text | |
| terminal_name | 终端名称 | text | |
| line_code | 所属流水线 | select | From 09.01 |
| station | 所属站点 | select | |
| terminal_type | 终端类型 | select | [INFERRED] 扫码枪/平板/工业平板 |
| ip_address | IP地址 | text | |
| port | 端口 | number | |
| is_connected | 连接状态 | status | 已连接/未连接 |
| is_enabled | 是否启用 | boolean | |
| 操作 | Actions | | Edit/Delete/Test Connection |

#### Form Fields

| Field ID | Field Name (CN) | Required | Type |
|----------|-----------------|----------|------|
| terminal_code | 终端编码 | Y | text |
| terminal_name | 终端名称 | Y | text |
| line_code | 所属流水线 | Y | select |
| station | 所属站点 | Y | select (filtered by line) |
| terminal_type | 终端类型 | Y | select |
| ip_address | IP地址 | Y | text |
| port | 端口 | N | number |
| mac_address | MAC地址 | N | text [INFERRED] |
| remark | 备注 | N | textarea |

#### Buttons

| Button Name (CN) | Action |
|------------------|--------|
| 新建 | Create |
| 编辑 | Edit |
| 删除 | Delete |
| 测试连接 | Test Connection |
| 批量导入 | Batch Import [INFERRED] |

---

### 09.03 分拣MES配置 (Sorting MES Configuration)

[CONFIRMED] Page name from module_texts.txt. Configures MES-level sorting rules and parameters.

#### List Page - Columns

| Column ID | Field Name (CN) | Type | Notes |
|-----------|-----------------|------|-------|
| config_code | 配置编码 | text | |
| config_name | 配置名称 | text | |
| sorting_type | 分拣类型 | select | [INFERRED] 按款号/按颜色/按尺码/按箱号 |
| applicable_line | 适用流水线 | select | |
| priority | 优先级 | number | |
| is_enabled | 是否启用 | boolean | |
| create_time | 创建时间 | datetime | |
| 操作 | Actions | | Edit/Delete |

#### Form Fields

| Field ID | Field Name (CN) | Required | Type |
|----------|-----------------|----------|------|
| config_code | 配置编码 | Y | text |
| config_name | 配置名称 | Y | text |
| sorting_type | 分拣类型 | Y | select |
| sorting_rule | 分拣规则 | Y | textarea [INFERRED] |
| applicable_line | 适用流水线 | Y | select (multi) |
| priority | 优先级 | N | number |
| destination_rules | 下位规则 | N | sub-table |
| remark | 备注 | N | textarea |

#### Filter / Search Fields

| Field | Type |
|-------|------|
| 配置编码 | text |
| 配置名称 | text |
| 分拣类型 | select |
| 适用流水线 | select |
| 是否启用 | select |

#### Buttons

| Button Name (CN) | Action |
|------------------|--------|
| 新建 | Create |
| 编辑 | Edit |
| 删除 | Delete |
| 复制 | Copy config |

---

### 09.04 分拣下位配置 (Sorting Lower-Level Configuration)

[CONFIRMED] Page name from module_texts.txt. Configures the destination/output routing for sorted items.

#### List Page - Columns

| Column ID | Field Name (CN) | Type | Notes |
|-----------|-----------------|------|-------|
| config_code | 配置编码 | text | |
| config_name | 配置名称 | text | |
| sorting_config | 关联分拣配置 | select | From 09.03 |
| destination_type | 下位类型 | select | [INFERRED] 包装站/装箱站/存储区 |
| destination_name | 下位名称 | text | |
| capacity | 容量上限 | number | |
| current_load | 当前负载 | number | |
| is_enabled | 是否启用 | boolean | |
| 操作 | Actions | | Edit/Delete |

#### Form Fields

| Field ID | Field Name (CN) | Required | Type |
|----------|-----------------|----------|------|
| config_code | 配置编码 | Y | text |
| config_name | 配置名称 | Y | text |
| sorting_config | 关联分拣配置 | Y | select |
| destination_type | 下位类型 | Y | select |
| destination_name | 下位名称 | Y | text |
| capacity | 容量上限 | N | number |
| overflow_rule | 溢出规则 | N | select [INFERRED] |
| remark | 备注 | N | textarea |

#### Buttons

| Button Name (CN) | Action |
|------------------|--------|
| 新建 | Create |
| 编辑 | Edit |
| 删除 | Delete |
| 重置计数 | Reset counter [INFERRED] |

---

## Cross-Module Integration Points (Modules 05-09)

| Source Module | Source Page | Target Module | Target Page | Data Flow |
|---------------|-------------|---------------|-------------|-----------|
| 采购 | 物料收货 | 质检.面料质检 | 面料质检 | Receipt triggers QC inspection |
| 采购 | 物料收货 | 质检.辅料质检 | 辅料质检 | Receipt triggers QC inspection |
| 质检 | 质检管理 | 仓库 | 库存管理 | QC result updates stock quality status |
| 生产 | 委外管理 | 物流.收货 | 半成品收货通知单 | Outsourcing creates receipt notice |
| 物流 | 半成品收货通知单 | 仓库 | 半成品仓库 | Receipt triggers WMS inbound |
| 生产 | 缝制任务 | 吊挂.吊挂 | 流水线配置 | Task uses hanging lines |
| 吊挂 | 流水线配置 | 生产 | 车间预排程 | Line config affects scheduling |
| 数据 | 基础面料 | 采购 | 采购订单 | Fabric master used in PO |
| 数据 | 基础辅料 | 采购 | 采购订单 | Accessories master used in PO |
| 数据 | 供应商 | 采购 | 采购订单 | Supplier used in PO |
| 数据 | 客户 | 销售 | 销售订单 | Customer used in SO |
| 报表 | All reports | All modules | All pages | Reports aggregate data from all modules |

---

## Appendix: Common UI Patterns (Modules 05-09)

### Standard List Page Pattern

```
[筛选区] - Collapsible filter bar
  [字段1] [字段2] [...] [查询] [重置]
[操作区]
  [新建] [批量删除] [导入] [导出]
[表格区] - Ant Design Table
  [列1] [列2] [...] [状态列(with badges)] [操作列(编辑/删除/查看)]
[分页区] - Ant Design Pagination
  共 X 条 | 10/20/50/100 条/页 | 第 1 页
```

### Standard Form Page Pattern

```
[面包屑] 首页 > 模块 > 页面名称
[表单区] - Ant Design Form
  [Section 1: 基本信息]
    [字段*] label: field-name
    [字段]  label: field-name
  [Section 2: 明细信息]
    [子表格 / 动态行]
[底部]
  [保存] [保存并新建] [取消]
```

### Confirmation Dialog Pattern

```
[Modal]
  Title: 提示 / 确认操作
  Body: 确认要[操作]该[实体]吗？
  Footer: [确定] [取消]
```

### Status Badge Color Convention

| Status Category | Color | Examples |
|-----------------|-------|----------|
| 草稿/待处理 | Orange | 待检验, 待收货, 待缝制 |
| 进行中 | Blue | 检验中, 部分收货, 缝制中 |
| 已完成/正常 | Green | 已完成, 已收货, 合格, 已启用 |
| 异常/拒绝 | Red | 不合格, 已停用, 异常 |
| 警告/让步 | Yellow | 让步使用, 超额 |
