#!/bin/bash
# analyze-for-animations.sh
# Analyzes a codebase and outputs animation opportunities

echo "=== Animation Opportunity Analysis ==="
echo ""

# Check for package.json
if [ -f "package.json" ]; then
    echo "📦 Package.json found"
    
    # Check framework
    if grep -q '"react"' package.json; then
        echo "   Framework: React"
    elif grep -q '"vue"' package.json; then
        echo "   Framework: Vue"
    elif grep -q '"svelte"' package.json; then
        echo "   Framework: Svelte"
    elif grep -q '"@angular/core"' package.json; then
        echo "   Framework: Angular"
    else
        echo "   Framework: Unknown/Vanilla"
    fi
    
    # Check if animejs installed
    if grep -q '"animejs"' package.json; then
        echo "   ✅ anime.js is installed"
    else
        echo "   ❌ anime.js NOT installed"
        echo "      Run: npm install animejs"
    fi
    echo ""
fi

echo "=== P0: High Priority Opportunities ==="
echo ""

echo "🔄 Loading States:"
grep -rn --include="*.tsx" --include="*.jsx" --include="*.vue" -E "(isLoading|loading|Spinner|skeleton)" 2>/dev/null | head -10
echo ""

echo "📄 Page Transitions / Routes:"
grep -rn --include="*.tsx" --include="*.jsx" --include="*.vue" -E "(Route|router|navigate|useNavigate|Link)" 2>/dev/null | head -10
echo ""

echo "=== P1: Medium Priority Opportunities ==="
echo ""

echo "📋 Lists with .map():"
grep -rn --include="*.tsx" --include="*.jsx" --include="*.vue" "\.map(" 2>/dev/null | grep -iE "(item|card|row|list)" | head -10
echo ""

echo "🗃️ Modals / Dialogs / Drawers:"
grep -rn --include="*.tsx" --include="*.jsx" --include="*.vue" -E "(Modal|Dialog|Drawer|Sheet|Popover)" 2>/dev/null | head -10
echo ""

echo "📝 Form Submissions:"
grep -rn --include="*.tsx" --include="*.jsx" --include="*.vue" -E "(onSubmit|handleSubmit|form)" 2>/dev/null | head -10
echo ""

echo "=== P2: Enhancement Opportunities ==="
echo ""

echo "🔘 Buttons:"
grep -rn --include="*.tsx" --include="*.jsx" --include="*.vue" -E "(<button|<Button|onClick)" 2>/dev/null | head -10
echo ""

echo "🃏 Cards / Tiles:"
grep -rn --include="*.tsx" --include="*.jsx" --include="*.vue" -E "(Card|Tile|className=\"card)" 2>/dev/null | head -10
echo ""

echo "📊 Data Displays (numbers, stats):"
grep -rn --include="*.tsx" --include="*.jsx" --include="*.vue" -E "(stat|metric|count|total|number)" 2>/dev/null | head -10
echo ""

echo "=== P3: Polish Opportunities ==="
echo ""

echo "🎯 Icons:"
grep -rn --include="*.tsx" --include="*.jsx" --include="*.vue" -E "(Icon|<svg|lucide)" 2>/dev/null | head -5
echo ""

echo "💬 Tooltips / Popovers:"
grep -rn --include="*.tsx" --include="*.jsx" --include="*.vue" -E "(Tooltip|Popover|title=)" 2>/dev/null | head -5
echo ""

echo "=== Component Files Found ==="
echo ""
find . -type f \( -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" \) -path "*/components/*" 2>/dev/null | head -20

echo ""
echo "=== Analysis Complete ==="
