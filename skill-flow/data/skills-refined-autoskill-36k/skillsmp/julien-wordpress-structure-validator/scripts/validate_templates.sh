#!/bin/bash
# WordPress Template Structure Validator
# Validates FSE theme template structure and naming conventions

set -e

THEME_PATH=$1

if [ -z "$THEME_PATH" ]; then
    echo "Usage: $0 <path/to/theme>"
    exit 1
fi

if [ ! -d "$THEME_PATH" ]; then
    echo "Error: Theme path not found: $THEME_PATH"
    exit 1
fi

TEMPLATES_DIR="$THEME_PATH/templates"
PARTS_DIR="$THEME_PATH/parts"

echo "========================================"
echo "WordPress Template Structure Validator"
echo "========================================"
echo ""
echo "Theme: $THEME_PATH"
echo ""

# Counter for issues
ERRORS=0
WARNINGS=0

# ========================================
# 1. Check required directories
# ========================================

echo "=== Directory Structure ==="
echo ""

if [ ! -d "$TEMPLATES_DIR" ]; then
    echo "❌ ERROR: templates/ directory missing"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ templates/ directory found"
fi

if [ ! -d "$PARTS_DIR" ]; then
    echo "⚠️  WARNING: parts/ directory missing (recommended)"
    WARNINGS=$((WARNINGS + 1))
else
    echo "✅ parts/ directory found"
fi

echo ""

# ========================================
# 2. Check required templates
# ========================================

echo "=== Required Templates ==="
echo ""

# index.html is REQUIRED
if [ ! -f "$TEMPLATES_DIR/index.html" ]; then
    echo "❌ ERROR: index.html missing (REQUIRED fallback template)"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ index.html present (fallback)"
fi

echo ""

# ========================================
# 3. List all templates found
# ========================================

echo "=== Templates Found ==="
echo ""

if [ -d "$TEMPLATES_DIR" ]; then
    TEMPLATE_COUNT=$(find "$TEMPLATES_DIR" -name "*.html" -type f | wc -l)
    echo "Total templates: $TEMPLATE_COUNT"
    echo ""

    find "$TEMPLATES_DIR" -name "*.html" -type f | while read file; do
        filename=$(basename "$file")
        echo "  - $filename"
    done
    echo ""
fi

# ========================================
# 4. Validate template syntax
# ========================================

echo "=== Template Syntax Validation ==="
echo ""

if [ -d "$TEMPLATES_DIR" ]; then
    find "$TEMPLATES_DIR" -name "*.html" -type f | while read file; do
        filename=$(basename "$file")

        # Check for WordPress blocks
        if ! grep -q "<!-- wp:" "$file"; then
            echo "⚠️  WARNING: $filename contains no WordPress blocks"
            WARNINGS=$((WARNINGS + 1))
        fi

        # Check for unclosed blocks (basic check)
        OPEN_BLOCKS=$(grep -c "<!-- wp:" "$file" || echo 0)
        CLOSE_BLOCKS=$(grep -c "<!-- /wp:" "$file" || echo 0)

        if [ "$OPEN_BLOCKS" -ne "$CLOSE_BLOCKS" ]; then
            echo "⚠️  WARNING: $filename may have unclosed blocks (open: $OPEN_BLOCKS, close: $CLOSE_BLOCKS)"
            WARNINGS=$((WARNINGS + 1))
        fi

        # Check for header/footer template parts
        if ! grep -q "wp:template-part" "$file"; then
            echo "⚠️  WARNING: $filename missing template-part (header/footer)"
            WARNINGS=$((WARNINGS + 1))
        fi
    done
fi

echo ""

# ========================================
# 5. Check naming conventions
# ========================================

echo "=== Naming Convention Check ==="
echo ""

if [ -d "$TEMPLATES_DIR" ]; then
    # Check for common naming patterns
    find "$TEMPLATES_DIR" -name "*.html" -type f | while read file; do
        filename=$(basename "$file")

        # Valid patterns:
        # - index.html
        # - page.html, page-{slug}.html, page-{id}.html
        # - single.html, single-{type}.html
        # - front-page.html, home.html
        # - archive.html, category.html, tag.html
        # - search.html, 404.html

        case "$filename" in
            index.html|page.html|single.html|front-page.html|home.html|archive.html|search.html|404.html)
                echo "✅ $filename (standard template)"
                ;;
            page-*.html|single-*.html|archive-*.html|category-*.html|tag-*.html|author-*.html|taxonomy-*.html)
                echo "✅ $filename (custom template)"
                ;;
            *)
                echo "⚠️  WARNING: $filename unusual naming (may not be recognized by WordPress)"
                WARNINGS=$((WARNINGS + 1))
                ;;
        esac
    done
fi

echo ""

# ========================================
# 6. Check template parts
# ========================================

echo "=== Template Parts ==="
echo ""

if [ -d "$PARTS_DIR" ]; then
    PARTS_COUNT=$(find "$PARTS_DIR" -name "*.html" -type f | wc -l)
    echo "Total template parts: $PARTS_COUNT"
    echo ""

    # Check for common parts
    if [ -f "$PARTS_DIR/header.html" ]; then
        echo "✅ header.html present"
    else
        echo "⚠️  WARNING: header.html missing (recommended)"
        WARNINGS=$((WARNINGS + 1))
    fi

    if [ -f "$PARTS_DIR/footer.html" ]; then
        echo "✅ footer.html present"
    else
        echo "⚠️  WARNING: footer.html missing (recommended)"
        WARNINGS=$((WARNINGS + 1))
    fi

    # List all parts
    echo ""
    echo "Template parts found:"
    find "$PARTS_DIR" -name "*.html" -type f | while read file; do
        filename=$(basename "$file")
        echo "  - $filename"
    done
else
    echo "⚠️  WARNING: No template parts directory"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""

# ========================================
# 7. Summary
# ========================================

echo "========================================"
echo "Validation Summary"
echo "========================================"
echo ""
echo "Errors:   $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ All validations passed!"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "⚠️  Validation passed with warnings"
    exit 0
else
    echo "❌ Validation failed with errors"
    exit 1
fi
