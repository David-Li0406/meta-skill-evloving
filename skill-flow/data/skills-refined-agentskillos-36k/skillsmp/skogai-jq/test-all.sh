#!/usr/bin/env bash
set -euo pipefail

# Run all transformation tests

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Running all jq-transforms tests..."
echo ""

# Track test results
FAILED_TESTS=()
PASSED_TESTS=()

# Find all test.sh files and run them
for test_script in "$SCRIPT_DIR"/*/test.sh; do
    if [[ -f "$test_script" ]]; then
        transformation=$(basename "$(dirname "$test_script")")
        echo "========================================"
        echo "Testing: $transformation"
        echo "========================================"

        if "$test_script"; then
            PASSED_TESTS+=("$transformation")
        else
            FAILED_TESTS+=("$transformation")
        fi
        echo ""
    fi
done

# Report results
echo "========================================"
echo "Test Summary"
echo "========================================"
echo "Passed: ${#PASSED_TESTS[@]}"
for test in "${PASSED_TESTS[@]}"; do
    echo "  ✓ $test"
done

if [[ ${#FAILED_TESTS[@]} -gt 0 ]]; then
    echo ""
    echo "Failed: ${#FAILED_TESTS[@]}"
    for test in "${FAILED_TESTS[@]}"; do
        echo "  ✗ $test"
    done
    exit 1
else
    echo ""
    echo "All tests passed! 🎉"
fi
