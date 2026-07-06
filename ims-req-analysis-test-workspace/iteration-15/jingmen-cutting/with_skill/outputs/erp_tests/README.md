# 荆门新裁剪需求2.0 — Playwright 自动化测试项目

> Environment: 荆门鹰美 (jingmen) — bak.jmym.dtsimple.pro
> Framework: Playwright + pytest (Python)
> Generated: 2026-07-03

---

## Quick Start

```bash
# 1. Setup virtual environment
python -m venv venv
source venv/bin/activate  # or: .\venv\Scripts\Activate.ps1 (Windows)

# 2. Install dependencies
pip install pytest pytest-playwright pytest-rerunfailures pytest-json-report
python -m playwright install chromium

# 3. Run tests
./run_tests.sh smoke       # P0 smoke tests
./run_tests.sh functional  # P0+P1 daily regression
./run_tests.sh full        # P0+P1+P2 pre-release validation
./run_tests.sh env         # SIT→Jingmen environment order
```

## Project Structure

```
erp_tests/
├── conftest.py              # Fixtures: browser, login, test data loading
├── test_smoke.py            # P0: Core path verification (8 tests)
├── test_functional.py       # P1: Business flows with @pytest.mark.parametrize (29 tests)
├── test_boundary.py         # P2: Edge cases and validation (24 tests)
├── test_integration.py      # P3: Cross-module workflows (2 tests)
├── test_quarantine.py       # Quarantined flaky tests
├── pages/
│   └── base_page.py         # Page Object Model: BasePage, ProductionPage
├── utils/
│   ├── test_data_loader.py  # JSON/CSV data loading utilities
│   └── test_data.py         # Static test data constants
├── test_data/
│   └── test_data.json       # External test datasets
├── pytest.ini               # Pytest config (markers, retry, timeouts)
├── run_tests.sh             # Bash execution script
├── run_tests.ps1            # PowerShell execution script
└── README.md                # This file
```

## Test Environment Order

```
Phase 1: SIT (test.fj.dtsimple.pro)
  ├── P0+P1 基础流程验证
  └── 通过标准: 100% P0, >=95% P1

Phase 2: Jingmen (bak.jmym.dtsimple.pro)
  ├── P0+P1+P2 客户定制验证
  └── 通过标准: 100% P0+P1, >=90% P2
```

## Flaky Test Strategy

### Retry Configuration
- `--reruns 2`: Each failed test retried up to 2 times (3 total attempts)
- `--reruns-delay 5`: 5 seconds between retries
- Configured in `pytest.ini` addopts

### Identification
- Tests failing >30% of runs over 1 week → flagged for quarantine
- Monitor via CI dashboards and `pytest_results.json` trends

### Quarantine
- Move flaky tests to `test_quarantine.py`
- Add `@pytest.mark.skip(reason="...")` with investigation notes
- Track in weekly review

### Weekly Review
- Every Monday: review `test_quarantine.py`
- Fix and un-quarantine, or document known issue and keep skip

## Available Markers

| Marker | Description |
|--------|-------------|
| `@pytest.mark.p0` | Smoke tests — build blockers |
| `@pytest.mark.p1` | Functional tests — core flows |
| `@pytest.mark.p2` | Boundary tests — edge cases |
| `@pytest.mark.p3` | Integration tests — cross-module |
| `@pytest.mark.pc` | PC端 browser tests |
| `@pytest.mark.pad` | PAD端 tablet tests |
| `@pytest.mark.jingmen` | 荆门 environment specific |
| `@pytest.mark.sit` | SIT environment specific |

## Test Data

Test data is stored in `test_data/test_data.json`. Each dataset maps to specific
test IDs. The data is loaded via `conftest.py` fixtures and used with
`@pytest.mark.parametrize`.

### Key Datasets
- `cpo_selection`: CPO selection variants (C-01~C-03)
- `marker_layer_allocation`: Marker layer allocation (C-04, V-02~V-05)
- `bed_creation_anticut`: Bed creation & anti-overcut (C-07~C-09, V-08~V-11)
- `hanging_station`: Hanging station fill logic (V-19~V-24)
- `mode_switch`: Auto/manual mode switching (F-04~F-06)
- `task_status`: Task status transitions (U-01~U-03, X-01~X-02)

## Notes

- **Jingmen specifics**: No enterprise selector, direct login (admin/ym5579), `.third-menu` navigation
- **Missing modules**: 样衣, 销售, 人事, 物流 — tests scoped to 生产 only
- **PAD emulation**: Tests marked `@pytest.mark.pad` use 1024x768 viewport
- **Selectors**: Actual CSS selectors depend on UI implementation; adjust in `pages/base_page.py` after first run
