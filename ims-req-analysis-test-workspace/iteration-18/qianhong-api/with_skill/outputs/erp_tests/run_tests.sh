#!/bin/bash
# IMS API Test Runner - 千虹接口文档 v3.0.1
# Usage: bash run_tests.sh [mode]

set -e

# Default to full suite if no mode specified
MODE="${1:-full}"

# Environment setup
export IMS_BASE_URL="${IMS_BASE_URL:-http://test.fj.dtsimple.pro/api/ims-open-api}"
export IMS_TEST_USERNAME="${IMS_TEST_USERNAME:-admin}"
export IMS_TEST_PASSWORD="${IMS_TEST_PASSWORD:-IMS@2026}"

cd "$(dirname "$0")"

echo "=========================================="
echo "IMS API Test Runner - 千虹接口文档 v3.0.1"
echo "Environment: $IMS_BASE_URL"
echo "Mode: $MODE"
echo "=========================================="

case "$MODE" in
    smoke)
        echo "[Smoke] Running P0 tests only..."
        python -m pytest erp_tests/test_api.py -m p0 -v --tb=short \
            --reruns 2 --reruns-delay 5 \
            --junitxml=reports/junit_smoke.xml \
            --json-report --json-report-file=reports/pytest_results_smoke.json
        ;;
    functional)
        echo "[Functional] Running P0+P1 tests..."
        python -m pytest erp_tests/test_api.py -m "p0 or p1" -v --tb=short \
            --reruns 2 --reruns-delay 5 \
            --junitxml=reports/junit_functional.xml \
            --json-report --json-report-file=reports/pytest_results_functional.json
        ;;
    full)
        echo "[Full] Running P0+P1+P2 tests..."
        python -m pytest erp_tests/test_api.py -m "p0 or p1 or p2" -v --tb=short \
            --reruns 2 --reruns-delay 5 \
            --junitxml=reports/junit_full.xml \
            --json-report --json-report-file=reports/pytest_results_full.json
        ;;
    integration)
        echo "[Integration] Running P3 tests..."
        python -m pytest erp_tests/test_api.py -m p3 -v --tb=short \
            --reruns 2 --reruns-delay 5 \
            --junitxml=reports/junit_integration.xml \
            --json-report --json-report-file=reports/pytest_results_integration.json
        ;;
    complete)
        echo "[Complete] Running ALL tests..."
        python -m pytest erp_tests/test_api.py -v --tb=short \
            --reruns 2 --reruns-delay 5 \
            --junitxml=reports/junit_complete.xml \
            --json-report --json-report-file=reports/pytest_results_complete.json
        ;;
    collect)
        echo "[Collect] Listing all test cases..."
        python -m pytest erp_tests/test_api.py --collect-only -q
        ;;
    *)
        echo "Unknown mode: $MODE"
        echo "Valid modes: smoke, functional, full, integration, complete, collect"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "Test execution completed."
echo "Report: reports/pytest_results_${MODE}.json"
echo "JUnit: reports/junit_${MODE}.xml"
echo "=========================================="
