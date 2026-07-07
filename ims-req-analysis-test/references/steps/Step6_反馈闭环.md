# Step 6: 反馈闭环

> 承接 Step 5（test_results）| 产出：lessons_learned → 更新知识库

---

## 6.1 反馈流程

```bash
pytest → test_results.json
  ↓
python scripts/ingest_feedback.py test_results.json
  ↓
lessons_learned.md → 更新 error_messages_catalog.md
                  → 更新 consolidated_domain_knowledge.md
                  → 更新 SKILL.md（如发现模式问题）
```

## 6.2 失败分类

| 类别 | 特征 | 处理 |
|------|------|------|
| **environment** | Connection refused, 502/503, timeout | `probe_env.py` 验证环境 |
| **data** | 404, duplicate, unique constraint | 使用 {{timestamp}}/{{uuid}} 唯一化 |
| **code** | 500, NullPointer, traceback | 报告开发团队，附 payload |
| **test_design** | AssertionError, 400 | 校验断言与 API 文档一致性 |
| **unknown** | 无法自动判断 | 人工排查 |

## 6.3 自愈策略

| 故障类型 | 策略 | 最大重试 |
|------|------|:---:|
| 401 Unauthorized | 刷新 Token | 5次 |
| 500 Server Error | 指数退避+抖动 | 3次 |
| 429 Rate Limit | 指数退避+抖动 | 3次 |
| 请求超时 | 调整超时+10s | 2次 |
| 连接失败 | 指数退避+抖动 | 3次 |

> 400 参数错误不自愈（直接失败）。自愈成功的用例标记 healed，不上报缺陷。

## 6.4 去重机制

同一接口+状态码+错误信息前50字符 → 同一指纹 → 只生成1条缺陷记录。

```
指纹 = MD5(path + expected_status + actual_status + error[:50])
```

## 6.5 知识库更新清单

执行后逐项检查并更新：

- [ ] `error_messages_catalog.md` — 追加新发现的错误消息
- [ ] `consolidated_domain_knowledge.md` — 追加新发现的状态转换/业务规则
- [ ] `customer_variants.md` — 如发现新客户差异
- [ ] `page_field_dictionary.md` — 如捕获新页面字段
- [ ] `SKILL.md` — 如发现模式问题需调整流程
- [ ] `[INFERRED]` → `[VERIFIED]` — 验证推断消息

## 6.6 产出清单

| 文件 | → 流向 |
|------|:---:|
| `lessons_learned.md` | 反馈报告 |
| 更新知识库文件 | 下次迭代使用 |

---

# 附录：完整工具链

```
Step 0: 需求分类 ──→ (人工决策)
Step 1: 需求分析 ──→ (人工+Skill)
Step 2: 用例生成 ──→ (Skill)
Step 3: 自动化脚本 ──→ generate_pytest.py + Skill
Step 4: 测试执行 ──→ probe_env.py + pytest
Step 5: 测试报告 ──→ (Skill)
Step 6: 反馈闭环 ──→ ingest_feedback.py
```

| 工具 | 用途 | 阶段 |
|------|------|:---:|
| Skill (ims-req-analysis-test) | 核心生成引擎 | 1-5 |
| `probe_env.py` | 环境探测 | 执行前 |
| `generate_pytest.py` | Spec→pytest | Step 3 |
| `ims_login.py` | 环境登录 | Step 3-4 |
| `ingest_feedback.py` | 结果反馈 | Step 6 |
