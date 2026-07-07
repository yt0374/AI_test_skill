# generate_test_data.py

**智能测试数据生成器 — 从需求文档自动生成边界值数据集**

读取 requirements_spec.md，提取数值约束和枚举定义，自动生成 pytest parametrize 可用的 JSON 数据集。

## 快速使用

```bash
python scripts/generate_test_data.py requirements_spec.md -o test_data.json
python scripts/generate_test_data.py requirements_spec.md --pairwise -o test_data_reduced.json
```

## 自动识别

| 约束模式 | 生成策略 | 示例 |
|---------|------|------|
| `X > N` | N-1(拒绝), N(拒绝), N+1(通过) | "金额>10000" |
| `X ≥ N` | N-1(拒绝), N(通过), N+1(通过) | "数量≥1" |
| `X < N` | N-1(通过), N(拒绝), N+1(拒绝) | "天数<30" |
| `X ≤ N` | N-1(通过), N(通过), N+1(拒绝) | "字符≤50" |
| `N~M 范围` | N-1/N/N+1/M-1/M/M+1 | "1~100字符" |
| `最多N次` | N-1(通过), N(通过), N+1(拒绝) | "最多3次" |

## 生成示例

```json
{
  "boundary_订单金额": {
    "description": "Boundary trio for 订单金额 (gt)",
    "dataset": [
      {"value": 9999, "expected": "reject"},
      {"value": 10000, "expected": "reject"},
      {"value": 10001, "expected": "pass"}
    ]
  }
}
```

## 工作流

```bash
# 1. Skill 生成 requirements_spec.md
# 2. 自动提取约束
python scripts/generate_test_data.py requirements_spec.md -o test_data.json
# 3. pytest 消费
# test_data.json → load_dataset() → @pytest.mark.parametrize
```
