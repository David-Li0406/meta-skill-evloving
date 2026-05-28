#!/bin/bash
# prp-checker-llm.sh - Intelligent PRP quality checker
#
# Uses Claude CLI to evaluate PRP quality with semantic understanding,
# not just pattern matching.
#
# Usage:
#   ./prp-checker-llm.sh <prp-file.md> [options]
#
# Options:
#   --spec <file>       Original spec for context (recommended)
#   --model <model>     Claude model: haiku (default), sonnet, opus
#   --json              Output JSON only (for scripting)
#   --fix               Attempt to fix issues and output revised PRP

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPTS_DIR="$SCRIPT_DIR/../prompts"

# Defaults
MODEL="haiku"  # Use haiku for fast checking
JSON_OUTPUT=false
FIX_MODE=false
SPEC_FILE=""

# Usage
usage() {
    echo "Usage: $0 <prp-file.md> [options]"
    echo ""
    echo "Intelligent PRP quality checker using Claude."
    echo ""
    echo "Options:"
    echo "  --spec <file>    Original spec for context (recommended)"
    echo "  --model <model>  Claude model: haiku (default/fast), sonnet, opus"
    echo "  --json           Output JSON only (for scripting)"
    echo "  --fix            Attempt to fix issues and output revised PRP"
    echo ""
    echo "Examples:"
    echo "  $0 PRPs/my-feature-prp.md"
    echo "  $0 PRPs/api-prp.md --spec specs/api-spec.md"
    echo "  $0 PRPs/feature-prp.md --json | jq '.quality_score'"
    exit 1
}

# Check for claude CLI
check_claude_cli() {
    if ! command -v claude &> /dev/null; then
        echo -e "${RED}ERROR: Claude CLI not found.${NC}"
        exit 1
    fi
}

# Call Claude CLI
call_claude() {
    local prompt="$1"
    local model_flag=""

    case "$MODEL" in
        "haiku")
            model_flag="--model claude-3-5-haiku-latest"
            ;;
        "sonnet")
            model_flag="--model claude-sonnet-4-20250514"
            ;;
        "opus")
            model_flag="--model claude-opus-4-20250514"
            ;;
    esac

    echo "$prompt" | claude $model_flag --print 2>/dev/null
}

# Parse arguments
if [[ $# -lt 1 ]]; then
    usage
fi

PRP_FILE="$1"
shift

while [[ $# -gt 0 ]]; do
    case "$1" in
        --spec)
            SPEC_FILE="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --fix)
            FIX_MODE=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# Validate PRP file
if [[ ! -f "$PRP_FILE" ]]; then
    echo -e "${RED}ERROR: PRP file not found: $PRP_FILE${NC}"
    exit 1
fi

check_claude_cli

# Read files
PRP_CONTENT=$(cat "$PRP_FILE")
SPEC_CONTENT=""
if [[ -n "$SPEC_FILE" ]] && [[ -f "$SPEC_FILE" ]]; then
    SPEC_CONTENT=$(cat "$SPEC_FILE")
fi

if [[ "$JSON_OUTPUT" == "false" ]]; then
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Intelligent PRP Checker${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "PRP: ${CYAN}$PRP_FILE${NC}"
    echo -e "Model: ${CYAN}$MODEL${NC}"
    echo ""
fi

# Build review prompt
REVIEW_PROMPT=$(cat "$PROMPTS_DIR/prp-review.md")

if [[ -n "$SPEC_CONTENT" ]]; then
    REVIEW_PROMPT="${REVIEW_PROMPT//\{\{SPEC_CONTENT\}\}/$SPEC_CONTENT}"
else
    REVIEW_PROMPT="${REVIEW_PROMPT//\{\{SPEC_CONTENT\}\}/[No spec provided for context]}"
fi
REVIEW_PROMPT="${REVIEW_PROMPT//\{\{PRP_CONTENT\}\}/$PRP_CONTENT}"

# Call Claude for review
if [[ "$JSON_OUTPUT" == "false" ]]; then
    echo -e "${BLUE}Analyzing PRP...${NC}"
fi

REVIEW_RESULT=$(call_claude "$REVIEW_PROMPT")

# Extract JSON
REVIEW_JSON=$(echo "$REVIEW_RESULT" | sed -n '/```json/,/```/p' | sed '1d;$d')
if [[ -z "$REVIEW_JSON" ]]; then
    REVIEW_JSON=$(echo "$REVIEW_RESULT" | grep -o '{.*}')
fi

if [[ "$JSON_OUTPUT" == "true" ]]; then
    echo "$REVIEW_JSON"
    exit 0
fi

# Parse and display results
echo ""

# Extract fields
STATUS=$(echo "$REVIEW_JSON" | grep -o '"overall_status":\s*"[^"]*"' | cut -d'"' -f4)
SCORE=$(echo "$REVIEW_JSON" | grep -o '"quality_score":\s*[0-9]*' | grep -o '[0-9]*')
SUMMARY=$(echo "$REVIEW_JSON" | grep -o '"summary":\s*"[^"]*"' | cut -d'"' -f4)

# Status display
case "$STATUS" in
    "PASS")
        echo -e "${GREEN}Status: PASS${NC}"
        ;;
    "NEEDS_REVISION")
        echo -e "${YELLOW}Status: NEEDS REVISION${NC}"
        ;;
    "REJECTED")
        echo -e "${RED}Status: REJECTED${NC}"
        ;;
    *)
        echo -e "Status: ${STATUS:-unknown}"
        ;;
esac

# Score display
if [[ -n "$SCORE" ]]; then
    if [[ "$SCORE" -ge 80 ]]; then
        echo -e "Quality Score: ${GREEN}$SCORE/100${NC}"
    elif [[ "$SCORE" -ge 60 ]]; then
        echo -e "Quality Score: ${YELLOW}$SCORE/100${NC}"
    else
        echo -e "Quality Score: ${RED}$SCORE/100${NC}"
    fi
fi

echo ""

# Summary
if [[ -n "$SUMMARY" ]]; then
    echo -e "${BLUE}Summary:${NC}"
    echo "  $SUMMARY"
    echo ""
fi

# Issues (extract and display)
echo -e "${BLUE}Issues Found:${NC}"

# Count issues by severity
BLOCKERS=$(echo "$REVIEW_JSON" | grep -o '"severity":\s*"BLOCKER"' | wc -l | tr -d ' ')
MAJORS=$(echo "$REVIEW_JSON" | grep -o '"severity":\s*"MAJOR"' | wc -l | tr -d ' ')
MINORS=$(echo "$REVIEW_JSON" | grep -o '"severity":\s*"MINOR"' | wc -l | tr -d ' ')

[[ "$BLOCKERS" -gt 0 ]] && echo -e "  ${RED}Blockers: $BLOCKERS${NC}"
[[ "$MAJORS" -gt 0 ]] && echo -e "  ${YELLOW}Major: $MAJORS${NC}"
[[ "$MINORS" -gt 0 ]] && echo -e "  Minor: $MINORS"

echo ""

# Full JSON for details
echo -e "${BLUE}Full Review:${NC}"
echo "$REVIEW_JSON" | python3 -m json.tool 2>/dev/null || echo "$REVIEW_JSON"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"

# Fix mode
if [[ "$FIX_MODE" == "true" ]] && [[ "$STATUS" != "PASS" ]]; then
    echo ""
    echo -e "${BLUE}Attempting to fix issues...${NC}"

    FIX_PROMPT="The following PRP has quality issues. Please fix them and output the complete revised PRP.

Issues:
$REVIEW_JSON

Original PRP:
$PRP_CONTENT

Output only the revised PRP markdown (no explanation, no code blocks):"

    FIXED_PRP=$(call_claude "$FIX_PROMPT")
    FIXED_PRP=$(echo "$FIXED_PRP" | sed '/^```markdown$/d' | sed '/^```$/d')

    FIXED_FILE="${PRP_FILE%.md}-fixed.md"
    echo "$FIXED_PRP" > "$FIXED_FILE"
    echo -e "${GREEN}Fixed PRP saved to: $FIXED_FILE${NC}"
fi

# Exit code based on status
case "$STATUS" in
    "PASS")
        exit 0
        ;;
    "NEEDS_REVISION")
        exit 1
        ;;
    "REJECTED")
        exit 2
        ;;
    *)
        exit 1
        ;;
esac
