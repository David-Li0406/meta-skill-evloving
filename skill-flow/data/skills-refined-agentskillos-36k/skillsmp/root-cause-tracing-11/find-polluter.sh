#!/usr/bin/env bash
# Accelerated bisection script to find test polluters
set -e

if [ $# -lt 1 ]; then
  echo "Usage: $0 <file_to_check> [test_pattern]"
  echo "Example: $0 '.git' '.*\\.test\\.ts$'"
  exit 1
fi

POLLUTION_CHECK="$1"
TEST_PATTERN="${2:-.*\.test\.ts$}"

echo "Searching for test that creates: $POLLUTION_CHECK"

# Use fd to find test files (fast, ignores node_modules/.git by default)
TEST_FILES=$(fd -t f -p "$TEST_PATTERN" | sort)
TOTAL=$(echo "$TEST_FILES" | wc -l | tr -d ' ')

echo "Found $TOTAL test files."

COUNT=0
for TEST_FILE in $TEST_FILES; do
  COUNT=$((COUNT + 1))
  if [ -e "$POLLUTION_CHECK" ]; then
    echo "Pollution detected BEFORE test $COUNT."
    exit 1
  fi

  echo -ne "[$COUNT/$TOTAL] Testing: $TEST_FILE\r"

  # PASS ARGUMENT CORRECTLY WITH --
  npm test -- "$TEST_FILE" > /dev/null 2>&1 || true

  if [ -e "$POLLUTION_CHECK" ]; then
    echo -e "\n\nFOUND POLLUTER: $TEST_FILE"
    exit 1
  fi
done

echo -e "\nAll tests clean."
exit 0
