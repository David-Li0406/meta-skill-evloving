#!/bin/bash
#
# reviewer.sh - Review PRP for completeness and quality
#
# Usage: ./agents/reviewer.sh <prp-file> [--output <dir>]
#
# Outputs:
#   - review.json with status, score, issues, and suggestions

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESIGN_OPS_ROOT="$(dirname "$SCRIPT_DIR")"

# Defaults
PRP_FILE=""
OUTPUT_DIR="."
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 <prp-file> [--output <dir>]"
            exit 0
            ;;
        -*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            PRP_FILE="$1"
            shift
            ;;
    esac
done

if [[ -z "$PRP_FILE" ]] || [[ ! -f "$PRP_FILE" ]]; then
    echo -e "${RED}Error: Valid PRP file required${NC}"
    exit 1
fi

echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  PRP REVIEWER - Quality Gate Check${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}PRP:${NC} $PRP_FILE"
echo ""

CONTENT=$(cat "$PRP_FILE")

# Arrays for tracking
declare -a ISSUES
declare -a SUGGESTIONS
declare -a PASSED

SCORE=100
ERRORS=0
WARNINGS=0

# ============================================================================
# SECTION 1: Required Sections Check
# ============================================================================
echo -e "${YELLOW}[1/5] Checking required sections...${NC}"

REQUIRED_SECTIONS=(
    "Context"
    "Validation Summary"
    "Requirements"
    "Scope"
    "Implementation Plan"
    "Testing Strategy"
    "Risk Assessment"
    "Validation Commands"
    "Recommended Thinking Level"
    "State Transitions"
)

for section in "${REQUIRED_SECTIONS[@]}"; do
    if echo "$CONTENT" | grep -qiE "^##.*$section"; then
        PASSED+=("Has section: $section")
        [[ "$VERBOSE" == "true" ]] && echo -e "  ${GREEN}✓${NC} $section"
    else
        ISSUES+=("Missing required section: $section")
        ((SCORE-=5))
        ((ERRORS++))
        [[ "$VERBOSE" == "true" ]] && echo -e "  ${RED}✗${NC} $section"
    fi
done

echo -e "  Checked ${#REQUIRED_SECTIONS[@]} required sections"

# ============================================================================
# SECTION 2: Placeholder Detection
# ============================================================================
echo -e "${YELLOW}[2/5] Checking for placeholders...${NC}"

# Check for common placeholder patterns
PLACEHOLDER_PATTERNS=(
    "<!-- .* -->"
    "TBD"
    "TODO"
    "\[.*\]"
    "PLACEHOLDER"
    "XXX"
)

PLACEHOLDER_COUNT=0
for pattern in "${PLACEHOLDER_PATTERNS[@]}"; do
    count=$(echo "$CONTENT" | grep -cE "$pattern" || true)
    PLACEHOLDER_COUNT=$((PLACEHOLDER_COUNT + count))
done

# HTML comments are expected, so only count other placeholders
COMMENT_COUNT=$(echo "$CONTENT" | grep -cE "<!-- .* -->" || true)
REAL_PLACEHOLDERS=$((PLACEHOLDER_COUNT - COMMENT_COUNT))

if [[ $REAL_PLACEHOLDERS -gt 10 ]]; then
    ISSUES+=("Too many placeholders remaining: $REAL_PLACEHOLDERS")
    ((SCORE-=15))
    ((ERRORS++))
elif [[ $REAL_PLACEHOLDERS -gt 5 ]]; then
    SUGGESTIONS+=("Reduce placeholder count: $REAL_PLACEHOLDERS remaining")
    ((SCORE-=5))
    ((WARNINGS++))
elif [[ $REAL_PLACEHOLDERS -gt 0 ]]; then
    SUGGESTIONS+=("Minor placeholders remaining: $REAL_PLACEHOLDERS")
    ((WARNINGS++))
else
    PASSED+=("No significant placeholders")
fi

echo -e "  Found $REAL_PLACEHOLDERS placeholders (excluding HTML comments)"

# ============================================================================
# SECTION 3: Validation Commands Check
# ============================================================================
echo -e "${YELLOW}[3/5] Checking validation commands...${NC}"

# Check for bash code blocks
BASH_BLOCKS=$(echo "$CONTENT" | grep -c '```bash' || true)

if [[ $BASH_BLOCKS -ge 4 ]]; then
    PASSED+=("Has adequate validation commands ($BASH_BLOCKS blocks)")
    [[ "$VERBOSE" == "true" ]] && echo -e "  ${GREEN}✓${NC} Found $BASH_BLOCKS bash blocks"
elif [[ $BASH_BLOCKS -ge 2 ]]; then
    SUGGESTIONS+=("Consider adding more validation commands (only $BASH_BLOCKS blocks)")
    ((WARNINGS++))
    [[ "$VERBOSE" == "true" ]] && echo -e "  ${YELLOW}!${NC} Only $BASH_BLOCKS bash blocks"
else
    ISSUES+=("Insufficient validation commands (only $BASH_BLOCKS blocks)")
    ((SCORE-=10))
    ((ERRORS++))
    [[ "$VERBOSE" == "true" ]] && echo -e "  ${RED}✗${NC} Only $BASH_BLOCKS bash blocks"
fi

# Check for actual commands in bash blocks
if echo "$CONTENT" | grep -qE "npm (test|run|build)|pytest|go test|curl|make"; then
    PASSED+=("Contains executable commands")
else
    SUGGESTIONS+=("Validation commands should contain actual executable commands")
    ((WARNINGS++))
fi

# ============================================================================
# SECTION 4: Confidence and Thinking Level
# ============================================================================
echo -e "${YELLOW}[4/5] Checking confidence and thinking level...${NC}"

# Check for confidence score
if echo "$CONTENT" | grep -qE "Confidence.*[0-9]+%"; then
    PASSED+=("Has confidence score")
    [[ "$VERBOSE" == "true" ]] && echo -e "  ${GREEN}✓${NC} Has confidence score"
else
    ISSUES+=("Missing confidence score")
    ((SCORE-=5))
    ((ERRORS++))
    [[ "$VERBOSE" == "true" ]] && echo -e "  ${RED}✗${NC} Missing confidence score"
fi

# Check for thinking level
if echo "$CONTENT" | grep -qiE "Thinking Level.*(Normal|Think|Ultrathink)"; then
    PASSED+=("Has thinking level")
    [[ "$VERBOSE" == "true" ]] && echo -e "  ${GREEN}✓${NC} Has thinking level"
else
    ISSUES+=("Missing thinking level recommendation")
    ((SCORE-=5))
    ((ERRORS++))
    [[ "$VERBOSE" == "true" ]] && echo -e "  ${RED}✗${NC} Missing thinking level"
fi

# ============================================================================
# SECTION 5: State Transitions and Execution Log
# ============================================================================
echo -e "${YELLOW}[5/5] Checking state transitions and log...${NC}"

# Check state transitions table
if echo "$CONTENT" | grep -qE "\| *State *\|.*\|"; then
    PASSED+=("Has state transitions table")
    [[ "$VERBOSE" == "true" ]] && echo -e "  ${GREEN}✓${NC} Has state transitions"
else
    SUGGESTIONS+=("Consider adding state transitions table")
    ((WARNINGS++))
fi

# Check execution log
if echo "$CONTENT" | grep -qE "\| *Date *\|.*Action"; then
    PASSED+=("Has execution log")
    [[ "$VERBOSE" == "true" ]] && echo -e "  ${GREEN}✓${NC} Has execution log"
else
    SUGGESTIONS+=("Consider initializing execution log")
    ((WARNINGS++))
fi

# Check current state
if echo "$CONTENT" | grep -qE "Current State.*:"; then
    PASSED+=("Has current state indicator")
else
    SUGGESTIONS+=("Add explicit current state indicator")
    ((WARNINGS++))
fi

# ============================================================================
# Calculate Final Score and Status
# ============================================================================
[[ $SCORE -lt 0 ]] && SCORE=0
[[ $SCORE -gt 100 ]] && SCORE=100

if [[ $ERRORS -eq 0 ]] && [[ $SCORE -ge 80 ]]; then
    STATUS="approved"
    STATUS_COLOR=$GREEN
elif [[ $ERRORS -le 2 ]] && [[ $SCORE -ge 60 ]]; then
    STATUS="needs_work"
    STATUS_COLOR=$YELLOW
else
    STATUS="rejected"
    STATUS_COLOR=$RED
fi

# ============================================================================
# Generate JSON Output
# ============================================================================
OUTPUT_FILE="$OUTPUT_DIR/review.json"

ISSUES_JSON=$(printf '%s\n' "${ISSUES[@]}" 2>/dev/null | jq -R . | jq -s . || echo "[]")
SUGGESTIONS_JSON=$(printf '%s\n' "${SUGGESTIONS[@]}" 2>/dev/null | jq -R . | jq -s . || echo "[]")
PASSED_JSON=$(printf '%s\n' "${PASSED[@]}" | jq -R . | jq -s .)

cat > "$OUTPUT_FILE" << EOF
{
  "prp_file": "$PRP_FILE",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "$STATUS",
  "score": $SCORE,
  "summary": {
    "errors": $ERRORS,
    "warnings": $WARNINGS,
    "passed": ${#PASSED[@]}
  },
  "issues": $ISSUES_JSON,
  "suggestions": $SUGGESTIONS_JSON,
  "passed": $PASSED_JSON
}
EOF

# ============================================================================
# Output Summary
# ============================================================================
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${STATUS_COLOR}Review Status: ${STATUS^^}${NC}"
echo -e "Output: $OUTPUT_FILE"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"

echo ""
echo -e "${BLUE}Score: ${SCORE}/100${NC}"
echo -e "  Errors:   $ERRORS"
echo -e "  Warnings: $WARNINGS"
echo -e "  Passed:   ${#PASSED[@]}"

if [[ ${#ISSUES[@]} -gt 0 ]]; then
    echo ""
    echo -e "${RED}Issues (must fix):${NC}"
    for issue in "${ISSUES[@]}"; do
        echo -e "  ${RED}✗${NC} $issue"
    done
fi

if [[ ${#SUGGESTIONS[@]} -gt 0 ]]; then
    echo ""
    echo -e "${YELLOW}Suggestions:${NC}"
    for suggestion in "${SUGGESTIONS[@]}"; do
        echo -e "  ${YELLOW}!${NC} $suggestion"
    done
fi

echo ""
case $STATUS in
    approved)
        echo -e "${GREEN}✓ PRP is ready for implementation${NC}"
        exit 0
        ;;
    needs_work)
        echo -e "${YELLOW}! PRP needs revisions before proceeding${NC}"
        exit 1
        ;;
    rejected)
        echo -e "${RED}✗ PRP requires significant rework${NC}"
        exit 2
        ;;
esac
