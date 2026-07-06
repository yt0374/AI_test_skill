# Jingmen Cutting System 2.0 - Automated Test Suite

> Playwright + pytest 自动化测试项目
> 模块：荆门鹰美裁剪系统（裁剪任务/床次拉布/扎卡打印/缝制挂片）
> 环境：bak.jmym.dtsimple.pro

---

## Environment Setup

### Prerequisites

- Python 3.10+
- Node.js 18+ (for Playwright browsers)

### Dependencies Installation

```bash
pip install pytest pytest-playwright pytest-rerunfailures pytest-html
playwright install chromium
```

### Environment Configuration

| 配置项 | 值 |
|--------|-----|
| URL | http://bak.jmym.dtsimple.pro |
| Username | admin |
| Password | ym5579 |
| Browser | Chromium (headless by default) |
| Enterprise Selector | None (Jingmen has direct login) |

## Project Structure

```
erp_tests/
├── conftest.py              # Fixtures: browser, login, data loading
├── test_smoke.py            # P0 smoke tests (9 cases)
├── test_functional.py       # P1 functional tests (32 cases)
├── test_boundary.py         # P2 boundary tests (29 cases)
├── test_integration.py      # P3 integration tests (6 cases)
├── test_quarantine.py       # Quarantined flaky tests
├── pages/
│   └── base_page.py         # Page Object Model helpers
├── utils/
│   ├── test_data_loader.py  # CSV/JSON data loading
│   └── test_data.py         # Static test data constants
└── test_data/
    └── api_payloads.json    # API test payloads (placeholder)
```

## Execution Modes

| Mode | Command (bash) | Command (PowerShell) | Tests |
|------|---------------|---------------------|-------|
| Smoke | `./run_tests.sh smoke` | `.\run_tests.ps1 smoke` | P0 only (9 cases) |
| Functional | `./run_tests.sh functional` | `.\run_tests.ps1 functional` | P0 + P1 (41 cases) |
| Full | `./run_tests.sh full` | `.\run_tests.ps1 full` | P0 + P1 + P2 (70 cases) |
| Integration | `./run_tests.sh integration` | `.\run_tests.ps1 integration` | P3 only (6 cases) |
| Complete | `./run_tests.sh complete` | `.\run_tests.ps1 complete` | All tests |
| Quarantine | `./run_tests.sh quarantine` | `.\run_tests.ps1 quarantine` | Quarantined only |

### Direct pytest Commands

```bash
# Run all tests
pytest -v --tb=short

# Run by marker
pytest -m p0 -v
pytest -m "p0 or p1" -v
pytest -m p2 -v

# Run specific file
pytest test_smoke.py -v
pytest test_boundary.py -v

# Run with headed browser (see the test running)
pytest --headed -v

# Run with slow motion (debug)
pytest --headed --slowmo=1000 -v
```

## Test Case Summary

| Priority | Count | File | Description |
|----------|-------|------|-------------|
| P0 | 9 | test_smoke.py | Core smoke: login, create task, create bed, ticket print, auto fill |
| P1 | 32 | test_functional.py | Main flows: CPO selection, editing, deletion, submission, mode switch |
| P2 | 29 | test_boundary.py | Edge cases: layer boundaries, state guards, validation, concurrency |
| P3 | 6 | test_integration.py | E2E: full single/merge CPO flow, overcut flow, cross-device consistency |
| Quarantine | 0 | test_quarantine.py | Flaky tests (initially empty, populated during execution) |

## Flaky Test Strategy

### Retry Rules

- All tests: max 2 retries with 5-second delay (`--reruns 2 --reruns-delay 5`)
- Integration tests: max 1 retry with 10-second delay
- Quarantined tests: no retries

### Identification Criteria

A test is marked as flaky when:
1. It fails in 3+ consecutive CI/CD runs with the same error
2. It passes when re-run individually
3. Root cause is environmental (network timing, async race conditions, animation timing)

### Quarantine Process

1. Move the flaky test to `test_quarantine.py`
2. Add `@pytest.mark.skip(reason="QUAR-XXX: ...")` with a bug ticket reference
3. Create a bug ticket in the issue tracker
4. Investigate root cause within 1 sprint
5. Fix the root cause OR add explicit wait/timeout handling

### Weekly Review

- Every Friday: review quarantined tests
- If fix is deployed: remove `@pytest.mark.skip`, move test back to original file
- If still flaky after 2 sprints: re-evaluate test value vs maintenance cost
- Maximum quarantine duration: 4 weeks (after which test is removed or permanently skipped)

## Prerequisites for Test Execution

Before running tests, ensure the Jingmen environment has:

1. **Valid production orders** with CPO numbers configured
2. **At least one marker (唛架)** with configured total plan layers
3. **At least one user account** with:
   - PC端: admin role for task creation/approval (admin / ym5579)
   - PAD端: operator role for bed creation (to be confirmed)

## Known Limitations

1. Exact CSS selectors may need adjustment after first run against the actual Jingmen UI
2. PAD-specific workflows use PC browser simulation (PAD-specific selectors to be added)
3. CPO data is simulated - real CPO numbers from the production system should be used
4. Concurrent test (N-01) uses simplified single-browser approach instead of true multi-session concurrency
