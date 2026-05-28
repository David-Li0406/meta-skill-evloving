#!/bin/bash

# Bookmark Checker: Component Structure Check
# Validates component sizes, props interfaces, and naming conventions

set -e

# Navigate to project root
PROJECT_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$PROJECT_ROOT"

echo "[COMPONENT_CHECK] Starting component validation..."

ISSUES=0
OVERSIZED=0
MISSING_USE_CLIENT=0
TOTAL_COMPONENTS=0
COMPONENTS_CHECKED=0
TOTAL_LINES=0

# Define size limits
MAX_COMPONENT_SIZE=200  # lines (warning at 100, error at 200)
RECOMMENDED_SIZE=100

# Check components directory exists
if [ ! -d "components" ]; then
  echo "ERROR: components/ directory not found"
  exit 2
fi

echo "Analyzing components in components/ directory..."

# Analyze each component file
for file in $(find components -name "*.tsx" -o -name "*.ts" | grep -v ".test" | grep -v ".spec"); do
  if [ -f "$file" ]; then
    TOTAL_COMPONENTS=$((TOTAL_COMPONENTS + 1))
    LINES=$(wc -l < "$file")
    TOTAL_LINES=$((TOTAL_LINES + LINES))

    # Check for "use client" directive in components that touch localStorage
    if grep -q "localStorage\|sessionStorage\|window\." "$file" 2>/dev/null; then
      if ! grep -q '"use client"' "$file"; then
        echo "WARN: $file accesses browser APIs but missing \"use client\" directive"
        MISSING_USE_CLIENT=$((MISSING_USE_CLIENT + 1))
        ISSUES=$((ISSUES + 1))
      fi
    fi

    # Check component size
    if [ "$LINES" -gt "$MAX_COMPONENT_SIZE" ]; then
      echo "ERROR: $file has $LINES lines (max $MAX_COMPONENT_SIZE)"
      OVERSIZED=$((OVERSIZED + 1))
      ISSUES=$((ISSUES + 1))
    elif [ "$LINES" -gt "$RECOMMENDED_SIZE" ]; then
      echo "WARN: $file has $LINES lines (recommended <$RECOMMENDED_SIZE)"
      ISSUES=$((ISSUES + 1))
    fi

    # Check for Props interface
    BASENAME=$(basename "$file")
    if grep -q "interface.*Props\|type.*Props" "$file"; then
      :  # Props interface found, good
    else
      # Only warn if component has function signature
      if grep -q "export.*function\|export.*default" "$file"; then
        if [ "$LINES" -gt 30 ]; then
          echo "WARN: $file exports component but no Props interface found"
          ISSUES=$((ISSUES + 1))
        fi
      fi
    fi

    COMPONENTS_CHECKED=$((COMPONENTS_CHECKED + 1))
  fi
done

# Calculate statistics
if [ "$COMPONENTS_CHECKED" -gt 0 ]; then
  AVG_SIZE=$((TOTAL_LINES / COMPONENTS_CHECKED))
  SMALL_COMPONENTS=$(find components -name "*.tsx" -o -name "*.ts" | xargs wc -l 2>/dev/null | awk -v size="$RECOMMENDED_SIZE" '$1 < size {count++} END {print count}' || echo 0)
  UNDERSIZED_PCT=$((SMALL_COMPONENTS * 100 / COMPONENTS_CHECKED))

  echo ""
  echo "📊 Component Statistics:"
  echo "  Total components: $COMPONENTS_CHECKED"
  echo "  Total lines: $TOTAL_LINES"
  echo "  Average size: $AVG_SIZE lines"
  echo "  Components <$RECOMMENDED_SIZE lines: $UNDERSIZED_PCT%"
  echo ""

  if [ "$UNDERSIZED_PCT" -ge 70 ]; then
    echo "✅ TARGET: $UNDERSIZED_PCT% components under $RECOMMENDED_SIZE lines (target: 70%+)"
  else
    echo "⚠️ TARGET: Only $UNDERSIZED_PCT% under $RECOMMENDED_SIZE lines (target: 70%+)"
  fi
fi

echo ""
echo "Component Issues Summary:"
echo "  Oversized components (>$MAX_COMPONENT_SIZE lines): $OVERSIZED"
echo "  Missing 'use client' directive: $MISSING_USE_CLIENT"
echo "  Total issues found: $ISSUES"

if [ "$ISSUES" -eq 0 ]; then
  echo ""
  echo "✅ COMPONENT_CHECK: PASS"
  exit 0
elif [ "$OVERSIZED" -gt 0 ]; then
  echo ""
  echo "❌ COMPONENT_CHECK: FAIL - Found $OVERSIZED oversized components"
  exit 2
else
  echo ""
  echo "⚠️ COMPONENT_CHECK: WARN - Found $ISSUES issues"
  exit 1
fi
