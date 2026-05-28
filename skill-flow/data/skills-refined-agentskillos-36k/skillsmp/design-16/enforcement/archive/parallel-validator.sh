#!/bin/bash
# parallel-validator.sh - Parallel invariant validation using background jobs
#
# Runs multiple invariant checks simultaneously, aggregates results.
# This is the "multiple Ralphs" approach - same methodology, parallel execution.
#
# Usage:
#   ./parallel-validator.sh <spec-file> [--workers N] [--threshold 95]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPTS_DIR="$SCRIPT_DIR/../prompts"
INVARIANTS_DIR="$SCRIPT_DIR/../invariants"

# Defaults
MAX_WORKERS=4
THRESHOLD=95
VERBOSE=false

usage() {
    echo "Usage: $0 <spec-file> [options]"
    echo ""
    echo "Parallel invariant validation - multiple checks run simultaneously."
    echo ""
    echo "Options:"
    echo "  --workers N      Max parallel workers (default: 4)"
    echo "  --threshold N    Quality threshold to pass (default: 95)"
    echo "  --verbose        Show detailed progress"
    echo "  --json           Output JSON only"
    exit 1
}

# Check for claude CLI
check_claude_cli() {
    if ! command -v claude &> /dev/null; then
        echo -e "${RED}ERROR: Claude CLI not found.${NC}" >&2
        exit 1
    fi
}

# Parse arguments
[[ $# -lt 1 ]] && usage

SPEC_FILE="$1"
shift

JSON_OUTPUT=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --workers) MAX_WORKERS="$2"; shift 2 ;;
        --threshold) THRESHOLD="$2"; shift 2 ;;
        --verbose) VERBOSE=true; shift ;;
        --json) JSON_OUTPUT=true; shift ;;
        *) echo -e "${RED}Unknown option: $1${NC}"; usage ;;
    esac
done

[[ ! -f "$SPEC_FILE" ]] && { echo -e "${RED}ERROR: Spec not found: $SPEC_FILE${NC}"; exit 1; }

check_claude_cli

# Create temp directory for parallel results
WORK_DIR=$(mktemp -d)
trap "rm -rf $WORK_DIR" EXIT

SPEC_CONTENT=$(cat "$SPEC_FILE")

# Define invariant groups for parallel checking
# Each group runs as a separate worker
declare -a INVARIANT_GROUPS=(
    "ambiguity|state|scope"
    "validation|cost|blast_radius"
    "degradation|reversibility|failure"
    "domain_specific"
)

# The validation prompt template
create_validation_prompt() {
    local group="$1"
    cat << 'PROMPT_END'
You are validating a specification against system invariants.

INVARIANTS TO CHECK (focus on these):
{{INVARIANT_GROUP}}

SPECIFICATION:
{{SPEC_CONTENT}}

For each invariant, check if the spec violates it. Be strict but fair.

Output JSON only:
```json
{
  "group": "{{GROUP_NAME}}",
  "checks": [
    {
      "invariant": "invariant name",
      "status": "PASS|FAIL|WARN",
      "confidence": 0.0-1.0,
      "location": "line or section reference",
      "issue": "description if not PASS",
      "fix": "suggested fix if not PASS"
    }
  ],
  "group_score": 0-100
}
```
PROMPT_END
}

# Invariant definitions for each group
get_invariant_definitions() {
    local group="$1"
    case "$group" in
        "ambiguity|state|scope")
            cat << 'EOF'
1. AMBIGUITY IS INVALID: Words like "properly", "appropriate", "reasonable", "fast", "secure" without quantified metrics are violations. Every quality must have: metric + threshold + measurement method.

2. STATE MUST BE EXPLICIT: All state transitions must be documented. Entry conditions, exit conditions, and error states must be defined. No implicit state changes.

3. SCOPE MUST BE BOUNDED: Clear in-scope and out-of-scope lists. No unbounded work. Explicit "NOT doing" section.
EOF
            ;;
        "validation|cost|blast_radius")
            cat << 'EOF'
4. VALIDATION MUST BE EXECUTABLE: Every requirement must have a concrete test. "User can X" must have specific verification steps. No untestable requirements.

5. COST BOUNDARIES EXPLICIT: Time, money, compute costs must have explicit bounds. "Reasonable cost" is a violation - must specify actual limits.

6. BLAST RADIUS DECLARED: What can this change break? Dependencies, downstream effects, rollback procedures must be documented.
EOF
            ;;
        "degradation|reversibility|failure")
            cat << 'EOF'
7. DEGRADATION PATH EXISTS: What happens when dependencies fail? Graceful degradation strategy required. No silent failures.

8. NO IRREVERSIBLE WITHOUT RECOVERY: Any destructive operation must have recovery plan. Data deletion, schema changes, etc. need rollback strategy.

9. EXECUTION MUST FAIL LOUDLY: Errors must surface clearly. No swallowed exceptions. Explicit error handling for all failure modes.
EOF
            ;;
        "domain_specific")
            cat << 'EOF'
10. DOMAIN CONSTRAINTS RESPECTED: Industry-specific requirements acknowledged. Compliance, regulations, standards referenced where applicable.

11. USER JOURNEY COMPLETE: End-to-end user flows documented. No gaps in user experience. Error recovery from user perspective.

12. TECHNICAL DEBT ACKNOWLEDGED: Known shortcuts documented. Future work identified. No hidden complexity.
EOF
            ;;
    esac
}

# Run a single validation worker
run_worker() {
    local worker_id="$1"
    local group="$2"
    local output_file="$WORK_DIR/result_${worker_id}.json"

    local invariant_defs=$(get_invariant_definitions "$group")
    local prompt=$(create_validation_prompt "$group")
    prompt="${prompt//\{\{INVARIANT_GROUP\}\}/$invariant_defs}"
    prompt="${prompt//\{\{SPEC_CONTENT\}\}/$SPEC_CONTENT}"
    prompt="${prompt//\{\{GROUP_NAME\}\}/$group}"

    # Call Claude CLI
    local result=$(echo "$prompt" | claude --model claude-3-5-haiku-latest --print 2>/dev/null)

    # Extract JSON
    local json=$(echo "$result" | sed -n '/```json/,/```/p' | sed '1d;$d')
    [[ -z "$json" ]] && json=$(echo "$result" | grep -o '{.*}' | head -1)
    [[ -z "$json" ]] && json='{"group":"'"$group"'","checks":[],"group_score":50,"error":"Failed to parse"}'

    echo "$json" > "$output_file"
}

# Main execution
[[ "$JSON_OUTPUT" == "false" ]] && {
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Parallel Invariant Validator${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "Spec: ${CYAN}$SPEC_FILE${NC}"
    echo -e "Workers: ${CYAN}$MAX_WORKERS${NC}"
    echo -e "Threshold: ${CYAN}$THRESHOLD%${NC}"
    echo ""
    echo -e "${BLUE}Launching parallel validation...${NC}"
}

# Launch workers in parallel
PIDS=()
for i in "${!INVARIANT_GROUPS[@]}"; do
    group="${INVARIANT_GROUPS[$i]}"
    [[ "$VERBOSE" == "true" ]] && echo -e "${CYAN}  Starting worker $i: $group${NC}"
    run_worker "$i" "$group" &
    PIDS+=($!)

    # Respect max workers
    if [[ ${#PIDS[@]} -ge $MAX_WORKERS ]]; then
        wait "${PIDS[0]}"
        PIDS=("${PIDS[@]:1}")
    fi
done

# Wait for all workers
wait

[[ "$VERBOSE" == "true" ]] && echo -e "${GREEN}  All workers complete${NC}"

# Aggregate results
TOTAL_SCORE=0
TOTAL_GROUPS=0
ALL_ISSUES=()
ALL_RESULTS="["

for i in "${!INVARIANT_GROUPS[@]}"; do
    result_file="$WORK_DIR/result_${i}.json"
    if [[ -f "$result_file" ]]; then
        result=$(cat "$result_file")
        score=$(echo "$result" | grep -o '"group_score":\s*[0-9]*' | grep -o '[0-9]*' | head -1)
        [[ -n "$score" ]] && {
            TOTAL_SCORE=$((TOTAL_SCORE + score))
            TOTAL_GROUPS=$((TOTAL_GROUPS + 1))
        }
        [[ "$i" -gt 0 ]] && ALL_RESULTS+=","
        ALL_RESULTS+="$result"
    fi
done

ALL_RESULTS+="]"

# Calculate final score
FINAL_SCORE=0
[[ $TOTAL_GROUPS -gt 0 ]] && FINAL_SCORE=$((TOTAL_SCORE / TOTAL_GROUPS))

# Determine pass/fail
STATUS="FAIL"
[[ $FINAL_SCORE -ge $THRESHOLD ]] && STATUS="PASS"

# Build final JSON
FINAL_JSON=$(cat << EOF
{
  "spec_file": "$SPEC_FILE",
  "threshold": $THRESHOLD,
  "final_score": $FINAL_SCORE,
  "status": "$STATUS",
  "groups_checked": $TOTAL_GROUPS,
  "group_results": $ALL_RESULTS
}
EOF
)

if [[ "$JSON_OUTPUT" == "true" ]]; then
    echo "$FINAL_JSON"
else
    echo ""
    echo -e "${BLUE}Results:${NC}"
    echo ""

    # Display per-group scores
    for i in "${!INVARIANT_GROUPS[@]}"; do
        result_file="$WORK_DIR/result_${i}.json"
        if [[ -f "$result_file" ]]; then
            group="${INVARIANT_GROUPS[$i]}"
            score=$(cat "$result_file" | grep -o '"group_score":\s*[0-9]*' | grep -o '[0-9]*' | head -1)
            if [[ -n "$score" ]]; then
                if [[ $score -ge 90 ]]; then
                    echo -e "  ${GREEN}[$score%]${NC} $group"
                elif [[ $score -ge 70 ]]; then
                    echo -e "  ${YELLOW}[$score%]${NC} $group"
                else
                    echo -e "  ${RED}[$score%]${NC} $group"
                fi
            fi
        fi
    done

    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"

    if [[ "$STATUS" == "PASS" ]]; then
        echo -e "  Final Score: ${GREEN}$FINAL_SCORE%${NC} (threshold: $THRESHOLD%)"
        echo -e "  Status: ${GREEN}PASS${NC}"
    else
        echo -e "  Final Score: ${RED}$FINAL_SCORE%${NC} (threshold: $THRESHOLD%)"
        echo -e "  Status: ${RED}FAIL${NC}"
    fi

    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
fi

# Exit code
[[ "$STATUS" == "PASS" ]] && exit 0 || exit 1
