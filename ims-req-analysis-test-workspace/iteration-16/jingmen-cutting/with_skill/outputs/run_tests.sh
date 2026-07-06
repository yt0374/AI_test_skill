#!/bin/bash
# =============================================================================
# Jingmen Cutting System 2.0 - Test Execution Script (Linux/macOS/Git Bash)
# Environment: 荆门鹰美 (bak.jmym.dtsimple.pro)
# =============================================================================
#
# Retry Strategy:
#   - First run: max 2 retries per test (pytest --reruns 2 --reruns-delay 5)
#   - If a test fails 3+ consecutive runs: quarantine
#   - Quarantined tests run separately with --lf (last-failed) for investigation
#   - Weekly: review quarantined tests, fix or permanently skip
#
# Usage:
#   ./run_tests.sh smoke       # P0 smoke tests only
#   ./run_tests.sh functional  # P0 + P1 functional tests
#   ./run_tests.sh full        # P0 + P1 + P2 boundary tests
#   ./run_tests.sh integration # P3 integration tests
#   ./run_tests.sh complete    # All tests (including quarantine)
#   ./run_tests.sh quarantine  # Quarantined tests only
# =============================================================================

set -e

cd "$(dirname "$0")/erp_tests"

echo "=========================================="
echo "  Jingmen Cutting System 2.0 Test Suite"
echo "  Environment: bak.jmym.dtsimple.pro"
echo "=========================================="

case "${1:-smoke}" in
  smoke)
    echo "[MODE] Smoke Tests (P0 only)"
    pytest -m p0 -v --tb=short --strict-markers --reruns 2 --reruns-delay 5 \
      --html=../reports/smoke_report.html --self-contained-html \
      --junitxml=../reports/smoke_junit.xml
    ;;
  functional)
    echo "[MODE] Functional Tests (P0 + P1)"
    pytest -m "p0 or p1" -v --tb=short --strict-markers --reruns 2 --reruns-delay 5 \
      --html=../reports/functional_report.html --self-contained-html \
      --junitxml=../reports/functional_junit.xml
    ;;
  full)
    echo "[MODE] Full Boundary Tests (P0 + P1 + P2)"
    pytest -m "p0 or p1 or p2" -v --tb=short --strict-markers --reruns 2 --reruns-delay 5 \
      --html=../reports/full_report.html --self-contained-html \
      --junitxml=../reports/full_junit.xml
    ;;
  integration)
    echo "[MODE] Integration Tests (P3)"
    pytest -m p3 -v --tb=long --strict-markers --reruns 1 --reruns-delay 10 \
      --html=../reports/integration_report.html --self-contained-html \
      --junitxml=../reports/integration_junit.xml
    ;;
  complete)
    echo "[MODE] Complete Test Suite (All tests)"
    pytest -v --tb=short --strict-markers --reruns 2 --reruns-delay 5 \
      --html=../reports/complete_report.html --self-contained-html \
      --junitxml=../reports/complete_junit.xml
    ;;
  quarantine)
    echo "[MODE] Quarantined Tests Only"
    pytest test_quarantine.py -v --tb=long --strict-markers \
      --html=../reports/quarantine_report.html --self-contained-html
    ;;
  *)
    echo "Usage: $0 {smoke|functional|full|integration|complete|quarantine}"
    exit 1
    ;;
esac

EXIT_CODE=$?

echo ""
echo "=========================================="
echo "  Test execution completed with exit code: $EXIT_CODE"
echo "=========================================="

exit $EXIT_CODE
