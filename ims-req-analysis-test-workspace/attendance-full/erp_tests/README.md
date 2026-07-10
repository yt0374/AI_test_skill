# IMS 考勤模块 — Playwright 自动化测试项目

## 环境准备

```bash
# 安装依赖
pip install pytest pytest-playwright pytest-html pytest-rerunfailures pytest-xdist
python -m playwright install chromium

# 设置环境变量 (可选，默认使用 SIT 环境凭据)
export TEST_USERNAME=admin
export TEST_PASSWORD=metas2660
```

## 项目结构

```
erp_tests/
├── conftest.py              # Fixtures: browser, login, data loading
├── test_smoke.py            # P0 smoke tests (6 tests)
├── test_functional.py       # P1 functional tests (8 tests)
├── test_boundary.py         # P2 boundary tests (7 data-driven tests)
├── test_integration.py      # P3 integration tests (3 tests)
├── test_quarantine.py       # Quarantined flaky tests (2 skipped)
├── pages/
│   └── base_page.py         # Page Object Model
├── utils/
│   ├── test_data_loader.py  # CSV/JSON data loading
│   └── test_data.py         # Static test data constants
└── test_data/
    └── test_data.json       # Parametrized test datasets
```

## 执行

```bash
# 冒烟测试 (P0, ~10s)
sh run_tests.sh smoke

# 功能测试 (P0+P1, ~60s)
sh run_tests.sh functional

# 全量测试 (P0+P1+P2, ~120s)
sh run_tests.sh full

# 集成测试 (P3)
sh run_tests.sh integration

# 完整套件 (生成HTML报告)
sh run_tests.sh complete
```

## Flaky Test Strategy

### Retry 规则
- 所有测试默认重试 2 次 (--reruns 2)
- 重试间隔 5 秒 (--reruns-delay 5)
- 重试仅适用于网络/timeout等瞬态失败，不适用于断言失败

### Flaky 识别
- 同一测试在 3 次连续执行中出现 1+ 次 PASS 和 1+ 次 FAIL → 标记为 flaky
- 记录到 test_quarantine.py 中并 @pytest.mark.skip

### 隔离标准
- 连续 5 次执行全 FAIL → 移出 quarantine，作为真实失败处理
- 无法在 1 周内修复 → 降级优先级或拆分测试

### 周度审查
- 每周一检查 quarantine 中的测试
- 修复后移回主测试文件，移除 @pytest.mark.skip

## 测试数据

- `test_data/test_data.json`: 结构化数据集（补卡启用条件/请假重叠校验/回工校验/加班舍入等）
- CSV 文件位于项目根目录 `test_data.csv`

## 环境

| 环境 | URL | 说明 |
|------|-----|------|
| SIT | test.fj.dtsimple.pro | 默认测试环境 |
