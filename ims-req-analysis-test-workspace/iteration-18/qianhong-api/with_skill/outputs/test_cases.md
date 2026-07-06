# 千虹接口文档 测试用例

> 模板版本：1.0 | 生成日期：2026-07-03

---

## 文档信息

| 字段 | 内容 |
|------|------|
| 依据需求 | 千虹接口文档 v3.0.1 (D:\需求文档\千虹接口文档.docx) |
| 生成版本 | 规则 1.0 |
| RAG 检索 | 命中 12 条 — 物料状态机、载具生命周期、WMS锁定规则、入库→绑定→出库链、枚举定义等 |
| 测试范围 | 千虹 IMS v3.x API/SPI 接口全量测试（15个端点） |
| 结构说明 | 复杂型（>30检查点）：H2(模块) → H3(接口) → H4(场景) → H5(检查点) |
| 待澄清汇总 | 12 条 |
| 复杂度 | 复杂 |

---

## 知识库检索摘要

从知识库检索到的相关上下文：

1. [domain] **WMS物料状态机**: 待收货→已收货→已入库→出库扣减。与本文档4.4→4.6→4.5→4.6流转一致
2. [domain] **WMS载具生命周期**: 初始⇄已上架⇄已下架。匹配4.1载具查询的carrierStatus枚举
3. [domain] **WMS锁定规则**: 已备料载具阻止收货/绑定/解绑。与4.5绑定操作前置条件对应
4. [domain] **IMS通用响应结构**: code/message/traceId/data。与文档3.4节完全一致
5. [domain] **Bearer Token认证**: Authorization: Bearer {token}。匹配3.2节
6. [domain] **千虹客户差异**: 主线子集，仅缺gm.平板#1，其他13模块一致
7. [domain] **SIT环境**: test.fj.dtsimple.pro，企业千虹_测试可选
8. [domain] **枚举命名规范**: 统一枚举值全局统一，预留扩展空间
9. [domain] **SemVer版本管理**: vX.Y.Z格式，与文档版本管理一致
10. [bug] **字段名冲突模式**: 同一字段名在不同表中含义不同（如deptName=Long vs String）
11. [best_practice] **异步接口测试模式**: API受理+SPI回调双端验证
12. [best_practice] **接口幂等性**: 相同requestId重复提交应有幂等保护

---

## 需求追溯表

| 需求段落 | 用例编号范围 | 覆盖说明 |
|----------|--------------|----------|
| 3.1 通信协议 | A-001~A-112 | HTTP POST JSON规范验证 |
| 3.2 鉴权方式 | A-001~A-011 | Token获取与Bearer鉴权全场景 |
| 3.3 通用请求头 | A-008~A-011 | Authorization+Metas-Request-Id验证 |
| 3.4 通用响应结构 | A-012, A-035, A-046 | code/message/traceId/data结构校验 |
| 3.5 API/SPI响应区别 | A-028~A-034, A-056~A-062 | 同步受理vs异步回调验证 |
| 4.0 获取访问令牌 | A-001~A-007 | 认证全场景（正常+异常+边界） |
| 4.1 载具信息查询 | A-012~A-018 | 查询深度+类型+状态全覆盖 |
| 4.2 库区查询 | A-035~A-045 | 模糊+属性+类型查询 |
| 4.3 载具任务执行 | A-019~A-027 | 3种任务类型+异常+并发 |
| 4.4 物料清单同步 | A-046~A-055 | 同步+初始化库存+扩展属性 |
| 4.5 货载绑定 | A-063~A-075 | 4种操作组合+前置条件+异常 |
| 4.6 物料出入库 | A-076~A-090 | stock/flow+inbound+outbound全覆盖 |
| 4.7 物料库存查询 | A-091~A-096 | 分页+筛选+边界 |
| 5.1 SPI载具任务回调 | A-028~A-034 | FINISHED/ERROR/超时/重试 |
| 5.2 SPI物料同步回调 | A-056~A-062 | SUCCESS/FAILURE/部分成功 |
| 生产订单同步 | A-097~A-103 | 最小必填+完整+异常 |
| 缝制任务单同步 | A-104~A-109 | 最小必填+关联+异常 |
| 工序产量视图 | A-110 | 视图字段结构 |
| 质检详情视图 | A-111 | 视图字段结构 |
| 6.1 物料类型枚举 | A-046~A-054 | fabric/trim/garment/cuttingPieces |
| 6.5 载具任务类型枚举 | A-019~A-023 | PUT_ON/PUT_DOWN/MOVE_OUTSIDE |
| 6.6 载具任务状态枚举 | A-028~A-034 | 5种状态 |
| 6.7 同步状态枚举 | A-056~A-062 | ACCEPTED/SUCCESS/FAILURE |
| 6.9 载具状态枚举 | A-012~A-018 | 7种状态 |
| 6.15 出入库类型枚举 | A-076~A-082 | 1入库/2出库 |
| 6.20 载具类型编码枚举 | A-012~A-018 | 6种载具类型 |

---

## 核心流程测试

### 流程1：完整物料生命周期 F-01

- ERP获取Token（POST /public/auth/authorization，有效凭证）
  - 返回code=0，data为Bearer Token字符串
  - Token用于后续所有API的Authorization头
- 同步物料清单（POST /material/item/sync）
  - 提交fabric类型物料清单，initInventory=false
  - 返回code=0，data.syncState=ACCEPTED
  - IMS异步处理完成后通过SPI回调通知syncState=SUCCESS
- 物料入库（POST /material/item/stock/flow, flowType=1）
  - 提交itemNo+itemAmount
  - 返回code=0，data.status=ACCEPTED
- 查询载具信息确认可用（POST /carrier/info, depth=1）
  - 返回载具基本信息，carrierBindStatus=0(空)
- 将物料绑定到载具（POST /carrier/item/link, BIND+INCR）
  - 提交carrierNo+itemNo
  - 返回code=0，data.status=ACCEPTED
- 下发载具上架任务（POST /carrier/task/execute, PUT_ON）
  - 提交carrierNo+sourceLocationCode+targetSpaceCode
  - 返回taskId, taskState=ACCEPTED
- IMS异步执行完成后SPI回调任务完成
  - taskState=FINISHED, 含finishTime
- 物料出库（POST /material/item/stock/flow, flowType=2）
  - 返回code=0，data.status=ACCEPTED
- 查询库存确认出库结果（POST /material/item/inventory）
  - inventory减少对应数量

### 流程2：载具全量替换绑定 F-02

- 载具已有物料A（通过流程1步骤1-5完成绑定）
- 查询载具确认当前绑定（POST /carrier/info, depth=3）
  - itemList含物料A
- 全量绑定新物料B和C（POST /carrier/item/link, BIND+FULL）
  - itemList=[物料B, 物料C]
  - 返回code=0
- 再次查询载具（POST /carrier/info, depth=3）
  - itemList仅含物料B和C，物料A已解绑

### 流程3：物料出入库约束验证 F-03

- 同步新物料但未入库（initInventory=false）
- 尝试绑定该物料到载具（POST /carrier/item/link, BIND+INCR）
  - 预期失败：物料未入库
- 先执行入库（POST /material/item/stock/flow, flowType=1）
- 再次尝试绑定
  - 预期成功
- 尝试出库（POST /material/item/stock/flow, flowType=2）
  - 预期成功（已入库后允许出库）

### 流程4：生产订单+缝制任务同步 F-04

- 同步生产订单（POST /production/v3/save）
  - 含productionOrderNo+styleCode+detailList+procedureList
  - 返回成功（响应结构待文档补充）
- 同步缝制任务单（POST /sewing/v3/save）
  - sewingCode关联上述productionOrderNo
  - 返回成功
- 关联不存在的生产订单
  - 预期失败或告警

---

## 详细功能点测试

## 认证模块

### 获取访问令牌 (POST /public/auth/authorization)

#### 正常获取Token A-001 P0

- 提交username=`admin`、password=`IMS@2026`
- 响应HTTP 200，code=0，message=`success`
- data字段为非空字符串（Bearer Token）
- token格式为 `IMS-v3-token-` 前缀

#### 错误密码获取Token A-002 P1

- 提交username=`admin`、password=`WrongPassword123`
- 响应HTTP 401或200+code非0
- message指明认证失败原因
- 不返回有效token

#### 不存在用户获取Token A-003 P1

- 提交username=`nonexistent_user_20260703`、password=`anypassword`
- 响应失败，不泄露用户是否存在（与A-002返回相同的错误信息格式）
- 不返回有效token

#### 空凭证获取Token A-004 P2

- 提交username=``（空字符串）、password=``（空字符串）
- 响应HTTP 400或422，code非0
- 错误信息指明缺失必填字段

#### 缺失username字段 A-005 P2

- 仅提交password=`IMS@2026`，不传username
- 响应HTTP 400或422
- 错误信息指明缺失username

#### 缺失password字段 A-006 P2

- 仅提交username=`admin`，不传password
- 响应HTTP 400或422
- 错误信息指明缺失password

#### Token格式验证 A-007 P2

- 正常获取Token后验证data字段
- data不为空、不为null、类型为String
- data不含特殊字符（如换行符、引号未闭合）

### Token鉴权验证

#### 无Token访问业务API A-008 P0

- 请求 POST /wms/v3/carrier/info，不携带Authorization头
- 响应HTTP 401
- message指明未认证

#### 过期Token访问业务API A-009 P1

- 使用已知过期token请求 POST /wms/v3/carrier/info
- 响应HTTP 401
- message指明token过期

#### 篡改Token访问业务API A-010 P2

- Authorization头设置为 `Bearer fake-invalid-token-12345`
- 响应HTTP 401
- message指明token无效

#### Metas-Request-Id可选性 A-011 P2

- 请求不含Metas-Request-Id头
- 正常返回（该头为推荐非必填，不强制）

---

## WMS载具模块

### 载具信息查询 (POST /wms/v3/carrier/info)

#### 查询存在载具(depth=3,完整信息) A-012 P0

- 提交carrierNo=`PALLET-001`，携带有效token
- 响应code=0，data含carrierNo、carrierTypeCode、carrierBindStatus、carrierStatus
- currentTask含taskId、taskType、taskState
- itemList含物料明细（itemNo、materialExtendCode、materialName、qty等）

#### 查询空载具(depth=1,最小信息) A-013 P1

- 提交carrierNo=空载具条码、depth=1
- 响应仅含载具基本信息
- carrierBindStatus=0
- 不含currentTask和itemList

#### 查询已绑定载具(depth=3,含物料) A-014 P1

- 提交carrierNo=已绑定物料的载具、depth=3
- 响应itemList为非空数组
- 每个物料含itemNo、materialExtendCode、materialName、qty、unit等

#### 查询不存在的载具 A-015 P2

- 提交carrierNo=`NONEXIST-CARRIER-999`
- 响应code非0（预期404语义），或data为null
- message指明载具不存在

#### 空carrierNo查询 A-016 P2

- 提交carrierNo=``（空字符串）
- 响应HTTP 400或422
- 错误信息指明carrierNo为必填

#### depth=0查询 A-017 P2

- 提交carrierNo=`PALLET-001`、depth=0
- 响应使用默认值depth=3，或返回400
- 若使用默认值则返回完整信息

#### depth超范围查询 A-018 P2

- 提交carrierNo=`PALLET-001`、depth=99
- 响应使用默认值depth=3，或返回400
- 若使用默认值则返回完整信息（不崩溃）

### 载具任务执行下发 (POST /wms/v3/carrier/task/execute)

#### 上架任务下发 A-019 P0

- 提交taskType=`PUT_ON`、carrierNo=`PALLET-001`、sourceLocationCode=`WCS-A-01-01`、targetSpaceCode=`ZONE-STORAGE`
- 响应code=0，data含taskId、taskType=PUT_ON、taskState=ACCEPTED

#### 下架任务下发 A-020 P1

- 提交taskType=`PUT_DOWN`、carrierNo=`PALLET-001`、sourceLocationCode=`WCS-A-01-01`、targetSpaceCode=`ZONE-SHIPPING`
- 响应taskType=PUT_DOWN、taskState=ACCEPTED

#### 库外移动任务下发 A-021 P1

- 提交taskType=`MOVE_OUTSIDE`、carrierNo=`PALLET-001`、sourceLocationCode=`WCS-A-01-01`、targetSpaceCode=`ZONE-OUTSIDE`
- 响应taskType=MOVE_OUTSIDE、taskState=ACCEPTED

#### 带bizTaskId的任务下发 A-022 P1

- 提交taskType=`PUT_ON`、carrierNo=`PALLET-001`、sourceLocationCode=`WCS-A-01-01`、targetSpaceCode=`ZONE-STORAGE`、bizTaskId=`BIZ-001`
- 响应正常，bizTaskId被接受

#### 非法taskType A-023 P2

- 提交taskType=`INVALID_TYPE`、carrierNo=`PALLET-001`
- 响应HTTP 400或422
- 错误信息指明taskType不在枚举范围内

#### 空carrierNo A-024 P2

- 提交taskType=`PUT_ON`、carrierNo=``
- 响应HTTP 400或422
- 错误信息指明carrierNo为必填

#### 空sourceLocationCode A-025 P2

- 提交taskType=`PUT_ON`、carrierNo=`PALLET-001`、sourceLocationCode=``
- 响应HTTP 400或422
- 错误信息指明sourceLocationCode为必填

#### 空targetSpaceCode A-026 P2

- 提交taskType=`PUT_ON`、carrierNo=`PALLET-001`、sourceLocationCode=`WCS-A-01-01`、targetSpaceCode=``
- 响应HTTP 400或422
- 错误信息指明targetSpaceCode为必填

#### 同一载具重复下发任务 A-027 P3

- 对同一carrierNo短时间内连续下发两次任务
- 第二次应返回错误（载具已有进行中任务）或排队处理
- 不产生数据混乱

### 载具任务SPI回调

#### SPI回调上架完成 A-028 P0

- IMS回调ERP：taskType=PUT_ON、taskState=FINISHED
- 回调体含taskId、carrierNo、startPositionCode、endPositionCode、finishTime
- finishTime格式为ISO 8601

#### SPI回调下架完成 A-029 P1

- IMS回调ERP：taskType=PUT_DOWN、taskState=FINISHED
- 含完整回调字段

#### SPI回调库外移动完成 A-030 P1

- IMS回调ERP：taskType=MOVE_OUTSIDE、taskState=FINISHED
- 含完整回调字段

#### SPI回调任务异常/取消 A-031 P2

- IMS回调ERP：taskState=CANCEL或taskState=ERROR
- ERP应能正确处理非FINISHED状态
- 不因非FINISHED状态崩溃

#### SPI回调ERP超时(>5s) A-032 P2

- ERP模拟响应时间>5秒
- IMS应触发重试机制
- 重试最多3次，采用指数退避

#### SPI回调重试后成功 A-033 P2

- 第1次回调ERP返回非200
- 第2次回调ERP返回200+code=0
- IMS不再重试

#### SPI回调ERP持续失败(3次全失败) A-034 P3

- ERP持续返回非200或超时
- IMS 3次重试后停止，记录失败日志
- 不无限重试

---

## WMS库区模块

### 库区查询-模糊 (POST /wms/v3/warehouse/space)

#### 库区模糊查询 A-035 P0

- 提交warehouseSpaceCode=`ZONE`（模糊匹配）
- 响应的data数组包含编码含ZONE的库区
- 每个库区含warehouseSpaceCode、warehouseSpaceName、warehouseCode等

#### 库区属性精准匹配 A-036 P1

- 提交spaceAttributes=[{"attrKey":"RECEIVING","attrVal":"收货区"}]
- 响应仅包含匹配属性的库区
- 若存在多个属性匹配的库区则全部返回

#### 空参数查询所有库区 A-037 P1

- 不提交任何参数（空JSON对象）
- 响应返回所有启用的库区
- data为数组

#### 不存在的库区编码 A-038 P2

- 提交warehouseSpaceCode=`NONEXIST_SPACE_999`
- 响应data为空数组，不报错
- code仍为0

#### 空spaceAttributes数组 A-039 P2

- 提交spaceAttributes=[]
- 等同于不过滤属性，返回所有匹配库区编码的库区
- 不因空数组报错

#### 禁用库区过滤 A-040 P2

- 对比查询结果中是否包含warehouseSpaceStatus=1的库区
- 预期：若模糊查询不自动过滤禁用，则包含；确认文档意图（待澄清 T-05）

### 库区查询-按仓库类型 (POST /wms/v3/warehouse/space/list)

#### 按面料仓类型查询 A-041 P0

- 提交warehouseTypeCode=`A`
- 响应data数组，每个元素含warehouseSpaceCode、warehouseSpaceName
- 不返回其他仓库类型的库区

#### 按裁片仓类型查询 A-042 P1

- 提交warehouseTypeCode=`C`
- 响应仅含裁片仓库区

#### 按辅料仓类型查询 A-043 P2

- 提交warehouseTypeCode=`G`
- 响应仅含辅料仓库区

#### 非法仓库类型 A-044 P2

- 提交warehouseTypeCode=`X`
- 响应HTTP 400或返回空数组
- 不崩溃

#### 缺失warehouseTypeCode A-045 P2

- 不传warehouseTypeCode
- 响应HTTP 400或422
- 错误信息指明warehouseTypeCode为必填

---

## WMS物料模块

### 物料物品清单同步 (POST /wms/v3/material/item/sync)

#### 面料清单同步(不初始化库存) A-046 P0

- 提交requestId=UUID、itemType=`fabric`、initInventory=false
- itemList含至少1条物料记录（itemNo、materialExtendCode、materialName、batchNo、itemUnit必填）
- 响应code=0、data.success=true、data.syncState=ACCEPTED、data.requestId匹配

#### 面料清单同步(初始化库存) A-047 P1

- 提交requestId=UUID、itemType=`fabric`、initInventory=true
- itemList含物料记录
- 响应正常，物料同步后自动入库

#### 辅料清单同步 A-048 P1

- 提交itemType=`trim`
- 响应正常接受（trim扩展属性待后续补充）

#### 含完整扩展属性的面料同步 A-049 P1

- itemList中物料含完整扩展属性（vatCode、lotCode、fabricNo、breadthValue、breadthUnit、weightValue、weightUnit、ingredient、needInspection、purveyor、incomingDate等）
- 响应正常，扩展属性被接受

#### 缺失requestId A-050 P2

- 不传requestId
- 响应HTTP 400或422
- 错误信息指明requestId为必填

#### 缺失itemType A-051 P2

- 不传itemType
- 响应HTTP 400或422
- 错误信息指明itemType为必填

#### 空itemList A-052 P2

- 提交itemList=[]
- 响应正常接受（空清单同步）或返回400
- 明确行为（待澄清 T-06）

#### itemNo重复 A-053 P2

- itemList中两个物料使用相同itemNo
- 响应应处理重复：拒绝或去重
- 不产生脏数据

#### 非法itemType A-054 P2

- 提交itemType=`invalid_type`
- 响应HTTP 400或422
- 错误信息指明itemType不在枚举范围

#### 相同requestId重复提交 A-055 P3

- 使用相同requestId提交两次完全相同的请求
- 第二次应返回幂等结果（成功或提示重复）
- 不产生重复数据

### 物料清单同步SPI回调

#### SPI回调同步成功 A-056 P0

- IMS回调ERP：syncState=SUCCESS
- 回调体含requestId、successList（非空数组）、failureList（空数组）
- successList含所有同步成功的itemNo

#### SPI回调同步失败 A-057 P1

- IMS回调ERP：syncState=FAILURE
- failureList含失败物料编号列表
- 每个失败物料应说明失败原因（待确认回调体是否含失败原因字段，T-07）

#### SPI回调部分成功 A-058 P1

- IMS回调ERP：syncState=FAILURE
- successList和failureList均有数据
- 成功和失败物料分别列出

#### SPI回调缺少requestId A-059 P2

- IMS回调中缺少requestId
- ERP应能处理或返回错误
- 不崩溃

#### SPI回调非法syncState A-060 P2

- syncState=INVALID_STATE
- ERP应能处理未知状态
- 不因未知状态崩溃

#### SPI回调空列表 A-061 P2

- successList=[] 且 failureList=[]
- 与syncState的矛盾处理（SUCCESS+空successList? 待澄清 T-08）

#### SPI回调超时+重试 A-062 P3

- 同A-032~A-034的SPI重试逻辑
- 针对物料同步回调的重试验证

### 货载绑定/解绑 (POST /wms/v3/carrier/item/link)

#### 增量绑定(BIND+INCR) A-063 P0

- 载具已有物料A，提交bindType=BIND、linkMode=INCR、itemList=[物料B]
- 响应code=0，data.status=ACCEPTED
- 查询载具确认载具上同时有物料A和物料B

#### 全量绑定(BIND+FULL) A-064 P0

- 载具已有物料A和物料B，提交bindType=BIND、linkMode=FULL、itemList=[物料C, 物料D]
- 响应正常
- 查询载具确认仅含物料C和物料D，物料A和B已解绑

#### 增量解绑(UNBIND+INCR) A-065 P1

- 载具已有物料A、B、C，提交bindType=UNBIND、linkMode=INCR、itemList=[物料A]
- 响应正常
- 查询载具确认仅含物料B和物料C

#### 全量解绑(UNBIND+FULL) A-066 P1

- 载具已有物料A、B，提交bindType=UNBIND、linkMode=FULL，不传itemList
- 响应正常
- 查询载具确认carrierBindStatus=0，无绑定物料

#### 绑定未入库物料 A-067 P1

- 提交bindType=BIND、linkMode=INCR、itemList中itemNo尚未入库
- 响应应拒绝（违反R003：物料须已入库）
- 错误信息指明物料未入库

#### 绑定不存在的物料 A-068 P1

- 提交itemNo=`NONEXIST_ITEM_999`
- 响应应拒绝
- 错误信息指明物料不存在

#### 缺失carrierNo A-069 P2

- 不传carrierNo
- 响应HTTP 400或422
- 错误信息指明carrierNo为必填

#### 缺失bindType A-070 P2

- 不传bindType
- 响应HTTP 400或422
- 错误信息指明bindType为必填

#### 非法bindType A-071 P2

- 提交bindType=`INVALID`
- 响应HTTP 400或422
- 错误信息指明bindType不在枚举范围

#### 非法linkMode A-072 P2

- 提交linkMode=`INVALID`
- 响应HTTP 400或422
- 错误信息指明linkMode不在枚举范围

#### UNBIND+FULL+传itemList(参数矛盾) A-073 P2

- 提交bindType=UNBIND、linkMode=FULL、itemList=[物料A]
- 文档定义此场景不传itemList，传了应如何处理？
- 预期：拒绝（参数矛盾）或忽略itemList执行全量解绑（待澄清 T-09）

#### BIND+INCR+空itemList A-074 P2

- 提交bindType=BIND、linkMode=INCR、itemList=[]
- 无物料可追加
- 预期：拒绝或正常返回但无变化（待澄清 T-10）

#### 已绑定物料重复绑定到同一载具 A-075 P3

- 载具已有物料A，BIND+INCR追加物料A
- 预期：去重或拒绝重复绑定
- 不产生重复记录

### 物料出入库-通用 (POST /wms/v3/material/item/stock/flow)

#### 物料入库(flowType=1) A-076 P0

- 提交requestId=UUID、flowType=`1`、itemList含已同步但未入库的itemNo
- 响应code=0，data.status=ACCEPTED

#### 物料出库(flowType=2) A-077 P1

- 提交requestId=UUID、flowType=`2`、itemList含已入库的itemNo
- 响应code=0，data.status=ACCEPTED

#### 未入库物料出库(flowType=2) A-078 P1

- 提交flowType=`2`、itemList中itemNo未入库
- 响应应拒绝（违反R001：先入库后出库）
- 错误信息指明物料未入库

#### 非法flowType A-079 P2

- 提交flowType=`3`
- 响应HTTP 400或422
- 错误信息指明flowType不在枚举范围

#### 缺失flowType A-080 P2

- 不传flowType
- 响应HTTP 400或422
- 错误信息指明flowType为必填

#### 空itemList A-081 P2

- 提交itemList=[]
- 响应应拒绝或返回空操作确认（待澄清 T-11）

#### 已出库物料重复出库 A-082 P3

- 对已出库物料再次提交flowType=2
- 响应应拒绝（库存不足）
- 错误信息指明库存不足

### 物料入库-独立端点 (POST /wms/v3/material/item/inbound)

#### 独立入库(正常) A-083 P0

- 提交requestId=UUID、itemList含有效itemNo+itemAmount
- 响应code=0，data.status=ACCEPTED

#### 独立入库(空itemList) A-084 P1

- 提交itemList=[]
- 响应同通用端点行为

#### 独立入库(缺失requestId) A-085 P2

- 不传requestId
- 响应HTTP 400或422

#### 独立入库(itemNo不存在) A-086 P2

- itemList中itemNo不存在
- 响应应拒绝
- 错误信息指明物料不存在

### 物料出库-独立端点 (POST /wms/v3/material/item/outbound)

#### 独立出库(正常) A-087 P0

- 提交requestId=UUID、itemList含已入库itemNo
- 响应code=0，data.status=ACCEPTED

#### 独立出库(未入库物料) A-088 P1

- itemList中itemNo未入库
- 响应拒绝（违反R001）

#### 独立出库(缺失requestId) A-089 P2

- 不传requestId
- 响应HTTP 400或422

#### 独立出库(出库数量=0) A-090 P2

- itemAmount=0
- 响应应拒绝（无效数量）或正常返回（0出库无意义但可能接受）

### 物料库存查询 (POST /wms/v3/material/item/inventory)

#### 库存查询(面料仓) A-091 P0

- 提交warehouseTypeCode=`A`
- 响应code=0，data含page、size、total、data[]
- data[]中每个物料含itemNo、materialExtendCode、materialName、inventory等

#### 库存查询(按物料itemNo) A-092 P1

- 提交warehouseTypeCode=`A`、itemNo=`FN20260604001`
- 响应data[]仅含该物料的库存记录

#### pageNo=0查询 A-093 P2

- 提交pageNo=0、pageSize=20
- 响应：使用默认值page=1，或返回400
- 不崩溃

#### pageNo负数查询 A-094 P2

- 提交pageNo=-1、pageSize=20
- 响应：使用默认值page=1，或返回400

#### pageSize=0查询 A-095 P2

- 提交pageSize=0
- 响应：使用默认值size=20，或返回400

#### pageSize超限查询 A-096 P2

- 提交pageSize=101（文档max=100）
- 响应：截断到100并正常返回，或返回400
- 不崩溃，不返回超过100条数据

---

## 生产模块

### 生产订单同步 (POST /production/v3/save)

#### 生产订单最小必填 A-097 P0

- 提交productionOrderNo=`PO-TEST-001`、styleCode=`STYLE-001`、styleName=`测试款号`
- 响应成功（响应结构待文档补充，T-12）
- data含requestId或订单确认信息

#### 生产订单含色码和工序 A-098 P1

- 提交完整字段：含detailList（garmentColorCode+garmentColorName+garmentSizeCode+garmentSizeName+number）和procedureList（procedureNumber+procedureName+procedureCode+sam+price）
- 响应成功

#### 生产订单空detailList A-099 P1

- 提交detailList=[]
- 响应正常（允许无色码明细的订单同步）

#### 缺失productionOrderNo A-100 P2

- 不传productionOrderNo
- 响应HTTP 400或422
- 错误信息指明productionOrderNo为必填

#### 缺失styleCode A-101 P2

- 不传styleCode
- 响应HTTP 400或422
- 错误信息指明styleCode为必填

#### detailList中缺失必填子字段 A-102 P2

- detailList中某条记录不传garmentColorCode
- 响应HTTP 400或422
- 错误信息指明garmentColorCode为必填

#### 重复productionOrderNo A-103 P3

- 使用相同productionOrderNo提交两次
- 第二次应幂等（覆盖更新或提示已存在）
- 不产生重复数据

### 缝制任务单同步 (POST /sewing/v3/save)

#### 缝制任务最小必填 A-104 P0

- 提交sewingCode=`SG-TEST-001`、productionOrderNo=`PO-TEST-001`、styleCode=`STYLE-001`
- 响应成功

#### 缝制任务含色码明细 A-105 P1

- 提交detailList含garmentColorCode、garmentColorName、garmentSizeCode、garmentSizeName、number、orderNo
- 响应成功，orderNo顺序被保留

#### 关联不存在productionOrderNo A-106 P1

- 提交productionOrderNo=`PO-NONEXIST-999`
- 响应：拒绝（生产订单不存在）或受理成功但后续告警（待澄清 T-13）

#### 缺失sewingCode A-107 P2

- 不传sewingCode
- 响应HTTP 400或422

#### detailList中缺失orderNo A-108 P2

- detailList记录中不传orderNo
- 响应HTTP 400或422
- 错误信息指明orderNo为必填

#### 重复sewingCode A-109 P3

- 相同sewingCode重复提交
- 第二次应幂等

---

## 视图模块

### 工序产量视图

#### 工序产量视图字段校验 A-110 P1

- 验证视图字段结构：factory_no、line_no、station_no、operator_no、style_code、sewing_code、production_order_code、procedure_number、procedure_name、procedure_code、procedure_sam、procedure_price、color_code、color_name、size_code、out_qty、rack_no、begin_time、out_station_time、insert_date、be_production、barcode、create_time
- procedure_price类型从`varchar(8,4)`改为DECIMAL(8,4)（待澄清 T-14）

### 质检详情视图

#### 质检详情视图字段校验 A-111 P1

- 验证视图字段结构含qc_date、out_qty（质检件数）等特有字段
- 字段名与工序产量视图一致的部分保持一致

---

## 安全附录

| 类别 | 编号 | 测试点 |
|------|------|--------|
| 认证 | A-008 | 未登录访问需鉴权接口返回401 |
| 认证 | A-009 | 过期Token返回401 |
| 认证 | A-010 | 篡改Token返回401 |
| 认证 | A-112 | 认证失败响应不区分"用户不存在"和"密码错误" |
| 敏感信息 | A-007 | Token响应不含password_hash或明文密码 |
| 重放攻击 | A-055 | 相同requestId重复提交应幂等 |
| 重放攻击 | A-103 | 重复productionOrderNo应幂等 |

---

## 性能附录

| 类别 | 编号 | 测试点 | 指标 |
|------|------|--------|------|
| 响应时间 | A-001 | Token获取P95 | ≤ 500ms |
| 响应时间 | A-012 | 载具查询P95 | ≤ 1000ms |
| 响应时间 | A-046 | 物料同步P95 | ≤ 1000ms |
| 响应时间 | A-091 | 库存查询(100条)P95 | ≤ 2000ms |
| SPI回调 | A-032 | ERP回调响应时间 | ≤ 5s（文档约束） |
| SPI回调 | A-034 | 重试最大次数 | = 3次 |
| 分页 | A-096 | pageSize=100 | 正常返回不超时 |

---

## 用例评审表

| 编号 | 名称 | 优先级 | 类型 | 标签 |
|------|------|--------|------|------|
| A-001 | 正常获取Token | P0 | smoke_sanity | auth,token,create |
| A-002 | 错误密码获取Token | P1 | functional | auth,token,validation |
| A-003 | 不存在用户获取Token | P1 | functional | auth,token,validation |
| A-004 | 空凭证获取Token | P2 | boundary | auth,token,boundary |
| A-005 | 缺失username字段 | P2 | boundary | auth,token,required |
| A-006 | 缺失password字段 | P2 | boundary | auth,token,required |
| A-007 | Token格式验证 | P2 | boundary | auth,token,format |
| A-008 | 无Token访问业务API | P0 | security | auth,security,401 |
| A-009 | 过期Token访问业务API | P1 | security | auth,security,expired |
| A-010 | 篡改Token访问业务API | P2 | security | auth,security,tampered |
| A-011 | Metas-Request-Id可选性 | P2 | boundary | auth,header,optional |
| A-012 | 查询存在载具(depth=3) | P0 | smoke_sanity | carrier,query,full |
| A-013 | 查询空载具(depth=1) | P1 | functional | carrier,query,empty |
| A-014 | 查询已绑定载具(depth=3) | P1 | functional | carrier,query,bound |
| A-015 | 查询不存在的载具 | P2 | boundary | carrier,query,notfound |
| A-016 | 空carrierNo查询 | P2 | boundary | carrier,validation,empty |
| A-017 | depth=0查询 | P2 | boundary | carrier,boundary,depth |
| A-018 | depth超范围查询 | P2 | boundary | carrier,boundary,depth |
| A-019 | 上架任务下发 | P0 | smoke_sanity | carrier,task,put_on |
| A-020 | 下架任务下发 | P1 | functional | carrier,task,put_down |
| A-021 | 库外移动任务下发 | P1 | functional | carrier,task,move_outside |
| A-022 | 带bizTaskId任务下发 | P1 | functional | carrier,task,optional |
| A-023 | 非法taskType | P2 | boundary | carrier,task,validation |
| A-024 | 空carrierNo任务下发 | P2 | boundary | carrier,task,validation |
| A-025 | 空sourceLocationCode | P2 | boundary | carrier,task,required |
| A-026 | 空targetSpaceCode | P2 | boundary | carrier,task,required |
| A-027 | 同一载具重复下发任务 | P3 | integration | carrier,task,concurrent |
| A-028 | SPI回调上架完成 | P0 | smoke_sanity | spi,callback,carrier,finished |
| A-029 | SPI回调下架完成 | P1 | functional | spi,callback,carrier |
| A-030 | SPI回调库外移动完成 | P1 | functional | spi,callback,carrier |
| A-031 | SPI回调任务异常/取消 | P2 | boundary | spi,callback,carrier,error |
| A-032 | SPI回调ERP超时(>5s) | P2 | boundary | spi,callback,timeout |
| A-033 | SPI回调重试后成功 | P2 | boundary | spi,callback,retry |
| A-034 | SPI回调持续失败 | P3 | integration | spi,callback,exhaust |
| A-035 | 库区模糊查询 | P0 | smoke_sanity | warehouse,space,query |
| A-036 | 库区属性精准匹配 | P1 | functional | warehouse,space,filter |
| A-037 | 空参数查询所有库区 | P1 | functional | warehouse,space,all |
| A-038 | 不存在的库区编码 | P2 | boundary | warehouse,space,notfound |
| A-039 | 空spaceAttributes | P2 | boundary | warehouse,space,empty |
| A-040 | 禁用库区过滤 | P2 | boundary | warehouse,space,status |
| A-041 | 按面料仓类型查询 | P0 | smoke_sanity | warehouse,space,list |
| A-042 | 按裁片仓类型查询 | P1 | functional | warehouse,space,list |
| A-043 | 按辅料仓类型查询 | P2 | boundary | warehouse,space,list |
| A-044 | 非法仓库类型 | P2 | boundary | warehouse,space,validation |
| A-045 | 缺失warehouseTypeCode | P2 | boundary | warehouse,space,required |
| A-046 | 面料清单同步(不初始化库存) | P0 | smoke_sanity | material,sync,fabric |
| A-047 | 面料清单同步(初始化库存) | P1 | functional | material,sync,init |
| A-048 | 辅料清单同步 | P1 | functional | material,sync,trim |
| A-049 | 含完整扩展属性同步 | P1 | functional | material,sync,extended |
| A-050 | 缺失requestId | P2 | boundary | material,sync,required |
| A-051 | 缺失itemType | P2 | boundary | material,sync,required |
| A-052 | 空itemList | P2 | boundary | material,sync,empty |
| A-053 | itemNo重复 | P2 | boundary | material,sync,duplicate |
| A-054 | 非法itemType | P2 | boundary | material,sync,validation |
| A-055 | 相同requestId重复提交 | P3 | integration | material,sync,idempotent |
| A-056 | SPI回调同步成功 | P0 | smoke_sanity | spi,callback,sync,success |
| A-057 | SPI回调同步失败 | P1 | functional | spi,callback,sync,failure |
| A-058 | SPI回调部分成功 | P1 | functional | spi,callback,sync,partial |
| A-059 | SPI回调缺少requestId | P2 | boundary | spi,callback,sync,required |
| A-060 | SPI回调非法syncState | P2 | boundary | spi,callback,sync,validation |
| A-061 | SPI回调空列表 | P2 | boundary | spi,callback,sync,empty |
| A-062 | SPI回调超时+重试 | P3 | integration | spi,callback,sync,retry |
| A-063 | 增量绑定(BIND+INCR) | P0 | smoke_sanity | carrier,bind,incr |
| A-064 | 全量绑定(BIND+FULL) | P0 | smoke_sanity | carrier,bind,full |
| A-065 | 增量解绑(UNBIND+INCR) | P1 | functional | carrier,unbind,incr |
| A-066 | 全量解绑(UNBIND+FULL) | P1 | functional | carrier,unbind,full |
| A-067 | 绑定未入库物料 | P1 | functional | carrier,bind,precondition |
| A-068 | 绑定不存在的物料 | P1 | functional | carrier,bind,notfound |
| A-069 | 缺失carrierNo | P2 | boundary | carrier,bind,required |
| A-070 | 缺失bindType | P2 | boundary | carrier,bind,required |
| A-071 | 非法bindType | P2 | boundary | carrier,bind,validation |
| A-072 | 非法linkMode | P2 | boundary | carrier,bind,validation |
| A-073 | UNBIND+FULL+传itemList | P2 | boundary | carrier,bind,contradiction |
| A-074 | BIND+INCR+空itemList | P2 | boundary | carrier,bind,empty |
| A-075 | 已绑定物料重复绑定 | P3 | integration | carrier,bind,duplicate |
| A-076 | 物料入库(flowType=1) | P0 | smoke_sanity | stock,flow,inbound |
| A-077 | 物料出库(flowType=2) | P1 | functional | stock,flow,outbound |
| A-078 | 未入库物料出库 | P1 | functional | stock,flow,precondition |
| A-079 | 非法flowType | P2 | boundary | stock,flow,validation |
| A-080 | 缺失flowType | P2 | boundary | stock,flow,required |
| A-081 | 空itemList | P2 | boundary | stock,flow,empty |
| A-082 | 已出库物料重复出库 | P3 | integration | stock,flow,duplicate |
| A-083 | 独立入库(正常) | P0 | smoke_sanity | stock,inbound,normal |
| A-084 | 独立入库(空itemList) | P1 | functional | stock,inbound,empty |
| A-085 | 独立入库(缺失requestId) | P2 | boundary | stock,inbound,required |
| A-086 | 独立入库(itemNo不存在) | P2 | boundary | stock,inbound,notfound |
| A-087 | 独立出库(正常) | P0 | smoke_sanity | stock,outbound,normal |
| A-088 | 独立出库(未入库物料) | P1 | functional | stock,outbound,precondition |
| A-089 | 独立出库(缺失requestId) | P2 | boundary | stock,outbound,required |
| A-090 | 独立出库(出库数量=0) | P2 | boundary | stock,outbound,zero |
| A-091 | 库存查询(面料仓) | P0 | smoke_sanity | inventory,query,fabric |
| A-092 | 库存查询(按物料) | P1 | functional | inventory,query,filter |
| A-093 | pageNo=0查询 | P2 | boundary | inventory,pagination,zero |
| A-094 | pageNo负数查询 | P2 | boundary | inventory,pagination,negative |
| A-095 | pageSize=0查询 | P2 | boundary | inventory,pagination,zero |
| A-096 | pageSize超限查询 | P2 | boundary | inventory,pagination,overflow |
| A-097 | 生产订单最小必填 | P0 | smoke_sanity | production,order,create |
| A-098 | 生产订单含色码和工序 | P1 | functional | production,order,full |
| A-099 | 生产订单空detailList | P1 | functional | production,order,empty |
| A-100 | 缺失productionOrderNo | P2 | boundary | production,order,required |
| A-101 | 缺失styleCode | P2 | boundary | production,order,required |
| A-102 | detailList缺失必填子字段 | P2 | boundary | production,order,subfield |
| A-103 | 重复productionOrderNo | P3 | integration | production,order,idempotent |
| A-104 | 缝制任务最小必填 | P0 | smoke_sanity | sewing,task,create |
| A-105 | 缝制任务含色码明细 | P1 | functional | sewing,task,full |
| A-106 | 关联不存在productionOrderNo | P1 | functional | sewing,task,relation |
| A-107 | 缺失sewingCode | P2 | boundary | sewing,task,required |
| A-108 | detailList缺失orderNo | P2 | boundary | sewing,task,subfield |
| A-109 | 重复sewingCode | P3 | integration | sewing,task,idempotent |
| A-110 | 工序产量视图字段校验 | P1 | functional | view,production,output |
| A-111 | 质检详情视图字段校验 | P1 | functional | view,quality,detail |
| A-112 | 认证失败不泄露用户信息 | P2 | security | auth,security,disclosure |

---

## 通用覆盖矩阵自检

| 维度 | 本模块是否触发 | 已覆盖 / 待澄清 | 备注 |
|------|:---:|---|------|
| **A 数据输入与校验** | 是 | | 所有API端点的请求体校验 |
| 必填字段 | 是 | A-005,A-006,A-024,A-025,A-026,A-050,A-051,A-069,A-070,A-080,A-085,A-089,A-100,A-101,A-107 | 每个必填字段各1条缺失测试 |
| 数值/金额/数量 | 是 | A-090,V-090-1,V-090-2 | 出库数量=0、负数、超大值 |
| 长度/最大最小限制 | 是 | A-093~A-096 | pageNo/PageSize边界trio |
| 格式要求 | 是 | A-007,A-016 | Token格式、空字符串 |
| 文本字段 | 是 | A-004,A-016 | 空字符串、纯空白 |
| 唯一性约束 | 是 | A-053,A-055,A-075,A-103,A-109 | itemNo/requestId/productionOrderNo重复 |
| 枚举/下拉 | 是 | A-023,A-044,A-054,A-071,A-072,A-079 | 非法枚举值全覆盖 |
| **B 列表与查询** | 是 | | 库存查询、库区查询 |
| 列表展示 | 是 | A-035,A-041,A-091 | 正常查询返回列表 |
| 状态/类型过滤 | 是 | A-036,A-040,A-092 | 属性筛选、按物料筛选 |
| 分页 | 是 | A-093~A-096 | pageNo/pageSize全边界 |
| 排序 | 否 | 无排序字段 | 库存查询无排序参数 |
| 搜索/关键词 | 是 | A-035 | 库区模糊查询 |
| **C 鉴权与角色** | 是 | | Bearer Token |
| 需登录才能使用 | 是 | A-008~A-011 | 无Token/过期/篡改Token |
| 管理员专属操作 | 否 | 无角色分级 | 所有API用户角色一致 |
| 仅匿名可访问 | 是 | A-001~A-007 | 获取Token无需认证 |
| **D 资源标识** | 是 | | |
| 按 ID 读详情 | 是 | A-012~A-014,A-092 | carrierNo/itemNo查询 |
| 写后读一致性 | 是 | F-01,F-02 | 流程1/2端到端验证 |
| 软删/下架行为 | 是 | A-066 | UNBIND+FULL解绑后查询确认 |
| **E 时间与状态** | 是 | | |
| 开始/结束时间三态 | 否 | 无时间窗字段 | |
| 状态机合法迁移 | 是 | F-01,F-02,F-03 | 物料生命周期 + 载具绑定生命周期 |
| 状态机非法迁移 | 是 | A-067,A-078,A-088 | 未入库→出库/绑定 |
| 次数限制 N 次 | 是 | A-034 | SPI回调最多重试3次 |
| **F 重复与一致性** | 是 | | |
| 提交/支付幂等 | 是 | A-055,A-103,A-109 | requestId/productionOrderNo幂等 |
| 同数据多次更新 | 是 | A-098,A-105 | 生产订单/缝制任务覆盖更新 |
| 并发操作 | 是 | A-027 | 同载具重复任务下发 T-15 |
| **G 错误与可用性** | 是 | | |
| 校验失败提示 | 是 | A-004~A-006,A-023等 | 错误信息指明具体字段 |
| 依赖不可用 | 是 | A-032~A-034 | SPI回调ERP不可用 T-16 |
| **H 接口契约** | 是 | | 15个端点全覆盖 |
| **I 非功能附录** | 是 | 安全附录+性能附录 | 7条安全+7条性能 |

---

## 边界值速查表

| 需求原文 | 阈值类型 | 阈值 | 必测值 | 对应编号 |
|----------|----------|------|--------|----------|
| depth: 默认3, 1/2/3有效 | 范围 | min=1, max=3 | 0, 1, 2, 3, 4, 99 | A-017, A-018 |
| pageSize: 默认20, max=100 | 上限 | N=100 | 0, 1, 20, 100, 101 | A-093~A-096 |
| pageNo: 默认1 | 下限 | min=1 | 0, -1, 1 | A-093, A-094 |
| SPI回调超时: 5s | 上限 | 5s | 4.9s, 5.0s, 5.1s | A-032 |
| SPI重试: 最多3次 | 上限 | N=3 | 1次, 2次, 3次, 4次(不应发生) | A-033, A-034 |
| flowType: 1入库/2出库 | 枚举 | 1,2 | 0, 1, 2, 3 | A-079 |
| bindType: BIND/UNBIND | 枚举 | 2值 | 各1合法+1非法 | A-071 |
| linkMode: FULL/INCR | 枚举 | 2值 | 各1合法+1非法 | A-072 |
| itemAmount: Decimal(18,3) | 精度 | 3位小数 | 0, 0.001, 999999999999999.999 | V-090-1, V-090-2 |
| wareTypeCode: A/C/D/G | 枚举 | 4值 | A, C, D, G, X(非法) | A-041~A-044 |
| taskType: 3种 | 枚举 | 3值 | PUT_ON, PUT_DOWN, MOVE_OUTSIDE, INVALID | A-019~A-023 |
| itemType: 4种 | 枚举 | 4值 | fabric, trim, garment, cuttingPieces, invalid | A-046~A-054 |
| carrierStatus: 0~5,-1 | 范围 | 7值 | 各合法状态的操作行为差异 | A-012~A-018 |
| syncState: ACCEPTED/SUCCESS/FAILURE | 枚举 | 3值 | 3合法+1非法 | A-056~A-060 |

---

## 待澄清清单

| # | 问题 | 关联编号 | 优先级 |
|---|------|----------|--------|
| T-01 | Token有效期多久？过期后刷新机制是什么？ | A-009 | P0 |
| T-02 | 4.4/4.6 URL路径缺失斜杠是文档错误还是实际路径如此？ | AUD-001, AUD-002, A-046, A-076 | P0 |
| T-03 | stock/flow、inbound、outbound三端点是否并存？各自使用场景？ | AUD-W03, A-076~A-090 | P0 |
| T-04 | 生产订单和缝制任务同步的响应结构是什么？ | AUD-005, A-097~A-109 | P0 |
| T-05 | 库区模糊查询是否自动过滤warehouseSpaceStatus=1(禁用)的库区？ | A-040 | P1 |
| T-06 | 物料同步时itemList=[]（空数组）是否允许？行为是什么？ | A-052 | P1 |
| T-07 | SPI物料同步回调的failureList中是否包含每个失败物料的失败原因？ | A-057 | P1 |
| T-08 | syncState=SUCCESS但successList=[]是否矛盾？如何定义？ | A-061 | P1 |
| T-09 | UNBIND+FULL时若传了itemList，是忽略itemList还是拒绝请求？ | A-073 | P1 |
| T-10 | BIND+INCR时若itemList=[]，是拒绝还是正常返回无变化？ | A-074 | P1 |
| T-11 | 物料出入库时itemList=[]（空数组）是否允许？ | A-081 | P2 |
| T-12 | deptName字段类型冲突（Long vs String）应如何修正？ | AUD-004, A-106 | P1 |
| T-13 | 缝制任务关联不存在productionOrderNo时，是拒绝还是受理后告警？ | A-106 | P1 |
| T-14 | 工序产量视图中procedure_price类型为varchar(8,4)是设计如此还是应为DECIMAL？ | A-110, AUD-W05 | P2 |
| T-15 | 同一载具已有执行中任务时，再次下发任务的行为定义？ | A-027 | P2 |
| T-16 | SPI回调3次全部失败后，IMS如何标记该任务？是否有告警机制？ | A-034 | P2 |

---

## API 接口测试 — 可提取 YAML 块

<!-- 以下 YAML block 可被 generate_pytest.py 直接提取执行 -->

---
kind: api_pytest
base_url: http://test.fj.dtsimple.pro/api/ims-open-api
setup: test_init
auth:
  type: bearer_login
  login_path: /public/auth/authorization
  username_field: username
  password_field: password
  username_env: IMS_TEST_USERNAME
  password_env: IMS_TEST_PASSWORD
  token_json_path: data
timeout_default: 30

cases:
  # ===== 4.0 获取访问令牌 =====
  - id: A-001
    name: "正常获取Token"
    method: POST
    path: /public/auth/authorization
    no_auth: true
    json_body:
      username: "__ENV__:IMS_TEST_USERNAME"
      password: "__ENV__:IMS_TEST_PASSWORD"
    expect_status: 200
    expect_json_subset:
      code: 0
      message: "success"
    extract_vars:
      access_token: $.data

  - id: A-002
    name: "错误密码获取Token"
    method: POST
    path: /public/auth/authorization
    no_auth: true
    json_body:
      username: "__ENV__:IMS_TEST_USERNAME"
      password: "WrongPassword123"
    expect_status: 401
    expect_body_substrings: ["认证失败"]

  - id: A-003
    name: "不存在用户获取Token"
    method: POST
    path: /public/auth/authorization
    no_auth: true
    json_body:
      username: "nonexistent_user_20260703"
      password: "anypassword"
    expect_status: 401

  - id: A-004
    name: "空凭证获取Token"
    method: POST
    path: /public/auth/authorization
    no_auth: true
    json_body:
      username: ""
      password: ""
    expect_status: 400

  - id: A-005
    name: "缺失username字段"
    method: POST
    path: /public/auth/authorization
    no_auth: true
    json_body:
      password: "IMS@2026"
    expect_status: 400

  - id: A-006
    name: "缺失password字段"
    method: POST
    path: /public/auth/authorization
    no_auth: true
    json_body:
      username: "admin"
    expect_status: 400

  # ===== Token 鉴权验证 =====
  - id: A-008
    name: "无Token访问业务API"
    method: POST
    path: /wms/v3/carrier/info
    no_auth: true
    json_body:
      carrierNo: "PALLET-001"
    expect_status: 401

  - id: A-009
    name: "过期Token访问业务API"
    method: POST
    path: /wms/v3/carrier/info
    headers:
      Authorization: "Bearer expired-token-for-test"
    json_body:
      carrierNo: "PALLET-001"
    expect_status: 401

  - id: A-010
    name: "篡改Token访问业务API"
    method: POST
    path: /wms/v3/carrier/info
    headers:
      Authorization: "Bearer fake-invalid-token-12345"
    json_body:
      carrierNo: "PALLET-001"
    expect_status: 401

  # ===== 4.1 载具信息查询 =====
  - id: A-012
    name: "查询存在载具(depth=3)"
    method: POST
    path: /wms/v3/carrier/info
    json_body:
      carrierNo: "PALLET-001"
      depth: 3
    expect_status: 200
    expect_json_subset:
      code: 0
    extract_vars:
      resp_carrierNo: $.data.carrierNo
    depends_on: [A-001]

  - id: A-015
    name: "查询不存在的载具"
    method: POST
    path: /wms/v3/carrier/info
    json_body:
      carrierNo: "NONEXIST-CARRIER-999"
    expect_status: 200
    depends_on: [A-001]

  - id: A-016
    name: "空carrierNo查询"
    method: POST
    path: /wms/v3/carrier/info
    json_body:
      carrierNo: ""
    expect_status: 400
    depends_on: [A-001]

  - id: A-017
    name: "depth=0查询"
    method: POST
    path: /wms/v3/carrier/info
    json_body:
      carrierNo: "PALLET-001"
      depth: 0
    expect_status: 200
    depends_on: [A-001]

  - id: A-018
    name: "depth=99超范围查询"
    method: POST
    path: /wms/v3/carrier/info
    json_body:
      carrierNo: "PALLET-001"
      depth: 99
    expect_status: 200
    depends_on: [A-001]

  # ===== 4.2 库区查询 =====
  - id: A-035
    name: "库区模糊查询"
    method: POST
    path: /wms/v3/warehouse/space
    json_body:
      warehouseSpaceCode: "ZONE"
    expect_status: 200
    expect_json_subset:
      code: 0
    depends_on: [A-001]

  - id: A-036
    name: "库区属性精准匹配"
    method: POST
    path: /wms/v3/warehouse/space
    json_body:
      spaceAttributes:
        - attrKey: "RECEIVING"
          attrVal: "收货区"
    expect_status: 200
    depends_on: [A-001]

  - id: A-038
    name: "不存在的库区编码"
    method: POST
    path: /wms/v3/warehouse/space
    json_body:
      warehouseSpaceCode: "NONEXIST_SPACE_999"
    expect_status: 200
    depends_on: [A-001]

  # ===== 4.2 库区查询(/list) =====
  - id: A-041
    name: "按面料仓类型查询库区"
    method: POST
    path: /wms/v3/warehouse/space/list
    json_body:
      warehouseTypeCode: "A"
    expect_status: 200
    expect_json_subset:
      code: 0
    depends_on: [A-001]

  - id: A-044
    name: "非法仓库类型"
    method: POST
    path: /wms/v3/warehouse/space/list
    json_body:
      warehouseTypeCode: "X"
    expect_status: 400
    depends_on: [A-001]

  - id: A-045
    name: "缺失warehouseTypeCode"
    method: POST
    path: /wms/v3/warehouse/space/list
    json_body: {}
    expect_status: 400
    depends_on: [A-001]

  # ===== 4.3 载具任务执行下发 =====
  - id: A-019
    name: "上架任务下发"
    method: POST
    path: /wms/v3/carrier/task/execute
    json_body:
      taskType: "PUT_ON"
      carrierNo: "PALLET-001"
      sourceLocationCode: "WCS-A-01-01"
      targetSpaceCode: "ZONE-STORAGE"
    expect_status: 200
    expect_json_subset:
      code: 0
    extract_vars:
      task_id: $.data.taskId
    depends_on: [A-001]

  - id: A-020
    name: "下架任务下发"
    method: POST
    path: /wms/v3/carrier/task/execute
    json_body:
      taskType: "PUT_DOWN"
      carrierNo: "PALLET-001"
      sourceLocationCode: "WCS-A-01-01"
      targetSpaceCode: "ZONE-SHIPPING"
    expect_status: 200
    depends_on: [A-001]

  - id: A-021
    name: "库外移动任务下发"
    method: POST
    path: /wms/v3/carrier/task/execute
    json_body:
      taskType: "MOVE_OUTSIDE"
      carrierNo: "PALLET-001"
      sourceLocationCode: "WCS-A-01-01"
      targetSpaceCode: "ZONE-OUTSIDE"
    expect_status: 200
    depends_on: [A-001]

  - id: A-023
    name: "非法taskType"
    method: POST
    path: /wms/v3/carrier/task/execute
    json_body:
      taskType: "INVALID_TYPE"
      carrierNo: "PALLET-001"
      sourceLocationCode: "WCS-A-01-01"
      targetSpaceCode: "ZONE-STORAGE"
    expect_status: 400
    depends_on: [A-001]

  - id: A-024
    name: "空carrierNo任务下发"
    method: POST
    path: /wms/v3/carrier/task/execute
    json_body:
      taskType: "PUT_ON"
      carrierNo: ""
      sourceLocationCode: "WCS-A-01-01"
      targetSpaceCode: "ZONE-STORAGE"
    expect_status: 400
    depends_on: [A-001]

  - id: A-025
    name: "空sourceLocationCode"
    method: POST
    path: /wms/v3/carrier/task/execute
    json_body:
      taskType: "PUT_ON"
      carrierNo: "PALLET-001"
      sourceLocationCode: ""
      targetSpaceCode: "ZONE-STORAGE"
    expect_status: 400
    depends_on: [A-001]

  - id: A-026
    name: "空targetSpaceCode"
    method: POST
    path: /wms/v3/carrier/task/execute
    json_body:
      taskType: "PUT_ON"
      carrierNo: "PALLET-001"
      sourceLocationCode: "WCS-A-01-01"
      targetSpaceCode: ""
    expect_status: 400
    depends_on: [A-001]

  # ===== 4.4 物料物品清单同步 =====
  - id: A-046
    name: "面料清单同步(不初始化库存)"
    method: POST
    path: /wms/v3/material/item/sync
    json_body:
      requestId: "{{uuid}}"
      itemType: "fabric"
      initInventory: false
      itemList:
        - itemNo: "FN-TEST-{{uuid}}"
          materialExtendCode: "MAT-TEST-001"
          materialName: "测试面料"
          batchNo: "BATCH-TEST-001"
          itemUnit: "M"
          itemAmount: 1000.0
    expect_status: 200
    expect_json_subset:
      code: 0
    extract_vars:
      sync_requestId: $.data.requestId
    depends_on: [A-001]

  - id: A-047
    name: "面料清单同步(初始化库存)"
    method: POST
    path: /wms/v3/material/item/sync
    json_body:
      requestId: "{{uuid}}"
      itemType: "fabric"
      initInventory: true
      itemList:
        - itemNo: "FN-INIT-{{uuid}}"
          materialExtendCode: "MAT-INIT-001"
          materialName: "初始化库存面料"
          batchNo: "BATCH-INIT-001"
          itemUnit: "M"
          itemAmount: 5000.0
    expect_status: 200
    depends_on: [A-001]

  - id: A-050
    name: "缺失requestId"
    method: POST
    path: /wms/v3/material/item/sync
    json_body:
      itemType: "fabric"
      itemList:
        - itemNo: "FN-TEST-002"
          materialExtendCode: "MAT-002"
          materialName: "测试面料2"
          batchNo: "BATCH-002"
          itemUnit: "M"
    expect_status: 400
    depends_on: [A-001]

  - id: A-051
    name: "缺失itemType"
    method: POST
    path: /wms/v3/material/item/sync
    json_body:
      requestId: "{{uuid}}"
      itemList:
        - itemNo: "FN-TEST-003"
          materialExtendCode: "MAT-003"
          materialName: "测试面料3"
          batchNo: "BATCH-003"
          itemUnit: "M"
    expect_status: 400
    depends_on: [A-001]

  - id: A-052
    name: "空itemList同步"
    method: POST
    path: /wms/v3/material/item/sync
    json_body:
      requestId: "{{uuid}}"
      itemType: "fabric"
      itemList: []
    expect_status: 200
    depends_on: [A-001]

  - id: A-054
    name: "非法itemType"
    method: POST
    path: /wms/v3/material/item/sync
    json_body:
      requestId: "{{uuid}}"
      itemType: "invalid_type"
      itemList:
        - itemNo: "FN-TEST-004"
          materialExtendCode: "MAT-004"
          materialName: "测试"
          batchNo: "BATCH-004"
          itemUnit: "M"
    expect_status: 400
    depends_on: [A-001]

  # ===== 4.5 货载绑定/解绑 =====
  - id: A-063
    name: "增量绑定(BIND+INCR)"
    method: POST
    path: /wms/v3/carrier/item/link
    json_body:
      requestId: "{{uuid}}"
      carrierNo: "PALLET-001"
      bindType: "BIND"
      linkMode: "INCR"
      itemType: "fabric"
      itemList:
        - itemNo: "FN-TEST-BIND-{{uuid}}"
    expect_status: 200
    expect_json_subset:
      code: 0
    depends_on: [A-001]

  - id: A-064
    name: "全量绑定(BIND+FULL)"
    method: POST
    path: /wms/v3/carrier/item/link
    json_body:
      requestId: "{{uuid}}"
      carrierNo: "PALLET-001"
      bindType: "BIND"
      linkMode: "FULL"
      itemType: "fabric"
      itemList:
        - itemNo: "FN-TEST-FULL-{{uuid}}"
    expect_status: 200
    depends_on: [A-001]

  - id: A-065
    name: "增量解绑(UNBIND+INCR)"
    method: POST
    path: /wms/v3/carrier/item/link
    json_body:
      requestId: "{{uuid}}"
      carrierNo: "PALLET-001"
      bindType: "UNBIND"
      linkMode: "INCR"
      itemType: "fabric"
      itemList:
        - itemNo: "FN-TEST-UNBIND-{{uuid}}"
    expect_status: 200
    depends_on: [A-001]

  - id: A-066
    name: "全量解绑(UNBIND+FULL)"
    method: POST
    path: /wms/v3/carrier/item/link
    json_body:
      requestId: "{{uuid}}"
      carrierNo: "PALLET-001"
      bindType: "UNBIND"
      linkMode: "FULL"
      itemType: "fabric"
    expect_status: 200
    depends_on: [A-001]

  - id: A-069
    name: "缺失carrierNo"
    method: POST
    path: /wms/v3/carrier/item/link
    json_body:
      requestId: "{{uuid}}"
      bindType: "BIND"
      linkMode: "INCR"
      itemType: "fabric"
      itemList:
        - itemNo: "FN-TEST-001"
    expect_status: 400
    depends_on: [A-001]

  - id: A-070
    name: "缺失bindType"
    method: POST
    path: /wms/v3/carrier/item/link
    json_body:
      requestId: "{{uuid}}"
      carrierNo: "PALLET-001"
      linkMode: "INCR"
      itemType: "fabric"
      itemList:
        - itemNo: "FN-TEST-001"
    expect_status: 400
    depends_on: [A-001]

  - id: A-071
    name: "非法bindType"
    method: POST
    path: /wms/v3/carrier/item/link
    json_body:
      requestId: "{{uuid}}"
      carrierNo: "PALLET-001"
      bindType: "INVALID"
      linkMode: "INCR"
      itemType: "fabric"
      itemList:
        - itemNo: "FN-TEST-001"
    expect_status: 400
    depends_on: [A-001]

  - id: A-072
    name: "非法linkMode"
    method: POST
    path: /wms/v3/carrier/item/link
    json_body:
      requestId: "{{uuid}}"
      carrierNo: "PALLET-001"
      bindType: "BIND"
      linkMode: "INVALID"
      itemType: "fabric"
      itemList:
        - itemNo: "FN-TEST-001"
    expect_status: 400
    depends_on: [A-001]

  - id: A-073
    name: "UNBIND+FULL+传itemList(参数矛盾)"
    method: POST
    path: /wms/v3/carrier/item/link
    json_body:
      requestId: "{{uuid}}"
      carrierNo: "PALLET-001"
      bindType: "UNBIND"
      linkMode: "FULL"
      itemType: "fabric"
      itemList:
        - itemNo: "FN-TEST-001"
    expect_status: 400
    depends_on: [A-001]

  - id: A-074
    name: "BIND+INCR+空itemList"
    method: POST
    path: /wms/v3/carrier/item/link
    json_body:
      requestId: "{{uuid}}"
      carrierNo: "PALLET-001"
      bindType: "BIND"
      linkMode: "INCR"
      itemType: "fabric"
      itemList: []
    expect_status: 400
    depends_on: [A-001]

  # ===== 4.6 物料出入库 =====
  - id: A-076
    name: "物料入库(flowType=1)"
    method: POST
    path: /wms/v3/material/item/stock/flow
    json_body:
      requestId: "{{uuid}}"
      flowType: "1"
      itemList:
        - itemNo: "FN-INVENTORY-{{uuid}}"
          itemUnit: "M"
          itemAmount: 5000.0
    expect_status: 200
    expect_json_subset:
      code: 0
    depends_on: [A-001]

  - id: A-077
    name: "物料出库(flowType=2)"
    method: POST
    path: /wms/v3/material/item/stock/flow
    json_body:
      requestId: "{{uuid}}"
      flowType: "2"
      itemList:
        - itemNo: "FN-INVENTORY-001"
          itemUnit: "M"
          itemAmount: 1000.0
    expect_status: 200
    depends_on: [A-001]

  - id: A-079
    name: "非法flowType"
    method: POST
    path: /wms/v3/material/item/stock/flow
    json_body:
      requestId: "{{uuid}}"
      flowType: "3"
      itemList:
        - itemNo: "FN-TEST-001"
    expect_status: 400
    depends_on: [A-001]

  - id: A-080
    name: "缺失flowType"
    method: POST
    path: /wms/v3/material/item/stock/flow
    json_body:
      requestId: "{{uuid}}"
      itemList:
        - itemNo: "FN-TEST-001"
    expect_status: 400
    depends_on: [A-001]

  # ===== 4.6a 独立入库 =====
  - id: A-083
    name: "独立入库(正常)"
    method: POST
    path: /wms/v3/material/item/inbound
    json_body:
      requestId: "{{uuid}}"
      itemList:
        - itemNo: "FN-INBOUND-{{uuid}}"
          itemUnit: "M"
          itemAmount: 3000.0
    expect_status: 200
    depends_on: [A-001]

  - id: A-085
    name: "独立入库(缺失requestId)"
    method: POST
    path: /wms/v3/material/item/inbound
    json_body:
      itemList:
        - itemNo: "FN-TEST-001"
    expect_status: 400
    depends_on: [A-001]

  # ===== 4.6b 独立出库 =====
  - id: A-087
    name: "独立出库(正常)"
    method: POST
    path: /wms/v3/material/item/outbound
    json_body:
      requestId: "{{uuid}}"
      itemList:
        - itemNo: "FN-INVENTORY-001"
          itemUnit: "M"
          itemAmount: 500.0
    expect_status: 200
    depends_on: [A-001]

  - id: A-089
    name: "独立出库(缺失requestId)"
    method: POST
    path: /wms/v3/material/item/outbound
    json_body:
      itemList:
        - itemNo: "FN-TEST-001"
    expect_status: 400
    depends_on: [A-001]

  - id: A-090
    name: "独立出库(出库数量=0)"
    method: POST
    path: /wms/v3/material/item/outbound
    json_body:
      requestId: "{{uuid}}"
      itemList:
        - itemNo: "FN-INVENTORY-001"
          itemUnit: "M"
          itemAmount: 0
    expect_status: 400
    depends_on: [A-001]

  # ===== 4.7 物料库存查询 =====
  - id: A-091
    name: "库存查询(面料仓)"
    method: POST
    path: /wms/v3/material/item/inventory
    json_body:
      warehouseTypeCode: "A"
      pageNo: 1
      pageSize: 20
    expect_status: 200
    expect_json_subset:
      code: 0
    depends_on: [A-001]

  - id: A-092
    name: "库存查询(按物料itemNo)"
    method: POST
    path: /wms/v3/material/item/inventory
    json_body:
      warehouseTypeCode: "A"
      itemNo: "FN20260604001"
    expect_status: 200
    depends_on: [A-001]

  - id: A-093
    name: "pageNo=0查询"
    method: POST
    path: /wms/v3/material/item/inventory
    json_body:
      warehouseTypeCode: "A"
      pageNo: 0
      pageSize: 20
    expect_status: 200
    depends_on: [A-001]

  - id: A-094
    name: "pageNo负数查询"
    method: POST
    path: /wms/v3/material/item/inventory
    json_body:
      warehouseTypeCode: "A"
      pageNo: -1
      pageSize: 20
    expect_status: 200
    depends_on: [A-001]

  - id: A-095
    name: "pageSize=0查询"
    method: POST
    path: /wms/v3/material/item/inventory
    json_body:
      warehouseTypeCode: "A"
      pageNo: 1
      pageSize: 0
    expect_status: 200
    depends_on: [A-001]

  - id: A-096
    name: "pageSize超限查询(101)"
    method: POST
    path: /wms/v3/material/item/inventory
    json_body:
      warehouseTypeCode: "A"
      pageNo: 1
      pageSize: 101
    expect_status: 200
    depends_on: [A-001]

  # ===== 生产订单同步 =====
  - id: A-097
    name: "生产订单最小必填"
    method: POST
    path: /production/v3/save
    json_body:
      productionOrderNo: "PO-TEST-{{uuid}}"
      styleCode: "STYLE-001"
      styleName: "测试款号"
    expect_status: 200
    depends_on: [A-001]

  - id: A-100
    name: "缺失productionOrderNo"
    method: POST
    path: /production/v3/save
    json_body:
      styleCode: "STYLE-001"
      styleName: "测试款号"
    expect_status: 400
    depends_on: [A-001]

  - id: A-101
    name: "缺失styleCode"
    method: POST
    path: /production/v3/save
    json_body:
      productionOrderNo: "PO-TEST-002"
      styleName: "测试款号"
    expect_status: 400
    depends_on: [A-001]

  # ===== 缝制任务单同步 =====
  - id: A-104
    name: "缝制任务最小必填"
    method: POST
    path: /sewing/v3/save
    json_body:
      sewingCode: "SG-TEST-{{uuid}}"
      productionOrderNo: "PO-TEST-001"
      styleCode: "STYLE-001"
    expect_status: 200
    depends_on: [A-001]

  - id: A-107
    name: "缺失sewingCode"
    method: POST
    path: /sewing/v3/save
    json_body:
      productionOrderNo: "PO-TEST-001"
      styleCode: "STYLE-001"
    expect_status: 400
    depends_on: [A-001]

  - id: A-108
    name: "detailList缺失orderNo"
    method: POST
    path: /sewing/v3/save
    json_body:
      sewingCode: "SG-TEST-002"
      productionOrderNo: "PO-TEST-001"
      styleCode: "STYLE-001"
      detailList:
        - garmentColorCode: "RED001"
          garmentColorName: "红色"
          garmentSizeCode: "SIZE_M"
          garmentSizeName: "M"
          number: 100
    expect_status: 400
    depends_on: [A-001]

scenarios:
  - name: "完整物料生命周期(流程1)"
    steps:
      - method: POST
        path: /public/auth/authorization
        json_body:
          username: "__ENV__:IMS_TEST_USERNAME"
          password: "__ENV__:IMS_TEST_PASSWORD"
        expect_status: 200
        no_auth: true
        capture:
          token: $.data
      - method: POST
        path: /wms/v3/material/item/sync
        headers:
          Authorization: "Bearer {token}"
          Metas-Request-Id: "{{uuid}}"
        json_body:
          requestId: "{{uuid}}"
          itemType: "fabric"
          initInventory: false
          itemList:
            - itemNo: "FN-E2E-{{uuid}}"
              materialExtendCode: "MAT-E2E-001"
              materialName: "E2E测试面料"
              batchNo: "BATCH-E2E-001"
              itemUnit: "M"
              itemAmount: 5000.0
        expect_status: 200
      - method: POST
        path: /wms/v3/material/item/stock/flow
        headers:
          Authorization: "Bearer {token}"
          Metas-Request-Id: "{{uuid}}"
        json_body:
          requestId: "{{uuid}}"
          flowType: "1"
          itemList:
            - itemNo: "{sync_itemNo}"
              itemUnit: "M"
              itemAmount: 5000.0
        expect_status: 200
      - method: POST
        path: /wms/v3/carrier/item/link
        headers:
          Authorization: "Bearer {token}"
          Metas-Request-Id: "{{uuid}}"
        json_body:
          requestId: "{{uuid}}"
          carrierNo: "PALLET-001"
          bindType: "BIND"
          linkMode: "INCR"
          itemType: "fabric"
          itemList:
            - itemNo: "{sync_itemNo}"
        expect_status: 200
      - method: POST
        path: /wms/v3/carrier/task/execute
        headers:
          Authorization: "Bearer {token}"
          Metas-Request-Id: "{{uuid}}"
        json_body:
          taskType: "PUT_ON"
          carrierNo: "PALLET-001"
          sourceLocationCode: "WCS-A-01-01"
          targetSpaceCode: "ZONE-STORAGE"
        expect_status: 200
      - method: POST
        path: /wms/v3/material/item/stock/flow
        headers:
          Authorization: "Bearer {token}"
          Metas-Request-Id: "{{uuid}}"
        json_body:
          requestId: "{{uuid}}"
          flowType: "2"
          itemList:
            - itemNo: "{sync_itemNo}"
              itemUnit: "M"
              itemAmount: 1000.0
        expect_status: 200

  - name: "载具全量替换绑定(流程2)"
    steps:
      - method: POST
        path: /public/auth/authorization
        json_body:
          username: "__ENV__:IMS_TEST_USERNAME"
          password: "__ENV__:IMS_TEST_PASSWORD"
        expect_status: 200
        no_auth: true
        capture:
          token: $.data
      - method: POST
        path: /wms/v3/carrier/item/link
        headers:
          Authorization: "Bearer {token}"
        json_body:
          requestId: "{{uuid}}"
          carrierNo: "PALLET-001"
          bindType: "BIND"
          linkMode: "INCR"
          itemType: "fabric"
          itemList:
            - itemNo: "FN-FLOW2-A"
        expect_status: 200
      - method: POST
        path: /wms/v3/carrier/info
        headers:
          Authorization: "Bearer {token}"
        json_body:
          carrierNo: "PALLET-001"
          depth: 3
        expect_status: 200
        expect_body_substrings: ["FN-FLOW2-A"]
      - method: POST
        path: /wms/v3/carrier/item/link
        headers:
          Authorization: "Bearer {token}"
        json_body:
          requestId: "{{uuid}}"
          carrierNo: "PALLET-001"
          bindType: "BIND"
          linkMode: "FULL"
          itemType: "fabric"
          itemList:
            - itemNo: "FN-FLOW2-B"
            - itemNo: "FN-FLOW2-C"
        expect_status: 200
      - method: POST
        path: /wms/v3/carrier/info
        headers:
          Authorization: "Bearer {token}"
        json_body:
          carrierNo: "PALLET-001"
          depth: 3
        expect_status: 200
        expect_body_substrings: ["FN-FLOW2-B", "FN-FLOW2-C"]
---
