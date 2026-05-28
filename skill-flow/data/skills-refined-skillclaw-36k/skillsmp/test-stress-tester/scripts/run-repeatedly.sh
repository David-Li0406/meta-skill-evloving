#!/bin/bash

TEST_FILE=$1
ITERATIONS=${2:-5}
LOG_FILE="./.agent/skills/test-stress-tester/stress-test.log"

if [ -z "$TEST_FILE" ]; then
  echo "Usage: $0 <test-file> [iterations]"
  exit 1
fi

echo "Running stress test for: $TEST_FILE"
echo "Iterations: $ITERATIONS"
echo "--- Starting Stress Test $(date) ---" > "$LOG_FILE"

PASS_COUNT=0
FAIL_COUNT=0

for i in $(seq 1 $ITERATIONS); do
  echo -n "Iteration $i/$ITERATIONS: "
  npm test -- "$TEST_FILE" --run >> "$LOG_FILE" 2>&1
  if [ $? -eq 0 ]; then
    echo "✅ PASSED"
    ((PASS_COUNT++))
  else
    echo "❌ FAILED"
    ((FAIL_COUNT++))
  fi
done

echo "-----------------------------------"
echo "Stress Test Complete!"
echo "Total iterations: $ITERATIONS"
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"
echo "Success Rate: $(( (PASS_COUNT * 100) / ITERATIONS ))%"
echo "-----------------------------------"
echo "Detailed logs available at: $LOG_FILE"

if [ $FAIL_COUNT -gt 0 ]; then
  exit 1
fi
exit 0
