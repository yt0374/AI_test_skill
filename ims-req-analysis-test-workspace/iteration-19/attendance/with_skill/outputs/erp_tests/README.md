# IMS Attendance (考勤) Module - Playwright E2E Tests

## Overview

End-to-end UI tests for the IMS Enterprise Resource Planning attendance (考勤) module, built with Playwright (Python sync API) and pytest.

**Environment:** SIT (`http://test.fj.dtsimple.pro`)
**Enterprise:** 最佳智造
**Module:** 人事 > 考勤

## Project Structure

```
erp_tests/
  conftest.py              # Browser fixtures, login, data loading
  test_smoke.py            # P0 smoke tests (navigation, page load, key CRUD)
  test_functional.py       # P1 functional tests (data-driven, lifecycle, search)
  test_boundary.py         # P2 boundary tests (edge cases, validation, state gates)
  test_integration.py      # P3 integration tests (cross-page flows, consistency)
  test_quarantine.py       # Quarantined flaky tests (skipped)
  pages/
    base_page.py           # Page Object Model base class
  utils/
    test_data_loader.py    # CSV/JSON data loader utilities
    test_data.py           # Static test data constants
  test_data/
    test_data.csv          # Test data (12 scenarios)
  README.md                # This file
```

## 7 Sub-Pages Under Test

| # | Sub-Page | Chinese | Description |
|---|----------|---------|-------------|
| 1 | 考勤登记 | Attendance Register | CRUD, import, replenish card |
| 2 | 回工登记 | Return-to-Work Register | Draft/effective lifecycle |
| 3 | 请假登记 | Leave Register | Draft/effective lifecycle, day-leave generation |
| 4 | 日考勤统计 | Daily Attendance Stats | Calculation engine, quick/batch replenish, sync |
| 5 | 月考勤统计 | Monthly Attendance Stats | Version management, detail, export |
| 6 | 小组出勤表 | Group Attendance Report | Group-level attendance summary |
| 7 | 员工缺勤表 | Employee Absence Report | Employee-level absence summary |

## Prerequisites

- Python 3.10+
- Playwright for Python

## Setup

### 1. Install Dependencies

```bash
pip install pytest pytest-playwright playwright
```

### 2. Install Playwright Browsers

```bash
playwright install chromium
```

### 3. Verify Test Data

Ensure `test_data/test_data.csv` is present with valid test scenarios.

## Running Tests

### Run All Tests

```bash
cd erp_tests
pytest -v --headed
```

### Run by Priority

```bash
# P0 smoke tests only (fast, must-pass)
pytest -v -m p0

# P1 functional tests
pytest -v -m p1

# P2 boundary tests
pytest -v -m p2

# P3 integration tests
pytest -v -m p3

# Exclude quarantine tests (on by default)
pytest -v -m "not quarantine"
```

### Run by Test File

```bash
pytest -v test_smoke.py
pytest -v test_functional.py
pytest -v test_boundary.py
pytest -v test_integration.py
```

### Run Specific Test

```bash
pytest -v test_smoke.py::TestAttendanceNavigation::test_navigate_to_subpage
```

### Useful Options

```bash
# Headless mode (CI)
pytest -v --headed=false

# Slow down for debugging
pytest -v --slowmo 500

# Parallel execution (requires pytest-xdist)
pytest -v -n 2

# Generate HTML report (requires pytest-html)
pytest -v --html=report.html
```

## Markers

| Marker | Priority | Description |
|--------|----------|-------------|
| `p0` | Smoke | Core path - must pass every build |
| `p1` | Functional | Key business flows, CRUD, search |
| `p2` | Boundary | Edge cases, validation, state gates |
| `p3` | Integration | Cross-page flows, consistency |
| `quarantine` | Skip | Known flaky tests, reviewed weekly |

## Test Data

`test_data/test_data.csv` contains 12 test scenarios covering:

- Normal attendance (D01-1)
- Late arrival (D01-2)
- Missing card (D01-3)
- No-show (D01-4)
- Return-to-work (D01-5)
- Annual leave (D01-6)
- Overtime (D01-7)
- Weekend overtime (D01-8)
- Pregnancy employee (D01-9)
- Nursing employee (D01-10)
- Overtime rounding 1.15H (D01-11)
- Overtime rounding 1.85H (D01-12)

## Login Flow

The SIT environment requires:
1. Navigate to `http://test.fj.dtsimple.pro`
2. Enter username/password (admin/admin123)
3. Select enterprise `最佳智造` from the enterprise list
4. Wait for dashboard

The `login` fixture in `conftest.py` handles this automatically.

## Navigation

Tests navigate via the sidebar module system:
1. Click `人事` in the main sidebar
2. Click the sub-page in the `.third-menu` panel

Helper functions `navigate_to_attendance()` and `BasePage.navigate_to_attendance()` are available.

## Page Object Model

`BasePage` provides:
- Navigation helpers (navigate_to_module, click_third_menu)
- Search/filter operations (click_search, fill_field, select_dropdown)
- CRUD operations (click_add, click_save, click_delete)
- Assertions (expect_success_toast, expect_table_has_rows)
- Modal helpers (confirm_dialog, expect_modal_visible)

## Contributing

When adding new tests:
1. Assign the correct priority marker (p0/p1/p2/p3)
2. Use `BasePage` methods for interactions
3. Use `expect()` for assertions (not raw `assert`)
4. Use `@pytest.mark.parametrize` for data-driven tests
5. Handle optional UI elements gracefully (check `.count()` before interacting)
