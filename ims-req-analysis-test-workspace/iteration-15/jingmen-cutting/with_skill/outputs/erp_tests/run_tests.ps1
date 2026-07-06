# =============================================================
# IMS ERP Test Execution Scripts (PowerShell)
# Project: 荆门新裁剪需求2.0
# Environment: jingmen (bak.jmym.dtsimple.pro)
# =============================================================

param(
    [ValidateSet("smoke", "functional", "full", "integration", "complete", "env", "report")]
    [string]$Mode = "functional"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  荆门新裁剪需求2.0 - Test Runner" -ForegroundColor Cyan
Write-Host "  Environment: jingmen (bak.jmym.dtsimple.pro)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Install dependencies (first run)
if (-not (Test-Path "venv")) {
    Write-Host "[SETUP] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install pytest pytest-playwright pytest-rerunfailures pytest-json-report
    python -m playwright install chromium
} else {
    .\venv\Scripts\Activate.ps1
}

# Create reports directory
New-Item -ItemType Directory -Force -Path "reports" | Out-Null

switch ($Mode) {
    "smoke" {
        Write-Host ">>> MODE: Smoke Tests (P0 only)" -ForegroundColor Green
        pytest erp_tests/ -m p0 --json-report --json-report-file=reports/pytest_results_smoke.json -v --tb=short
    }
    "functional" {
        Write-Host ">>> MODE: Functional Regression (P0 + P1)" -ForegroundColor Green
        pytest erp_tests/ -m "p0 or p1" --json-report --json-report-file=reports/pytest_results_functional.json -v --tb=short
    }
    "full" {
        Write-Host ">>> MODE: Full Suite (P0 + P1 + P2)" -ForegroundColor Green
        pytest erp_tests/ -m "p0 or p1 or p2" --json-report --json-report-file=reports/pytest_results_full.json -v --tb=short
    }
    "integration" {
        Write-Host ">>> MODE: Integration Tests (P3)" -ForegroundColor Green
        pytest erp_tests/ -m p3 --json-report --json-report-file=reports/pytest_results_integration.json -v --tb=short
    }
    "complete" {
        Write-Host ">>> MODE: Complete Suite (All tests)" -ForegroundColor Green
        pytest erp_tests/ --json-report --json-report-file=reports/pytest_results_complete.json --junitxml=reports/junit.xml -v --tb=short
    }
    "env" {
        Write-Host ">>> MODE: SIT -> Jingmen Environment Order" -ForegroundColor Green
        Write-Host "--- Phase 1: SIT Environment (P0+P1) ---" -ForegroundColor Yellow
        pytest erp_tests/ -m "p0 or p1 and sit" --json-report --json-report-file=reports/pytest_results_sit.json -v --tb=short
        Write-Host "--- Phase 2: Jingmen Environment (P0+P1+P2) ---" -ForegroundColor Yellow
        pytest erp_tests/ -m "p0 or p1 or p2 and jingmen" --json-report --json-report-file=reports/pytest_results_jingmen.json -v --tb=short
    }
    "report" {
        Write-Host ">>> Generating aggregated test report..." -ForegroundColor Green
        # Report generation logic
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Test execution complete" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
