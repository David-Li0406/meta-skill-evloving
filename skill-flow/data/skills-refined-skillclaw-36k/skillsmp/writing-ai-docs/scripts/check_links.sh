#!/bin/bash

# Check for broken links in markdown files using markdown-link-check
# Uses npx for zero-install convenience
#
# Usage:
#   bash scripts/check_links.sh <file-or-pattern> [file-or-pattern...]
#
# Examples:
#   bash scripts/check_links.sh README.md
#   bash scripts/check_links.sh SKILL.md references/*.md
#   bash scripts/check_links.sh "**/*.md"
#   bash scripts/check_links.sh templates/api-endpoint.md templates/tutorial.md

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Config file path
CONFIG_FILE="$PROJECT_ROOT/.markdown-link-check.json"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔗 Checking Links in Markdown Files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $# -eq 0 ]; then
    echo -e "${RED}Error: No files specified${NC}"
    echo ""
    echo "Usage: bash scripts/check_links.sh <file-or-pattern> [file-or-pattern...]"
    echo ""
    echo "Examples:"
    echo "  bash scripts/check_links.sh README.md"
    echo "  bash scripts/check_links.sh SKILL.md references/*.md"
    echo '  bash scripts/check_links.sh "**/*.md"'
    echo "  bash scripts/check_links.sh templates/api-endpoint.md templates/tutorial.md"
    exit 1
fi

# Check if config file exists
if [ -f "$CONFIG_FILE" ]; then
    echo -e "${GREEN}✓${NC} Using config: .markdown-link-check.json"
    CONFIG_OPTION="--config $CONFIG_FILE"
else
    echo -e "${YELLOW}⚠${NC} No config file found (.markdown-link-check.json)"
    CONFIG_OPTION=""
fi

echo ""

# Collect all files to check
FILES=()
for pattern in "$@"; do
    # If pattern contains glob characters, expand it
    if [[ "$pattern" == *"*"* ]]; then
        # Use find for glob patterns
        while IFS= read -r -d '' file; do
            FILES+=("$file")
        done < <(find "$PROJECT_ROOT" -path "$PROJECT_ROOT/$pattern" -type f -print0 2>/dev/null || true)
    else
        # Direct file path
        if [ -f "$pattern" ]; then
            FILES+=("$pattern")
        elif [ -f "$PROJECT_ROOT/$pattern" ]; then
            FILES+=("$PROJECT_ROOT/$pattern")
        else
            echo -e "${YELLOW}⚠${NC} File not found: $pattern (skipping)"
        fi
    fi
done

if [ ${#FILES[@]} -eq 0 ]; then
    echo -e "${RED}✗ No files found to check${NC}"
    exit 1
fi

echo "Found ${#FILES[@]} file(s) to check"
echo ""

# Track results
TOTAL_FILES=0
PASSED_FILES=0
FAILED_FILES=0

# Check each file
for file in "${FILES[@]}"; do
    TOTAL_FILES=$((TOTAL_FILES + 1))

    # Get relative path for display
    REL_PATH="${file#$PROJECT_ROOT/}"

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Checking: $REL_PATH"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Run markdown-link-check
    if npx markdown-link-check $CONFIG_OPTION "$file"; then
        PASSED_FILES=$((PASSED_FILES + 1))
        echo -e "${GREEN}✓ All links valid${NC}"
    else
        FAILED_FILES=$((FAILED_FILES + 1))
        echo -e "${RED}✗ Broken links found${NC}"
    fi

    echo ""
done

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Total files checked: $TOTAL_FILES"
echo -e "${GREEN}Passed: $PASSED_FILES${NC}"
if [ $FAILED_FILES -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED_FILES${NC}"
else
    echo -e "Failed: 0"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAILED_FILES -gt 0 ]; then
    exit 1
else
    echo -e "${GREEN}✓ All links are valid!${NC}"
    exit 0
fi
