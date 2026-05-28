#!/bin/bash
#
# Run all validation tests for orchestration framework
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Running Orchestration Framework Tests"
echo "========================================"
echo ""

# Validate required skills exist before running tests
echo "🔍 Checking required skills..."
VALIDATION_RESULT=$(node -e "
const { validateRequiredSkills } = require('./config.js');
const result = validateRequiredSkills();
if (!result.valid) {
  console.error('Missing required skills: ' + result.missing.join(', '));
  process.exit(1);
}
console.log('All required skills present');
" 2>&1)
VALIDATION_EXIT=$?

if [ $VALIDATION_EXIT -ne 0 ]; then
  echo "❌ $VALIDATION_RESULT"
  echo ""
  echo "Please ensure all required skills are installed:"
  echo "  - project-management (at .web-agency/skills/project-management/)"
  echo ""
  exit 1
fi
echo "✅ $VALIDATION_RESULT"
echo ""

TESTS=(
  "validate-framework-structure.test.js"
  "validate-agents.test.js"
  "validate-routing.test.js"
  "validate-templates.test.js"
  "validate-workflows.test.js"
  "validate-orchestrator-routing.test.js"
  "validate-template-generation.test.js"
  "validate-agent-examples.test.js"
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

echo "=================================="
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
