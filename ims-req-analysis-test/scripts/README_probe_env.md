# probe_env.py

**环境探测 — 执行前检测 API 可用性**

在生成测试脚本之前，探测目标环境确认哪些端点实际可用，避免全量 404 或环境不匹配导致的无效执行。

## 快速开始

```bash
# 1. 基础探测（使用 Spec 中的 base_url）
python scripts/probe_env.py spec.md

# 2. 指定不同的 base_url
python scripts/probe_env.py spec.md --base-url http://wms-server:8080/api

# 3. 探测 + 生成过滤后的 Spec（仅保留可用端点）
python scripts/probe_env.py spec.md --filter-spec -o spec_filtered.md
```

## 输出

| 文件 | 内容 |
|------|------|
| `*_env_report.md` | 兼容性报告：每端点状态、汇总统计、建议 |
| `*_filtered.md` | 过滤后 Spec，仅保留可执行端点（`--filter-spec` 时生成） |

## 端点分类

探测后将每个端点归入以下类别：

| 分类 | HTTP 状态 | 含义 | 处理建议 |
|------|----------|------|---------|
| `available` | 200+JSON | API 可用 | ✅ 可直接执行 |
| `auth_required` | 401/403 | 需要认证 | 配置 Token 后可测 |
| `not_found` | 404 | 路径不存在 | 更正 base_url 或路径前缀 |
| `method_not_allowed` | 405 | HTTP 方法不支持 | 检查接口文档的 method 定义 |
| `spa_page` | 200+HTML | 前端页面，非 API 后端 | API 可能在其他端口/域名 |
| `server_error` | 5xx | 服务端错误 | 检查目标环境健康状态 |
| `unreachable` | 0 | 网络不可达 | 检查 VPN/防火墙/代理 |

## 标准工作流

```bash
# 完整流程：探测 → 过滤 → 生成 → 执行
python scripts/probe_env.py spec.md --filter-spec -o spec_available.md
python scripts/generate_pytest.py spec_available.md -o test.py
pytest test.py -v --tb=short
```

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| 全部 `not_found` | base_url 错误或 API 路径前缀不对 | 用 `--base-url` 尝试不同地址，如加 `/gateway` 前缀 |
| 全部 `spa_page` | 探测的是前端服务器 | API 后端通常在另一个端口（如 8080）或子域名 |
| 全部 `unreachable` | 网络不通或 DNS 解析失败 | 检查 VPN/防火墙/代理设置，确认目标环境可 ping |
| GET 可用但 POST 返回 405 | NGINX 只允许 GET 到 SPA 路由 | 确认 API 网关地址，非前端地址 |
