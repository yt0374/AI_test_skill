#!/usr/bin/env bash
# =============================================================================
# Jingmen Cutting 2.0 — Test Execution Script
# Environment: jingmen (bak.jmym.dtsimple.pro)
# Login: admin / ym5579 (direct login, no enterprise selector)
# =============================================================================
#
# Windows PowerShell equivalent: see comments at end of this file.
# To run on Windows PowerShell, copy the PS1 blocks below.
#
# =============================================================================
# Quick Start
# =============================================================================
#   chmod +x run_tests.sh
#   ./run_tests.sh smoke        # P0 only (fast, ~2 min)
#   ./run_tests.sh functional   # P0 + P1 (daily regression, ~8 min)
#   ./run_tests.sh full         # P0 + P1 + P2 (pre-release, ~15 min)
#   ./run_tests.sh integration  # P3 integration tests (~5 min)
#   ./run_tests.sh all          # Complete suite (~20 min)
#   ./run_tests.sh quarantine   # Quarantined flaky tests
# =============================================================================

set -euo pipefail

MODE="${1:-smoke}"
REPORT_DIR="reports/$(date +%Y-%m-%d_%H%M%S)"
mkdir -p "$REPORT_DIR"

echo "=========================================="
echo " Jingmen Cutting 2.0 Test Suite"
echo " Environment: bak.jmym.dtsimple.pro"
echo " Mode: $MODE"
echo " Report: $REPORT_DIR"
echo "=========================================="

case "$MODE" in
  smoke)
    echo "[Smoke] Running P0 tests..."
    pytest erp_tests/ -m p0 \
      --junitxml="$REPORT_DIR/junit.xml" \
      --json-report --json-report-file="$REPORT_DIR/pytest_results.json" \
      --html="$REPORT_DIR/report.html" --self-contained-html \
      -v --tb=short
    ;;

  functional)
    echo "[Functional] Running P0 + P1 tests..."
    pytest erp_tests/ -m "p0 or p1" \
      --junitxml="$REPORT_DIR/junit.xml" \
      --json-report --json-report-file="$REPORT_DIR/pytest_results.json" \
      -v --tb=short
    ;;

  full)
    echo "[Full] Running P0 + P1 + P2 tests..."
    pytest erp_tests/ -m "p0 or p1 or p2" \
      --junitxml="$REPORT_DIR/junit.xml" \
      --json-report --json-report-file="$REPORT_DIR/pytest_results.json" \
      -v --tb=short
    ;;

  integration)
    echo "[Integration] Running P3 cross-module tests..."
    pytest erp_tests/ -m p3 \
      --junitxml="$REPORT_DIR/junit.xml" \
      --json-report --json-report-file="$REPORT_DIR/pytest_results.json" \
      -v --tb=long
    ;;

  all|complete)
    echo "[All] Running complete test suite..."
    pytest erp_tests/ \
      --junitxml="$REPORT_DIR/junit.xml" \
      --json-report --json-report-file="$REPORT_DIR/pytest_results.json" \
      -v --tb=short
    ;;

  quarantine)
    echo "[Quarantine] Running quarantined flaky tests..."
    pytest erp_tests/ -m quarantine \
      --junitxml="$REPORT_DIR/junit.xml" \
      --json-report --json-report-file="$REPORT_DIR/pytest_results.json" \
      -v --tb=short
    ;;

  *)
    echo "Usage: $0 {smoke|functional|full|integration|all|quarantine}"
    exit 1
    ;;
esac

EXIT_CODE=$?
echo ""
echo "=========================================="
echo " Test execution complete (exit: $EXIT_CODE)"
echo " Reports: $REPORT_DIR/"
echo "=========================================="
exit $EXIT_CODE

# =============================================================================
# Windows PowerShell Equivalent (run_tests.ps1)
# =============================================================================
# Copy the block below to run_tests.ps1 for Windows execution:
#
#   param([string]$Mode = "smoke")
#   $ReportDir = "reports/$(Get-Date -Format 'yyyy-MM-dd_HHmmss')"
#   New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null
#
#   Write-Host "==========================================" -ForegroundColor Cyan
#   Write-Host " Jingmen Cutting 2.0 Test Suite" -ForegroundColor Cyan
#   Write-Host " Environment: bak.jmym.dtsimple.pro" -ForegroundColor Cyan
#   Write-Host " Mode: $Mode" -ForegroundColor Cyan
#   Write-Host "==========================================" -ForegroundColor Cyan
#
#   switch ($Mode) {
#     "smoke"       { pytest erp_tests/ -m p0 --junitxml="$ReportDir/junit.xml" --json-report --json-report-file="$ReportDir/pytest_results.json" -v --tb=short }
#     "functional"  { pytest erp_tests/ -m "p0 or p1" --junitxml="$ReportDir/junit.xml" --json-report --json-report-file="$ReportDir/pytest_results.json" -v --tb=short }
#     "full"        { pytest erp_tests/ -m "p0 or p1 or p2" --junitxml="$ReportDir/junit.xml" --json-report --json-report-file="$ReportDir/pytest_results.json" -v --tb=short }
#     "integration" { pytest erp_tests/ -m p3 --junitxml="$ReportDir/junit.xml" --json-report --json-report-file="$ReportDir/pytest_results.json" -v --tb=long }
#     "all"         { pytest erp_tests/ --junitxml="$ReportDir/junit.xml" --json-report --json-report-file="$ReportDir/pytest_results.json" -v --tb=short }
#     "quarantine"  { pytest erp_tests/ -m quarantine --junitxml="$ReportDir/junit.xml" --json-report --json-report-file="$ReportDir/pytest_results.json" -v --tb=short }
#     default       { Write-Host "Usage: .\run_tests.ps1 {smoke|functional|full|integration|all|quarantine}" }
#   }
#
#   Write-Host "`n==========================================" -ForegroundColor Cyan
#   Write-Host " Reports: $ReportDir/" -ForegroundColor Cyan
#   Write-Host "==========================================" -ForegroundColor Cyan
#
# =============================================================================
# Environment Notes
# =============================================================================
# - Jingmen (荆门鹰美): bak.jmym.dtsimple.pro, admin/ym5579
# - Direct login; no enterprise selector
# - Module names are simple (e.g., '生产' not 'gm.生产#3')
# - .third-menu panel for sub-menu navigation
# =============================================================================
