# IMS ERP Production & Offline Module - Feature Knowledge Synthesis

## 1. Module Overview

This document synthesizes feature points from five extraction files covering:
- **Production Orders (生产订单)**: Order lifecycle management, tabs, permissions
- **Offline Module (线外模块)**: PC/PAD task management, assignment, reporting
- **Offline Proxy Reporting (线外代报工)**: PDA proxy workflow, scanning, employee/process selection
- **PAD Offline Reporting Station (PAD线外报工站)**: Scanning and batch reporting
- **PC Workstation Configuration (PC工作站配置)**: Workstation CRUD, role binding

---

## 2. State Machines & Business Rules

### 2.1 Production Order State Machine
```
草稿(Draft) --> 审核中(Under Review) --> 生效(Active) --> 已发布(Published) --> 生产中(In Production) --> 已完成(Completed)
     ^              |
     |    [反审核]    |
     +--------------+
```
- **反审核**: Status changes from 审核中 to 草稿; page becomes non-editable
- **生效**: Triggers 款号 generation rules (style-mode config dependent)
- Both 生效 and 已发布 statuses lock most edit fields

### 2.2 款号 (Style Number) Generation Rules (System Config: `style-mode`)
| Config Value | Rule | Behavior |
|---|---|---|
| 1 | 款号+客户款号+销售订单号 组合唯一 | 生效 does NOT generate new 款号 |
| 2 | 款号+客户款号 组合唯一 | 生效 MAY generate new 款号 if combo not exists |

**When style-mode=2 AND 款号 does not exist**: New 款号 created with status=草稿, data copied from tabs: 基本信息, 颜色尺码, 部位尺寸, 工艺要求, 生产工序, 配料说明

**When style-mode=2 AND 款号 exists**: No new 款号; incremental update of 颜色尺码 only (union of existing + new colors/sizes)

### 2.3 Offline Task State Machine
```
PC端: 保存 --> 未发布 ---> 已发布 (= PAD: 待分配)
PAD端: 待分配 -->[确认分配]--> 待生产 -->[首道工序扫描/出库]--> 生产中 -->[线外完成]--> 已完成 -->[恢复]--> 生产中
```
- Recovery allowed only within 3 months of completion
- Delete allowed for: 未发布, 已发布, 待生产 statuses
- Edit allowed for all statuses (未发布 through 已完成)

### 2.4 Production Order Permission by Status

| Button/Tab | Visible When Status |
|---|---|
| 复制 | All statuses |
| 删除 | 草稿, 审核中, 生效 |
| 反审核 | 审核中 only |
| 物料维护 | 生效, 已发布 |
| 唛架新增 | 生效, 已发布 |
| 唛架变更/复制/删除 | 审核中, 生效, 已发布 |
| 色码配置 | 草稿 only |
| 删除线外任务 | 未发布, 已发布, 待生产 |

### 2.5 Key System Configurations

| Config Key | Module | Description |
|---|---|---|
| `style-mode` | ALL | 款号 唯一校验 mode (1 or 2) |
| `cuttingTypeValid` | 生产唛架 | 裁片类型 必填校验 (0/1) |
| `markerCodeRatioSectionValid` | 生产唛架 | 唛架号/配比/段长 必填校验 (0/1) |
| `production:spt_without_arrange` | 线外 | 是否需要工序编排 (0/1) |
| `production:spt_add_sewing_section` | 线外 | 任务加取缝制工段 (0/1) |
| `production:spt_user_station_check` | 线外 | 操作员/工作站必填校验 (0/1) |
| `production:customize_outline_code` | 线外 | 线外任务单号自定义 (0/1) |
| `production:spt_procedure_arrange_mode` | 线外 | 工序编排模式 (0/1/2) |
| `production:work_report:page_control_user_scan` | 线外 | 报工员工卡扫描框显示 (0/1) |
| `production:spt_pad_user_report_work_model` | 线外 | 员工报工模式 (0=仅分配人, 1=分配人+未分配人) |
| `production:report_work_count_check` | 线外 | 报工数量是否允许超实际裁剪数 (0/1) |
| `cutting_piece_finish_check` | 线外 | 报工是否校验裁片验片 (0/1) |
| `wms:cuttingPieces:main_cut_can_out_confirm_in_offline_station` | 线外 | 主布能否在线外出库 (0/1) |

---

## 3. Page Structures & Field Names

### 3.1 Production Order Detail Tabs
```
基本信息 | 颜色尺码 | 部位尺寸 | 工艺要求 | 生产工序 | 物料信息 | 配料说明 | 吊牌管理 | 唛架管理 | 生产进度 | 装箱
```
Key fields (基本信息):
- 图片, 生产订单号, 款号, 款号名称, 款式名称, 客户, 品牌, 季度, 入仓期, 生产车间, 备注
- List fields: 客户生产计划单号, PO, Item Code, 客户款号, 销售订单号, 下单日期, 入仓期, 件数

### 3.2 Offline Task Card Fields
PC端: 线外任务单号 (SPT+YY+MMDD+NNN), 线外状态, 生产订单号, 款号, BUY, 成衣色称/尺码, 已分配数, 生产组别, 计划线外日期, 实际线外日期

PAD端 adds: 缝制组别(协同), 已完成数

### 3.3 Offline Task Detail Pages (PAD)

| Status | Available Buttons | Key Info |
|---|---|---|
| 待分配 | 保存, 确认分配 | 工序编排 (drag-drop工序/操作员/工作站) |
| 待生产 | 工序编排 | Shows assigned operators/workstations |
| 生产中 | 工作汇总, 工序编排, 线外完成, 编辑/保存 | 工序产量tab + 生产进度tab |
| 已完成 | 恢复 (within 3 months) | 产量只读展示, 筛选今日/昨日/本月 |

### 3.4 Workstation Configuration Fields
```
工作站编号, 工作站名称, 站位属性, 站位分类, 所属区域, 所属工段, 所属产线, 关联区域, 
设备类型, 绑定设备MAC地址, 理论节拍, 理论节拍单位, 状态, 备注, 条码关联
```
Workstation statuses: 启用, 作废, 停用

### 3.5 站位分类 by 工段 Type
- **裁剪工段**: 松布, 拉布, 开裁, 验片, 拼罗纹, 慰烫, 热转移印, 绣花, 印花, 花片收发
- **缝制工段**: 挂片, 分包, 配片, 车缝, 中查
- **尾整工段**: 水洗发出/接收, 车主唛, 打钮, 剪线, 新查, 整烫, 度尺, 复查, 一包, FQC, 二包, 验针, 返工, FQA

---

## 4. Validation Rules & Error Conditions

### 4.1 Production Order - Manual Add Validation
| Field | Error Message |
|---|---|
| 款号 empty | 请输入款号 |
| 客户款号 empty | 请输入客户款号 |
| 客户 empty | 请选择客户 |
| 品牌 empty | 请选择品牌 |
| 下单日期 empty | 请选择下单日期 |
| 入客仓期 empty | 请选择入客仓期 |
| 生产部门 empty | 请选择生产部门 |

### 4.2 Production Order - Edit Validation
- 款号 empty: "请输入款号"
- 客户 empty: "请选择客户"
- 品牌 empty: "请选择品牌"
- 生产车间 empty: "请选择生产车间"
- 客户款号/下单日期/入仓期 empty: "保存失败，客户款号、下单日期和入仓期不能为空！"

### 4.3 Color/Size Tab - 生效 Validation
- All color-size cells empty: "颜色尺码标签页下每个色码至少有一个大于0的对应件数"
- Per color-code at least one count > 0: 生效成功

### 4.4 Production Process Import Validation
- 客户款号 empty: 导入失败
- 工序编号/工序代码/工序名称/工段 empty: 导入失败
- 一级部位 empty + 二级部位 has value: 导入失败
- SAM value > 4 decimal places: "数值类型错误(最多4位小数)"
- SAM negative: "数值类型错误(最多4位小数)"
- SAM non-numeric: "数值类型错误(最多4位小数)"
- All data-dictionary fields (工段, 部位, 设备, 辅助工具, 级别): not-in-dict = 导入失败

### 4.5 Marker Management Validation
- 唛架号 duplicate: "唛架号不能重复, {唛架号}"
- 段长 <= 0: "段长需大于0"
- 裁片类型 empty (when cuttingTypeValid=1): "裁片类型不能为空"
- Marker号 unique within same production order only

### 4.6 Offline Task Validation
- 生产组别, 计划线外日期: required fields
- 任务单号 duplicate: "任务单号重复，请修改"
- 分配数 > 待分配数: maximum clamped to 待分配数 (新增不允许超分配; 编辑可以)
- 色/码卡片待分配数=0: 显示"分配完毕"标识; 0<待分配数<订单数量: no marker; 已分配数>订单数量: "超出分配"

### 4.7 Offline Process Assignment Validation (PAD)
- 产量工序 not selected: 保存失败
- 所有工序 no 制程 selected: 确认分配失败
- 操作员 or 工作站 at least one required (depends on config `production:spt_user_station_check`)

### 4.8 Proxy Reporting (代报工) Validation
- 工序+员工 both unselected: 开始扫描 disabled
- 系数 empty: "系数不能为空" / "请分配系数"
- 系数 = 0: "系数需大于零且小数位数最大两位"
- 扎卡不存在: "裁片扎卡不存在" / "未查询到对应扎卡"
- 扎卡 not 本单: "请扫描本单下扎卡"
- 重复扎卡: "同扎号扎卡请勿重复报工"
- 工序只许主布报工 + 辅布: "只允许主布报工"
- 扎卡未验片: "扎卡未验片完成或未免检"
- 工序编排已调整: "工序编排已调整，请检查后重试"
- 员工 not assigned to process: "{工号}被分配所选工序"

### 4.9 Workstation Configuration Validation
- 工作站编号/名称/站位分类/设备类型/所属工段/所属产线/状态: required
- 工作站编号 duplicate: "工作站编号重复"
- 理论节拍: "请输入0-10000000之间的数字,最多2位小数"
- Role-bound workstation: "当前用户无该工作站权限"

---

## 5. Cross-Module Interactions

### 5.1 Production Order --> Style Number Management (款号管理)
- 生产订单生效 creates/updates 款号 in 技术模块
- Data sync: 基本信息, 颜色尺码, 部位尺寸, 工艺要求, 生产工序, 配料说明
- 物料用量tab, 色码用量tab, 物料配色tab, 物料配码tab: displayed empty in new 款号

### 5.2 Production Order --> Material Info (物料信息)
- Read-only display; queries 款号管理 in real-time
- "物料维护" button navigates to 技术-款号管理-款号详情-物料需求-物料用量tab

### 5.3 Production Order --> Cutting Tasks
- 裁剪开单数 appears when 裁剪任务 created
- 裁剪实裁数 appears when 扎卡 generated
- 裁剪正品数 (验片数) updates when 验片任务 completed

### 5.4 Offline Task <--> Sewing Task (缝制任务)
- 已发布 缝制任务 generates 待分配缝制任务单
- Deleting published sewing task should sync-delete offline task (currently broken)
- 缝制组别(协同) optional field for cross-coordination

### 5.5 Offline Task <--> Production Order
- 已发布 生产订单 generates 待分配生产订单 (only if total 待分配数>0)
- 生产订单反发布: reverse flow not fully defined yet
- 生产进度tab: 线外完成数 synced from offline reporting

### 5.6 Offline Reporting --> Production Reports
- PC 生产全流程报表: synced 线外完成数
- PC 生产订单详情-生产进度tab: synced 线外完成数
- PAD 线外组长-生产进度tab: synced 完成件数
- PAD 扎卡路径查询: synced 报工扎卡信息

### 5.7 Offline Module <--> WMS (Warehouse)
- 裁片出库: scans carrier boxes; checks `wms:cuttingPieces:main_cut_can_out_confirm_in_offline_station` for 主布 restriction
- 裁片入库: tray binding, storage location selection
- 裁片箱查询: linked to 线外任务 for process range display

### 5.8 Offline Module <--> Cutting Module
- `cutting_piece_finish_check`: 报工 validates 裁片验片 completion
- 主布/辅布 type check: `cutType:"1"` = 主布, `cutType:"2"` = 辅布
- 工序 "只许主布报工" flag controls material type acceptance

### 5.9 Workstation <--> Role Management
- Workstations can bind roles; only bound roles can select workstation
- Non-bound role: "当前用户无该工作站权限" on PDA login
- Role deleted after binding: user keeps access but workstation removed from dropdown

---

## 6. Test Scenarios

### 6.1 Permission Tests (P0)
- Tab visibility based on role menu permissions (吊牌管理, 物料信息, 唛架管理)
- Button visibility by role + order status combination (新增, 复制, 删除, 反审核, 物料维护)
- 线外代报工 手工录入 button permission

### 6.2 State Machine Tests (P0)
- Production order: 草稿 -> 审核中 -> 生效 -> 已发布 -> 生产中 -> 已完成
- 反审核 flow: 审核中 -> 草稿 (page non-editable)
- 生效 triggers 款号 generation
- Offline task: 未发布 -> 已发布 -> 待分配 -> 待生产 -> 生产中 -> 已完成
- Recovery within/after 3 months
- Delete in each valid status

### 6.3 款号 Generation Tests (P0)
- style-mode=1: no new 款号 on 生效
- style-mode=2: new 款号 when combo not exists; incremental color/size when exists
- 复制生产订单 + 款号 exists/not-exists scenarios
- Color/size union logic across multiple production orders

### 6.4 Color/Size Configuration Tests (P0)
- Add/delete color and size rows
- Enable/disable colors and sizes
- Sort order validation
- Cross-tab sync: 颜色尺码 <-> 配料说明 (color dynamic columns), 颜色尺码 <-> 部位尺寸 (size dynamic columns)
- 生效 validation: at least one >0 count per color-code

### 6.5 Import Tests (P0)
- Format validation: only xlsx/xls accepted
- Required field empty (all + per-field)
- Data dictionary value validation (工段, 部位, 设备, etc.)
- SAM/单价 numeric validation (negative, >4 decimals, non-numeric)
- Duplicate 工序编号: 导入失败
- Case sensitivity: 客户款号 (暂不考虑), 基础工序代码 (case-sensitive OK)

### 6.6 Offline Task Assignment Tests (P0)
- Drag production order to create new task card
- Assign by 成衣色称 vs. 尺码 dimension
- Mixed assignment dimensions validation
- 分配数 modification (max capped at 待分配数 for new; allowed to exceed for edit)
- 分配完毕/超出分配 indicator display
- Multiple groups same/different 缝制任务 assignment

### 6.7 Offline Process Arrangement Tests (P1)
- Drag-drop process reordering
- Operator assignment: single/multiple, same/different groups
- Workstation assignment: single/multiple
- Process merging (制程 inheritance rules)
- Sync process from production order
- 确认分配: 制程 + 产量工序 required

### 6.8 Proxy Reporting (代报工) Tests (P1)
- Employee scanning validation (no user, no archive, left-job)
- Process availability by selected employee(s) - all 10+ combinatorial cases
- Employee availability by selected process(es) - all combinatorial cases
- Report allocation coefficient: default(1), <0, =0, >2 decimals
- Auto-calculate ratio: single employee=100%, multi=coefficient/sum
- 开始扫描 disabled unless both 工序+员工 selected

### 6.9 Scan & Batch Report Tests (P1)
- Material type: 裁片箱/面料托盘/辅料箱/成品箱
- State checks: in-storage, not-received, invalidated
- Duplicate scan: allowed, not repeated
- 主布/辅布 type check with 只许主布报工 flag
- 裁片验片 completion check
- Process/employee re-arranged during scanning
- Partial process already reported (二次确认)
- Same 扎号 different 裁片类型 duplicate check
- 报工数量 vs. actual 裁剪件数 (config `report_work_count_check`)

### 6.10 Workstation Configuration Tests (P1)
- CRUD with all required field validation
- 站位分类 dropdown filtered by 工段 type
- Import with all validation combinations
- Status transitions: 启用 <-> 停用, -> 作废 -> 启用
- Workstation number uniqueness (case-insensitive)
- Role binding/unbinding effects on PDA login
- 理论节拍 numeric validation

### 6.11 Cross-Module Sync Tests (P2)
- 生产订单生效 -> 款号管理 data verification (all tabs)
- 配料说明同步 -> 物料配色 data refresh (二次确认)
- 唛架号 default from 系统唛架号
- PAD报工 -> PC/PAD detail pages count sync
- 生产进度tab data chaining: 裁剪 -> 线外 -> 缝制 -> 尾整
- Offline task delete cascading (PC + PAD)

### 6.12 Resource Data Sources
- 客户: 档案-客户
- 品牌: 档案-品牌
- 生产部门: 部门管理 (类型=车间)
- 生产组别: 组织架构>部门管理 (工段=线外工段, 部门类型=组别)
- 操作员: 部门管理 (部门类型=车间&组别)
- 工作站: 工作站配置 (所属工段=线外工段, 设备类型=PAD)
- 制程: 基础制程 (工段=线外工段)
- 生产订单列表 (复制): 已生效&已发布&已完成 status
- 款号列表 (复制配料说明): 生效 status only
- 样衣列表 (复制工艺要求): 生效&已发布 status only
- 关联区域: 仓库管理 (面料/辅料/裁片/成品仓) + 系统字典 (生产/线外/设备)

### 6.13 Data Dictionary Dependencies
- 站位分类 (依赖上级: 工段类型)
- 设备类型: PLC, PC, PAD, PDA, ABB, 裁床, 台板, 松布机, 拆箱机, 叠盘机, 码垛机, 辅料接收, AGV
- 站位属性: SPS(特种工艺站), CSS(裁片分拣站), SS(缝制站), FS(后整站), IS(整烫站), IPS(初始包装站), FPS(终包装站), IQS(来料QC站), IPQS(过程QC站), FQS(终检QC站), AS(全能站)
- 币种: $, $, HK$, $, JPY$

---

## 7. Key Formulas

| Formula | Context |
|---|---|
| 件数 (唛架) | 配比之和 x 层数 |
| 总米长 (唛架) | 段长 x 层数 |
| 分配占比 | 个人系数 / 所有员工系数之和 |
| 金额 (吊牌) | 单价 x 件数 |
| 线外任务单号格式 | SPT + YY + MMDD + NNN (流水号) |
| 工作站编号格式 | 工厂编码 + 区域编码 + 站位分类编码 + 设备类型编号 + 4位流水号 |
| 生产率 | 报工件数 (实际产量 = 调整后) |
