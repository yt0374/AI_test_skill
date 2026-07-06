# =============================================================================
# Jingmen Cutting System 2.0 - Test Execution Script (Windows PowerShell)
# Environment: Jingmen Yingmei (bak.jmym.dtsimple.pro)
# =============================================================================
#
# Retry Strategy:
#   - First run: max 2 retries per test (pytest --reruns 2 --reruns-delay 5)
#   - If a test fails 3+ consecutive runs: quarantine
#   - Quarantined tests run separately with --lf (last-failed) for investigation
#   - Weekly: review quarantined tests, fix or permanently skip
#
# Usage:
#   .\run_tests.ps1 smoke       # P0 smoke tests only
#   .\run_tests.ps1 functional  # P0 + P1 functional tests
#   .\run_tests.ps1 full        # P0 + P1 + P2 boundary tests
#   .\run_tests.ps1 integration # P3 integration tests
#   .\run_tests.ps1 complete    # All tests (including quarantine)
#   .\run_tests.ps1 quarantine  # Quarantined tests only
# =============================================================================

param(
    [ValidateSet("smoke", "functional", "full", "integration", "complete", "quarantine")]
    [string]$Mode = "smoke"
)

Set-Location "$PSScriptRoot\erp_tests"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Jingmen Cutting System 2.0 Test Suite" -ForegroundColor Cyan
Write-Host "  Environment: bak.jmym.dtsimple.pro" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$commonArgs = @(
    "-v", "--tb=short", "--strict-markers"
)

$retryArgs = @("--reruns", "2", "--reruns-delay", "5")

switch ($Mode) {
    "smoke" {
        Write-Host "[MODE] Smoke Tests (P0 only)" -ForegroundColor Yellow
        $reportDir = "..\reports"
        New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
        pytest -m p0 @commonArgs @retryArgs `
            --html="$reportDir\smoke_report.html" --self-contained-html `
            --junitxml="$reportDir\smoke_junit.xml"
    }
    "functional" {
        Write-Host "[MODE] Functional Tests (P0 + P1)" -ForegroundColor Yellow
        $reportDir = "..\reports"
        New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
        pytest -m "p0 or p1" @commonArgs @retryArgs `
            --html="$reportDir\functional_report.html" --self-contained-html `
            --junitxml="$reportDir\functional_junit.xml"
    }
    "full" {
        Write-Host "[MODE] Full Boundary Tests (P0 + P1 + P2)" -ForegroundColor Yellow
        $reportDir = "..\reports"
        New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
        pytest -m "p0 or p1 or p2" @commonArgs @retryArgs `
            --html="$reportDir\full_report.html" --self-contained-html `
            --junitxml="$reportDir\full_junit.xml"
    }
    "integration" {
        Write-Host "[MODE] Integration Tests (P3)" -ForegroundColor Yellow
        $reportDir = "..\reports"
        New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
        pytest -m p3 @commonArgs --reruns 1 --reruns-delay 10 `
            --html="$reportDir\integration_report.html" --self-contained-html `
            --junitxml="$reportDir\integration_junit.xml"
    }
    "complete" {
        Write-Host "[MODE] Complete Test Suite (All tests)" -ForegroundColor Yellow
        $reportDir = "..\reports"
        New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
        pytest @commonArgs @retryArgs `
            --html="$reportDir\complete_report.html" --self-contained-html `
            --junitxml="$reportDir\complete_junit.xml"
    }
    "quarantine" {
        Write-Host "[MODE] Quarantined Tests Only" -ForegroundColor Yellow
        $reportDir = "..\reports"
        New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
        pytest test_quarantine.py @commonArgs `
            --html="$reportDir\quarantine_report.html" --self-contained-html
    }
}

$exitCode = $LASTEXITCODE

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Test execution completed with exit code: $exitCode" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

exit $exitCode
