# 千虹接口文档 — 测试数据编目

> 版本：v1.0 | 日期：2026-07-03

---

## 1. 认证数据

| 类别 | 变化维度 | 测试数据 | 说明 |
|------|---------|----------|------|
| 正常登录 | 有效凭证 | username=admin, password=IMS@2026 | 文档示例值 |
| 错误密码 | 无效凭证 | username=admin, password=wrong | 认证失败 |
| 不存在用户 | 无效用户名 | username=nonexistent, password=any | 认证失败 |
| 空凭证 | 缺失必填 | username="", password="" | 参数校验 |
| 过期Token | 时序 | 使用超期token | 需环境支持 |
| 篡改Token | 安全 | Bearer fake-token-xxx | 安全校验 |

## 2. 载具数据

| 类别 | 变化维度 | 测试数据 | 说明 |
|------|---------|----------|------|
| 正常载具 | 面料托盘 | carrierNo=PALLET-001, carrierTypeCode=01 | 文档示例 |
| 空载具 | 无物料 | carrierBindStatus=0 | 绑定状态为空 |
| 已绑定载具 | 有物料 | carrierBindStatus=1, itemList非空 | 含物料列表 |
| 松布架 | 载具类型02 | carrierTypeCode=02 | |
| 裁片箱 | 载具类型03 | carrierTypeCode=03 | |
| 成品箱 | 载具类型04 | carrierTypeCode=04 | |
| 辅料箱 | 载具类型07 | carrierTypeCode=07 | |
| 料架 | 载具类型08 | carrierTypeCode=08 | |
| 不存在的载具 | 无效条码 | carrierNo=NONEXIST-999 | 查询/操作不存在 |
| 异常状态载具 | carrierStatus=-1 | 异常状态的载具操作 | |
| 已完成任务载具 | taskState=FINISH | 重复下发任务 | |
| 执行中载具 | taskState=WORKING | 并发任务下发 | |

## 3. 库区数据

| 类别 | 变化维度 | 测试数据 | 说明 |
|------|---------|----------|------|
| 正常库区 | 面料仓收货区 | warehouseSpaceCode=ZONE-RECEIVING, warehouseTypeCode=A | |
| 全部库区 | 面料仓 | warehouseTypeCode=A | /list接口 |
| 裁片仓 | warehouseTypeCode=C | |
| 成品仓 | warehouseTypeCode=D | |
| 辅料仓 | warehouseTypeCode=G | |
| 模糊匹配 | warehouseSpaceCode=ZONE | 模糊查询 |
| 属性筛选 | attrKey=RECEIVING, attrVal=收货区 | 精准匹配 |
| 禁用的库区 | warehouseSpaceStatus=1 | 禁用状态 |
| 不存在的库区 | warehouseSpaceCode=FAKE | 查询无结果 |

## 4. 物料数据

| 类别 | 变化维度 | 测试数据 | 说明 |
|------|---------|----------|------|
| 正常面料 | fabric类型 | itemNo=FN20260604001, materialExtendCode=MAT-001 | 文档示例 |
| 含扩展属性 | 面料完整字段 | vatCode, lotCode, fabricNo, breadthValue等 | 面料扩展属性 |
| 辅料 | trim类型 | itemType=trim | 扩展属性待后续补充 |
| 成品 | garment类型 | itemType=garment | |
| 裁片 | cuttingPieces类型 | itemType=cuttingPieces | |
| 已入库物料 | 可绑定可出库 | itemNo已完成入库的 | |
| 未入库物料 | 不可绑定不可出库 | itemNo未入库的 | |
| 不存在的物料 | 无效itemNo | itemNo=FAKE-ITEM | |
| 初始化库存 | initInventory=true | 同步后自动入库 | |
| 不初始化库存 | initInventory=false | 仅同步不入库 | |

## 5. 任务数据

| 类别 | 变化维度 | 测试数据 | 说明 |
|------|---------|----------|------|
| 上架任务 | PUT_ON | taskType=PUT_ON, targetSpaceCode=ZONE-STORAGE | |
| 下架任务 | PUT_DOWN | taskType=PUT_DOWN, targetSpaceCode=ZONE-SHIPPING | |
| 库外移动 | MOVE_OUTSIDE | taskType=MOVE_OUTSIDE, targetSpaceCode=ZONE-OUTSIDE | |
| 带关联任务 | bizTaskId | 有值 | 关联业务任务 |
| 无关联任务 | bizTaskId | null或不传 | |
| 非法任务类型 | taskType=INVALID | 校验失败 | |

## 6. 绑定数据

| 类别 | 变化维度 | 测试数据 | 说明 |
|------|---------|----------|------|
| 增量绑定 | BIND+INCR | bindType=BIND, linkMode=INCR | 追加物料 |
| 全量绑定 | BIND+FULL | bindType=BIND, linkMode=FULL | 替换全部物料 |
| 增量解绑 | UNBIND+INCR | bindType=UNBIND, linkMode=INCR | 解绑指定物料 |
| 全量解绑 | UNBIND+FULL | bindType=UNBIND, linkMode=FULL, 不传itemList | 清空载具 |
| 非法组合 | UNBIND+FULL+itemList非空 | 参数矛盾 | |
| 未入库物料绑定 | itemNo未入库+BIND | 违反R003 | |

## 7. 出入库数据

| 类别 | 变化维度 | 测试数据 | 说明 |
|------|---------|----------|------|
| 入库(通用) | flowType=1 | flowType="1" | stock/flow端点 |
| 出库(通用) | flowType=2 | flowType="2" | stock/flow端点 |
| 入库(独立) | inbound端点 | /material/item/inbound | 独立端点 |
| 出库(独立) | outbound端点 | /material/item/outbound | 独立端点 |
| 非法flowType | flowType=3 | 校验失败 | |
| 未入库物料出库 | flowType=2+未入库itemNo | 违反R001 | |
| 重复出库 | 已出库物料再出库 | 库存不足 | |

## 8. 库存查询数据

| 类别 | 变化维度 | 测试数据 | 说明 |
|------|---------|----------|------|
| 按仓库类型 | warehouseTypeCode=A | 面料仓库存 | |
| 按库区 | warehouseSpaceCode=ZONE-STORAGE | 指定库区 | |
| 按物料 | itemNo=FN20260604001 | 单个物料 | |
| 按载具 | carrierNo=PALLET-001 | 载具上物料 | |
| 分页-首页 | pageNo=1, pageSize=20 | 第一页 | |
| 分页-超限 | pageSize=200 | 超过max 100 | |
| 分页-非法 | pageNo=0或负数 | 边界值 | |

## 9. 生产订单数据

| 类别 | 变化维度 | 测试数据 | 说明 |
|------|---------|----------|------|
| 最小必填 | productionOrderNo+styleCode+styleName | 最小有效字段 | |
| 含色码明细 | detailList有数据 | 色码列表 | |
| 含工序列表 | procedureList有数据 | 工序列表 | |
| 空色码明细 | detailList=[] | 边界 | |
| 重复订单号 | productionOrderNo重复 | 幂等性 | |

## 10. 缝制任务单数据

| 类别 | 变化维度 | 测试数据 | 说明 |
|------|---------|----------|------|
| 最小必填 | sewingCode+productionOrderNo+styleCode | 最小有效字段 | |
| 含色码明细 | detailList有数据 | 含orderNo顺序 | |
| 关联已有生产订单 | productionOrderNo已存在 | 正常关联 | |
| 关联不存在生产订单 | productionOrderNo不存在 | 错误处理 | |
