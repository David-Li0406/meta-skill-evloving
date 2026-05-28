#!/bin/bash
# validator-llm.sh - LLM-powered intelligent invariant validator v2.0
#
# Uses Claude to semantically validate specs against invariants.
# Features:
#   - Chain-of-thought reasoning for accurate analysis
#   - Two-pass validation: quick scan + deep analysis
#   - Example-based prompting from real violations
#   - Automatic spec fix generation
#   - Parallel invariant checking support
#
# Usage:
#   ./validator-llm.sh <spec-file> [--domain <domain>] [--threshold 95]
#   ./validator-llm.sh <spec-file> --deep   # Use sonnet for thorough analysis
#   ./validator-llm.sh <spec-file> --fix    # Generate fixed spec

set -e

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
MODEL="haiku"
THRESHOLD=95
DOMAIN=""
JSON_OUTPUT=false
FIX_MODE=false
DEEP_MODE=false
TWO_PASS=false
VERBOSE=false

usage() {
    echo "Usage: $0 <spec-file> [options]"
    echo ""
    echo "LLM-powered invariant validation with semantic understanding."
    echo ""
    echo "Options:"
    echo "  --domain <name>    Domain invariants to include (consumer, api, etc.)"
    echo "  --threshold <N>    Pass threshold 0-100 (default: 95)"
    echo "  --model <model>    haiku (default/fast), sonnet, opus"
    echo "  --deep             Use sonnet for thorough analysis (overrides --model)"
    echo "  --two-pass         Quick scan with haiku, deep analysis with sonnet on violations"
    echo "  --json             Output JSON only"
    echo "  --fix              Generate fixed spec with violations resolved"
    echo "  --verbose          Show reasoning process"
    echo ""
    echo "Examples:"
    echo "  $0 specs/feature.md"
    echo "  $0 specs/api.md --domain integration --threshold 90"
    echo "  $0 specs/api.md --deep --fix    # Thorough analysis + generate fixes"
    echo "  $0 specs/api.md --two-pass      # Fast scan, deep dive on issues"
    exit 1
}

check_claude_cli() {
    command -v claude &> /dev/null || { echo -e "${RED}ERROR: Claude CLI not found.${NC}" >&2; exit 1; }
}

call_claude() {
    local prompt="$1"
    local model_flag=""
    case "$MODEL" in
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
        --domain) DOMAIN="$2"; shift 2 ;;
        --threshold) THRESHOLD="$2"; shift 2 ;;
        --model) MODEL="$2"; shift 2 ;;
        --deep) DEEP_MODE=true; MODEL="sonnet"; shift ;;
        --two-pass) TWO_PASS=true; shift ;;
        --json) JSON_OUTPUT=true; shift ;;
        --fix) FIX_MODE=true; shift ;;
        --verbose) VERBOSE=true; shift ;;
        *) echo -e "${RED}Unknown option: $1${NC}"; usage ;;
    esac
done

[[ ! -f "$SPEC_FILE" ]] && { echo -e "${RED}ERROR: Spec not found: $SPEC_FILE${NC}"; exit 1; }

check_claude_cli

SPEC_CONTENT=$(cat "$SPEC_FILE")

# Load invariants
UNIVERSAL_INVARIANTS=""
[[ -f "$INVARIANTS_FILE" ]] && UNIVERSAL_INVARIANTS=$(cat "$INVARIANTS_FILE")

DOMAIN_INVARIANTS=""
if [[ -n "$DOMAIN" ]]; then
    DOMAIN_FILE="$DOMAINS_DIR/${DOMAIN}.md"
    [[ -f "$DOMAIN_FILE" ]] && DOMAIN_INVARIANTS=$(cat "$DOMAIN_FILE")
fi

# If no invariants files, use embedded
[[ -z "$UNIVERSAL_INVARIANTS" ]] && UNIVERSAL_INVARIANTS=$(cat << 'INVARIANTS'
# System Invariants

## 1. Ambiguity is Invalid
Words like "properly", "appropriate", "reasonable", "fast", "secure" are violations unless quantified with metric + threshold + measurement.

## 2. State Must Be Explicit
All state transitions documented. Entry/exit conditions defined. No implicit state changes.

## 3. Emotional Intent Must Compile
User feelings must map to concrete mechanisms. "Feel confident" → show success rate + undo option.

## 4. No Irreversible Without Recovery
Destructive operations need rollback plans. Data deletion needs recovery strategy.

## 5. Execution Must Fail Loudly
Errors surface clearly. No silent failures. Explicit error handling.

## 6. Scope Must Be Bounded
Clear in-scope/out-of-scope. No unbounded work. Explicit "NOT doing" section.

## 7. Validation Must Be Executable
Every requirement has concrete test. "User can X" has verification steps.

## 8. Cost Boundaries Explicit
Time, money, compute costs have explicit bounds. No "reasonable cost".

## 9. Blast Radius Declared
Dependencies, downstream effects, rollback procedures documented.

## 10. Degradation Path Exists
What happens when dependencies fail? Graceful degradation required.
INVARIANTS
)

[[ "$JSON_OUTPUT" == "false" ]] && {
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║           LLM-Powered Invariant Validator                     ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "Spec:      ${CYAN}$SPEC_FILE${NC}"
    echo -e "Domain:    ${CYAN}${DOMAIN:-universal}${NC}"
    echo -e "Threshold: ${CYAN}$THRESHOLD%${NC}"
    echo ""
}

# Build validation prompt with chain-of-thought reasoning
VALIDATE_PROMPT=$(cat << 'PROMPT_END'
You are an expert specification validator enforcing a strict invariant system. Your job is to catch problems BEFORE they become expensive failures in execution.

## Your Validation Framework

You will use chain-of-thought reasoning to analyze each invariant:

1. **Understand the invariant's intent** - What class of problems does it prevent?
2. **Scan the spec for potential violations** - Look for patterns, keywords, and missing elements
3. **Analyze context** - Is this actually a violation or acceptable in context?
4. **Determine severity** - BLOCKER (blocks execution), MAJOR (significant risk), MINOR (should fix)
5. **Provide actionable fix** - Specific text replacement, not vague advice

## Invariants to Enforce

{{INVARIANTS}}

{{DOMAIN_SECTION}}

## Specification to Validate

{{SPEC_CONTENT}}

## Validation Examples

Here are examples of correct violation detection:

**Example 1 - Ambiguity Violation:**
- Spec text: "Ensure the system handles errors properly"
- Violation: "properly" is subjective without criteria
- Fix: "Ensure the system: (1) logs errors with stack trace to CloudWatch, (2) returns HTTP 5xx with error code, (3) triggers PagerDuty alert for >10 errors/min"

**Example 2 - False Positive (NOT a violation):**
- Spec text: "Upload limit: 10MB per file, max 50 files per batch"
- Analysis: This IS bounded (specific limits given)
- Result: No violation - scope is explicit

**Example 3 - State Violation:**
- Spec text: "User submits the form"
- Violation: No before-state or after-state defined
- Fix: "User submits form: form.state changes from EDITING → SUBMITTED → triggers validation_job → on success: form.state = CONFIRMED + email_sent"

**Example 4 - Missing Degradation Path:**
- Spec text: "Fetch weather data from OpenWeather API"
- Violation: No fallback if API fails
- Fix: "Fetch weather from OpenWeather API (timeout: 3s) → fallback: cached_data_<24h_old → fallback: show 'Weather unavailable' + allow manual override"

## Your Analysis Process

Think through each invariant systematically:

<analysis>
For Invariant #1 (Ambiguity):
- Scanning for: "properly", "easily", "quality", "appropriate", "reasonable", "fast", "secure", "good"
- Found: [list any found]
- Context check: [is it defined with metrics nearby?]
- Verdict: [PASS/VIOLATION with evidence]

For Invariant #2 (State):
- Scanning for: verbs without state transitions
- Found actions: [list actions]
- State transitions defined? [yes/no for each]
- Verdict: [PASS/VIOLATION with evidence]

[Continue for all 10 invariants...]
</analysis>

## Scoring Guide

- **95-100**: No violations, exemplary spec
- **85-94**: Minor wording issues only (easily fixed)
- **75-84**: Some missing details but core is solid
- **60-74**: Significant gaps that need work
- **<60**: Major violations, needs rewrite

## Output Format

After your analysis, output ONLY this JSON (no other text):

```json
{
  "spec_file": "{{SPEC_FILE}}",
  "overall_score": 0-100,
  "status": "PASS|NEEDS_WORK|REJECTED",
  "summary": "One sentence assessment",
  "analysis_notes": "Brief reasoning for score",
  "violations": [
    {
      "invariant": "#N - Invariant Name",
      "severity": "BLOCKER|MAJOR|MINOR",
      "location": "Section: X / Line containing: 'quoted text'",
      "violating_text": "exact quoted text from spec",
      "issue": "Clear explanation of the problem",
      "fix": "Specific replacement text or addition"
    }
  ],
  "strengths": ["What the spec does well - be specific"],
  "recommendations": ["Optional improvements beyond violations"],
  "confidence": 0.0-1.0
}
```
PROMPT_END
)

VALIDATE_PROMPT="${VALIDATE_PROMPT//\{\{INVARIANTS\}\}/$UNIVERSAL_INVARIANTS}"
VALIDATE_PROMPT="${VALIDATE_PROMPT//\{\{SPEC_FILE\}\}/$(basename "$SPEC_FILE")}"

if [[ -n "$DOMAIN_INVARIANTS" ]]; then
    DOMAIN_SECTION="DOMAIN-SPECIFIC INVARIANTS ($DOMAIN):
$DOMAIN_INVARIANTS"
    VALIDATE_PROMPT="${VALIDATE_PROMPT//\{\{DOMAIN_SECTION\}\}/$DOMAIN_SECTION}"
else
    VALIDATE_PROMPT="${VALIDATE_PROMPT//\{\{DOMAIN_SECTION\}\}/}"
fi

VALIDATE_PROMPT="${VALIDATE_PROMPT//\{\{SPEC_CONTENT\}\}/$SPEC_CONTENT}"

# Two-pass validation: quick scan first, then deep analysis on violations
if [[ "$TWO_PASS" == "true" ]]; then
    [[ "$JSON_OUTPUT" == "false" ]] && echo -e "${BLUE}Pass 1: Quick scan with haiku...${NC}"

    QUICK_RESULT=$(echo "$VALIDATE_PROMPT" | claude --model claude-3-5-haiku-latest --print 2>/dev/null)
    QUICK_JSON=$(echo "$QUICK_RESULT" | sed -n '/```json/,/```/p' | sed '1d;$d')
    [[ -z "$QUICK_JSON" ]] && QUICK_JSON=$(echo "$QUICK_RESULT" | grep -o '{.*}')

    QUICK_SCORE=$(echo "$QUICK_JSON" | grep -o '"overall_score":\s*[0-9]*' | grep -o '[0-9]*' | head -1)
    [[ -z "$QUICK_SCORE" ]] && QUICK_SCORE=0

    [[ "$JSON_OUTPUT" == "false" ]] && echo -e "${CYAN}   Quick score: $QUICK_SCORE%${NC}"

    # If quick scan found issues, do deep analysis
    if [[ $QUICK_SCORE -lt $THRESHOLD ]]; then
        [[ "$JSON_OUTPUT" == "false" ]] && echo -e "${BLUE}Pass 2: Deep analysis with sonnet...${NC}"
        MODEL="sonnet"
        RESULT=$(call_claude "$VALIDATE_PROMPT")
    else
        RESULT="$QUICK_RESULT"
    fi
else
    [[ "$JSON_OUTPUT" == "false" ]] && {
        if [[ "$DEEP_MODE" == "true" ]]; then
            echo -e "${BLUE}Deep validation with sonnet...${NC}"
        else
            echo -e "${BLUE}Validating...${NC}"
        fi
    }
    RESULT=$(call_claude "$VALIDATE_PROMPT")
fi

[[ "$VERBOSE" == "true" ]] && {
    echo -e "${MAGENTA}Raw LLM response:${NC}"
    echo "$RESULT" | head -50
    echo "..."
    echo ""
}

# Extract JSON
RESULT_JSON=$(echo "$RESULT" | sed -n '/```json/,/```/p' | sed '1d;$d')
[[ -z "$RESULT_JSON" ]] && RESULT_JSON=$(echo "$RESULT" | grep -o '{.*}')

# Parse results
SCORE=$(echo "$RESULT_JSON" | grep -o '"overall_score":\s*[0-9]*' | grep -o '[0-9]*' | head -1)
STATUS=$(echo "$RESULT_JSON" | grep -o '"status":\s*"[^"]*"' | cut -d'"' -f4)
SUMMARY=$(echo "$RESULT_JSON" | grep -o '"summary":\s*"[^"]*"' | cut -d'"' -f4)

[[ -z "$SCORE" ]] && SCORE=0
[[ -z "$STATUS" ]] && STATUS="UNKNOWN"

# Determine pass/fail against threshold
PASSED=false
[[ $SCORE -ge $THRESHOLD ]] && PASSED=true

if [[ "$JSON_OUTPUT" == "true" ]]; then
    # Add threshold info to JSON
    echo "$RESULT_JSON" | sed 's/}$/,"threshold":'"$THRESHOLD"',"passed":'"$PASSED"'}/'
else
    echo ""

    # Count violations by severity
    BLOCKERS=$(echo "$RESULT_JSON" | grep -o '"severity":\s*"BLOCKER"' | wc -l | tr -d ' ')
    MAJORS=$(echo "$RESULT_JSON" | grep -o '"severity":\s*"MAJOR"' | wc -l | tr -d ' ')
    MINORS=$(echo "$RESULT_JSON" | grep -o '"severity":\s*"MINOR"' | wc -l | tr -d ' ')

    # Display results
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

    # Violations summary
    TOTAL_VIOLATIONS=$((BLOCKERS + MAJORS + MINORS))
    if [[ $TOTAL_VIOLATIONS -gt 0 ]]; then
        echo -e "${BLUE}Violations:${NC}"
        [[ $BLOCKERS -gt 0 ]] && echo -e "  ${RED}Blockers: $BLOCKERS${NC}"
        [[ $MAJORS -gt 0 ]] && echo -e "  ${YELLOW}Major: $MAJORS${NC}"
        [[ $MINORS -gt 0 ]] && echo -e "  Minor: $MINORS"
        echo ""
    else
        echo -e "${GREEN}No violations found!${NC}"
        echo ""
    fi

    # Show detailed violations
    if [[ $TOTAL_VIOLATIONS -gt 0 ]]; then
        echo -e "${BLUE}Violation Details:${NC}"
        echo "$RESULT_JSON" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for i, v in enumerate(data.get('violations', []), 1):
        sev = v.get('severity', 'UNKNOWN')
        color = '\033[0;31m' if sev == 'BLOCKER' else '\033[1;33m' if sev == 'MAJOR' else '\033[0m'
        reset = '\033[0m'
        print(f\"{color}{i}. [{sev}] {v.get('invariant', 'Unknown')}{reset}\")
        print(f\"   Location: {v.get('location', 'Unknown')}\")
        print(f\"   Issue: {v.get('issue', 'No description')}\")
        print(f\"   Fix: {v.get('fix', 'No suggestion')}\")
        print()
except:
    pass
" 2>/dev/null || echo "$RESULT_JSON"
        echo ""
    fi

    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

    # Generate fixed spec if requested
    if [[ "$FIX_MODE" == "true" ]] && [[ $TOTAL_VIOLATIONS -gt 0 ]]; then
        echo ""
        echo -e "${BLUE}Generating fixed specification...${NC}"

        FIX_PROMPT=$(cat << 'FIX_END'
You are fixing a specification to resolve invariant violations.

ORIGINAL SPECIFICATION:
{{SPEC_CONTENT}}

VIOLATIONS TO FIX:
{{VIOLATIONS_JSON}}

Instructions:
1. Apply ALL suggested fixes from the violations list
2. Preserve the original structure and intent
3. Do not remove content that wasn't flagged
4. Ensure fixes are concrete and specific (metrics, thresholds, state transitions)
5. Output the COMPLETE fixed specification

Output the fixed specification in markdown (no code blocks wrapping the entire spec):
FIX_END
)
        FIX_PROMPT="${FIX_PROMPT//\{\{SPEC_CONTENT\}\}/$SPEC_CONTENT}"
        FIX_PROMPT="${FIX_PROMPT//\{\{VIOLATIONS_JSON\}\}/$RESULT_JSON}"

        FIXED_SPEC=$(echo "$FIX_PROMPT" | claude --model claude-sonnet-4-20250514 --print 2>/dev/null)
        FIXED_SPEC=$(echo "$FIXED_SPEC" | sed '/^```markdown$/d' | sed '/^```$/d')

        # Save fixed spec
        FIXED_FILE="${SPEC_FILE%.md}-fixed.md"
        echo "$FIXED_SPEC" > "$FIXED_FILE"

        echo -e "${GREEN}   ✓ Fixed spec saved to: $FIXED_FILE${NC}"
        echo ""

        # Show diff summary
        ORIG_LINES=$(wc -l < "$SPEC_FILE" | tr -d ' ')
        FIXED_LINES=$(wc -l < "$FIXED_FILE" | tr -d ' ')
        echo -e "   Original: ${CYAN}$ORIG_LINES lines${NC}"
        echo -e "   Fixed:    ${CYAN}$FIXED_LINES lines${NC}"
        echo ""
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    fi
fi

# Exit code
[[ "$PASSED" == "true" ]] && exit 0 || exit 1
