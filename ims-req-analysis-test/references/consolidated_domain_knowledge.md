# IMS ERP Consolidated Knowledge

> Merged from: live system capture (2026-07-01), module_texts static dump (2026-06-30), official docs (12 documents), implicit rule analysis
> Convention: `[LIVE]` = confirmed via live system capture; `[STATIC]` = from module_texts.txt navigation text only; `[DOC]` = from official IMS documents

---

## Quick Reference

### Top 6 State Machines (most test-critical)

| # | State Machine | Module | Key Risk |
|---|--------------|--------|----------|
| 1 | **Production Order**: 草稿→审核中→生效→已发布→完成 | 生产 | Most transitions; hard rollback (反发布→反生效) |
| 2 | **Sales Order**: 草稿→生效→中止→生效 (cycle) | 销售 | Drives all downstream; split creates children |
| 3 | **Sewing Task**: 新增→产前准备→待缝制→缝制中→已完成 | 生产 | Real-time hanging system; 换款→暂停→恢复 |
| 4 | **WMS Material**: 待收货→已收货→已入库→出库扣减 | 仓库 | PDA-driven; 面料/裁片 partial outbound NOT supported |
| 5 | **Purchase Order**: 草稿→生效→确认到货 (locks receipt) | 采购 | 确认到货 locks downstream; only 草稿 deletable |
| 6 | **Sorting Hanger Lifecycle**: 上架扫描→路由中→库区等待→下架执行→下架扫描→(空衣架回流/包装) | 吊挂 | Hardware-driven; 7 scenarios; 4异常触发条件 |

### Top 10 Validation Rules

| # | Rule | Module |
|---|------|--------|
| 1 | 已发布生产订单不可直接编辑; 必须 反发布→反生效 | 生产 |
| 2 | 已备料载具/物料锁定: 阻止收货、绑定、解绑、合载 | 仓库 |
| 3 | 已收货物料不可重复收货、不可删除 (仅待收货可删) | 仓库 |
| 4 | 叫箱数超过剩余可叫箱数 → "已超额叫箱" (除非有权限+选原因) | 仓库 |
| 5 | 面料/裁片不支持部分出库 (辅料支持) | 仓库 |
| 6 | 质检: 总扣分 > 可接受分数 = 不合格 | 质检 |
| 7 | 挂片站必须是生产订单首工序 | 生产 |
| 8 | 缺失BOM无法计算物料需求 | 生产 |
| 9 | 缝制产线必须指定产量工序, 否则阻止上线 | 吊挂 |
| 10 | 箱型货位: 同盘同型数量>1.65上限 → 阻止 | 仓库 |

### Additional Sorting System Rules [DOC]

| # | Rule | Trigger |
|---|------|---------|
| S1 | 1个存储杆同时只1个任务 | 并发冲突 |
| S2 | 1个分拣区域同时只1个存储杆执行 | 并发冲突 |
| S3 | 子任务超时10min → 重试(默认无限次) | 超时 |
| S4 | 未绑定加工方案/方案下线 → 送入异常站 | 路由失败 |
| S5 | 目标满站 → 回源站转圈 | 路由失败 |
| S6 | 库区有空→按维度分配; 无空→混色混码进最少杆 | 分配逻辑 |

### Top 5 Error Messages

| # | Error Message | Trigger Condition |
|---|--------------|-------------------|
| 1 | "该载具已备料，无法使用当前功能，请先备货解绑" | 操作已备料载具 |
| 2 | "该载具存在其他领料单的物料" | 载具含不同领料单物料 |
| 3 | "已超额叫箱" | 叫箱数超过剩余可叫箱数 |
| 4 | "无效的物料条码，请确保面料在库存内" | 扫描不在库存中的条码 |
| 5 | "成品纸箱数量超过上限数" | 同盘同型箱数 > 1.65上限 |

### Sorting System Error Scenarios [DOC]

| # | Scenario | Result |
|---|----------|--------|
| E1 | 未绑定加工方案 | 送入异常站下架口, 人工处理 |
| E2 | 加工方案已下线 | 送入异常站下架口, 人工处理 |
| E3 | 未绑定下架任务 | 送入异常站下架口, 人工处理 |
| E4 | 目标满站 | 回源站转圈 |
| E5 | 子任务超时(>10min) | 自动重试(默认无限次) |
| E6 | 干燥房满 | 降级一级(TBD) |

---

## Module-by-Module

### Sidebar: All Modules

14 modules in sidebar, each as `gm.模块名#N`. The `#N` is a role tier (not session counter):
Tier 1: 样衣,销售,仓库,质检,物流,报表,数据,吊挂,平板,人事,看板,系统
Tier 2: 采购
Tier 3: 生产 (highest, likely elevated permissions) [STATIC]

Navigation: All 14 roles visible in every module sidebar. `/` separator divides module menu from `gm.首页#2` + notification area. Global notifications: 签证到期提醒, 护照到期提醒 (badge capped at `99+`). [STATIC]

---

### 01 - 销售 (Sales) `gm.销售#1`

**Menu** [LIVE: 3 items, STATIC hierarchy]:
```
订单/
  └── 销售订单
排期/
  ├── 订单预排期
  └── 订单排期表
```

**State Machine** [DOC]:
```
草稿 --[生效]--> 生效 --[中止]--> 中止 --[反中止]--> 生效
生效 --[反生效]--> 草稿
生效 --[变更]--> modify ETA/warehouse date
生效 --[拆分]--> creates Draft child orders (split by color/size qty)
```

**Business Rules**:
- Order first, then scheduling. Two-level scheduling: 预排期 (draft) → 排期表 (final). [STATIC]
- No visible sales return/refund, change/cancel, or pricing pages. These may be inline operations. [STATIC]

**Cross-module**: Sales Order → Material Requirements (采购) + Production Order (生产)

---

### 02 - 采购 (Purchasing) `gm.采购#2`

**Menu** [LIVE: 17 items, STATIC hierarchy]:
```
需求/
  ├── 物料需求审核
  ├── 按单物料需求
  ├── 备货面料需求通知单
  └── 备货辅料需求通知单  [LIVE captured: F:4 C:21]
订单/
  ├── 采购计划
  ├── 采购订单
  ├── 面料采购计划
  ├── 辅料采购计划
  ├── 面料采购订单
  ├── 辅料采购订单
  └── 现金采购订单
收货/
  ├── 面料收货通知单
  ├── 辅料收货通知单
  ├── 面料其他收货通知单
  └── 面料期初收货通知单
退货/
  ├── 面料退货通知单
  └── 辅料退货通知单
```

**State Machines** [DOC]:

Material Requirements:
```
草稿 --[提交审核]--> 审核中 --[审核通过]--> available for PO
审核中 --[撤回送审]--> 草稿
审核通过 --[反审核]--> editable (only if no PO created yet)
```

Purchase Order:
```
草稿 --[生效]--> 生效 --[确认到货]--> locks receipt notices
草稿 --[删除]--> only in 草稿
```

**Captured Page: 备货辅料需求通知单** [LIVE]
Fields: 物料需求通知单号(text), 供应商(search), 客户(search), 口岸(search)
Key columns: 状态, 版本号, 供应商, 客户, 预计离港日期, 口岸, 销售订单号, 款号, 辅料编号, 需求数, 总需求数
Statuses: 生效, 审核中, 草稿 | Buttons: 查询, 更多筛选, 辅料新增, 重置, 编辑

**Business Rules**:
- Demand-driven: 需求→订单→收货→退货. 物料需求审核 is FIRST gate. [STATIC]
- Fabric and accessory SPLIT: separate plans, orders, receipts, returns. Never mixed. [STATIC]
- 现金采购订单 bypasses planning phase (no 现金采购计划). [STATIC]
- Fabric has extra receipt types (其他收货, 期初收货). 辅料 does not. [STATIC]

**Cross-module**: Production material demand → 采购; Purchase Order → WMS receipt → Inventory

---

### 03 - 生产 (Production) `gm.生产#3`

**Menu** [STATIC: 29 pages, no live capture for this module]:
```
排程/
  ├── 车间预排程, 组别预排程, 生产排程表, 排程计划表
  ├── 组别日产量负荷表, 组别周产量负荷表
  ├── 缝制日目标, 缝制日目标达成表, 吊挂目标设置
订单/
  ├── 生产订单, 生产订单审核, 洗水订单, CPO明细表
任务/
  ├── 松布任务, 裁剪任务, 委外管理, 线外任务, 缝制任务, 尾整任务
生产领料/
  ├── 面料领料申请单, 辅料领料申请单, 裁片领料申请单
生产过程/
  ├── 裁剪完成转移单, 成衣尾整接收, 包码管理, 包载绑定管理
成品/
  ├── 装箱明细管理, 箱型管理, 装箱单
```

**State Machines** [DOC]:

Production Order:
```
草稿 --[提交审核]--> 审核中 --[通过]--> back to edit flow
                --[驳回]--> editing
草稿 --[生效]--> 生效 --[发布]--> 已发布
已发布 --[反发布]--> 生效 --[反生效]--> 草稿
已发布 --[完成]--> 完成
已发布 --[发起领料]--> 领料流程
```
Key: Only editable in 草稿. To edit 已发布: must 反发布 → 反生效.

Sewing Task:
```
新增缝制计划 --> 产前准备 --[提交]--> 待缝制 --[挂片成功]--> 缝制中
缝制中 --[换款]--> 缝制暂停 --[恢复]--> 缝制中
缝制中 --[缝制完成]--> 已完成
```

**Business Rules**:
- Physical sequence: 松布→裁剪→缝制→尾整 matches real garment flow. [STATIC]
- Two-level scheduling: 车间 (coarse) → 组别 (detailed). Load tracked per group. [STATIC]
- 生产订单审核 is a separate gate before task generation. [STATIC]
- 洗水订单 is a distinct order type with separate workflow. [STATIC]
- Picking requests material-type-specific: 面料/辅料/裁片 each own form. [STATIC]
- 线外任务 = offline/manual operations parallel to hanging line. [STATIC]
- 裁剪完成转移单: formal transfer trigger to next stage. [STATIC]
- Packaging hierarchy: 装箱明细→箱型管理→装箱单. [STATIC]

**Validation** [DOC]:
- Edit 已发布 order directly → blocked; must 反发布→反生效 first
- Add process to order with hung pieces → must append to end
- Go online without 普通站/全能工站 → validation rejects
- First process must be 挂片站
- Missing style name → cutting tasks cannot generate 扎卡 tags
- Missing BOM → cannot calculate material requirements

**Cross-module**: Sales BOM → Production Order → Material calculation; Production Order → Picking (WMS)

---

### 04 - 仓库 (Warehouse) `gm.仓库#1`

**Menu** [LIVE: 43 items, STATIC hierarchy]:
```
仓库管理/
  ├── 仓库管理, 工作区列表, 库区管理, 库位管理, 载具管理, 料架管理
面料仓库/
  ├── 面料货载管理, 面料物料清单, 面料库存管理, 面料仓出入库流水, 面料退料回库单
松布仓库/
  ├── 松布库存管理, 松布出入库流水
辅料仓库/
  ├── 辅料物料清单, 辅料库存管理, 辅料出入库流水
裁片仓库/
  ├── 裁片物料清单, 裁片库存管理, 裁片出入库流水
成品仓库/
  ├── 成品物料清单, 成品货载管理, 成品箱物流记录, 成品库存管理
  ├── 成品出入库流水, 箱出入库流水
  ├── 成品收货通知单, 成品出库通知单, 成品入库单, 成品出库单, 成品箱库存管理
半成品仓库/
  ├── 半成品库存管理, 半成品物料清单, 半成品出入库流水
盘点/
  ├── 调整单管理, 盘点单管理
调度/
  ├── 阶段模版配置, 任务寻找策略, 任务模版配置, 任务记录
开箱/
  ├── 开箱规则, 开箱机配置, 叫箱需求单, 开箱任务记录
```

**State Machines** [DOC]:
- **WMS Material**: 待收货→已收货(临时库区)→已入库(立库库区)→出库扣减. Partial outbound: only 辅料 (面料/裁片: full only).
- **WMS Carrier**: 初始⇄已上架⇄已下架 (cycle via 货载上架/下架).
- **备料**: 未备料⇄已备料. Locking: 已备料 blocks 载具收货/货载绑定/解绑/物料合载.
- **裁片配套**: 待配套⇄已配套 (绑定/解绑).
- **开箱任务**: 初始化→执行中→已完成 (cancel→已取消 from 初始化/执行中; 异常→重试).
- **叫箱需求单**: 待完成→已完成 (送箱数>=叫箱数 or 手动完成).

**Formulas** [DOC]:
- 可用库存 = 当前库存 - 已分配数量 - 安全库存; 可下单最大数量 = floor(库存数量 x 0.80)
- Unboxing: 剩余可叫箱数 = 需求箱数 - 已叫箱数; 建议叫箱数 = 包装完成数 - 已叫箱数 (neg→0)
- Box Type Allocation: same tray same type: <=1.2上限→1.2货位, 1.2-1.65上限→1.65货位, >1.65上限→**Block**; mixed types→always 1.65货位

**Validation & Errors** [DOC]:
- Duplicate receipt / delete received material → block (only 待收货 deletable)
- Shelve non-initial carrier / empty carrier shelving bound carrier → block
- 已备料载具: "该载具已备料，无法使用当前功能，请先备货解绑"
- Wrong picking order: "该载具存在其他领料单的物料" / "该载具存在未解绑、未备料的物料"
- Invalid barcode: "无效的物料条码，请确保面料在库存内"
- 超额叫箱: "已超额叫箱" (unless permission + reason); 叫箱仅限尾整工段
- 箱数超限: "成品纸箱数量超过上限数"

**Business Rules**:
- Six segregated inventory types. 松布 is SEPARATE from 面料 (post-relaxing fabric). [STATIC]
- Feature richness: 成品仓库(11) > 面料仓库(5) > 辅料/裁片/半成品(3) > 松布(2). [STATIC]
- 面料退料回库单: fabric-only return-to-warehouse flow. [STATIC]
- 调整单 (direct adjustment) vs 盘点单 (formal count) are distinct processes. [STATIC]
- Dispatch uses template-based config (阶段模版, 任务模版). [STATIC]
- 开箱 workflow: 规则→机配置→叫箱需求→任务记录. [STATIC]

---

### 05 - 质检 (Quality) `gm.质检#1`

**Menu** [LIVE: 5 items, STATIC hierarchy]:
```
质量管理/
  ├── 面料质检, 辅料质检, 成品质检, 缝制质检
质检配置/    (global QC config)
```

**State Machine** [DOC]:
```
待检验 --[开始检验]--> 检验中 --[完成]--> 已完成
Approval: 确认检验结果 (OK/NG/让步使用 — varies by location)
```

**Formulas** [DOC]:
- 100码: 可接受分数 = (实际码数 x 扣分配置) / 100
- 百平方码: 可接受分数 = (实际码数 x 实际封度 x 扣分配置) / 100 / 36
- 次损率100码: (总扣分 x 0.25 x 100) / 实际码数
- 次损率百平方码: (总扣分 x 0.25 x 100 x 36) / 实际码数 / 实际封度
- 通过: 总扣分 <= 可接受分数. 不合格: 总扣分 > 可接受分数

**Business Rules**:
- Four inspection types, unified config. 质检配置 is global, not per-type. [STATIC]
- QC scope mapping: 面料质检→面料/松布仓, 辅料质检→辅料仓, 成品质检→成品仓, 缝制质检→in-process. [STATIC]
- QC is a gate at multiple points: receiving QC, in-process QC, final QC. [DOC]

---

### 06 - 物流 (Logistics) `gm.物流#1`

**Menu** [LIVE: 1 item]:
```
收货/
  └── 半成品收货通知单
```

**Business Rules**: Thin shell module. Real logistics happens in 成品仓库 (shipping) and 生产模块 (inter-stage transfer). 半成品收货通知单 suggests external semi-finished goods receipt. [STATIC]

---

### 07 - 报表 (Reports) `gm.报表#1`

**Menu** [LIVE: 81 items, STATIC hierarchy/categories]:
14 categories. Highest density: 生产(15), 裁剪&裁片(14), 吊挂(14).

**Captured Pages** [LIVE]:

**物料采购明细表** [F:3 C:38] Fields: 采购订单号, 币种, 仓位
Key cols: 采购订单号, 供应商, 物料编号, 物料名称, 款号, 采购数量, 单价, 总金额, 到货数量, 差异数

**物料收货明细表** [F:4 C:40] Fields: 收货通知单号, 供应商, 物料编号, 供应商物料编码
Key cols: 收货通知单号, 供应商, 物料编号, 实际收货数量, 到货日期, 采购订单号, 销售订单号, 差异数

**裁剪日产量报表** [F:4 C:21] Fields: 拉布开始时间, 销售订单号, 生产订单号, 裁剪任务单号
Key cols: 款号, 裁剪任务单号, 成衣色号/尺码, 部门/组别, 床次, 计划件数, 裁剪件数, 合格件数, 裁成率

All: Buttons 导出/透视/查询/更多筛选/重置. Badge: 99+, 0.

**Business Rules**: Reports organized by business domain, not technical module. Finance reports minimal (AR+AP only) -- suggesting external finance system (金蝶/用友). [STATIC]

---

### 08 - 数据 (Master Data) `gm.数据#1`

**Menu** [LIVE: 17 items, STATIC hierarchy]:
```
档案/
  ├── 基础工序管理, 外购品管理, 基础面料, 基础辅料
  ├── 供应商, 客户, 品牌, 工厂日历, 作息安排
  ├── 港口管理, 单位转换, 基础制程, 送货工厂管理, 尺码管理, 报工系数配置
技术/
  ├── 款号管理, 工艺要求
```

Note: Live system has 17 (no 模板管理, no duplicate 基础辅料). [LIVE authoritative]

**Business Rules**:
- Split: 档案 (operational reference) vs 技术 (product/process engineering). [STATIC]
- 基础工序管理 is FIRST entry -- process definitions are most fundamental master data. [STATIC]
- 工厂日历, 作息安排, 港口管理 are site-specific (multi-factory = different values). [STATIC]
- Hierarchy: 款号(WHAT) → 模板(HOW to cut) → 工艺要求(HOW to sew/finish). [STATIC]
- 报工系数配置: work-reporting coefficient for piece-rate calculation. [STATIC]

---

### 09 - 吊挂 (Hanging System) `gm.吊挂#1`

**Menu** [STATIC, no live capture]:
```
吊挂/
  ├── 流水线配置, 吊挂扫码终端配置
分拣/
  ├── 分拣MES配置, 分拣下位配置
```

**Validation** [DOC]:
- No 产量工序 designated → prevented; must select one
- 过站工序不回流: checked = hangers skip already-passed processes
- Rework without reason → each reworked process must have reason
- QC rework rate recorded on rework STATION, not inspection station

**Business Rules**: Line config (topology) vs terminal config (station hardware) are separate concerns. Sorting MES-integrated. [STATIC]

---

#### 09-A - 分拣系统 (Sorting System) [DOC: 分拣系统业务逻辑梳理.docx]

##### 硬件定义 (7种)

| 硬件 | 编码 | 逻辑含义 | 说明 |
|------|------|---------|------|
| 分流阀 | Vxxx | = 入站站位 | 存储区前物理分流点，进站入口 |
| 上架口 | Rxxx | 上架入口 | 衣服首次进入系统的操作口 |
| 下架口 | Pxxx | 下架出口 | 衣服离开存储系统的操作口 |
| 支轨 | Bxxx | 分支轨道 | 连接主线与库区的分支路径 |
| 库区 | Cx'x'x | = 出站站位 | 存储/缓存区域，分一级(混合)、二级(SKU精准) |
| 电动线 | Sxxx | 一条道 | 单通道主线传输 |
| 分拣线 | Sxxx | 多条岔路口 | 多分支主轨道 |

##### 整体业务流程

```
上架(选SKU) → 分流阀入站 → 库区入口[扫描衣架条码→确认入库] → 库区杆等待
→ 下架呼叫 → 衣架出库 → 下架口[扫描衣架条码→确认出库] → 包装 → 空衣架回流
```

**上架分流**:
- 自动绑定上架: 荆门/凯奥尼
- 手动绑定上架: 新基/安吉纳
- 分流阀判断三路: 插单款(跳过缓存) / 需干燥(去干燥房) / 正常(进入分配)
- 干燥房: 有空→静置计时(全局/方案) | 满→降级一级(TBD)

**库区分配层级**:
- 缓存杆(锁定SKU) → 一级库区(混合, 有空按维度分配, 无空混色混码) → 二级库区(SKU精准, 承接让道)

**下架呼叫**:
- 优先级: ①转圈 > ②二级 > ③一级
- 父任务拆子任务
- 子任务超时10min, 重试默认无数次
- 约束: 1个存储杆同时只1个任务; 1个分拣区域同时只1个存储杆执行

**空衣架回收**: 少的进→满站也进, 无视衣架状态

**异常路由**: 缺绑定方案/方案下线 → 异常站; 目标满站 → 回源站转圈

##### 七大业务场景

| # | 场景 | 路径 | 关键验证点 |
|---|------|------|-----------|
| 1 | 正常路径 | 上架→一级库区→下架→空衣架回流 | 库区分配逻辑, 衣架条码扫描确认 |
| 2 | 干燥房路径(荆门) | 上架→分流阀→干燥房(跳过一级)→静置计时→下架 | 干燥房满→降级一级; 静置计时全局vs方案 |
| 3 | 缓存杆路径 | 上架→缓存杆(锁定SKU)→等正式下架→出站 | SKU锁定, 暂不出库 |
| 4 | 插单款快速通道 | 新: 跳过缓存杆→快速通道→优先出库; 旧: 标记"需优先出"→下次呼叫优先 | 新旧插单款不同处理路径 |
| 5 | 空衣架回流 | 取衣→空衣架回轨道→入站→分配空衣架下架口 | 满站也进, 无视衣架状态 |
| 6 | 同款让道 | 一级库区→让道→重新入站→二级库区(满则回流一级) | 让道衣架路径正确性 |
| 7 | 异常站路由 | 无法确定目标→异常站下架口→人工处理 | 触发: 未绑定方案/方案下线/未绑定任务/目标满站 |

##### 关键业务规则

| 规则ID | 规则 | 类型 |
|--------|------|------|
| SORT-01 | 1个存储杆同时只1个任务 | 并发约束 |
| SORT-02 | 1个分拣区域同时只1个存储杆执行 | 并发约束 |
| SORT-03 | 子任务超时10min，重试默认无数次 | 超时策略 |
| SORT-04 | 下架优先级: 转圈 > 二级 > 一级 | 优先级 |
| SORT-05 | 库区有空→按维度(SKU/分色分码); 无空→混色混码进最少杆 | 分配策略 |
| SORT-06 | 上架必须扫描衣架条码+确认入库 | 确认点 |
| SORT-07 | 下架必须扫描衣架条码+确认出库 | 确认点 |
| SORT-08 | 未绑定加工方案/方案下线→异常站 | 异常路由 |
| SORT-09 | 目标满站→回源站转圈 | 异常路由 |
| SORT-10 | 空衣架回收站: 少的进→满站也进, 无视衣架状态 | 回收策略 |

##### 异常触发条件

| 触发条件 | 结果 |
|---------|------|
| 未绑定加工方案 | 送入异常站下架口, 人工处理 |
| 加工方案已下线 | 送入异常站下架口, 人工处理 |
| 未绑定下架任务 | 送入异常站下架口, 人工处理 |
| 目标满站 | 回源站转圈(非异常站) |
| 子任务超时(>10min) | 重试(默认无限次) |
| 上架口容量满 | 阻止继续上架 |
| 短时间批量上架 | 系统压力测试点 |

##### 客户差异

| 客户 | 上架方式 | 特殊流程 | 备注 |
|------|---------|---------|------|
| 荆门 | 自动绑定 | 干燥房路径, 静置计时 | |
| 安吉纳 | 手动绑定 | **独立任务状态机, 后整菜单, 站位调度** | 详见下方安吉纳专节 |
| 新基 | 手动绑定 | 剪线区/新查区, 全流程未走通 | |
| 凯奥尼 | 自动绑定 | - | |
| 医美 | - | 过隧道机(待梳理) | |

##### 安吉纳分拣系统（基于用户手册）[DOC: 安吉纳分拣系统用户手册.docx]

安吉纳分拣系统与主线有大量结构性差异，核心在于采用 **PC管理配置 + PAD现场操作** 双层架构。

**关键差异摘要**:
- **菜单**: PAD端使用"后整"菜单（非"吊挂"），PC端多一个"分拣系统基础配置"页面
- **任务模型**: 独立状态机（产前准备→待分拣→分拣中），无父/子任务拆分，无超时重试
- **下架触发**: 下架位操作员直接呼叫（非包装站装箱清单触发）
- **硬件**: 无干燥房、缓存杆、支轨(Bxxx)；有回流杆（一级库区让道分流）
- **独有功能**: 站位管理（启用/禁用/清除/校准）、产线控制（批量开关）、衣架更换、人工站位调度、物流记录/异常日志/操作日志
- **一级库区**: 同色同款存放，同款不足混款；包装触发送快速通道到包装位
- **二级库区**: 包装下架优先选择
- **未实现**: 干燥房、缓存杆、插单款、异常站、并发约束、加工方案检测

**安吉纳独有PAD功能页面**:

| 页面 | 菜单位置 | 功能 |
|------|---------|------|
| 分拣任务 | 后整 > 分拣管理 | 创建分拣任务(从缝制任务单)、编辑站位分配、上线/发布/开始分拣 |
| 产线控制 | 后整 > 分拣管理 | 单线开关 + 批量全部开启/关闭 |
| 站位管理 | 后整 > 分拣管理 | 查看站位容量、启用/禁用站位、清除站内/在途衣架、校准 |
| 衣架路径 | 后整 > 分拣管理 | 查询衣架路径+事件、关联缝制路径、衣架更换 |
| 包装位详情 | 后整 > 分拣管理 | 查看下架任务(已取消/分拣中/已结束)、同步站位 |
| 上架位 | 后整 > 上架位 | 选生产订单+SKU→按提升按钮→扫码绑定，日产量+1 |
| 下架位 | 后整 > 下架位 | 选SKU→填调货数量→呼叫，可呼叫数过滤，自动刷新 |
| 分拣线(物流记录) | 调试 > 分拣线 | 多维查询衣架流转过程 |
| 分拣线(站位调度) | 调试 > 分拣线 | 点对点调度: 上架位→库区/下架位, 库区→库区/下架位 |
| 分拣线(异常日志) | 调试 > 分拣线 | 异常衣架日志 |
| 分拣线(操作日志) | 调试 > 分拣线 | 用户操作审计 |

**安吉纳分拣任务状态机**:
```
新增任务 → 产前准备 → [上线] → [发布] → 待分拣 → [开始分拣] → 分拣中
```
注意: "保存"仅存配置不生效，"上线"才生效。

**安吉纳站位调度状态机**:
```
新增 → 保存 → 初始化 → [启动] → 进行中 → [完成] → 已完成
```

**安吉纳未实现的主线功能**:
干燥房路径、缓存杆路径、插单款快速通道、异常站路由、父/子任务拆分、10min超时/无限重试、存储杆/分拣区域并发约束、加工方案绑定检测、下架扫描确认出库。

> 详细差异参考: `feature_sorting_system.md` 第14节

##### 设备集成点

| 设备 | 编码 | 集成方式 | 人机交互 | 安吉纳 |
|------|------|---------|---------|--------|
| 上架口终端 | Rxxx | 工业平板 + 扫码枪/RFID | 选SKU, 扫描确认入库 | PAD平板 + 分拣条码枪, 需按物理提升按钮 |
| 下架口终端 | Pxxx | 工业平板 + 扫码枪/RFID | 扫描确认出库 | PAD平板, 无强制扫描确认出库 |
| 分流阀 | Vxxx | PLC控制 | 自动分流 | 存在，路由逻辑简化 |
| 库区杆位 | Cxxx | 传感器 | 自动检测占用 | 称"储存杆" |
| 电动/分拣线 | Sxxx | 电机控制 | 自动传输 | 统称"分拣线"，不区分单/多分支 |
| 回流杆 | - | - | - | **安吉纳特有**: 一级库区让道分流 |
| 高速摄像头 | - | 视觉系统 | 重算(待确认) | 安吉纳未提及 |
| 隧道机 | - | - | 安吉纳/医美(待确认) | **安吉纳手册未提及** |

##### 待确认项 (TBD)

| 编号 | 内容 | 优先级 | 状态 |
|------|------|--------|------|
| TBD-01 | 干燥房满"降级一级"具体策略 | 高 | 待确认（仅荆门适用） |
| TBD-02 | 干燥房静置计时: 全局vs方案区别 | 高 | 待确认（仅荆门适用） |
| TBD-03 | 高速摄像头重算逻辑 | 中 | 待确认（安吉纳未提及） |
| TBD-04 | 隧道机流程(安吉纳/医美) | 中 | **安吉纳手册未提及隧道机**，医美仍待确认 |
| TBD-05 | 新基上架到下架完整流程 | 高 | 待确认 |
| TBD-06 | 各客户调度策略差异详情 | 高 | **安吉纳已梳理**（见上方安吉纳专节）；荆门/新基/凯奥尼待补充 |

> 详细参考: `feature_sorting_system.md`

---

### 10 - 人事 (HR) `gm.人事#1`

**Menu** [LIVE: 19 items]:
员工档案, 工资预支, 在职月工资, 请假登记, 回工登记, 考勤登记, 日考勤统计, 月考勤统计, 小组出勤表, 员工缺勤表, 月考勤统计表, 计件登记, 日计件统计, 月计件统计, 班次设置, 假类设置, 节假日设置, 工资汇率设置, 工资项设置

**Business Rules**: [STATIC inferred]
- Employee ID: 6-digit numeric (100xxx-108xxx observed, 8000+ employees). 100xxx = Chinese-named staff; 101xxx-108xxx = Khmer-named workers.
- Visa/Passport expiry alerts are global notifications appearing in all modules.
- Timestamp format: `YYYY/MM/DD HH:MM:SS`. Document dates: `YYYY/MM/DD`.

---

### 11 - 系统 (System) `gm.系统#1`

**Menu** [LIVE: 18 items]:
部门管理, 角色, 用户, 数据字典, 菜单分配, 多语言配置, 页面配置管理, 系统配置, 导入导出模版, 全局配置, 文件解析配置, 系统权限配置, 系统权限控制规则, 工作站配置, 模版管理, 通知管理, 打印模板管理, 操作日志

---

### 12 - 平板 (Tablet) `gm.平板#1`

**Menu** [LIVE: 1 item]:
缝制管理（PAD）

---

### 13 - 看板 (Dashboard) `gm.看板#1`

No capture data. [No data available]

---

### 14 - 样衣 (Sample) `gm.样衣#1`

No capture data. 7 dedicated reports in 报表 module indicate significant business area. [STATIC inferred]

---

## Appendix

### A. Full Cross-Module Flow Map

```
数据(主数据)
  │
  ▼
销售 ──→ 采购 ──→ 仓库/WMS ──→ 生产/MES ──→ 质检
                  │    ↑           │    ↑        │
                  │    └──领料─────┘    │        │
                  │                    │        │
                  └──→ 物流 ←──成品出库─┘        │
                         │                      │
                    吊挂系统                      │
                    ├─ 缝制执行                  │
                    └─ 分拣系统                  │
                       ├─ 上架(←WMS成品入库)     │
                       ├─ 库区存储               │
                       ├─ 下架呼叫(←生产包装站)   │
                       ├─ 出库→成品仓库           │
                       └─ 空衣架回流             │
                         │                      │
                    报表(跨所有模块读取)←─────────┘
```

Key chains:
1. Sales Order BOM → Production Order → Material calculation
2. Production Order → Material Demand → Demand Review → Purchase Plan → Purchase Order
3. Purchase Order → Receipt Notice → Material Receipt → Inventory
4. Published PO → Picking Request → (if 松布=是) → Cloth Loosening
5. Completed Receipt → Auto-generate Inspection Sheet → QC Results
6. Finished goods → Receipt Notice → Box Calling → Unboxing → Delivery
7. RFID-bound cut pieces → Carrier routing → Sewing line entry
8. 缝制下线 → Package codes → Finishing tasks
9. PMS <-> IMS: Receipt notices, box types sync
10. ERP <-> IMS: Orders, plans, BOM, inventory, progress bidirectional sync
11. 分拣系统: 生产包装站下发装箱清单 → 分拣下架呼叫 → 衣架出库 → 成品 → 空衣架回流上架位

### B. Version/Location Differences

| Feature | Standard | Jingmen (荆门) | Cambodia (新基) |
|---------|----------|---------------|-----------------|
| QC Approval | Whole-order | Material+color level OK/NG/让步使用 | Not specified |
| LOT色 | No | Yes | No |
| 辅料收货模式 | All 3 modes | 先录后贴 | 无箱贴 |
| 缝制质检 | Not detailed | Full 3-type workflow | Hanging-system QC |

### C. ID Conventions & Encoding

| ID Type | Pattern | Example | Notes |
|---------|---------|---------|-------|
| Employee ID | 6-digit numeric | 100072 | 100xxx=Chinese, 101xxx+ =Khmer |
| Material/Style context | `ML` + 3-4 digits | ML863 | Appears in breadcrumbs across all modules |
| Module role | `gm.模块名#N` | gm.生产#3 | N = role tier (1=operator, 2=approver, 3=elevated) |
| Page-level ID | `gm.页面名#N` | gm.裁剪日产量明细统计表#2 | Rare; only observed in 报表 module |
| Timestamp | `YYYY/MM/DD HH:MM:SS` | 2026/06/30 08:00:13 | 24-hour clock |
| Document date | `YYYY/MM/DD` | 2025/12/05 | Date only, no time |

### D. Test Scenario Patterns

1. **Status gating**: Test valid path AND all invalid status attempts for every operation.
2. **Dual confirmation**: Deletes/submissions require second confirm. Test confirm AND cancel.
3. **Permission boundaries**: Save != Publish. Test visibility per role tier (#1/#2/#3).
4. **FIFO ordering**: Allocation follows creation time. Test with varying insertion orders.
5. **Partial vs Full**: 辅料 partial outbound supported; 面料/裁片 not.
6. **Locking**: Prepared/matched items locked from other operations. Test locked+unlocked.
7. **Formula boundaries**: Test at exact thresholds (1.2上限, 1.65上限, 0, negative, overflow).
8. **Multi-terminal**: Same operation may differ on PC/PAD/PDA/Tablet.
9. **Cross-module sync**: Data should appear downstream within expected latency.
10. **Re-binding**: Carrier/material re-binding triggers unbind-first-then-bind.
11. **Sorting - Capacity boundaries**: Test 库区满/空, 上架口容量满, 干燥房满→降级.
12. **Sorting - Priority correctness**: 下架优先级 ①转圈 > ②二级 > ③一级 must hold.
13. **Sorting - Exception routing**: Unbound方案/下线方案/无下架任务 → 异常站.
14. **Sorting - 让道 path validation**: Verify衣架路径 after让道 (一级→二级 or 二级→一级回流).
15. **Sorting - Concurrent constraint**: Enforce 1杆1任务 + 1分拣区域1杆执行.
16. **Sorting - Timer boundaries**: 子任务10min超时 triggers retry (infinite default).

### E. Device Operations

| Device | Modules | Interaction | 安吉纳 |
|--------|---------|-------------|--------|
| PC | Config, Sales, Purchase, QC review, Production order, Reports | Browser management | + **分拣系统基础配置** |
| PAD | QC inspection, Offline tasks, Cloth loosening, Layering, Sewing | Shop floor touch | **后整**菜单: 分拣管理/上架位/下架位/调试 |
| PDA | Material receiving, Cargo bind/shelve, Outbound, Outsourcing | Barcode scanning | |
| Industrial Tablet | Piece hanging, QC in hanging system, **分拣上架SKU选择** | Station fixed position | 安吉纳: PAD替代工业平板 |
| 扫码枪/RFID | **分拣上架口(Rxxx)/下架口(Pxxx)衣架条码扫描** | Barcode/RFID scanning | 安吉纳: 分拣条码枪, 上架扫码绑定(无下架扫码确认) |
| PLC Controller | **分拣分流阀(Vxxx)/电动线/分拣线控制** | Industrial automation | |
| 高速摄像头 | **分拣: 衣架重算(待确认)** | Visual recognition | 安吉纳未提及 |
| 隧道机 | **分拣: 安吉纳/医美(待梳理)** | Tunnel processing | **安吉纳手册未提及隧道机** |

### F. Sorting System Hardware Encoding [DOC]

| 硬件 | 编码 | 逻辑含义 | 集成方式 | 安吉纳 |
|------|------|---------|---------|--------|
| 分流阀 | Vxxx | = 入站站位 | PLC自动分流 | 存在，路由逻辑简化 |
| 上架口 | Rxxx | 上架入口 | 工业平板+扫码枪/RFID | 称"上架位"，PAD+分拣条码枪，物理提升按钮 |
| 下架口 | Pxxx | 下架出口 | 工业平板+扫码枪/RFID | 称"下架位/包装位"，无下架扫描确认 |
| 支轨 | Bxxx | 分支轨道 | 机械连接 | **安吉纳未提及** |
| 库区 | Cx'x'x | = 出站站位(一级/二级) | 传感器检测占用 | 称"储存杆" |
| 电动线 | Sxxx | 一条道(单通道) | 电机控制 | 安吉纳不区分，统一称"分拣线" |
| 分拣线 | Sxxx | 多条岔路口(多分支) | 电机控制+分岔控制 | 安吉纳统称"分拣线" |
| **回流杆** | - | 一级库区让道分流 | - | **安吉纳特有** |
