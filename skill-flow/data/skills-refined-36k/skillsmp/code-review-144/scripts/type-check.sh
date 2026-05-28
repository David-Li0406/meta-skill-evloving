#!/bin/bash
# TypeScript Type Safety Check
# Usage: ./type-check.sh [file|directory]

PROJECT_ROOT="/Users/jietaoxie/my-prototype-logistics"
FRONTEND_DIR="$PROJECT_ROOT/frontend/CretasFoodTrace"
TARGET="${1:-}"

echo "=========================================="
echo "  TypeScript Type Safety Check"
echo "=========================================="

cd "$FRONTEND_DIR" || exit 1

# If specific file provided, check only that file
if [ -n "$TARGET" ]; then
    echo "Target: $TARGET"
    echo ""
    npx tsc --noEmit --skipLibCheck "$TARGET" 2>&1
    exit $?
fi

# Full project check
echo "Running full TypeScript check..."
echo ""

# Run tsc and capture output
TSC_OUTPUT=$(npx tsc --noEmit --skipLibCheck 2>&1)
TSC_EXIT=$?

if [ $TSC_EXIT -eq 0 ]; then
    echo "TypeScript: ALL PASSED"
else
    # Count errors
    ERROR_COUNT=$(echo "$TSC_OUTPUT" | grep -c "error TS")

    echo "TypeScript: $ERROR_COUNT ERRORS FOUND"
    echo ""

    # Show first 30 errors
    echo "$TSC_OUTPUT" | head -50

    if [ "$ERROR_COUNT" -gt 50 ]; then
        echo ""
        echo "... and $((ERROR_COUNT - 50)) more errors"
    fi
fi

echo ""
echo "=========================================="

# Additional checks
echo ""
echo "Additional Analysis:"
echo ""

# Count 'as any' usage
AS_ANY=$(grep -r "as any" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')
echo "  - 'as any' usage: $AS_ANY occurrences"

# Count 'any' type annotations
ANY_TYPE=$(grep -r ": any" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')
echo "  - ': any' type annotations: $ANY_TYPE occurrences"

# Files with most type issues
echo ""
echo "Files with most 'as any' usage:"
grep -r "as any" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | cut -d: -f1 | sort | uniq -c | sort -rn | head -5

exit $TSC_EXIT
