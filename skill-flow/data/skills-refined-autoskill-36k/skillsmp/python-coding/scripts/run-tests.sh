#!/bin/bash
# Run pytest on a specified test file or directory
#
# Usage: run-tests.sh [test_path] [--verbose]
#
# Arguments:
#   test_path: Path to test file or directory (optional, defaults to current directory)
#   --verbose: Run tests with verbose output
#
# Exit codes:
#   0: All tests passed
#   1: Some tests failed
#   2: Error running tests

set -e

TEST_PATH="."
VERBOSE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose|-v)
            VERBOSE="-v"
            shift
            ;;
        *)
            TEST_PATH="$1"
            shift
            ;;
    esac
done

# Check if pytest is available
if ! command -v pytest &> /dev/null; then
    echo "Error: pytest is not installed"
    echo "Install with: pip install pytest"
    exit 2
fi

# Check if test path exists
if [ ! -e "$TEST_PATH" ]; then
    echo "Error: Test path not found: $TEST_PATH"
    exit 2
fi

echo "Running tests: $TEST_PATH"
echo "=========================================="

# Build pytest command
PYTEST_CMD="pytest $TEST_PATH $VERBOSE"

echo "Command: $PYTEST_CMD"
echo ""

# Run pytest
if $PYTEST_CMD; then
    echo ""
    echo "=========================================="
    echo "✓ All tests passed"
    exit 0
else
    echo ""
    echo "=========================================="
    echo "✗ Some tests failed"
    exit 1
fi

