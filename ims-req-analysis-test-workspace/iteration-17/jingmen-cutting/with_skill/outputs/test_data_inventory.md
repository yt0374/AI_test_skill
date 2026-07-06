# Test Data Inventory: 荆门新裁剪2.0

> 基于需求文档提取，结合荆门环境 (bak.jmym.dtsimple.pro) 特征

---

## 1. Entity Catalog

### 1.1 CPO (Customer Purchase Order)

| Variation | Description | Test Relevance |
|-----------|-------------|----------------|
| Single CPO | 裁剪任务只包含一个 CPO | 场景B：指定扎卡，优先绑定 |
| Multiple CPO (same delivery date) | 多个 CPO 同一交期 | 智能合并验证 |
| Multiple CPO (different delivery dates) | 多个 CPO 不同交期 | 智能合并边界、交期排序验证 |
| All CPO selected | 全选当前订单所有 CPO | 全选功能验证 |
| CPO with zero remaining quantity | 已满额 CPO | 满额切换提示 |
| CPO with partial quantity | 部分满额 CPO | 混合充数场景 |

### 1.2 裁剪任务 (Cutting Task)

| Variation | Description | Test Relevance |
|-----------|-------------|----------------|
| 未开始 (Not Started) | 刚创建，无床次 | 可编辑/删除，不可开始拉布 |
| 拉布中 (In Progress) | 至少有一个床次为拉布中或已拉布 | 不可编辑/删除，可新增床次 |
| 已完成 (Completed) | 所有床次已提交，剩余层数为 0 | 不可新增床次 |
| Single CPO task | 仅关联一个 CPO | 扎卡印刷 CPO 号 |
| Merged CPO task | 关联多个 CPO | 通用扎卡，隐藏 CPO |

### 1.3 唛架 (Marker)

| Variation | Description | Test Relevance |
|-----------|-------------|----------------|
| 未分配 (Available) | 剩余层数 = 总计划层数 | 初次分配基准 |
| 部分分配 (Partial) | 0 < 剩余层数 < 总计划层数 | 递减规则验证 |
| 分配完毕 (Fully Allocated) | 剩余层数 = 0 | 不可再选择 |
| 超出分配 (Over-allocated) | （防超分配禁止） | 强控拒绝场景 |

### 1.4 床次 (Bed/Lay)

| Variation | Description | Test Relevance |
|-----------|-------------|----------------|
| 拉布中 (Laying) | 创建成功但未提交完成 | 暂扣层数 |
| 已拉布 (Completed) | 提交完成，锁定实际层数 | 锁定层数，生成床次号 |
| 输入层数 = 剩余 | 边界：恰好用完 | 校验通过，剩余归零 |
| 输入层数 < 剩余 | 正常场景 | 校验通过 |
| 输入层数 > 剩余 | 边界：超裁 | 软预警/强控禁止 |

### 1.5 扎卡 (Tag)

| Variation | Description | Test Relevance |
|-----------|-------------|----------------|
| 通用扎卡 (Generic) | 无 CPO 信息，合并 CPO 任务 | 挂片自动充数 |
| 指定扎卡 (Specific) | 有 CPO 号，单一 CPO 任务 | 优先绑定+顺延 |

### 1.6 挂片模式 (Hanging Mode)

| Variation | Description | Test Relevance |
|-----------|-------------|----------------|
| 自动充数 (Auto) | 默认模式，系统自动分配 | 交期排序验证 |
| 手动充数 (Manual) | 员工自主选择 CPO | 自由选择、满额切换 |
| 自动→手动切换 | 保存进度后切换 | 进度保持验证 |
| 手动→自动切换 | 重新按交期计算 | 重新分配验证 |

---

## 2. Data Variation Dimensions

| Requirement | Data Entity | Variations Needed | Coverage Target |
|-------------|------------|-------------------|-----------------|
| F001 (CPO选择) | CPO | Single, Multiple-SameDate, Multiple-DiffDate, All | 4/4 |
| F002 (唛架分配) | 唛架 | Available, Partial, Full, Over | 4/4 |
| F003 (裁剪任务管理) | 裁剪任务 | NotStarted, InProgress, Completed | 3/3 |
| F004 (床次创建) | 床次 | Normal, Exact Boundary, Over | 3/3 |
| F005 (床次提交) | 床次 | Equal, Less, More than reserved | 3/3 |
| F008 (扎卡打印) | 扎卡 | Generic, Specific | 2/2 |
| F009 (自动充数) | 挂片 | Generic tag, Specific tag, CPO full | 3/3 |
| F010 (手动充数) | 挂片 | Free select, Full CPO switch, Mode toggle | 3/3 |

---

## 3. Test Data Records

### 3.1 CPO Test Set

| CPO ID | 交期 | 件数 | 用途 |
|--------|------|------|------|
| CPO-A | 2026-07-01 | 500 | 单独裁剪（单一CPO场景） |
| CPO-B | 2026-07-05 | 300 | 合并裁剪（同交期） |
| CPO-C | 2026-07-05 | 200 | 合并裁剪（同交期，与B合并） |
| CPO-D | 2026-07-10 | 400 | 不同交期合并测试 |
| CPO-E | 2026-07-01 | 100 | 与A同交期，测试智能合并 |

### 3.2 唛架 Test Set

| 唛架 ID | 总计划层数 | 测试阶段 |
|---------|-----------|---------|
| MK-001 | 100 | 初始：可用=100 |
| MK-001 | 100 | 分配40→可用=60 |
| MK-001 | 100 | 再分配50→可用=10 |
| MK-001 | 100 | 尝试分配20→拒绝（超出） |

### 3.3 床次 Test Set

| 床次 | 布卷号 | 输入层数 | 剩余可用 | 预期结果 |
|------|--------|---------|---------|---------|
| B-01 | FB001 | 30 | 60 | 通过，暂扣30 |
| B-02 | FB002 | 30 | 30 | 通过，剩余=0 |
| B-03 | FB003 | 5 | 0 | 预警（剩余不足10层） |
| B-04 | FB004 | 10 | 0 | 强控禁止（剩余为负） |

### 3.4 挂片 Test Set

| 场景 | 扎卡类型 | CPO 状态 | 预期行为 |
|------|---------|---------|---------|
| H-01 | 通用扎卡 | CPO-A(7/1,500), CPO-B(7/5,300) | 自动充入A→满额→切换B |
| H-02 | 指定扎卡(CPO-A) | CPO-A(7/1,500), CPO-B(7/5,300) | 优先A→满额→顺延B |
| H-03 | 手动选择 | 所有CPO未满 | 自由选择CPO-B→挂片 |
| H-04 | 手动选择 | CPO-B已满 | 弹窗提示"CPO B 数量已满" |

---

## 4. Module Data Source Mappings

| Data Entity | Source Module | Source Page | Key Fields |
|-------------|--------------|-------------|------------|
| CPO | 生产 | 生产订单 | CPO编号, 交期, 件数, 颜色, 尺码 |
| 生产订单 | 生产 | 生产订单 | 生产订单号, 款号, 客户, 品牌 |
| 唛架 | 生产 | 唛架管理 | 唛架号, 总计划层数, 段长, 配比 |
| 布卷号 | 仓库 | 面料库存管理 | 物料条码, 缸号, 库存数量 |
| 生产组别 | 生产 | 部门管理 | 组别名称, 工段类型 |
| 款号 | 数据 | 款号管理 | 款号, 客户款号, 颜色尺码 |

---

## 5. Environment-Specific Data (荆门 jingmen)

| Attribute | Value |
|-----------|-------|
| 环境 URL | `http://bak.jmym.dtsimple.pro` |
| 账号 | admin / ym5579 |
| 登录方式 | 直接登录（无企业选择器） |
| 模块命名 | 简单名（`生产` 非 `gm.生产#3`） |
| 子菜单 | `.third-menu` 面板 |
| 生产模块菜单项 | 35项（含线外任务、裁剪任务、床次任务等） |
| 缺模块 | 样衣、销售、人事、物流 |
| 特殊配置 | LOT色支持、面料+颜色级质检 |
