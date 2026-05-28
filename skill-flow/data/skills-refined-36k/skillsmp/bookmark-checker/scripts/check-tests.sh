#!/bin/bash

# Bookmark Checker: Test Suite Check
# Runs Jest tests and reports coverage metrics

set -e

# Navigate to project root
PROJECT_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$PROJECT_ROOT"

echo "[TEST_CHECK] Starting test validation..."

# Check if Jest is available
if ! command -v npx &> /dev/null; then
  echo "ERROR: npx not found. Install Node.js first."
  exit 2
fi

# Check jest.config.js or jest configuration exists
if [ ! -f "jest.config.js" ] && ! grep -q '"jest"' package.json 2>/dev/null; then
  echo "⚠️ Jest not configured in project"
  echo "INFO: Skipping test check (no Jest config found)"
  exit 0
fi

# Check for test files
TEST_COUNT=$(find __tests__ -name "*.test.ts" -o -name "*.test.tsx" -o -name "*.spec.ts" -o -name "*.spec.tsx" 2>/dev/null | wc -l || echo 0)

if [ "$TEST_COUNT" -eq 0 ]; then
  echo "⚠️ No test files found"
  echo "INFO: Create tests in __tests__/ directory for coverage"
  exit 0
fi

echo "📊 Test Statistics:"
echo "  Test files found: $TEST_COUNT"
echo ""

# Try to run tests with coverage
echo "Running tests with coverage..."
echo ""

# Create temporary coverage report file
COVERAGE_FILE="/tmp/jest_coverage.json"

# Run Jest with coverage (non-blocking if tests fail)
if npx jest --coverage --json --outputFile=$COVERAGE_FILE --testPathPattern="__tests__" 2>&1 | tee /tmp/jest_output.txt; then
  TEST_STATUS="PASS"
  TEST_EXIT=0
else
  TEST_STATUS="FAIL"
  TEST_EXIT=1
fi

# Parse test results
if [ -f "/tmp/jest_output.txt" ]; then
  PASSED=$(grep -o "passed" /tmp/jest_output.txt | wc -l || echo 0)
  FAILED=$(grep -o "failed" /tmp/jest_output.txt | wc -l || echo 0)

  if [ "$FAILED" -eq 0 ] && [ "$PASSED" -gt 0 ]; then
    echo "✅ All tests passed"
  elif [ "$FAILED" -gt 0 ]; then
    echo "❌ $FAILED tests failed"
  fi
fi

# Parse coverage if available
if [ -f "$COVERAGE_FILE" ]; then
  # Try to extract coverage percentages
  COVERAGE_JSON=$(cat $COVERAGE_FILE 2>/dev/null | grep -o '"coverage".*' || echo "")

  if [ -n "$COVERAGE_JSON" ]; then
    echo ""
    echo "📈 Coverage Report:"
    echo "  (Coverage data generated - check full report for details)"
  fi
fi

echo ""
echo "Test Summary:"
echo "  Status: $TEST_STATUS"

if [ "$TEST_EXIT" -eq 0 ]; then
  echo ""
  echo "✅ TEST_CHECK: PASS"
  exit 0
else
  echo ""
  echo "⚠️ TEST_CHECK: WARN - Some tests failed (review output)"
  exit 1
fi
