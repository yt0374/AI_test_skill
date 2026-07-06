# IMS Error Messages & Prompts Catalog

> Auto-extracted from 7 knowledge base documents on 2026-06-30.
> Source docs:
> 1. 通用WMS业务操作流程.docx
> 2. WMS开箱模块.docx
> 3. WMS产品需求规划.docx
> 4. 面料备料全流程功能.docx
> 5. 裁片配套绑定全流程.docx
> 6. 通用-IMS系统操作手册V1.0.2【吊挂】.docx
> 7. 使用手册-吊挂.docx

---

## Module: 通用WMS (Warehouse Management System - General)

### Page: PC - 面料物料清单
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "已收货的物料信息不可删除" | error (business rule) | 尝试删除已收货的物料时 | 通用WMS业务操作流程 |
| "未收货的物料信息可以删除" | info (business rule) | 仅未收货状态的物料支持删除 | 通用WMS业务操作流程 |

### Page: PDA - 物料收货
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "已收货的物料不可重复收货" | error | 扫描已收货状态的物料再次收货时 | 通用WMS业务操作流程 |

### Page: PDA - 货载绑定
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "货载绑定中绑定的物料，必须是已收货的物料信息" | error (validation rule) | 绑定未收货的物料时 | 通用WMS业务操作流程 |

### Page: PDA - 货载上架
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "货载上架扫描的载具必须是初始状态/已下架状态，否则无法进行上架操作" | error | 扫描非初始状态且非已下架状态的载具上架时 | 通用WMS业务操作流程 |
| "此时任务已无法取消" | warning | 上架任务进入"上架中"状态后尝试取消 | 通用WMS业务操作流程 |
| "上架成功后，PC-面料库存中对应所属库区会变更为对应上架的立库库区" | success (implicit) | 上架任务完成 | 通用WMS业务操作流程 |

### Page: PDA - 货载下架
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "货载下架查询的物料信息必须是在立库库内的信息，临时区/未收货的物料是无法查询出来的" | error | 查询不在立库库内的物料时 | 通用WMS业务操作流程 |
| "此时任务已无法取消" | warning | 下架任务进入"下架中"状态后尝试取消 | 通用WMS业务操作流程 |

### Page: PDA - 出库确认
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "出库成功后，对应物料的库存信息相关进行扣减" | success (implicit) | 出库操作完成 | 通用WMS业务操作流程 |
| "目前仅辅料支持部分出库；面料目前仅支持全部出库" | error (validation rule) | 对面料/裁片尝试部分出库时 | 通用WMS业务操作流程 |

### Page: PDA - 空载上架
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "已绑定载具的载具无法在空载上架界面进行上架操作" | error | 扫描已绑定物料的载具进行空载上架时 | 通用WMS业务操作流程 |

### Page: PDA - 上下架记录
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "等待执行的任务可取消" | info | 查看等待执行的上架/下架任务时 | 通用WMS业务操作流程 |

---

## Module: WMS开箱模块 (WMS Carton Opening Module)

### Page: PC - 箱型管理
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "成品纸箱数量超过上限数" | error (上架拦截) | 同托盘同箱型数量大于1.65货位上限数量，执行上架时 | WMS开箱模块 |

### Page: PC - 开箱机配置
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "顺序号不允许重复" | error | 新增开箱机配置保存时，顺序号与已有记录冲突 | WMS开箱模块 |
| 删除操作弹窗二次确认 | confirm | 点击删除开箱机配置时 | WMS开箱模块 |

### Page: PDA - 一般叫箱
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| PDA提示用户输入叫箱需求数量，默认带入建议叫箱数 | prompt | 勾选箱型卡片后 | WMS开箱模块 |
| "已超额叫箱。" | error (拦截提示) | 填写的需求数量超过剩余可叫数量，且用户无【超额叫箱】权限时 | WMS开箱模块 |
| 超额叫箱原因选择提示 | prompt | 填写的需求数量超过剩余可叫数量，且用户有【超额叫箱】权限时（需选择原因） | WMS开箱模块 |
| 提交叫箱需求单二次确认弹窗 | confirm | 点击提交叫箱需求单时 | WMS开箱模块 |
| "提交叫箱需求单成功" | success | 二次确认后提交成功 | WMS开箱模块 |

### Page: PDA - 例外叫箱
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 提交叫箱需求单二次确认弹窗 | confirm | 点击提交叫箱需求单时 | WMS开箱模块 |
| "提交叫箱需求单成功" | success | 二次确认后提交成功 | WMS开箱模块 |

### Page: PC - 叫箱需求单详情
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 手动点击完成弹窗二次确认 | confirm | 手动将单据转为已完成状态时 | WMS开箱模块 |

### Page: PDA - 开箱执行
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "本次开箱数必须是整数" | error (validation) | 输入非整数开箱数时 | WMS开箱模块 |
| "不可以超过叫箱数-已开箱数" | error (validation) | 输入的开箱数超过(叫箱数-已开箱数)时 | WMS开箱模块 |
| 下发开箱任务二次确认弹窗 | confirm | 点击下发开箱任务时 | WMS开箱模块 |
| 页面提示成功 | success | 开箱任务下发成功 | WMS开箱模块 |

### Page: PDA - 开箱派送
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 下发送箱任务二次确认弹窗 | confirm | 点击下发送箱任务时 | WMS开箱模块 |
| 页面提示成功 | success | 送箱任务下发成功 | WMS开箱模块 |

### Page: PC - 开箱任务记录
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 取消任务弹窗二次确认 | confirm | 点击取消开箱任务时 | WMS开箱模块 |
| 初始化状态：此时可以取消任务 | info | 任务状态为"初始化"时 | WMS开箱模块 |
| 执行中状态：开箱机已开始执行，此时可以取消任务 | info | 任务状态为"执行中"时 | WMS开箱模块 |
| 异常状态：开箱机上报异常，此时可以取消任务或者重试 | warning/info | 任务状态为"异常"时 | WMS开箱模块 |

---

## Module: 面料备料全流程 (Fabric Preparation Full Flow)

### Page: PDA - 面料备料绑定
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "该载具存在其他领料单的物料" | error | 扫描载具时，载具内含属于其他备料领料单的未解绑物料 | 面料备料全流程功能 |
| "该载具存在未解绑、未备料的物料" | error | 扫描载具时，载具内含不属于备料状态的未解绑物料 | 面料备料全流程功能 |
| "无效的物料条码，请确保面料在库存内。" | error (异常提示) | 扫描的物料条码不在库存内 | 面料备料全流程功能 |
| "备货绑定成功" | success | 确认绑定操作完成，载具和物料标记为已备料 | 面料备料全流程功能 |
| 成功提示反馈3s，自动返回选择领料单页面 | success (UI behavior) | 绑定成功后 | 面料备料全流程功能 |

### Page: PDA - 面料备料解绑
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "无效载具条码" | error | 扫描无效的载具条码时 | 面料备料全流程功能 |
| "请扫描已备料的载具" | error/prompt | 扫描处于未备料状态的载具时 | 面料备料全流程功能 |
| 确认单个解绑弹窗 | confirm | 扫描布卷解绑或点击解绑单个时 | 面料备料全流程功能 |
| 确认全部解绑弹窗 | confirm | 点击全部解绑时 | 面料备料全流程功能 |
| 成功提示反馈3s，当前载具页面刷新 | success | 解绑完成后 | 面料备料全流程功能 |

### Page: PDA - 已备料状态影响（载具收货/货载绑定/货载解绑/物料合载）
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "该载具已备料，无法使用当前功能，请先备货解绑。" | error | 在载具收货/货载绑定/货载解绑/物料合载功能中扫描已备料状态的载具时 | 面料备料全流程功能 |

### Page: PDA - 已备料状态影响（按单出库/领料单出库）
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 已备料物料无法被其他领料单用于出库，只能被锁定的备料领料单用于出库 | error (business rule) | 用非锁定领料单对已备料物料执行出库时 | 面料备料全流程功能 |

---

## Module: 裁片配套绑定全流程 (Cut-Piece Matching Binding)

### Page: PDA - 裁片按扎配套绑定 / 裁片按床配套绑定
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 提示扫描载具条码 | prompt | 进入绑定页面时 | 裁片配套绑定全流程 |
| "配套绑定成功。" | success | 点击确认配套绑定后 | 裁片配套绑定全流程 |
| 具体的部件不支持移除，扎号、床次允许移除 | info (validation rule) | 尝试移除部件时 | 裁片配套绑定全流程 |

### Page: PDA - 裁片配套解绑
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 确认配套解绑弹窗 | confirm | 点击确认配套解绑时 | 裁片配套绑定全流程 |
| 解绑完成刷新页面 | success (UI behavior) | 解绑操作完成后 | 裁片配套绑定全流程 |
| 配套状态从"已配套"转化为"待配套" | success (implicit) | 解绑后裁片状态变更 | 裁片配套绑定全流程 |

---

## Module: 吊挂 - 生产订单 (Hanging System - Production Orders)

### Page: PC - 生产订单编辑
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 生产订单为"草稿"状态可进行编辑操作 | info (business rule) | 生产订单处于草稿状态时 | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| 生产订单为"已发布状态"，需先"返发布"-"反生效"才可编辑 | info (business rule) | 尝试编辑已发布的生产订单时 | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| 开启页面右上方"自动保存"后，点击切换Tab页，系统将自动保存改动信息 | info (UI behavior) | 自动保存配置开启时 | 通用-IMS系统操作手册V1.0.2【吊挂】 |

### Page: PC - 缝制任务
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 保存：将缝制任务保存在本地（缝制组长不可见） | info | 点击保存时 | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| 发布：将缝制任务发布至线上（缝制组长可见） | info | 点击发布时 | 通用-IMS系统操作手册V1.0.2【吊挂】 |

### Page: PAD - 缝制管理 - 工序编排
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "加工方案必须有普通站或者全能工站" | error (上线前系统校验) | 上线时加工方案中没有普通站或全能工站 | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| "过站工序不回流"选项说明：勾选后已完成的衣架不会回流 | info (配置说明) | 工序回流配置 | 通用-IMS系统操作手册V1.0.2【吊挂】 |

### Page: PAD - 挂片
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 挂片数量超出设定数量时，弹出小框，可输入继续超挂的数量 | prompt (超挂输入框) | 挂片数量超过设定数量时 | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| 切换色码时，提示弹窗，点击确定 | confirm (色码切换确认) | 点击目标色码切换时 | 通用-IMS系统操作手册V1.0.2【吊挂】 |

### Page: PAD - 质检 - 返工
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 选择工序号和返工原因，点击确定，衣架打回对应站位 | confirm (返工确认) | 执行质检返工操作时 | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| "每选择一道工序都要选择原因后再选择另一道需要返工的工序" | info (操作规则) | 多道工序返工操作时 | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| "质检返工后，返工率是记录在被返工的站位而非质检站" | info (业务规则) | 返工操作后 | 通用-IMS系统操作手册V1.0.2【吊挂】 |

### Page: PAD - 站位管理
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "每个站位都有衣架容量限制，是该站位最大允许存在衣架数量" | info (限制说明) | 站位管理页面 | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| 清除站内衣架：输入数量，确认后系统内衣架数量减去该数值 | confirm (操作确认) | 清除站内衣架操作 | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| 清除在途衣架：输入数量，确认后系统内在途衣架数量相应扣减 | confirm (操作确认) | 清除在途衣架操作 | 通用-IMS系统操作手册V1.0.2【吊挂】 |

### Page: PAD - 衣架更换
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 输入原衣架号和新衣架号，点击确认，新衣架被赋予原衣架路径 | confirm (衣架更换确认) | 执行衣架更换操作时 | 通用-IMS系统操作手册V1.0.2【吊挂】 |

### Page: PC - 用户管理
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 新增用户确认 | confirm | 录入用户信息后点击"确认" | 通用-IMS系统操作手册V1.0.2【吊挂】 |

---

## Module: 吊挂使用流程 (Hanging System Usage Flow)

### Page: PAD - 缝制管理 - 产前准备
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 缝制任务提交确认 | confirm | 点击"提交"，任务从"产前准备"变更为"待缝制" | 通用-IMS系统操作手册V1.0.2【吊挂】 |

### Page: PAD - 挂片 - 换款
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 切换款式确认 | confirm | 点击"换款"后选择款式点击"确定" | 使用手册-吊挂 / 通用-IMS操作手册 |

---

## Module: 吊挂 - 系统配置 & 通用规则

### Page: 通用
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "模拟程序仅测试环境有，生产上禁止绑定站位" | warning | 生产环境使用模拟程序功能时 | 使用手册-吊挂 |
| "生产车间有对应的权限" | info (权限提示) | 创建生产订单时 | 使用手册-吊挂 |

---

## Module: WMS产品需求规划 (WMS Product Planning)

### Page: 载具绑库位
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "载具绑库位需要保证库位无任务" | error (validation rule) | 库位有任务时执行载具绑库位操作 | WMS产品需求规划 |

### Page: 站位释放
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "站位释放需要保证库位无任务" | error (validation rule) | 库位有任务时执行站位释放操作 | WMS产品需求规划 |

---

## Summary of Message Patterns by Type

### Error Messages (错误提示)
| # | Message Text | Source |
|---|-------------|--------|
| 1 | "顺序号不允许重复" | WMS开箱模块 |
| 2 | "成品纸箱数量超过上限数" | WMS开箱模块 |
| 3 | "已超额叫箱。" | WMS开箱模块 |
| 4 | "不可以超过叫箱数-已开箱数" | WMS开箱模块 |
| 5 | "已收货的物料不可重复收货" | 通用WMS业务操作流程 |
| 6 | "已收货的物料信息不可删除" | 通用WMS业务操作流程 |
| 7 | "货载上架扫描的载具必须是初始状态/已下架状态，否则无法进行上架操作" | 通用WMS业务操作流程 |
| 8 | "货载下架查询的物料信息必须是在立库库内的信息，临时区/未收货的物料是无法查询出来的" | 通用WMS业务操作流程 |
| 9 | "已绑定载具的载具无法在空载上架界面进行上架操作" | 通用WMS业务操作流程 |
| 10 | "目前仅辅料支持部分出库；面料目前仅支持全部出库" | 通用WMS业务操作流程 |
| 11 | "货载绑定中绑定的物料，必须是已收货的物料信息" | 通用WMS业务操作流程 |
| 12 | "该载具存在其他领料单的物料" | 面料备料全流程功能 |
| 13 | "该载具存在未解绑、未备料的物料" | 面料备料全流程功能 |
| 14 | "无效的物料条码，请确保面料在库存内。" | 面料备料全流程功能 |
| 15 | "无效载具条码" | 面料备料全流程功能 |
| 16 | "请扫描已备料的载具" | 面料备料全流程功能 |
| 17 | "该载具已备料，无法使用当前功能，请先备货解绑。" | 面料备料全流程功能 |
| 18 | 已备料物料无法被其他领料单用于出库 | 面料备料全流程功能 |
| 19 | "加工方案必须有普通站或者全能工站" | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| 20 | "载具绑库位需要保证库位无任务" | WMS产品需求规划 |
| 21 | "站位释放需要保证库位无任务" | WMS产品需求规划 |
| 22 | "具体的部件不支持移除" | 裁片配套绑定全流程 |

### Warning Messages (警告提示)
| # | Message Text | Source |
|---|-------------|--------|
| 1 | "此时任务已无法取消" (上架中/下架中) | 通用WMS业务操作流程 |
| 2 | "模拟程序仅测试环境有，生产上禁止绑定站位" | 使用手册-吊挂 |
| 3 | 开箱任务异常状态：开箱机上报异常 | WMS开箱模块 |

### Success Messages (成功提示)
| # | Message Text | Source |
|---|-------------|--------|
| 1 | "提交叫箱需求单成功" | WMS开箱模块 |
| 2 | 下发开箱任务页面提示成功 | WMS开箱模块 |
| 3 | 下发送箱任务页面提示成功 | WMS开箱模块 |
| 4 | "备货绑定成功" | 面料备料全流程功能 |
| 5 | 备料绑定/解绑成功提示反馈3s | 面料备料全流程功能 |
| 6 | "配套绑定成功。" | 裁片配套绑定全流程 |

### Confirmation Dialogs (二次确认/弹窗)
| # | Dialog / Trigger | Source |
|---|-----------------|--------|
| 1 | 删除开箱机配置二次确认 | WMS开箱模块 |
| 2 | 提交叫箱需求单二次确认 | WMS开箱模块 |
| 3 | 手动点击完成单据二次确认 | WMS开箱模块 |
| 4 | 下发开箱任务二次确认 | WMS开箱模块 |
| 5 | 下发送箱任务二次确认 | WMS开箱模块 |
| 6 | 取消开箱任务二次确认 | WMS开箱模块 |
| 7 | 确认单个解绑弹窗 | 面料备料全流程功能 |
| 8 | 确认全部解绑弹窗 | 面料备料全流程功能 |
| 9 | 确认配套解绑弹窗 | 裁片配套绑定全流程 |
| 10 | 挂片超挂数量输入弹窗 | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| 11 | 色码切换确认弹窗 | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| 12 | 返工确认弹窗 | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| 13 | 衣架更换确认弹窗 | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| 14 | 清除站内/在途衣架确认弹窗 | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| 15 | 新增用户确认 | 通用-IMS系统操作手册V1.0.2【吊挂】 |
| 16 | 缝制任务提交确认 | 通用-IMS系统操作手册V1.0.2【吊挂】 |

### Prompts (输入提示/引导文字)
| # | Prompt Text | Source |
|---|------------|--------|
| 1 | PDA提示用户输入叫箱需求数量，默认带入建议叫箱数 | WMS开箱模块 |
| 2 | 超额叫箱原因选择提示 | WMS开箱模块 |
| 3 | 提示扫描载具条码 | 裁片配套绑定全流程 |
| 4 | 挂片超挂数量输入提示 | 通用-IMS系统操作手册V1.0.2【吊挂】 |

---

## Document Coverage Notes

- **WMS产品需求规划.docx**: Primarily a feature/module planning spreadsheet. Contains mostly module names, terminal types, and factory assignments rather than UI messages. Only validation rules around "库位无任务" were extractable.
- **通用-IMS系统操作手册V1.0.2【吊挂】.docx**: Operational manual; most UI interactions are described narratively (e.g., "点击确认", "点击保存") rather than quoting exact system messages. Extracted messages are inferred from operational constraints and explicit PS notes.
- **使用手册-吊挂.docx**: Short usage guide with similar narrative style. Contains only high-level flow descriptions.

---

> Expansion on 2026-07-02 from 4 additional knowledge base documents:
> - feature_production_offline.md
> - feature_procurement_picking.md
> - feature_style_reports.md
> - implicit_business_rules.md (no messages extracted -- navigation/menu structure only)

---

## Module: 生产订单 & 线外 (Production Orders & Offline)

### Page: PC - 生产订单 - 手动新增
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "请输入款号" | error (validation) | 款号字段为空时提交 | feature_production_offline |
| "请输入客户款号" | error (validation) | 客户款号字段为空时提交 | feature_production_offline |
| "请选择客户" | error (validation) | 客户字段为空时提交 | feature_production_offline |
| "请选择品牌" | error (validation) | 品牌字段为空时提交 | feature_production_offline |
| "请选择下单日期" | error (validation) | 下单日期字段为空时提交 | feature_production_offline |
| "请选择入客仓期" | error (validation) | 入客仓期字段为空时提交 | feature_production_offline |
| "请选择生产部门" | error (validation) | 生产部门字段为空时提交 | feature_production_offline |

### Page: PC - 生产订单 - 编辑
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "请输入款号" | error (validation) | 款号字段为空时编辑保存 | feature_production_offline |
| "请选择客户" | error (validation) | 客户字段为空时编辑保存 | feature_production_offline |
| "请选择品牌" | error (validation) | 品牌字段为空时编辑保存 | feature_production_offline |
| "请选择生产车间" | error (validation) | 生产车间字段为空时编辑保存 | feature_production_offline |
| "保存失败，客户款号、下单日期和入仓期不能为空！" | error (validation) | 客户款号、下单日期或入仓期任一为空时编辑保存 | feature_production_offline |

### Page: PC - 生产订单 - 颜色尺码Tab - 生效
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "颜色尺码标签页下每个色码至少有一个大于0的对应件数" | error (validation) | 所有色码的件数均为0或空时点击生效 | feature_production_offline |
| 生效成功 | success (implicit) | 每个色码至少有一个大于0的件数 | feature_production_offline |

### Page: PC - 生产订单 - 生产工序导入
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 导入失败 | error (validation) | 客户款号为空 | feature_production_offline |
| 导入失败 | error (validation) | 工序编号/工序代码/工序名称/工段任一为空 | feature_production_offline |
| 导入失败 | error (validation) | 一级部位为空且二级部位有值 | feature_production_offline |
| 导入失败 | error (validation) | 工序编号重复 | feature_production_offline |
| 导入失败 | error (validation) | 工段/部位/设备/辅助工具/级别不在数据字典中 | feature_production_offline |
| "数值类型错误(最多4位小数)" | error (validation) | SAM值超过4位小数 | feature_production_offline |
| "数值类型错误(最多4位小数)" | error (validation) | SAM值为负数 | feature_production_offline |
| "数值类型错误(最多4位小数)" | error (validation) | SAM值为非数字字符 | feature_production_offline |

### Page: PC - 生产订单 - 唛架管理
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "唛架号不能重复, {唛架号}" | error (validation) | 新增唛架时唛架号与已有记录重复 | feature_production_offline |
| "段长需大于0" | error (validation) | 段长值 <= 0 时 | feature_production_offline |
| "裁片类型不能为空" | error (validation) | cuttingTypeValid=1 且裁片类型为空时 | feature_production_offline |

### Page: PC - 线外任务
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "任务单号重复，请修改" | error (validation) | 线外任务单号与已有记录重复 | feature_production_offline |
| "分配完毕" | info (status indicator) | 色/码卡片待分配数=0 | feature_production_offline |
| "超出分配" | warning (status indicator) | 已分配数 > 订单数量 | feature_production_offline |

### Page: PAD - 线外任务 - 确认分配
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 保存失败 | error (validation) | 产量工序未选择 | feature_production_offline |
| 确认分配失败 | error (validation) | 所有工序未选择制程 | feature_production_offline |
| 确认分配失败 | error (validation) | 操作员和工作站均为空 (取决于config production:spt_user_station_check) | feature_production_offline |

### Page: PDA - 线外代报工 (Proxy Reporting)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 开始扫描按钮置灰 | info (UI state) | 工序和员工均未选择时 | feature_production_offline |
| "系数不能为空" | error (validation) | 系数字段为空时 | feature_production_offline |
| "请分配系数" | error/prompt (validation) | 系数未分配时 | feature_production_offline |
| "系数需大于零且小数位数最大两位" | error (validation) | 系数=0或小数超过2位 | feature_production_offline |
| "裁片扎卡不存在" | error (validation) | 扫描的扎卡在系统中不存在 | feature_production_offline |
| "未查询到对应扎卡" | error (validation) | 扫描不到对应的裁片扎卡记录 | feature_production_offline |
| "请扫描本单下扎卡" | error (validation) | 扫描的扎卡不属于当前单据 | feature_production_offline |
| "同扎号扎卡请勿重复报工" | error (validation) | 同一扎号的扎卡被重复扫描报工 | feature_production_offline |
| "只允许主布报工" | error (validation) | 工序标记"只许主布报工"但扫描的裁片为辅布类型 | feature_production_offline |
| "扎卡未验片完成或未免检" | error (validation) | cutting_piece_finish_check=1 且扎卡未完成验片 | feature_production_offline |
| "工序编排已调整，请检查后重试" | error (validation) | 扫描过程中工序编排被其他人调整 | feature_production_offline |
| "{工号}未被分配所选工序" | error (validation) | 员工未被分配到所选的报工工序 | feature_production_offline |

### Page: PC - 工作站配置 (Workstation Configuration)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "工作站编号重复" | error (validation) | 新增/编辑工作站时编号与已有记录重复 | feature_production_offline |
| "请输入0-10000000之间的数字,最多2位小数" | error (validation) | 理论节拍值不在0-10000000范围内或超过2位小数 | feature_production_offline |
| "当前用户无该工作站权限" | error (permission) | 用户角色未绑定该工作站时登录PDA | feature_production_offline |

---

## Module: 采购领料 & 裁片外协 (Procurement Picking & Cut-Parts Outsource)

### Page: PC - 面料领料单 (Fabric Picking Order)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "必填字段缺失[领料仓库]" | error (validation) | 生效时领料仓库为空 | feature_procurement_picking |
| "必填字段缺失[领料日期]" | error (validation) | 生效时领料日期为空 | feature_procurement_picking |
| 生效失败 | error (validation) | 是否需松布=是 且 松布组别为空 | feature_procurement_picking |
| "请选择一条数据" | error (validation) | 新增领料单时未勾选任何生产订单 | feature_procurement_picking |

### Page: PC - 面料领料单 - 新增领料明细
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 已新增过的物料复选框禁用 | info (UI state) | 同materialId+materialColorId+customerStyleCode+productionOrderStyleId组合已存在 | feature_procurement_picking |

### Page: PC - 辅料领料单 (Accessory Picking Order)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "必填字段缺失[领料仓库]" | error (validation) | 生效时领料仓库为空 | feature_procurement_picking |
| "必填字段缺失[领料日期]" | error (validation) | 生效时领料日期为空 | feature_procurement_picking |
| 保存失败 + 输入框标红 | error (validation) | 生产组别为空时保存 | feature_procurement_picking |
| "最少选择一条数据" | error (validation) | 选择裁剪床次弹窗中未勾选任何床次点确认 | feature_procurement_picking |
| 已新增过的物料复选框禁用 | info (UI state) | 同materialId+colorId+sizeId+customerStyleCode+productionOrderStyleId组合已存在 | feature_procurement_picking |

### Page: PDA - 领料出库 (Picking Outbound)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 出库失败 | error (强校验) | 面料: 物料编号+色号+供应商物料编码与领料单不一致 | feature_procurement_picking |
| 出库失败 | error (强校验) | 辅料: 物料编号+色号+尺码+供应商物料编码与领料单不一致 | feature_procurement_picking |
| 二次确认提示 | confirm (弱校验) | 面料: 销售单号/采购单号/缸号/lot色/客户款号与领料单不一致 | feature_procurement_picking |
| 二次确认提示 | confirm (弱校验) | 辅料: 销售单号与领料单不一致 | feature_procurement_picking |

### Page: PDA - 裁片外协 - 新增任务
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "裁片外协单号重复" | error (validation) | 手动输入的外协单号与已有记录重复 | feature_procurement_picking |
| "请选择接收组织" | error (validation) | 接收组织下拉框为空时提交 | feature_procurement_picking |
| 新增成功后记住上次填写值 | info (UI behavior) | 再次进入新增页面时回显上次填写值 | feature_procurement_picking |

### Page: PDA - 裁片外协 - 扫描 (All 4 Stages)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "未找到该条码的载具" | error (validation) | 扫描的条码在系统中不存在任何载具记录 | feature_procurement_picking |
| "裁片箱[箱号]中未查询到裁片" | error (validation) | 扫描的载具存在但其中无裁片信息 | feature_procurement_picking |
| "裁片已存在其他外协任务" | error (validation) | 扫描的裁片已被另一个未完成的外协任务使用 | feature_procurement_picking |
| "以下裁片未验片完成或未免检，无法外协发出{扎号+部位类型}" | error (validation) | bundle_strap_complete_model=1 且裁片未完成验片 | feature_procurement_picking |
| "单个单据只允许相同生产订单裁片发出" | error (validation) | diff_productionorder_add_order_model=1 且扫描了不同生产订单的裁片 | feature_procurement_picking |
| "存在委外验片未完成的扎卡" | error (validation) | outsource_strap_complete_switch=1 且存在委外验片未完成 | feature_procurement_picking |
| "裁片[扎号]状态为[花厂发出]，不能进行当前操作" | error (status gate) | 在按箱花厂发出阶段扫描了状态为花厂发出的裁片 | feature_procurement_picking |
| 二次确认: "共计X包X件，是否确认完成本次任务？" | confirm | 有箱码裁片，点击确认发出/接收/完成 | feature_procurement_picking |
| 按钮置灰不可点击 | info (UI state) | 无任何箱码裁片时[完成/确认发出]按钮 | feature_procurement_picking |

---

## Module: 款号管理 & 报表 (Style Management & Reports)

### Page: PC - 款号管理 - 新增款号
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| 新增失败 | error (validation) | 款号为空 | feature_style_reports |
| 新增失败 | error (validation) | 款号已存在 | feature_style_reports |
| 新增失败 | error (validation) | 客户为空 | feature_style_reports |
| 新增失败 + 提示 | error (validation) | config=1: 款号+客户款号+销售订单号组合重复 | feature_style_reports |
| 新增失败 + 提示 | error (validation) | config=2: 款号+客户款号组合重复 | feature_style_reports |

### Page: PC - 款号管理 - 复制
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "请选择一条数据" | error (validation) | 复制弹窗中未选择任何款号 | feature_style_reports |
| "请选择一条数据" | error (validation) | 跨页选择（仅当前页选中生效） | feature_style_reports |

### Page: PC - 款号管理 - 物料需求导入 (Material Import)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "物料编号不能为空" | error (validation) | 导入数据中物料编号为空 + 标红 | feature_style_reports |
| "未匹配到系统内已有物料档案，请先新增此物料后重试" | error (validation) | 导入的物料编号在系统中不存在 | feature_style_reports |
| "运算符不存在" | error (validation) | 运算符不是 + 或 x | feature_style_reports |
| "数值类型错误" | error (validation) | 单件用量/备品为非数字（中文/英文/特殊字符） | feature_style_reports |

### Page: PC - 款号管理 - 部位尺寸导入
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "未匹配到款号下已有尺码，请先新增此尺码后重试" | error (validation) | 导入的尺码不在款号已有尺码列表中 | feature_style_reports |
| "部位及量法不能为空" | error (validation) | 部位及量法字段为空 | feature_style_reports |

### Page: PC - 款号管理 - 用线指示导入
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "色号不存在" | error (validation) | 导入的色号在款号颜色尺码中不存在 | feature_style_reports |

### Page: PC - 款号管理 - 生产工序导入
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "工序编号不可重复" | error (validation) | 导入数据中工序编号有重复 | feature_style_reports |
| "工段不存在" | error (validation) | 导入的工段值不在数据字典中 | feature_style_reports |
| "级别不存在" (实际提示"工段不存在") | error (validation) | 导入的级别值不在数据字典中 | feature_style_reports |

### Page: PC - 款号管理 - 生产工序保存
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "数值类型错误(最多4位小数)" | error (validation) | SAM/单价超过4位小数 | feature_style_reports |
| 保存失败 + 提示 | error (validation) | 工序编号/名称/工段任一为空 | feature_style_reports |

### Page: PC - 款号管理 - 部位尺寸保存
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "部位及量法不能为空" | error (validation) | 部位及量法字段为空时保存 | feature_style_reports |

### Page: PC - 款号管理 - 物料管理
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "物料编号已存在" | error (validation) | 新增物料时物料编号与已有记录重复 | feature_style_reports |
| "物料不存在，请先新增/选择物料" | error (validation) | 编辑物料时物料记录不存在 | feature_style_reports |
| 保存失败 + 标红提示 | error (validation) | 必填字段为空 | feature_style_reports |

### Page: PC - 生产订单删除 (下游校验)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "存在下游单据时无法删除{code}, 请检查后重试" | error (validation) | 生产订单存在下游单据时尝试删除 | feature_style_reports |
| "下游单据{code}已在生产中，无法删除" | error (validation) | 下游单据已进入生产状态时尝试删除 | feature_style_reports |
| "生产订单已经生成" | error (validation) | 反生效时生产订单已生成 | feature_style_reports |
| "订单生产计划已经生成" | error (validation) | 反生效时生产计划已生成 | feature_style_reports |

### Page: PC - 任务删除 (Task Deletion)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "修改状态异常" | error (validation) | 松布任务在"松布中"状态时尝试中止 | feature_style_reports |
| "生产中的线外任务不能取消分配" | error (validation) | 线外任务在"生产中"状态时尝试删除 | feature_style_reports |
| "已生产的单据不允许删除" | error (validation) | 尾整任务在"尾整中"状态时尝试删除 | feature_style_reports |
| "{code}下单箱件数必填" | error (validation) | 批量生成装箱单时单箱件数缺失 | feature_style_reports |

### Page: PAD - 裁剪/尾整任务
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc |
|-------------|------|------------------|------------|
| "裁剪床次任务不存在" | error (runtime) | PAD端扫描已被删除的裁剪任务 | feature_style_reports |
| "报工件数已超出尾整任务单分配件数" | error (validation) | PAD端尾整任务被删除后仍尝试报工 | feature_style_reports |

---

## Summary of Message Patterns by Type (Expansion 2026-07-02)

### Error Messages (错误提示) - New
| # | Message Text | Source |
|---|-------------|--------|
| 23 | "请输入款号" | feature_production_offline |
| 24 | "请输入客户款号" | feature_production_offline |
| 25 | "请选择客户" | feature_production_offline |
| 26 | "请选择品牌" | feature_production_offline |
| 27 | "请选择下单日期" | feature_production_offline |
| 28 | "请选择入客仓期" | feature_production_offline |
| 29 | "请选择生产部门" | feature_production_offline |
| 30 | "请选择生产车间" | feature_production_offline |
| 31 | "保存失败，客户款号、下单日期和入仓期不能为空！" | feature_production_offline |
| 32 | "颜色尺码标签页下每个色码至少有一个大于0的对应件数" | feature_production_offline |
| 33 | "数值类型错误(最多4位小数)" | feature_production_offline / feature_style_reports |
| 34 | "唛架号不能重复, {唛架号}" | feature_production_offline |
| 35 | "段长需大于0" | feature_production_offline |
| 36 | "裁片类型不能为空" | feature_production_offline |
| 37 | "任务单号重复，请修改" | feature_production_offline |
| 38 | "系数不能为空" | feature_production_offline |
| 39 | "请分配系数" | feature_production_offline |
| 40 | "系数需大于零且小数位数最大两位" | feature_production_offline |
| 41 | "裁片扎卡不存在" | feature_production_offline |
| 42 | "未查询到对应扎卡" | feature_production_offline |
| 43 | "请扫描本单下扎卡" | feature_production_offline |
| 44 | "同扎号扎卡请勿重复报工" | feature_production_offline |
| 45 | "只允许主布报工" | feature_production_offline |
| 46 | "扎卡未验片完成或未免检" | feature_production_offline |
| 47 | "工序编排已调整，请检查后重试" | feature_production_offline |
| 48 | "{工号}未被分配所选工序" | feature_production_offline |
| 49 | "工作站编号重复" | feature_production_offline |
| 50 | "请输入0-10000000之间的数字,最多2位小数" | feature_production_offline |
| 51 | "当前用户无该工作站权限" | feature_production_offline |
| 52 | "必填字段缺失[领料仓库]" | feature_procurement_picking |
| 53 | "必填字段缺失[领料日期]" | feature_procurement_picking |
| 54 | "请选择一条数据" | feature_procurement_picking / feature_style_reports |
| 55 | "最少选择一条数据" | feature_procurement_picking |
| 56 | "裁片外协单号重复" | feature_procurement_picking |
| 57 | "请选择接收组织" | feature_procurement_picking |
| 58 | "未找到该条码的载具" | feature_procurement_picking |
| 59 | "裁片箱[箱号]中未查询到裁片" | feature_procurement_picking |
| 60 | "裁片已存在其他外协任务" | feature_procurement_picking |
| 61 | "以下裁片未验片完成或未免检，无法外协发出{扎号+部位类型}" | feature_procurement_picking |
| 62 | "单个单据只允许相同生产订单裁片发出" | feature_procurement_picking |
| 63 | "存在委外验片未完成的扎卡" | feature_procurement_picking |
| 64 | "裁片[扎号]状态为[花厂发出]，不能进行当前操作" | feature_procurement_picking |
| 65 | "物料编号不能为空" | feature_style_reports |
| 66 | "未匹配到系统内已有物料档案，请先新增此物料后重试" | feature_style_reports |
| 67 | "运算符不存在" | feature_style_reports |
| 68 | "数值类型错误" | feature_style_reports |
| 69 | "未匹配到款号下已有尺码，请先新增此尺码后重试" | feature_style_reports |
| 70 | "部位及量法不能为空" | feature_style_reports |
| 71 | "色号不存在" | feature_style_reports |
| 72 | "工序编号不可重复" | feature_style_reports |
| 73 | "工段不存在" | feature_style_reports |
| 74 | "物料编号已存在" | feature_style_reports |
| 75 | "物料不存在，请先新增/选择物料" | feature_style_reports |
| 76 | "存在下游单据时无法删除{code}, 请检查后重试" | feature_style_reports |
| 77 | "下游单据{code}已在生产中，无法删除" | feature_style_reports |
| 78 | "生产订单已经生成" | feature_style_reports |
| 79 | "订单生产计划已经生成" | feature_style_reports |
| 80 | "修改状态异常" | feature_style_reports |
| 81 | "生产中的线外任务不能取消分配" | feature_style_reports |
| 82 | "已生产的单据不允许删除" | feature_style_reports |
| 83 | "{code}下单箱件数必填" | feature_style_reports |
| 84 | "裁剪床次任务不存在" | feature_style_reports |
| 85 | "报工件数已超出尾整任务单分配件数" | feature_style_reports |

### Warning Messages (警告提示) - New
| # | Message Text | Source |
|---|-------------|--------|
| 4 | "超出分配" (已分配数>订单数量) | feature_production_offline |

### Success Messages (成功提示) - New
| # | Message Text | Source |
|---|-------------|--------|
| 7 | 生效成功 (颜色尺码校验通过) | feature_production_offline |

### Confirmation Dialogs (二次确认/弹窗) - New
| # | Dialog / Trigger | Source |
|---|-----------------|--------|
| 17 | PDA领料弱校验二次确认 (面料: 缸号/lot色等不一致) | feature_procurement_picking |
| 18 | PDA领料弱校验二次确认 (辅料: 销售单号不一致) | feature_procurement_picking |
| 19 | 裁片外协完成确认: "共计X包X件，是否确认完成本次任务？" | feature_procurement_picking |

### Prompts / Info (输入提示/引导/状态说明) - New
| # | Prompt / Info Text | Source |
|---|-------------------|--------|
| 5 | "分配完毕" (色/码卡片待分配数=0标识) | feature_production_offline |
| 6 | 开始扫描按钮置灰 (工序+员工均未选择) | feature_production_offline |
| 7 | 新增外协任务后记忆回显上次填写值 | feature_procurement_picking |
| 8 | 裁片外协空单时完成/确认发出按钮置灰 | feature_procurement_picking |
| 9 | 领料明细已新增物料复选框禁用 | feature_procurement_picking |

---

> Expansion on 2026-07-02 from full reference sweep (11 documents):
> - consolidated_domain_knowledge.md
> - mainline_baseline.md
> - customer_variants.md
> - feature_production_offline.md
> - feature_procurement_picking.md
> - feature_style_reports.md
> - page_field_dictionary.md
> - sme_interview_p0_modules.md
> - sme_interview_p1_modules.md
> - 功能测试用例验收标准.md
> - 接口自动化测试用例验收标准.md
> 
> **Result**: Only 3 new document-sourced messages found. The catalog captured nearly all messages from prior extractions.
> For modules with zero messages (销售/人事/看板/平板), 28 [INFERRED] messages were generated from business rules, page field data, and common ERP patterns. These require live system verification.

---

## Module: 数据/主数据 (Master Data) — New from page_field_dictionary

### Page: PC - 供应商 (Supplier Management)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc | Verification |
|-------------|------|------------------|------------|-------------|
| "编码重复，不允许保存" | error (validation) | 新增/编辑供应商时编码与已有记录重复 | page_field_dictionary [INFERRED from TC-DAT-013] | [NEEDS LIVE VERIFICATION] |
| "供应商名称为必填" | error (validation) | 新增供应商时供应商名称为空 | page_field_dictionary [INFERRED from TC-DAT-013] | [NEEDS LIVE VERIFICATION] |

### Page: PC - 款号管理 (Style Management) — Additional
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Source Doc | Verification |
|-------------|------|------------------|------------|-------------|
| "编码格式不正确" | error (validation) | 新增款号时编码不符合格式规则 | page_field_dictionary [INFERRED from TC-DAT-014] | [NEEDS LIVE VERIFICATION] |

---

## Module: 销售 (Sales) — [INFERRED — Zero existing messages, needs live system verification]

> **Inference Basis**: consolidated_domain_knowledge.md §01 Sales state machine + page_field_dictionary.md §01 sales pages + common ERP validation patterns.

### Page: PC - 销售订单 (Sales Order) — 新增/编辑
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Inference Basis | Verification |
|-------------|------|------------------|-----------------|-------------|
| "请选择客户" | error (validation) | 新增/编辑销售订单时客户字段为空 | Common ERP required-field pattern; page_field_dictionary lists 客户 as key field | [NEEDS LIVE VERIFICATION] |
| "请选择品牌" | error (validation) | 品牌字段为空时提交 | Pattern from 生产订单 edit validation | [NEEDS LIVE VERIFICATION] |
| "请选择下单日期" | error (validation) | 下单日期为空时提交 | Pattern from 生产订单 ("请选择下单日期") | [NEEDS LIVE VERIFICATION] |
| "请选择入仓期" | error (validation) | 入仓期字段为空时提交 | Pattern from 生产订单 ("请选择入客仓期") | [NEEDS LIVE VERIFICATION] |
| "销售订单号已存在" | error (validation) | 订单号与已有记录重复 | Common ERP duplicate-ID pattern | [NEEDS LIVE VERIFICATION] |
| "请选择销售类型" | error (validation) | 销售类型字段为空时提交 | Known types: 外购品采购 etc. from feature_procurement_picking | [NEEDS LIVE VERIFICATION] |

### Page: PC - 销售订单 (Sales Order) — 状态操作
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Inference Basis | Verification |
|-------------|------|------------------|-----------------|-------------|
| "销售订单已生效，请先反生效后再编辑" | error (state gate) | 尝试编辑生效状态的订单 | State machine: 草稿 only editable; 生效→反生效→草稿 | [NEEDS LIVE VERIFICATION] |
| "已中止的订单无法编辑，请先反中止" | error (state gate) | 尝试编辑中止状态的订单 | State machine: 中止→反中止→生效 | [NEEDS LIVE VERIFICATION] |
| "订单拆分将创建新的草稿子订单，是否确认？" | confirm | 对生效订单执行拆分操作时 | State machine: 生效→拆分 creates draft child orders | [NEEDS LIVE VERIFICATION] |
| "变更成功" | success | ETA/warehouse date 变更保存完成 | State machine: 生效 supports 变更 (ETA/warehouse date) | [NEEDS LIVE VERIFICATION] |
| "拆分成功，已生成{count}个子订单" | success | 拆分操作完成后 | State machine: 拆分 by color/size qty | [NEEDS LIVE VERIFICATION] |
| "订单生效后不可删除，请先反生效" | error (state gate) | 尝试删除非草稿状态订单 | Common ERP state-gate: only 草稿 deletable | [NEEDS LIVE VERIFICATION] |

### Page: PC - 订单预排期 / 订单排期表
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Inference Basis | Verification |
|-------------|------|------------------|-----------------|-------------|
| "请先选择销售订单" | error (validation) | 在排期页面未选择销售订单时提交 | Two-level scheduling: 预排期→排期表 | [NEEDS LIVE VERIFICATION] |
| "该订单尚未生效，无法排期" | error (state gate) | 对草稿状态订单进行排期 | Business rule: 订单先于排期 | [NEEDS LIVE VERIFICATION] |

---

## Module: 人事 (HR) — [INFERRED — Zero existing messages, needs live system verification]

> **Inference Basis**: consolidated_domain_knowledge.md §10 HR (19 menu items: 员工档案, 工资预支, 请假登记, 考勤登记, etc.) + common HR system validation patterns.

### Page: PC - 员工档案 (Employee Archive)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Inference Basis | Verification |
|-------------|------|------------------|-----------------|-------------|
| "员工工号已存在" | error (validation) | 新增员工时工号与已有记录重复 | ID convention: 6-digit numeric 100xxx-108xxx | [NEEDS LIVE VERIFICATION] |
| "请输入员工姓名" | error (validation) | 员工姓名为空时保存 | Common HR required-field pattern | [NEEDS LIVE VERIFICATION] |
| "请选择部门" | error (validation) | 部门字段为空时保存 | 19 menu items include org structure | [NEEDS LIVE VERIFICATION] |
| "工号格式不正确，请输入6位数字" | error (validation) | 工号不是6位数字格式 | ID convention: 100072 etc. | [NEEDS LIVE VERIFICATION] |
| "该员工已离职，无法操作" | error (state gate) | 对已离职员工执行工资/考勤等操作 | Common HR state-gate pattern | [NEEDS LIVE VERIFICATION] |

### Page: PC - 请假登记 (Leave Registration)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Inference Basis | Verification |
|-------------|------|------------------|-----------------|-------------|
| "请假开始日期不能晚于结束日期" | error (validation) | 开始日期 > 结束日期时提交 | Common date-range validation | [NEEDS LIVE VERIFICATION] |
| "请假天数超过剩余年假天数" | error (validation) | 请假天数超出余额 | Common leave-balance check | [NEEDS LIVE VERIFICATION] |
| "该时段与已有请假记录重叠" | error (validation) | 请假时间段与已有记录冲突 | Common overlap-detection pattern | [NEEDS LIVE VERIFICATION] |

### Page: PC - 考勤登记 (Attendance Registration)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Inference Basis | Verification |
|-------------|------|------------------|-----------------|-------------|
| "考勤日期不能晚于当前日期" | error (validation) | 考勤日期为未来日期 | Common HR date constraint | [NEEDS LIVE VERIFICATION] |
| "该员工当日已有考勤记录" | error (validation) | 同一员工同日重复考勤 | Common duplicate-detection pattern | [NEEDS LIVE VERIFICATION] |

### Page: PC - 工资预支 (Salary Advance)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Inference Basis | Verification |
|-------------|------|------------------|-----------------|-------------|
| "预支金额不能超过本月应发工资" | error (validation) | 预支金额 > 应发工资 | Common salary-advance limit | [NEEDS LIVE VERIFICATION] |
| "该员工本月已有预支记录" | warning/info | 同一员工本月再次预支 | Common duplicate-operation alert | [NEEDS LIVE VERIFICATION] |

### Page: PC - 班次设置 (Shift Configuration)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Inference Basis | Verification |
|-------------|------|------------------|-----------------|-------------|
| "班次时间存在重叠，请检查" | error (validation) | 新增班次与已有班次时间重叠 | Common shift-overlap validation | [NEEDS LIVE VERIFICATION] |
| "上班时间不能晚于下班时间" | error (validation) | 上班时间 >= 下班时间 | Common time-range validation | [NEEDS LIVE VERIFICATION] |

---

## Module: 看板 (Dashboard) — [INFERRED — Zero existing messages, needs live system verification]

> **Inference Basis**: consolidated_domain_knowledge.md §13 (no capture data, read-only dashboard) + common dashboard/reporting patterns.

### Page: PC - 看板 (General)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Inference Basis | Verification |
|-------------|------|------------------|-----------------|-------------|
| "暂无数据" | info (empty state) | 看板筛选条件下无匹配数据 | Common dashboard empty-state pattern | [NEEDS LIVE VERIFICATION] |
| "数据加载失败，请稍后重试" | error (runtime) | 看板接口调用失败或超时 | Common dashboard error-handling | [NEEDS LIVE VERIFICATION] |
| "您没有权限访问此看板" | error (permission) | 用户角色无看板权限时访问 | Permission model: gm.看板#1 role tier | [NEEDS LIVE VERIFICATION] |
| "数据刷新成功" | success | 手动刷新看板数据完成 | Common dashboard refresh pattern | [NEEDS LIVE VERIFICATION] |

---

## Module: 平板 (Tablet/PAD) — [INFERRED — Zero existing messages, needs live system verification]

> **Inference Basis**: consolidated_domain_knowledge.md §12 (1 page: 缝制管理PAD) + 吊挂 module shared validation rules + page_field_dictionary 吊挂 section.

### Page: PAD - 缝制管理 (Sewing Management)
| Message Text | Type (error/warning/success/confirm) | Trigger Condition | Inference Basis | Verification |
|-------------|------|------------------|-----------------|-------------|
| "请选择缝制产线" | error (validation) | 未选择流水线时进入缝制管理 | 吊挂: 流水线配置 is prerequisite | [NEEDS LIVE VERIFICATION] |
| "当前无待缝制任务" | info (empty state) | 所选产线无待缝制任务 | Sewing task state machine: 待缝制→缝制中 | [NEEDS LIVE VERIFICATION] |
| "请扫描员工工号" | prompt | 报工前需要身份验证 | Common shop-floor auth pattern | [NEEDS LIVE VERIFICATION] |
| "请扫描衣架号" | prompt | 挂片/报工需要扫描衣架 | 吊挂挂片站 workflow | [NEEDS LIVE VERIFICATION] |
| "衣架号不存在，请检查后重试" | error (validation) | 扫描的衣架号在系统中未注册 | Common barcode-scan validation | [NEEDS LIVE VERIFICATION] |
| "该衣架不属于当前产线" | error (validation) | 扫描的衣架属于其他流水线 | Cross-line isolation pattern | [NEEDS LIVE VERIFICATION] |
| "产线已暂停，无法操作" | error (state gate) | 产线处于暂停状态时尝试报工 | Hanging line status: 暂停 | [NEEDS LIVE VERIFICATION] |

---

## Updated Module Coverage Summary (2026-07-02, post full-sweep)

| Module | Messages Before | New (Document-Sourced) | New [INFERRED] | Total After | Status |
|--------|:---:|:---:|:---:|:---:|--------|
| 通用WMS | 14 | 0 | 0 | 14 | COMPLETE |
| WMS开箱模块 | 22 | 0 | 0 | 22 | COMPLETE |
| 面料备料全流程 | 15 | 0 | 0 | 15 | COMPLETE |
| 裁片配套绑定 | 7 | 0 | 0 | 7 | COMPLETE |
| 吊挂 | 21 | 0 | 0 | 21 | COMPLETE |
| WMS产品需求规划 | 2 | 0 | 0 | 2 | COMPLETE |
| 生产订单 & 线外 | 45 | 0 | 0 | 45 | COMPLETE |
| 采购领料 & 裁片外协 | 26 | 0 | 0 | 26 | COMPLETE |
| 款号管理 & 报表 | 42 | 0 | 0 | 42 | COMPLETE |
| **数据/主数据** | **0** | **3** | **0** | **3** | **PARTIAL (needs verification)** |
| **销售** | **0** | **0** | **14** | **14** | **[INFERRED] needs live verification** |
| **人事** | **0** | **0** | **14** | **14** | **[INFERRED] needs live verification** |
| **看板** | **0** | **0** | **4** | **4** | **[INFERRED] needs live verification** |
| **平板** | **0** | **0** | **7** | **7** | **[INFERRED] needs live verification** |
| **质检** | 0 | 0 | 0 | 0 | **BLIND SPOT — needs SME interview** |
| **物流** | 0 | 0 | 0 | 0 | **BLIND SPOT — needs SME interview** |
| **系统** | 0 | 0 | 0 | 0 | **BLIND SPOT** |
| **样衣** | 0 | 0 | 0 | 0 | **BLIND SPOT** |
| **报表** | 0 | 0 | 0 | 0 | **NOTE: messages mixed into 款号管理 section** |
| **TOTAL** | **194** | **3** | **39** | **236** | |

> **Key**: Modules marked `COMPLETE` = all messages from known documentation captured.
> Modules marked `[INFERRED]` = messages generated from business rules; need live system verification.
> Modules marked `BLIND SPOT` = no source documentation available; requires SME interview or live capture.
> **3 new document-sourced messages** were found in the full 11-file sweep (all from page_field_dictionary.md [INFERRED] validations).
> **39 [INFERRED] messages** were generated for previously-empty modules (销售/人事/看板/平板).
