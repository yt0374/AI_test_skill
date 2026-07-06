# generate_pytest.py

**api_pytest Spec → pytest 代码生成器**

将 YAML frontmatter 格式的 API 测试 Spec 编译为可直接执行的 pytest 脚本。

## 快速开始

```bash
# 1. 编写 Spec（参考 接口自动化测试用例验收标准.md）
# 2. 生成 pytest 脚本
python scripts/generate_pytest.py <spec.md> --output <test_file.py>

# 3. 验证生成结果
pytest <test_file.py> --collect-only -q

# 4. 执行测试
pytest <test_file.py> -v --tb=short
```

## Spec 格式要求

```yaml
---
kind: api_pytest                          # 必填，固定值
base_url: http://test.example.com/api     # 必填，API 基础地址
timeout_default: 30                       # 可选，默认 30s
auth:                                     # 可选，Bearer 登录
  type: bearer_login
  login_path: /auth/login
  username_field: username
  password_field: password
  username_env: TEST_USERNAME
  password_env: TEST_PASSWORD
  token_json_path: token

cases:                                    # cases[] 与 scenarios[] 至少其一
  - id: TC-XXX-001                        # 必填，全表唯一
    name: "用例名称"                       # 可选
    method: GET|POST|PUT|DELETE            # 必填
    path: /api/xxx                         # 必填，以 / 开头
    expect_status: 200                     # 必填
    json_body: {field: value}              # 可选，请求体
    query: {key: value}                    # 可选，URL 参数
    no_auth: true                          # 可选，跳过认证
    extract_vars:                          # 可选，提取响应字段到变量池
      var_name: $.json.path
    depends_on: [TC-XXX-001]               # 可选，上游依赖
    data_source: data/xxx.csv              # 可选，CSV 参数化
    expect_json_subset: {field: value}     # 可选，JSON 字段断言
    expect_body_substrings: ["子串"]       # 可选，响应体包含检查
    timeout: 30                            # 可选，单 case 超时

scenarios:                                 # 多步场景
  - name: "场景名"                          # 必填
    steps:
      - method: POST
        path: /api/xxx
        json_body: {...}
        expect_status: 201
        capture:                           # 步间传值
          var_name: $.json.path
      - method: GET
        path: /api/xxx/{var_name}
        expect_status: 200
---
```

## 占位符

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `{{timestamp}}` | 秒级时间戳 | `"PO-{{timestamp}}"` → `"PO-1751428800"` |
| `{{uuid}}` | UUID4 前 8 位 | `"CODE-{{uuid}}"` → `"CODE-a1b2c3d4"` |
| `${变量名}` | 变量池引用 | `"${synced_code}"` → 由 extract_vars/capture 产出 |

## 支持的断言

| 断言类型 | Spec 字段 | 生成效果 |
|----------|----------|---------|
| 状态码 | `expect_status: 200` | `assert r.status_code == 200` |
| JSON 字段值 | `expect_json_subset: {status: "成功"}` | `assert data["status"] == "成功"` |
| 响应体子串 | `expect_body_substrings: ["carrierCode"]` | `assert "carrierCode" in r.text` |
| 响应时间 | `expect_response_time_ms: 3000` | 未自动生成，需手动添加 |

## 依赖链机制

```
TC-SYNC-001 (extract: synced_code)
  ↓ depends_on
TC-BIND-001 (use: ${synced_code}, extract: bound_carrier)
  ↓ depends_on  
TC-INB-001 (use: ${bound_carrier})
```

上游失败时下游自动 `pytest.skip()`，不产生级联误报。

## 环境变量

```bash
# .env 或 CI 变量
export TEST_USERNAME=admin
export TEST_PASSWORD=metas2660
export API_TOKEN=           # 直接 Token（跳过登录）
```

## 验证命令

```bash
# Spec 语法检查
python -c "import yaml; yaml.safe_load(open('spec.md').read().split('---')[1])"

# 生成 + 采集
python scripts/generate_pytest.py spec.md -o test.py && pytest test.py --collect-only -q

# 完整验收流程
python scripts/generate_pytest.py spec.md -o test.py
pytest test.py --collect-only -q     # Step 1: 验证可采集
pytest test.py -v --tb=short         # Step 2: 执行
pytest test.py --html=reports/api_report.html  # Step 3: 报告
```

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `SyntaxError: invalid syntax` | Spec 格式错误或路径含特殊字符 | 检查 YAML 缩进，路径使用 `/` |
| `NameError: name '_load_csv' is not defined` | 旧版生成器 bug | 更新到最新 `generate_pytest.py` |
| `collected 0 items` | 生成文件有语法错误 | `python -c "import ast; ast.parse(open('test.py').read())"` |
| `401 Unauthorized` | Token 未获取或环境变量未设 | 检查 `TEST_USERNAME`/`TEST_PASSWORD` |
