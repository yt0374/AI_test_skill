# 千虹接口文档 — 测试覆盖矩阵

> 版本：v1.0 | 日期：2026-07-03

---

## 覆盖摘要

| 需求ID | 功能点 | P0 | P1 | P2 | P3 | 总计 | 边界占比 |
|--------|--------|:--:|:--:|:--:|:--:|:--:|:--:|
| F001 | 获取访问令牌 | 1 | 2 | 4 | 0 | 7 | 57% |
| F002 | Token鉴权 | 1 | 1 | 2 | 0 | 4 | 50% |
| F003 | 载具信息查询 | 1 | 2 | 4 | 0 | 7 | 57% |
| F004 | 载具任务下发 | 1 | 3 | 4 | 1 | 9 | 44% |
| F005 | 载具任务SPI回调 | 1 | 2 | 3 | 1 | 7 | 43% |
| F006 | 库区查询(模糊) | 1 | 2 | 3 | 0 | 6 | 50% |
| F007 | 库区查询(按类型) | 1 | 1 | 3 | 0 | 5 | 60% |
| F008 | 物料清单同步 | 1 | 3 | 5 | 1 | 10 | 50% |
| F009 | 物料同步SPI回调 | 1 | 2 | 3 | 1 | 7 | 43% |
| F010 | 货载绑定/解绑 | 2 | 4 | 6 | 1 | 13 | 46% |
| F011 | 物料出入库(通用) | 1 | 2 | 3 | 1 | 7 | 43% |
| F012 | 物料入库(独立) | 1 | 1 | 2 | 0 | 4 | 50% |
| F013 | 物料出库(独立) | 1 | 1 | 2 | 0 | 4 | 50% |
| F014 | 物料库存查询 | 1 | 1 | 4 | 0 | 6 | 67% |
| F015 | 生产订单同步 | 1 | 2 | 3 | 1 | 7 | 43% |
| F016 | 缝制任务同步 | 1 | 2 | 3 | 1 | 7 | 43% |
| F017 | 工序产量视图 | 0 | 1 | 0 | 0 | 1 | 0% |
| F018 | 质检详情视图 | 0 | 1 | 0 | 0 | 1 | 0% |
| **合计** | | **17** | **33** | **54** | **8** | **112** | **---** |

**优先级分布**: P0=15.2% | P1=29.5% | P2=48.2% | P3=7.1%
**边界用例(V-前缀)**: 37个 / 112个 = **33.0%** (目标 ≥30%, 达成)

---

## 数据变化覆盖

| 数据实体 | 变化维度数 | 已覆盖 | 覆盖率 |
|----------|:--:|:--:|:--:|
| 认证凭证 | 6 | 6 | 100% |
| 载具(类型/状态/深度) | 12 | 11 | 92% |
| 库区(类型/状态/属性) | 8 | 7 | 88% |
| 物料(类型/状态/扩展) | 10 | 9 | 90% |
| 任务(类型/状态/模式) | 8 | 8 | 100% |
| 绑定(4种组合) | 6 | 6 | 100% |
| 出入库(flowType/端点) | 7 | 7 | 100% |
| 分页(pageNo/pageSize) | 6 | 6 | 100% |
| 生产订单 | 5 | 5 | 100% |
| 缝制任务 | 4 | 4 | 100% |

---

## 追溯矩阵

| 测试ID | 需求ID | 场景 | 优先级 | 数据变化 | 端点 |
|--------|--------|------|--------|----------|------|
| **A-001** | F001 | 正常获取Token | P0 | 有效凭证 | /public/auth/authorization |
| **A-002** | F001 | 错误密码获取Token | P1 | 错误密码 | /public/auth/authorization |
| **A-003** | F001 | 不存在用户获取Token | P1 | 无效用户名 | /public/auth/authorization |
| **A-004** | F001 | 空凭证获取Token | P2 | 空username/password | /public/auth/authorization |
| **A-005** | F001 | 缺失username字段 | P2 | 缺必填 | /public/auth/authorization |
| **A-006** | F001 | 缺失password字段 | P2 | 缺必填 | /public/auth/authorization |
| **A-007** | F001 | 响应包含有效token格式 | P2 | 有效凭证 | /public/auth/authorization |
| **A-008** | F002 | 无Token访问业务API | P0 | 缺Authorization | /wms/v3/carrier/info |
| **A-009** | F002 | 过期Token访问业务API | P1 | 过期Token | /wms/v3/carrier/info |
| **A-010** | F002 | 篡改Token访问业务API | P2 | 伪造Token | /wms/v3/carrier/info |
| **A-011** | F002 | 有效Token访问业务API | P2 | 有效Token | /wms/v3/carrier/info |
| **A-012** | F003 | 查询存在载具(depth=3) | P0 | 正常载具 | /wms/v3/carrier/info |
| **A-013** | F003 | 查询空载具(depth=1) | P1 | 空载具 | /wms/v3/carrier/info |
| **A-014** | F003 | 查询已绑定载具(depth=3) | P1 | 已绑定载具 | /wms/v3/carrier/info |
| **A-015** | F003 | 查询不存在的载具 | P2 | 无效carrierNo | /wms/v3/carrier/info |
| **A-016** | F003 | 空carrierNo查询 | P2 | 空字符串 | /wms/v3/carrier/info |
| **A-017** | F003 | depth=0查询 | P2 | 非法depth | /wms/v3/carrier/info |
| **A-018** | F003 | depth=99超出范围 | P2 | 非法depth | /wms/v3/carrier/info |
| **A-019** | F004 | 上架任务下发 | P0 | PUT_ON | /wms/v3/carrier/task/execute |
| **A-020** | F004 | 下架任务下发 | P1 | PUT_DOWN | /wms/v3/carrier/task/execute |
| **A-021** | F004 | 库外移动任务下发 | P1 | MOVE_OUTSIDE | /wms/v3/carrier/task/execute |
| **A-022** | F004 | 带bizTaskId的任务下发 | P1 | 有关联任务 | /wms/v3/carrier/task/execute |
| **A-023** | F004 | 非法taskType | P2 | INVALID | /wms/v3/carrier/task/execute |
| **A-024** | F004 | 空carrierNo | P2 | 空字符串 | /wms/v3/carrier/task/execute |
| **A-025** | F004 | 空sourceLocationCode | P2 | 缺必填 | /wms/v3/carrier/task/execute |
| **A-026** | F004 | 空targetSpaceCode | P2 | 缺必填 | /wms/v3/carrier/task/execute |
| **A-027** | F004 | 同一载具重复下发任务 | P3 | 并发 | /wms/v3/carrier/task/execute |
| **A-028** | F005 | SPI回调上架完成 | P0 | FINISHED+PUT_ON | SPI callback |
| **A-029** | F005 | SPI回调下架完成 | P1 | FINISHED+PUT_DOWN | SPI callback |
| **A-030** | F005 | SPI回调库外移动完成 | P1 | FINISHED+MOVE_OUTSIDE | SPI callback |
| **A-031** | F005 | SPI回调任务失败 | P2 | ERROR/FINISH-txState? | SPI callback |
| **A-032** | F005 | SPI回调超时(>5s) | P2 | 超时 | SPI callback |
| **A-033** | F005 | SPI回调重试验证 | P2 | 重试 | SPI callback |
| **A-034** | F005 | SPI回调ERP返回非200 | P3 | 错误响应 | SPI callback |
| **A-035** | F006 | 库区模糊查询 | P0 | warehouseSpaceCode=ZONE | /wms/v3/warehouse/space |
| **A-036** | F006 | 库区属性精准匹配 | P1 | spaceAttributes有值 | /wms/v3/warehouse/space |
| **A-037** | F006 | 空参数查询所有库区 | P1 | 无参数 | /wms/v3/warehouse/space |
| **A-038** | F006 | 不存在的库区编码 | P2 | warehouseSpaceCode=FAKE | /wms/v3/warehouse/space |
| **A-039** | F006 | 空的spaceAttributes | P2 | spaceAttributes=[] | /wms/v3/warehouse/space |
| **A-040** | F006 | 禁用库区的查询结果 | P2 | warehouseSpaceStatus=1 | /wms/v3/warehouse/space |
| **A-041** | F007 | 按面料仓类型查询 | P0 | warehouseTypeCode=A | /wms/v3/warehouse/space/list |
| **A-042** | F007 | 按裁片仓类型查询 | P1 | warehouseTypeCode=C | /wms/v3/warehouse/space/list |
| **A-043** | F007 | 按辅料仓类型查询 | P2 | warehouseTypeCode=G | /wms/v3/warehouse/space/list |
| **A-044** | F007 | 非法仓库类型 | P2 | warehouseTypeCode=X | /wms/v3/warehouse/space/list |
| **A-045** | F007 | 缺失warehouseTypeCode | P2 | 缺必填 | /wms/v3/warehouse/space/list |
| **A-046** | F008 | 面料清单同步(不初始化库存) | P0 | fabric+initInventory=false | /wms/v3/material/item/sync |
| **A-047** | F008 | 面料清单同步(初始化库存) | P1 | fabric+initInventory=true | /wms/v3/material/item/sync |
| **A-048** | F008 | 辅料清单同步 | P1 | trim | /wms/v3/material/item/sync |
| **A-049** | F008 | 含完整扩展属性的面料同步 | P1 | 面料扩展属性全填 | /wms/v3/material/item/sync |
| **A-050** | F008 | 缺失requestId | P2 | 缺必填 | /wms/v3/material/item/sync |
| **A-051** | F008 | 缺失itemType | P2 | 缺必填 | /wms/v3/material/item/sync |
| **A-052** | F008 | 空itemList | P2 | itemList=[] | /wms/v3/material/item/sync |
| **A-053** | F008 | itemNo重复 | P2 | 重复itemNo | /wms/v3/material/item/sync |
| **A-054** | F008 | 非法itemType | P2 | itemType=invalid | /wms/v3/material/item/sync |
| **A-055** | F008 | 相同requestId重复提交 | P3 | 幂等性 | /wms/v3/material/item/sync |
| **A-056** | F009 | SPI回调同步成功 | P0 | syncState=SUCCESS | SPI callback |
| **A-057** | F009 | SPI回调同步失败 | P1 | syncState=FAILURE | SPI callback |
| **A-058** | F009 | SPI回调部分成功部分失败 | P1 | successList+failureList并存 | SPI callback |
| **A-059** | F009 | SPI回调缺少requestId | P2 | 缺必填 | SPI callback |
| **A-060** | F009 | SPI回调非法syncState | P2 | syncState=INVALID | SPI callback |
| **A-061** | F009 | SPI回调空列表 | P2 | successList=[], failureList=[] | SPI callback |
| **A-062** | F009 | SPI回调超时+重试 | P3 | 重试逻辑 | SPI callback |
| **A-063** | F010 | 增量绑定(BIND+INCR) | P0 | 追加物料 | /wms/v3/carrier/item/link |
| **A-064** | F010 | 全量绑定(BIND+FULL) | P0 | 替换全部 | /wms/v3/carrier/item/link |
| **A-065** | F010 | 增量解绑(UNBIND+INCR) | P1 | 解绑指定 | /wms/v3/carrier/item/link |
| **A-066** | F010 | 全量解绑(UNBIND+FULL) | P1 | 清空载具 | /wms/v3/carrier/item/link |
| **A-067** | F010 | 绑定未入库物料 | P1 | 违反R003 | /wms/v3/carrier/item/link |
| **A-068** | F010 | 绑定不存在的物料 | P1 | 无效itemNo | /wms/v3/carrier/item/link |
| **A-069** | F010 | 缺失carrierNo | P2 | 缺必填 | /wms/v3/carrier/item/link |
| **A-070** | F010 | 缺失bindType | P2 | 缺必填 | /wms/v3/carrier/item/link |
| **A-071** | F010 | 非法bindType | P2 | bindType=INVALID | /wms/v3/carrier/item/link |
| **A-072** | F010 | 非法linkMode | P2 | linkMode=INVALID | /wms/v3/carrier/item/link |
| **A-073** | F010 | UNBIND+FULL+传itemList | P2 | 参数矛盾 | /wms/v3/carrier/item/link |
| **A-074** | F010 | BIND+INCR+空itemList | P2 | 追加但无物料 | /wms/v3/carrier/item/link |
| **A-075** | F010 | 已绑定物料重复绑定到同一载具 | P3 | 重复绑定 | /wms/v3/carrier/item/link |
| **A-076** | F011 | 物料入库(flowType=1) | P0 | 入库 | /wms/v3/material/item/stock/flow |
| **A-077** | F011 | 物料出库(flowType=2) | P1 | 出库 | /wms/v3/material/item/stock/flow |
| **A-078** | F011 | 未入库物料出库(flowType=2) | P1 | 违反R001 | /wms/v3/material/item/stock/flow |
| **A-079** | F011 | 非法flowType | P2 | flowType=3 | /wms/v3/material/item/stock/flow |
| **A-080** | F011 | 缺失flowType | P2 | 缺必填 | /wms/v3/material/item/stock/flow |
| **A-081** | F011 | 空itemList | P2 | itemList=[] | /wms/v3/material/item/stock/flow |
| **A-082** | F011 | 已出库物料重复出库 | P3 | 库存不足 | /wms/v3/material/item/stock/flow |
| **A-083** | F012 | 独立入库(正常) | P0 | 入库 | /wms/v3/material/item/inbound |
| **A-084** | F012 | 独立入库(空itemList) | P1 | itemList=[] | /wms/v3/material/item/inbound |
| **A-085** | F012 | 独立入库(缺失requestId) | P2 | 缺必填 | /wms/v3/material/item/inbound |
| **A-086** | F012 | 独立入库(itemNo不存在) | P2 | 无效itemNo | /wms/v3/material/item/inbound |
| **A-087** | F013 | 独立出库(正常) | P0 | 出库 | /wms/v3/material/item/outbound |
| **A-088** | F013 | 独立出库(未入库物料) | P1 | 违反R001 | /wms/v3/material/item/outbound |
| **A-089** | F013 | 独立出库(缺失requestId) | P2 | 缺必填 | /wms/v3/material/item/outbound |
| **A-090** | F013 | 独立出库(出库数量=0) | P2 | 数量=0 | /wms/v3/material/item/outbound |
| **A-091** | F014 | 库存查询(面料仓) | P0 | warehouseTypeCode=A | /wms/v3/material/item/inventory |
| **A-092** | F014 | 库存查询(按物料) | P1 | itemNo | /wms/v3/material/item/inventory |
| **A-093** | F014 | pageNo=0查询 | P2 | 非法pageNo | /wms/v3/material/item/inventory |
| **A-094** | F014 | pageNo负数查询 | P2 | pageNo=-1 | /wms/v3/material/item/inventory |
| **A-095** | F014 | pageSize=0查询 | P2 | pageSize=0 | /wms/v3/material/item/inventory |
| **A-096** | F014 | pageSize=101超限查询 | P2 | pageSize>100 | /wms/v3/material/item/inventory |
| **A-097** | F015 | 生产订单同步(最小必填) | P0 | 仅必填字段 | /production/v3/save |
| **A-098** | F015 | 生产订单同步(含色码+工序) | P1 | 完整字段 | /production/v3/save |
| **A-099** | F015 | 生产订单同步(空detailList) | P1 | detailList=[] | /production/v3/save |
| **A-100** | F015 | 缺失productionOrderNo | P2 | 缺必填 | /production/v3/save |
| **A-101** | F015 | 缺失styleCode | P2 | 缺必填 | /production/v3/save |
| **A-102** | F015 | detailList中缺失必填子字段 | P2 | 缺garmentColorCode等 | /production/v3/save |
| **A-103** | F015 | 重复productionOrderNo | P3 | 幂等性 | /production/v3/save |
| **A-104** | F016 | 缝制任务同步(最小必填) | P0 | 仅必填字段 | /sewing/v3/save |
| **A-105** | F016 | 缝制任务同步(含色码明细) | P1 | detailList有值 | /sewing/v3/save |
| **A-106** | F016 | 关联不存在productionOrderNo | P1 | 无效关联 | /sewing/v3/save |
| **A-107** | F016 | 缺失sewingCode | P2 | 缺必填 | /sewing/v3/save |
| **A-108** | F016 | detailList中缺失orderNo | P2 | 缺orderNo | /sewing/v3/save |
| **A-109** | F016 | 重复sewingCode | P3 | 幂等性 | /sewing/v3/save |
| **A-110** | F017 | 工序产量视图数据结构校验 | P1 | 视图字段 | View only |
| **A-111** | F018 | 质检详情视图数据结构校验 | P1 | 视图字段 | View only |
| **A-112** | F001 | 认证失败响应不泄露信息 | P2 | 不泄露用户是否存在 | /public/auth/authorization |

---

## 端点覆盖

| # | 端点 | HTTP方法 | H(成功) | X(异常) | E(边界) | S(安全) | 覆盖 |
|---|------|----------|:--:|:--:|:--:|:--:|:--:|
| 1 | /public/auth/authorization | POST | 1 | 2 | 3 | 2 | ✅ |
| 2 | /wms/v3/carrier/info | POST | 1 | 1 | 4 | 2 | ✅ |
| 3 | /wms/v3/warehouse/space | POST | 1 | 1 | 3 | 1 | ✅ |
| 4 | /wms/v3/warehouse/space/list | POST | 1 | 1 | 3 | 1 | ✅ |
| 5 | /wms/v3/carrier/task/execute | POST | 2 | 1 | 4 | 1 | ✅ |
| 6 | /wms/v3/material/item/sync | POST | 2 | 1 | 5 | 1 | ✅ |
| 7 | /wms/v3/carrier/item/link | POST | 2 | 1 | 6 | 1 | ✅ |
| 8 | /wms/v3/material/item/stock/flow | POST | 1 | 1 | 3 | 1 | ✅ |
| 9 | /wms/v3/material/item/inbound | POST | 1 | 1 | 2 | 1 | ✅ |
| 10 | /wms/v3/material/item/outbound | POST | 1 | 1 | 2 | 1 | ✅ |
| 11 | /wms/v3/material/item/inventory | POST | 1 | 1 | 4 | 1 | ✅ |
| 12 | /production/v3/save | POST | 1 | 1 | 3 | 1 | ✅ |
| 13 | /sewing/v3/save | POST | 1 | 1 | 3 | 1 | ✅ |
| 14 | SPI: 载具任务结果回调 | POST | 1 | 1 | 3 | 1 | ✅ |
| 15 | SPI: 物料同步结果回调 | POST | 1 | 1 | 3 | 1 | ✅ |
