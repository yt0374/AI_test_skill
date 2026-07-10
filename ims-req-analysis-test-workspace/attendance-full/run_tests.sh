#!/bin/bash
# IMS Attendance Test Execution Script
# Usage:
#   sh run_tests.sh smoke       # P0 smoke tests
#   sh run_tests.sh functional  # P0+P1 functional tests
#   sh run_tests.sh full        # P0+P1+P2 boundary tests
#   sh run_tests.sh integration # P3 integration tests
#   sh run_tests.sh complete    # All tests
#   sh run_tests.sh quarantine  # Quarantined tests only

MODE=${1:-smoke}

case $MODE in
  smoke)
    echo "=== Running P0 Smoke Tests ==="
    pytest erp_tests/ -m p0 -v --tb=line
    ;;
  functional)
    echo "=== Running P0+P1 Functional Tests ==="
    pytest erp_tests/ -m "p0 or p1" -v --tb=short
    ;;
  full)
    echo "=== Running P0+P1+P2 Full Tests ==="
    pytest erp_tests/ -m "p0 or p1 or p2" -v --tb=short
    ;;
  integration)
    echo "=== Running P3 Integration Tests ==="
    pytest erp_tests/ -m p3 -v --tb=long
    ;;
  complete)
    echo "=== Running Complete Test Suite ==="
    pytest erp_tests/ -v --tb=short --html=reports/test_report.html --self-contained-html
    ;;
  quarantine)
    echo "=== Running Quarantined Tests ==="
    pytest erp_tests/ -m quarantine -v --tb=short
    ;;
  *)
    echo "Usage: sh run_tests.sh [smoke|functional|full|integration|complete|quarantine]"
    exit 1
    ;;
esac

echo "=== Done ==="
