# 荆门新裁剪需求2.0 - 完整测试方案

## 输出目录结构

```
outputs/
├── 01_requirements_analysis/
│   └── requirements_analysis.md          # 需求分析报告（系统架构、业务规则、风险评估）
├── 02_test_cases/
│   └── test_cases.md                     # 68个测试用例（P0-P3全覆盖）
├── 03_playwright_scripts/
│   ├── conftest.py                       # pytest配置和fixtures
│   ├── pytest.ini                        # pytest项目配置
│   └── test_jingmen_cutting.py           # Playwright自动化测试脚本
└── 04_test_reports/
    └── test_report.md                    # 测试报告模板（含结果追踪和缺陷管理）
```

## 快速开始

### 1. 安装依赖

```bash
pip install pytest playwright pytest-playwright pytest-html pytest-xdist
playwright install chromium
```

### 2. 配置测试环境

编辑 `test_jingmen_cutting.py` 中的全局变量：

```python
BASE_URL = "http://your-ims-server:port"
PC_USER = "your_pc_account"
PC_PASS = "your_password"
PAD_USER = "your_pad_account"
PAD_PASS = "your_password"
```

### 3. 运行测试

```bash
# 进入脚本目录
cd 03_playwright_scripts

# 运行全部测试
pytest test_jingmen_cutting.py -v

# 仅运行P0关键用例
pytest test_jingmen_cutting.py -v -k "P0"

# 运行指定模块
pytest test_jingmen_cutting.py -v -k "CuttingTask"

# 生成HTML报告
pytest test_jingmen_cutting.py -v --html=test_report.html --self-contained-html

# 并发执行加速
pytest test_jingmen_cutting.py -v -n auto
```

## 测试覆盖范围

| 模块 | 用例数 | P0 | P1 | P2 | P3 | 描述 |
|------|--------|-----|-----|-----|-----|------|
| 裁剪任务 | 16 | 6 | 6 | 3 | 1 | CPO选择/合并、唛架层数分配与递减 |
| 床次任务 | 16 | 6 | 5 | 3 | 2 | PAD创建床次、层数校验、状态流转 |
| 扎卡打印 | 8 | 2 | 4 | 1 | 1 | CPO关联规则、分扎计件 |
| 缝制挂片 | 16 | 5 | 6 | 3 | 2 | 自动/手动充数、模式切换 |
| 超裁审核 | 7 | 2 | 2 | 2 | 1 | 预警/强控、PC端审核 |
| 端到端 | 5 | 2 | 2 | 0 | 1 | 完整业务链路 |
| **合计** | **68** | **23** | **25** | **12** | **8** | |

## 核心测试场景

1. **唛架层数防超分配**：P0级，100层计划→分配40+50层→仅剩10层→超额禁止
2. **并发床次创建**：P1级，3小组同时创建→剩余层数实时校验→防超裁
3. **CPO智能合并**：P1级，同交期自动归组→确认后创建合并任务
4. **扎卡CPO显示规则**：P0级，合并CPO隐藏CPO信息→单一CPO显示CPO号
5. **挂片自动分配**：P0级，按交期自动选择CPO→满额自动切换
6. **超裁审核链路**：P0级，PAD触发→PC审核→放行/驳回
7. **完整端到端流程**：P0级，裁剪→拉布→扎卡→挂片全链路
