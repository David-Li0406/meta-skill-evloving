#!/bin/bash
# WordPress Block Styles Checker
# Analyzes registered block styles in functions.php

set -e

THEME_PATH=$1

if [ -z "$THEME_PATH" ]; then
    echo "Usage: $0 <path/to/theme>"
    exit 1
fi

FUNCTIONS_PHP="$THEME_PATH/functions.php"

if [ ! -f "$FUNCTIONS_PHP" ]; then
    echo "Error: functions.php not found at $THEME_PATH"
    exit 1
fi

echo "========================================"
echo "WordPress Block Styles Checker"
echo "========================================"
echo ""
echo "Theme: $THEME_PATH"
echo ""

ERRORS=0
WARNINGS=0

# ========================================
# 1. Check if register_block_style exists
# ========================================

echo "=== Block Styles Registration ==="
echo ""

if ! grep -q "register_block_style" "$FUNCTIONS_PHP"; then
    echo "⚠️  WARNING: No block styles registered"
    WARNINGS=$((WARNINGS + 1))
else
    # Count registered block styles
    STYLE_COUNT=$(grep -c "register_block_style" "$FUNCTIONS_PHP" || echo 0)
    echo "✅ Block styles found: $STYLE_COUNT registrations"
    echo ""

    # Extract and list block styles
    echo "Registered block styles:"
    echo ""

    # Parse function calls (simplified)
    grep -A 3 "register_block_style" "$FUNCTIONS_PHP" | grep "'name'" | sed "s/.*'name'.*=> *'\([^']*\)'.*/  - \1/" | sort -u

    echo ""
fi

# ========================================
# 2. Check naming conventions
# ========================================

echo "=== Naming Convention Check ==="
echo ""

# Extract style names
STYLE_NAMES=$(grep -A 3 "register_block_style" "$FUNCTIONS_PHP" | grep "'name'" | sed "s/.*'name'.*=> *'\([^']*\)'.*/\1/" || echo "")

if [ -n "$STYLE_NAMES" ]; then
    while IFS= read -r style_name; do
        # Check for kebab-case (recommended)
        if [[ "$style_name" =~ ^[a-z]+(-[a-z]+)*$ ]]; then
            echo "✅ $style_name (kebab-case)"
        else
            echo "⚠️  WARNING: $style_name (should use kebab-case)"
            WARNINGS=$((WARNINGS + 1))
        fi
    done <<< "$STYLE_NAMES"
else
    echo "No styles to check"
fi

echo ""

# ========================================
# 3. Check for inline styles vs external CSS
# ========================================

echo "=== Style Implementation ==="
echo ""

INLINE_STYLES=$(grep -c "'inline_style'" "$FUNCTIONS_PHP" || echo 0)
EXTERNAL_CSS=$(grep -c "wp_enqueue_block_style" "$FUNCTIONS_PHP" || echo 0)

echo "Inline styles: $INLINE_STYLES"
echo "External CSS files: $EXTERNAL_CSS"
echo ""

if [ "$INLINE_STYLES" -gt 10 ]; then
    echo "⚠️  WARNING: Many inline styles ($INLINE_STYLES). Consider using external CSS files for complex styles."
    WARNINGS=$((WARNINGS + 1))
fi

# ========================================
# 4. Check for common block types
# ========================================

echo "=== Block Types Used ==="
echo ""

# Common core blocks
BLOCKS=("core/heading" "core/paragraph" "core/group" "core/button" "core/image" "core/columns" "core/column")

for block in "${BLOCKS[@]}"; do
    if grep -q "'$block'" "$FUNCTIONS_PHP"; then
        echo "✅ $block has custom styles"
    fi
done

echo ""

# ========================================
# 5. Check for unused enqueued styles
# ========================================

echo "=== CSS File Usage ==="
echo ""

# Find all wp_enqueue_style calls
ENQUEUED_FILES=$(grep "wp_enqueue_style" "$FUNCTIONS_PHP" | grep -o "get_template_directory_uri.*\.css" | sed "s/.*'\([^']*\.css\)'.*/\1/" || echo "")

if [ -n "$ENQUEUED_FILES" ]; then
    echo "Enqueued CSS files:"
    echo ""

    while IFS= read -r css_file; do
        # Extract just the filename
        filename=$(basename "$css_file")
        full_path="$THEME_PATH/$css_file"

        if [ -f "$full_path" ]; then
            size=$(du -h "$full_path" | cut -f1)
            echo "  ✅ $filename ($size)"
        else
            echo "  ❌ $filename (FILE NOT FOUND)"
            ERRORS=$((ERRORS + 1))
        fi
    done <<< "$ENQUEUED_FILES"
else
    echo "No CSS files enqueued via wp_enqueue_style"
fi

echo ""

# ========================================
# 6. Check for version numbers (cache busting)
# ========================================

echo "=== Version Management ==="
echo ""

# Check if versions are used in enqueue calls
if grep -q "wp_enqueue_style.*'[0-9]" "$FUNCTIONS_PHP"; then
    echo "✅ Versions defined for cache busting"
else
    echo "⚠️  WARNING: No version numbers found. Consider adding versions for cache busting."
    WARNINGS=$((WARNINGS + 1))
fi

# Check if wp_get_theme()->get('Version') is used
if grep -q "wp_get_theme.*Version" "$FUNCTIONS_PHP"; then
    echo "✅ Dynamic versioning from theme version"
fi

echo ""

# ========================================
# 7. Check file permissions (if running with Docker access)
# ========================================

echo "=== File Permissions ==="
echo ""

PERMS=$(stat -c "%a" "$FUNCTIONS_PHP" 2>/dev/null || stat -f "%OLp" "$FUNCTIONS_PHP" 2>/dev/null || echo "unknown")

if [ "$PERMS" = "644" ]; then
    echo "✅ functions.php permissions: 644 (correct)"
elif [ "$PERMS" = "unknown" ]; then
    echo "⚠️  Could not check permissions"
else
    echo "⚠️  WARNING: functions.php permissions: $PERMS (recommended: 644)"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""

# ========================================
# Summary
# ========================================

echo "========================================"
echo "Validation Summary"
echo "========================================"
echo ""
echo "Errors:   $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ All checks passed!"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "⚠️  Passed with warnings"
    exit 0
else
    echo "❌ Failed with errors"
    exit 1
fi
