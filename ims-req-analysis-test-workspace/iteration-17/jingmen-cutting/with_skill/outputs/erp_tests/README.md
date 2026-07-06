# Jingmen Cutting 2.0 — E2E Test Suite

Automated Playwright + pytest test suite for the Jingmen Eagle Beauty (荆门鹰美) Cutting Module 2.0 overhaul.

## Environment

| Item | Value |
|------|-------|
| Customer | 荆门鹰美 |
| URL | `http://bak.jmym.dtsimple.pro` |
| Credentials | `admin` / `ym5579` |
| Login | Direct (no enterprise selector) |
| Modules | 生产 (Cutting Tasks, Bed Tasks, Tag Printing), 吊挂 (Hanging) |

## Prerequisites

```bash
# Python 3.10+
pip install pytest pytest-playwright pytest-json-report pytest-rerunfailures pytest-html
playwright install chromium
```

## Quick Start

```bash
# Smoke test (P0 only, ~2 min)
./run_tests.sh smoke

# Daily regression (P0+P1, ~8 min)
./run_tests.sh functional

# Pre-release validation (P0+P1+P2, ~15 min)
./run_tests.sh full

# Integration tests (P3, ~5 min)
./run_tests.sh integration

# Complete suite (~20 min)
./run_tests.sh all
```

Windows PowerShell:
```powershell
.\run_tests.ps1 smoke
.\run_tests.ps1 functional
```

## Project Structure

```
erp_tests/
├── conftest.py              # Fixtures: browser, login, data loading
├── test_smoke.py            # P0 tests (9 cases)
├── test_functional.py       # P1 parametrized tests (25 cases)
├── test_boundary.py         # P2 boundary tests (10 cases)
├── test_integration.py      # P3 cross-module tests (3 cases)
├── test_quarantine.py       # Quarantined flaky tests
├── pages/
│   └── base_page.py         # Page Object Model
├── utils/
│   ├── test_data_loader.py  # CSV/JSON loading utilities
│   └── test_data.py         # Static constants
└── test_data/               # External CSV datasets
```

## Test Priority Distribution

| Priority | Count | % | Description |
|----------|-------|---|-------------|
| P0 | 9 | 20% | Smoke: Core CPO selection, bed creation, tag printing, auto-fill |
| P1 | 25 | 56% | Functional: Full CRUD, status transitions, data-driven parametrize |
| P2 | 10 | 22% | Boundary: Input validation, state gates, anti-overcut, concurrency |
| P3 | 1 | 2% | Integration: Cross-module E2E, data consistency |
| Quarantine | 3 | — | Isolated flaky tests (skipped by default) |

## Test Data

Test data is driven by `test_data.csv` in the parent directory.
Key parameterized scenarios:

| Dataset | Scenario | Variations |
|---------|----------|------------|
| D01 | CPO Selection & Marker Allocation | Single, Multiple, Full, Over-allocation |
| D02 | Bed Creation | Normal, Boundary, Warning, Block |
| D03 | Bed Completion | Exact match, Under, Over-range |
| D04 | Hanging Auto-Fill | Generic tag order, Specific tag priority |
| D05 | Anti-Overcut | Warning threshold, Hard block, Approval |

## Page Object Model

`pages/base_page.py` provides shared UI patterns:
- `navigate_to_module(module_name)` — Sidebar navigation (Jingmen simple names)
- `click_third_menu(*items)` — Third-menu panel navigation
- `pad_scan_barcode(barcode)` — Simulate PAD barcode scan
- `pad_input_number(label, value)` — PAD numeric input
- `expect_success_toast()` / `expect_error_toast()` — Common assertions

## Custom Pytest Markers

```ini
@pytest.mark.p0          # Smoke tests
@pytest.mark.p1          # Functional tests
@pytest.mark.p2          # Boundary tests
@pytest.mark.p3          # Integration tests
@pytest.mark.flaky       # Known intermittent
@pytest.mark.quarantine  # Isolated (skipped)
```

## Flaky Test Strategy

### Retry Rules
- Default: 2 retries, 5-second delay (configured in `pytest.ini`)
- P0 tests: 3 retries (critical path must be reliable)
- P3 tests: 1 retry (integration tests are inherently slower)

### Identification
Tests are flagged as flaky when they:
1. Fail 3+ times in the last 10 CI runs with different failure modes
2. Pass locally consistently but fail in CI
3. Have timing-dependent assertions (PAD modal render delays)

### Quarantine Criteria
A test is moved to `test_quarantine.py` when:
1. Confirmed flaky by 2+ team members
2. Root cause identified but fix requires upstream change
3. @pytest.mark.skip added with date, reason, and failure pattern

### Weekly Review
- **Every Monday**: Review all quarantined tests
- Un-skip tests that have been fixed (run 10x consecutively, must pass 10/10)
- Remove quarantine for tests fixed >2 weeks ago
- File bugs for tests still quarantined after 4 weeks

## Running Specific Tests

```bash
# Single test file
pytest erp_tests/test_smoke.py -v

# Specific test class
pytest erp_tests/test_boundary.py::TestLayerBoundaryValues -v

# Specific test case
pytest erp_tests/test_smoke.py::TestCuttingTaskCreation::test_create_task_single_cpo -v

# Parametrize filter
pytest erp_tests/test_functional.py -k "marker" -v

# Skip quarantine
pytest erp_tests/ -m "not quarantine" -v
```

## Debugging

```bash
# Headed mode (see browser)
pytest erp_tests/ -m p0 --headed -v

# Slow-mo (500ms delay between actions)
pytest erp_tests/ -m p0 --headed --slowmo=500 -v

# Single test, show stdout
pytest erp_tests/test_smoke.py -v -s

# Break on failure (requires debugpy)
pytest erp_tests/ -m p0 --pdb
```
