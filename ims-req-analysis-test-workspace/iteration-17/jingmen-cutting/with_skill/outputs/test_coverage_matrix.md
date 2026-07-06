# Test Coverage Matrix: 荆门新裁剪2.0

## Coverage Summary

| Requirement | P0 | P1 | P2 | P3 | Total | Coverage % |
|------------|----|----|----|----|-------|-----------|
| F001 (CPO选择与合并) | 2 | 2 | 0 | 1 | 5 | 100% |
| F002 (唛架层数分配与递减) | 0 | 4 | 2 | 0 | 6 | 100% |
| F003 (顶层任务管理PC) | 2 | 2 | 1 | 0 | 5 | 100% |
| F004 (现场床次创建PAD) | 1 | 2 | 3 | 0 | 6 | 100% |
| F005 (床次提交完成) | 0 | 3 | 0 | 0 | 3 | 100% |
| F006 (床次号唯一性) | 0 | 1 | 2 | 0 | 3 | 100% |
| F007 (防超裁机制) | 0 | 4 | 1 | 0 | 5 | 100% |
| F008 (扎卡打印CPO关联) | 2 | 2 | 0 | 0 | 4 | 100% |
| F009 (自动充数模式) | 2 | 1 | 0 | 0 | 3 | 100% |
| F010 (手动充数模式) | 0 | 4 | 1 | 0 | 5 | 100% |
| **合计** | **9** | **25** | **10** | **1** | **45** | — |

## Priority Distribution

| Priority | Count | % | Target | Status |
|----------|-------|---|--------|--------|
| P0 | 9 | 20.0% | ≤20% | In Range |
| P1 | 25 | 55.6% | ≈40% | Slightly Over |
| P2 | 10 | 22.2% | ≈30% | Under |
| P3 | 1 | 2.2% | ≤10% | In Range |
| **Total** | **45** | 100% | — | — |

## Data Variation Coverage

| Data Entity | Variations Defined | Variations Covered | Coverage % |
|-------------|-------------------|-------------------|-----------|
| CPO | 6 | 6 | 100% |
| 裁剪任务状态 | 3 | 3 | 100% |
| 唛架分配状态 | 4 | 4 | 100% |
| 床次创建状态 | 3 | 3 | 100% |
| 扎卡类型 | 2 | 2 | 100% |
| 挂片模式 | 4 | 4 | 100% |

## Traceability Matrix

| Test ID | Requirement ID | Scenario | Priority | Data Variation | Module |
|---------|---------------|----------|----------|---------------|--------|
| F-01 | F001-F008 | 单CPO全流程 | P0 | Single CPO | 裁剪+扎卡+挂片 |
| F-02 | F001-F007 | 多CPO合并+并发 | P0 | Multiple CPO | 裁剪+床次 |
| F-03 | F010 | 手动充数挂片 | P1 | Manual mode | 挂片 |
| F-04 | F003 | 裁剪任务PAD同步 | P0 | Not started | 裁剪 |
| F-05 | F009 | 通用扎卡自动分配 | P0 | Generic tag | 挂片 |
| F-06 | F009 | 指定扎卡优先绑定 | P0 | Specific tag | 挂片 |
| F-07 | F009 | 指定扎卡满额顺延 | P1 | Tag type | 挂片 |
| F-08 | F010 | 手动模式CPO列表 | P1 | Manual mode | 挂片 |
| F-09 | F010 | 手动自由挂片 | P1 | Manual mode | 挂片 |
| F-10 | F010 | CPO满额强制切换 | P1 | Full CPO | 挂片 |
| F-11 | F010 | 自动→手动切换 | P1 | Mode switch | 挂片 |
| F-12 | F010 | 手动→自动切换 | P1 | Mode switch | 挂片 |
| F-13 | F010 | 自由选择跳过交期 | P2 | Manual mode | 挂片 |
| C-01 | F001 | 单CPO创建任务 | P0 | Single CPO | 裁剪 |
| C-02 | F001 | 多CPO创建任务 | P0 | Multiple CPO | 裁剪 |
| C-03 | F001 | 全选CPO | P1 | All CPO | 裁剪 |
| C-04 | F001 | 智能合并CPO | P1 | Same delivery date | 裁剪 |
| C-05 | F003 | 任务默认未开始 | P0 | Initial state | 裁剪 |
| C-06 | F004 | 床次层数小于剩余 | P0 | Normal input | 床次 |
| C-07 | F004 | 床次层数等于剩余 | P1 | Exact boundary | 床次 |
| C-08 | F005 | 实际层数等于暂扣 | P1 | Exact match | 床次 |
| L-01 | F008 | 合并CPO隐藏CPO | P0 | Merged CPO | 扎卡 |
| L-02 | F008 | 单一CPO显示CPO | P0 | Single CPO | 扎卡 |
| D-01 | F008 | 合并CPO按布卷分扎 | P1 | Merged CPO | 扎卡 |
| D-02 | F008 | 单一CPO按件数分扎 | P1 | Single CPO | 扎卡 |
| U-01 | F003 | 未开始可编辑 | P1 | Not started | 裁剪 |
| X-01 | F003 | 未开始可删除 | P1 | Not started | 裁剪 |
| V-01 | F002 | 唛架层数递减 | P1 | Partial allocation | 唛架 |
| V-02 | F002 | 唛架满禁止选择 | P1 | Full allocation | 唛架 |
| V-03 | F002 | 超剩余拒绝 | P1 | Over allocation | 唛架 |
| V-04 | F002 | 层数为0拒绝 | P2 | Zero input | 唛架 |
| V-05 | F002 | 层数等于剩余 | P2 | Exact boundary | 唛架 |
| V-06 | F002 | 未选唛架拒绝 | P2 | Missing required | 唛架 |
| V-07 | F003 | 拉布中禁编辑 | P1 | State gate | 裁剪 |
| V-08 | F003 | 拉布中禁删除 | P1 | State gate | 裁剪 |
| V-09 | F003 | 已完成禁新增床次 | P2 | State gate | 裁剪 |
| V-10 | F004 | 无效布卷号 | P2 | Invalid barcode | 床次 |
| V-11 | F004 | 非正整数层数 | P2 | Invalid input | 床次 |
| V-12 | F004+F007 | 超剩余预警 | P1 | Soft warning | 床次 |
| V-13 | F004+F007 | 超剩余强控 | P1 | Hard block | 床次 |
| V-14 | F004 | 并发先到先得 | P2 | Concurrent | 床次 |
| V-15 | F005 | 实际<暂扣归还 | P1 | Less than reserved | 床次 |
| V-16 | F005 | 实际超出可调范围 | P1 | Over range | 床次 |
| V-17 | F006 | 床次号全局递增 | P1 | Sequential | 床次 |
| V-18 | F006 | 同秒DB ID为准 | P2 | Concurrent | 床次 |
| V-19 | F006 | 主布C辅布F前缀 | P2 | Prefix rule | 床次 |
| V-20 | F007 | 软预警阈值 | P1 | Threshold trigger | 防超裁 |
| V-21 | F007 | 强控禁止 | P1 | Hard block | 防超裁 |
| V-22 | F007 | PC审核放行 | P1 | Approve | 防超裁 |
| V-23 | F007 | PC审核驳回 | P2 | Reject | 防超裁 |

## Boundary Test Coverage (V- prefix)

| Boundary Target | Tests | % of Total |
|----------------|-------|------------|
| 层数边界 (唛架分配) | V-01, V-02, V-03, V-04, V-05 | 5 |
| 层数边界 (床次创建) | V-12, V-13, V-20, V-21 | 4 |
| 状态门控边界 | V-07, V-08, V-09 | 3 |
| 输入校验边界 | V-10, V-11, V-16 | 3 |
| 唯一性边界 | V-17, V-18, V-19 | 3 |
| 并发边界 | V-14 | 1 |
| 审核边界 | V-22, V-23 | 2 |
| 必填边界 | V-06, V-04 | 2 |
| **Total V- cases** | | **23 (51.1%)** |

> Boundary test ratio: 23/45 = 51.1% — exceeds the ≥30% target.
