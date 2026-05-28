#!/bin/bash
# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

#
# Parallel Test Runner with Auto-Logging and Tail
#
# This wrapper script:
# 1. Runs tests in background with output to log file
# 2. Uses tail -f to follow the log in real-time
# 3. Cleans up background process on exit
#
# Usage:
#   ./run_tests_with_log.sh [OPTIONS]
#
# All OPTIONS are passed to run_tests_parallel.sh
#
# Common Options:
#   -c, --concurrency N     Max concurrent test files (default: 4)
#   -t, --timeout DURATION  Timeout per test file (default: 30m)
#   -C, --cleanup           Run cleanup before tests (requires BCM credentials)
#   --resources-only        Run only resource tests
#   --data-sources-only     Run only data source tests
#   --verbose               Show detailed test output
#   -h, --help              Show all options
#
# Examples:
#   # Run all tests with max concurrency
#   ./run_tests_with_log.sh -c 21 -t 30m
#
#   # Run with cleanup before tests
#   ./run_tests_with_log.sh --cleanup -c 21
#
#   # Run only resource tests with cleanup
#   ./run_tests_with_log.sh --resources-only -c 8 --cleanup
#

set -euo pipefail

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create log file with timestamp
LOG_FILE="/tmp/terraform-tests-$(date +%Y%m%d-%H%M%S).log"

echo "======================================"
echo "Parallel Test Execution with Logging"
echo "======================================"
echo "Log file: $LOG_FILE"
echo "Press Ctrl+C to stop monitoring (tests will continue)"
echo "======================================"
echo ""

# Cleanup function
cleanup() {
    if [ -n "${TEST_PID:-}" ] && kill -0 "$TEST_PID" 2>/dev/null; then
        echo ""
        echo "Tests still running in background (PID: $TEST_PID)"
        echo "Log file: $LOG_FILE"
        echo "To monitor: tail -f $LOG_FILE"
        echo "To stop tests: kill $TEST_PID"
    fi
}

trap cleanup EXIT

# Start tests in background
"$SCRIPT_DIR/run_tests_parallel.sh" "$@" > "$LOG_FILE" 2>&1 &
TEST_PID=$!

echo "Tests started (PID: $TEST_PID)"
echo "Monitoring output..."
echo ""

# Wait a moment for file to be created
sleep 1

# Tail the log file
tail -f "$LOG_FILE" &
TAIL_PID=$!

# Wait for tests to complete
wait "$TEST_PID" 2>/dev/null || true
TEST_EXIT_CODE=$?

# Stop tailing
kill "$TAIL_PID" 2>/dev/null || true

echo ""
echo "======================================"
echo "Tests completed with exit code: $TEST_EXIT_CODE"
echo "Full log saved to: $LOG_FILE"
echo "======================================"

exit $TEST_EXIT_CODE
