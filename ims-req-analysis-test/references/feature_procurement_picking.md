# Procurement & Picking Feature Reference

> Sources: V3.1.1 面料领料单, V3.1.3 辅料领料单, PDA裁片外协收发, 外购品采购测试.docx
> Covers: fabric/accessory picking, cut-parts outsource send/receive, external product purchasing

---

## Quick Reference

### State Machines (this domain)

| # | State Machine | Module | Key Risk |
|---|--------------|--------|----------|
| 1 | **Picking Order** (面料/辅料): 草稿→生效→完成 | 领料 | 生效后不可编辑; 完成触发松布任务 |
| 2 | **Outsource Task** (裁片外协): 新增→已完成 (per stage) | 裁片外协 | 四阶段流转; 状态门禁严格 |
| 3 | **Cut Parts Status**: 初始→外协发出→花厂接收→花厂发出→外协收回 | 裁片外协 | 循环可重发; 重复扫描检测 |
| 4 | **External Purchase**: 销售订单→采购计划→采购订单→收货通知→收货单 | 外购品 | 跨模块联动: 销售→采购→仓库 |

### Top 10 Validation Rules

| # | Rule | Module |
|---|------|--------|
| 1 | 面料领料单生效: 领料仓库+领料日期必填, 否则"必填字段缺失" | 面料领料 |
| 2 | 辅料领料单生效: 领料仓库+领料日期+生产组别(3.2.7)必填 | 辅料领料 |
| 3 | PDA出库强校验: 面料[物料编号+色号+供应商物料编码]必须一致 | PDA领料 |
| 4 | PDA出库强校验: 辅料[物料编号+色号+尺码+供应商物料编码]必须一致 | PDA领料 |
| 5 | 裁片外协扫码: 裁片已存在其他外协任务→"裁片已存在其他外协任务" | 裁片外协 |
| 6 | 裁片外协扫码: 未验片完成→"以下裁片未验片完成或未免检，无法外协发出" | 裁片外协 |
| 7 | 裁片外协: 不同生产订单同单发出(配置控制)→"单个单据只允许相同生产订单裁片发出" | 裁片外协 |
| 8 | 外协单号重复→"裁片外协单号重复" | 裁片外协 |
| 9 | 新增领料单: 未勾选生产订单→"请选择一条数据" | 领料 |
| 10 | 新增领料明细: 已新增过的物料复选框禁用(materialId+materialColorId+customerStyleCode+productionOrderStyleId) | 领料 |

### Top 5 Error Messages

| # | Error Message | Trigger Condition |
|---|--------------|-------------------|
| 1 | "必填字段缺失[领料仓库]" | 生效时领料仓库为空 |
| 2 | "必填字段缺失[领料日期]" | 生效时领料日期为空 |
| 3 | "裁片已存在其他外协任务" | 扫描已被其他外协任务使用的裁片 |
| 4 | "以下裁片未验片完成或未免检，无法外协发出{扎号+部位类型}" | 验片未完成的裁片外协发出 |
| 5 | "单个单据只允许相同生产订单裁片发出" | 配置禁止混单时扫描不同生产订单裁片 |

---

## 1. Fabric Picking Order (面料领料单) - V3.1.1

### 1.1 Picking Order Generation Rules (from Cutting Tasks)

系统配置决定面料领料单的拆分规则（不同工厂不同配置）:

```
配置值: 0 = 不拆分
  丰基: 3 (按组别和物料拆分)
  新基: 3 (按组别和物料拆分)
  安吉纳: 0 (不拆分)
  红动: 0 (不拆分)
  太平鸟: 0 (不拆分)
```

**拆分规则详解:**

| 配置 | 规则 | 行为 |
|------|------|------|
| 0 | 不拆分 | 选一个床次→一个领料单; 选多个床次→一个领料单 |
| 1 | 按组别拆分 | 同组别→一个领料单; 不同组别→多个领料单 |
| 2 | 按物料拆分 | 同物料编号→一个领料单; 不同物料→多个领料单 |
| 3 | 按组别和物料 | 两者都相同→一个领料单; 任一个不同→分别生成领料单 |

**关键:** 配置3下，裁剪组别不同+物料编号不同 → 每个(组别, 物料)组合生成一个独立领料单。

### 1.2 State Machine

```
草稿(Draft) --[保存]--> 草稿
草稿 --[生效]--> 生效(Active) --[完成]--> 完成(Done)
生效 --[PDA领料出库]--> (实领数更新，领料状态变化)
草稿 --[删除]--> (删除，二次确认)
```

**领料状态 (per line item):**
```
待领料: 应领数 > 实领数
领料中: 应领数 > 实领数 > 0  (V3.2.3新增)
已领料: 应领数 <= 实领数
```

### 1.3 Header Fields

| Field | Edit Mode | View Mode | Notes |
|-------|-----------|-----------|-------|
| 面料领料单号 | 输入框(自动生成可手动修改) | 显示 | System auto-generate, editable |
| 销售订单号 | 置灰(多个展示多个) | 显示多个 | From production order |
| 生产订单号 | 置灰(多个展示多个) | 显示多个 | From production order |
| 品牌 | 置灰(去重展示) | 去重展示 | Same brand deduped |
| 季度 | 置灰(去重展示) | 去重展示 | Same season deduped |
| 生产组别 | 来源=生产订单:可下拉; 来源=裁剪任务:置灰 | 多个用,间隔 | V3.2.7新增; 部门类型=组别 |
| 是否需松布 | 需要/不需要 | 显示 | V3.2.7新增 |
| 松布组别 | 需要松布时可下拉选择 | 显示 | V3.2.7新增; 来源=部门类型组别 |
| 领料仓库 | 输入框(默认面料仓库) | 默认面料仓库 | Required for 生效 |
| 领料日期 | 日期选择器 | 显示 | 来源=生产订单:空; 来源=裁剪任务:取最早计划裁剪日期 |
| 应领数 | 置灰(明细应领数合计) | 明细应领数合计 | Auto-sum |
| 通知日期 | - | =生效日期 | View mode only |
| 创建人 | - | 首次保存用户 | View mode only |
| 备注 | 输入框(默认空) | 显示 | Editable |

**松布组别下拉数据来源 (按钮权限控制):**
- 安吉纳/红动/太平鸟: 部门类型=组别的部门
- 丰基/新基: 部门类型=组别的部门 + 工段=裁剪工段

### 1.4 Line Item Fields (Edit Mode)

| Field | Type | Notes |
|-------|------|-------|
| 物料信息(成份/名称/密度/组织/支数/CW幅宽/W克重/ART#) | 显示 | Read-only material info |
| 物料色号 | 显示 | 去重展示，不可编辑 |
| 销售订单号 | 显示 | 带入展示 |
| 客户款号 | 显示 | 带入展示 |
| 采购订单号 | 下拉多选 | 根据销售订单号查询关联PO |
| 应领数 | 输入框 | 默认空，手动输入，保存2位小数 |
| 领料需求数 | - | 预留字段(唛架得出)，本期不做 |
| 库存数 | 显示 | MES面料库存数 |
| 单位 | 显示 | 取基础物料单位 |
| 缸号 | 下拉多选 | 查询库存已有值，去重展示 |
| Lot色 | 下拉多选 | 查询库存已有值 |
| 客要缩率 | 文本框 | - |
| 扭曲度 | 输入框 | - |

### 1.5 Line Item Fields (View Mode)

Additional fields vs edit mode:
- **领料状态**: 待领料/领料中/已领料
- **实领数**: PDA实际领料出库数量
- **实领卷数**: PDA实际领料出库布卷数
- **库存数**: IMS面料库存数 - 领料出库数量
- **操作-查看明细**: 进入领料明细页面

### 1.6 领料明细页面 (View Mode)

| Field | Notes |
|-------|-------|
| Header: 物料名称, 供应商物料编码, 物料色号, 需求缸号, 需求Lot色, 需求缩率, 需求扭曲度, 应领数量, 实领数量, 单位 | - |
| Detail rows: 缸号, 卷号, 实领数量, Lot色, 缩率, 扭曲度, 采购订单号, 销售订单号 | - |

### 1.7 Business Rules & Validation

**生效校验:**
- 领料仓库为空 → "必填字段缺失[领料仓库]"
- 领料日期为空 → "必填字段缺失[领料日期]"
- 是否需松布=是 且 松布组别为空 → 生效失败 (bugId7922)

**完成触发的松布任务:**
| 条件 | 行为 |
|------|------|
| 是否需松布=空 | 不生成松布任务 |
| 是否需松布=否 | 不生成松布任务 |
| 是否需松布=是 | 生成松布任务，显示松布组别 (bug7923) |
| 来源=生产订单+手动选生产组别 | 生成松布任务，显示对应生产组别 (bugId7926) |

**来源标识:**
- 通过新增面料领料单创建 → 来源=生产订单
- 通过裁剪任务发起 → 来源=裁剪任务

**按钮可见性:**
| 按钮 | 草稿 | 生效 | 完成 |
|------|------|------|------|
| 编辑 | Yes | - | - |
| 复制 | Yes | Yes | Yes |
| 删除 | Yes | - | - |
| 生效 | Yes | - | - |
| 完成 | - | Yes | - |
| 打印 | Yes | Yes | Yes |
| 导出 | 暂不做 | 暂不做 | 暂不做 |

### 1.8 Cross-Module Interactions

- **生产订单** → 领料单: 来源数据(销售订单号/生产订单号/客户款号)
- **组别排程** → 领料单: 开裁日期(多个取最早)
- **裁剪任务** → 领料单: 发起领料; 床次→生产组别
- **基础物料** → 领料单: 物料信息, 单位
- **PDA领料出库** → 领料单: 实领数/实领卷数更新
- **MES库存** → 领料单: 库存数查询
- **松布任务** ← 领料单: 完成时自动生成

---

## 2. Accessory Picking Order (辅料领料单) - V3.1.3

### 2.1 State Machine

(Same as fabric picking order)
```
草稿 --[保存]--> 草稿 --[生效]--> 生效 --[完成]--> 完成
```

### 2.2 Key Differences from Fabric Picking

| Aspect | 面料领料单 | 辅料领料单 |
|--------|-----------|-----------|
| 仓库 | 面料仓库 | 辅料仓库 |
| 明细唯一键 | materialId+materialColorId+customerStyleCode+productionOrderStyleId | materialId+materialColorId+materialSizeId+customerStyleCode+productionOrderStyleId |
| 拆分配置 | 有(0/1/2/3) | 无(无裁剪任务拆分逻辑) |
| 新增弹窗筛选 | 销售订单号/生产订单号/客户款号/**开裁日期** | 销售订单号/生产订单号/客户款号(无开裁日期) |
| 生产组别 | 来源决定可编辑性 | 始终下拉单选框(必填) |
| 松布 | 有松布流程 | 无松布流程 |
| 裁剪床号 | 无 | V3.2.7新增, 弹窗选择已完成床次 |
| 裁剪合格件数 | 无 | V3.2.7新增, 自动计算 |
| 规格 | 无 | 取基础辅料规格成份 |
| 物料尺码 | 无 | 有 |
| 打印 | 所有状态 | 仅生效&完成状态 |

### 2.3 Header Fields

| Field | Edit Mode | View Mode | Notes |
|-------|-----------|-----------|-------|
| 辅料领料单号 | 输入框(自动生成可手动修改) | 显示 | - |
| 销售订单号 | 置灰(多个展示多个) | 显示多个 | - |
| 生产订单号 | 置灰(多个展示多个) | 显示多个 | - |
| 裁剪床号 | 点击弹出[选择床次]弹窗 | 裁剪任务单号\|床次号 | V3.2.7新增; 显示不下用...悬浮展示 |
| 裁剪合格件数 | 置灰(自动计算) | 自动计算 | V3.2.7新增 |
| 品牌 | 置灰(去重展示) | 去重展示 | - |
| 季度 | 置灰(去重展示) | 去重展示 | - |
| 生产组别 | 下拉单选框(必填) | 显示 | V3.2.7新增; 部门类型=组别 |
| 领料仓库 | 输入框(默认辅料仓库) | 默认辅料仓库 | Required |
| 领料日期 | 日期选择器(默认空) | 显示选择的生产组别 | Required |
| 应领数 | 置灰(默认0) | 明细应领数合计 | Auto-sum |
| 备注 | 输入框(默认空) | 显示 | Editable |
| 通知日期 | - | =生效日期 | View mode only |
| 创建人 | - | 首次保存用户 | View mode only |

### 2.4 选择床次弹窗

**数据来源:** 裁剪任务中已完成的床次任务

**左侧(待选择):**
- 复选框, 裁剪任务单号, 床次号, 裁剪组别, 开裁类型, 成衣色号, 成衣色称, 配比, 裁剪合格数
- 多行分页展示
- 筛选: 裁剪任务单号, 裁剪组别, 开裁类型, 成衣色号, 成衣色称

**右侧(已选中):**
- 裁剪任务单号, 床次号, 裁剪合格数
- 操作列: [取消选中]按钮
- 上下滑动展示

**交互:**
- 左侧勾选→右侧展示; 左侧取消→右侧移除
- 未勾选点击确认→"最少选择一条数据"
- 确认后关闭弹窗，显示: 裁剪任务单号|床次号(多个用,间隔)

### 2.5 Line Item Fields

| Field | Edit Mode | Notes |
|-------|-----------|-------|
| 物料名称 | 不可编辑 | - |
| 供应商物料编码 | 不可编辑 | - |
| 物料颜色 | 不可编辑 | - |
| 物料色号 | 不可编辑 | 去重展示 |
| 物料尺码 | 不可编辑 | - |
| 规格 | 不可编辑 | 取基础辅料规格成份 |
| 销售订单号 | 不可编辑 | 带入展示 |
| 客户款号 | 不可编辑 | 带入展示 |
| 采购订单号 | 下拉多选 | 根据销售订单号查询 |
| 应领数 | 输入框 | 默认空，手动输入，不控制小数位 |
| 领料需求数 | - | 预留字段 |
| 库存数 | 不可编辑 | MES辅料库存数 |
| 单位 | 不可编辑 | 取基础辅料单位 |

### 2.6 View Mode Line Items

Additional fields:
- **领料状态**: 待领料/领料中/已领料 (same logic as fabric)
- **实领数**: PDA辅料出库后展示
- **库存数**: IMS面料库存数

### 2.7 领料明细页面

| Category | Fields |
|----------|--------|
| Header | 物料名称, 供应商物料编码, 物料颜色, 物料色号, 物料尺码, 规格, 应领数量, 实领数量, 单位, 销售订单号, 款号, 客户款号 |
| Detail | 实领数量, 箱号, 箱码, 采购订单号, 原销售订单号, 原款号, 原客户款号 |

### 2.8 辅料清单 & 库存

- 辅料收货单生效后 → 自动生成辅料清单
- PC端有辅料库存查询

---

## 3. PDA Cut Parts Outsource Send/Receive (裁片外协收发)

### 3.1 Overall Workflow (4 Stages)

```
Stage 1: PDA_按箱裁床发出 (Cut Bed Send-Out)
  └─ 新增裁片外协任务 → 扫描裁片箱码 → 确认发出 → 裁片状态→"外协发出"

Stage 2: PDA_按箱花厂接收 (Flower Factory Receive)
  └─ 扫描已发出的裁片箱 → 确认接收 → 裁片状态→"花厂接收"

Stage 3: PDA_按箱花厂发出 (Flower Factory Send-Out)
  └─ 扫描花厂已接收的裁片箱 → 确认发出 → 裁片状态→"花厂发出"

Stage 4: PDA_按箱裁床收回 (Cut Bed Take-Back)
  └─ 扫描花厂已发出的裁片箱 → 确认收回 → 裁片状态→"外协收回"
```

**循环支持:** 裁片走完一轮收发流程(外协收回)后，可重新发起新一轮外协任务。

### 3.2 Cut Parts Status State Machine

```
初始状态 --[按箱裁床发出]--> 外协发出 --[按箱花厂接收]--> 花厂接收
花厂接收 --[按箱花厂发出]--> 花厂发出 --[按箱裁床收回]--> 外协收回
外协收回 --[新一轮外协]--> 初始状态 (可循环)
```

### 3.3 Stage Status Gate (which statuses are accepted per stage)

| Current Status → Stage | 初始 | 外协发出 | 花厂接收 | 花厂发出 | 外协收回 |
|------------------------|------|----------|----------|----------|----------|
| 按箱裁床发出 | OK | FAIL | FAIL | FAIL | OK (新一轮) |
| 按箱花厂接收 | FAIL | OK | FAIL | FAIL | FAIL |
| 按箱花厂发出 | FAIL | FAIL | OK | FAIL | FAIL |
| 按箱裁床收回 | FAIL | OK (提示) | FAIL | OK | FAIL |

### 3.4 Create Outsource Task (新增裁片外协任务)

**Fields:**
| Field | Type | Validation |
|-------|------|------------|
| 外协单号 | 输入框(默认空) | 空→自动生成"CPFC+年(后两位)月日+三位序号"; 手动输入→唯一性校验 |
| 接收组织 | 下拉框 | 必填; 来源=供应商类别=外发加工 |
| 来源组织 | 下拉框 | 必填; 来源=部门类型=车间 |

**Memory:** 新增成功后记住上次填写值，再次进入新增页面回显。

### 3.5 Task List (分页列表)

**筛选:** 单据状态(未完成/已完成)

**卡片字段:**
- 外协单号, 状态, 裁片发出扎数
- 生产订单号, 款号, 款式名称
- 成衣颜色(色号|色称, 多个逗号间隔), 成衣尺码(多个逗号间隔)
- 制程, 接收组织, 来源组织
- 发出人(单据创建人), 发出时间(单据确认发出时间)
- 上下滑动加载更多

### 3.6 Task Detail Page

**条码输入框:** 支持手动输入和扫描裁片箱码

**单据字段:** 外协单号, 实际发出箱数|扎数|件数, 生产订单号, 款号, 款式名称, 成衣颜色, 成衣尺码, [删除]按钮

**[收起全部] 按钮:** 收起所有已展开的箱卡片

**箱卡片字段:** 箱号, 总扎数|总件数, 删除icon, 生产订单号, 款号, 裁片类型(多个逗号间隔), 成衣颜色, 成衣尺码, [查看明细]按钮

### 3.7 箱详情页面

**箱字段:** 箱号, 总扎数|总件数

**[收起全部]按钮:** 收起所有已展开扎卡卡片

**扎卡字段:** 扎号, 件数, 裁片类型, 生产订单号, 款号, 成衣颜色|尺码(色码逗号间隔)

### 3.8 Scan Validation Rules

**载具类型扫描:**
- 裁片箱 → 扫描成功展示
- 面料托盘/松布架/辅料箱/成品箱/周转箱/超规格辅料框 → (非裁片载具)
- 车笼/辅料车 → 箱码中无裁片信息
- 空载具 → "裁片箱[箱号]中未查询到裁片"
- 不存在载具 → "未找到该条码的载具"

**重复扫描:** 同载具重复扫描→允许但不重复展示

**跨任务冲突:** 裁片已存在其他外协任务→"裁片已存在其他外协任务"

### 3.9 System Configurations

| Config Key | Values | Effect |
|------------|--------|--------|
| `mes-production:diff_productionorder_add_order_model` | 0=允许, 1=不允许 | 裁片外协-允许不同生产订单同单发出 |
| `mes-production:bundle_strap_complete_model` | 0=不校验, 1=校验 | 裁片外协任务-是否校验验片完成 |
| `mes-production:outsource_strap_complete_switch` | 0=关闭, 1=开启 | 裁片委外验片完成校验开关 |

### 3.10 Confirm Send/Receive Validation (All 4 Stages)

**通用校验流程:**
1. 无箱码裁片→[完成/确认发出]按钮置灰
2. 有箱码裁片→按钮高亮可点击
3. 点击→二次确认: "共计X包X件，是否确认完成本次任务？"
4. 三级配置校验: bundle_strap_complete_model + diff_productionorder_add_order_model + outsource_strap_complete_switch

**成功结果 (所有4阶段共用):**
1. 裁片外协任务状态→已完成
2. 裁片扎卡状态→对应阶段状态
3. 委外发出区站位释放
4. 裁片与裁片箱不解绑，不出库，仅库区变更

---

## 4. External Product Purchasing (外购品采购)

> Source: 凯奥尼-外购品采购测试.docx

### 4.1 Business Flow

```
销售订单(销售类型=外购品采购) --[生效]--> 生效
  └─ 外购品采购计划 --[生成采购订单]--> 生效
       └─ 外购品采购订单 --[计划新增]-->  
            └─ 外购品收货通知单 --[新增采购收货单]--> 生效
```

### 4.2 Key Characteristics

- **入口:** 销售订单中选择销售类型="外购品采购"
- **区别于普通采购:** 从销售订单驱动，走专用外购品采购计划
- **采购订单来源:** 计划新增 (而非手工新增)
- **收货流程:** 收货通知单 → 采购收货单

### 4.3 Cross-Module Interactions

| Step | Source Module | Target Module | Data Flow |
|------|--------------|---------------|-----------|
| 1 | 销售订单 | 外购品采购计划 | 销售类型=外购品采购的订单 |
| 2 | 外购品采购计划 | 采购订单 | 生成采购订单(生效) |
| 3 | 采购订单 | 收货通知单 | 计划新增的PO |
| 4 | 收货通知单 | 采购收货单 | 新增采购收货单(生效) |

---

## 5. PDA Picking Outbound (PDA领料出库)

### 5.1 General Rules

- 领料单列表仅显示: 未完成待领料的单据
- Supports both fabric and accessory picking

### 5.2 Strong Validation (强校验) - Blocks Outbound

**面料:**
- Keys: `["materialExtendCode", "colorCode", "clothNo"]`
- 物料编号+色号+供应商物料编码 必须一致，否则出库失败

**辅料:**
- Keys: `["materialExtendCode", "colorCode", "clothNo", "sizeCode"]`
- 物料编号+色号+尺码+供应商物料编码 必须一致，否则出库失败

### 5.3 Weak Validation (弱校验) - Warns but Continues

**面料:**
- Keys: `["po", "purchaseOrderCode", "fabricVatcodeCode", "lot", "customStyleCode"]`
- 销售单号+采购单号+缸号+lot色+客户款号，任一项与领料单不同→二次确认提示，仍可出库

**辅料:**
- Keys: `["po"]`
- 销售单号与领料单不同→二次确认提示，仍可出库

---

## 6. Test Scenarios Summary

### 6.1 Fabric Picking - High Priority

| ID | Scenario | Expected |
|----|----------|----------|
| F-PICK-01 | 配置0: 选多个床次→生成一个领料单 | 1领料单包含所有床次 |
| F-PICK-02 | 配置3: 不同组别+不同物料→分别生成领料单 | N个领料单(每个组别物料组合) |
| F-PICK-03 | 生效时领料仓库为空 | "必填字段缺失[领料仓库]" |
| F-PICK-04 | 生效时领料日期为空 | "必填字段缺失[领料日期]" |
| F-PICK-05 | 松布=是 且松布组别为空→生效 | 生效失败 (bug7922) |
| F-PICK-06 | 完成领料单(松布=是) | 自动生成松布任务+显示松布组别 |
| F-PICK-07 | 完成领料单(松布=否) | 不生成松布任务 |
| F-PICK-08 | PDA强校验: 物料编号不一致出库 | 出库失败 |
| F-PICK-09 | PDA弱校验: 缸号不同→二次确认→确认 | 仍可出库 |
| F-PICK-10 | 新增领料明细: 已新增物料复选框禁用 | 无法重复添加 |
| F-PICK-11 | 复制领料单 | 状态=草稿，仅复制物料明细，布卷明细不复制 |

### 6.2 Accessory Picking - High Priority

| ID | Scenario | Expected |
|----|----------|----------|
| A-PICK-01 | 选择裁剪床次: 未勾选点确认 | "最少选择一条数据" |
| A-PICK-02 | 选择裁剪床次: 确认后回显 | 裁剪任务单号\|床次号 |
| A-PICK-03 | 生产组别为空→保存 | 保存失败，输入框标红 |
| A-PICK-04 | 裁剪合格件数自动计算 | 选中床次的合格数总和 |
| A-PICK-05 | 生效时领料仓库为空 | "必填字段缺失[领料仓库]" |
| A-PICK-06 | 新增明细唯一键去重 | 同materialId+colorId+sizeId+customerStyleCode+productionOrderStyleId禁用 |
| A-PICK-07 | 打印按钮: 草稿状态 | 不显示(仅生效&完成显示) |
| A-PICK-08 | 辅料收货单生效→生成清单 | 辅料清单自动生成 |

### 6.3 Cut Parts Outsource - High Priority

| ID | Scenario | Expected |
|----|----------|----------|
| OUT-01 | 新增外协任务: 空外协单号 | 系统自动生成 CPFC+YYMMDD+001 |
| OUT-02 | 新增外协任务: 重复外协单号 | "裁片外协单号重复" |
| OUT-03 | 新增外协任务: 空接收组织 | "请选择接收组织" |
| OUT-04 | 新增后记忆: 再次进入 | 回显上次填写值 |
| OUT-05 | 扫描不存在的载具 | "未找到该条码的载具" |
| OUT-06 | 扫描空载具 | "裁片箱[箱号]中未查询到裁片" |
| OUT-07 | 扫描已被其他外协任务使用的裁片 | "裁片已存在其他外协任务" |
| OUT-08 | 按箱裁床发出: 扫描状态=外协发出的裁片 | 扫描失败 |
| OUT-09 | 按箱花厂接收: 扫描状态=外协发出的裁片 | 扫描成功 |
| OUT-10 | 按箱花厂发出: 扫描状态=花厂发出的裁片 | "裁片[扎号]状态为[花厂发出]，不能进行当前操作" |
| OUT-11 | 按箱裁床收回: 扫描状态=花厂发出的裁片 | 扫描成功 |
| OUT-12 | 验片未完成→确认发出(config=1) | "以下裁片未验片完成或未免检，无法外协发出" |
| OUT-13 | 不同生产订单同单(config=0) | 发出成功 |
| OUT-14 | 不同生产订单同单(config=1) | "单个单据只允许相同生产订单裁片发出" |
| OUT-15 | 空单确认发出 | 按钮置灰不可点击 |
| OUT-16 | 完成一轮后重新发起 | 扫描成功(循环支持) |
| OUT-17 | 花厂接收: 从箱中移除扎卡 | 二次确认→扎卡与箱解绑 |
| OUT-18 | 委外验片完成校验(config=1) | "存在委外验片未完成的扎卡" |

### 6.4 External Product Purchasing - High Priority

| ID | Scenario | Expected |
|----|----------|----------|
| EXT-PUR-01 | 销售订单选择外购品采购类型→生效 | 订单生效 |
| EXT-PUR-02 | 外购品采购计划→生成采购订单→生效 | PO生成并生效 |
| EXT-PUR-03 | 外购品采购订单→计划新增 | PO创建成功 |
| EXT-PUR-04 | 外购品收货通知单→新增采购收货单→生效 | 收货完成 |
| EXT-PUR-05 | 端到端: 销售订单→收货完成 | 全流程通过 |

---

## 7. Field Name Quick Reference

### 7.1 Fabric Picking (面料领料单)

| Chinese | English | Type |
|---------|---------|------|
| 面料领料单号 | Fabric Picking Order No. | Text |
| 状态 | Status | Enum: 草稿/生效/完成 |
| 领料仓库 | Picking Warehouse | Text (default: 面料仓库) |
| 领料日期 | Picking Date | Date (from 开裁日期) |
| 通知日期 | Notification Date | Date (=发布日期 or 生效日期) |
| 创建人 | Creator | Text |
| 供应商物料编码 | Supplier Material Code | Text |
| 物料编码 | Material Code | Text |
| 物料名称 | Material Name | Text |
| 物料色号 | Material Color Code | Text |
| 供应商 | Supplier | Text |
| 实领数量 | Actual Picked Qty | Number |
| 单位 | Unit | Text |
| 实领卷数 | Actual Picked Rolls | Number |
| 销售订单号 | Sales Order No. | Text |
| 生产订单号 | Production Order No. | Text |
| 款号 | Style No. | Text |
| 客户款号 | Customer Style No. | Text |
| 品牌 | Brand | Text |
| 季度 | Season | Text |
| 生产组别 | Production Group | Dropdown (V3.2.7) |
| 是否需松布 | Need Fabric Relaxation | Boolean (V3.2.7) |
| 松布组别 | Relaxation Group | Dropdown (V3.2.7) |
| 来源 | Source | Enum: 生产订单/裁剪任务单 |
| 领料状态 | Picking Status | Enum: 待领料/领料中/已领料 |
| 缸号 | Vat No. | Multi-select dropdown |
| Lot色 | Lot Color | Multi-select dropdown |
| 客要缩率 | Customer Shrinkage | Text |
| 扭曲度 | Twist Degree | Number |

### 7.2 Accessory Picking (辅料领料单)

Additional fields beyond fabric picking:

| Chinese | English | Type |
|---------|---------|------|
| 辅料领料单号 | Accessory Picking Order No. | Text |
| 物料颜色 | Material Color | Text |
| 物料尺码 | Material Size | Text |
| 规格 | Specification | Text |
| 裁剪床号 | Cutting Bed No. | Text (V3.2.7) |
| 裁剪合格件数 | Cutting Qualified Qty | Number (V3.2.7) |
| 裁剪任务单号 | Cutting Task No. | Text |
| 床次号 | Bed Batch No. | Text |
| 开裁类型 | Cutting Type | Text |
| 成衣色号 | Garment Color Code | Text |
| 成衣色称 | Garment Color Name | Text |
| 配比 | Ratio | Number |
| 箱号 | Box No. | Text |
| 箱码 | Box Code | Text |

### 7.3 Cut Parts Outsource (裁片外协)

| Chinese | English | Type |
|---------|---------|------|
| 外协单号 | Outsource Order No. | Text (auto: CPFC+YYMMDD+NNN) |
| 接收组织 | Receiving Org | Dropdown (supplier type=外发加工) |
| 来源组织 | Source Org | Dropdown (dept type=车间) |
| 裁片发出扎数 | Cut Parts Sent Bundles | Number |
| 制程 | Process | Text |
| 发出人 | Sender | Text (单据创建人) |
| 发出时间 | Send Time | DateTime |
| 实际发出箱数 | Actual Sent Boxes | Number |
| 裁片类型 | Cut Part Type | Text |
| 扎号 | Bundle No. | Text |
| 件数 | Piece Count | Number |
| 裁片状态 | Cut Part Status | Enum: 初始/外协发出/花厂接收/花厂发出/外协收回 |
| 裁片箱 | Cut Parts Box | Carrier type |

### 7.4 External Purchase (外购品采购)

| Chinese | English | Notes |
|---------|---------|-------|
| 销售类型 | Sales Type | =外购品采购 |
| 外购品采购计划 | External Purchase Plan | Sales-driven |
| 外购品采购订单 | External Purchase Order | Plan-generated |
| 外购品收货通知单 | External Purchase Receipt Notice | triggers receipt |
| 采购收货单 | Purchase Receipt Order | Final receipt document |

---

## 8. Configuration Summary

| Config Key | Domain | Values | Default Per Factory |
|------------|--------|--------|---------------------|
| 领料单拆分模式 | 面料领料 | 0/1/2/3 | 丰基=3, 新基=3, 安吉纳=0, 红动=0, 太平鸟=0 |
| mes-production:diff_productionorder_add_order_model | 裁片外协 | 0允许/1不允许 | per factory |
| mes-production:bundle_strap_complete_model | 裁片外协 | 0不校验/1校验 | per factory |
| mes-production:outsource_strap_complete_switch | 裁片外协 | 0关闭/1开启 | per factory |

---

## 9. Known Bugs (from source)

| Bug ID | Description | Module |
|--------|-------------|--------|
| bugId7922 | 是否需松布=是且松布组别为空时，生效无错误提示 | 面料领料 |
| bugId7923 | 是否需松布=是时完成领料单，松布组别不显示 | 面料领料 |
| bugId7926 | 来源=生产订单+手动选生产组别，完成时松布任务不显示生产组别 | 面料领料 |
