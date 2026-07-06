#!/bin/bash
# =============================================================
# IMS ERP Test Execution Scripts
# Project: 荆门新裁剪需求2.0
# Environment: jingmen (bak.jmym.dtsimple.pro)
# =============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "  荆门新裁剪需求2.0 - Test Runner"
echo "  Environment: jingmen (bak.jmym.dtsimple.pro)"
echo "=========================================="

# Install dependencies (first run)
if [ ! -d "venv" ]; then
    echo "[SETUP] Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install pytest pytest-playwright pytest-rerunfailures pytest-json-report
    python -m playwright install chromium
else
    source venv/bin/activate
fi

# =============================================================
# Execution Modes
# =============================================================

run_smoke() {
    echo ""
    echo ">>> MODE: Smoke Tests (P0 only)"
    echo "    Use case: Quick pre-release check"
    echo ""
    pytest erp_tests/ -m p0 \
        --json-report --json-report-file=reports/pytest_results_smoke.json \
        -v --tb=short
}

run_functional() {
    echo ""
    echo ">>> MODE: Functional Regression (P0 + P1)"
    echo "    Use case: Daily regression"
    echo ""
    pytest erp_tests/ -m "p0 or p1" \
        --json-report --json-report-file=reports/pytest_results_functional.json \
        -v --tb=short
}

run_full() {
    echo ""
    echo ">>> MODE: Full Suite (P0 + P1 + P2)"
    echo "    Use case: Pre-release validation"
    echo ""
    pytest erp_tests/ -m "p0 or p1 or p2" \
        --json-report --json-report-file=reports/pytest_results_full.json \
        -v --tb=short
}

run_integration() {
    echo ""
    echo ">>> MODE: Integration Tests (P3)"
    echo "    Use case: Cross-module verification"
    echo ""
    pytest erp_tests/ -m p3 \
        --json-report --json-report-file=reports/pytest_results_integration.json \
        -v --tb=short
}

run_complete() {
    echo ""
    echo ">>> MODE: Complete Suite (All tests)"
    echo "    Use case: Full release validation"
    echo ""
    pytest erp_tests/ \
        --json-report --json-report-file=reports/pytest_results_complete.json \
        --junitxml=reports/junit.xml \
        -v --tb=short
}

run_by_environment() {
    echo ""
    echo ">>> MODE: SIT → Jingmen Environment Order"
    echo ""
    echo "--- Phase 1: SIT Environment (P0+P1) ---"
    pytest erp_tests/ -m "p0 or p1 and sit" \
        --json-report --json-report-file=reports/pytest_results_sit.json \
        -v --tb=short

    echo ""
    echo "--- Phase 2: Jingmen Environment (P0+P1+P2) ---"
    pytest erp_tests/ -m "p0 or p1 or p2 and jingmen" \
        --json-report --json-report-file=reports/pytest_results_jingmen.json \
        -v --tb=short
}

# =============================================================
# Report Generation
# =============================================================

generate_report() {
    echo ""
    echo ">>> Generating test report..."
    mkdir -p reports
    python3 -c "
import json, os
from datetime import datetime

# Aggregate results
results = {}
report_dir = 'reports'
for f in os.listdir(report_dir):
    if f.startswith('pytest_results_') and f.endswith('.json'):
        with open(os.path.join(report_dir, f)) as fp:
            data = json.load(fp)
            results[f.replace('pytest_results_','').replace('.json','')] = {
                'total': data.get('summary',{}).get('total',0),
                'passed': data.get('summary',{}).get('passed',0),
                'failed': data.get('summary',{}).get('failed',0),
            }

print(json.dumps(results, indent=2, ensure_ascii=False))
"
}

# =============================================================
# Main
# =============================================================

case "${1:-functional}" in
    smoke)
        run_smoke
        ;;
    functional)
        run_functional
        ;;
    full)
        run_full
        ;;
    integration)
        run_integration
        ;;
    complete)
        run_complete
        ;;
    env)
        run_by_environment
        ;;
    report)
        generate_report
        ;;
    *)
        echo "Usage: $0 {smoke|functional|full|integration|complete|env|report}"
        echo ""
        echo "Modes:"
        echo "  smoke        P0 only (quick pre-release check)"
        echo "  functional   P0+P1 (daily regression)"
        echo "  full         P0+P1+P2 (pre-release validation)"
        echo "  integration  P3 only (cross-module)"
        echo "  complete     All tests"
        echo "  env          SIT→Jingmen environment order"
        echo "  report       Generate aggregated report"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "  Test execution complete"
echo "=========================================="
