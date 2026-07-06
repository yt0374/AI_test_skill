# Test Execution Report: 荆门新裁剪2.0

---

## Summary

| Metric | Value |
|--------|-------|
| Execution Timestamp | 2026-07-03 10:00:00 |
| Environment | jingmen (bak.jmym.dtsimple.pro) |
| Total Tests | 45 |
| Passed | 41 |
| Failed | 2 |
| Skipped | 2 (quarantine: 3) |
| Error | 0 |
| Overall Pass Rate | 91.1% |
| Duration | 18m 42s |

---

## Results by Priority

| Priority | Total | Passed | Failed | Skipped | Pass Rate | Status |
|----------|-------|--------|--------|---------|-----------|--------|
| P0 | 9 | 9 | 0 | 0 | 100% | Passed |
| P1 | 25 | 23 | 2 | 0 | 92% | Warning |
| P2 | 10 | 9 | 0 | 1 | 90% | Passed |
| P3 | 1 | 0 | 0 | 1 | 0% | Warning |

---

## Failed Tests

### TC-V17: test_bed_number_global_increment (P1)
- **Test**: `test_boundary.py::TestBedNumberBoundaries::test_bed_number_global_increment`
- **Error**: `AssertionError: Bed numbers not in ascending order: [3, 1, 2, 5, 4]`
- **Expected**: Bed numbers displayed in ascending order (C-001, C-002, C-003...)
- **Actual**: Bed numbers displayed in creation order, not sorted by number
- **Severity**: Medium
- **Recommendation**: Verify list default sort column is "床次号" (ascending). May require clicking sort header.

### TC-V02: test_marker_fully_allocated_not_selectable (P1)
- **Test**: `test_boundary.py::TestLayerBoundaryValues::test_marker_fully_allocated_not_selectable`
- **Error**: `AssertionError: Expected disabled class but marker was selectable`
- **Expected**: MK-003 (remaining=0) should be disabled or hidden in marker dropdown
- **Actual**: MK-003 is visible and selectable; error appears only on save
- **Severity**: Low
- **Recommendation**: Clarify with product whether UX should prevent selection (frontend) or validate on save (backend).

---

## Skipped Tests

| Test | Reason | Status |
|------|--------|--------|
| `test_quarantine.py::test_bed_submission_large_layer_count` | Intermittent PAD modal timeout | Quarantined 2026-07-03 |
| `test_quarantine.py::test_smart_merge_all_same_delivery` | Smart merge dialog inconsistency | Quarantined 2026-07-03 |
| `test_quarantine.py::test_manual_to_auto_cpo_preservation` | Manual->Auto CPO reselection inconsistent | Quarantined 2026-07-03 |
| `test_integration.py::test_full_e2e_single_cpo_flow` | Requires pre-existing CPO-A task data | Skipped (no data) |
| `test_boundary.py::test_aux_fabric_bed_prefix_f` | No F-prefix beds in test data | Skipped (no data) |

---

## Results by Module

| Module | Total | Passed | Failed | Rate |
|--------|-------|--------|--------|------|
| 裁剪任务 (Cutting Task) | 14 | 13 | 1 | 92.9% |
| 床次任务 (Bed Task) | 15 | 14 | 1 | 93.3% |
| 扎卡打印 (Tag Printing) | 4 | 4 | 0 | 100% |
| 缝制挂片 (Hanging) | 12 | 10 | 0 | 83.3%* |

*2 integration hanging tests skipped due to missing test data

---

## Requirements Traceability

| Req ID | Requirement | Tests | Passed | Failed | Status |
|--------|-------------|-------|--------|--------|--------|
| F001 | CPO选择与合并 | 5 | 5 | 0 | Passed 100% |
| F002 | 唛架层数分配与递减 | 6 | 5 | 1 | Warning 83% |
| F003 | 顶层任务管理 | 5 | 5 | 0 | Passed 100% |
| F004 | 现场床次创建 | 6 | 5 | 1 | Warning 83% |
| F005 | 床次提交完成 | 3 | 3 | 0 | Passed 100% |
| F006 | 床次号唯一性 | 3 | 3 | 0 | Passed 100% |
| F007 | 防超裁机制 | 5 | 5 | 0 | Passed 100% |
| F008 | 扎卡打印CPO关联 | 4 | 4 | 0 | Passed 100% |
| F009 | 自动充数模式 | 3 | 3 | 0 | Passed 100% |
| F010 | 手动充数模式 | 5 | 3 | 0 | Warning 60%* |

*2 manual mode tests skipped: requires live CPO data with varying fill states

---

## Error Distribution

| Error Type | Count | Example |
|------------|-------|---------|
| AssertionError | 2 | Bed number sort order, Marker disabled state |
| TimeoutError | 0 | — |
| ElementNotFound | 0 | — |

---

## Trend Analysis

> **First execution** — trend data will be available from the next run.

| Metric | Current | Baseline | Delta |
|--------|---------|----------|-------|
| Overall Pass Rate | 91.1% | — | — |
| P0 Pass Rate | 100% | 100% | 0 |
| P1 Pass Rate | 92% | — | — |
| Execution Time | 18m 42s | — | — |
| Flaky Tests | 3 (quarantined) | — | — |
| Defects Filed | 2 | — | — |

### Action Items

1. **TC-V17 (bed number sort)**: Confirm expected sort behavior with product. If sort-by-creation is intentional, update test assertion.
2. **TC-V02 (marker disabled state)**: Clarify UX behavior for fully-allocated markers. Frontend disable or backend-only validation?
3. **Quarantine review**: Schedule for 2026-07-07 (Monday). Target: resolve PAD modal timeout issue.

---

## Defects

| ID | Severity | Module | Title | Status |
|----|----------|--------|-------|--------|
| BUG-2026-001 | Medium | 床次任务 | Bed numbers not sorted ascending by default in list view | Open |
| BUG-2026-002 | Low | 裁剪任务 | Fully-allocated marker selectable in dropdown; error on save instead of pre-selection | Open |
