#!/bin/bash
# prp-checker.sh - LLM-Powered PRP Quality Checker v2.0
#
# Uses Claude with Rubric-Based Assessment to validate PRP quality.
# No regex pattern matching - semantic understanding of quality.
#
# Usage:
#   ./prp-checker.sh <prp-file> [--threshold 90] [--fix]

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

# Defaults
MODEL="sonnet"
THRESHOLD=90
JSON_OUTPUT=false
FIX_MODE=false
VERBOSE=false

usage() {
    echo "Usage: $0 <prp-file> [options]"
    echo ""
    echo "LLM-powered PRP quality assessment with rubric-based scoring."
    echo ""
    echo "Options:"
    echo "  --threshold <N>   Pass threshold 0-100 (default: 90)"
    echo "  --model <model>   haiku (fast), sonnet (default), opus"
    echo "  --json            Output JSON only"
    echo "  --fix             Generate improved PRP with issues fixed"
    echo "  --verbose         Show detailed assessment"
    echo ""
    echo "Examples:"
    echo "  $0 PRPs/feature-prp.md"
    echo "  $0 PRPs/feature-prp.md --threshold 95 --fix"
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
PRP_FILE=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --threshold) THRESHOLD="$2"; shift 2 ;;
        --model) MODEL="$2"; shift 2 ;;
        --json) JSON_OUTPUT=true; shift ;;
        --fix) FIX_MODE=true; shift ;;
        --verbose) VERBOSE=true; shift ;;
        --help|-h) usage ;;
        --version) echo "prp-checker.sh version $VERSION"; exit 0 ;;
        -*)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
        *)
            [[ -z "$PRP_FILE" ]] && PRP_FILE="$1" || { echo -e "${RED}Unknown argument: $1${NC}"; usage; }
            shift
            ;;
    esac
done

[[ -z "$PRP_FILE" ]] && { echo -e "${RED}ERROR: PRP file required${NC}"; usage; }
[[ ! -f "$PRP_FILE" ]] && { echo -e "${RED}ERROR: PRP not found: $PRP_FILE${NC}"; exit 1; }

check_claude_cli

PRP_CONTENT=$(cat "$PRP_FILE")

[[ "$JSON_OUTPUT" == "false" ]] && {
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║        LLM-Powered PRP Quality Checker v$VERSION                 ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "PRP:       ${CYAN}$PRP_FILE${NC}"
    echo -e "Threshold: ${CYAN}$THRESHOLD%${NC}"
    echo -e "Model:     ${CYAN}$MODEL${NC}"
    echo ""
}

# Build Rubric-Based Assessment prompt
CHECK_PROMPT=$(cat << 'PROMPT_END'
You are assessing the quality of a Product Requirements Prompt (PRP) using rubric-based scoring.

## PRP Quality Dimensions

Score each dimension 0-20 points:

### 1. COMPLETENESS (0-20 points)
- **20**: All sections present and thoroughly detailed
- **15**: All required sections present, some could be expanded
- **10**: Missing 1-2 sections or major gaps in content
- **5**: Missing multiple required sections
- **0**: Skeleton only, not usable

Required sections: Meta, Overview, Success Criteria, Timeline with Gates, Risks, Resources, Validation Commands

### 2. SPECIFICITY (0-20 points)
- **20**: All metrics have numbers, no vague terms, concrete criteria
- **15**: Most metrics specific, 1-2 vague terms
- **10**: Mix of specific and vague, some placeholders
- **5**: Mostly vague language, many placeholders
- **0**: No specific metrics, all hand-wavy

Check for: "properly", "efficiently", "good quality", "[FILL_IN]", "TBD"

### 3. EXECUTABILITY (0-20 points)
- **20**: Engineer could start immediately, all decisions made
- **15**: Minor clarifications needed, mostly executable
- **10**: Some ambiguity about approach or order
- **5**: Significant decisions still needed
- **0**: Cannot determine what to actually do

Check: Clear phases, task breakdowns, validation commands that actually run

### 4. TESTABILITY (0-20 points)
- **20**: Every requirement has concrete pass/fail criteria
- **15**: Most requirements testable, few subjective
- **10**: Mix of testable and subjective criteria
- **5**: Most criteria are subjective
- **0**: No way to verify completion

Check: Validation gates, success metrics, bash commands

### 5. STRUCTURE (0-20 points)
- **20**: Professional format, tables, checklists, state diagrams
- **15**: Well-organized, uses markdown effectively
- **10**: Readable but could be better organized
- **5**: Hard to navigate, inconsistent formatting
- **0**: Unstructured text dump

Check: Markdown tables, checkboxes, headers, clear sections

## Few-Shot Examples

### Example: High Score (95+)
```
## Success Criteria
- Response time: <200ms p95 (measured via DataDog APM)
- Error rate: <0.1% over 24hr rolling window
- User satisfaction: NPS ≥50 (measured in post-deploy survey)

## Validation Gate 1
GATE_1_PASS := unit_tests_pass AND coverage ≥ 80% AND lint_score = 0
```
**Score**: High specificity (numbers), high testability (clear pass/fail)

### Example: Low Score (60-)
```
## Success Criteria
- System should work properly
- Users should be satisfied
- Performance should be good

## Timeline
- Phase 1: Build stuff
- Phase 2: Test and fix
```
**Score**: Low specificity (vague), low testability (how to measure?), low executability (what exactly to build?)

### Example: Missing Section (Major Deduction)
PRP has no Risk Assessment section
**Score**: -15 from completeness, overall cap at 85

## PRP to Assess

{{PRP_CONTENT}}

## Your Assessment

1. Score each dimension independently
2. Note specific issues with exact quotes
3. **CRITICAL**: Distinguish between PRP-level issues (fixable in PRP) and SPEC-level issues (require source spec changes)
4. Calculate total (sum of 5 dimensions, max 100)

## Issue Classification

**SPEC-LEVEL issues** (require going back to source spec):
- Success criteria undefined in source → can't invent metrics
- Scope boundaries unclear → can't determine what's in/out
- User requirements missing → can't specify behavior
- Technical constraints not stated → can't make architecture decisions

**PRP-LEVEL issues** (fixable in PRP without spec changes):
- Missing section that can be derived from existing spec content
- Formatting/structure problems
- Placeholders that have answers elsewhere in PRP
- Validation commands not written but requirements are clear

## Output Format

```json
{
  "prp_file": "{{PRP_FILENAME}}",
  "overall_score": <sum of dimensions, 0-100>,
  "status": "<PASS if ≥threshold | NEEDS_WORK if 70-threshold | REJECTED if <70>",
  "dimensions": {
    "completeness": {"score": <0-20>, "notes": "<assessment>"},
    "specificity": {"score": <0-20>, "notes": "<assessment>"},
    "executability": {"score": <0-20>, "notes": "<assessment>"},
    "testability": {"score": <0-20>, "notes": "<assessment>"},
    "structure": {"score": <0-20>, "notes": "<assessment>"}
  },
  "issues": [
    {
      "dimension": "<which dimension>",
      "severity": "<BLOCKER|MAJOR|MINOR>",
      "location": "<section or quoted text>",
      "problem": "<what's wrong>",
      "fix": "<specific improvement>"
    }
  ],
  "spec_issues": [
    {
      "severity": "<BLOCKER|MAJOR>",
      "problem": "<what the source spec is missing>",
      "spec_fix": "<what needs to be added to the source spec>",
      "why_spec_level": "<why this can't be fixed in PRP alone>"
    }
  ],
  "has_spec_issues": <true if spec_issues is non-empty, false otherwise>,
  "missing_sections": ["<list any missing required sections>"],
  "placeholder_count": <number of [FILL_IN] or {{}} found>,
  "strengths": ["<what the PRP does well>"],
  "summary": "<one sentence overall assessment>"
}
```
PROMPT_END
)

CHECK_PROMPT="${CHECK_PROMPT//\{\{PRP_CONTENT\}\}/$PRP_CONTENT}"
CHECK_PROMPT="${CHECK_PROMPT//\{\{PRP_FILENAME\}\}/$(basename "$PRP_FILE")}"

[[ "$JSON_OUTPUT" == "false" ]] && echo -e "${BLUE}Assessing PRP quality...${NC}"

RESULT=$(call_claude "$CHECK_PROMPT" "$MODEL")

[[ "$VERBOSE" == "true" ]] && {
    echo ""
    echo -e "${MAGENTA}━━━ Full Assessment ━━━${NC}"
    echo "$RESULT" | head -80
    echo "..."
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Extract JSON
RESULT_JSON=$(echo "$RESULT" | sed -n '/```json/,/```/p' | sed '1d;$d')
[[ -z "$RESULT_JSON" ]] && RESULT_JSON=$(echo "$RESULT" | grep -o '{.*}' | tail -1)

# Parse results
SCORE=$(echo "$RESULT_JSON" | grep -o '"overall_score":\s*[0-9]*' | grep -o '[0-9]*' | head -1)
STATUS=$(echo "$RESULT_JSON" | grep -o '"status":\s*"[^"]*"' | cut -d'"' -f4)
SUMMARY=$(echo "$RESULT_JSON" | grep -o '"summary":\s*"[^"]*"' | cut -d'"' -f4)
PLACEHOLDERS=$(echo "$RESULT_JSON" | grep -o '"placeholder_count":\s*[0-9]*' | grep -o '[0-9]*' | head -1)
HAS_SPEC_ISSUES=$(echo "$RESULT_JSON" | grep -o '"has_spec_issues":\s*true' | head -1)

[[ -z "$SCORE" ]] && SCORE=0
[[ -z "$STATUS" ]] && STATUS="UNKNOWN"
[[ -z "$PLACEHOLDERS" ]] && PLACEHOLDERS=0
[[ -n "$HAS_SPEC_ISSUES" ]] && HAS_SPEC_ISSUES="true" || HAS_SPEC_ISSUES="false"

PASSED=false
[[ $SCORE -ge $THRESHOLD ]] && PASSED=true

if [[ "$JSON_OUTPUT" == "true" ]]; then
    echo "$RESULT_JSON" | sed 's/}$/,"threshold":'"$THRESHOLD"',"passed":'"$PASSED"',"has_spec_issues":'"$HAS_SPEC_ISSUES"'}/'
else
    echo ""

    # Display dimension scores
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "  ${CYAN}Dimension Scores${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""

    echo "$RESULT_JSON" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    dims = data.get('dimensions', {})
    for name, info in dims.items():
        score = info.get('score', 0)
        max_score = 20
        bar_len = int(score / max_score * 20)
        bar = '█' * bar_len + '░' * (20 - bar_len)
        color = '\033[0;32m' if score >= 16 else '\033[1;33m' if score >= 12 else '\033[0;31m'
        reset = '\033[0m'
        print(f\"  {name.upper():15} {color}{bar} {score:2}/20{reset}\")
except Exception as e:
    print(f'Parse error: {e}')
" 2>/dev/null

    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

    if [[ $SCORE -ge $THRESHOLD ]]; then
        echo -e "  Overall Score: ${GREEN}$SCORE/100${NC} (threshold: $THRESHOLD)"
        echo -e "  Status:        ${GREEN}PASS${NC}"
    elif [[ $SCORE -ge 70 ]]; then
        echo -e "  Overall Score: ${YELLOW}$SCORE/100${NC} (threshold: $THRESHOLD)"
        echo -e "  Status:        ${YELLOW}NEEDS WORK${NC}"
    else
        echo -e "  Overall Score: ${RED}$SCORE/100${NC} (threshold: $THRESHOLD)"
        echo -e "  Status:        ${RED}REJECTED${NC}"
    fi

    [[ $PLACEHOLDERS -gt 0 ]] && echo -e "  Placeholders:  ${YELLOW}$PLACEHOLDERS unfilled${NC}"

    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""

    [[ -n "$SUMMARY" ]] && echo -e "${CYAN}Summary:${NC} $SUMMARY"
    echo ""

    # Show spec-level issues first (these block PRP fixes)
    if [[ "$HAS_SPEC_ISSUES" == "true" ]]; then
        echo -e "${RED}╔═══════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${RED}║  SPEC-LEVEL ISSUES DETECTED (require source spec changes)     ║${NC}"
        echo -e "${RED}╚═══════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo "$RESULT_JSON" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for i, issue in enumerate(data.get('spec_issues', []), 1):
        sev = issue.get('severity', 'MAJOR')
        print(f\"\033[0;31m{i}. [{sev}] {issue.get('problem', 'N/A')}\033[0m\")
        print(f\"   Spec fix: {issue.get('spec_fix', 'N/A')}\")
        print(f\"   Why spec-level: {issue.get('why_spec_level', 'N/A')}\")
        print()
except:
    pass
" 2>/dev/null
        echo -e "${YELLOW}⚠ These issues cannot be fixed in the PRP - source spec must be updated${NC}"
        echo ""
    fi

    # Show PRP-level issues
    ISSUE_COUNT=$(echo "$RESULT_JSON" | grep -o '"severity"' | wc -l | tr -d ' ')
    if [[ $ISSUE_COUNT -gt 0 ]]; then
        echo -e "${BLUE}Issues to Address:${NC}"
        echo "$RESULT_JSON" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for i, issue in enumerate(data.get('issues', [])[:5], 1):
        sev = issue.get('severity', 'UNKNOWN')
        color = '\033[0;31m' if sev == 'BLOCKER' else '\033[1;33m' if sev == 'MAJOR' else '\033[0m'
        reset = '\033[0m'
        print(f\"{color}{i}. [{sev}] {issue.get('dimension', 'General')}{reset}\")
        print(f\"   Problem: {issue.get('problem', 'N/A')}\")
        print(f\"   Fix: {issue.get('fix', 'N/A')}\")
        print()
except:
    pass
" 2>/dev/null
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

    # Generate improved PRP if requested
    if [[ "$FIX_MODE" == "true" ]] && [[ $SCORE -lt $THRESHOLD ]]; then
        echo ""
        echo -e "${BLUE}Generating improved PRP...${NC}"

        IMPROVE_PROMPT=$(cat << 'IMPROVE_END'
You are improving a PRP to fix the identified PRP-LEVEL quality issues.

## Current PRP
{{PRP_CONTENT}}

## Quality Assessment
{{ASSESSMENT_JSON}}

## Instructions
1. Fix ONLY the PRP-level issues in the "issues" array
2. DO NOT attempt to fix spec-level issues (in "spec_issues" array) - those require source spec changes
3. Keep the same overall structure
4. Replace vague terms with specific metrics WHERE the spec provides enough context
5. Fill in placeholders ONLY if the answer exists elsewhere in the PRP
6. Add missing sections if they can be derived from existing content
7. Ensure all validation gates have concrete pass/fail criteria

## Critical Rule
If a problem stems from missing information in the source spec (marked as spec_issues),
leave a clear placeholder like "[SPEC: needs success metric definition]" rather than
inventing values. This signals the spec needs updating.

Output the COMPLETE improved PRP in markdown:
IMPROVE_END
)
        IMPROVE_PROMPT="${IMPROVE_PROMPT//\{\{PRP_CONTENT\}\}/$PRP_CONTENT}"
        IMPROVE_PROMPT="${IMPROVE_PROMPT//\{\{ASSESSMENT_JSON\}\}/$RESULT_JSON}"

        IMPROVED_PRP=$(call_claude "$IMPROVE_PROMPT" "sonnet")
        IMPROVED_PRP=$(echo "$IMPROVED_PRP" | sed '/^```markdown$/d' | sed '/^```$/d')

        IMPROVED_FILE="${PRP_FILE%.md}-improved.md"
        echo "$IMPROVED_PRP" > "$IMPROVED_FILE"

        echo -e "${GREEN}   ✓ Improved PRP saved to: $IMPROVED_FILE${NC}"
        echo ""

        ORIG_LINES=$(wc -l < "$PRP_FILE" | tr -d ' ')
        IMPROVED_LINES=$(wc -l < "$IMPROVED_FILE" | tr -d ' ')
        echo -e "   Original: ${CYAN}$ORIG_LINES lines${NC}"
        echo -e "   Improved: ${CYAN}$IMPROVED_LINES lines${NC}"
        echo ""
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    fi
fi

[[ "$PASSED" == "true" ]] && exit 0 || exit 1
