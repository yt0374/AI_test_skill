#!/bin/bash
# Windows PowerShell test runner (cross-platform note: use run_tests.sh on Linux/Mac)
# Usage: .\run_tests.ps1 [mode]

param(
    [string]$Mode = "full"
)

$env:IMS_BASE_URL = if ($env:IMS_BASE_URL) { $env:IMS_BASE_URL } else { "http://test.fj.dtsimple.pro/api/ims-open-api" }
$env:IMS_TEST_USERNAME = if ($env:IMS_TEST_USERNAME) { $env:IMS_TEST_USERNAME } else { "admin" }
$env:IMS_TEST_PASSWORD = if ($env:IMS_TEST_PASSWORD) { $env:IMS_TEST_PASSWORD } else { "IMS@2026" }

Write-Host "=========================================="
Write-Host "IMS API Test Runner - 千虹接口文档 v3.0.1"
Write-Host "Environment: $env:IMS_BASE_URL"
Write-Host "Mode: $Mode"
Write-Host "=========================================="

$pytestArgs = @()

switch ($Mode) {
    "smoke" {
        Write-Host "[Smoke] Running P0 tests only..."
        $pytestArgs = @("-m", "p0")
    }
    "functional" {
        Write-Host "[Functional] Running P0+P1 tests..."
        $pytestArgs = @("-m", "p0 or p1")
    }
    "full" {
        Write-Host "[Full] Running P0+P1+P2 tests..."
        $pytestArgs = @("-m", "p0 or p1 or p2")
    }
    "integration" {
        Write-Host "[Integration] Running P3 tests..."
        $pytestArgs = @("-m", "p3")
    }
    "complete" {
        Write-Host "[Complete] Running ALL tests..."
        $pytestArgs = @()
    }
    "collect" {
        Write-Host "[Collect] Listing all test cases..."
        python -m pytest erp_tests/test_api.py --collect-only -q
        return
    }
    default {
        Write-Host "Unknown mode: $Mode"
        Write-Host "Valid modes: smoke, functional, full, integration, complete, collect"
        exit 1
    }
}

python -m pytest erp_tests/test_api.py $pytestArgs -v --tb=short `
    --reruns 2 --reruns-delay 5 `
    --junitxml=reports/junit_$Mode.xml `
    --json-report --json-report-file=reports/pytest_results_$Mode.json

Write-Host ""
Write-Host "=========================================="
Write-Host "Test execution completed."
Write-Host "=========================================="
