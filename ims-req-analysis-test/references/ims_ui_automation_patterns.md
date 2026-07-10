# IMS UI 自动化实战经验 (2026-07-09)

> 来源：考勤模块全流程自动化实战，覆盖 7 个页面、38 条自动化用例。

---

## 1. Ant Design 表格数据提取

### 问题：数据提取始终返回 0 条

**根因**：两个 bug 叠加导致静默失败。

```python
# ❌ 错误写法
rows = page.locator(".ant-table-tbody tr")           # Bug 1: 匹配了空状态行
headers = page.locator(".ant-table-thead th").all_inner_texts()
for row in rows:
    cells = row.locator("td").all_inner_texts()
    if len(cells) == len(headers):                    # Bug 2: 永远 False
        results.append(dict(zip(headers, cells)))
```

**Bug 1 — 行选择器**：Ant Design 表格中 `tr` 包括空状态提示行和展开行，必须用 `tr.ant-table-row` 只取数据行。

**Bug 2 — 列偏移**：每行 td 比 th 多一列（选择框），`len(cells) == len(headers)` 永远不成立，**所有行静默丢弃**。

```python
# ✅ 正确写法
rows = page.locator(".ant-table-tbody tr.ant-table-row")
offset = len(cells) - len(headers)
if offset > 0:
    cells = cells[offset:]  # 跳过选择列
```

### 按钮匹配

```python
# ❌ 错误：.ant-btn-primary 可能在弹窗中先匹配到弹窗按钮
page.locator("button:has-text('查询'), .ant-btn-primary").first.click()

# ✅ 正确：遍历可见按钮，匹配文本
for btn in page.locator("button:visible").all():
    if "查" in btn.inner_text() and "询" in btn.inner_text():
        btn.click(); break
```

---

## 2. IMS DatePicker（只读输入框）

IMS 使用 Ant Design DatePicker，`<input>` 带 `readonly` 属性。

```python
# ❌ 错误：fill() 超时报 "element is not editable"
date_input.fill("2026-07-09")

# ✅ 方案 1：force=True 绕过只读检查
date_input.fill("2026-07-09", force=True)

# ✅ 方案 2：用日历 UI 选择日期（更可靠）
picker.click()  # 打开日历面板
for cell in page.locator(".ant-picker-cell-inner").all():
    if cell.inner_text() == "8":
        cell.click(); break
```

**日期格式**：IMS UI 显示 `2026/07/09`（斜杠），API 查询两者均兼容。

---

## 3. IMS Excel 导入

### 模板列映射（反直觉）

| IMS 模板列 | 应填内容 | 直觉预期 |
|-----------|---------|---------|
| Name | **工号** | 姓名 |
| Ac-No | **姓名** | 工号 |
| sTime | 考勤时间 `yyyy-MM-dd HH:mm:ss` | ✅ 正确 |
| Machine | 设备号或留空 | ✅ 正确 |

### 导入交互链

```
点击 "excel导入" → 弹窗打开
  → 点击 "选择文件" → 用 file_chooser 选文件
    → 等待预览解析（检查无"错误"字样）
      → 轮询 "确认导入" 按钮启用（`is-disabled` class 消失）
        → 自然点击（不用 force=True）
```

### 去重检查

```python
# 导入前查询考勤登记，已有数据则跳过
page.goto(DETAIL_URL); click_button("查 询")
if page.locator(".ant-table-tbody tr.ant-table-row").count() > 0:
    print("Skip — data exists"); return
```

---

## 4. 日考勤计算

### 交互链

```
点击 "日考勤计算" → 弹窗打开
  → 日期默认已填当天（通常正确，无需修改）
  → 如需修改：fill(value, force=True)（只读 input）
  → 点击 "确认"
    → 轮询 body 全文中的 "任务完成"（非仅 modal-body）
      → 点击 .ant-modal-close 关闭弹窗
```

### 任务完成轮询

```python
# ❌ 错误：只查 modal-body
page.locator(".ant-modal-body").inner_text()

# ✅ 正确：查整个 body（进度提示可能在 modal 外）
for attempt in range(90):
    page.wait_for_timeout(2000)
    if "任务完成" in page.locator("body").inner_text():
        break
```

---

## 5. 员工数据提取

### 员工档案表结构

IMS 员工档案表有 61+ 列，必须按表头关键字定位：

```python
headers = page.locator(".ant-table-thead th").all_inner_texts()
id_col = next(i for i,h in enumerate(headers) if "工号" in h) + 1    # +1 跳过选择列
name_col = next(i for i,h in enumerate(headers) if "姓名" in h) + 1
status_col = next(i for i,h in enumerate(headers) if "状态" in h) + 1

# 按 td 逐个单元格提取
cells = row.locator("td")
emp_id = cells.nth(id_col).inner_text().strip()
name = cells.nth(name_col).inner_text().strip()
```

**注意**：`all_inner_texts()` 按空格分词会导致复杂表格索引错位，必须用逐列 `locator("td")` 访问。

### 环境隔离

不同环境员工数据不同，必须按环境分别存储：
```
extracted_data/
├── employees_sit.json
├── employees_uat.json
├── employees_jingmen.json
└── daily_stats_sit.json
```

---

## 6. IMS SPA 路由

IMS 是 Vue 3 SPA，使用 hash 路由。考勤模块 URL：

| 页面 | Hash URL |
|------|------|
| 考勤登记 | `/#/personnel/workAttendance/detail` |
| 回工登记 | `/#/personnel/workAttendance/returningWork` |
| 请假登记 | `/#/personnel/workAttendance/leave` |
| 日考勤统计 | `/#/personnel/workAttendance/dailyReportNew` |
| 月考勤统计 | `/#/personnel/workAttendance/monthlyReport` |
| 小组出勤表 | `/#/personnel/workAttendance/teamAttendanceReport` |
| 员工缺勤表 | `/#/personnel/workAttendance/employeeAbsenceReport` |
| 员工档案 | `/#/personnel/staffManagement/staffFile` |

**注意**：直接构造 hash URL 导航不需要侧边栏交互，比点击侧边栏可靠得多。

---

## 7. IMS API 模式

| API | 用途 |
|-----|------|
| `POST /api/ims-auth/auth/login` | 登录（密码需 MD5） |
| `POST /api/ims-auth/attendance/item/page` | 考勤登记查询 |
| `POST /api/ims-auth/attendance/item/import` | 考勤导入（两步式） |
| `POST /api/ims-auth/attendance/leave/page` | 请假登记查询 |
| `POST /api/low-code/dataTypeClassification/commonPullDownList` | 通用下拉数据 |

**登录密码**：IMS 要求 MD5 哈希：`hashlib.md5(password.encode()).hexdigest()`

**Token 位置**：`response["data"]["token"]`（非 `result.token`）

---

## 8. 数据驱动测试架构

```python
# conftest.py — 数据集缓存 + 分类 fixtures
_dataset_cache = None  # 模块级缓存，一次提取所有测试复用

@pytest.fixture
def test_dataset(logged_in_page):
    global _dataset_cache
    if _dataset_cache is None:
        _dataset_cache = extract_and_build(logged_in_page)
    return _dataset_cache

@pytest.fixture
def normal_employee(test_dataset):
    emp = test_dataset["samples"].get("normal_employee")
    if emp: return emp
    pytest.skip("No normal employee data")  # 优雅降级
```

**分类维度**：
- `normal_employee` — 考勤异常=正常 且 迟到=0
- `late_employee` — 迟到 > 0
- `absent_employee` — 考勤异常 = 没上班
- `missing_card_employee` — 考勤异常 = 缺卡
- `by_shift` — 按班次分组
