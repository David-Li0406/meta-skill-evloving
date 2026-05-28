#!/bin/bash
#
# Run all Testing Process skill validation tests
#
# Usage: ./run-tests.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=================================================="
echo "  Testing Process Skill - Validation Tests"
echo "=================================================="

# Run all tests
echo ""
echo "Running agent validation..."
node validate-agents.test.js

echo ""
echo "Running domain validation..."
node validate-domains.test.js

echo ""
echo "Running routing validation..."
node validate-routing.test.js

echo ""
echo "Running markdown validation..."
node validate-markdown.test.js

echo ""
echo "=================================================="
echo "  All tests completed successfully!"
echo "=================================================="
