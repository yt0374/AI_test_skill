# Feature Synthesis: Style Management & Reports

> Synthesized from four feature-point extraction documents:
> - V3.0.x 丰基 款号 (Style Management, ~2500 lines)
> - V3.2.27.4 (Report currency formatting, order deletion, department/workshop linkage)
> - V3.3.1 (Cutting daily output report, CPO deletion, packing list generation)
> - [持续] Export column customization

---

## 1. Style (款号) Management

### 1.1 Creation Sources (bizType)

| Source | Trigger | bizType |
|--------|---------|---------|
| 办单 (Sample Order) | Click `引用新增` | 1 |
| 手动 (Manual) | Click `新增` or `复制款号` | 2 |
| 销售订单 (Sales Order) | Sales order生效后 | 3 |

**Copy rule**: Copying a style clears `客户款号` and `销售订单号`.

### 1.2 Uniqueness Rules (System Config: `style-mode`)

**Config key**: `style-mode`, Module: `ALL`

| Config Value | Tenant | Uniqueness Fields |
|--------------|--------|-------------------|
| 1 | 丰基 | 款号 + 客户款号 + 销售订单号 (3-field unique) |
| 2 | 安吉纳/红动 | 款号 + 客户款号 (2-field unique) |

### 1.3 Auto-generation on Production Order Effective (配置值=2)

When a production order takes effect:
- **款号不存在 + 客户款号不存在**: Creates new style, copies tabs 1-6 (基本信息, 颜色尺码, 部位尺寸, 工艺要求, 生产工序, 配料说明)
- **款号不存在 + 客户款号存在**: Creates new style, copies tabs 1-6
- **款号存在 + 客户款号不存在**: Creates new style, copies tabs 1-6
- **款号存在 + 客户款号存在**: No new style; **incremental update** of color/size data only

**Color/Size incremental merge behavior (配置值=2)**:
- Color/size sets are **union-merged** (never shrink): existing colors/sizes persist, new ones are appended
- Multiple production orders under same style+customer style merge colors/sizes additively
- Other tabs' existing values are preserved; new dynamic columns (color/size) appear with empty values

### 1.4 Auto-generation on Sales Order Effective

**配置值=1 (丰基)**:
- All 8 combinations of {款号, 客户款号, 销售订单号} exist/not-exist are tested
- `销售订单生效失败` cases: when 销售订单号 already exists for that style+customer combination
- New style copies selected style's data (物料用量, 色码用量, 物料配色, 物料配码, 部位尺寸, 工艺要求, 用线指示, 生产工序)
- **Known bug**: 单位 field - sales order passes null, style assigns default "cm", causing mismatch (Bug转任务926)

**配置值=2 (安吉纳)**:
- Same as production order logic: union-merge color/size, no style duplication if 款号+客户款号 exists
- Existing style receives incremental color/size updates only

### 1.5 Style List Page

**Filter fields**:
- 款号 (input), 款式名称 (dropdown), 款号名称 (dropdown), 客户 (dropdown), 状态 (dropdown: 草稿/生效)
- V3.1.2 added: 来源 (dropdown: 办单/手动/销售订单), 客户款号 (input), 销售订单号 (input)

**List columns**: 款号, 客户款号 (V3.1.2), 销售订单号 (V3.1.2), 款式名称, 款号名称, 客户, 品牌, 季度, 国家(deleted), 状态, 创建人, 创建时间

**Row actions**:
- `编辑` button: removed in V3.1.2
- `复制` button: only for 生效 status
- `删除` button: only for 草稿 status

### 1.6 Manual Style Creation (新增)

**Required fields**: 款号 (must not be empty, must not exist), 客户 (must not be empty)

**Editable fields**: 款号, 客户款号, 客户, 国家(deleted), 品牌, 款式名称, 款号名称, 季度, 特殊工艺(multi-select), EQ (numeric, 2517-new field), 备注

**Uniqueness validation**:
- Config=1: 款号+客户款号+销售订单号 unique; same combination fails with error
- Config=2: 款号+客户款号 unique

### 1.7 Reference-Add from 办单 (Sample Order)

- Only shows 办单 with status: 生效, 已发布, 完成
- Resulting style status = 草稿
- Only copies color/size combinations that have quantity values (non-zero)
- Color/size order: enabled colors first, then disabled (bug6497, task872)
- Various tabs copy corresponding data from the sample order

### 1.8 State Transitions

```
草稿 (Draft)
  |-- [生效] --> 生效 (Effective) [page becomes read-only, [反生效] button appears]
  |-- [删除] --> (deleted)

生效 (Effective)
  |-- [反生效] --> 草稿 (Draft) [[生效] button reappears]
  |-- [复制] --> creates new 草稿 style (clears 客户款号, 销售订单号)
```

### 1.9 Style Detail Page Tabs

**Tab list**: 基本信息, 颜色尺码, 物料需求 (物料用量/色码用量/物料配色/物料配码/物料清单), 部位尺寸, 工艺要求, 用线指示, 部位管理, 生产工序, 操作日志

**Auto-save toggle**: When ON, auto-saves changed tab content on tab switch. When OFF, prompts user to confirm save/discard.

### 1.10 Color/Size Tab

- Separate color list (成衣色号, 成衣色称) and size list (成衣尺码)
- Row-level add/delete; batch delete via checkbox
- Copy from other styles (only 生效 status); single-select, overwrites existing
- **Color/Size merge rules when copying**: same color&size shows values; different shows empty; partial match shows only matching values

### 1.11 Material Requirements (物料需求)

**Sub-tabs**: 物料用量, 色码用量, 物料配色, 物料配码, 物料清单

**Key validation points**:
- Import: xlsx/xls OK, docx rejected
- 单件用量/备品: integers and decimals (2dp) OK; Chinese/English/special chars rejected with "数值类型错误"
- 运算符: only `+` and `×` valid; others rejected with "运算符不存在"
- Duplicate 物料编号: allowed, shown as separate rows
- Empty required field: red highlight + import button disabled

**物料清单 generation config**: `core-data:generate_inventory_when_zero_usage`
- 0: Skip rows with 0 or empty 色码用量
- 1 (default): Generate all rows, values are 0 or empty

### 1.12 Copy Across Tabs (General Pattern)

All tabs (颜色尺码, 物料用量, 部位尺寸, 工艺要求, 用线指示, 部位管理, 生产工序) support copy:
- Only 生效 status styles shown
- **Single-select** radio button (not multi-select)
- Cross-page selection: only current page selection counts
- No selection: error "请选择一条数据"
- Copy overwrites existing data fully
- Order preserved from source

**Color/size dynamic column copy rules**:
- Same color/size: values displayed
- Different color/size: empty
- Partial overlap: only matching columns show values

### 1.13 Tab-Level Permission Control

Each tab has edit/import/copy permissions configured separately. `销售订单号` field visibility controlled by permission toggle across list page and all detail tabs.

---

## 2. Report Module

### 2.1 Currency/Amount Formatting (千位符) - V3.2.27.4

**Affected reports and fields**:

| Report | Fields with 千位符 |
|--------|-------------------|
| 采购-物料采购明细表 | 单价, 总金额; 汇总: 总金额; 透视: 总金额求和总计 |
| 采购-物料收货明细表 | 单价, 总金额; 汇总: 总金额; 透视: 总金额求和总计 |
| 财务-应收报表 | 订单总价, 发运后应收总价 |
| 财务-应付报表 | 采购单价, 采购总金额, 收货应收总金额 |
| 裁剪-裁剪员工实时报工表 | 工资 |
| 生产-线外员工实时报工表 | 工资 |
| 吊挂-员工实时报工表 | 工资 |
| 生产-尾整员工实时报工表 | 工资 |

**Format rules**:
- 千位符 applied to list data, summary items, and pivot grid
- Data is **右对齐 (right-aligned)** with the formatting
- **Pivot export** shows 千位符 on screen but **cannot be exported with 千位符** (known limitation)
- General export (通用导出) does show 千位符

### 2.2 Department/Workshop/Group Linkage - V3.2.27.4

**Reports**: 员工实时报工表, 工序产量汇总表, 日产量报表, 生产质量明细表

**Cascade rules**:
- Select 部门 -> 车间 dropdown shows only that department's workshops -> 组别 shows that workshop's groups
- Select 车间 -> 组别 shows that workshop's groups
- Select 组别 directly -> shows results
- **Clearing/clash rules**: When switching higher-level filter, lower-level selections are cleared
  - Selecting 部门 after 车间 is chosen: 车间 cleared, group shows department-level groups
  - Selecting 车间 after 组别 is chosen: 组别 cleared
  - Selecting 部门 after 组别 is chosen: 组别 cleared
- **Sort order**: dropdowns sorted by system-defined order

### 2.3 Cutting Daily Output Report - V3.3.1

**Field updates based on inventory transaction types**:

| Transaction | 出库数 updated? | 出库时间 updated? | 库区 | Notes |
|-------------|:---:|:---:|------|-------|
| 裁剪验片出库 | No | No | - | Even after 裁片验片完成 |
| 委外验片出库 | No | No | - | 外协验片时间/合格数 updated |
| 出库确认 | **Yes** | **Yes** | Cleared | |
| 新进物料入库 (收货) | No | No | Updated | |
| 委外出库 | **Yes** | **Yes** | Cleared | 是否印绣/发花时间/发花数 updated |
| 委外收货 | No | No | Updated | 收花时间/收花数 updated |
| 外协发出 (裁片/成衣) | **Yes** | **Yes** | Cleared | |
| 外购收回 | No | No | - | No inventory flow |
| 按箱裁床发出 | No | No | Updated | No inventory flow |

**Key finding**: Only 出库确认, 委外出库, and 外协发出 correctly update 出库数 and 出库时间. 裁剪验片出库 and 委外验片出库 do NOT update these fields (this is the bug addressed by this version).

### 2.4 Export Column Customization (持续功能)

**Scope**: Cross-report export that respects user's column settings

**Report coverage table**:

| Module | Report | Debug Mode | Column Settings |
|--------|--------|:---:|:---:|
| 缝制 | 生产质量报表 | OK (rename/hide/reorder) | OK (hide/reorder) |
| 裁剪&裁片 | 裁剪日产量报表 | OK | OK |
| 吊挂 | 员工考勤报表 | OK (no debug config) | OK |
| 吊挂 | 工序产量汇总表 | OK | OK |
| 吊挂 | 日产量报表 | OK (no debug config) | OK |
| 吊挂 | 生产质量明细表 | OK | OK |
| 吊挂 | 小组日质检明细表 | OK | OK |
| 吊挂 | 车间月质检汇总表 | OK | OK |
| 样衣 | 办单全流程跟踪表 | OK | OK |
| 样衣 | 采购物料跟踪表 | OK | OK |
| 生产 | 采购跟踪表 | OK | OK |
| 生产 | 水洗日产量报表 | OK | OK |

**Export behaviors**:
- **修改字段名称**: Exported with renamed column headers
- **隐藏字段**: Hidden columns excluded from export
- **调整字段顺序**: Export order matches user's configured order
- Debug mode and Column Settings (列设置) are two separate code paths, both tested

---

## 3. Data Format Rules

### 3.1 Numeric Fields (千位符, 右对齐)
- Applied to all amount/wage fields across reports
- Right-aligned display
- Export includes 千位符 formatting
- Pivot export limitation: 千位符 visible on screen, not preserved in pivot export

### 3.2 Decimal Precision
- **EQ**: 2 decimal places
- **单件用量/备品**: 2 decimal places (import/display)
- **SAM/单价**: Up to 4 decimal places; exceeding 4 rejected with "数值类型错误(最多4位小数)"
- **Negative values for SAM/单价**: Input rejected (shows 0), import rejected with "数值类型错误(最多4位小数)"

### 3.3 Input Validation (Numeric)
- **SAM/单价 input**: Chinese/English/special chars rejected (shows empty); negative rejected (shows 0); integer/0/decimal accepted
- **单件用量/备品 import**: negative allowed; Chinese/English/special chars -> "数值类型错误"

---

## 4. Export Customization

### 4.1 Column Selection & User Preferences
- Export honors: field name changes, visibility (hidden vs shown), order
- Two mechanisms: Debug mode (development) and Column Settings (user-facing)
- Both paths tested independently across all report types

### 4.2 Pivot Export Limitation
- 千位符 shown on screen in pivot view
- Export from pivot grid does NOT preserve 千位符 (noted as "无法实现")

---

## 5. Version-Specific Changes & Regression Targets

### V3.0.x (丰基 款号 - baseline)
- Complete style management module
- `style-mode` config (1=丰基, 2=安吉纳)
- All tab functionality, copy/import/export features

### V3.1.1
- Import functionality added for 物料用量, 部位尺寸

### V3.1.2
- List page: added 来源, 客户款号, 销售订单号 filters and columns
- Removed `编辑` button from list row actions
- Removed 国家 field

### V3.1.7
- 用线指示 import: removed 供应商不存在 validation check

### V3.1.9
- Copy dialogs added 创建时间 and 销售订单号 columns

### V3.2.27.4
- 千位符 + 右对齐 for amount/wage fields across 8 reports
- Production order deletion validation rework (下游单据 checks)
- Department/Workshop/Group cascade filtering for 员工实时报工表 + 3 other reports
- Cutting/bed task deletion rules
- Various deletion validation across 线外/缝制/尾整/松布 tasks

### V3.3.1
- 裁剪日产量明细表: 出库数 update logic fixed (sub-type differentiation)
- CPO deletion: mark-delete flag sets production order qty to 0
- Packing list: filter out CPO with qty=0; 吊牌条码 duplicate rules for different 生产订单+CPO combos

### Export Column Customization (持续)
- Ongoing: all reports respect column settings on export

---

## 6. Key Field Names & Validation Rules

### 6.1 Tab Data Flow (Style -> Production Order)

**Tabs copied from Production Order to new Style** (on 生效):
1. 基本信息 (partial: 款号, 款号名称, 款式名称, 客户, 品牌, 季度, 客户款号, 销售订单号)
2. 颜色尺码
3. 物料用量 (empty for new style from production order)
4. 色码用量 (empty)
5. 物料配色 (empty)
6. 物料配码 (empty)
7. 部位尺寸
8. 工艺要求
9. 用线指示 (copied from 配料说明)
10. 部位管理 (empty)
11. 生产工序

### 6.2 Critical Validation Rules

| Context | Rule | Error Message |
|---------|------|---------------|
| 新增款号 | 款号为空 | 新增失败 |
| 新增款号 | 款号已存在 | 新增失败 |
| 新增款号 | 客户为空 | 新增失败 |
| 款号唯一 (config=1) | 款号+客户款号+销售订单号 duplicate | 新增失败 + 提示 |
| 复制 | No style selected | 请选择一条数据 |
| 复制 | Cross-page selection | 请选择一条数据 (only current page counts) |
| 生产订单删除 | Has downstream documents | "存在下游单据时无法删除{code}, 请检查后重试" |
| 生产订单删除 | Downstream in production | "下游单据{code}已在生产中，无法删除" |
| 生产订单反生效 | 生产订单已生成 | "生产订单已经生成" |
| 生产订单反生效 | 生产计划已生成 | "订单生产计划已经生成" |
| 导入-物料 | 物料编号为空 | "物料编号不能为空" (red) |
| 导入-物料 | 物料编号不存在 | "未匹配到系统内已有物料档案，请先新增此物料后重试" |
| 导入-物料 | 运算符非法 | "运算符不存在" |
| 导入-物料 | 单件用量非数字 | "数值类型错误" |
| 导入-部位尺寸 | 尺码不匹配 | "未匹配到款号下已有尺码，请先新增此尺码后重试" |
| 导入-部位尺寸 | 部位及量法为空 | "部位及量法不能为空" |
| 导入-用线指示 | 色号不存在 | "色号不存在" |
| 导入-生产工序 | 工序编号重复 | "工序编号不可重复" |
| 导入-生产工序 | 工段不存在 | "工段不存在" |
| 导入-生产工序 | 级别不存在 | "工段不存在" (sic) |
| 保存-生产工序 | SAM/单价 >4dp | "数值类型错误(最多4位小数)" |
| 保存-生产工序 | 工序编号/名称/工段为空 | 保存失败 + 提示 |
| 部位尺寸-保存 | 部位及量法为空 | "部位及量法不能为空" |
| 松布中止 | 松布中状态 | "修改状态异常" |
| 线外任务删除 | 生产中状态 | "生产中的线外任务不能取消分配" |
| 尾整任务删除 | 尾整中状态 | "已生产的单据不允许删除" |
| 批量生成箱单 | 单箱件数缺失 | "{code}下单箱件数必填" |
| 新增物料 | 物料编号已存在 | "物料编号已存在" |
| 新增物料 | 必填字段为空 | 保存失败 + 标红提示 |
| 编辑物料 | 物料不存在 | "物料不存在，请先新增/选择物料" |

### 6.3 CPO Deletion Behavior (V3.3.1)

- CPO marked with delete flag via import or API sync
- Disappears from CPO list
- Production order count for that CPO becomes 0
- If only CPO on production order: order count = 0, still publishable
- 缝制/线外 task creation: production order greyed out when count=0
- 裁剪 task creation: still possible despite count=0
- 尾整 task: shown in dialog but cannot be dragged to create
- Re-importing CPO without delete flag: restores CPO data, production order count updates correctly

### 6.4 吊牌条码 Duplicate Rules (V3.3.1)

| Condition | 吊牌条码 |
|-----------|:---:|
| Same 生产订单, same 款, same CPO, same color, different size | Cannot duplicate |
| Same 生产订单, same 款, same CPO, different color, same size | Cannot duplicate |
| Same 生产订单, same 款, same CPO, different color, different size | Cannot duplicate |
| Same 生产订单, same 款, **different** CPO, same color, same size | **Can duplicate** |
| Same 生产订单, same 款, different CPO, other combos | Cannot duplicate |
| **Different** 生产订单, same 款, different CPO, same color, same size | **Can duplicate** |
| Different 生产订单, other combos | Cannot duplicate |
| Different 生产订单, different 款, different CPO | Cannot duplicate |

---

## 7. Known Bugs / Quirks

1. **单位 field mismatch**: Sales order生效 passes null for 单位; style assigns default "cm" -- new style's 单位 differs from source (Bug转任务926)
2. **Pivot export 千位符**: Not preserved on pivot export (marked "无法实现")
3. **用线指示 import -- 字母大小写**: Column header case must exactly match 颜色尺码 tab case; mismatch = import failure
4. **Post-deletion null pointer**: Deleting production order and then accessing orphaned downstream tasks causes null pointer errors in 裁剪/缝制/尾整/松布 task pages
5. **松布中止**: Cannot abort 松布中 status; "修改状态异常"
6. **裁剪任务 PAD端**: After task deleted, PAD scan prompts "裁剪床次任务不存在"
7. **尾整任务 PAD端**: Deleting task while PAD has it selected -> 报工提交 fails with "报工件数已超出尾整任务单分配件数"
8. **裁片出库**: 裁剪验片出库 and 委外验片出库 do not update 出库数/出库时间 in 裁剪日产量明细报表 (addressed in V3.3.1)
