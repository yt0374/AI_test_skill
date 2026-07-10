# Step 3: 自动化脚本

> 承接 Step 2（用例+数据文件）| 产出：erp_tests/ + api_spec + pytest.ini

---

## 3.1 项目结构

```
erp_tests/
├── conftest.py              # browser/login/api_client/data_loaders
├── test_smoke.py            # P0 冒烟
├── test_functional.py       # P1 功能（参数化）
├── test_boundary.py         # P2 边界
├── test_integration.py      # P3 集成
├── test_api.py              # API测试（API-heavy文档）
├── test_quarantine.py       # 隔离区
├── pages/base_page.py       # POM
├── utils/                   # test_data_loader + constants
├── test_data/               # JSON/CSV + api_payloads
├── pytest.ini               # 配置
├── run_tests.sh             # 执行脚本
└── README.md
```

## 3.2 用例→代码映射

| Step 2产出 | Step 3文件 | 示例 |
|:---:|------|------|
| F-xx 核心流程 | test_smoke.py (P0) | F-01: 销售订单页面加载 |
| V-xx 校验 | test_boundary.py (P2) | V-05: 信用额度参数化 |
| C-/U-/L- 功能 | test_functional.py (P1) | L-01: 订单列表筛选 |
| A-xx API | test_api.py (P1-P2) | A-01: 物料同步字段校验 |
| 集成 | test_integration.py (P3) | 生产→采购→WMS E2E |

## 3.3 API Spec 编译（API-heavy文档）

```bash
# Spec(YAML) → pytest 脚本
python scripts/generate_pytest.py spec.md -o test_api.py
pytest test_api.py --collect-only -q  # 验证
```

**生成能力：** 字段校验 / Schema验证 / 枚举覆盖 / H+X双覆盖 / S安全 / E边界 / 回调模拟 / 变量池链

## 3.4 数据参数化

> **承接 Step 2.7**：test_data.json → pytest parametrize

```python
DATA = load_dataset("credit_limit_validation")
PARAMS = [(d["customer"], d["limit"], d["amount"],
           d["expected"], d.get("message","")) for d in DATA]

@pytest.mark.p1
@pytest.mark.parametrize("customer,limit,amount,expected,msg", PARAMS)
def test_credit_validation(page, customer, limit, amount, expected, msg):
    ...
```

## 3.5 Flaky 策略

| 机制 | 配置 |
|------|------|
| 自动重试 | `--reruns 2 --reruns-delay 5` |
| 识别 | 重试通过→`@pytest.mark.flaky` |
| 隔离 | >50%失败×5轮→test_quarantine.py |
| 周审 | 每周审阅，修复或退役 |

## 3.6 失败截图（自动）

conftest.py 内置 `pytest_runtest_makereport` 钩子，测试失败时自动截图：

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    if outcome.get_result().failed and call.when == "call":
        page = item.funcargs.get("page")
        if page:
            page.screenshot(path=f"reports/screenshots/{item.name}_{timestamp}.png")
```

截图保存到 `reports/screenshots/`，文件名含用例名+时间戳。断言失败/超时/错误均触发。

## 3.7 环境登录

```python
from scripts.ims_login import login
login(page, "sit", enterprise="最佳智造")
login(page, "xinji")
```

自动处理企业选择器（SIT/UAT）和差异化密码（UAT最佳智造→qwe123）。

## 3.8 文件数控制

| 文档类型 | 目标文件数 |
|:---:|:---:|
| API-heavy | ≤20 |
| UI-heavy | ≤16 |
| Hybrid | ≤22 |
| Light | ≤12 |

**精简规则：** .ps1合并到.sh / .html仅.md / .json跳过(CSV全覆盖) / quarantine跳过(Light)

## 3.9 产出清单

| 文件 | 内容 | → 流向 |
|------|------|:---:|
| `erp_tests/` | Playwright/pytest 完整项目 | → Step 4 |
| `pytest.ini` | Pytest 配置（markers+retry） | → Step 4 |
| `run_tests.sh` | 执行脚本（6模式） | → Step 4 |
