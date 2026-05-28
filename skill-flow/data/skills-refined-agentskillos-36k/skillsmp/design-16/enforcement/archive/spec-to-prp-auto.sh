#!/bin/bash
# spec-to-prp-auto.sh - Auto-loop spec to PRP with quality threshold
#
# The "Ralph loop" - iterates until quality threshold reached.
# Uses prp-checker.sh --fix for improvements (single source of truth).
#
# Usage:
#   ./spec-to-prp-auto.sh <spec-file> [--threshold 95] [--max-iterations 5]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPTS_DIR="$SCRIPT_DIR/../prompts"
TEMPLATES_DIR="$SCRIPT_DIR/../templates"
OUTPUT_DIR="$SCRIPT_DIR/../output"

# Defaults
THRESHOLD=95
MAX_ITERATIONS=5
MODEL="sonnet"
VERBOSE=false

usage() {
    echo "Usage: $0 <spec-file> [options]"
    echo ""
    echo "Auto-loop spec-to-PRP generation until quality threshold reached."
    echo "Uses prp-checker.sh --fix for improvements (single source of truth)."
    echo ""
    echo "Options:"
    echo "  --output <file>       Output PRP file path"
    echo "  --threshold <N>       Quality threshold 0-100 (default: 95)"
    echo "  --max-iterations <N>  Max improvement iterations (default: 5)"
    echo "  --model <model>       Model for generation: haiku, sonnet (default), opus"
    echo "  --verbose             Show detailed progress"
    echo ""
    echo "Example:"
    echo "  $0 specs/phase1.md --threshold 95 --max-iterations 5"
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
        --threshold) THRESHOLD="$2"; shift 2 ;;
        --max-iterations) MAX_ITERATIONS="$2"; shift 2 ;;
        --model) MODEL="$2"; shift 2 ;;
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

SPEC_CONTENT=$(cat "$SPEC_FILE")

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          SPEC-TO-PRP AUTO-LOOP (Ralph Mode)                   ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Spec:       ${CYAN}$SPEC_FILE${NC}"
echo -e "Output:     ${CYAN}$OUTPUT_FILE${NC}"
echo -e "Threshold:  ${CYAN}$THRESHOLD%${NC}"
echo -e "Max Iters:  ${CYAN}$MAX_ITERATIONS${NC}"
echo ""

# ============================================================================
# PHASE 1: Initial PRP Generation
# ============================================================================

echo -e "${BLUE}[Phase 1] Generating initial PRP...${NC}"

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

# ============================================================================
# PHASE 2: Quality Check Loop (The Ralph Loop)
# ============================================================================

echo ""
echo -e "${BLUE}[Phase 2] Quality improvement loop...${NC}"

ITERATION=0
CURRENT_SCORE=0
BEST_SCORE=0
BEST_PRP="$PRP_CONTENT"

while [[ $ITERATION -lt $MAX_ITERATIONS ]]; do
    ITERATION=$((ITERATION + 1))
    echo ""
    echo -e "${MAGENTA}  ━━━ Iteration $ITERATION/$MAX_ITERATIONS ━━━${NC}"

    # Check quality using prp-checker.sh
    echo -e "${CYAN}   Checking quality...${NC}"

    CHECK_RESULT=$("$SCRIPT_DIR/prp-checker.sh" "$OUTPUT_FILE" --json --threshold "$THRESHOLD" 2>/dev/null || echo '{"overall_score":0}')

    CURRENT_SCORE=$(echo "$CHECK_RESULT" | grep -o '"overall_score":\s*[0-9]*' | grep -o '[0-9]*' | head -1)
    [[ -z "$CURRENT_SCORE" ]] && CURRENT_SCORE=0

    # Track best version
    if [[ $CURRENT_SCORE -gt $BEST_SCORE ]]; then
        BEST_SCORE=$CURRENT_SCORE
        BEST_PRP=$(cat "$OUTPUT_FILE")
    fi

    # Display score
    if [[ $CURRENT_SCORE -ge $THRESHOLD ]]; then
        echo -e "${GREEN}   Score: $CURRENT_SCORE% (threshold: $THRESHOLD%) ✓${NC}"
        echo -e "${GREEN}   ✓ Quality threshold reached!${NC}"
        break
    elif [[ $CURRENT_SCORE -ge 80 ]]; then
        echo -e "${YELLOW}   Score: $CURRENT_SCORE% (threshold: $THRESHOLD%)${NC}"
    else
        echo -e "${RED}   Score: $CURRENT_SCORE% (threshold: $THRESHOLD%)${NC}"
    fi

    # If not at threshold and not last iteration, use --fix to improve
    if [[ $ITERATION -lt $MAX_ITERATIONS ]]; then
        echo -e "${CYAN}   Improving PRP using prp-checker --fix...${NC}"

        # Run prp-checker with --fix flag (generates improved version)
        "$SCRIPT_DIR/prp-checker.sh" "$OUTPUT_FILE" --fix --threshold "$THRESHOLD" > /dev/null 2>&1 || true

        # The --fix flag creates {file}-improved.md
        IMPROVED_FILE="${OUTPUT_FILE%.md}-improved.md"

        if [[ -f "$IMPROVED_FILE" ]]; then
            # Replace original with improved version
            mv "$IMPROVED_FILE" "$OUTPUT_FILE"
            echo -e "${GREEN}   ✓ PRP improved${NC}"
        else
            echo -e "${YELLOW}   ⚠ No improvement generated, continuing...${NC}"
        fi
    fi
done

# ============================================================================
# PHASE 3: Final Output
# ============================================================================

echo ""
echo -e "${BLUE}[Phase 3] Finalizing...${NC}"

# Use best version if current isn't better
if [[ $BEST_SCORE -gt $CURRENT_SCORE ]]; then
    echo -e "${YELLOW}   Using best iteration (score: $BEST_SCORE%)${NC}"
    echo "$BEST_PRP" > "$OUTPUT_FILE"
    CURRENT_SCORE=$BEST_SCORE
fi

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    GENERATION COMPLETE                        ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Output:     ${CYAN}$OUTPUT_FILE${NC}"
echo -e "Iterations: ${CYAN}$ITERATION${NC}"

if [[ $CURRENT_SCORE -ge $THRESHOLD ]]; then
    echo -e "Score:      ${GREEN}$CURRENT_SCORE%${NC} (threshold: $THRESHOLD%)"
    echo -e "Status:     ${GREEN}PASS${NC}"
    EXIT_CODE=0
else
    echo -e "Score:      ${YELLOW}$CURRENT_SCORE%${NC} (threshold: $THRESHOLD%)"
    echo -e "Status:     ${YELLOW}BEST EFFORT${NC} (did not reach threshold)"
    EXIT_CODE=1
fi

echo ""

# Summary stats
LINES=$(wc -l < "$OUTPUT_FILE" | tr -d ' ')
PLACEHOLDERS=$(grep -cE '\[FILL_|\{\{' "$OUTPUT_FILE" 2>/dev/null || echo "0")
echo -e "PRP Stats:  ${CYAN}$LINES lines, $PLACEHOLDERS placeholders${NC}"
echo ""

exit $EXIT_CODE
