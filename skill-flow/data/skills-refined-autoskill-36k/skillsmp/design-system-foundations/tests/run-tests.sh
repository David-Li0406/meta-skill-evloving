#!/bin/bash
#
# Run all validation tests for design-system-foundations skill
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MIN_NODE_VERSION=14

# Check Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is required but not installed"
    echo "   Please install Node.js ${MIN_NODE_VERSION}+ from https://nodejs.org"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | sed 's/v//' | cut -d. -f1)
if [ "$NODE_VERSION" -lt "$MIN_NODE_VERSION" ]; then
    echo "⚠️  Warning: Node.js ${MIN_NODE_VERSION}+ recommended (found v$(node -v | sed 's/v//'))"
    echo "   Some features may not work correctly"
fi

# Install dependencies if package.json has any
if [ -f "$SCRIPT_DIR/package.json" ]; then
    # Check if node_modules exists, if not install
    if [ ! -d "$SCRIPT_DIR/node_modules" ]; then
        echo "📦 Installing dependencies..."
        npm install --prefix "$SCRIPT_DIR" --silent 2>/dev/null || true
    fi
fi

echo "🚀 Running Design System Foundations Skill Tests"
echo "================================================="
echo ""

TESTS=(
  "validate-skill.test.js"
  "validate-levels.test.js"
  "validate-agents.test.js"
  "validate-tokens.test.js"
  "validate-docs.test.js"
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

echo "================================================="
echo ""
echo "📊 Final Summary"
echo "   Tests run: ${#TESTS[@]}"
echo "   Passed: $PASSED"
echo "   Failed: $FAILED"
echo ""

# Output JSON summary for CI parsing (on a single line for easy grep)
LEVELS=$(node -e "try { console.log(require('./config.js').LEVEL_COUNT) } catch(e) { console.log(4) }" 2>/dev/null || echo "4")
AGENTS=$(node -e "try { const c = require('./config.js'); let total = 0; Object.values(c.EXPECTED_AGENTS_PER_LEVEL).forEach(a => total += a.length); console.log(total) } catch(e) { console.log(21) }" 2>/dev/null || echo "21")
echo "JSON_SUMMARY: {\"levels\":$LEVELS,\"agents\":$AGENTS,\"suites\":${#TESTS[@]},\"passed\":$PASSED,\"failed\":$FAILED}"

if [ $FAILED -gt 0 ]; then
  echo "❌ Some test suites failed"
  exit 1
else
  echo "✅ All test suites passed"
  exit 0
fi
