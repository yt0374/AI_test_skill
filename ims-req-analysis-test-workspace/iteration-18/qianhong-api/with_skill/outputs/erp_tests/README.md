# 千虹API接口测试 — 自动化项目

千虹客户 IMS v3.x API/SPI 接口自动化测试项目。基于 pytest + httpx，覆盖15个API端点。

## 环境要求

- Python 3.10+
- httpx
- pytest
- pytest-rerunfailures
- pytest-json-report

## 安装

```bash
pip install httpx pytest pytest-rerunfailures pytest-json-report
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `IMS_BASE_URL` | `http://test.fj.dtsimple.pro/api/ims-open-api` | IMS API基地址 |
| `IMS_TEST_USERNAME` | `admin` | 测试账号用户名 |
| `IMS_TEST_PASSWORD` | `IMS@2026` | 测试账号密码 |

## 执行命令

| 模式 | 命令 | 说明 |
|------|------|------|
| Smoke | `pytest erp_tests/test_api.py -m p0 -v` | P0冒烟（17条） |
| Functional | `pytest erp_tests/test_api.py -m "p0 or p1" -v` | P0+P1功能（50条） |
| Full | `pytest erp_tests/test_api.py -m "p0 or p1 or p2" -v` | P0+P1+P2全量（104条） |
| Complete | `pytest erp_tests/test_api.py -v` | 含P3集成（112条） |

或使用执行脚本：
```bash
# Linux/Mac
bash erp_tests/run_tests.sh smoke
bash erp_tests/run_tests.sh full

# Windows PowerShell
.\erp_tests\run_tests.ps1 smoke
.\erp_tests\run_tests.ps1 full
```

## 项目结构

```
erp_tests/
├── conftest.py           # Fixtures: api_client, auth_token
├── test_api.py           # API测试主文件（112个测试用例）
├── test_quarantine.py    # 隔离的不稳定测试
├── pytest.ini            # Pytest配置（markers + retry）
├── run_tests.sh          # Linux/Mac执行脚本
├── run_tests.ps1         # Windows PowerShell执行脚本
├── utils/
│   └── test_data_loader.py  # 测试数据加载工具
└── test_data/
    └── api_payloads.json    # API测试payloads
```

## 环境执行顺序

1. **SIT环境**（千虹_测试）：test.fj.dtsimple.pro → 选择企业"千虹_测试"
2. **模拟生产**（如需要）：根据customer_variants.md，千虹为SIT主线子集，无需独立模拟生产环境

## Flaky Test Strategy

### 重试策略
- `--reruns 2`：失败用例自动重试2次
- `--reruns-delay 5`：重试间隔5秒
- 仅对5xx/网络错误重试，4xx不重试（参数错误无意义重试）

### 识别标准
- 同一用例在7天内失败 > 3次
- 失败模式不固定（非确定性）
- 根因确认为环境/数据问题（非代码缺陷）

### 隔离标准
- 满足识别标准后移入 `test_quarantine.py`
- 添加 `@pytest.mark.skip` 和 `@pytest.mark.quarantine`
- 记录隔离原因和时间

### 审查周期
- 每周一审查隔离用例
- 修复后移回主测试文件
- 超过2周未修复的标记为已知问题

## 测试数据

测试数据定义在两个文件中：
- `../test_data.csv` — 数据变化场景CSV（业务评审用）
- `../test_data.json` — 结构化JSON数据（自动化加载用）

## 文档审计要点

生成的测试脚本考虑了以下文档问题（详见 `../requirements_audit.md`）：
- URL路径缺失斜杠（AUD-001/002）— 测试中使用补全后的路径
- 字段名冲突 deptName（AUD-004）— 待文档修正后更新
- Token刷新未定义（AUD-W01）— 在conftest中使用session级token
- 生产/缝制同步缺响应（AUD-005）— 仅做状态码验证
