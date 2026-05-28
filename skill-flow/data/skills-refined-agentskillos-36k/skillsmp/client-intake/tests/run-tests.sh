#!/bin/bash
#
# Run all validation tests for client-intake skill
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Running Client Intake Skill Tests"
echo "====================================="
echo ""

TESTS=(
  "validate-agents.test.js"
  "validate-domains.test.js"
  "validate-routing.test.js"
)

PASSED=0
FAILED=0

for test in "${TESTS[@]}"; do
  echo "▶ Running $test..."
  echo ""

  if node "$SCRIPT_DIR/$test"; then
    PASSED=$((PASSED + 1))
  else
    FAILED=$((FAILED + 1))
  fi

  echo ""
done

echo "====================================="
echo ""
echo "📊 Final Summary"
echo "   Tests run: ${#TESTS[@]}"
echo "   Passed: $PASSED"
echo "   Failed: $FAILED"
echo ""

if [ $FAILED -gt 0 ]; then
  echo "❌ Some test suites failed"
  exit 1
else
  echo "✅ All test suites passed"
  exit 0
fi
