#!/bin/bash
# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

#
# Terraform Provider Test Compilation Verification Script
#
# Quickly verifies that test files compile without errors after modernization.
# Does not run tests, only checks for syntax and compilation errors.
#
# Usage:
#   ./verify_compilation.sh <test_directory>
#   ./verify_compilation.sh ./internal/provider/
#

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
TEST_DIR="${1:-.internal/provider}"

if [ ! -d "$TEST_DIR" ]; then
    echo -e "${RED}Error: Directory $TEST_DIR does not exist${NC}"
    exit 1
fi

echo "===== Terraform Provider Test Compilation Verification ====="
echo "Test Directory: $TEST_DIR"
echo ""

# Set Go environment variables for workspace
export GOMODCACHE="${GOMODCACHE:-/workspace/.go/pkg/mod}"
export GOCACHE="${GOCACHE:-/workspace/.go/cache}"
export GOPATH="${GOPATH:-/workspace/.go}"

echo "Go Environment:"
echo "  GOMODCACHE: $GOMODCACHE"
echo "  GOCACHE: $GOCACHE"
echo "  GOPATH: $GOPATH"
echo ""

# Create temporary output file for compilation
TEMP_OUTPUT=$(mktemp /tmp/provider_test_compile.XXXXXX)

echo "Compiling test files..."
echo ""

# Attempt to compile
if go test -c "$TEST_DIR" -o "$TEMP_OUTPUT" 2>&1 | tee /tmp/compile_log.txt; then
    # Success
    echo ""
    echo -e "${GREEN}✅ SUCCESS: All tests compile without errors${NC}"
    echo ""

    # Show statistics
    TEST_COUNT=$(grep -h "^func TestAcc" "$TEST_DIR"/*_test.go 2>/dev/null | wc -l)
    FILE_COUNT=$(ls -1 "$TEST_DIR"/*_test.go 2>/dev/null | wc -l)

    echo "Statistics:"
    echo "  Test files: $FILE_COUNT"
    echo "  Test functions: $TEST_COUNT"
    echo ""

    # Cleanup
    rm -f "$TEMP_OUTPUT" /tmp/compile_log.txt
    exit 0
else
    # Failure
    echo ""
    echo -e "${RED}❌ COMPILATION FAILED${NC}"
    echo ""

    # Parse and display errors nicely
    echo "Errors found:"
    echo ""

    # Extract error lines
    grep -E "^#|:\d+:\d+:" /tmp/compile_log.txt | head -n 20

    echo ""
    echo -e "${YELLOW}Full compilation log saved to: /tmp/compile_log.txt${NC}"
    echo ""

    # Cleanup temporary file
    rm -f "$TEMP_OUTPUT"

    exit 1
fi
