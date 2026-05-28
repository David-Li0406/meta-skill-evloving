#!/bin/bash
# spec-to-prp-pipeline.sh - Complete pipeline with dual Ralph loops
#
# Full orchestration:
#   1. SPEC LOOP: Validate spec → fix with validator.sh --fix → re-validate → until 95%+
#   2. PRP LOOP:  Generate PRP → check with prp-checker.sh → fix → until 95%+
#
# Single source of truth: uses validator.sh and prp-checker.sh for both checking AND fixing.
#
# Usage:
#   ./spec-to-prp-pipeline.sh <spec-file> [options]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
WHITE='\033[1;37m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/../output"

# Defaults
SPEC_THRESHOLD=95
PRP_THRESHOLD=95
MAX_SPEC_ITERATIONS=3
MAX_PRP_ITERATIONS=5
MODEL="sonnet"
DOMAIN=""
SKIP_SPEC_VALIDATION=false
VERBOSE=false

usage() {
    echo "Usage: $0 <spec-file> [options]"
    echo ""
    echo "Complete spec-to-PRP pipeline with dual quality loops."
    echo "Uses validator.sh --fix and prp-checker.sh --fix (single source of truth)."
    echo ""
    echo "Options:"
    echo "  --output <file>           Output PRP file"
    echo "  --spec-threshold <N>      Spec validation threshold (default: 95)"
    echo "  --prp-threshold <N>       PRP quality threshold (default: 95)"
    echo "  --max-spec-iters <N>      Max spec improvement iterations (default: 3)"
    echo "  --max-prp-iters <N>       Max PRP improvement iterations (default: 5)"
    echo "  --domain <name>           Domain invariants to apply"
    echo "  --skip-spec-validation    Skip spec validation loop"
    echo "  --verbose                 Detailed output"
    echo ""
    exit 1
}

check_claude_cli() {
    command -v claude &> /dev/null || { echo -e "${RED}ERROR: Claude CLI not found.${NC}" >&2; exit 1; }
}

call_claude() {
    local prompt="$1"
    local model="${2:-sonnet}"
    local model_flag=""
    case "$model" in
        "haiku") model_flag="--model claude-3-5-haiku-latest" ;;
        "sonnet") model_flag="--model claude-sonnet-4-20250514" ;;
        "opus") model_flag="--model claude-opus-4-20250514" ;;
    esac
    echo "$prompt" | claude $model_flag --print 2>/dev/null
}

# Parse arguments
[[ $# -lt 1 ]] && usage

SPEC_FILE="$1"
shift

while [[ $# -gt 0 ]]; do
    case "$1" in
        --output) OUTPUT_FILE="$2"; shift 2 ;;
        --spec-threshold) SPEC_THRESHOLD="$2"; shift 2 ;;
        --prp-threshold) PRP_THRESHOLD="$2"; shift 2 ;;
        --max-spec-iters) MAX_SPEC_ITERATIONS="$2"; shift 2 ;;
        --max-prp-iters) MAX_PRP_ITERATIONS="$2"; shift 2 ;;
        --domain) DOMAIN="$2"; shift 2 ;;
        --skip-spec-validation) SKIP_SPEC_VALIDATION=true; shift ;;
        --verbose) VERBOSE=true; shift ;;
        *) echo -e "${RED}Unknown option: $1${NC}"; usage ;;
    esac
done

[[ ! -f "$SPEC_FILE" ]] && { echo -e "${RED}ERROR: Spec not found: $SPEC_FILE${NC}"; exit 1; }

check_claude_cli

# Set output file
SPEC_BASENAME=$(basename "$SPEC_FILE" .md)
[[ -z "$OUTPUT_FILE" ]] && {
    mkdir -p "$OUTPUT_DIR"
    OUTPUT_FILE="$OUTPUT_DIR/${SPEC_BASENAME}-prp.md"
}

# Work directory for intermediate files
WORK_DIR=$(mktemp -d)
trap "rm -rf $WORK_DIR" EXIT

# Copy spec to work directory for potential modifications
WORKING_SPEC="$WORK_DIR/spec.md"
cp "$SPEC_FILE" "$WORKING_SPEC"

echo -e "${WHITE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${WHITE}║         SPEC-TO-PRP PIPELINE (Dual Ralph Loop)                ║${NC}"
echo -e "${WHITE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Input:          ${CYAN}$SPEC_FILE${NC}"
echo -e "Output:         ${CYAN}$OUTPUT_FILE${NC}"
echo -e "Spec Threshold: ${CYAN}$SPEC_THRESHOLD%${NC}"
echo -e "PRP Threshold:  ${CYAN}$PRP_THRESHOLD%${NC}"
[[ -n "$DOMAIN" ]] && echo -e "Domain:         ${CYAN}$DOMAIN${NC}"
echo ""

# ============================================================================
# PHASE 1: SPEC VALIDATION LOOP
# ============================================================================

SPEC_SCORE=0
SPEC_ITERATION=0

if [[ "$SKIP_SPEC_VALIDATION" == "false" ]]; then
    echo -e "${BLUE}╭───────────────────────────────────────────────────────────────╮${NC}"
    echo -e "${BLUE}│  PHASE 1: Spec Validation Loop                                │${NC}"
    echo -e "${BLUE}╰───────────────────────────────────────────────────────────────╯${NC}"
    echo ""

    SPEC_PASSED=false

    while [[ $SPEC_ITERATION -lt $MAX_SPEC_ITERATIONS ]] && [[ "$SPEC_PASSED" == "false" ]]; do
        SPEC_ITERATION=$((SPEC_ITERATION + 1))
        echo -e "${MAGENTA}  ━━━ Spec Iteration $SPEC_ITERATION/$MAX_SPEC_ITERATIONS ━━━${NC}"

        # Validate spec using validator.sh
        echo -e "${CYAN}   Validating spec...${NC}"

        DOMAIN_FLAG=""
        [[ -n "$DOMAIN" ]] && DOMAIN_FLAG="--domain $DOMAIN"

        VALIDATE_RESULT=$("$SCRIPT_DIR/validator.sh" "$WORKING_SPEC" $DOMAIN_FLAG --threshold "$SPEC_THRESHOLD" --json 2>/dev/null || echo '{"overall_score":0}')

        SPEC_SCORE=$(echo "$VALIDATE_RESULT" | grep -o '"overall_score":\s*[0-9]*' | grep -o '[0-9]*' | head -1)
        [[ -z "$SPEC_SCORE" ]] && SPEC_SCORE=0

        if [[ $SPEC_SCORE -ge $SPEC_THRESHOLD ]]; then
            echo -e "${GREEN}   Score: $SPEC_SCORE% ✓${NC}"
            SPEC_PASSED=true
        else
            echo -e "${YELLOW}   Score: $SPEC_SCORE%${NC}"

            # If not last iteration, use validator.sh --fix to improve
            if [[ $SPEC_ITERATION -lt $MAX_SPEC_ITERATIONS ]]; then
                echo -e "${CYAN}   Improving spec using validator --fix...${NC}"

                "$SCRIPT_DIR/validator.sh" "$WORKING_SPEC" $DOMAIN_FLAG --fix --threshold "$SPEC_THRESHOLD" > /dev/null 2>&1 || true

                # The --fix flag creates {file}-fixed.md
                FIXED_SPEC="${WORKING_SPEC%.md}-fixed.md"

                if [[ -f "$FIXED_SPEC" ]]; then
                    mv "$FIXED_SPEC" "$WORKING_SPEC"
                    echo -e "${GREEN}   ✓ Spec improved${NC}"
                else
                    echo -e "${YELLOW}   ⚠ No improvement generated${NC}"
                fi
            fi
        fi
        echo ""
    done

    if [[ "$SPEC_PASSED" == "true" ]]; then
        echo -e "${GREEN}  ✓ Spec validation passed ($SPEC_SCORE%)${NC}"
    else
        echo -e "${YELLOW}  ⚠ Spec at $SPEC_SCORE% (best effort, continuing)${NC}"
    fi
    echo ""
else
    echo -e "${YELLOW}Skipping spec validation (--skip-spec-validation)${NC}"
    echo ""
fi

# ============================================================================
# PHASE 2: PRP GENERATION LOOP
# ============================================================================

echo -e "${BLUE}╭───────────────────────────────────────────────────────────────╮${NC}"
echo -e "${BLUE}│  PHASE 2: PRP Generation Loop                                 │${NC}"
echo -e "${BLUE}╰───────────────────────────────────────────────────────────────╯${NC}"
echo ""

# Read the (potentially improved) spec
SPEC_CONTENT=$(cat "$WORKING_SPEC")

# Initial PRP generation
echo -e "${CYAN}   Generating initial PRP...${NC}"

GENERATE_PROMPT=$(cat << 'PROMPT_END'
Transform this specification into a complete Product Requirements Prompt (PRP).

## Specification
{{SPEC_CONTENT}}

## PRP Requirements
Generate a complete PRP with these sections:

1. **Meta** - prp_id, source_spec, created_date, status
2. **Overview** - Problem statement, solution summary, scope
3. **Success Criteria** - Measurable metrics with specific numbers
4. **Timeline** - Phases with validation gates (GATE_X_PASS := condition)
5. **Risk Assessment** - Risks with likelihood, impact, mitigation
6. **Resource Requirements** - People, tools, infrastructure
7. **Communication Plan** - Stakeholders, cadence, channels
8. **Validation Commands** - Actual bash commands to verify completion

## Critical Rules
- NO placeholders like [FILL_IN] or {{VARIABLE}} - use specific values
- ALL metrics must have numbers (e.g., "<200ms" not "fast")
- ALL gates must have concrete pass/fail conditions
- Include real bash commands, not descriptions

Output the complete PRP in markdown:
PROMPT_END
)
GENERATE_PROMPT="${GENERATE_PROMPT//\{\{SPEC_CONTENT\}\}/$SPEC_CONTENT}"

PRP_CONTENT=$(call_claude "$GENERATE_PROMPT" "$MODEL")
PRP_CONTENT=$(echo "$PRP_CONTENT" | sed '/^```markdown$/d' | sed '/^```$/d')

echo "$PRP_CONTENT" > "$OUTPUT_FILE"
echo -e "${GREEN}   ✓ Initial PRP generated${NC}"
echo ""

# PRP quality loop with spec feedback
PRP_ITERATION=0
PRP_SCORE=0
PRP_PASSED=false
BEST_PRP="$PRP_CONTENT"
BEST_SCORE=0
SPEC_FEEDBACK_COUNT=0
MAX_SPEC_FEEDBACKS=2  # Limit how many times we go back to spec

while [[ $PRP_ITERATION -lt $MAX_PRP_ITERATIONS ]] && [[ "$PRP_PASSED" == "false" ]]; do
    PRP_ITERATION=$((PRP_ITERATION + 1))
    echo -e "${MAGENTA}  ━━━ PRP Iteration $PRP_ITERATION/$MAX_PRP_ITERATIONS ━━━${NC}"

    # Check PRP quality using prp-checker.sh
    echo -e "${CYAN}   Checking PRP quality...${NC}"

    CHECK_RESULT=$("$SCRIPT_DIR/prp-checker.sh" "$OUTPUT_FILE" --json --threshold "$PRP_THRESHOLD" 2>/dev/null || echo '{"overall_score":0}')

    PRP_SCORE=$(echo "$CHECK_RESULT" | grep -o '"overall_score":\s*[0-9]*' | grep -o '[0-9]*' | head -1)
    HAS_SPEC_ISSUES=$(echo "$CHECK_RESULT" | grep -o '"has_spec_issues":\s*true' | head -1)
    [[ -z "$PRP_SCORE" ]] && PRP_SCORE=0

    # Track best
    if [[ $PRP_SCORE -gt $BEST_SCORE ]]; then
        BEST_SCORE=$PRP_SCORE
        BEST_PRP=$(cat "$OUTPUT_FILE")
    fi

    if [[ $PRP_SCORE -ge $PRP_THRESHOLD ]]; then
        echo -e "${GREEN}   Score: $PRP_SCORE% ✓${NC}"
        PRP_PASSED=true
    else
        echo -e "${YELLOW}   Score: $PRP_SCORE%${NC}"

        # Check for spec-level issues that require going back to spec
        if [[ -n "$HAS_SPEC_ISSUES" ]] && [[ $SPEC_FEEDBACK_COUNT -lt $MAX_SPEC_FEEDBACKS ]]; then
            SPEC_FEEDBACK_COUNT=$((SPEC_FEEDBACK_COUNT + 1))
            echo -e "${RED}   ⚠ Spec-level issues detected! Routing back to spec improvement...${NC}"
            echo ""

            # Extract spec issues and create fix prompt
            SPEC_ISSUES=$(echo "$CHECK_RESULT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for issue in data.get('spec_issues', []):
        print(f\"- {issue.get('problem', 'N/A')}\")
        print(f\"  Fix: {issue.get('spec_fix', 'N/A')}\")
except:
    pass
" 2>/dev/null)

            if [[ -n "$SPEC_ISSUES" ]]; then
                echo -e "${CYAN}   Spec issues to fix:${NC}"
                echo "$SPEC_ISSUES" | head -10
                echo ""

                # Use validator.sh --fix with the spec issues as context
                echo -e "${CYAN}   Improving spec with identified issues...${NC}"

                # Create a temporary file with the issues for the fix prompt
                ISSUES_FILE="$WORK_DIR/spec-issues.txt"
                echo "$SPEC_ISSUES" > "$ISSUES_FILE"

                "$SCRIPT_DIR/validator.sh" "$WORKING_SPEC" $DOMAIN_FLAG --fix --threshold "$SPEC_THRESHOLD" > /dev/null 2>&1 || true

                FIXED_SPEC="${WORKING_SPEC%.md}-fixed.md"
                if [[ -f "$FIXED_SPEC" ]]; then
                    mv "$FIXED_SPEC" "$WORKING_SPEC"
                    echo -e "${GREEN}   ✓ Spec improved based on PRP feedback${NC}"

                    # Regenerate PRP from improved spec
                    echo -e "${CYAN}   Regenerating PRP from improved spec...${NC}"
                    SPEC_CONTENT=$(cat "$WORKING_SPEC")
                    GENERATE_PROMPT="${GENERATE_PROMPT//\{\{SPEC_CONTENT\}\}/$SPEC_CONTENT}"
                    PRP_CONTENT=$(call_claude "$GENERATE_PROMPT" "$MODEL")
                    PRP_CONTENT=$(echo "$PRP_CONTENT" | sed '/^```markdown$/d' | sed '/^```$/d')
                    echo "$PRP_CONTENT" > "$OUTPUT_FILE"
                    echo -e "${GREEN}   ✓ PRP regenerated${NC}"
                else
                    echo -e "${YELLOW}   ⚠ Could not improve spec, continuing with PRP fixes${NC}"
                fi
            fi
        # If not last iteration and no spec issues, use prp-checker.sh --fix to improve
        elif [[ $PRP_ITERATION -lt $MAX_PRP_ITERATIONS ]]; then
            echo -e "${CYAN}   Improving PRP using prp-checker --fix...${NC}"

            "$SCRIPT_DIR/prp-checker.sh" "$OUTPUT_FILE" --fix --threshold "$PRP_THRESHOLD" > /dev/null 2>&1 || true

            # The --fix flag creates {file}-improved.md
            IMPROVED_FILE="${OUTPUT_FILE%.md}-improved.md"

            if [[ -f "$IMPROVED_FILE" ]]; then
                mv "$IMPROVED_FILE" "$OUTPUT_FILE"
                echo -e "${GREEN}   ✓ PRP improved${NC}"
            else
                echo -e "${YELLOW}   ⚠ No improvement generated${NC}"
            fi
        fi
    fi
    echo ""
done

# Use best version if current isn't better
if [[ $BEST_SCORE -gt $PRP_SCORE ]]; then
    echo "$BEST_PRP" > "$OUTPUT_FILE"
    PRP_SCORE=$BEST_SCORE
fi

# ============================================================================
# PHASE 3: OUTPUT
# ============================================================================

echo -e "${BLUE}╭───────────────────────────────────────────────────────────────╮${NC}"
echo -e "${BLUE}│  PHASE 3: Output                                              │${NC}"
echo -e "${BLUE}╰───────────────────────────────────────────────────────────────╯${NC}"
echo ""

mkdir -p "$(dirname "$OUTPUT_FILE")"

# Stats
LINES=$(wc -l < "$OUTPUT_FILE" | tr -d ' ')
PLACEHOLDERS=$(grep -cE '\[FILL_|\{\{' "$OUTPUT_FILE" 2>/dev/null || echo "0")

echo ""
echo -e "${WHITE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${WHITE}║                    PIPELINE COMPLETE                          ║${NC}"
echo -e "${WHITE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  Output:         ${CYAN}$OUTPUT_FILE${NC}"
echo -e "  Spec Score:     ${CYAN}${SPEC_SCORE:-N/A}%${NC} (${SPEC_ITERATION:-0} iterations)"
echo -e "  PRP Score:      ${CYAN}$PRP_SCORE%${NC} ($PRP_ITERATION iterations)"
[[ $SPEC_FEEDBACK_COUNT -gt 0 ]] && echo -e "  Spec Feedbacks: ${CYAN}$SPEC_FEEDBACK_COUNT${NC} (PRP→Spec loops)"
echo -e "  PRP Stats:      ${CYAN}$LINES lines, $PLACEHOLDERS placeholders${NC}"
echo ""

if [[ $PRP_SCORE -ge $PRP_THRESHOLD ]]; then
    echo -e "  ${GREEN}✓ PASSED - Quality threshold met${NC}"
    EXIT_CODE=0
else
    echo -e "  ${YELLOW}⚠ BEST EFFORT - Did not reach threshold${NC}"
    EXIT_CODE=1
fi

echo ""
exit $EXIT_CODE
