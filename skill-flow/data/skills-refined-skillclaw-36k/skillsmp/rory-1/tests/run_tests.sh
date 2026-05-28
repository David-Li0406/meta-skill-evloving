#!/bin/bash
# CMO Agent Test Runner
# Usage: ./run_tests.sh [options]
#
# Options:
#   --all       Run all tests
#   --base      Run base/credential tests only
#   --api       Run API client tests only
#   --ads       Run ads safety tests only
#   --coverage  Run with coverage report

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "Installing pytest and dependencies..."
    pip install pytest pytest-cov httpx pyyaml python-dotenv
fi

echo "=========================================="
echo "CMO Agent Test Suite"
echo "=========================================="
echo ""

case "${1:-all}" in
    --base)
        echo "Running base/credential tests..."
        pytest tests/test_base.py -v
        ;;
    --api)
        echo "Running API client tests..."
        pytest tests/test_api_clients.py -v
        ;;
    --ads)
        echo "Running ads safety tests..."
        pytest tests/test_ads_safety.py -v
        ;;
    --coverage)
        echo "Running all tests with coverage..."
        pytest tests/ -v --cov=tools --cov-report=term-missing --cov-report=html
        echo ""
        echo "Coverage report generated in htmlcov/"
        ;;
    --all|*)
        echo "Running all tests..."
        pytest tests/ -v
        ;;
esac

echo ""
echo "=========================================="
echo "Tests completed!"
echo "=========================================="
