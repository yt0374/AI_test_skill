#!/usr/bin/env bash
# ==============================================================================
# IMS Attendance (考勤) Test Execution Script
# ==============================================================================
# Retry strategy:
#   - 1st retry: potential timing issue (e.g., slow page load, animation delay)
#   - 2nd retry: potential environment flakiness (e.g., network hiccup, CI variance)
#   - After 2 retries fail: mark as quarantine candidate for manual review
# ==============================================================================

set -euo pipefail

# Ensure we're in the project root
cd "$(dirname "$0")"

echo "============================================"
echo "  IMS Attendance Test Runner"
echo "============================================"

case "${1:-help}" in
  smoke)
    echo ">>> Running SMOKE tests (P0 only)"
    pytest -m p0
    ;;

  functional)
    echo ">>> Running FUNCTIONAL tests (P0 + P1)"
    pytest -m "p0 or p1"
    ;;

  full)
    echo ">>> Running FULL tests (P0 + P1 + P2)"
    pytest -m "p0 or p1 or p2"
    ;;

  integration)
    echo ">>> Running INTEGRATION tests (P3 only)"
    pytest -m p3
    ;;

  complete)
    echo ">>> Running COMPLETE suite (all markers)"
    pytest
    ;;

  report)
    echo ">>> Running COMPLETE suite with HTML report"
    mkdir -p reports
    pytest --html=reports/test_report.html --self-contained-html
    echo ">>> Report saved to reports/test_report.html"
    ;;

  help|*)
    echo "Usage: run_tests.sh <mode>"
    echo ""
    echo "Modes:"
    echo "  smoke         P0 smoke tests only        (fast, critical path)"
    echo "  functional    P0 + P1 functional tests    (core business flows)"
    echo "  full          P0 + P1 + P2 boundary tests (broad coverage)"
    echo "  integration   P3 integration tests        (cross-module)"
    echo "  complete      All markers, no filter      (full suite)"
    echo "  report        Complete suite + HTML report (--self-contained-html)"
    echo ""
    echo "Examples:"
    echo "  ./run_tests.sh smoke"
    echo "  ./run_tests.sh report"
    ;;
esac
