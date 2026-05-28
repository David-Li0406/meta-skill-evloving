#!/bin/bash
# Check code against dev_instruction_v3.md standards
# Usage: ./check-standards.sh [directory]

DIR="${1:-src}"

echo "🔍 Checking code standards in $DIR..."
echo ""

ISSUES=0

# Check for export default
echo "=== Checking for 'export default' ==="
DEFAULTS=$(grep -rn "export default" "$DIR" --include="*.tsx" --include="*.ts" 2>/dev/null || true)
if [ -n "$DEFAULTS" ]; then
    echo "❌ Found export default usage:"
    echo "$DEFAULTS"
    ISSUES=$((ISSUES + 1))
else
    echo "✅ No export default found"
fi
echo ""

# Check for onClick on potential HeroUI components
echo "=== Checking for 'onClick' on HeroUI components ==="
ONCLICKS=$(grep -rn "onClick=" "$DIR" --include="*.tsx" 2>/dev/null || true)
if [ -n "$ONCLICKS" ]; then
    echo "⚠️  Found onClick usage (verify these are not HeroUI components):"
    echo "$ONCLICKS"
    ISSUES=$((ISSUES + 1))
else
    echo "✅ No onClick found"
fi
echo ""

# Check for 'any' type
echo "=== Checking for 'any' type ==="
ANYS=$(grep -rn ": any" "$DIR" --include="*.tsx" --include="*.ts" 2>/dev/null || true)
if [ -n "$ANYS" ]; then
    echo "❌ Found 'any' type usage:"
    echo "$ANYS"
    ISSUES=$((ISSUES + 1))
else
    echo "✅ No 'any' types found"
fi
echo ""

# Check for use client
echo "=== Checking for 'use client' directive ==="
USECLIENT=$(grep -rn '"use client"' "$DIR" --include="*.tsx" --include="*.ts" 2>/dev/null || true)
if [ -n "$USECLIENT" ]; then
    echo "❌ Found 'use client' directive (not needed in Vite SPA):"
    echo "$USECLIENT"
    ISSUES=$((ISSUES + 1))
else
    echo "✅ No 'use client' directives found"
fi
echo ""

# Summary
echo "=== Summary ==="
if [ $ISSUES -eq 0 ]; then
    echo "✅ All checks passed!"
else
    echo "⚠️  Found $ISSUES potential issue(s). Review and fix before committing."
fi
