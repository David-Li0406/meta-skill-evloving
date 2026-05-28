#!/bin/bash

# Bookmark Checker: TypeScript Type Check
# Verifies TypeScript compilation and type safety

set -e

# Navigate to project root (5 levels up from this script)
PROJECT_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$PROJECT_ROOT"

echo "[TYPE_CHECK] Starting TypeScript validation..."

ERRORS=0
WARNINGS=0

# Check if TypeScript is installed
if ! command -v npx &> /dev/null; then
  echo "ERROR: npx not found. Install Node.js first."
  exit 2
fi

# Check tsconfig.json exists
if [ ! -f "tsconfig.json" ]; then
  echo "ERROR: tsconfig.json not found"
  exit 2
fi

# Run TypeScript compiler in noEmit mode (don't generate files)
if npx tsc --noEmit 2>&1 | tee /tmp/tsc_output.txt; then
  echo "✅ TYPE_CHECK: PASS - No TypeScript errors"
  ERRORS=0
else
  ERRORS=$(grep -c "error TS" /tmp/tsc_output.txt 2>/dev/null || echo 0)
  WARNINGS=$(grep -c "warning TS" /tmp/tsc_output.txt 2>/dev/null || echo 0)
  echo "❌ TYPE_CHECK: FAIL - Found $ERRORS errors, $WARNINGS warnings"
  exit 1
fi

# Count any implicit any types
ANY_COUNT=$(grep -r ":\s*any\b" lib/ components/ hooks/ --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l || echo 0)

if [ "$ANY_COUNT" -gt 0 ]; then
  echo "⚠️ INFO: Found $ANY_COUNT instances of 'any' type (should be <5)"
  WARNINGS=$((WARNINGS + 1))
fi

# Report results
if [ $ERRORS -eq 0 ]; then
  echo "INFO: TypeScript compilation successful"
  echo "INFO: Warnings found: $WARNINGS"
  echo "INFO: 'any' type instances: $ANY_COUNT"
  exit 0
else
  echo "ERROR: TypeScript compilation failed with $ERRORS errors"
  exit 2
fi
