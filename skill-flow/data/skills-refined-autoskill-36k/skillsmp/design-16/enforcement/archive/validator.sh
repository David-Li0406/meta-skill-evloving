#!/bin/bash
# validator.sh - LLM-Powered Invariant Validator v2.0
#
# Uses Claude with Chain-of-Thought reasoning to validate specs against invariants.
# No regex pattern matching - pure semantic understanding.
#
# Usage:
#   ./validator.sh <spec-file> [--domain <domain>] [--threshold 95]

set -e

VERSION="2.0.0"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOMAINS_DIR="$SCRIPT_DIR/../domains"
INVARIANTS_FILE="$SCRIPT_DIR/../system-invariants.md"

# Defaults
MODEL="sonnet"
THRESHOLD=95
DOMAIN=""
JSON_OUTPUT=false
FIX_MODE=false
VERBOSE=false

usage() {
    echo "Usage: $0 <spec-file> [options]"
    echo ""
    echo "LLM-powered invariant validation with Chain-of-Thought reasoning."
    echo ""
    echo "Options:"
    echo "  --domain <name>    Domain invariants (consumer, integration, etc.)"
    echo "  --threshold <N>    Pass threshold 0-100 (default: 95)"
    echo "  --model <model>    haiku (fast), sonnet (default), opus (thorough)"
    echo "  --json             Output JSON only"
    echo "  --fix              Generate fixed spec with violations resolved"
    echo "  --verbose          Show reasoning process"
    echo ""
    echo "Examples:"
    echo "  $0 specs/feature.md"
    echo "  $0 specs/api.md --domain integration --threshold 90"
    echo "  $0 specs/api.md --fix  # Generate fixed version"
    exit 1
}

check_claude_cli() {
    command -v claude &> /dev/null || { echo -e "${RED}ERROR: Claude CLI not found.${NC}" >&2; exit 1; }
}

call_claude() {
    local prompt="$1"
    local model="$2"
    local model_flag=""
    case "$model" in
        "haiku") model_flag="--model claude-3-5-haiku-latest" ;;
        "sonnet") model_flag="--model claude-sonnet-4-20250514" ;;
        "opus") model_flag="--model claude-opus-4-20250514" ;;
    esac
    echo "$prompt" | claude $model_flag --print 2>/dev/null
}

# Parse arguments
SPEC_FILE=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --domain) DOMAIN="$2"; shift 2 ;;
        --threshold) THRESHOLD="$2"; shift 2 ;;
        --model) MODEL="$2"; shift 2 ;;
        --json) JSON_OUTPUT=true; shift ;;
        --fix) FIX_MODE=true; shift ;;
        --verbose) VERBOSE=true; shift ;;
        --help|-h) usage ;;
        --version) echo "validator.sh version $VERSION"; exit 0 ;;
        -*)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
        *)
            [[ -z "$SPEC_FILE" ]] && SPEC_FILE="$1" || { echo -e "${RED}Unknown argument: $1${NC}"; usage; }
            shift
            ;;
    esac
done

[[ -z "$SPEC_FILE" ]] && { echo -e "${RED}ERROR: Spec file required${NC}"; usage; }
[[ ! -f "$SPEC_FILE" ]] && { echo -e "${RED}ERROR: Spec not found: $SPEC_FILE${NC}"; exit 1; }

check_claude_cli

SPEC_CONTENT=$(cat "$SPEC_FILE")

# Load invariants
INVARIANTS=""
[[ -f "$INVARIANTS_FILE" ]] && INVARIANTS=$(cat "$INVARIANTS_FILE")

# Fallback embedded invariants if file not found
[[ -z "$INVARIANTS" ]] && INVARIANTS=$(cat << 'INV_END'
# System Invariants (Core 10)

## 1. Ambiguity is Invalid
Words like "properly", "easily", "good", "quality", "appropriate", "reasonable" are violations UNLESS they have: metric + threshold + measurement method defined.

## 2. State Must Be Explicit
Every action verb needs: before_state → action → after_state. No implicit state changes.

## 3. Emotional Intent Must Compile
"Feel confident", "feel safe" etc. must map to concrete mechanisms: emotion := specific_implementation

## 4. No Irreversible Without Recovery
Delete, destroy, drop operations need: recovery_mechanism + time_window

## 5. Execution Must Fail Loudly
No "gracefully", "silently", "try to continue". Errors need: detection + alerting + blocking

## 6. Scope Must Be Bounded
No unbounded "all", "everything", "entire". Need: max_count OR max_size OR pagination

## 7. Validation Must Be Executable
Every "ensure", "verify" needs: metric + threshold + measurement_method

## 8. Cost Boundaries Explicit
API calls, storage, compute need: limit + budget + circuit_breaker

## 9. Blast Radius Declared
Write operations need: affected_scope + dependencies + recovery_cost

## 10. Degradation Path Exists
External dependencies need: primary + fallback1 + fallback2 OR explicit_fail
INV_END
)

DOMAIN_INVARIANTS=""
if [[ -n "$DOMAIN" ]]; then
    DOMAIN_FILE="$DOMAINS_DIR/${DOMAIN}.md"
    [[ -f "$DOMAIN_FILE" ]] && DOMAIN_INVARIANTS=$(cat "$DOMAIN_FILE")
fi

[[ "$JSON_OUTPUT" == "false" ]] && {
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║      LLM-Powered Invariant Validator v$VERSION                   ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "Spec:      ${CYAN}$SPEC_FILE${NC}"
    echo -e "Domain:    ${CYAN}${DOMAIN:-universal}${NC}"
    echo -e "Threshold: ${CYAN}$THRESHOLD%${NC}"
    echo -e "Model:     ${CYAN}$MODEL${NC}"
    echo ""
}

# Build Rubric-Based Assessment prompt with Few-Shot Examples
# This approach is more effective than pure CoT for structured evaluation tasks
VALIDATE_PROMPT=$(cat << 'PROMPT_END'
You are validating a specification against system invariants using rubric-based assessment.

## Evaluation Method: Rubric + Few-Shot Examples

For each invariant, apply this rubric:
- **PASS (0 points)**: Requirement fully satisfied or not applicable
- **MINOR (-2 points)**: Wording could be clearer but intent is unambiguous
- **MAJOR (-5 points)**: Missing required element that affects execution
- **BLOCKER (-10 points)**: Fundamental violation that blocks implementation

## Invariants with Scoring Rubrics

{{INVARIANTS}}

{{DOMAIN_SECTION}}

## Few-Shot Examples

### Example 1: Ambiguity Violation (MAJOR)
**Spec text**: "The system should handle large files efficiently"
**Violation**: "large" and "efficiently" are undefined
**Fix**: "The system should handle files up to 100MB, processing at ≥10MB/sec, timeout after 30s"

### Example 2: NOT a Violation (Context Makes It Clear)
**Spec text**: "Upload limit: 10MB per file, max 50 files per batch, timeout 60s"
**Analysis**: All terms are quantified - this PASSES invariant #1 and #6
**Result**: PASS - do not flag this

### Example 3: State Violation (MAJOR)
**Spec text**: "User submits the order"
**Violation**: No before/after state defined
**Fix**: "User submits order: order.state DRAFT → SUBMITTED → triggers validation → on pass: CONFIRMED + email sent"

### Example 4: False Positive to Avoid
**Spec text**: "Ensure all tests pass before deployment"
**Analysis**: "all tests" in testing context is bounded (the test suite), not unbounded data
**Result**: PASS - this is acceptable usage

### Example 5: Degradation Path Missing (MAJOR)
**Spec text**: "Fetch product data from inventory API"
**Violation**: No fallback if API unavailable
**Fix**: "Fetch from inventory API (timeout: 3s) → fallback: cached data <1hr old → fallback: show 'unavailable' banner"

### Example 6: Proper Error Handling (PASS)
**Spec text**: "On validation failure: return HTTP 400 with error details, log to monitoring, block form submission"
**Analysis**: Error path is explicit with detection + response + blocking
**Result**: PASS

## Specification to Validate

{{SPEC_CONTENT}}

## Your Task

1. Read the entire spec first to understand context
2. For each invariant, apply the rubric:
   - Find relevant text (or note absence)
   - Compare against the rubric criteria
   - Score using the point system
   - If violation: quote exact text and provide specific fix
3. Calculate total score: Start at 100, subtract violation points
4. Be strict on real issues, lenient on false positives

## Output Format

```json
{
  "spec_file": "{{SPEC_FILENAME}}",
  "overall_score": <100 minus deductions>,
  "status": "<PASS if ≥95 | NEEDS_WORK if 80-94 | REJECTED if <80>",
  "summary": "<one sentence: what's good and what needs work>",
  "invariant_results": [
    {"id": 1, "name": "Ambiguity", "result": "PASS|MINOR|MAJOR|BLOCKER", "points_deducted": 0}
  ],
  "violations": [
    {
      "invariant_id": <number>,
      "invariant_name": "<name>",
      "severity": "<MINOR|MAJOR|BLOCKER>",
      "points": <-2|-5|-10>,
      "location": "<section name or line hint>",
      "violating_text": "<exact quote from spec>",
      "issue": "<why this violates the invariant>",
      "fix": "<specific replacement text>"
    }
  ],
  "strengths": ["<specific things done well>"],
  "confidence": <0.8-1.0>
}
```
PROMPT_END
)

# Substitute variables
VALIDATE_PROMPT="${VALIDATE_PROMPT//\{\{INVARIANTS\}\}/$INVARIANTS}"
VALIDATE_PROMPT="${VALIDATE_PROMPT//\{\{SPEC_CONTENT\}\}/$SPEC_CONTENT}"
VALIDATE_PROMPT="${VALIDATE_PROMPT//\{\{SPEC_FILENAME\}\}/$(basename "$SPEC_FILE")}"

if [[ -n "$DOMAIN_INVARIANTS" ]]; then
    DOMAIN_SECTION="## Domain-Specific Invariants ($DOMAIN)

$DOMAIN_INVARIANTS"
    VALIDATE_PROMPT="${VALIDATE_PROMPT//\{\{DOMAIN_SECTION\}\}/$DOMAIN_SECTION}"
else
    VALIDATE_PROMPT="${VALIDATE_PROMPT//\{\{DOMAIN_SECTION\}\}/}"
fi

[[ "$JSON_OUTPUT" == "false" ]] && echo -e "${BLUE}Analyzing with Chain-of-Thought reasoning...${NC}"

RESULT=$(call_claude "$VALIDATE_PROMPT" "$MODEL")

[[ "$VERBOSE" == "true" ]] && {
    echo ""
    echo -e "${MAGENTA}━━━ LLM Reasoning ━━━${NC}"
    echo "$RESULT" | grep -A 1000 '<reasoning>' | grep -B 1000 '</reasoning>' | head -100
    echo "..."
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Extract JSON
RESULT_JSON=$(echo "$RESULT" | sed -n '/```json/,/```/p' | sed '1d;$d')
[[ -z "$RESULT_JSON" ]] && RESULT_JSON=$(echo "$RESULT" | grep -o '{.*}' | tail -1)

# Parse results
SCORE=$(echo "$RESULT_JSON" | grep -o '"overall_score":\s*[0-9]*' | grep -o '[0-9]*' | head -1)
STATUS=$(echo "$RESULT_JSON" | grep -o '"status":\s*"[^"]*"' | cut -d'"' -f4)
SUMMARY=$(echo "$RESULT_JSON" | grep -o '"summary":\s*"[^"]*"' | cut -d'"' -f4)

[[ -z "$SCORE" ]] && SCORE=0
[[ -z "$STATUS" ]] && STATUS="UNKNOWN"

PASSED=false
[[ $SCORE -ge $THRESHOLD ]] && PASSED=true

if [[ "$JSON_OUTPUT" == "true" ]]; then
    echo "$RESULT_JSON" | sed 's/}$/,"threshold":'"$THRESHOLD"',"passed":'"$PASSED"'}/'
else
    echo ""

    # Count violations by severity
    BLOCKERS=$(echo "$RESULT_JSON" | grep -o '"severity":\s*"BLOCKER"' | wc -l | tr -d ' ')
    MAJORS=$(echo "$RESULT_JSON" | grep -o '"severity":\s*"MAJOR"' | wc -l | tr -d ' ')
    MINORS=$(echo "$RESULT_JSON" | grep -o '"severity":\s*"MINOR"' | wc -l | tr -d ' ')
    WARNINGS=$(echo "$RESULT_JSON" | grep -o '"warnings":\s*\[' | wc -l | tr -d ' ')

    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

    if [[ $SCORE -ge $THRESHOLD ]]; then
        echo -e "  Score:  ${GREEN}$SCORE%${NC} (threshold: $THRESHOLD%)"
        echo -e "  Status: ${GREEN}PASS${NC}"
    elif [[ $SCORE -ge 80 ]]; then
        echo -e "  Score:  ${YELLOW}$SCORE%${NC} (threshold: $THRESHOLD%)"
        echo -e "  Status: ${YELLOW}NEEDS WORK${NC}"
    else
        echo -e "  Score:  ${RED}$SCORE%${NC} (threshold: $THRESHOLD%)"
        echo -e "  Status: ${RED}REJECTED${NC}"
    fi

    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""

    [[ -n "$SUMMARY" ]] && echo -e "${CYAN}Summary:${NC} $SUMMARY"
    echo ""

    TOTAL_VIOLATIONS=$((BLOCKERS + MAJORS + MINORS))
    if [[ $TOTAL_VIOLATIONS -gt 0 ]]; then
        echo -e "${BLUE}Violations:${NC}"
        [[ $BLOCKERS -gt 0 ]] && echo -e "  ${RED}Blockers: $BLOCKERS${NC}"
        [[ $MAJORS -gt 0 ]] && echo -e "  ${YELLOW}Major: $MAJORS${NC}"
        [[ $MINORS -gt 0 ]] && echo -e "  Minor: $MINORS"
        echo ""

        # Show violation details
        echo -e "${BLUE}Violation Details:${NC}"
        echo "$RESULT_JSON" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for i, v in enumerate(data.get('violations', []), 1):
        sev = v.get('severity', 'UNKNOWN')
        color = '\033[0;31m' if sev == 'BLOCKER' else '\033[1;33m' if sev == 'MAJOR' else '\033[0m'
        reset = '\033[0m'
        inv_name = v.get('invariant_name', v.get('invariant_id', 'Unknown'))
        print(f\"{color}{i}. [{sev}] #{v.get('invariant_id', '?')} - {inv_name}{reset}\")
        if v.get('violating_text'):
            print(f\"   Text: \\\"{v.get('violating_text')[:60]}...\\\"\")
        print(f\"   Issue: {v.get('issue', 'No description')}\")
        print(f\"   Fix: {v.get('fix', 'No suggestion')}\")
        print()
except Exception as e:
    print(f'JSON parse error: {e}')
" 2>/dev/null || echo "$RESULT_JSON"
        echo ""
    else
        echo -e "${GREEN}No violations found!${NC}"
        echo ""
    fi

    # Show strengths
    STRENGTHS=$(echo "$RESULT_JSON" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for s in data.get('strengths', [])[:3]:
        print(f'  + {s}')
except:
    pass
" 2>/dev/null)
    if [[ -n "$STRENGTHS" ]]; then
        echo -e "${GREEN}Strengths:${NC}"
        echo "$STRENGTHS"
        echo ""
    fi

    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

    # Generate fixed spec if requested
    if [[ "$FIX_MODE" == "true" ]] && [[ $TOTAL_VIOLATIONS -gt 0 ]]; then
        echo ""
        echo -e "${BLUE}Generating fixed specification...${NC}"

        FIX_PROMPT=$(cat << 'FIX_END'
You are fixing a specification to resolve all invariant violations.

## Original Specification
{{SPEC_CONTENT}}

## Violations to Fix
{{VIOLATIONS_JSON}}

## Instructions
1. Apply ALL fixes from the violations list
2. Keep the original structure and sections intact
3. Only change what's necessary to fix violations
4. Make fixes concrete and specific (metrics, thresholds, state transitions)
5. Don't add unnecessary content

Output the COMPLETE fixed specification in markdown:
FIX_END
)
        FIX_PROMPT="${FIX_PROMPT//\{\{SPEC_CONTENT\}\}/$SPEC_CONTENT}"
        FIX_PROMPT="${FIX_PROMPT//\{\{VIOLATIONS_JSON\}\}/$RESULT_JSON}"

        FIXED_SPEC=$(call_claude "$FIX_PROMPT" "sonnet")
        FIXED_SPEC=$(echo "$FIXED_SPEC" | sed '/^```markdown$/d' | sed '/^```$/d')

        FIXED_FILE="${SPEC_FILE%.md}-fixed.md"
        echo "$FIXED_SPEC" > "$FIXED_FILE"

        echo -e "${GREEN}   ✓ Fixed spec saved to: $FIXED_FILE${NC}"
        echo ""

        ORIG_LINES=$(wc -l < "$SPEC_FILE" | tr -d ' ')
        FIXED_LINES=$(wc -l < "$FIXED_FILE" | tr -d ' ')
        echo -e "   Original: ${CYAN}$ORIG_LINES lines${NC}"
        echo -e "   Fixed:    ${CYAN}$FIXED_LINES lines${NC}"
        echo ""
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    fi
fi

[[ "$PASSED" == "true" ]] && exit 0 || exit 1
