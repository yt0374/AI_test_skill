# IMS ERP Test Scripts

Python 工具脚本，支持测试全生命周期自动化。

## 脚本一览

| 脚本 | 用途 | 输入 | 输出 |
|------|------|------|------|
| `probe_env.py` | 环境探测，确认 API 可用性 | spec.md | `*_env_report.md`, `*_filtered.md` |
| `generate_pytest.py` | Spec → pytest 代码生成 | spec.md (YAML frontmatter) | `test_api.py` |
| `generate_test_data.py` | 需求文档 → 边界值数据集 | `requirements_spec.md` | `test_data.json` |
| `ingest_feedback.py` | 执行结果 → 反馈分析 | `test_results.json` | `lessons_learned.md` |
| `ims_login.py` | IMS 系统登录工具 | 环境配置 | Session/Token |

---

## probe_env.py — 环境探测

执行前检测 API 可用性，避免全量 404 或环境不匹配。

```bash
python scripts/probe_env.py spec.md                          # 基础探测
python scripts/probe_env.py spec.md --base-url http://wms-server:8080/api
python scripts/probe_env.py spec.md --filter-spec -o spec_filtered.md  # 仅保留可用端点
```

**端点分类：** `available`(200+JSON), `auth_required`(401/403), `not_found`(404), `method_not_allowed`(405), `spa_page`(200+HTML), `server_error`(5xx), `unreachable`(0)

---

## generate_pytest.py — Spec → pytest

将 YAML frontmatter 格式的 API 测试 Spec 编译为可执行 pytest 脚本。

```bash
python scripts/generate_pytest.py <spec.md> --output <test_file.py>
pytest <test_file.py> --collect-only -q          # 验证可采集
pytest <test_file.py> -v --tb=short              # 执行
```

**Spec 格式：** `kind: api_pytest`，含 `base_url`、`cases[]`（id/method/path/expect_status/json_body/extract_vars/depends_on/data_source）和 `scenarios[]`（多步场景 + capture 步间传值）。

**占位符：** `{{timestamp}}`（秒级时间戳）、`{{uuid}}`（UUID4前8位）、`${变量名}`（变量池引用）。

**依赖链：** 上游 `extract_vars` → 下游 `depends_on` + `${var}` → 上游失败时下游自动 `pytest.skip()`。

```bash
# Spec 语法检查
python -c "import yaml; yaml.safe_load(open('spec.md').read().split('---')[1])"
# 完整验收流程
python scripts/generate_pytest.py spec.md -o test.py
pytest test.py --collect-only -q && pytest test.py -v --tb=short
```

---

## generate_test_data.py — 边界值生成

从 requirements_spec.md 提取数值约束和枚举定义，自动生成 pytest parametrize 可用的 JSON 数据集。

```bash
python scripts/generate_test_data.py requirements_spec.md -o test_data.json
python scripts/generate_test_data.py requirements_spec.md --pairwise -o test_data_reduced.json
```

**约束识别：** `X > N`(N-1拒绝/N拒绝/N+1通过), `X ≥ N`(N-1拒绝/N通过/N+1通过), `X < N`, `X ≤ N`, `N~M范围`(6点), `最多N次`

---

## ingest_feedback.py — 反馈闭环

读取 `test_results.json`，分析失败模式，生成改进建议。

```bash
python scripts/ingest_feedback.py test_results.json -o reports/
# 输出: lessons_learned.md — 失败分类、根因分析、知识库更新建议
```

**失败分类：** `environment`(502/503/504), `data`(404/duplicate), `code`(500/traceback), `test_design`(AssertionError/400), `unknown`

**去重：** `MD5(path + expected_status + actual_status + error[:50])` → 同一指纹只计1个根因。

---

## 完整闭环工作流

```bash
# Step 1: 探测环境
python scripts/probe_env.py spec.md --filter-spec -o spec_available.md

# Step 2: 生成脚本
python scripts/generate_pytest.py spec_available.md -o test.py

# Step 3: 执行测试
pytest test.py -v --tb=short --html=reports/test_report.html

# Step 4: 反馈分析
python scripts/ingest_feedback.py test_results.json -o reports/

# Step 5: 更新知识库
# → error_messages_catalog.md / consolidated_domain_knowledge.md
```

## 环境变量

```bash
export TEST_USERNAME=admin
export TEST_PASSWORD=metas2660
export API_TOKEN=           # 直接 Token（跳过登录）
```
