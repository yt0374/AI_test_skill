# Step 4: 测试执行

> 承接 Step 3（erp_tests/）| 产出：pytest_results.json

---

## 4.1 环境执行顺序

```
SIT (test.fj.dtsimple.pro, 主线)
  │  P0+P1: 100% P0, ≥95% P1
  ↓
客户验证（按优先级）:
  ├── 1️⃣ UAT企业（如有）→ uat.fj.dtsimple.pro
  └── 2️⃣ 模拟生产 bak.*（如无UAT）
  │  P0+P1: 100% P0, ≥90% P2
  ↓
上线
```

### 环境说明

| 环境 | URL | 类型 | 企业选择器 |
|------|-----|:---:|:---:|
| SIT | test.fj.dtsimple.pro | 测试 | ✅ 13个 |
| UAT | uat.fj.dtsimple.pro | 验收 | ✅ 6个 |
| xinji | bak.xinji.dtsimple.pro | 模拟生产 | ❌ |
| jingmen | bak.jmym.dtsimple.pro | 模拟生产 | ❌ |
| ajn | bak.ajn.dtsimple.pro | 模拟生产 | ❌ |

## 4.2 执行模式

| 模式 | 命令 | 场景 | 耗时 |
|------|------|------|:---:|
| Smoke | `pytest -m p0` | 每次提交 | ~5min |
| API | `pytest test_api.py` | 接口验证 | ~10min |
| Functional | `pytest -m "p0 or p1"` | 每日回归 | ~15min |
| Full | `pytest -m "p0 or p1 or p2"` | 发布前验证 | ~30min |
| Integration | `pytest -m p3` | 跨模块 | ~20min |
| Complete | `pytest` | 全量 | ~60min |

## 4.3 执行前检查

```bash
# 1. 环境探测
python scripts/probe_env.py spec.md --env sit

# 2. 验证可采集
pytest erp_tests/ --collect-only -q

# 3. 执行
./run_tests.sh smoke   # 或 functional/full/complete
```

## 4.4 多客户并行

```
SIT (主线基线)
  ↓
├── UAT > 安吉纳_验收 (如有)
├── 模拟生产 > xinji (新基)
├── 模拟生产 > jingmen (荆门)
└── 模拟生产 > ajn (安吉纳，如无UAT)
```

差异用例从 `references/customer_variants.md` 读取，仅对差异模块执行。
公共模块用例在 SIT 阶段完成，不在客户环境重复执行。

## 4.5 通过标准

| 阶段 | 环境 | 用例范围 | 通过标准 | 阻塞条件 |
|:---:|------|------|------|------|
| 1 | SIT | P0+P1 | 100% P0, ≥95% P1 | 任一 P0 失败 |
| 2 | 客户验证 | P0+P1+P2 | 100% P0+P1, ≥90% P2 | 任一 P1 失败 |
| 3 | 上线 | P0~P3 | 100% P0+P1, ≥85% P2+P3 | 任一 P0 失败 |

## 4.6 产出清单

| 文件 | 内容 | → 流向 |
|------|------|:---:|
| `pytest_results.json` | 结构化执行结果 | → Step 5 |
| `junit.xml` | CI 集成 | → Step 5 |
