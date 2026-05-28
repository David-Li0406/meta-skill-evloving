#!/bin/bash
# Validate SKILL.md structure and content
# Usage: ./validate-skill.sh <skill-directory>

set -e

SKILL_DIR="${1:-.}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
ERRORS=0
WARNINGS=0

echo "🔍 Validating skill in: $SKILL_DIR"
echo ""

# Check if SKILL.md exists
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo -e "${RED}❌ SKILL.md not found${NC}"
    exit 1
fi

SKILL_FILE="$SKILL_DIR/SKILL.md"

# Extract frontmatter (lines between first two --- markers)
FRONTMATTER=$(sed -n '2,/^---$/p' "$SKILL_FILE" | sed '$d')

# Check required frontmatter fields
echo "📋 Checking YAML frontmatter..."

if ! echo "$FRONTMATTER" | grep -q "^name:"; then
    echo -e "${RED}❌ Missing 'name' field in frontmatter${NC}"
    ((ERRORS++))
else
    NAME=$(echo "$FRONTMATTER" | grep "^name:" | sed 's/name: *//')
    echo -e "${GREEN}✅ Name: $NAME${NC}"

    # Validate name format
    if [[ ! "$NAME" =~ ^[a-z0-9-]+$ ]]; then
        echo -e "${RED}❌ Name must be lowercase letters, numbers, and hyphens only${NC}"
        ((ERRORS++))
    fi

    # Check if name matches directory
    DIR_NAME=$(basename "$SKILL_DIR")
    if [ "$NAME" != "$DIR_NAME" ]; then
        echo -e "${YELLOW}⚠️  Name '$NAME' doesn't match directory '$DIR_NAME'${NC}"
        ((WARNINGS++))
    fi
fi

if ! echo "$FRONTMATTER" | grep -q "^description:"; then
    echo -e "${RED}❌ Missing 'description' field in frontmatter${NC}"
    ((ERRORS++))
else
    DESCRIPTION=$(echo "$FRONTMATTER" | grep "^description:" | sed 's/description: *//')
    echo -e "${GREEN}✅ Description present${NC}"

    # Check description length
    DESC_LENGTH=${#DESCRIPTION}
    if [ $DESC_LENGTH -gt 1024 ]; then
        echo -e "${RED}❌ Description too long ($DESC_LENGTH chars, max 1024)${NC}"
        ((ERRORS++))
    fi

    # Check for third person
    if echo "$DESCRIPTION" | grep -qi "you \|your \|I can\|I will"; then
        echo -e "${YELLOW}⚠️  Description should be in third person (avoid 'you', 'your', 'I can')${NC}"
        ((WARNINGS++))
    fi

    # Check for trigger phrases
    if ! echo "$DESCRIPTION" | grep -qi "this skill should be used when\|use when\|use this"; then
        echo -e "${YELLOW}⚠️  Description should include trigger phrases (when to use)${NC}"
        ((WARNINGS++))
    fi
fi

echo ""
echo "📝 Checking XML structure..."

# Check for required tags (skip first frontmatter block)
BODY=$(awk 'BEGIN {skip=1} /^---$/ && NR==1 {next} /^---$/ && skip==1 {skip=0; next} skip==0 {print}' "$SKILL_FILE")

if ! echo "$BODY" | grep -q "<objective>"; then
    echo -e "${RED}❌ Missing required tag: <objective>${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✅ <objective> tag present${NC}"
fi

if ! echo "$BODY" | grep -q "<quick_start>"; then
    echo -e "${RED}❌ Missing required tag: <quick_start>${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✅ <quick_start> tag present${NC}"
fi

if ! echo "$BODY" | grep -q "<success_criteria>\|<when_successful>"; then
    echo -e "${RED}❌ Missing required tag: <success_criteria> or <when_successful>${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✅ Success criteria tag present${NC}"
fi

# Check for markdown headings in body (anti-pattern, excluding code blocks)
# Use awk to track if we're inside code blocks
HEADINGS_OUTSIDE_CODE=$(awk '
/^```/ { in_code = !in_code; next }
!in_code && /^#+ / { print NR": "$0 }
' "$SKILL_FILE")

if [ -n "$HEADINGS_OUTSIDE_CODE" ]; then
    echo -e "${YELLOW}⚠️  Found markdown headings outside code blocks (should use XML tags)${NC}"
    ((WARNINGS++))
    echo "   Lines with markdown headings:"
    echo "$HEADINGS_OUTSIDE_CODE" | sed 's/^/   /'
fi

# Check for unclosed XML tags
OPEN_TAGS=$(echo "$BODY" | grep -o "<[a-z_][a-z_0-9]*>" | sort)
CLOSE_TAGS=$(echo "$BODY" | grep -o "</[a-z_][a-z_0-9]*>" | sed 's/<\///' | sed 's/>//' | sort)

if [ "$OPEN_TAGS" != "$CLOSE_TAGS" ]; then
    echo -e "${YELLOW}⚠️  Potentially unclosed XML tags detected${NC}"
    ((WARNINGS++))
fi

echo ""
echo "📁 Checking file organization..."

# Check line count
LINE_COUNT=$(wc -l < "$SKILL_FILE")
echo "   SKILL.md: $LINE_COUNT lines"

if [ $LINE_COUNT -gt 1000 ]; then
    echo -e "${YELLOW}⚠️  SKILL.md is long ($LINE_COUNT lines). Consider moving content to references/${NC}"
    ((WARNINGS++))
elif [ $LINE_COUNT -gt 500 ]; then
    echo -e "${YELLOW}⚠️  SKILL.md is getting long ($LINE_COUNT lines). Target: <500 lines${NC}"
    ((WARNINGS++))
fi

# Check for references directory
if [ -d "$SKILL_DIR/references" ]; then
    REF_COUNT=$(find "$SKILL_DIR/references" -name "*.md" | wc -l)
    echo -e "${GREEN}✅ references/ directory found ($REF_COUNT files)${NC}"

    # Check if references are mentioned in SKILL.md
    while IFS= read -r ref_file; do
        ref_name=$(basename "$ref_file")
        if ! grep -q "$ref_name" "$SKILL_FILE"; then
            echo -e "${YELLOW}⚠️  Reference file '$ref_name' not mentioned in SKILL.md${NC}"
            ((WARNINGS++))
        fi
    done < <(find "$SKILL_DIR/references" -name "*.md")
fi

# Check for scripts directory
if [ -d "$SKILL_DIR/scripts" ]; then
    SCRIPT_COUNT=$(find "$SKILL_DIR/scripts" -type f | wc -l)
    echo -e "${GREEN}✅ scripts/ directory found ($SCRIPT_COUNT files)${NC}"
fi

echo ""
echo "═══════════════════════════════════════"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ Skill validation passed!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Skill validation passed with $WARNINGS warning(s)${NC}"
    exit 0
else
    echo -e "${RED}❌ Skill validation failed with $ERRORS error(s) and $WARNINGS warning(s)${NC}"
    exit 1
fi
