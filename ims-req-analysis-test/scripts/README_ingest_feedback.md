# ingest_feedback.py

**测试反馈闭环 — 执行结果回灌知识库**

读取 `test_results.json`，分析失败模式，生成改进建议。

## 快速使用

```bash
# 执行测试后运行
python scripts/ingest_feedback.py test_results.json -o reports/

# 输出
#   lessons_learned.md  — 失败分类、根因分析、知识库更新建议
```

## 失败分类

| 类别 | 判定特征 | 处理 |
|------|---------|------|
| `environment` | Connection refused, 502/503/504, timeout | 检查目标服务，运行 probe_env.py |
| `data` | 404, duplicate, 冲突 | 使用 {{timestamp}}/{{uuid}} 唯一化数据 |
| `code` | 500, NullPointer, traceback | 报告开发团队，附带请求 payload |
| `test_design` | AssertionError, 400 | 校验断言与 API 文档一致性 |
| `unknown` | 无法自动分类 | 人工排查 |

## 去重机制

同一接口+状态码+错误信息 → 同一指纹 → 只计为 1 个根因，避免重复缺陷。

```
指纹 = MD5(path + expected_status + actual_status + error[:50])
```

## 标准工作流

```bash
# 完整闭环
python scripts/probe_env.py spec.md --filter-spec       # 1. 探测环境
python scripts/generate_pytest.py spec.md -o test.py     # 2. 生成脚本
pytest test.py -v --tb=short                            # 3. 执行测试
python scripts/ingest_feedback.py test_results.json     # 4. 反馈分析
# → 更新 error_messages_catalog.md                        5. 更新知识库
# → 更新 consolidated_domain_knowledge.md
```
