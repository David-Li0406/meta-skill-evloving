#!/bin/bash
# Full Code Review Script
# Usage: ./full-review.sh [directory]

set -e

PROJECT_ROOT="/Users/jietaoxie/my-prototype-logistics"
FRONTEND_DIR="$PROJECT_ROOT/frontend/CretasFoodTrace"
BACKEND_DIR="$PROJECT_ROOT/backend-java"
TARGET_DIR="${1:-$FRONTEND_DIR/src}"

echo "=========================================="
echo "  Cretas Code Review"
echo "=========================================="
echo "Target: $TARGET_DIR"
echo ""

# Function to count issues
count_issues() {
    local count="$1"
    local name="$2"
    if [ "$count" -gt 0 ]; then
        echo "  - $name: $count issues found"
    else
        echo "  - $name: PASS"
    fi
}

# 1. Anti-Pattern Check
echo "[1/5] Anti-Pattern Analysis..."
echo ""

AS_ANY_COUNT=$(grep -r "as any" "$TARGET_DIR" --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')
EMPTY_CATCH=$(grep -r "catch.*{" "$TARGET_DIR" --include="*.ts" --include="*.tsx" 2>/dev/null | grep -c "{ }" || echo 0)
TODO_COUNT=$(grep -r "TODO\|FIXME\|HACK" "$TARGET_DIR" --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')
OR_DEFAULT=$(grep -r "\|\| 0\|\| ''\|\| \[\]" "$TARGET_DIR" --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')

count_issues "$AS_ANY_COUNT" "as any type assertions"
count_issues "$EMPTY_CATCH" "Empty catch blocks"
count_issues "$TODO_COUNT" "TODO/FIXME comments"
count_issues "$OR_DEFAULT" "|| default values (should use ??)"

# 2. TypeScript Check
echo ""
echo "[2/5] TypeScript Strict Mode..."
if [ -d "$FRONTEND_DIR" ]; then
    cd "$FRONTEND_DIR"
    if npx tsc --noEmit --skipLibCheck 2>&1 | head -20; then
        echo "  TypeScript: PASS"
    else
        echo "  TypeScript: ISSUES FOUND (see above)"
    fi
else
    echo "  Skipped (frontend directory not found)"
fi

# 3. Security Check
echo ""
echo "[3/5] Security Analysis..."

ASYNC_TOKEN=$(grep -r "AsyncStorage.*token\|token.*AsyncStorage" "$TARGET_DIR" --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')
HARDCODED_KEY=$(grep -r "apiKey\s*=\s*['\"]" "$TARGET_DIR" --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')
CONSOLE_SENSITIVE=$(grep -r "console\.log.*password\|console\.log.*token" "$TARGET_DIR" --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')

count_issues "$ASYNC_TOKEN" "Token in AsyncStorage (insecure)"
count_issues "$HARDCODED_KEY" "Hardcoded API keys"
count_issues "$CONSOLE_SENSITIVE" "Sensitive data in console.log"

# 4. Code Complexity
echo ""
echo "[4/5] Code Complexity..."

LARGE_FILES=$(find "$TARGET_DIR" -name "*.ts" -o -name "*.tsx" 2>/dev/null | xargs wc -l 2>/dev/null | awk '$1 > 500 {print}' | wc -l | tr -d ' ')
DEEP_NESTING=$(grep -r "if.*if.*if\|\.then.*\.then.*\.then" "$TARGET_DIR" --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')

count_issues "$LARGE_FILES" "Files > 500 lines (consider splitting)"
count_issues "$DEEP_NESTING" "Deep nesting (> 3 levels)"

# 5. Summary
echo ""
echo "[5/5] Summary..."
TOTAL=$((AS_ANY_COUNT + EMPTY_CATCH + TODO_COUNT + ASYNC_TOKEN + HARDCODED_KEY))

echo ""
echo "=========================================="
if [ "$TOTAL" -gt 20 ]; then
    echo "  Review Result: NEEDS ATTENTION ($TOTAL issues)"
elif [ "$TOTAL" -gt 0 ]; then
    echo "  Review Result: ACCEPTABLE ($TOTAL minor issues)"
else
    echo "  Review Result: EXCELLENT (0 issues)"
fi
echo "=========================================="
echo ""
echo "Top files with 'as any' usage:"
grep -r "as any" "$TARGET_DIR" --include="*.ts" --include="*.tsx" 2>/dev/null | cut -d: -f1 | sort | uniq -c | sort -rn | head -5
