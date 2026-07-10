# IMS Attendance Test Execution Script (PowerShell)
# Usage:
#   .\run_tests.ps1 smoke       # P0 smoke tests
#   .\run_tests.ps1 functional  # P0+P1 functional tests
#   .\run_tests.ps1 full        # P0+P1+P2 boundary tests
#   .\run_tests.ps1 integration # P3 integration tests
#   .\run_tests.ps1 complete    # All tests

param([string]$Mode = "smoke")

switch ($Mode) {
  "smoke" {
    Write-Host "=== Running P0 Smoke Tests ==="
    pytest erp_tests/ -m p0 -v --tb=line
  }
  "functional" {
    Write-Host "=== Running P0+P1 Functional Tests ==="
    pytest erp_tests/ -m "p0 or p1" -v --tb=short
  }
  "full" {
    Write-Host "=== Running P0+P1+P2 Full Tests ==="
    pytest erp_tests/ -m "p0 or p1 or p2" -v --tb=short
  }
  "integration" {
    Write-Host "=== Running P3 Integration Tests ==="
    pytest erp_tests/ -m p3 -v --tb=long
  }
  "complete" {
    Write-Host "=== Running Complete Test Suite ==="
    pytest erp_tests/ -v --tb=short --html=reports/test_report.html --self-contained-html
  }
  default {
    Write-Host "Usage: .\run_tests.ps1 [smoke|functional|full|integration|complete]"
  }
}
