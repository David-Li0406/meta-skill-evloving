#!/bin/bash

# Run validation tests for backend-developer skill
# Usage: ./run-tests.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🧪 Running backend-developer skill validation tests..."
echo ""

node "$SCRIPT_DIR/validate-agents.test.js"

echo "Done!"
