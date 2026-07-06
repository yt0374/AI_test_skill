# IMS 多环境管理方案

## 概述

IMS ERP 部署在多个环境中，每个环境有不同的配置、UI 结构和模块命名。
本方案通过 **环境配置文件** 统一管理差异，脚本和 Skill 自动适配。

## 环境配置结构

```
environments/
├── sit.json           # SIT 测试环境
├── xinji.json         # 新基(柬埔寨)客户环境
├── jingmen.json       # 荆门客户环境（待添加）
├── qianhong.json      # 千虹客户环境（待添加）
├── _template.json     # 新环境配置模板
└── README.md          # 本文档
```

## 已知差异矩阵

| 特性 | SIT (test.fj) | 新基 (xinji) | 荆门 | 千虹 |
|------|:---:|:---:|:---:|:---:|
| 模块命名 | `gm.销售#1` | `销售` | ? | ? |
| 子菜单类型 | `.third-menu` 面板 | 内容区卡片 | ? | ? |
| 物流/设备 | `物流` | `设备` | ? | ? |
| URL 格式 | 长路径 | 短路径 | ? | ? |
| 标题格式 | `gm.首页#2` | `首页` | ? | ? |
| 侧边栏默认 | 收起 | 展开? | ? | ? |
| **登录流程** | **用户名→密码→选择企业→登录** | **用户名→密码→登录** | ? | ? |
| 企业选择器 | 10个选项（最佳智造/安吉纳_测试/...） | 无 | ? | ? |

## 登录流程差异

### SIT (test.fj)
```
1. 输入用户名/密码
2. 点击企业选择器 (.ant-select) → 下拉列表出现
3. 选择企业（如 "最佳智造", "安吉纳_测试"）
4. 点击登录按钮
```

### xinji (bak.xinji)
```
1. 输入用户名/密码
2. 直接点击登录按钮
```

### 自动化登录

```python
from scripts.ims_login import login

# SIT — 自动选择企业
login(page, env_name="sit", enterprise="最佳智造")

# xinji — 直接登录
login(page, env_name="xinji")
```

## 使用方式

### 脚本指定环境

```bash
# probe_env.py — 支持 --env 参数
python scripts/probe_env.py spec.md --env sit
python scripts/probe_env.py spec.md --env xinji

# generate_pytest.py — 支持 --env 参数
python scripts/generate_pytest.py spec.md --env xinji -o test.py
```

### Skill 中指定环境

```
用户: "在新基环境上测试面料仓入库流程"
Skill: 自动加载 environments/xinji.json，使用该环境的 URL/选择器/模块名
```

### 添加新环境

1. 复制 `_template.json` → `{customer_name}.json`
2. 填写 URL、凭据
3. 运行探测脚本自动发现模块名和 UI 结构
4. 补充 URL patterns
5. 记录与 SIT 的差异

## 环境探测命令

```bash
# 自动发现模块名和 UI 结构
python scripts/probe_env.py --discover --env <env_name>
```
