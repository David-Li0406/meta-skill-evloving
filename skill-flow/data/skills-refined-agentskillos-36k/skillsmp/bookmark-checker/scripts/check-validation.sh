#!/bin/bash

# Bookmark Checker: Validation Schema Check
# Verifies Zod schema coverage and type alignment

set -e

# Navigate to project root
PROJECT_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$PROJECT_ROOT"

echo "[VALIDATION_CHECK] Starting schema coverage validation..."

ISSUES=0
MISSING_SCHEMAS=0

# Check files exist
if [ ! -f "lib/types.ts" ]; then
  echo "ERROR: lib/types.ts not found"
  exit 2
fi

if [ ! -f "lib/validation.ts" ]; then
  echo "ERROR: lib/validation.ts not found"
  exit 2
fi

echo "Analyzing type and schema alignment..."
echo ""

# Extract type definitions
echo "📋 Type Definitions in lib/types.ts:"
TYPES=$(grep -E "^(export )?(interface|type)" lib/types.ts | sed 's/export //g' | sed 's/ {.*//' | wc -l)
echo "  Found $TYPES type definitions"

# Extract schema definitions
echo ""
echo "✓ Zod Schemas in lib/validation.ts:"
SCHEMAS=$(grep -E "^export const.*Schema = z\." lib/validation.ts | wc -l)
echo "  Found $SCHEMAS Zod schemas"

# List specific schemas
echo ""
echo "  Schema list:"
grep -E "^export const.*Schema = z\." lib/validation.ts | sed 's/export const //g' | sed 's/ =.*//' | sed 's/^/    - /' | head -20

# Check for specific critical types
echo ""
echo "🔍 Critical Type Checks:"

CRITICAL_TYPES=("Bookmark" "Space" "PinnedView" "VaultKeyEnvelope" "EncryptedRecord" "SyncConflict")
CRITICAL_SCHEMAS=("BookmarkSchema" "SpaceSchema" "PinnedViewSchema" "VaultKeyEnvelopeSchema" "EncryptedRecordSchema" "SyncConflictSchema")

for i in "${!CRITICAL_TYPES[@]}"; do
  TYPE="${CRITICAL_TYPES[$i]}"
  SCHEMA="${CRITICAL_SCHEMAS[$i]}"

  # Check if type exists
  if grep -q "^export.*\b$TYPE\b" lib/types.ts; then
    if grep -q "^export const $SCHEMA" lib/validation.ts; then
      echo "  ✅ $TYPE → has schema"
    else
      echo "  ❌ $TYPE → MISSING schema"
      MISSING_SCHEMAS=$((MISSING_SCHEMAS + 1))
      ISSUES=$((ISSUES + 1))
    fi
  fi
done

# Coverage calculation
if [ "$TYPES" -gt 0 ]; then
  COVERAGE=$((SCHEMAS * 100 / TYPES))
  echo ""
  echo "📊 Schema Coverage: $SCHEMAS/$TYPES schemas ($COVERAGE%)"

  if [ "$COVERAGE" -ge 80 ]; then
    echo "  ✅ TARGET: Coverage above 80%"
  elif [ "$COVERAGE" -ge 50 ]; then
    echo "  ⚠️ TARGET: Coverage below 80% (at $COVERAGE%)"
    ISSUES=$((ISSUES + 1))
  else
    echo "  ❌ TARGET: Coverage critically low (at $COVERAGE%)"
    ISSUES=$((ISSUES + 1))
  fi
fi

# Check for validation patterns in components
echo ""
echo "🔎 Validation Pattern Check:"
VALIDATION_USAGE=$(grep -r "\.safeParse\|\.parse\|Schema\." components/ --include="*.tsx" --include="*.ts" 2>/dev/null | wc -l || echo 0)
echo "  Validation calls in components: $VALIDATION_USAGE"

if [ "$VALIDATION_USAGE" -lt 5 ]; then
  echo "  ⚠️ Low validation usage in components"
fi

# Check for untyped data sources
echo ""
echo "⚠️ Data Source Type Checks:"
ANY_UNTYPED=$(grep -r ": any\b" lib/ components/ --include="*.ts" --include="*.tsx" | grep -v "// " | wc -l || echo 0)
echo "  Untyped (any) instances: $ANY_UNTYPED"

if [ "$ANY_UNTYPED" -gt 10 ]; then
  echo "  ❌ Excessive use of 'any' type"
  ISSUES=$((ISSUES + 1))
elif [ "$ANY_UNTYPED" -gt 0 ]; then
  echo "  ⚠️ Some 'any' types present (try to reduce)"
fi

echo ""
echo "Summary:"
echo "  Total issues: $ISSUES"
echo "  Missing critical schemas: $MISSING_SCHEMAS"

if [ "$ISSUES" -eq 0 ]; then
  echo ""
  echo "✅ VALIDATION_CHECK: PASS"
  exit 0
elif [ "$MISSING_SCHEMAS" -gt 0 ] && [ "$MISSING_SCHEMAS" -gt 3 ]; then
  echo ""
  echo "❌ VALIDATION_CHECK: FAIL - Too many missing schemas"
  exit 2
else
  echo ""
  echo "⚠️ VALIDATION_CHECK: WARN - Review validation coverage"
  exit 1
fi
