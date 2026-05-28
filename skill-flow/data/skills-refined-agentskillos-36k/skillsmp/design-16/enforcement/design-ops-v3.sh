#!/bin/bash
# design-ops-v3.sh - Simplified Design Ops Pipeline
#
# Philosophy: LLM is ADVISORY, human decides. No auto-fix loops.
#
# Workflow (in order):
#   1. stress-test  - "Is the spec complete?" (coverage against requirements/journeys)
#   2. validate     - "Is the spec clear?" (structure, ambiguity)
#   3. generate     - Create PRP from spec (one-shot)
#   4. check        - Verify PRP quality
#   5. Human reviews and approves
#
# Usage:
#   ./design-ops-v3.sh stress-test <spec> [--requirements <file>]  # Coverage check (RUN FIRST)
#   ./design-ops-v3.sh validate <spec-file>                        # Clarity check
#   ./design-ops-v3.sh generate <spec-file>                        # Generate PRP
#   ./design-ops-v3.sh check <prp-file>                            # Check PRP quality
#   ./design-ops-v3.sh ralph-check <prp-file> --steps <dir>        # Validate implementation against PRP

set -e

VERSION="3.3.0"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
DIM='\033[2m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# PRP Generation Configuration
# Auto-detect base from script location (works for anyone cloning the repo)
DESIGN_OPS_BASE="${DESIGN_OPS_BASE:-$(dirname "$SCRIPT_DIR")}"
INVARIANTS_DIR="$DESIGN_OPS_BASE"
DOMAINS_DIR="$DESIGN_OPS_BASE/domains"
TEMPLATES_DIR="$DESIGN_OPS_BASE/templates"

# Model configuration (can be overridden via environment variable)
# Options: claude-sonnet-4-20250514, claude-opus-4-20250514, etc.
CLAUDE_MODEL="${CLAUDE_MODEL:-claude-sonnet-4-20250514}"

# Pipeline state directory (stores inter-command state)
PIPELINE_STATE_DIR="${PIPELINE_STATE_DIR:-$HOME/.design-ops-state}"

# =============================================================================
# PIPELINE STATE MANAGEMENT (continuity between commands)
# =============================================================================

# Get state file path for a spec
get_state_file_path() {
    local spec_file="$1"
    local spec_basename
    spec_basename=$(basename "$spec_file" .md)
    mkdir -p "$PIPELINE_STATE_DIR"
    echo "$PIPELINE_STATE_DIR/${spec_basename}.state.json"
}

# Read pipeline state (returns empty JSON object if no state)
read_pipeline_state() {
    local state_file="$1"
    if [[ -f "$state_file" ]]; then
        cat "$state_file"
    else
        echo '{}'
    fi
}

# Write pipeline state
write_pipeline_state() {
    local state_file="$1"
    local state_json="$2"
    echo "$state_json" > "$state_file"
}

# Update pipeline state with new command findings
# Usage: update_pipeline_state "$state_file" "stress-test" "$findings_json"
update_pipeline_state() {
    local state_file="$1"
    local command="$2"
    local findings="$3"
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

    local current_state
    current_state=$(read_pipeline_state "$state_file")

    # Use python for JSON manipulation (more reliable than jq dependency)
    local new_state
    new_state=$(python3 -c "
import json
import sys

current = json.loads('''$current_state''')
findings = json.loads('''$findings''')

current['$command'] = {
    'timestamp': '$timestamp',
    'findings': findings
}
current['last_updated'] = '$timestamp'
current['last_command'] = '$command'

print(json.dumps(current, indent=2))
" 2>/dev/null)

    if [[ -n "$new_state" ]]; then
        write_pipeline_state "$state_file" "$new_state"
    fi
}

# Get accumulated issues count from state (affects confidence)
get_accumulated_issues() {
    local state_file="$1"
    local state
    state=$(read_pipeline_state "$state_file")

    python3 -c "
import json
state = json.loads('''$state''')
issues = 0

# Count stress-test issues
st = state.get('stress-test', {}).get('findings', {})
issues += len(st.get('invariant_violations', []))
issues += len(st.get('critical_blockers', []))

# Count validate issues
v = state.get('validate', {}).get('findings', {})
issues += len(v.get('ambiguity_flags', []))

print(issues)
" 2>/dev/null || echo "0"
}

# Domain mapping function (bash 3.x compatible)
# Returns: file:start-end or empty if not found
get_domain_mapping() {
    local domain="$1"
    case "$domain" in
        "consumer product"|"consumer-product")
            echo "consumer-product.md:11-15" ;;
        "physical construction"|"physical-construction"|"construction")
            echo "physical-construction.md:16-21" ;;
        "data architecture"|"data-architecture"|"data")
            echo "data-architecture.md:22-26" ;;
        "integration")
            echo "integration.md:27-30" ;;
        "healthcare ai"|"healthcare-ai")
            echo "healthcare-ai.md:27-30" ;;
        "hls"|"hls solution accelerator"|"hls-solution-accelerator"|"databricks")
            echo "hls-solution-accelerator.md:31-38" ;;
        "remote management"|"remote-management"|"remote")
            echo "remote-management.md:31-36" ;;
        "skill gap"|"skill-gap"|"skill-gap-transcendence")
            echo "skill-gap-transcendence.md:37-43" ;;
        *)
            echo "" ;;
    esac
}

# Cost tracking (estimates based on Claude API pricing)
TOTAL_INPUT_TOKENS=0
TOTAL_OUTPUT_TOKENS=0

usage() {
    echo "Design Ops v$VERSION - Unified Design Pipeline"
    echo ""
    echo "Usage: $0 <command> [file] [options]"
    echo ""
    echo "CORE COMMANDS (run in this order):"
    echo "  stress-test <spec>   Check completeness (requirements, journeys, failure modes)"
    echo "  validate <spec>      Check clarity (structure, ambiguity)"
    echo "  generate <spec>      Generate PRP from spec (one-shot)"
    echo "  check <prp>          Check PRP quality"
    echo "  implement <prp>      Generate Ralph steps from PRP (--output <dir> --phase N)"
    echo "  ralph-check <prp>    Validate implementation against PRP (--steps <dir>)"
    echo ""
    echo "ADVANCED COMMANDS (extended features):"
    echo "  orchestrate <spec>   Multi-agent pipeline (analyze → generate → review)"
    echo "  watch <spec>         File watcher for continuous validation"
    echo "  dashboard            Interactive validation status dashboard"
    echo "  retro <prp>          Retrospective analysis after implementation"
    echo ""
    echo "OPTIONS:"
    echo "  --output <dir>       Output directory for implement command"
    echo "  --phase <N>          Generate only phase N (for implement command)"
    echo "  --steps <dir>        Steps directory for ralph-check"
    echo "  --requirements <f>   Requirements file for stress-test (optional)"
    echo "  --journeys <f>       User journeys file for stress-test (optional)"
    echo "  --quick              Skip LLM assessment (deterministic only)"
    echo "  --skip-review        Skip interactive review prompt (for CI/automation)"
    echo "  --verbose            Show detailed output"
    echo ""
    echo "WORKFLOW:"
    echo "  1. stress-test  →  Catch obvious gaps in completeness"
    echo "  2. validate     →  Catch obvious gaps in clarity → HUMAN REVIEW GATE"
    echo "  3. generate     →  Create PRP + auto-check → HUMAN REVIEW GATE"
    echo "  4. implement    →  Generate Ralph steps from PRP"
    echo "  5. ralph-check  →  Verify steps match PRP → HUMAN REVIEW GATE"
    echo "  6. Execute      →  ./ralph.sh N to run steps"
    echo ""
    echo "Run '$0 <command> --help' for command-specific help."
    echo ""
    echo "Philosophy: This is a CHECKLIST ASSISTANT, not a judge."
    echo "            It catches obvious gaps. YOU catch subtle design flaws."
    exit 1
}

# ============================================================================
# ROBUST JSON PARSING (uses python, not grep)
# ============================================================================

parse_json() {
    local json="$1"
    local field="$2"
    echo "$json" | python3 -c "
import json, sys
try:
    # Try to extract JSON from markdown code blocks
    text = sys.stdin.read()
    if '\`\`\`json' in text:
        start = text.find('\`\`\`json') + 7
        end = text.find('\`\`\`', start)
        text = text[start:end].strip()
    elif '\`\`\`' in text:
        start = text.find('\`\`\`') + 3
        end = text.find('\`\`\`', start)
        text = text[start:end].strip()

    data = json.loads(text)
    field = '$field'

    # Navigate nested fields like 'dimensions.completeness.score'
    for key in field.split('.'):
        if isinstance(data, dict):
            data = data.get(key, '')
        else:
            data = ''
            break
    print(data if data != '' else '')
except Exception as e:
    print('')
" 2>/dev/null
}

extract_json() {
    local text="$1"
    echo "$text" | python3 -c "
import json, sys, re
text = sys.stdin.read()

# Try to find JSON in the text
patterns = [
    r'\`\`\`json\s*([\s\S]*?)\`\`\`',
    r'\`\`\`\s*([\s\S]*?)\`\`\`',
    r'(\{[\s\S]*\})'
]

for pattern in patterns:
    match = re.search(pattern, text)
    if match:
        try:
            candidate = match.group(1).strip()
            json.loads(candidate)  # Validate it's valid JSON
            print(candidate)
            sys.exit(0)
        except:
            continue

print('{}')
" 2>/dev/null
}

# ============================================================================
# COST TRACKING
# ============================================================================

estimate_tokens() {
    local text="$1"
    # Rough estimate: 1 token ≈ 4 characters
    echo $(( ${#text} / 4 ))
}

track_cost() {
    local input_text="$1"
    local output_text="$2"

    local input_tokens=$(estimate_tokens "$input_text")
    local output_tokens=$(estimate_tokens "$output_text")

    TOTAL_INPUT_TOKENS=$((TOTAL_INPUT_TOKENS + input_tokens))
    TOTAL_OUTPUT_TOKENS=$((TOTAL_OUTPUT_TOKENS + output_tokens))
}

show_cost_summary() {
    # Sonnet pricing: $3/M input, $15/M output (approximate)
    local input_cost=$(echo "scale=4; $TOTAL_INPUT_TOKENS * 0.000003" | bc)
    local output_cost=$(echo "scale=4; $TOTAL_OUTPUT_TOKENS * 0.000015" | bc)
    local total_cost=$(echo "scale=4; $input_cost + $output_cost" | bc)

    echo ""
    echo -e "${CYAN}Cost estimate: ~\$${total_cost} (${TOTAL_INPUT_TOKENS} input + ${TOTAL_OUTPUT_TOKENS} output tokens)${NC}"
}

# ============================================================================
# HUMAN REVIEW GATE
# ============================================================================

require_review_acknowledgment() {
    local context="$1"  # "validate" or "check"
    local file="$2"     # The file being reviewed

    # Skip if --skip-review flag was passed
    if [[ "$SKIP_REVIEW" == "true" ]]; then
        echo ""
        echo -e "${YELLOW}[--skip-review] Skipping interactive review gate${NC}"
        return 0
    fi

    # Check if running in a terminal (stdin is a tty)
    if [[ ! -t 0 ]]; then
        echo ""
        echo -e "${RED}╔═══════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${RED}║  HUMAN REVIEW GATE - ALL ITEMS REQUIRE ACKNOWLEDGMENT         ║${NC}"
        echo -e "${RED}╚═══════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "  ${YELLOW}No interactive terminal detected.${NC}"
        echo -e "  ${YELLOW}ALL items above (errors, warnings, suggestions) must be reviewed.${NC}"
        echo ""
        echo -e "  ${CYAN}To proceed after review:${NC}"
        echo -e "  ${DIM}1. Review ALL items in the checklist above${NC}"
        echo -e "  ${DIM}2. Re-run with --skip-review ONLY after human approval${NC}"
        echo ""
        return 1
    fi

    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  ${YELLOW}HUMAN REVIEW REQUIRED${BLUE}                                        ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  ${YELLOW}YOU catch design flaws. This tool only catches structural gaps.${NC}"
    echo -e "  The LLM suggestions above are a starting point, not the answer."
    echo ""
    echo -e "  ${CYAN}What did you decide about the suggestions above?${NC}"
    echo -e "  ${DIM}(e.g., \"Ignoring #2, adding #4, #1 not applicable\" or \"All good\")${NC}"
    echo -e "  ${DIM}Type 'stop' to abort, 'skip' to proceed without logging${NC}"
    echo ""

    while true; do
        echo -ne "  Your decision: "
        read -r response

        # Handle special commands
        case "${response,,}" in
            stop|abort|quit|exit|n|no)
                echo ""
                echo -e "  ${YELLOW}Stopped. Fix issues and run again.${NC}"
                exit 0
                ;;
            skip)
                echo ""
                echo -e "  ${YELLOW}Skipped logging. Proceeding...${NC}"
                return 0
                ;;
            "")
                echo -e "  ${RED}Please document your decision (or type 'stop' to abort)${NC}"
                continue
                ;;
        esac

        # Log the decision
        local log_dir="${DESIGNOPS_LOG_DIR:-/tmp/design-ops-decisions}"
        mkdir -p "$log_dir"

        local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
        local log_file="$log_dir/decisions.log"
        local file_basename=$(basename "${file:-unknown}")

        # Append to log file
        {
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "Timestamp: $timestamp"
            echo "Command:   $context"
            echo "File:      $file_basename"
            echo "Decision:  $response"
            echo ""
        } >> "$log_file"

        echo ""
        echo -e "  ${GREEN}✓ Decision logged. Proceeding...${NC}"
        echo -e "  ${DIM}(Log: $log_file)${NC}"
        return 0
    done
}

# ============================================================================
# LLM INTERFACE
# ============================================================================

call_claude() {
    local prompt="$1"
    local thinking_level="${2:-Normal}"  # Optional: Normal, Think, Think Hard, Ultrathink
    local result

    # For Ultrathink level, add explicit Chain of Thought instructions
    if [[ "$thinking_level" == "Ultrathink" ]]; then
        prompt="EXTENDED THINKING MODE ACTIVATED

Before generating your response, work through these steps internally:
1. ANALYZE: What are all the requirements and constraints?
2. DECOMPOSE: Break down into sub-problems
3. VERIFY: Check each assumption against invariants
4. SYNTHESIZE: Combine verified components
5. VALIDATE: Ensure completeness before output

Take your time. Quality over speed.

---

$prompt"
    elif [[ "$thinking_level" == "Think Hard" ]]; then
        prompt="CAREFUL ANALYSIS REQUIRED

Before responding:
1. Identify all integration points and edge cases
2. Verify assumptions are explicitly stated
3. Check for potential invariant violations

---

$prompt"
    fi

    # Use piping for large prompts + --no-session-persistence to prevent context leaking
    result=$(echo "$prompt" | claude --model "$CLAUDE_MODEL" --print --no-session-persistence 2>/dev/null)

    track_cost "$prompt" "$result"
    echo "$result"
}

# ============================================================================
# DETERMINISTIC CHECKS (Fast, Free, Reliable)
# ============================================================================

check_spec_structure() {
    local file="$1"
    local content
    content=$(cat "$file")

    local issues=()
    local warnings=()

    echo -e "${BLUE}━━━ Deterministic Checks ━━━${NC}"

    # Required sections
    if ! echo "$content" | grep -qiE "^#.*problem|^##.*problem|problem.*statement"; then
        issues+=("Missing: Problem statement")
    else
        echo -e "  ${GREEN}✓${NC} Problem statement found"
    fi

    if ! echo "$content" | grep -qiE "success.*criter|acceptance.*criter|done.*when|definition.*done"; then
        issues+=("Missing: Success criteria")
    else
        echo -e "  ${GREEN}✓${NC} Success criteria found"
    fi

    if ! echo "$content" | grep -qiE "scope|boundar|in.scope|out.of.scope|non-goal"; then
        warnings+=("Consider adding: Scope boundaries")
    else
        echo -e "  ${GREEN}✓${NC} Scope defined"
    fi

    if ! echo "$content" | grep -qiE "test|verif|validat"; then
        warnings+=("Consider adding: Test/validation approach")
    else
        echo -e "  ${GREEN}✓${NC} Testing mentioned"
    fi

    # Check for vague words (warning only)
    local vague_count
    vague_count=$(echo "$content" | grep -ciE "properly|efficiently|adequate|reasonable|good quality|as needed" 2>/dev/null) || vague_count=0
    if [[ $vague_count -gt 3 ]]; then
        warnings+=("Found $vague_count vague terms (properly, efficiently, etc.)")
    fi

    # Check minimum content
    local word_count
    word_count=$(wc -w < "$file" | tr -d ' ')
    if [[ $word_count -lt 100 ]]; then
        issues+=("Too short: $word_count words (minimum ~100)")
    fi

    echo ""

    # Report
    if [[ ${#issues[@]} -gt 0 ]]; then
        echo -e "${RED}Issues (must fix):${NC}"
        for issue in "${issues[@]}"; do
            echo -e "  ${RED}✗${NC} $issue"
        done
    fi

    if [[ ${#warnings[@]} -gt 0 ]]; then
        echo -e "${YELLOW}Warnings (consider fixing):${NC}"
        for warning in "${warnings[@]}"; do
            echo -e "  ${YELLOW}!${NC} $warning"
        done
    fi

    # Return grade
    if [[ ${#issues[@]} -gt 0 ]]; then
        echo "FAIL"
    elif [[ ${#warnings[@]} -gt 2 ]]; then
        echo "NEEDS_WORK"
    else
        echo "PASS"
    fi
}

check_prp_structure() {
    local file="$1"
    local content
    content=$(cat "$file")

    local issues=()
    local warnings=()

    echo -e "${BLUE}━━━ Deterministic Checks ━━━${NC}"

    # Required PRP sections
    local required_sections=("overview" "success criteria" "timeline" "risk" "validation")

    for section in "${required_sections[@]}"; do
        if echo "$content" | grep -qiE "^#+.*$section"; then
            echo -e "  ${GREEN}✓${NC} $section section found"
        else
            issues+=("Missing section: $section")
        fi
    done

    # Check for unfilled placeholders
    local placeholder_count
    placeholder_count=$(grep -cE '\[FILL|\[TODO|\[TBD|\{\{' "$file" 2>/dev/null) || placeholder_count=0
    if [[ $placeholder_count -gt 0 ]]; then
        issues+=("Found $placeholder_count unfilled placeholders")
    fi

    # Check for LLM reasoning that shouldn't be in output
    if head -30 "$file" | grep -qiE "let me|I'll|I will|here's my|thinking"; then
        warnings+=("PRP may contain LLM reasoning that should be removed")
    fi

    echo ""

    if [[ ${#issues[@]} -gt 0 ]]; then
        echo -e "${RED}Issues (must fix):${NC}"
        for issue in "${issues[@]}"; do
            echo -e "  ${RED}✗${NC} $issue"
        done
    fi

    if [[ ${#warnings[@]} -gt 0 ]]; then
        echo -e "${YELLOW}Warnings:${NC}"
        for warning in "${warnings[@]}"; do
            echo -e "  ${YELLOW}!${NC} $warning"
        done
    fi

    if [[ ${#issues[@]} -gt 0 ]]; then
        echo "FAIL"
    elif [[ ${#warnings[@]} -gt 0 ]]; then
        echo "NEEDS_WORK"
    else
        echo "PASS"
    fi
}

# ============================================================================
# LLM ADVISORY ASSESSMENT (Suggestions, not auto-fix)
# ============================================================================

get_llm_assessment() {
    local file="$1"
    local type="$2"  # "spec" or "prp"
    local content
    content=$(cat "$file")

    echo -e "${BLUE}━━━ LLM Advisory Assessment ━━━${NC}"
    echo -e "${CYAN}Getting suggestions (not auto-fixing)...${NC}"

    local schema prompt
    if [[ "$type" == "spec" ]]; then
        # Schema for spec validation - focuses on ambiguity/clarity
        schema='{"type":"object","properties":{"summary":{"type":"string"},"ambiguity_flags":{"type":"array","items":{"type":"string"}},"implicit_assumptions":{"type":"array","items":{"type":"string"}},"suggestions":{"type":"array","items":{"type":"string"}},"strengths":{"type":"array","items":{"type":"string"}}},"required":["summary","ambiguity_flags","suggestions"]}'

        prompt="You are validating a specification for CLARITY and UNAMBIGUITY (not completeness - that was checked in stress-test).

CLARITY INVARIANT (Invariant #1): Every term must have operational definition.
Flag any of these vague terms WITHOUT objective criteria attached:
- 'properly', 'correctly', 'efficiently', 'quickly'
- 'good', 'quality', 'robust', 'secure'
- 'intuitive', 'user-friendly', 'easy to use'
- 'as needed', 'appropriate', 'reasonable'
- 'should', 'may', 'might' (without clear conditions)

SPECIFICATION:
$content

Check for:
1. Vague terms without measurable definitions (quote the exact text)
2. Implicit assumptions not stated explicitly
3. Ambiguous state transitions (what happens between states?)
4. Success criteria that can't be objectively measured
5. Missing edge case definitions

Provide:
- summary: One sentence on clarity level
- ambiguity_flags: Specific vague terms found and where (quote the text, e.g., 'Line says \"handle errors properly\" - what does properly mean?') - max 5
- implicit_assumptions: Things the spec assumes but doesn't state explicitly - max 3
- suggestions: How to make unclear sections more specific - max 5
- strengths: What's already clear and well-defined - max 2

If you are uncertain about any assessment, flag it with [UNCERTAIN: reason]. It's better to express uncertainty than to guess."
    else
        # Schema for PRP validation - focuses on implementation readiness
        schema='{"type":"object","properties":{"summary":{"type":"string"},"blockers":{"type":"array","items":{"type":"string"}},"confidence_assessment":{"type":"string"},"missing_detail":{"type":"array","items":{"type":"string"}},"strengths":{"type":"array","items":{"type":"string"}}},"required":["summary","blockers"]}'

        prompt="You are validating a PRP (Product Requirements Prompt) for implementation readiness.

PRP:
$content

Check:
1. CONFIDENCE SCORE SANITY: Does the stated confidence (X/10) seem accurate given the content?
2. EXTRACTION COMPLETENESS: Are there sections marked NOT_SPECIFIED_IN_SPEC that seem wrong?
3. THINKING LEVEL: Does the recommended thinking level match the complexity?
4. APPENDIX CONTENT: Are technical details (schemas, APIs, wireframes) present if the PRP mentions them?
5. ACTIONABILITY: Could an engineer start implementation immediately, or are there blockers?

Provide:
- summary: One sentence on implementation readiness
- blockers: Issues that MUST be resolved before implementation (max 3)
- confidence_assessment: Is the stated confidence score accurate? Why/why not?
- missing_detail: Technical content that seems missing despite being referenced - max 3
- strengths: What makes this PRP implementation-ready - max 2

If you are uncertain about any assessment, flag it with [UNCERTAIN: reason]. It's better to express uncertainty than to guess."
    fi

    local raw_result result
    raw_result=$(echo "$prompt" | claude --model "$CLAUDE_MODEL" --print --output-format json --json-schema "$schema" 2>/dev/null)

    # Extract structured_output from the wrapper JSON
    result=$(echo "$raw_result" | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d.get('structured_output',{})))" 2>/dev/null)

    track_cost "$prompt" "$result"

    if [[ -z "$result" || "$result" == "{}" ]]; then
        echo -e "${YELLOW}LLM call failed or returned empty${NC}"
        echo "SKIPPED"
        return
    fi

    # Parse the structured JSON response
    local summary
    summary=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('summary',''))" 2>/dev/null)

    echo ""
    echo -e "Summary: $summary"
    echo ""

    if [[ "$type" == "spec" ]]; then
        # Display spec validation results (ambiguity-focused)
        echo "$result" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)

    # Ambiguity flags (Invariant #1)
    flags = data.get('ambiguity_flags', [])
    if flags:
        print('\033[91mAmbiguity Flags (Invariant #1):\033[0m')
        for f in flags[:5]:
            print(f'  ✗ {f}')
        print()
    else:
        print('\033[92mNo ambiguity flags - terminology is clear\033[0m')
        print()

    # Implicit assumptions
    assumptions = data.get('implicit_assumptions', [])
    if assumptions:
        print('\033[93mImplicit Assumptions:\033[0m')
        for a in assumptions[:3]:
            print(f'  ? {a}')
        print()

    # Suggestions
    suggestions = data.get('suggestions', [])
    if suggestions:
        print('\033[93mSuggestions:\033[0m')
        for i, s in enumerate(suggestions[:5], 1):
            print(f'  {i}. {s}')
        print()

    # Strengths
    strengths = data.get('strengths', [])
    if strengths:
        print('Strengths:')
        for s in strengths[:2]:
            print(f'  ✓ {s}')
except Exception as e:
    print(f'  (Could not parse: {e})')
" 2>/dev/null
    else
        # Display PRP validation results (implementation-readiness focused)
        echo "$result" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)

    # Blockers
    blockers = data.get('blockers', [])
    if blockers:
        print('\033[91mBlockers (must resolve):\033[0m')
        for b in blockers[:3]:
            print(f'  ✗ {b}')
        print()
    else:
        print('\033[92mNo blockers - ready for implementation\033[0m')
        print()

    # Confidence assessment
    conf = data.get('confidence_assessment', '')
    if conf:
        print('\033[96mConfidence Assessment:\033[0m')
        print(f'  {conf}')
        print()

    # Missing detail
    missing = data.get('missing_detail', [])
    if missing:
        print('\033[93mMissing Detail:\033[0m')
        for m in missing[:3]:
            print(f'  ? {m}')
        print()

    # Strengths
    strengths = data.get('strengths', [])
    if strengths:
        print('Strengths:')
        for s in strengths[:2]:
            print(f'  ✓ {s}')
except Exception as e:
    print(f'  (Could not parse: {e})')
" 2>/dev/null
    fi

    echo ""
    echo "DONE"  # Signal completion, not a grade
    echo "STATE_JSON:$result"  # For pipeline state capture
}

# =============================================================================
# PRP GENERATION HELPERS
# =============================================================================

# Parse domains from spec header
parse_domains() {
    local spec_content="$1"

    local domain_line
    domain_line=$(echo "$spec_content" | grep -iE "^\*?\*?Domain\*?\*?:" | head -1)

    if [[ -z "$domain_line" ]]; then
        echo "universal"
        return
    fi

    local domain_value
    domain_value=$(echo "$domain_line" | sed 's/.*://' | tr '[:upper:]' '[:lower:]' | xargs)

    echo "$domain_value" | tr '+,' '\n' | while read -r domain; do
        domain=$(echo "$domain" | xargs)
        [[ -n "$domain" ]] && echo "$domain"
    done
}

# Resolve domains to invariant files and counts
resolve_domain_invariants() {
    local spec_content="$1"

    local domains
    domains=$(parse_domains "$spec_content")

    local invariant_refs=""
    local total_count=11
    local domain_count=0
    local has_skill_gap=false

    invariant_refs="Universal: $INVARIANTS_DIR/system-invariants.md (invariants 1-11)"

    while IFS= read -r domain; do
        [[ -z "$domain" || "$domain" == "universal" ]] && continue

        local mapping
        mapping=$(get_domain_mapping "$domain")
        if [[ -n "$mapping" ]]; then
            local file="${mapping%%:*}"
            local range="${mapping##*:}"
            local start="${range%%-*}"
            local end="${range##*-}"
            local count=$((end - start + 1))

            invariant_refs+="\nDomain ($domain): $DOMAINS_DIR/$file (invariants $range)"
            total_count=$((total_count + count))
            domain_count=$((domain_count + 1))

            [[ "$file" == "skill-gap-transcendence.md" ]] && has_skill_gap=true
        else
            invariant_refs+="\nDomain ($domain): UNKNOWN - manual review required"
            domain_count=$((domain_count + 1))
        fi
    done <<< "$domains"

    echo "INVARIANT_REFS<<EOF"
    echo -e "$invariant_refs"
    echo "EOF"
    echo "TOTAL_INVARIANTS=$total_count"
    echo "DOMAIN_COUNT=$domain_count"
    echo "HAS_SKILL_GAP=$has_skill_gap"
}

# Analyze spec for confidence factors
analyze_spec_confidence() {
    local spec_content="$1"

    # Factor 1: Requirement Clarity (30%)
    local clarity_score=0.5
    if echo "$spec_content" | grep -qiE "## Success Criteria|### Success Criteria"; then
        clarity_score=0.7
        if echo "$spec_content" | grep -qE "\|.*Target.*\||\|.*Metric.*\|"; then
            clarity_score=0.9
        fi
    fi

    # Factor 2: Pattern Availability (25%)
    local pattern_score=0.4
    if echo "$spec_content" | grep -qE "src/|app/|components/|\.tsx|\.ts|existing"; then
        pattern_score=0.7
    fi
    if echo "$spec_content" | grep -qiE "## Examples|### Examples|## Patterns|existing.*pattern"; then
        pattern_score=0.9
    fi

    # Factor 3: Test Coverage Plan (20%)
    local test_score=0.3
    local validation_count
    validation_count=$(echo "$spec_content" | grep -cE "npm (test|run)|pytest|curl|verify|assert" 2>/dev/null | head -1 || echo "0")
    validation_count=${validation_count:-0}
    if [[ "$validation_count" -ge 4 ]] 2>/dev/null; then
        test_score=0.9
    elif [[ "$validation_count" -ge 2 ]] 2>/dev/null; then
        test_score=0.7
    elif [[ "$validation_count" -ge 1 ]] 2>/dev/null; then
        test_score=0.5
    fi

    # Factor 4: Edge Case Handling (15%)
    local edge_score=0.3
    local failure_count
    failure_count=$(echo "$spec_content" | grep -cE "^### FM[0-9]|Failure Mode|## Failure" 2>/dev/null | head -1 || echo "0")
    failure_count=${failure_count:-0}
    if [[ "$failure_count" -ge 3 ]] 2>/dev/null; then
        edge_score=0.9
    elif [[ "$failure_count" -ge 1 ]] 2>/dev/null; then
        edge_score=0.6
    fi
    if echo "$spec_content" | grep -qiE "Degradation|Fallback|Recovery"; then
        edge_score=$(echo "$edge_score + 0.1" | bc)
        [[ $(echo "$edge_score > 1.0" | bc) -eq 1 ]] && edge_score=1.0
    fi

    # Factor 5: Tech Familiarity (10%)
    local tech_score=0.8
    if echo "$spec_content" | grep -qiE "skill.?gap|unknown|learning|first.?time|new.?tech"; then
        tech_score=0.4
    fi

    local score
    score=$(echo "scale=2; ($clarity_score * 0.30) + ($pattern_score * 0.25) + ($test_score * 0.20) + ($edge_score * 0.15) + ($tech_score * 0.10)" | bc)
    score=$(echo "scale=1; $score * 10" | bc)

    echo "CLARITY_SCORE=$clarity_score"
    echo "PATTERN_SCORE=$pattern_score"
    echo "TEST_SCORE=$test_score"
    echo "EDGE_SCORE=$edge_score"
    echo "TECH_SCORE=$tech_score"
    echo "CONFIDENCE_SCORE=$score"
}

# Determine thinking level
determine_thinking_level() {
    local confidence="$1"
    local domain_count="$2"
    local invariant_count="$3"
    local has_skill_gap="$4"

    local level="Normal"
    local focus=""

    local conf_int
    conf_int=$(echo "$confidence" | cut -d'.' -f1)

    if [[ "$conf_int" -lt 5 ]] || [[ "$domain_count" -ge 3 ]] || [[ "$invariant_count" -gt 30 ]]; then
        level="Ultrathink"
        focus="Verify all assumptions before implementation|Check invariant compliance at each decision point"
    elif [[ "$conf_int" -lt 7 ]] || [[ "$domain_count" -ge 2 ]] || [[ "$invariant_count" -gt 20 ]]; then
        level="Think Hard"
        focus="Validate integration points|Consider edge cases explicitly"
    elif [[ "$conf_int" -lt 9 ]]; then
        level="Think"
        focus="Adapt patterns to context|Verify success criteria mapping"
    else
        focus="Execute plan|Standard validation"
    fi

    if [[ "$has_skill_gap" == "true" ]]; then
        if [[ "$level" == "Normal" ]]; then
            level="Think"
        elif [[ "$level" == "Think" ]]; then
            level="Think Hard"
        fi
        focus="$focus|Discovery phase required - unknown unknowns likely"
    fi

    echo "THINKING_LEVEL=$level"
    echo "THINKING_FOCUS=$focus"
}

# =============================================================================
# PRP GENERATION (2026 Best Practices)
# =============================================================================

generate_prp() {
    local spec_file="$1"
    local output_file="$2"
    local spec_content
    spec_content=$(cat "$spec_file")

    local spec_name
    spec_name=$(basename "$spec_file" .md)

    # Calculate spec hash for caching
    local spec_hash
    spec_hash=$(echo "$spec_content" | md5 2>/dev/null || echo "$spec_content" | md5sum | cut -d' ' -f1)

    # Check if cached PRP exists with same spec hash
    if [[ -f "$output_file" ]]; then
        local cached_hash
        cached_hash=$(grep "spec_hash:" "$output_file" 2>/dev/null | head -1 | awk '{print $2}')
        if [[ "$cached_hash" == "$spec_hash" ]]; then
            echo -e "${GREEN}━━━ Using Cached PRP ━━━${NC}"
            echo -e "  Output: ${CYAN}$output_file${NC}"
            echo -e "  Spec hash matches cached PRP (${spec_hash:0:8}...)"
            echo -e "  ${YELLOW}To force regeneration, delete the PRP file first.${NC}"
            return 0
        fi
    fi

    # Calculate next PRP ID (increment based on existing PRPs)
    local today
    today=$(date +%Y-%m-%d)
    local prp_dir
    prp_dir=$(dirname "$output_file")

    local seq_num=1
    if [[ -d "$prp_dir" ]]; then
        # Find highest sequence number for today's PRPs
        local existing_max
        existing_max=$(grep -rh "prp_id: PRP-$today-" "$prp_dir"/*.md 2>/dev/null | \
            grep -oE "PRP-$today-[0-9]+" | \
            sed "s/PRP-$today-//" | \
            sort -n | tail -1)
        if [[ -n "$existing_max" ]]; then
            seq_num=$((existing_max + 1))
        fi
    fi
    local prp_id
    prp_id=$(printf "PRP-%s-%03d" "$today" "$seq_num")

    echo -e "${BLUE}━━━ Generating PRP (2026 Best Practices) ━━━${NC}"
    echo -e "  PRP ID: ${CYAN}$prp_id${NC}"

    # Step 1: Parse domains and resolve invariants
    echo -e "${CYAN}Analyzing spec domains...${NC}"
    local domain_info
    domain_info=$(resolve_domain_invariants "$spec_content")

    local invariant_refs total_invariants domain_count has_skill_gap
    invariant_refs=$(echo "$domain_info" | sed -n '/INVARIANT_REFS<<EOF/,/EOF/p' | sed '1d;$d')
    total_invariants=$(echo "$domain_info" | grep "TOTAL_INVARIANTS=" | cut -d= -f2)
    domain_count=$(echo "$domain_info" | grep "DOMAIN_COUNT=" | cut -d= -f2)
    has_skill_gap=$(echo "$domain_info" | grep "HAS_SKILL_GAP=" | cut -d= -f2)

    echo -e "  Domains detected: $domain_count (+ universal)"
    echo -e "  Total invariants: $total_invariants"
    [[ "$has_skill_gap" == "true" ]] && echo -e "  ${YELLOW}⚠ Skill-gap domain detected${NC}"

    # Step 2: Calculate confidence
    echo -e "${CYAN}Calculating confidence score...${NC}"
    local confidence_info
    confidence_info=$(analyze_spec_confidence "$spec_content")

    local confidence_score clarity_score pattern_score test_score edge_score tech_score
    confidence_score=$(echo "$confidence_info" | grep "CONFIDENCE_SCORE=" | cut -d= -f2)
    clarity_score=$(echo "$confidence_info" | grep "CLARITY_SCORE=" | cut -d= -f2)
    pattern_score=$(echo "$confidence_info" | grep "PATTERN_SCORE=" | cut -d= -f2)
    test_score=$(echo "$confidence_info" | grep "TEST_SCORE=" | cut -d= -f2)
    edge_score=$(echo "$confidence_info" | grep "EDGE_SCORE=" | cut -d= -f2)
    tech_score=$(echo "$confidence_info" | grep "TECH_SCORE=" | cut -d= -f2)

    # Check pipeline state for accumulated issues (affects confidence)
    local state_file
    state_file=$(get_state_file_path "$spec_file")
    local accumulated_issues
    accumulated_issues=$(get_accumulated_issues "$state_file")

    if [[ "$accumulated_issues" -gt 0 ]]; then
        # Reduce confidence by 0.5 per accumulated issue (max 2 points reduction)
        local penalty
        penalty=$(echo "scale=1; $accumulated_issues * 0.5" | bc)
        [[ $(echo "$penalty > 2" | bc) -eq 1 ]] && penalty=2
        confidence_score=$(echo "scale=1; $confidence_score - $penalty" | bc)
        [[ $(echo "$confidence_score < 1" | bc) -eq 1 ]] && confidence_score=1
        echo -e "  Confidence: $confidence_score/10 ${YELLOW}(adjusted: -$penalty from $accumulated_issues prior issues)${NC}"
    else
        echo -e "  Confidence: $confidence_score/10"
    fi

    # Step 3: Determine thinking level
    local thinking_info
    thinking_info=$(determine_thinking_level "$confidence_score" "$domain_count" "$total_invariants" "$has_skill_gap")

    local thinking_level thinking_focus
    thinking_level=$(echo "$thinking_info" | grep "THINKING_LEVEL=" | cut -d= -f2)
    thinking_focus=$(echo "$thinking_info" | grep "THINKING_FOCUS=" | cut -d= -f2)

    echo -e "  Thinking level: ${YELLOW}$thinking_level${NC}"

    # Step 4: Determine risk level
    local risk_level
    if (( $(echo "$confidence_score < 5" | bc -l) )); then
        risk_level="Low/Red - STOP: Address gaps before proceeding"
    elif (( $(echo "$confidence_score < 7" | bc -l) )); then
        risk_level="Medium/Yellow - CAUTION: Proceed with risk mitigation"
    else
        risk_level="High/Green - PROCEED: Normal execution path"
    fi

    # Step 5: Load PRP template or use fallback
    local prp_template_note=""
    if [[ -f "$TEMPLATES_DIR/prp-base.md" ]]; then
        prp_template_note="Using template: $TEMPLATES_DIR/prp-base.md"
    else
        prp_template_note="Template not found - using inline structure"
    fi
    echo -e "  ${DIM}$prp_template_note${NC}"

    # Step 6: Build the prompt
    echo -e "${CYAN}Generating PRP...${NC}"

    local prompt="You are a PRP compiler. Your job is EXTRACTION and TRANSFORMATION from a validated spec.

CRITICAL RULES:
- Extract content from the spec below. Do NOT invent content.
- If a spec section is missing or unclear, use \"NOT_SPECIFIED_IN_SPEC\" for that field
- Preserve all specific numbers, commands, file paths, and technical details exactly
- Copy Validation Commands VERBATIM - do not paraphrase
- If unsure about any extraction, flag it with [UNCERTAIN: reason]

DOMAIN & INVARIANTS (reference paths only):
$invariant_refs

PRE-CALCULATED VALUES (use these directly in the PRP):
- PRP ID: $prp_id
- Source Spec: $spec_file
- Validation Date: $(date +%Y-%m-%d)
- Confidence Score: $confidence_score/10
- Risk Level: $risk_level
- Thinking Level: $thinking_level
- Thinking Focus: $(echo "$thinking_focus" | tr '|' ', ')
- Domain Count: $domain_count
- Invariant Count: $total_invariants

CONFIDENCE BREAKDOWN (include in Section 2):
| Factor | Weight | Score | Notes |
|--------|--------|-------|-------|
| Requirement Clarity | 30% | $clarity_score | Success criteria with metrics |
| Pattern Availability | 25% | $pattern_score | Existing code references |
| Test Coverage Plan | 20% | $test_score | Validation commands count |
| Edge Case Handling | 15% | $edge_score | Failure modes documented |
| Tech Familiarity | 10% | $tech_score | Known vs skill-gap |

VERBATIM PRESERVATION (copy these sections EXACTLY, do not summarize):
- Database Schema (SQL) → Include complete CREATE TABLE statements
- Validation Commands → Copy all bash/curl commands exactly
- API Endpoints → Preserve full endpoint specifications
- Column Mappings → Include all column names and transformations
- Error Messages → Copy exact error text
- UI Wireframes (ASCII) → Preserve character-for-character
- State Transitions → Copy the full state machine notation
- Code Snippets → Preserve all code exactly
- Tables with data → Copy all rows, do not truncate

SUMMARIZATION ALLOWED (these can be condensed):
- Problem Statement → Keep to 2-3 sentences
- Overview narrative → Condense to 1 paragraph
- Background/context sections → Brief summary

EXTRACTION MAP - Follow this mapping:
| Spec Section | → | PRP Section | Extraction Rule |
|--------------|---|-------------|-----------------|
| Problem Statement | → | 1.1 Problem Statement | Summarize to 2-3 sentences |
| Overview | → | 1.2 Solution Summary | Summarize WHAT not HOW |
| Scope (In/Out) | → | 1.3 Scope Boundaries | Convert to table, keep ALL items |
| Success Criteria table | → | 2.1 Primary Metrics | VERBATIM - copy table exactly |
| Database Schema (SQL) | → | Appendix B: Database Schema | VERBATIM - full CREATE TABLE |
| Column Mappings | → | Appendix D: Import Mappings | VERBATIM - all columns |
| API Endpoints | → | Appendix C: API Specification | VERBATIM - all endpoints |
| UI Wireframes | → | Appendix E: UI Reference | VERBATIM - preserve ASCII art |
| Feature sections (F0, F1...) | → | Phase sections | Keep ALL requirements as checklist |
| Validation Commands | → | 8. Validation Commands | VERBATIM - copy all commands |
| Failure Modes (FM1...) | → | 4.1 Risk Matrix | VERBATIM descriptions + probability/impact |
| Degradation Paths | → | 4.2 Fallback Strategies | VERBATIM as IF/THEN format |
| Error Messages | → | Appendix F: Error Catalog | VERBATIM - all error strings |
| Dependencies | → | 5.3 External Dependencies | VERBATIM - preserve table |
| Algorithm Details | → | Appendix G: Algorithm Details | VERBATIM - fuzzy search, etc. |
| Open Questions | → | Add to risks + Appendix | VERBATIM - list all |

LENGTH REQUIREMENT:
The output PRP should be approximately the same length as the input spec, or LONGER.
A 368-line spec should produce a 350-500 line PRP.
If your output is significantly shorter, you are summarizing too aggressively - go back and include more detail.

PRP STRUCTURE TO OUTPUT:
# PRP: $spec_name

## Meta
\`\`\`yaml
prp_id: $prp_id
source_spec: $spec_file
spec_hash: $spec_hash
validation_status: PASSED
validated_date: $(date +%Y-%m-%d)
domain: [extracted from spec]
version: 1.0
\`\`\`

## Confidence Score
### Overall Score
| Score | Risk Level | Recommendation |
|-------|------------|----------------|
| $confidence_score | [color] | [action] |

### Breakdown
[Use the confidence breakdown table above]

## 1. Project Overview
### 1.1 Problem Statement
[Extract from spec]

### 1.2 Solution Summary
[Extract from spec overview]

### 1.3 Scope Boundaries
| In Scope | Out of Scope |
|----------|--------------|
[Extract from spec]

## 2. Success Criteria
[Extract success criteria table from spec EXACTLY]

## 3. Timeline with Validation Gates
[Map F0, F1, F2... to Phase 1, Phase 2, Phase 3... with gates]

## 4. Risk Assessment
### 4.1 Risk Matrix
[Extract from Failure Modes, add probability/impact]

### 4.2 Fallback Strategies
[Extract from Degradation Paths as IF/THEN]

## 5. Resource Requirements
### 5.3 External Dependencies
[Extract dependencies table]

## 8. Validation Commands
### 8.1 Test Verification
[COPY VERBATIM from spec Validation Commands section]

## 9. Recommended Thinking Level
| Factor | Value | Impact |
|--------|-------|--------|
| Confidence Score | $confidence_score | [impact note] |
| Domains Involved | $domain_count | [impact note] |
| Invariants Applied | $total_invariants | [impact note] |

**Overall Level**: $thinking_level
**Apply higher thinking to**: $(echo "$thinking_focus" | tr '|' ', ')

## 10. State Transitions
[Extract from spec state transitions if present, or derive from feature flows]

## Appendix A: Source Spec Reference
**Spec Path**: $spec_file
**Invariants Validated**: Universal (1-11)$(echo "$invariant_refs" | grep "Domain" | sed 's/.*invariants /+ /g' | tr '\n' ' ')

## Appendix B: Database Schema
[VERBATIM - Include ALL CREATE TABLE statements from spec]

## Appendix C: API Specification
[VERBATIM - Include ALL API endpoints from spec]

## Appendix D: Import Column Mappings
[VERBATIM - Include ALL column mapping tables from spec]

## Appendix E: UI Wireframes
[VERBATIM - Include ALL ASCII wireframes/mockups from spec]

## Appendix F: Error Message Catalog
[VERBATIM - Include ALL error messages from spec]

## Appendix G: Algorithm Details
[VERBATIM - Include fuzzy search, matching algorithms from spec]

QUALITY CHECK BEFORE RESPONDING:
Before outputting the PRP, verify:
1. Did you include ALL database schema SQL? (If spec has CREATE TABLE, PRP must have it)
2. Did you include ALL API endpoints? (Count them - spec has X, PRP should have X)
3. Did you include ALL validation commands? (Copy verbatim)
4. Did you preserve UI wireframes? (ASCII art must be character-perfect)
5. Did you include ALL column mappings? (Every column from import sections)
6. Did you include ALL error messages? (Every error string from spec)
7. Is your output at least 80% the length of the input spec?

If any answer is NO, go back and add the missing content before outputting.

SPEC CONTENT:
<spec>
$spec_content
</spec>

OUTPUT:
Start directly with: # PRP: $spec_name
Fill all sections above.
Do not include any preamble or explanation before the PRP."

    local result
    result=$(call_claude "$prompt" "$thinking_level")

    # Clean up
    local cleaned
    cleaned=$(echo "$result" | sed -n '/^# PRP/,$p')

    if [[ -z "$cleaned" ]]; then
        cleaned="$result"
    fi

    cleaned=$(echo "$cleaned" | sed '/^```markdown$/d' | sed '/^```$/d')

    echo "$cleaned" > "$output_file"

    local lines
    lines=$(wc -l < "$output_file" | tr -d ' ')
    echo -e "${GREEN}✓ Generated: $output_file ($lines lines)${NC}"
    echo -e "${CYAN}  Confidence: $confidence_score/10 | Thinking: $thinking_level${NC}"
}

# ============================================================================
# MAIN COMMANDS
# ============================================================================

cmd_stress_test() {
    local spec_file="$1"
    local requirements_file="$2"
    local journeys_file="$3"
    local quick="$4"

    [[ ! -f "$spec_file" ]] && { echo -e "${RED}File not found: $spec_file${NC}"; exit 1; }

    local spec_content
    spec_content=$(cat "$spec_file")

    local requirements_content=""
    local journeys_content=""

    [[ -n "$requirements_file" ]] && [[ -f "$requirements_file" ]] && requirements_content=$(cat "$requirements_file")
    [[ -n "$journeys_file" ]] && [[ -f "$journeys_file" ]] && journeys_content=$(cat "$journeys_file")

    # Get pipeline state file for this spec
    local state_file
    state_file=$(get_state_file_path "$spec_file")

    # Variable to store LLM result for state saving
    local llm_result="{}"

    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  SPEC STRESS TEST (v$VERSION) - Completeness Check              ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "Spec: ${CYAN}$spec_file${NC}"
    [[ -n "$requirements_file" ]] && echo -e "Requirements: ${CYAN}$requirements_file${NC}"
    [[ -n "$journeys_file" ]] && echo -e "User Journeys: ${CYAN}$journeys_file${NC}"
    echo ""

    # ━━━ Domain Detection ━━━
    echo -e "${BLUE}━━━ Domain Detection ━━━${NC}"
    local domain_result
    domain_result=$(resolve_domain_invariants "$spec_content")

    local invariant_refs total_invariants domain_count
    invariant_refs=$(echo "$domain_result" | sed -n '/^INVARIANT_REFS<<EOF$/,/^EOF$/p' | sed '1d;$d')
    total_invariants=$(echo "$domain_result" | grep "^TOTAL_INVARIANTS=" | cut -d= -f2)
    domain_count=$(echo "$domain_result" | grep "^DOMAIN_COUNT=" | cut -d= -f2)

    echo -e "  Domains detected: ${CYAN}$((domain_count + 1))${NC} (including universal)"
    echo -e "  Total invariants: ${CYAN}$total_invariants${NC}"
    echo -e "$invariant_refs" | while read -r line; do
        [[ -n "$line" ]] && echo -e "    ${CYAN}→${NC} $line"
    done
    echo ""

    # ━━━ Deterministic Coverage Checks ━━━
    echo -e "${BLUE}━━━ Deterministic Coverage Checks ━━━${NC}"

    local issues=()
    local warnings=()
    local coverage_items=0
    local covered_items=0

    # Check for user journey coverage indicators
    if echo "$spec_content" | grep -qiE "happy path|success.*path|normal.*flow"; then
        echo -e "  ${GREEN}✓${NC} Happy path mentioned"
        ((covered_items++))
    else
        warnings+=("Happy path not explicitly described")
    fi
    ((coverage_items++))

    if echo "$spec_content" | grep -qiE "error|fail|exception|invalid|edge.case"; then
        echo -e "  ${GREEN}✓${NC} Error cases mentioned"
        ((covered_items++))
    else
        issues+=("Error/failure cases not addressed")
    fi
    ((coverage_items++))

    if echo "$spec_content" | grep -qiE "empty|null|zero|no.*data|missing"; then
        echo -e "  ${GREEN}✓${NC} Empty/null states mentioned"
        ((covered_items++))
    else
        warnings+=("Empty/null states not explicitly handled")
    fi
    ((coverage_items++))

    if echo "$spec_content" | grep -qiE "timeout|offline|unavailable|network|api.*fail"; then
        echo -e "  ${GREEN}✓${NC} Failure modes mentioned (timeout, offline, etc.)"
        ((covered_items++))
    else
        issues+=("External failure modes not addressed (API down, timeout, offline)")
    fi
    ((coverage_items++))

    if echo "$spec_content" | grep -qiE "concurrent|race|simultaneous|parallel"; then
        echo -e "  ${GREEN}✓${NC} Concurrency considerations mentioned"
        ((covered_items++))
    else
        warnings+=("Concurrency not explicitly addressed (may not apply)")
    fi
    ((coverage_items++))

    if echo "$spec_content" | grep -qiE "limit|max|min|bound|threshold|quota"; then
        echo -e "  ${GREEN}✓${NC} Limits/boundaries mentioned"
        ((covered_items++))
    else
        warnings+=("Limits/boundaries not specified")
    fi
    ((coverage_items++))

    echo ""

    # Report issues
    if [[ ${#issues[@]} -gt 0 ]]; then
        echo -e "${RED}Gaps (should address):${NC}"
        for issue in "${issues[@]}"; do
            echo -e "  ${RED}✗${NC} $issue"
        done
        echo ""
    fi

    if [[ ${#warnings[@]} -gt 0 ]]; then
        echo -e "${YELLOW}Consider (may not apply):${NC}"
        for warning in "${warnings[@]}"; do
            echo -e "  ${YELLOW}?${NC} $warning"
        done
        echo ""
    fi

    local coverage_pct=$((covered_items * 100 / coverage_items))
    echo -e "Basic Coverage: ${CYAN}$covered_items/$coverage_items ($coverage_pct%)${NC}"
    echo ""

    # ━━━ LLM Deep Analysis ━━━
    if [[ "$quick" != "true" ]]; then
        echo -e "${BLUE}━━━ LLM Deep Analysis ━━━${NC}"
        echo -e "${CYAN}Analyzing completeness...${NC}"

        # JSON schema for structured output - includes invariant violations
        local schema='{"type":"object","properties":{"summary":{"type":"string"},"invariant_violations":{"type":"array","items":{"type":"string"}},"missing_failure_modes":{"type":"array","items":{"type":"string"}},"missing_coverage":{"type":"array","items":{"type":"string"}},"critical_blockers":{"type":"array","items":{"type":"string"}}},"required":["summary","critical_blockers"]}'

        local prompt="You are a QA engineer stress-testing a specification against domain-specific invariants.

APPLICABLE INVARIANTS:
$invariant_refs

Key invariants to check:
- Invariant #1 (Ambiguity is Invalid): Every term must have operational definition
- Invariant #4 (No Irreversible Without Recovery): Destructive actions need undo/confirmation
- Invariant #5 (Execution Must Fail Loudly): Errors must be visible, not silent
- Invariant #7 (Validation Must Be Executable): Success criteria must be testable
- Invariant #10 (Degradation Path Exists): What happens when dependencies fail?

SPECIFICATION:
$spec_content"

        if [[ -n "$requirements_content" ]]; then
            prompt="$prompt

REQUIREMENTS TO COVER:
$requirements_content"
        fi

        if [[ -n "$journeys_content" ]]; then
            prompt="$prompt

USER JOURNEYS TO COVER:
$journeys_content"
        fi

        prompt="$prompt

Check this spec for violations of the applicable invariants. Be specific - reference invariant numbers.

Provide:
- summary: One sentence on overall completeness
- invariant_violations: Specific invariants that may be violated (reference by number, e.g., 'Invariant #4: delete without undo') - max 5
- missing_failure_modes: Failure scenarios required by domain but not addressed - max 5
- missing_coverage: User journey steps or requirements not covered - max 5
- critical_blockers: Questions that MUST be answered before proceeding - max 5

If you are uncertain about any assessment, flag it with [UNCERTAIN: reason]. It's better to express uncertainty than to guess."

        local raw_result result
        raw_result=$(echo "$prompt" | claude --model "$CLAUDE_MODEL" --print --output-format json --json-schema "$schema" 2>/dev/null)

        # Extract structured_output from the wrapper JSON
        result=$(echo "$raw_result" | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d.get('structured_output',{})))" 2>/dev/null)

        track_cost "$prompt" "$result"

        # Store result for pipeline state
        [[ -n "$result" && "$result" != "{}" ]] && llm_result="$result"

        if [[ -n "$result" && "$result" != "{}" ]]; then
            local summary
            summary=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('summary',''))" 2>/dev/null)

            echo ""
            echo -e "Summary: $summary"
            echo ""

            # Show invariant violations
            echo -e "${RED}Invariant Violations:${NC}"
            echo "$result" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    violations = data.get('invariant_violations', [])
    if violations:
        for v in violations[:5]:
            print(f'  ✗ {v}')
    else:
        print('  (None identified - invariants satisfied)')
except:
    print('  (Could not parse)')
" 2>/dev/null

            # Show missing coverage
            echo ""
            echo -e "${YELLOW}Missing Coverage:${NC}"
            echo "$result" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    missing = data.get('missing_coverage', [])
    if missing:
        for m in missing[:5]:
            print(f'  ? {m}')
    else:
        print('  (None identified)')
except:
    print('  (Could not parse)')
" 2>/dev/null

            # Show failure modes to consider
            echo ""
            echo -e "${YELLOW}Failure Modes to Consider:${NC}"
            echo "$result" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    missing = data.get('missing_failure_modes', [])
    if missing:
        for m in missing[:5]:
            print(f'  ? {m}')
    else:
        print('  (None identified)')
except:
    print('  (Could not parse)')
" 2>/dev/null

            # Show critical blockers
            echo ""
            echo -e "${RED}Critical Blockers:${NC}"
            echo "$result" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    blockers = data.get('critical_blockers', [])
    if blockers:
        for i, b in enumerate(blockers[:5], 1):
            print(f'  {i}. {b}')
    else:
        print('  (None - ready for implementation)')
except:
    print('  (Could not parse)')
" 2>/dev/null

            echo ""
        else
            echo -e "${YELLOW}LLM call failed or returned empty${NC}"
        fi
    fi

    # ━━━ Summary ━━━
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  LIMITATIONS: This catches obvious gaps, not subtle design flaws.${NC}"
    echo -e "${CYAN}               The suggestions above matter more than this summary.${NC}"
    echo -e "${BLUE}───────────────────────────────────────────────────────────────${NC}"

    if [[ ${#issues[@]} -ge 2 ]]; then
        echo -e "  Status: ${RED}REVIEW REQUIRED${NC}"
        echo -e "  Found ${RED}${#issues[@]} gaps${NC} that likely need addressing."
        echo -e "  ${YELLOW}→ Review the suggestions above. You decide what's valid.${NC}"
    elif [[ ${#issues[@]} -ge 1 ]] || [[ ${#warnings[@]} -ge 3 ]]; then
        echo -e "  Status: ${YELLOW}ITEMS TO REVIEW${NC}"
        echo -e "  Found some potential gaps. May or may not apply to your context."
        echo -e "  ${YELLOW}→ Review the suggestions above. You decide what's valid.${NC}"
    else
        echo -e "  Status: ${GREEN}NO OBVIOUS GAPS${NC}"
        echo -e "  Basic completeness checks passed."
        echo -e "  ${YELLOW}→ This doesn't mean it's perfect. Review the suggestions anyway.${NC}"
    fi

    echo ""
    echo -e "  ${CYAN}Next step: ./design-ops-v3.sh validate $spec_file${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

    [[ "$quick" != "true" ]] && show_cost_summary

    # Save findings to pipeline state
    update_pipeline_state "$state_file" "stress-test" "$llm_result"
    echo -e "  ${DIM}State saved: $state_file${NC}"
    echo ""
}

cmd_validate() {
    local file="$1"
    local quick="$2"

    [[ ! -f "$file" ]] && { echo -e "${RED}File not found: $file${NC}"; exit 1; }

    local content
    content=$(cat "$file")

    # Get pipeline state file for this spec
    local state_file
    state_file=$(get_state_file_path "$file")

    # Variable to store LLM result for state saving
    local llm_result="{}"

    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  SPEC VALIDATION (v$VERSION)                                    ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "File: ${CYAN}$file${NC}"

    # ━━━ Domain Detection ━━━
    local domain_result
    domain_result=$(resolve_domain_invariants "$content")

    local invariant_refs total_invariants domain_count
    invariant_refs=$(echo "$domain_result" | sed -n '/^INVARIANT_REFS<<EOF$/,/^EOF$/p' | sed '1d;$d')
    total_invariants=$(echo "$domain_result" | grep "^TOTAL_INVARIANTS=" | cut -d= -f2)
    domain_count=$(echo "$domain_result" | grep "^DOMAIN_COUNT=" | cut -d= -f2)

    echo -e "  Domains: ${CYAN}$((domain_count + 1))${NC} | Invariants: ${CYAN}$total_invariants${NC}"
    echo ""

    # Deterministic checks (always run)
    local struct_output struct_grade
    struct_output=$(check_spec_structure "$file")
    echo "$struct_output" | sed '$d'  # Display all but last line (which is grade)
    struct_grade=$(echo "$struct_output" | tail -1)

    local llm_grade="SKIPPED"
    if [[ "$quick" != "true" ]]; then
        echo ""
        local llm_output
        llm_output=$(get_llm_assessment "$file" "spec")
        # Extract STATE_JSON from last line, display rest
        llm_result=$(echo "$llm_output" | grep "^STATE_JSON:" | sed 's/^STATE_JSON://')
        echo "$llm_output" | grep -v "^STATE_JSON:" | sed '$d'
        llm_grade=$(echo "$llm_output" | grep -v "^STATE_JSON:" | tail -1)
    fi

    # ━━━ Summary ━━━
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  LIMITATIONS: This checks structure and common issues, not semantic${NC}"
    echo -e "${CYAN}               correctness. The suggestions above matter more than this summary.${NC}"
    echo -e "${BLUE}───────────────────────────────────────────────────────────────${NC}"

    # Status based on structural checks only (LLM just provides suggestions)
    if [[ "$struct_grade" == "FAIL" ]]; then
        echo -e "  Status: ${RED}STRUCTURAL ISSUES${NC}"
        echo -e "  Missing required sections or has unfilled placeholders."
        echo -e "  ${YELLOW}→ Fix structural issues, then review suggestions above.${NC}"
    elif [[ "$struct_grade" == "NEEDS_WORK" ]]; then
        echo -e "  Status: ${YELLOW}ITEMS TO REVIEW${NC}"
        echo -e "  Found potential clarity issues. May or may not apply."
        echo -e "  ${YELLOW}→ Review the suggestions above. You decide what's valid.${NC}"
    else
        echo -e "  Status: ${GREEN}NO OBVIOUS GAPS${NC}"
        echo -e "  Basic structure checks passed."
        echo -e "  ${YELLOW}→ Review the suggestions above anyway.${NC}"
    fi

    echo ""
    echo -e "  ${CYAN}Next step: ./design-ops-v3.sh generate $file${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

    [[ "$quick" != "true" ]] && show_cost_summary

    # Require human acknowledgment before proceeding
    require_review_acknowledgment "validate" "$file"

    # Save findings to pipeline state
    update_pipeline_state "$state_file" "validate" "$llm_result"
    echo -e "  ${DIM}State saved: $state_file${NC}"
    echo ""
}

cmd_generate() {
    local spec_file="$1"
    local output_file="$2"

    [[ ! -f "$spec_file" ]] && { echo -e "${RED}File not found: $spec_file${NC}"; exit 1; }

    # Default output path
    if [[ -z "$output_file" ]]; then
        local basename
        basename=$(basename "$spec_file" .md)
        output_file="${spec_file%/*}/../PRPs/${basename}-prp.md"
    fi

    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  PRP GENERATION (v$VERSION)                                     ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "Input:  ${CYAN}$spec_file${NC}"
    echo -e "Output: ${CYAN}$output_file${NC}"
    echo ""

    # Create output directory if needed
    mkdir -p "$(dirname "$output_file")"

    # Generate (one-shot)
    generate_prp "$spec_file" "$output_file"

    echo ""
    echo -e "${GREEN}✓ PRP generated. Running quality check...${NC}"
    echo ""

    # Automatically run check on the generated PRP
    cmd_check "$output_file" "$QUICK"
}

cmd_check() {
    local file="$1"
    local quick="$2"

    [[ ! -f "$file" ]] && { echo -e "${RED}File not found: $file${NC}"; exit 1; }

    local content
    content=$(cat "$file")

    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  PRP QUALITY CHECK (v$VERSION)                                  ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "File: ${CYAN}$file${NC}"

    # ━━━ Domain Detection (from PRP content) ━━━
    local domain_result
    domain_result=$(resolve_domain_invariants "$content")

    local total_invariants domain_count
    total_invariants=$(echo "$domain_result" | grep "^TOTAL_INVARIANTS=" | cut -d= -f2)
    domain_count=$(echo "$domain_result" | grep "^DOMAIN_COUNT=" | cut -d= -f2)

    echo -e "  Domains: ${CYAN}$((domain_count + 1))${NC} | Invariants: ${CYAN}$total_invariants${NC}"

    # ━━━ Source Spec Detection ━━━
    local source_spec=""
    local source_spec_content=""

    # Try to extract source_spec from PRP meta block
    source_spec=$(echo "$content" | grep -E "^source_spec:" | head -1 | sed 's/source_spec://' | xargs)

    if [[ -z "$source_spec" ]]; then
        # Try alternative format: Source Spec Reference in appendix
        source_spec=$(echo "$content" | grep -E "Spec Path:" | head -1 | sed 's/.*Spec Path://' | xargs)
    fi

    if [[ -n "$source_spec" && -f "$source_spec" ]]; then
        echo -e "  Source spec: ${CYAN}$source_spec${NC}"
        source_spec_content=$(cat "$source_spec")
    else
        echo -e "  Source spec: ${YELLOW}Not found or not accessible${NC}"
    fi
    echo ""

    local struct_output struct_grade
    struct_output=$(check_prp_structure "$file")
    echo "$struct_output" | sed '$d'  # Display all but last line (which is grade)
    struct_grade=$(echo "$struct_output" | tail -1)

    local llm_grade="SKIPPED"
    if [[ "$quick" != "true" ]]; then
        echo ""

        # If we have the source spec, do a comparison check
        if [[ -n "$source_spec_content" ]]; then
            echo -e "${BLUE}━━━ Spec-to-PRP Comparison ━━━${NC}"
            echo -e "${CYAN}Checking if PRP preserved key spec content...${NC}"
            echo ""

            # Quick deterministic checks for key content preservation
            local preserved=0
            local missing=0

            # Check for SQL/schema preservation
            if echo "$source_spec_content" | grep -qiE "CREATE TABLE|ALTER TABLE|SQL"; then
                if echo "$content" | grep -qiE "CREATE TABLE|ALTER TABLE|Database Schema"; then
                    echo -e "  ${GREEN}✓${NC} Database schema content preserved"
                    ((preserved++))
                else
                    echo -e "  ${RED}✗${NC} Source has SQL/schema but PRP may be missing it"
                    ((missing++))
                fi
            fi

            # Check for API endpoint preservation
            if echo "$source_spec_content" | grep -qiE "GET /|POST /|PUT /|DELETE /|/api/"; then
                if echo "$content" | grep -qiE "GET /|POST /|PUT /|DELETE /|/api/|API Spec"; then
                    echo -e "  ${GREEN}✓${NC} API endpoints preserved"
                    ((preserved++))
                else
                    echo -e "  ${RED}✗${NC} Source has API endpoints but PRP may be missing them"
                    ((missing++))
                fi
            fi

            # Check for wireframe/ASCII art preservation
            if echo "$source_spec_content" | grep -qE "┌|└|├|│|─"; then
                if echo "$content" | grep -qE "┌|└|├|│|─"; then
                    echo -e "  ${GREEN}✓${NC} ASCII wireframes preserved"
                    ((preserved++))
                else
                    echo -e "  ${RED}✗${NC} Source has ASCII wireframes but PRP may be missing them"
                    ((missing++))
                fi
            fi

            # Check for error messages preservation
            if echo "$source_spec_content" | grep -qiE "error message|Error:|\".*not found\""; then
                if echo "$content" | grep -qiE "error message|Error Catalog|\".*not found\""; then
                    echo -e "  ${GREEN}✓${NC} Error messages preserved"
                    ((preserved++))
                else
                    echo -e "  ${YELLOW}?${NC} Source has error messages - verify PRP includes them"
                    ((missing++))
                fi
            fi

            echo ""
            if [[ $missing -gt 0 ]]; then
                echo -e "  ${YELLOW}Found $missing potential extraction gaps - review LLM assessment below${NC}"
            else
                echo -e "  ${GREEN}Key content appears preserved${NC}"
            fi
            echo ""
        fi

        local llm_output
        llm_output=$(get_llm_assessment "$file" "prp")
        echo "$llm_output" | sed '$d'
        llm_grade=$(echo "$llm_output" | tail -1)
    fi

    # ━━━ Summary ━━━
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  LIMITATIONS: This checks PRP structure and executability, not whether${NC}"
    echo -e "${CYAN}               the requirements are correct. The suggestions matter more.${NC}"
    echo -e "${BLUE}───────────────────────────────────────────────────────────────${NC}"

    # Status based on structural checks only (LLM just provides suggestions)
    if [[ "$struct_grade" == "FAIL" ]]; then
        echo -e "  Status: ${RED}STRUCTURAL ISSUES${NC}"
        echo -e "  PRP is missing sections or has unfilled placeholders."
        echo -e "  ${YELLOW}→ Fix structural issues before implementation.${NC}"
    elif [[ "$struct_grade" == "NEEDS_WORK" ]]; then
        echo -e "  Status: ${YELLOW}ITEMS TO REVIEW${NC}"
        echo -e "  Found potential issues. May or may not apply to your context."
        echo -e "  ${YELLOW}→ Review the suggestions above. You decide what matters.${NC}"
    else
        echo -e "  Status: ${GREEN}NO OBVIOUS GAPS${NC}"
        echo -e "  Basic PRP structure checks passed."
        echo -e "  ${YELLOW}→ Review the suggestions above anyway.${NC}"
    fi

    echo ""
    echo -e "  ${CYAN}Next step: Human review, then implementation${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

    [[ "$quick" != "true" ]] && show_cost_summary

    # Require human acknowledgment before proceeding
    require_review_acknowledgment "check" "$file"

    echo ""
}

# ============================================================================
# RALPH IMPLEMENTATION CHECK (validates code/steps against PRP)
# ============================================================================

check_ralph_deterministic() {
    local prp_file="$1"
    local steps_dir="$2"
    local prp_content
    prp_content=$(cat "$prp_file")

    local issues=()
    local warnings=()

    echo -e "${BLUE}━━━ Deterministic Checks ━━━${NC}"

    # 1. Extract schema definitions from PRP (generic - works with any tables)
    echo -e "${CYAN}Extracting PRP schema definitions...${NC}"

    # Extract CREATE TABLE statements from PRP
    local tables_found=0
    local prp_columns=()

    # Look for CREATE TABLE statements
    while IFS= read -r table_match; do
        if [[ -n "$table_match" ]]; then
            ((tables_found++))
            local table_name
            table_name=$(echo "$table_match" | grep -oE "CREATE TABLE [a-z_]+" | awk '{print $3}')
            echo -e "  ${GREEN}✓${NC} Found table: $table_name"

            # Extract column names from the CREATE TABLE block
            local cols
            cols=$(echo "$prp_content" | sed -n "/$table_match/,/);/p" | grep -E "^\s+[a-z_]+" | awk '{print $1}' | tr '\n' ' ')
            [[ -n "$cols" ]] && prp_columns+=("$table_name:$cols")
        fi
    done < <(echo "$prp_content" | grep -E "CREATE TABLE [a-z_]+" | head -10)

    # Also check for markdown table schemas (| column | type | format)
    if echo "$prp_content" | grep -qE "^\|.*Column.*\|.*Type.*\|"; then
        echo -e "  ${GREEN}✓${NC} Found markdown schema tables"
        ((tables_found++))
    fi

    # Also check for column mapping tables
    if echo "$prp_content" | grep -qiE "column.*mapping|import.*column"; then
        echo -e "  ${GREEN}✓${NC} Found column mapping definitions"
        ((tables_found++))
    fi

    if [[ $tables_found -eq 0 ]]; then
        warnings+=("No explicit schema definitions found in PRP")
    fi

    # Check Ralph steps for schema consistency (generic check)
    if [[ -d "$steps_dir" ]] && [[ $tables_found -gt 0 ]]; then
        echo ""
        echo -e "${CYAN}Checking schema consistency with steps...${NC}"

        # Extract column names mentioned in PRP (from CREATE TABLE or markdown tables)
        local prp_fields
        prp_fields=$(echo "$prp_content" | grep -oE '\b[a-z]+_[a-z_]+\b' | sort -u | tr '\n' ' ')

        # Extract column names mentioned in steps
        local step_fields
        step_fields=$(cat "$steps_dir"/*.sh 2>/dev/null | grep -oE '\b[a-z]+_[a-z_]+\b' | sort -u | tr '\n' ' ')

        # Find fields in steps but not in PRP (potential mismatches)
        local mismatches=0
        for field in $step_fields; do
            # Skip common non-schema words
            [[ "$field" =~ ^(npm_run|git_add|echo_e|set_e|local_|dev_null)$ ]] && continue

            # Check if it looks like a database field and isn't in PRP
            if [[ "$field" =~ _id$|_name$|_type$|_code$|_date$|_at$ ]]; then
                if ! echo "$prp_fields" | grep -qw "$field"; then
                    # Only warn if it's a likely schema field
                    if echo "$prp_content" | grep -qiE "schema|table|column"; then
                        ((mismatches++))
                        [[ $mismatches -le 3 ]] && warnings+=("Field '$field' in steps but not found in PRP schema")
                    fi
                fi
            fi
        done

        if [[ $mismatches -eq 0 ]]; then
            echo -e "  ${GREEN}✓${NC} No obvious schema mismatches detected"
        else
            echo -e "  ${YELLOW}!${NC} Found $mismatches potential field name mismatches"
        fi
    fi

    # 2. Check for route definitions
    echo ""
    echo -e "${CYAN}Checking route definitions...${NC}"

    local prp_routes=()
    while IFS= read -r route; do
        [[ -n "$route" ]] && prp_routes+=("$route")
    done < <(echo "$prp_content" | grep -oE '/[a-z]+(/[a-z]+)?' | sort -u)

    if [[ ${#prp_routes[@]} -gt 0 ]]; then
        echo -e "  ${GREEN}✓${NC} PRP defines routes: ${prp_routes[*]}"

        # Verify routes exist in steps
        if [[ -d "$steps_dir" ]]; then
            for route in "${prp_routes[@]}"; do
                if ! grep -rq "$route" "$steps_dir"/*.sh 2>/dev/null; then
                    warnings+=("Route '$route' defined in PRP but not found in steps")
                fi
            done
        fi
    fi

    # 3. Check success criteria coverage
    echo ""
    echo -e "${CYAN}Checking success criteria coverage...${NC}"

    local criteria_count=0
    while IFS= read -r line; do
        if echo "$line" | grep -qE '^\|[^|]+\|[^|]+\|'; then
            ((criteria_count++))
        fi
    done < <(echo "$prp_content" | sed -n '/Success Criteria/,/^##/p' | grep -E '^\|')

    if [[ $criteria_count -gt 0 ]]; then
        echo -e "  ${GREEN}✓${NC} Found $criteria_count success criteria in PRP"
    else
        warnings+=("No tabular success criteria found in PRP")
    fi

    # 4. Check validation requirements
    echo ""
    echo -e "${CYAN}Checking validation requirements...${NC}"

    if echo "$prp_content" | grep -qiE "validation|validat"; then
        # Extract specific validation rules
        local validation_rules=()
        while IFS= read -r rule; do
            [[ -n "$rule" ]] && validation_rules+=("$rule")
        done < <(echo "$prp_content" | grep -iE "must|should|required|format.*valid|unique" | head -10)

        echo -e "  ${GREEN}✓${NC} Found ${#validation_rules[@]} validation rules in PRP"
    else
        warnings+=("No validation rules found in PRP")
    fi

    # 5. Step header format checks (2026 best practices)
    echo ""
    echo -e "${CYAN}Checking step header format...${NC}"

    for step in "$steps_dir"/step-*.sh; do
        [[ ! -f "$step" ]] && continue
        local step_name
        step_name=$(basename "$step")

        # Check for invariant references
        if ! grep -q "Invariants Applied:" "$step"; then
            issues+=("$step_name: Missing 'Invariants Applied:' section in header")
        else
            echo -e "  ${GREEN}✓${NC} $step_name: Has invariant references"
        fi

        # Check for thinking level
        if ! grep -q "Thinking Level:" "$step"; then
            warnings+=("$step_name: Missing 'Thinking Level:' in header")
        fi

        # Check for confidence
        if ! grep -q "Confidence:" "$step"; then
            warnings+=("$step_name: Missing 'Confidence:' in header")
        fi

        # Check for PRP hash
        if ! grep -q "PRP Hash:" "$step"; then
            warnings+=("$step_name: Missing 'PRP Hash:' for traceability")
        fi

        # Check for OBJECTIVE section
        if ! grep -q "=== OBJECTIVE" "$step"; then
            warnings+=("$step_name: Missing '=== OBJECTIVE ===' section")
        fi

        # Check for ACCEPTANCE CRITERIA section
        if ! grep -q "=== ACCEPTANCE CRITERIA" "$step"; then
            warnings+=("$step_name: Missing '=== ACCEPTANCE CRITERIA ===' section")
        fi
    done

    # 6. Test format checks
    echo ""
    echo -e "${CYAN}Checking test format...${NC}"

    for test in "$steps_dir"/test-*.sh; do
        [[ ! -f "$test" ]] && continue
        local test_name
        test_name=$(basename "$test")

        # Check for PRP SUCCESS CRITERIA section
        if ! grep -q "=== PRP SUCCESS CRITERIA" "$test"; then
            issues+=("$test_name: Missing '=== PRP SUCCESS CRITERIA (VERBATIM) ===' section")
        else
            echo -e "  ${GREEN}✓${NC} $test_name: Has verbatim success criteria"
        fi

        # Check for PRP VALIDATION COMMANDS section
        if ! grep -q "=== PRP VALIDATION COMMANDS" "$test"; then
            warnings+=("$test_name: Missing '=== PRP VALIDATION COMMANDS (VERBATIM) ===' section")
        fi

        # Check for PLAYWRIGHT_VERIFY
        if ! grep -q "PLAYWRIGHT_VERIFY" "$test"; then
            warnings+=("$test_name: Missing PLAYWRIGHT_VERIFY JSON block")
        else
            # Check PLAYWRIGHT_VERIFY has prp_ref
            if ! grep -A 30 "PLAYWRIGHT_VERIFY" "$test" | grep -q "prp_ref\|prp_criteria"; then
                warnings+=("$test_name: PLAYWRIGHT_VERIFY missing prp_ref/prp_criteria fields")
            else
                echo -e "  ${GREEN}✓${NC} $test_name: PLAYWRIGHT_VERIFY has prp references"
            fi
        fi

        # Check for invariant checks
        if ! grep -q "check_invariant_\|Invariant #" "$test"; then
            warnings+=("$test_name: No invariant-specific checks found")
        fi
    done

    # 7. Gate format checks
    echo ""
    echo -e "${CYAN}Checking gate format...${NC}"

    for gate in "$steps_dir"/gate-*.sh; do
        [[ ! -f "$gate" ]] && continue
        local gate_name
        gate_name=$(basename "$gate")

        # Check for success criteria aggregation
        if ! grep -q "Success Criteria Aggregated:" "$gate"; then
            issues+=("$gate_name: Missing 'Success Criteria Aggregated:' in header")
        else
            echo -e "  ${GREEN}✓${NC} $gate_name: Has success criteria aggregation"
        fi

        # Check for performance targets
        if ! grep -qE "Performance Targets:|BUILD_TIME|performance" "$gate"; then
            warnings+=("$gate_name: Missing performance target checks")
        fi

        # Check for accessibility audit
        if ! grep -qE "axe|accessibility|Invariant #11" "$gate"; then
            warnings+=("$gate_name: Missing accessibility audit (Invariant #11)")
        fi

        # Check for phase test execution
        if ! grep -qE "for test in|test-.*\.sh" "$gate"; then
            warnings+=("$gate_name: Doesn't appear to run phase tests")
        fi
    done

    # 8. PRP hash verification
    echo ""
    echo -e "${CYAN}Checking PRP hash consistency...${NC}"

    local current_prp_hash
    current_prp_hash=$(md5sum "$prp_file" 2>/dev/null | cut -c1-7 || md5 -q "$prp_file" 2>/dev/null | cut -c1-7 || echo "unknown")

    local hash_mismatches=0
    for file in "$steps_dir"/step-*.sh "$steps_dir"/test-*.sh "$steps_dir"/gate-*.sh; do
        [[ ! -f "$file" ]] && continue
        local file_hash
        file_hash=$(grep "PRP Hash:" "$file" 2>/dev/null | awk '{print $NF}')
        if [[ -n "$file_hash" && "$file_hash" != "$current_prp_hash" ]]; then
            warnings+=("$(basename "$file"): PRP hash mismatch (file: $file_hash, current: $current_prp_hash)")
            ((hash_mismatches++))
        fi
    done

    if [[ $hash_mismatches -eq 0 ]]; then
        echo -e "  ${GREEN}✓${NC} All files have consistent PRP hash (or no hash headers)"
    else
        echo -e "  ${YELLOW}!${NC} $hash_mismatches files have stale PRP hash"
    fi

    # 9. Coverage matrix checks
    echo ""
    echo -e "${CYAN}Checking PRP-COVERAGE.md...${NC}"

    local coverage_file="$steps_dir/PRP-COVERAGE.md"
    if [[ -f "$coverage_file" ]]; then
        # Check for SC→test mapping
        if ! grep -qE "Success Criteria.*Test Mapping|SC-.*test-" "$coverage_file"; then
            warnings+=("PRP-COVERAGE.md: Missing Success Criteria → Test mapping table")
        else
            echo -e "  ${GREEN}✓${NC} Has SC → Test mapping"
        fi

        # Check for invariant coverage table
        if ! grep -q "Invariant Coverage" "$coverage_file"; then
            warnings+=("PRP-COVERAGE.md: Missing Invariant Coverage table")
        else
            echo -e "  ${GREEN}✓${NC} Has Invariant Coverage table"
        fi
    else
        issues+=("PRP-COVERAGE.md: File not found")
    fi

    # 10. Generation log check
    local gen_log="$steps_dir/RALPH-GENERATION-LOG.md"
    if [[ -f "$gen_log" ]]; then
        echo -e "  ${GREEN}✓${NC} RALPH-GENERATION-LOG.md exists"
    else
        warnings+=("RALPH-GENERATION-LOG.md: File not found (uncertainties not documented)")
    fi

    echo ""

    # Report
    if [[ ${#issues[@]} -gt 0 ]]; then
        echo -e "${RED}Issues (implementation doesn't match PRP):${NC}"
        for issue in "${issues[@]}"; do
            echo -e "  ${RED}✗${NC} $issue"
        done
    fi

    if [[ ${#warnings[@]} -gt 0 ]]; then
        echo -e "${YELLOW}Warnings (consider reviewing):${NC}"
        for warning in "${warnings[@]}"; do
            echo -e "  ${YELLOW}!${NC} $warning"
        done
    fi

    # Return grade
    if [[ ${#issues[@]} -gt 0 ]]; then
        echo "FAIL"
    elif [[ ${#warnings[@]} -gt 2 ]]; then
        echo "NEEDS_WORK"
    else
        echo "PASS"
    fi
}

get_ralph_llm_assessment() {
    local prp_file="$1"
    local steps_dir="$2"
    local prp_content
    prp_content=$(cat "$prp_file")

    # Get a sample of step content (first 3 steps)
    local steps_sample=""
    for step in $(ls "$steps_dir"/step-*.sh 2>/dev/null | head -3); do
        steps_sample+="--- $(basename "$step") ---"$'\n'
        steps_sample+=$(head -100 "$step")$'\n\n'
    done

    echo -e "${BLUE}━━━ LLM Advisory Assessment ━━━${NC}"
    echo -e "${CYAN}Analyzing PRP compliance...${NC}"

    local schema='{"type":"object","properties":{"summary":{"type":"string"},"compliance_gaps":{"type":"array","items":{"type":"string"}},"schema_issues":{"type":"array","items":{"type":"string"}},"missing_features":{"type":"array","items":{"type":"string"}},"strengths":{"type":"array","items":{"type":"string"}}},"required":["summary","compliance_gaps"]}'

    local prompt="You are validating that implementation steps match a PRP (Product Requirements Prompt).

PRP (SOURCE OF TRUTH):
$prp_content

IMPLEMENTATION STEPS (sample):
$steps_sample

Analyze whether the implementation follows the PRP. Provide:
- summary: One sentence on overall compliance
- compliance_gaps: Specific ways the steps deviate from PRP requirements (max 5)
- schema_issues: Field names, types, or constraints that don't match PRP definitions (max 5)
- missing_features: PRP features not addressed in the steps (max 5)
- strengths: What the implementation does well (1-2)

If you are uncertain about any assessment, flag it with [UNCERTAIN: reason]. It's better to express uncertainty than to guess."

    local raw_result result
    raw_result=$(echo "$prompt" | claude --model "$CLAUDE_MODEL" --print --output-format json --json-schema "$schema" 2>/dev/null)

    result=$(echo "$raw_result" | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d.get('structured_output',{})))" 2>/dev/null)

    track_cost "$prompt" "$result"

    if [[ -z "$result" || "$result" == "{}" ]]; then
        echo -e "${YELLOW}LLM call failed or returned empty${NC}"
        echo "SKIPPED"
        return
    fi

    local summary
    summary=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('summary',''))" 2>/dev/null)

    echo ""
    echo -e "Summary: $summary"
    echo ""

    echo -e "${YELLOW}Compliance Gaps:${NC}"
    echo "$result" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    gaps = data.get('compliance_gaps', [])
    if gaps:
        for g in gaps[:5]:
            print(f'  ✗ {g}')
    else:
        print('  (None identified)')
except:
    print('  (Could not parse)')
" 2>/dev/null

    echo ""
    echo -e "${YELLOW}Schema Issues:${NC}"
    echo "$result" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    issues = data.get('schema_issues', [])
    if issues:
        for i in issues[:5]:
            print(f'  ✗ {i}')
    else:
        print('  (None identified)')
except:
    print('  (Could not parse)')
" 2>/dev/null

    echo ""
    echo -e "${YELLOW}Missing Features:${NC}"
    echo "$result" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    missing = data.get('missing_features', [])
    if missing:
        for m in missing[:5]:
            print(f'  ? {m}')
    else:
        print('  (None identified)')
except:
    print('  (Could not parse)')
" 2>/dev/null

    echo ""
    echo -e "${GREEN}Strengths:${NC}"
    echo "$result" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    strengths = data.get('strengths', [])
    if strengths:
        for s in strengths[:3]:
            print(f'  ✓ {s}')
    else:
        print('  (None noted)')
except:
    print('  (Could not parse)')
" 2>/dev/null

    echo ""
    echo "DONE"
}

# ============================================================================
# RALPH STEP GENERATION (implement command)
# ============================================================================

cmd_implement() {
    local prp_file="$1"
    local output_dir="$2"
    local phase="$3"  # Optional: --parallel=N
    
    [[ ! -f "$prp_file" ]] && { echo -e "${RED}PRP file not found: $prp_file${NC}"; exit 1; }
    
    # Delegate to implement-incremental.sh (parallelized)
    local script_dir
    script_dir="$(dirname "${BASH_SOURCE[0]}")"
    
    local args=("$prp_file")
    [[ -n "$output_dir" ]] && args+=("--output" "$output_dir")
    [[ -n "$phase" ]] && args+=("$phase")  # Pass through --parallel=N
    
    exec "$script_dir/implement-incremental.sh" "${args[@]}"
}

# ============================================================================
# IMPLEMENT-PREPARE: Prepare prompts for Claude Code direct generation
# ============================================================================
cmd_implement_prepare() {
    local prp_file="$1"
    local output_dir="$2"

    [[ ! -f "$prp_file" ]] && { echo -e "${RED}PRP file not found: $prp_file${NC}"; exit 1; }

    local prp_content
    prp_content=$(cat "$prp_file")

    local prp_name
    prp_name=$(basename "$prp_file" .md | sed 's/-prp$//')

    # Default output directory
    if [[ -z "$output_dir" ]]; then
        output_dir="./ralph-steps-${prp_name}"
    fi

    mkdir -p "$output_dir/.prompts"

    # Extract PRP metadata
    local prp_id prp_hash
    prp_id=$(echo "$prp_content" | grep -E "^prp_id:" | head -1 | sed 's/.*://' | xargs)
    if command -v md5sum &> /dev/null; then
        prp_hash=$(md5sum "$prp_file" | cut -c1-7)
    else
        prp_hash=$(md5 -q "$prp_file" | cut -c1-7)
    fi

    # =========================================================================
    # Extract Success Criteria from Section 2
    # =========================================================================
    # Supports two formats:
    # 1. | ID | Criterion | Metric |  (SC-N.N format)
    # 2. | Metric | Target | Measurement | (generate SC-N.N from row number)
    local success_criteria=()
    local in_success_criteria=0
    local sc_row=0
    local sc_format=""  # "id_first" or "metric_first"

    while IFS= read -r line; do
        # Detect Section 2 header
        if [[ "$line" =~ ^##\ 2\.\ Success\ Criteria ]] || [[ "$line" =~ ^##\ 2\ Success\ Criteria ]]; then
            in_success_criteria=1
            continue
        fi

        # Exit when hitting next section
        if [[ $in_success_criteria -eq 1 && "$line" =~ ^##\ [0-9] ]]; then
            in_success_criteria=0
        fi

        # Skip header separator
        [[ "$line" =~ ^\|-+\| ]] && continue

        # Detect format from header row
        if [[ $in_success_criteria -eq 1 && "$line" =~ ^\|.*ID.*Criterion ]]; then
            sc_format="id_first"
            continue
        fi
        if [[ $in_success_criteria -eq 1 && "$line" =~ ^\|.*Metric.*Target ]]; then
            sc_format="metric_first"
            continue
        fi

        # Parse table rows
        if [[ $in_success_criteria -eq 1 && "$line" =~ ^\|[^-] ]]; then
            # Remove leading/trailing pipes and split
            local row
            row=$(echo "$line" | sed 's/^|//;s/|$//' | sed 's/|/\t/g')

            if [[ "$sc_format" == "id_first" ]]; then
                # Format: | SC-1.1 | Criterion | Metric |
                local sc_id sc_criterion sc_metric
                sc_id=$(echo "$row" | cut -f1 | xargs)
                sc_criterion=$(echo "$row" | cut -f2 | xargs)
                sc_metric=$(echo "$row" | cut -f3 | xargs)
                [[ -n "$sc_id" && "$sc_id" != "ID" ]] && success_criteria+=("$sc_id|$sc_criterion|$sc_metric")
            elif [[ "$sc_format" == "metric_first" ]]; then
                # Format: | Metric | Target | Measurement |
                # Generate SC-G.N (G = Global, applies to all phases)
                sc_row=$((sc_row + 1))
                local sc_metric sc_target sc_measurement
                sc_metric=$(echo "$row" | cut -f1 | xargs)
                sc_target=$(echo "$row" | cut -f2 | xargs)
                sc_measurement=$(echo "$row" | cut -f3 | xargs)
                [[ -n "$sc_metric" && "$sc_metric" != "Metric" ]] && success_criteria+=("SC-G.${sc_row}|$sc_metric: $sc_target|$sc_measurement")
            fi
        fi
    done < "$prp_file"

    # =========================================================================
    # Extract Global Validation Commands from Section 8
    # =========================================================================
    local global_validation_commands=()
    local in_validation_section=0
    local in_code_block=0

    while IFS= read -r line; do
        # Detect Section 8 header
        if [[ "$line" =~ ^##\ 8\.\ Validation\ Commands ]] || [[ "$line" =~ ^##\ [0-9]+\.\ Validation\ Commands ]]; then
            in_validation_section=1
            continue
        fi

        # Exit when hitting next section
        if [[ $in_validation_section -eq 1 && "$line" =~ ^##\ [0-9] && ! "$line" =~ Validation ]]; then
            in_validation_section=0
        fi

        # Track code blocks
        if [[ $in_validation_section -eq 1 ]]; then
            if [[ "$line" =~ ^\`\`\`bash ]]; then
                in_code_block=1
                continue
            fi
            if [[ "$line" =~ ^\`\`\` && $in_code_block -eq 1 ]]; then
                in_code_block=0
                continue
            fi
            # Capture commands (skip comments and empty lines)
            if [[ $in_code_block -eq 1 && -n "$line" && ! "$line" =~ ^#.*Expected ]]; then
                global_validation_commands+=("$line")
            fi
        fi
    done < "$prp_file"

    # =========================================================================
    # Extract Deliverables, Phases, and Per-Phase Validation Commands
    # =========================================================================
    local deliverables=()
    local phases=()
    local phase_validation_commands=()  # Indexed by phase number
    local in_deliverables=0
    local in_phase_code_block=0
    local current_phase=""
    local current_phase_num=""
    local current_phase_cmds=""

    while IFS= read -r line; do
        # Stop processing phases when hitting a major section (## N.)
        if [[ "$line" =~ ^##\ [0-9]+\. && ! "$line" =~ Timeline ]]; then
            # Save final phase's commands before exiting
            if [[ -n "$current_phase_num" && -n "$current_phase_cmds" ]]; then
                phase_validation_commands+=("$current_phase_num|$current_phase_cmds")
                current_phase_num=""
                current_phase_cmds=""
            fi
            continue
        fi

        if [[ "$line" =~ ^###\ Phase\ ([0-9]+):\ (.+) ]]; then
            # Save previous phase's validation commands
            if [[ -n "$current_phase_num" && -n "$current_phase_cmds" ]]; then
                phase_validation_commands+=("$current_phase_num|$current_phase_cmds")
            fi

            current_phase_num="${BASH_REMATCH[1]}"
            current_phase="${BASH_REMATCH[1]}: ${BASH_REMATCH[2]}"
            current_phase_cmds=""

            # Track unique phases
            local phase_exists=0
            for p in "${phases[@]}"; do
                [[ "$p" == "$current_phase" ]] && phase_exists=1 && break
            done
            [[ $phase_exists -eq 0 ]] && phases+=("$current_phase")
            in_deliverables=0
            in_phase_code_block=0
        fi

        # Match both **Deliverables:** and #### Deliverables formats
        if [[ "$line" == "**Deliverables:**" || "$line" =~ ^#{1,4}[[:space:]]*Deliverables ]]; then
            in_deliverables=1
            continue
        fi

        # End deliverables section on next heading, bold section, or empty line
        if [[ $in_deliverables -eq 1 && ("$line" == "**Validation Gate:**" || "$line" =~ ^\*\* || "$line" =~ ^### || "$line" =~ ^#### || -z "$line") ]]; then
            in_deliverables=0
        fi

        if [[ $in_deliverables -eq 1 && "$line" =~ ^-\ (.+) ]]; then
            local deliverable="${BASH_REMATCH[1]}"
            # Strip checkbox markers [ ] if present
            deliverable="${deliverable#\[ \] }"
            deliverable="${deliverable#\[\] }"
            deliverables+=("$current_phase|$deliverable")
        fi

        # Capture per-phase validation commands (code blocks after deliverables, within phases only)
        if [[ -n "$current_phase_num" && "$line" =~ ^\`\`\`bash ]]; then
            in_phase_code_block=1
            continue
        fi
        if [[ "$line" =~ ^\`\`\` && $in_phase_code_block -eq 1 ]]; then
            in_phase_code_block=0
            continue
        fi
        if [[ $in_phase_code_block -eq 1 && -n "$line" && ! "$line" =~ ^#.*Expected ]]; then
            [[ -n "$current_phase_cmds" ]] && current_phase_cmds="$current_phase_cmds;"
            current_phase_cmds="${current_phase_cmds}${line}"
        fi
    done < "$prp_file"

    # Save last phase's validation commands
    if [[ -n "$current_phase_num" && -n "$current_phase_cmds" ]]; then
        phase_validation_commands+=("$current_phase_num|$current_phase_cmds")
    fi

    local total=${#deliverables[@]}
    local total_phases=${#phases[@]}

    [[ $total -eq 0 ]] && { echo -e "${RED}No deliverables found in PRP${NC}"; exit 1; }

    # Generate individual prompt files
    for i in "${!deliverables[@]}"; do
        local step_num=$((i + 1))
        local step_padded=$(printf "%02d" $step_num)
        IFS='|' read -r phase deliverable <<< "${deliverables[$i]}"

        # Extract phase number
        local phase_num
        phase_num=$(echo "$phase" | cut -d: -f1 | xargs)

        # Build acceptance criteria section from extracted success_criteria
        # Include both phase-specific (SC-N.x) and global (SC-G.x) criteria
        local criteria_section=""
        for sc in "${success_criteria[@]}"; do
            local sc_id sc_criterion sc_metric
            IFS='|' read -r sc_id sc_criterion sc_metric <<< "$sc"
            # Match SC-N.x where N is the phase number, OR SC-G.x (global)
            if [[ "$sc_id" =~ ^SC-${phase_num}\. ]] || [[ "$sc_id" =~ ^SC-G\. ]]; then
                criteria_section="${criteria_section}# ${sc_id}: ${sc_criterion} | ${sc_metric}
"
            fi
        done

        # Build validation commands section for this phase
        local validation_section=""
        for pvc in "${phase_validation_commands[@]}"; do
            local pnum pcmds
            IFS='|' read -r pnum pcmds <<< "$pvc"
            if [[ "$pnum" == "$phase_num" ]]; then
                IFS=';' read -ra cmds <<< "$pcmds"
                for cmd in "${cmds[@]}"; do
                    [[ -n "$cmd" ]] && validation_section="${validation_section}# ${cmd}
"
                done
            fi
        done

        cat > "$output_dir/.prompts/step-${step_padded}.prompt.md" << PROMPT_EOF
# Generate Step ${step_padded}

## Context
- PRP ID: ${prp_id:-unknown}
- PRP Hash: ${prp_hash}
- Phase: ${phase}
- Step Number: ${step_num}
- Deliverable: ${deliverable}

## Success Criteria (EXTRACTED FROM PRP - use VERBATIM)
${criteria_section:-# No criteria found for this phase - generate appropriate SC-${phase_num}.N criteria}

## Validation Commands (EXTRACTED FROM PRP)
${validation_section:-# No validation commands for this phase}

## Task
Generate \`step-${step_padded}.sh\` implementing this deliverable.

## Required Output Format (EXACT - all sections required)
\`\`\`bash
#!/bin/bash
# ==============================================================================
# Step ${step_num}: ${deliverable}
# ==============================================================================
# PRP: ${prp_id:-unknown}
# PRP Hash: ${prp_hash}
# PRP Phase: Phase ${phase}
# PRP Deliverable: ${deliverable}
#
# Invariants Applied:
#   - #1 (Ambiguity): No vague terms, specific implementation
#   - #7 (Validation): Testable outputs
#
# Thinking Level: Normal
# Confidence: 7/10 (Medium)
# ==============================================================================

set -e

echo "Step ${step_num}: ${deliverable}"

# === OBJECTIVE ===
# ${deliverable}

# === ACCEPTANCE CRITERIA (from PRP Section 2) ===
${criteria_section:-# SC-${phase_num}.1: [criterion]}

# === IMPLEMENTATION ===
# [Your implementation here - actual code, not placeholders]

echo "Step ${step_num} complete"
\`\`\`

## Rules
1. Generate actual implementation code, not placeholders
2. Be specific about files to create/modify
3. Include working code snippets
4. Reference the deliverable exactly
5. MUST include "Invariants Applied:" section in header
6. MUST include "Thinking Level:" and "Confidence:" in header
7. MUST include "=== ACCEPTANCE CRITERIA ===" section with criteria from above
PROMPT_EOF
    done

    # Generate test prompt template
    cat > "$output_dir/.prompts/tests.prompt.md" << 'TEST_PROMPT_EOF'
# Generate Test Files

For each step-NN.sh, generate a corresponding test-NN.sh with this EXACT structure:

```bash
#!/bin/bash
# ==============================================================================
# Test NN: [deliverable]
# ==============================================================================
# PRP: [prp_id]
# PRP Phase: [Phase N]
# Success Criteria Tested: SC-N.1, SC-N.2
# Invariants Verified: #1, #7
# ==============================================================================

set -e

PASS=0
FAIL=0

check() {
    if eval "$1"; then
        echo "  [PASS] $2"
        PASS=$((PASS + 1))
    else
        echo "  [FAIL] $2"
        FAIL=$((FAIL + 1))
    fi
}

echo "Testing Step NN: [deliverable]"

# === PRP SUCCESS CRITERIA (VERBATIM from PRP Section 2) ===
# SC-N.1: [exact text from PRP]
# SC-N.2: [exact text from PRP]
# === END PRP CRITERIA ===

# === FILE EXISTENCE CHECKS ===
check "test -f <expected_file>" "SC-N.1: File exists"

# === CONTENT CHECKS ===
check "grep -q '<expected_content>' <file>" "SC-N.2: Content correct"

# === PRP VALIDATION COMMANDS (VERBATIM from PRP Appendix) ===
# [Copy validation commands from PRP if any]
# === END VERBATIM ===

# === INVARIANT #7: Validation Executable ===
check "true" "Invariant #7: All checks are executable"

# === PLAYWRIGHT VERIFICATION (if UI step) ===
cat << 'PLAYWRIGHT_VERIFY'
{
  "route": "/path",
  "prp_phase": "N.M",
  "prp_criteria": ["SC-N.1"],
  "checks": [
    { "type": "heading", "level": 1, "text": "Expected Title" }
  ]
}
PLAYWRIGHT_VERIFY

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] || exit 1
```

## REQUIRED Sections (all must be present):
1. `# === PRP SUCCESS CRITERIA (VERBATIM from PRP Section 2) ===`
2. `# === PRP VALIDATION COMMANDS (VERBATIM from PRP Appendix) ===`
3. `PLAYWRIGHT_VERIFY` JSON block (even if empty for non-UI steps)
4. Invariant-specific checks (reference by number)
TEST_PROMPT_EOF

    # Generate manifest JSON
    local manifest_file="$output_dir/.manifest.json"

    # Helper function to get phase validation commands
    get_phase_validation() {
        local phase_num="$1"
        for pvc in "${phase_validation_commands[@]}"; do
            local pnum pcmds
            IFS='|' read -r pnum pcmds <<< "$pvc"
            if [[ "$pnum" == "$phase_num" ]]; then
                echo "$pcmds"
                return
            fi
        done
        echo ""
    }

    # Helper function to get success criteria for a phase
    # Includes both phase-specific (SC-N.x) and global (SC-G.x) criteria
    get_phase_criteria() {
        local phase_num="$1"
        local criteria=""
        for sc in "${success_criteria[@]}"; do
            local sc_id sc_crit sc_metric
            IFS='|' read -r sc_id sc_crit sc_metric <<< "$sc"
            # Match SC-N.x where N is the phase number, OR SC-G.x (global)
            if [[ "$sc_id" =~ ^SC-${phase_num}\. ]] || [[ "$sc_id" =~ ^SC-G\. ]]; then
                [[ -n "$criteria" ]] && criteria="$criteria,"
                criteria="${criteria}\"$sc_id\""
            fi
        done
        echo "$criteria"
    }

    # Build JSON manually (no jq dependency)
    echo "{" > "$manifest_file"
    echo "  \"prp_id\": \"${prp_id:-unknown}\"," >> "$manifest_file"
    echo "  \"prp_hash\": \"${prp_hash}\"," >> "$manifest_file"
    echo "  \"prp_file\": \"$(realpath "$prp_file")\"," >> "$manifest_file"
    echo "  \"output_dir\": \"$(realpath "$output_dir")\"," >> "$manifest_file"
    echo "  \"total_steps\": ${total}," >> "$manifest_file"
    echo "  \"total_phases\": ${total_phases}," >> "$manifest_file"

    # Success criteria array
    echo "  \"success_criteria\": [" >> "$manifest_file"
    for i in "${!success_criteria[@]}"; do
        local sc_id sc_criterion sc_metric
        IFS='|' read -r sc_id sc_criterion sc_metric <<< "${success_criteria[$i]}"
        local comma=","
        [[ $i -eq $((${#success_criteria[@]} - 1)) ]] && comma=""
        # Escape quotes
        sc_criterion=$(echo "$sc_criterion" | sed 's/"/\\"/g')
        sc_metric=$(echo "$sc_metric" | sed 's/"/\\"/g')
        echo "    {" >> "$manifest_file"
        echo "      \"id\": \"${sc_id}\"," >> "$manifest_file"
        echo "      \"criterion\": \"${sc_criterion}\"," >> "$manifest_file"
        echo "      \"metric\": \"${sc_metric}\"" >> "$manifest_file"
        echo "    }${comma}" >> "$manifest_file"
    done
    echo "  ]," >> "$manifest_file"

    # Global validation commands array
    echo "  \"global_validation_commands\": [" >> "$manifest_file"
    for i in "${!global_validation_commands[@]}"; do
        local cmd="${global_validation_commands[$i]}"
        local comma=","
        [[ $i -eq $((${#global_validation_commands[@]} - 1)) ]] && comma=""
        # Escape quotes and backslashes
        cmd=$(echo "$cmd" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')
        echo "    \"${cmd}\"${comma}" >> "$manifest_file"
    done
    echo "  ]," >> "$manifest_file"

    # Phases array
    echo "  \"phases\": [" >> "$manifest_file"
    for i in "${!phases[@]}"; do
        local comma=","
        [[ $i -eq $((${#phases[@]} - 1)) ]] && comma=""
        echo "    \"${phases[$i]}\"${comma}" >> "$manifest_file"
    done
    echo "  ]," >> "$manifest_file"

    # Deliverables array with linked criteria and validation commands
    echo "  \"deliverables\": [" >> "$manifest_file"
    for i in "${!deliverables[@]}"; do
        local step_num=$((i + 1))
        local step_padded=$(printf "%02d" $step_num)
        IFS='|' read -r phase deliverable <<< "${deliverables[$i]}"
        local comma=","
        [[ $i -eq $((${#deliverables[@]} - 1)) ]] && comma=""

        # Extract phase number from "N: Title"
        local phase_num
        phase_num=$(echo "$phase" | cut -d: -f1 | xargs)

        # Get linked success criteria for this phase
        local linked_criteria
        linked_criteria=$(get_phase_criteria "$phase_num")

        # Get validation commands for this phase
        local phase_cmds
        phase_cmds=$(get_phase_validation "$phase_num")

        # Escape quotes in deliverable
        deliverable=$(echo "$deliverable" | sed 's/"/\\"/g')

        echo "    {" >> "$manifest_file"
        echo "      \"step\": ${step_num}," >> "$manifest_file"
        echo "      \"step_padded\": \"${step_padded}\"," >> "$manifest_file"
        echo "      \"phase\": \"${phase}\"," >> "$manifest_file"
        echo "      \"phase_num\": ${phase_num}," >> "$manifest_file"
        echo "      \"deliverable\": \"${deliverable}\"," >> "$manifest_file"
        echo "      \"success_criteria\": [${linked_criteria}]," >> "$manifest_file"
        if [[ -n "$phase_cmds" ]]; then
            # Split by ; and output as array
            echo -n "      \"validation_commands\": [" >> "$manifest_file"
            local first=1
            IFS=';' read -ra cmds <<< "$phase_cmds"
            for cmd in "${cmds[@]}"; do
                [[ -z "$cmd" ]] && continue
                cmd=$(echo "$cmd" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | xargs)
                [[ $first -eq 0 ]] && echo -n ", " >> "$manifest_file"
                echo -n "\"$cmd\"" >> "$manifest_file"
                first=0
            done
            echo "]," >> "$manifest_file"
        else
            echo "      \"validation_commands\": []," >> "$manifest_file"
        fi
        echo "      \"prompt_file\": \".prompts/step-${step_padded}.prompt.md\"," >> "$manifest_file"
        echo "      \"output_file\": \"step-${step_padded}.sh\"," >> "$manifest_file"
        echo "      \"test_file\": \"test-${step_padded}.sh\"" >> "$manifest_file"
        echo "    }${comma}" >> "$manifest_file"
    done
    echo "  ]" >> "$manifest_file"
    echo "}" >> "$manifest_file"

    # Output summary
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  IMPLEMENT-PREPARE COMPLETE                                   ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "PRP:        ${CYAN}${prp_file}${NC}"
    echo -e "Output:     ${CYAN}${output_dir}${NC}"
    echo -e "Manifest:   ${CYAN}${output_dir}/.manifest.json${NC}"
    echo -e "Prompts:    ${CYAN}${total} step prompts in .prompts/${NC}"
    echo -e "Phases:     ${CYAN}${total_phases}${NC}"
    echo -e "Criteria:   ${CYAN}${#success_criteria[@]} success criteria extracted${NC}"
    echo -e "Commands:   ${CYAN}${#global_validation_commands[@]} global + ${#phase_validation_commands[@]} per-phase${NC}"
    echo ""
    echo -e "${YELLOW}Ready for Claude Code direct generation.${NC}"
    echo -e "Run: ${CYAN}/implement ${prp_file} --output ${output_dir}${NC}"
}

# ============================================================================
# SPEC-PREPARE: Extract user journey content for spec generation
# Output: manifest.json with journey steps, personas, pain points
# Claude Code uses this to generate spec directly (no nested CLI)
# ============================================================================
cmd_spec_prepare() {
    local journey_file="$1"
    local output_dir="$2"
    local personas_dir="$3"
    local research_dir="$4"

    [[ ! -f "$journey_file" ]] && { echo -e "${RED}Journey file not found: $journey_file${NC}"; exit 1; }

    # Resolve absolute path
    journey_file=$(cd "$(dirname "$journey_file")" && pwd)/$(basename "$journey_file")

    local journey_name
    journey_name=$(basename "$journey_file" .md)

    # Default output directory
    if [[ -z "$output_dir" ]]; then
        output_dir="${journey_file%/*}/../specs/.spec-from-${journey_name}"
    fi

    mkdir -p "$output_dir"

    local journey_content
    journey_content=$(cat "$journey_file")

    # =========================================================================
    # Extract Journey Structure
    # =========================================================================

    # Extract title (first H1)
    local journey_title
    journey_title=$(echo "$journey_content" | grep -m1 "^# " | sed 's/^# //')

    # Extract persona references
    local personas_found=()
    while IFS= read -r line; do
        [[ -n "$line" ]] && personas_found+=("$line")
    done < <(echo "$journey_content" | grep -ioE "persona:[[:space:]]*[^,\n]+" | sed 's/persona:[[:space:]]*//' | sort -u)

    # Extract steps (numbered items or H2/H3 sections)
    local steps_count=0
    steps_count=$(echo "$journey_content" | grep -cE "^[0-9]+\.|^##|^###" || echo "0")

    # Extract pain points (look for "pain", "friction", "problem", "issue", "frustrat")
    local pain_points=()
    while IFS= read -r line; do
        [[ -n "$line" ]] && pain_points+=("$line")
    done < <(echo "$journey_content" | grep -iE "pain|friction|problem|issue|frustrat" | head -10)

    # Extract goals/outcomes (look for "goal", "outcome", "success", "want", "need")
    local goals=()
    while IFS= read -r line; do
        [[ -n "$line" ]] && goals+=("$line")
    done < <(echo "$journey_content" | grep -iE "goal|outcome|success|want to|need to|should be able" | head -10)

    # Extract touchpoints/systems mentioned
    local systems=()
    while IFS= read -r line; do
        [[ -n "$line" ]] && systems+=("$line")
    done < <(echo "$journey_content" | grep -ioE "system|api|database|ui|interface|service|endpoint|component" | sort -u | head -10)

    # =========================================================================
    # Find Related Files
    # =========================================================================
    local journey_dir
    journey_dir=$(dirname "$journey_file")
    local design_dir="${journey_dir}/.."

    # Find persona files
    local persona_files=()
    if [[ -n "$personas_dir" && -d "$personas_dir" ]]; then
        while IFS= read -r f; do
            [[ -n "$f" ]] && persona_files+=("$f")
        done < <(find "$personas_dir" -name "*.md" -type f 2>/dev/null)
    elif [[ -d "${design_dir}/personas" ]]; then
        while IFS= read -r f; do
            [[ -n "$f" ]] && persona_files+=("$f")
        done < <(find "${design_dir}/personas" -name "*.md" -type f 2>/dev/null)
    fi

    # Find research files
    local research_files=()
    if [[ -n "$research_dir" && -d "$research_dir" ]]; then
        while IFS= read -r f; do
            [[ -n "$f" ]] && research_files+=("$f")
        done < <(find "$research_dir" -name "*.md" -type f 2>/dev/null)
    elif [[ -d "${design_dir}/research" ]]; then
        while IFS= read -r f; do
            [[ -n "$f" ]] && research_files+=("$f")
        done < <(find "${design_dir}/research" -name "*.md" -type f 2>/dev/null)
    fi

    # Find other journey files (for context)
    local other_journeys=()
    while IFS= read -r f; do
        [[ -n "$f" && "$f" != "$journey_file" ]] && other_journeys+=("$f")
    done < <(find "$journey_dir" -name "*.md" -type f 2>/dev/null)

    # =========================================================================
    # Determine Spec Output Path
    # =========================================================================
    local spec_output_file
    local specs_dir="${design_dir}/specs"
    mkdir -p "$specs_dir"

    # Convert journey name to spec name
    local spec_name
    spec_name=$(echo "$journey_name" | sed 's/-journey$//' | sed 's/_journey$//' | sed 's/journey-//' | sed 's/journey_//')
    spec_output_file="${specs_dir}/${spec_name}-spec.md"

    # =========================================================================
    # Generate Manifest
    # =========================================================================
    local journey_hash
    journey_hash=$(git hash-object "$journey_file" 2>/dev/null | head -c 7 || md5 -q "$journey_file" 2>/dev/null | head -c 7 || echo "unknown")

    local manifest_file="$output_dir/.manifest.json"

    # Build personas JSON array
    local personas_json="["
    local first=true
    for p in "${personas_found[@]}"; do
        if [[ "$first" == "true" ]]; then
            personas_json+="\"$p\""
            first=false
        else
            personas_json+=",\"$p\""
        fi
    done
    personas_json+="]"

    # Build persona files JSON array
    local persona_files_json="["
    first=true
    for f in "${persona_files[@]}"; do
        if [[ "$first" == "true" ]]; then
            persona_files_json+="\"$f\""
            first=false
        else
            persona_files_json+=",\"$f\""
        fi
    done
    persona_files_json+="]"

    # Build research files JSON array
    local research_files_json="["
    first=true
    for f in "${research_files[@]}"; do
        if [[ "$first" == "true" ]]; then
            research_files_json+="\"$f\""
            first=false
        else
            research_files_json+=",\"$f\""
        fi
    done
    research_files_json+="]"

    # Build pain points JSON array
    local pain_points_json="["
    first=true
    for p in "${pain_points[@]}"; do
        # Escape quotes and newlines
        local escaped
        escaped=$(echo "$p" | sed 's/"/\\"/g' | tr '\n' ' ')
        if [[ "$first" == "true" ]]; then
            pain_points_json+="\"$escaped\""
            first=false
        else
            pain_points_json+=",\"$escaped\""
        fi
    done
    pain_points_json+="]"

    # Build goals JSON array
    local goals_json="["
    first=true
    for g in "${goals[@]}"; do
        local escaped
        escaped=$(echo "$g" | sed 's/"/\\"/g' | tr '\n' ' ')
        if [[ "$first" == "true" ]]; then
            goals_json+="\"$escaped\""
            first=false
        else
            goals_json+=",\"$escaped\""
        fi
    done
    goals_json+="]"

    cat > "$manifest_file" << EOF
{
  "journey_file": "$journey_file",
  "journey_hash": "$journey_hash",
  "journey_title": "$journey_title",
  "output_dir": "$output_dir",
  "spec_output_file": "$spec_output_file",
  "created_date": "$(date +%Y-%m-%d)",
  "extracted": {
    "steps_count": $steps_count,
    "personas_referenced": $personas_json,
    "pain_points": $pain_points_json,
    "goals": $goals_json,
    "systems_mentioned": ${#systems[@]}
  },
  "related_files": {
    "persona_files": $persona_files_json,
    "research_files": $research_files_json,
    "other_journeys": ${#other_journeys[@]}
  },
  "spec_template": {
    "sections": [
      "Problem Statement (from pain points)",
      "Scope (bounded by journey steps)",
      "Functional Requirements (one per major journey step)",
      "Non-Functional Requirements (performance, security)",
      "Success Criteria (measurable, from goals)",
      "Failure Modes (edge cases, errors)",
      "Dependencies",
      "Test Verification"
    ],
    "naming_convention": "FR-XX for functional requirements",
    "success_criteria_format": "| ID | Criterion | Metric | Target |"
  },
  "generation_prompt": {
    "context": "journey_to_spec",
    "instructions": [
      "Generate a complete specification from the user journey",
      "Each major journey step becomes a functional requirement",
      "Pain points inform the problem statement",
      "Goals become measurable success criteria",
      "Include failure modes for each requirement",
      "Add non-functional requirements (latency, accessibility)",
      "Include test verification section with specific commands"
    ],
    "output_format": "markdown spec following design-ops template"
  }
}
EOF

    # Copy journey content for Claude Code to analyze
    cp "$journey_file" "$output_dir/journey-content.md"

    # Copy persona files if found
    if [[ ${#persona_files[@]} -gt 0 ]]; then
        mkdir -p "$output_dir/personas"
        for f in "${persona_files[@]}"; do
            cp "$f" "$output_dir/personas/" 2>/dev/null
        done
    fi

    # Copy research files if found
    if [[ ${#research_files[@]} -gt 0 ]]; then
        mkdir -p "$output_dir/research"
        for f in "${research_files[@]}"; do
            cp "$f" "$output_dir/research/" 2>/dev/null
        done
    fi

    # =========================================================================
    # Output Summary
    # =========================================================================
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  SPEC-PREPARE COMPLETE                                        ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "Journey:    ${CYAN}$journey_file${NC}"
    echo -e "Title:      ${CYAN}$journey_title${NC}"
    echo -e "Output:     ${CYAN}$output_dir${NC}"
    echo -e "Spec file:  ${CYAN}$spec_output_file${NC}"
    echo ""
    echo -e "${BLUE}Extracted from Journey:${NC}"
    echo -e "  Steps:        ${CYAN}$steps_count${NC}"
    echo -e "  Personas:     ${CYAN}${#personas_found[@]}${NC}"
    echo -e "  Pain points:  ${CYAN}${#pain_points[@]}${NC}"
    echo -e "  Goals:        ${CYAN}${#goals[@]}${NC}"
    echo ""
    echo -e "${BLUE}Related Files Found:${NC}"
    echo -e "  Persona files:  ${CYAN}${#persona_files[@]}${NC}"
    echo -e "  Research files: ${CYAN}${#research_files[@]}${NC}"
    echo -e "  Other journeys: ${CYAN}${#other_journeys[@]}${NC}"
    echo ""
    echo -e "${YELLOW}Ready for Claude Code spec generation.${NC}"
    echo -e "Run: ${CYAN}/spec ${journey_file}${NC}"
}

# ============================================================================
# GENERATE-PREPARE: Extract spec content for PRP generation
# ============================================================================

cmd_generate_prepare() {
    local spec_file="$1"
    local output_dir="$2"

    [[ ! -f "$spec_file" ]] && { echo -e "${RED}Spec file not found: $spec_file${NC}"; exit 1; }

    local spec_content
    spec_content=$(cat "$spec_file")

    local spec_name
    spec_name=$(basename "$spec_file" .md)

    # Default output directory
    if [[ -z "$output_dir" ]]; then
        output_dir="${spec_file%/*}/../PRPs/.generate-${spec_name}"
    fi

    mkdir -p "$output_dir"

    # Calculate spec hash
    local spec_hash
    if command -v md5sum &> /dev/null; then
        spec_hash=$(md5sum "$spec_file" | cut -c1-7)
    else
        spec_hash=$(md5 -q "$spec_file" | cut -c1-7)
    fi

    # Generate PRP ID
    local today prp_id
    today=$(date +%Y-%m-%d)
    local prp_dir="${spec_file%/*}/../PRPs"
    local seq_num=1
    if [[ -d "$prp_dir" ]]; then
        local existing_max
        existing_max=$(grep -rh "prp_id: PRP-$today-" "$prp_dir"/*.md 2>/dev/null | \
            grep -oE "PRP-$today-[0-9]+" | \
            sed "s/PRP-$today-//" | \
            sort -n | tail -1)
        if [[ -n "$existing_max" ]]; then
            seq_num=$((existing_max + 1))
        fi
    fi
    prp_id=$(printf "PRP-%s-%03d" "$today" "$seq_num")

    # =========================================================================
    # Extract title
    # =========================================================================
    local title
    title=$(echo "$spec_content" | grep -E "^# " | head -1 | sed 's/^# //')

    # =========================================================================
    # Extract Problem Statement
    # =========================================================================
    local problem_statement=""
    local in_problem=0
    while IFS= read -r line; do
        if [[ "$line" =~ ^##\ Problem\ Statement ]]; then
            in_problem=1
            continue
        fi
        if [[ $in_problem -eq 1 && "$line" =~ ^##\  ]]; then
            in_problem=0
        fi
        if [[ $in_problem -eq 1 && -n "$line" && ! "$line" =~ ^--- ]]; then
            problem_statement="${problem_statement}${line}\n"
        fi
    done <<< "$spec_content"

    # =========================================================================
    # Extract Scope (In/Out)
    # =========================================================================
    local scope_in=()
    local scope_out=()
    local in_scope_section=0
    local scope_type=""

    while IFS= read -r line; do
        if [[ "$line" =~ ^##\ Scope ]]; then
            in_scope_section=1
            continue
        fi
        if [[ $in_scope_section -eq 1 && "$line" =~ ^##\  ]]; then
            in_scope_section=0
        fi
        if [[ $in_scope_section -eq 1 ]]; then
            if [[ "$line" =~ ^\*\*In\ Scope ]]; then
                scope_type="in"
                continue
            fi
            if [[ "$line" =~ ^\*\*Out\ of\ Scope ]] || [[ "$line" =~ ^\*\*Out\ Scope ]]; then
                scope_type="out"
                continue
            fi
            if [[ "$line" =~ ^-\  ]]; then
                local item="${line#- }"
                if [[ "$scope_type" == "in" ]]; then
                    scope_in+=("$item")
                elif [[ "$scope_type" == "out" ]]; then
                    scope_out+=("$item")
                fi
            fi
        fi
    done <<< "$spec_content"

    # =========================================================================
    # Extract Functional Requirements (FR-XXX sections)
    # =========================================================================
    local requirements=()
    local current_fr_id=""
    local current_fr_title=""
    local current_fr_content=""
    local in_fr=0

    while IFS= read -r line; do
        if [[ "$line" =~ ^###\ (FR-[A-Z0-9]+):\ (.+) ]]; then
            # Save previous FR if exists
            if [[ -n "$current_fr_id" ]]; then
                requirements+=("$current_fr_id|$current_fr_title|$current_fr_content")
            fi
            current_fr_id="${BASH_REMATCH[1]}"
            current_fr_title="${BASH_REMATCH[2]}"
            current_fr_content=""
            in_fr=1
            continue
        fi
        if [[ $in_fr -eq 1 && "$line" =~ ^###\  ]]; then
            # Save and reset
            if [[ -n "$current_fr_id" ]]; then
                requirements+=("$current_fr_id|$current_fr_title|$current_fr_content")
            fi
            current_fr_id=""
            current_fr_title=""
            current_fr_content=""
            in_fr=0
        fi
        if [[ $in_fr -eq 1 ]]; then
            current_fr_content="${current_fr_content}${line}\n"
        fi
    done <<< "$spec_content"
    # Don't forget last FR
    if [[ -n "$current_fr_id" ]]; then
        requirements+=("$current_fr_id|$current_fr_title|$current_fr_content")
    fi

    # =========================================================================
    # Extract Code Blocks (verbatim)
    # =========================================================================
    local code_blocks=()
    local in_code_block=0
    local current_code=""
    local code_lang=""

    while IFS= read -r line; do
        if [[ "$line" =~ ^\`\`\`([a-z]*) && $in_code_block -eq 0 ]]; then
            in_code_block=1
            code_lang="${BASH_REMATCH[1]}"
            current_code=""
            continue
        fi
        if [[ "$line" =~ ^\`\`\` && $in_code_block -eq 1 ]]; then
            in_code_block=0
            [[ -n "$current_code" ]] && code_blocks+=("$code_lang|$current_code")
            continue
        fi
        if [[ $in_code_block -eq 1 ]]; then
            current_code="${current_code}${line}\n"
        fi
    done <<< "$spec_content"

    # =========================================================================
    # Extract Tables (verbatim)
    # =========================================================================
    local tables=()
    local in_table=0
    local current_table=""

    while IFS= read -r line; do
        if [[ "$line" =~ ^\| && $in_table -eq 0 ]]; then
            in_table=1
            current_table="$line"
            continue
        fi
        if [[ $in_table -eq 1 ]]; then
            if [[ "$line" =~ ^\| ]]; then
                current_table="${current_table}\n${line}"
            else
                tables+=("$current_table")
                current_table=""
                in_table=0
            fi
        fi
    done <<< "$spec_content"
    # Don't forget last table
    [[ -n "$current_table" ]] && tables+=("$current_table")

    # =========================================================================
    # Extract Validation Commands section
    # =========================================================================
    local validation_commands=()
    local in_validation=0
    local in_val_code=0

    while IFS= read -r line; do
        if [[ "$line" =~ ^##\ Validation ]] || [[ "$line" =~ ^##.*Validation\ Commands ]]; then
            in_validation=1
            continue
        fi
        if [[ $in_validation -eq 1 && "$line" =~ ^##\  && ! "$line" =~ Validation ]]; then
            in_validation=0
        fi
        if [[ $in_validation -eq 1 ]]; then
            if [[ "$line" =~ ^\`\`\`bash ]]; then
                in_val_code=1
                continue
            fi
            if [[ "$line" =~ ^\`\`\` && $in_val_code -eq 1 ]]; then
                in_val_code=0
                continue
            fi
            if [[ $in_val_code -eq 1 && -n "$line" && ! "$line" =~ ^#.*Expected ]]; then
                validation_commands+=("$line")
            fi
        fi
    done <<< "$spec_content"

    # =========================================================================
    # Extract Success Criteria
    # =========================================================================
    local success_criteria=()
    local in_success=0
    local sc_row=0

    while IFS= read -r line; do
        if [[ "$line" =~ ^##\ Success\ Criteria ]] || [[ "$line" =~ ^##.*Success ]]; then
            in_success=1
            continue
        fi
        if [[ $in_success -eq 1 && "$line" =~ ^##\  ]]; then
            in_success=0
        fi
        # Skip header rows
        [[ "$line" =~ ^\|-+\| ]] && continue
        [[ "$line" =~ ^\|.*Metric.*Target ]] && continue
        [[ "$line" =~ ^\|.*ID.*Criterion ]] && continue

        if [[ $in_success -eq 1 && "$line" =~ ^\|[^-] ]]; then
            sc_row=$((sc_row + 1))
            local row
            row=$(echo "$line" | sed 's/^|//;s/|$//' | sed 's/|/\t/g')
            local col1 col2 col3
            col1=$(echo "$row" | cut -f1 | xargs)
            col2=$(echo "$row" | cut -f2 | xargs)
            col3=$(echo "$row" | cut -f3 | xargs)
            [[ -n "$col1" ]] && success_criteria+=("SC-G.${sc_row}|$col1: $col2|$col3")
        fi
    done <<< "$spec_content"

    # =========================================================================
    # Calculate confidence and thinking level (reuse existing functions)
    # =========================================================================
    local domain_info
    domain_info=$(resolve_domain_invariants "$spec_content")

    local invariant_refs total_invariants domain_count has_skill_gap domain_name
    invariant_refs=$(echo "$domain_info" | sed -n '/INVARIANT_REFS<<EOF/,/EOF/p' | sed '1d;$d')
    total_invariants=$(echo "$domain_info" | grep "TOTAL_INVARIANTS=" | cut -d= -f2)
    domain_count=$(echo "$domain_info" | grep "DOMAIN_COUNT=" | cut -d= -f2)
    has_skill_gap=$(echo "$domain_info" | grep "HAS_SKILL_GAP=" | cut -d= -f2)
    domain_name=$(echo "$domain_info" | grep "DOMAIN_NAME=" | cut -d= -f2)

    local confidence_info
    confidence_info=$(analyze_spec_confidence "$spec_content")

    local confidence_score clarity_score pattern_score test_score edge_score tech_score
    confidence_score=$(echo "$confidence_info" | grep "CONFIDENCE_SCORE=" | cut -d= -f2)
    clarity_score=$(echo "$confidence_info" | grep "CLARITY_SCORE=" | cut -d= -f2)
    pattern_score=$(echo "$confidence_info" | grep "PATTERN_SCORE=" | cut -d= -f2)
    test_score=$(echo "$confidence_info" | grep "TEST_SCORE=" | cut -d= -f2)
    edge_score=$(echo "$confidence_info" | grep "EDGE_SCORE=" | cut -d= -f2)
    tech_score=$(echo "$confidence_info" | grep "TECH_SCORE=" | cut -d= -f2)

    local thinking_info
    thinking_info=$(determine_thinking_level "$confidence_score" "$domain_count" "$total_invariants" "$has_skill_gap")

    local thinking_level thinking_focus
    thinking_level=$(echo "$thinking_info" | grep "THINKING_LEVEL=" | cut -d= -f2)
    thinking_focus=$(echo "$thinking_info" | grep "THINKING_FOCUS=" | cut -d= -f2)

    # Determine risk level
    local risk_level
    if (( $(echo "$confidence_score < 5" | bc -l) )); then
        risk_level="Low/Red"
    elif (( $(echo "$confidence_score < 7" | bc -l) )); then
        risk_level="Medium/Yellow"
    else
        risk_level="High/Green"
    fi

    # =========================================================================
    # Check for related files (journeys, personas, research)
    # =========================================================================
    local spec_dir="${spec_file%/*}"
    local design_dir="${spec_dir}/.."
    local journeys=()
    local personas=()
    local research=()

    if [[ -d "$design_dir/journeys" ]]; then
        while IFS= read -r -d '' f; do
            journeys+=("$f")
        done < <(find "$design_dir/journeys" -name "*.md" -print0 2>/dev/null)
    fi
    if [[ -d "$design_dir/personas" ]]; then
        while IFS= read -r -d '' f; do
            personas+=("$f")
        done < <(find "$design_dir/personas" -name "*.md" -print0 2>/dev/null)
    fi
    if [[ -d "$design_dir/research" ]]; then
        while IFS= read -r -d '' f; do
            research+=("$f")
        done < <(find "$design_dir/research" -name "*.md" -print0 2>/dev/null)
    fi

    # =========================================================================
    # Generate manifest JSON
    # =========================================================================
    local manifest_file="$output_dir/.manifest.json"
    local output_prp_file="${spec_file%/*}/../PRPs/${spec_name}-prp.md"

    # Helper to escape JSON strings
    json_escape() {
        echo "$1" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | sed 's/\t/\\t/g' | tr '\n' ' ' | sed 's/\\n */\\n/g'
    }

    echo "{" > "$manifest_file"
    echo "  \"prp_id\": \"$prp_id\"," >> "$manifest_file"
    echo "  \"spec_file\": \"$(realpath "$spec_file")\"," >> "$manifest_file"
    echo "  \"spec_hash\": \"$spec_hash\"," >> "$manifest_file"
    echo "  \"output_file\": \"$(realpath "$output_prp_file" 2>/dev/null || echo "$output_prp_file")\"," >> "$manifest_file"
    echo "  \"template_file\": \"$TEMPLATES_DIR/prp-base.md\"," >> "$manifest_file"
    echo "  \"generated_date\": \"$(date +%Y-%m-%d)\"," >> "$manifest_file"

    # Extracted content
    echo "  \"extracted\": {" >> "$manifest_file"
    echo "    \"title\": \"$(json_escape "$title")\"," >> "$manifest_file"
    echo "    \"problem_statement\": \"$(json_escape "$problem_statement")\"," >> "$manifest_file"

    # Scope arrays
    echo "    \"scope_in\": [" >> "$manifest_file"
    for i in "${!scope_in[@]}"; do
        local comma=","
        [[ $i -eq $((${#scope_in[@]} - 1)) ]] && comma=""
        echo "      \"$(json_escape "${scope_in[$i]}")\"${comma}" >> "$manifest_file"
    done
    echo "    ]," >> "$manifest_file"

    echo "    \"scope_out\": [" >> "$manifest_file"
    for i in "${!scope_out[@]}"; do
        local comma=","
        [[ $i -eq $((${#scope_out[@]} - 1)) ]] && comma=""
        echo "      \"$(json_escape "${scope_out[$i]}")\"${comma}" >> "$manifest_file"
    done
    echo "    ]," >> "$manifest_file"

    # Requirements
    echo "    \"functional_requirements\": [" >> "$manifest_file"
    for i in "${!requirements[@]}"; do
        local comma=","
        [[ $i -eq $((${#requirements[@]} - 1)) ]] && comma=""
        IFS='|' read -r fr_id fr_title fr_content <<< "${requirements[$i]}"
        echo "      {" >> "$manifest_file"
        echo "        \"id\": \"$fr_id\"," >> "$manifest_file"
        echo "        \"title\": \"$(json_escape "$fr_title")\"," >> "$manifest_file"
        echo "        \"content\": \"$(json_escape "$fr_content")\"" >> "$manifest_file"
        echo "      }${comma}" >> "$manifest_file"
    done
    echo "    ]," >> "$manifest_file"

    # Success criteria
    echo "    \"success_criteria\": [" >> "$manifest_file"
    for i in "${!success_criteria[@]}"; do
        local comma=","
        [[ $i -eq $((${#success_criteria[@]} - 1)) ]] && comma=""
        IFS='|' read -r sc_id sc_crit sc_metric <<< "${success_criteria[$i]}"
        echo "      { \"id\": \"$sc_id\", \"criterion\": \"$(json_escape "$sc_crit")\", \"metric\": \"$(json_escape "$sc_metric")\" }${comma}" >> "$manifest_file"
    done
    echo "    ]," >> "$manifest_file"

    # Validation commands
    echo "    \"validation_commands\": [" >> "$manifest_file"
    for i in "${!validation_commands[@]}"; do
        local comma=","
        [[ $i -eq $((${#validation_commands[@]} - 1)) ]] && comma=""
        echo "      \"$(json_escape "${validation_commands[$i]}")\"${comma}" >> "$manifest_file"
    done
    echo "    ]," >> "$manifest_file"

    # Code blocks count and tables count (content saved to files)
    echo "    \"code_blocks_count\": ${#code_blocks[@]}," >> "$manifest_file"
    echo "    \"tables_count\": ${#tables[@]}" >> "$manifest_file"
    echo "  }," >> "$manifest_file"

    # Calculated values
    echo "  \"calculated\": {" >> "$manifest_file"
    echo "    \"confidence_score\": $confidence_score," >> "$manifest_file"
    echo "    \"confidence_breakdown\": {" >> "$manifest_file"
    echo "      \"clarity\": $clarity_score," >> "$manifest_file"
    echo "      \"patterns\": $pattern_score," >> "$manifest_file"
    echo "      \"tests\": $test_score," >> "$manifest_file"
    echo "      \"edges\": $edge_score," >> "$manifest_file"
    echo "      \"tech\": $tech_score" >> "$manifest_file"
    echo "    }," >> "$manifest_file"
    echo "    \"risk_level\": \"$risk_level\"," >> "$manifest_file"
    echo "    \"thinking_level\": \"$thinking_level\"," >> "$manifest_file"
    echo "    \"thinking_focus\": \"$(echo "$thinking_focus" | tr '|' ', ')\"," >> "$manifest_file"
    echo "    \"domain\": \"${domain_name:-universal}\"," >> "$manifest_file"
    echo "    \"domain_count\": $domain_count," >> "$manifest_file"
    echo "    \"invariant_count\": $total_invariants" >> "$manifest_file"
    echo "  }," >> "$manifest_file"

    # Related files
    echo "  \"related_files\": {" >> "$manifest_file"
    echo "    \"journeys\": [" >> "$manifest_file"
    for i in "${!journeys[@]}"; do
        local comma=","
        [[ $i -eq $((${#journeys[@]} - 1)) ]] && comma=""
        echo "      \"${journeys[$i]}\"${comma}" >> "$manifest_file"
    done
    echo "    ]," >> "$manifest_file"
    echo "    \"personas\": [" >> "$manifest_file"
    for i in "${!personas[@]}"; do
        local comma=","
        [[ $i -eq $((${#personas[@]} - 1)) ]] && comma=""
        echo "      \"${personas[$i]}\"${comma}" >> "$manifest_file"
    done
    echo "    ]," >> "$manifest_file"
    echo "    \"research\": [" >> "$manifest_file"
    for i in "${!research[@]}"; do
        local comma=","
        [[ $i -eq $((${#research[@]} - 1)) ]] && comma=""
        echo "      \"${research[$i]}\"${comma}" >> "$manifest_file"
    done
    echo "    ]" >> "$manifest_file"
    echo "  }" >> "$manifest_file"

    echo "}" >> "$manifest_file"

    # Save code blocks to separate files (for verbatim preservation)
    local blocks_dir="$output_dir/code_blocks"
    mkdir -p "$blocks_dir"
    for i in "${!code_blocks[@]}"; do
        IFS='|' read -r lang content <<< "${code_blocks[$i]}"
        echo -e "$content" > "$blocks_dir/block-$((i+1)).$lang"
    done

    # Save tables to separate file
    echo "" > "$output_dir/tables.md"
    for i in "${!tables[@]}"; do
        echo -e "### Table $((i+1))\n" >> "$output_dir/tables.md"
        echo -e "${tables[$i]}\n" >> "$output_dir/tables.md"
    done

    # Output summary
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  GENERATE-PREPARE COMPLETE                                    ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "Spec:       ${CYAN}${spec_file}${NC}"
    echo -e "Output:     ${CYAN}${output_dir}${NC}"
    echo -e "Manifest:   ${CYAN}${output_dir}/.manifest.json${NC}"
    echo ""
    echo -e "${BLUE}Extracted:${NC}"
    echo -e "  Title:        ${CYAN}${title}${NC}"
    echo -e "  Problem:      ${CYAN}$(echo -e "$problem_statement" | head -1 | cut -c1-50)...${NC}"
    echo -e "  Scope In:     ${CYAN}${#scope_in[@]} items${NC}"
    echo -e "  Scope Out:    ${CYAN}${#scope_out[@]} items${NC}"
    echo -e "  Requirements: ${CYAN}${#requirements[@]} FRs${NC}"
    echo -e "  Criteria:     ${CYAN}${#success_criteria[@]} success criteria${NC}"
    echo -e "  Commands:     ${CYAN}${#validation_commands[@]} validation commands${NC}"
    echo -e "  Code blocks:  ${CYAN}${#code_blocks[@]} (saved to code_blocks/)${NC}"
    echo -e "  Tables:       ${CYAN}${#tables[@]} (saved to tables.md)${NC}"
    echo ""
    echo -e "${BLUE}Calculated:${NC}"
    echo -e "  PRP ID:       ${CYAN}${prp_id}${NC}"
    echo -e "  Confidence:   ${CYAN}${confidence_score}/10 (${risk_level})${NC}"
    echo -e "  Thinking:     ${CYAN}${thinking_level}${NC}"
    echo -e "  Domain:       ${CYAN}${domain_name:-universal} (${domain_count} domains, ${total_invariants} invariants)${NC}"
    echo ""
    if [[ ${#journeys[@]} -gt 0 ]] || [[ ${#personas[@]} -gt 0 ]] || [[ ${#research[@]} -gt 0 ]]; then
        echo -e "${BLUE}Related files found:${NC}"
        [[ ${#journeys[@]} -gt 0 ]] && echo -e "  Journeys:     ${CYAN}${#journeys[@]}${NC}"
        [[ ${#personas[@]} -gt 0 ]] && echo -e "  Personas:     ${CYAN}${#personas[@]}${NC}"
        [[ ${#research[@]} -gt 0 ]] && echo -e "  Research:     ${CYAN}${#research[@]}${NC}"
        echo ""
    fi
    echo -e "${YELLOW}Ready for Claude Code PRP generation.${NC}"
    echo -e "Run: ${CYAN}/generate ${spec_file}${NC}"
}

# ============================================================================
# VALIDATE-PREPARE: Extract spec content and run deterministic checks
# Output: manifest.json with spec sections, deterministic results, domain info
# Claude Code uses this to do LLM analysis directly (no nested CLI)
# ============================================================================
cmd_validate_prepare() {
    local spec_file="$1"
    local output_dir="$2"

    [[ ! -f "$spec_file" ]] && { echo -e "${RED}File not found: $spec_file${NC}"; exit 1; }

    # Resolve absolute path
    spec_file=$(cd "$(dirname "$spec_file")" && pwd)/$(basename "$spec_file")

    local spec_name
    spec_name=$(basename "$spec_file" .md)

    # Default output directory
    if [[ -z "$output_dir" ]]; then
        output_dir="${spec_file%/*}/.validate-${spec_name}"
    fi

    mkdir -p "$output_dir"

    local spec_content
    spec_content=$(cat "$spec_file")

    # =========================================================================
    # Run deterministic checks (same as check_spec_structure)
    # =========================================================================
    local issues=()
    local warnings=()

    # Required sections
    if ! echo "$spec_content" | grep -qiE "^#.*problem|^##.*problem|problem.*statement"; then
        issues+=("Missing: Problem statement")
    fi

    if ! echo "$spec_content" | grep -qiE "success.*criter|acceptance.*criter|done.*when|definition.*done"; then
        issues+=("Missing: Success criteria")
    fi

    if ! echo "$spec_content" | grep -qiE "scope|boundar|in.scope|out.of.scope|non-goal"; then
        warnings+=("Consider adding: Scope boundaries")
    fi

    if ! echo "$spec_content" | grep -qiE "test|verif|validat"; then
        warnings+=("Consider adding: Test/validation approach")
    fi

    # Check for vague words
    local vague_count
    vague_count=$(echo "$spec_content" | grep -ciE "properly|efficiently|adequate|reasonable|good quality|as needed" 2>/dev/null) || vague_count=0
    if [[ $vague_count -gt 3 ]]; then
        warnings+=("Found $vague_count vague terms (properly, efficiently, etc.)")
    fi

    # Check minimum content
    local word_count
    word_count=$(wc -w < "$spec_file" | tr -d ' ')
    if [[ $word_count -lt 100 ]]; then
        issues+=("Too short: $word_count words (minimum ~100)")
    fi

    # Determine grade
    local deterministic_grade="PASS"
    if [[ ${#issues[@]} -gt 0 ]]; then
        deterministic_grade="FAIL"
    elif [[ ${#warnings[@]} -gt 2 ]]; then
        deterministic_grade="NEEDS_WORK"
    fi

    # =========================================================================
    # Detect domains and invariants
    # =========================================================================
    local domain_info
    domain_info=$(resolve_domain_invariants "$spec_content")

    local invariant_refs total_invariants domain_count domain_name
    invariant_refs=$(echo "$domain_info" | sed -n '/INVARIANT_REFS<<EOF/,/EOF/p' | sed '1d;$d')
    total_invariants=$(echo "$domain_info" | grep "TOTAL_INVARIANTS=" | cut -d= -f2)
    domain_count=$(echo "$domain_info" | grep "DOMAIN_COUNT=" | cut -d= -f2)
    domain_name=$(echo "$domain_info" | grep "DOMAIN_NAME=" | cut -d= -f2)

    # =========================================================================
    # Extract key sections for LLM analysis
    # =========================================================================
    # Extract problem statement
    local problem_statement=""
    local in_problem=0
    while IFS= read -r line; do
        if [[ "$line" =~ ^##.*[Pp]roblem ]] || [[ "$line" =~ ^#.*[Pp]roblem ]]; then
            in_problem=1
            continue
        fi
        if [[ $in_problem -eq 1 && "$line" =~ ^## ]]; then
            break
        fi
        [[ $in_problem -eq 1 ]] && problem_statement+="$line"$'\n'
    done <<< "$spec_content"

    # Extract all tables (for context)
    local tables=""
    local in_table=0
    while IFS= read -r line; do
        if [[ "$line" =~ ^\|.*\| ]]; then
            in_table=1
            tables+="$line"$'\n'
        elif [[ $in_table -eq 1 && ! "$line" =~ ^\|.*\| ]]; then
            in_table=0
            tables+=$'\n'
        fi
    done <<< "$spec_content"

    # Extract code blocks (for context)
    local code_blocks=""
    local in_code=0
    while IFS= read -r line; do
        if [[ "$line" =~ ^\`\`\` ]]; then
            if [[ $in_code -eq 0 ]]; then
                in_code=1
            else
                in_code=0
                code_blocks+="$line"$'\n\n'
            fi
        fi
        [[ $in_code -eq 1 ]] && code_blocks+="$line"$'\n'
    done <<< "$spec_content"

    # Find vague terms with line numbers
    local vague_terms=()
    local line_num=0
    while IFS= read -r line; do
        line_num=$((line_num + 1))
        if echo "$line" | grep -qiE "properly|efficiently|adequate|reasonable|good quality|as needed|intuitive|user-friendly|as appropriate"; then
            local match
            match=$(echo "$line" | grep -oiE "(properly|efficiently|adequate|reasonable|good quality|as needed|intuitive|user-friendly|as appropriate)[^.]*" | head -1)
            [[ -n "$match" ]] && vague_terms+=("Line $line_num: \"...$match...\"")
        fi
    done <<< "$spec_content"

    # =========================================================================
    # Generate manifest JSON
    # =========================================================================
    local manifest_file="$output_dir/.manifest.json"
    local spec_hash
    spec_hash=$(echo "$spec_content" | shasum | cut -c1-7)

    # Helper to escape JSON strings
    json_escape() {
        local s="$1"
        s="${s//\\/\\\\}"
        s="${s//\"/\\\"}"
        s="${s//$'\n'/\\n}"
        s="${s//$'\t'/\\t}"
        s="${s//$'\r'/}"
        echo "$s"
    }

    # Build issues array
    local issues_json="["
    local first=1
    for issue in "${issues[@]}"; do
        [[ $first -eq 0 ]] && issues_json+=","
        issues_json+="\"$(json_escape "$issue")\""
        first=0
    done
    issues_json+="]"

    # Build warnings array
    local warnings_json="["
    first=1
    for warning in "${warnings[@]}"; do
        [[ $first -eq 0 ]] && warnings_json+=","
        warnings_json+="\"$(json_escape "$warning")\""
        first=0
    done
    warnings_json+="]"

    # Build vague_terms array
    local vague_json="["
    first=1
    for term in "${vague_terms[@]}"; do
        [[ $first -eq 0 ]] && vague_json+=","
        vague_json+="\"$(json_escape "$term")\""
        first=0
    done
    vague_json+="]"

    # Write manifest
    cat > "$manifest_file" << EOF
{
  "spec_file": "$spec_file",
  "spec_hash": "$spec_hash",
  "output_dir": "$output_dir",
  "validated_date": "$(date +%Y-%m-%d)",
  "deterministic_checks": {
    "grade": "$deterministic_grade",
    "issues": $issues_json,
    "warnings": $warnings_json,
    "word_count": $word_count,
    "vague_term_count": $vague_count,
    "vague_terms": $vague_json
  },
  "domain_info": {
    "domain_name": "${domain_name:-universal}",
    "domain_count": ${domain_count:-0},
    "total_invariants": ${total_invariants:-11}
  },
  "llm_analysis_prompt": {
    "context": "spec_validation",
    "invariant_focus": "Invariant #1 (Ambiguity): Every term must have operational definition",
    "check_for": [
      "Vague terms without measurable definitions",
      "Implicit assumptions not stated explicitly",
      "Ambiguous state transitions",
      "Success criteria that cannot be objectively measured",
      "Missing edge case definitions"
    ],
    "output_schema": {
      "summary": "One sentence on clarity level",
      "ambiguity_flags": "Specific vague terms found (quote text, max 5)",
      "implicit_assumptions": "Things spec assumes but does not state (max 3)",
      "suggestions": "How to make unclear sections more specific (max 5)",
      "strengths": "What is already clear and well-defined (max 2)"
    }
  }
}
EOF

    # Also save the full spec content for Claude Code to analyze
    cp "$spec_file" "$output_dir/spec-content.md"

    # =========================================================================
    # Output summary
    # =========================================================================
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  VALIDATE-PREPARE COMPLETE                                    ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "Spec:       ${CYAN}$spec_file${NC}"
    echo -e "Output:     ${CYAN}$output_dir${NC}"
    echo -e "Manifest:   ${CYAN}$manifest_file${NC}"
    echo ""
    echo -e "${BLUE}Deterministic Checks:${NC}"
    echo -e "  Grade:      ${CYAN}$deterministic_grade${NC}"
    echo -e "  Issues:     ${CYAN}${#issues[@]}${NC}"
    echo -e "  Warnings:   ${CYAN}${#warnings[@]}${NC}"
    echo -e "  Word count: ${CYAN}$word_count${NC}"
    echo -e "  Vague terms: ${CYAN}$vague_count${NC}"
    echo ""
    echo -e "${BLUE}Domain Info:${NC}"
    echo -e "  Domain:     ${CYAN}${domain_name:-universal}${NC}"
    echo -e "  Invariants: ${CYAN}${total_invariants:-11}${NC}"
    echo ""
    echo -e "${YELLOW}Ready for Claude Code LLM analysis.${NC}"
    echo -e "Run: ${CYAN}/validate ${spec_file}${NC}"
}

# ============================================================================
# STRESS-TEST-PREPARE: Run coverage checks and extract data for LLM analysis
# Output: manifest.json with coverage results, domain info, invariant refs
# Claude Code uses this to do deep analysis directly (no nested CLI)
# ============================================================================
cmd_stress_test_prepare() {
    local spec_file="$1"
    local requirements_file="$2"
    local journeys_file="$3"
    local output_dir="$4"

    [[ ! -f "$spec_file" ]] && { echo -e "${RED}File not found: $spec_file${NC}"; exit 1; }

    # Resolve absolute path
    spec_file=$(cd "$(dirname "$spec_file")" && pwd)/$(basename "$spec_file")

    local spec_name
    spec_name=$(basename "$spec_file" .md)

    # Default output directory
    if [[ -z "$output_dir" ]]; then
        output_dir="${spec_file%/*}/.stress-test-${spec_name}"
    fi

    mkdir -p "$output_dir"

    local spec_content
    spec_content=$(cat "$spec_file")

    # =========================================================================
    # Domain Detection
    # =========================================================================
    local domain_result
    domain_result=$(resolve_domain_invariants "$spec_content")

    local invariant_refs total_invariants domain_count domain_name
    invariant_refs=$(echo "$domain_result" | sed -n '/^INVARIANT_REFS<<EOF$/,/^EOF$/p' | sed '1d;$d')
    total_invariants=$(echo "$domain_result" | grep "^TOTAL_INVARIANTS=" | cut -d= -f2)
    domain_count=$(echo "$domain_result" | grep "^DOMAIN_COUNT=" | cut -d= -f2)
    domain_name=$(echo "$domain_result" | grep "^DOMAIN_NAME=" | cut -d= -f2)

    # =========================================================================
    # Deterministic Coverage Checks
    # =========================================================================
    local coverage_checks=()
    local issues=()
    local warnings=()

    # Happy path
    if echo "$spec_content" | grep -qiE "happy path|success.*path|normal.*flow"; then
        coverage_checks+=('{"check": "happy_path", "passed": true, "label": "Happy path mentioned"}')
    else
        coverage_checks+=('{"check": "happy_path", "passed": false, "label": "Happy path not explicitly described"}')
        warnings+=("Happy path not explicitly described")
    fi

    # Error cases
    if echo "$spec_content" | grep -qiE "error|fail|exception|invalid|edge.case"; then
        coverage_checks+=('{"check": "error_cases", "passed": true, "label": "Error cases mentioned"}')
    else
        coverage_checks+=('{"check": "error_cases", "passed": false, "label": "Error/failure cases not addressed"}')
        issues+=("Error/failure cases not addressed")
    fi

    # Empty/null states
    if echo "$spec_content" | grep -qiE "empty|null|zero|no.*data|missing"; then
        coverage_checks+=('{"check": "empty_states", "passed": true, "label": "Empty/null states mentioned"}')
    else
        coverage_checks+=('{"check": "empty_states", "passed": false, "label": "Empty/null states not explicitly handled"}')
        warnings+=("Empty/null states not explicitly handled")
    fi

    # External failure modes
    if echo "$spec_content" | grep -qiE "timeout|offline|unavailable|network|api.*fail"; then
        coverage_checks+=('{"check": "failure_modes", "passed": true, "label": "Failure modes mentioned (timeout, offline, etc.)"}')
    else
        coverage_checks+=('{"check": "failure_modes", "passed": false, "label": "External failure modes not addressed"}')
        issues+=("External failure modes not addressed (API down, timeout, offline)")
    fi

    # Concurrency
    if echo "$spec_content" | grep -qiE "concurrent|race|simultaneous|parallel"; then
        coverage_checks+=('{"check": "concurrency", "passed": true, "label": "Concurrency considerations mentioned"}')
    else
        coverage_checks+=('{"check": "concurrency", "passed": false, "label": "Concurrency not explicitly addressed (may not apply)"}')
        warnings+=("Concurrency not explicitly addressed (may not apply)")
    fi

    # Limits/boundaries
    if echo "$spec_content" | grep -qiE "limit|max|min|bound|threshold|quota"; then
        coverage_checks+=('{"check": "limits", "passed": true, "label": "Limits/boundaries mentioned"}')
    else
        coverage_checks+=('{"check": "limits", "passed": false, "label": "Limits/boundaries not specified"}')
        warnings+=("Limits/boundaries not specified")
    fi

    # Calculate coverage
    local passed_count=0
    local total_count=${#coverage_checks[@]}
    for check in "${coverage_checks[@]}"; do
        if echo "$check" | grep -q '"passed": true'; then
            ((passed_count++))
        fi
    done
    local coverage_pct=$((passed_count * 100 / total_count))

    # Determine status
    local status
    if [[ ${#issues[@]} -ge 2 ]]; then
        status="REVIEW_REQUIRED"
    elif [[ ${#issues[@]} -ge 1 ]] || [[ ${#warnings[@]} -ge 3 ]]; then
        status="ITEMS_TO_REVIEW"
    else
        status="NO_OBVIOUS_GAPS"
    fi

    # =========================================================================
    # Handle additional files
    # =========================================================================
    local has_requirements="false"
    local has_journeys="false"

    if [[ -n "$requirements_file" ]] && [[ -f "$requirements_file" ]]; then
        cp "$requirements_file" "$output_dir/requirements.md"
        has_requirements="true"
    fi

    if [[ -n "$journeys_file" ]] && [[ -f "$journeys_file" ]]; then
        cp "$journeys_file" "$output_dir/journeys.md"
        has_journeys="true"
    fi

    # =========================================================================
    # Generate manifest
    # =========================================================================
    local spec_hash
    spec_hash=$(git hash-object "$spec_file" 2>/dev/null | head -c 7 || md5 -q "$spec_file" 2>/dev/null | head -c 7 || echo "unknown")

    local manifest_file="$output_dir/.manifest.json"

    # Build coverage checks JSON array
    local checks_json="["
    local first=true
    for check in "${coverage_checks[@]}"; do
        if [[ "$first" == "true" ]]; then
            checks_json+="$check"
            first=false
        else
            checks_json+=",$check"
        fi
    done
    checks_json+="]"

    # Build issues JSON array
    local issues_json="["
    first=true
    for issue in "${issues[@]}"; do
        if [[ "$first" == "true" ]]; then
            issues_json+="\"$issue\""
            first=false
        else
            issues_json+=",\"$issue\""
        fi
    done
    issues_json+="]"

    # Build warnings JSON array
    local warnings_json="["
    first=true
    for warning in "${warnings[@]}"; do
        if [[ "$first" == "true" ]]; then
            warnings_json+="\"$warning\""
            first=false
        else
            warnings_json+=",\"$warning\""
        fi
    done
    warnings_json+="]"

    # Escape invariant refs for JSON (newlines to \n) - macOS compatible
    local invariant_refs_escaped
    invariant_refs_escaped=$(echo "$invariant_refs" | tr '\n' ' ' | sed 's/  */ /g')

    cat > "$manifest_file" << EOF
{
  "spec_file": "$spec_file",
  "spec_hash": "$spec_hash",
  "output_dir": "$output_dir",
  "stress_test_date": "$(date +%Y-%m-%d)",
  "coverage_checks": {
    "checks": $checks_json,
    "passed": $passed_count,
    "total": $total_count,
    "percentage": $coverage_pct,
    "issues": $issues_json,
    "warnings": $warnings_json,
    "status": "$status"
  },
  "domain_info": {
    "domain_name": "${domain_name:-universal}",
    "domain_count": ${domain_count:-0},
    "total_invariants": ${total_invariants:-11},
    "invariant_refs": "$invariant_refs_escaped"
  },
  "additional_files": {
    "has_requirements": $has_requirements,
    "has_journeys": $has_journeys
  },
  "llm_analysis_prompt": {
    "context": "spec_stress_test",
    "focus": "Completeness and invariant coverage",
    "key_invariants": [
      "Invariant #1 (Ambiguity): Every term must have operational definition",
      "Invariant #4 (No Irreversible Without Recovery): Destructive actions need undo/confirmation",
      "Invariant #5 (Fail Loudly): Errors must be visible, not silent",
      "Invariant #7 (Validation Executable): Success criteria must be testable",
      "Invariant #10 (Degradation Path): What happens when dependencies fail?"
    ],
    "output_schema": {
      "summary": "One sentence on overall completeness",
      "invariant_violations": "Specific invariants violated (reference by number, max 5)",
      "missing_failure_modes": "Failure scenarios not addressed (max 5)",
      "missing_coverage": "User journey steps or requirements not covered (max 5)",
      "critical_blockers": "Questions that MUST be answered before proceeding (max 5)"
    }
  }
}
EOF

    # Save spec content for Claude Code to analyze
    cp "$spec_file" "$output_dir/spec-content.md"

    # =========================================================================
    # Output summary
    # =========================================================================
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  STRESS-TEST-PREPARE COMPLETE                                 ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "Spec:       ${CYAN}$spec_file${NC}"
    echo -e "Output:     ${CYAN}$output_dir${NC}"
    echo -e "Manifest:   ${CYAN}$manifest_file${NC}"
    echo ""
    echo -e "${BLUE}Coverage Checks:${NC}"
    echo -e "  Passed:   ${CYAN}$passed_count/$total_count ($coverage_pct%)${NC}"
    echo -e "  Issues:   ${CYAN}${#issues[@]}${NC}"
    echo -e "  Warnings: ${CYAN}${#warnings[@]}${NC}"
    echo -e "  Status:   ${CYAN}$status${NC}"
    echo ""
    echo -e "${BLUE}Domain Info:${NC}"
    echo -e "  Domain:     ${CYAN}${domain_name:-universal}${NC}"
    echo -e "  Invariants: ${CYAN}${total_invariants:-11}${NC}"
    echo ""
    [[ "$has_requirements" == "true" ]] && echo -e "  ${GREEN}+${NC} Requirements file included"
    [[ "$has_journeys" == "true" ]] && echo -e "  ${GREEN}+${NC} User journeys file included"
    echo ""
    echo -e "${YELLOW}Ready for Claude Code LLM analysis.${NC}"
    echo -e "Run: ${CYAN}/stress-test ${spec_file}${NC}"
}

# ============================================================================
# CHECK-PREPARE: Run PRP quality checks and extract data for LLM analysis
# Output: manifest.json with structural results, source spec comparison
# Claude Code uses this to do LLM assessment directly (no nested CLI)
# ============================================================================
cmd_check_prepare() {
    local prp_file="$1"
    local output_dir="$2"

    [[ ! -f "$prp_file" ]] && { echo -e "${RED}File not found: $prp_file${NC}"; exit 1; }

    # Resolve absolute path
    prp_file=$(cd "$(dirname "$prp_file")" && pwd)/$(basename "$prp_file")

    local prp_name
    prp_name=$(basename "$prp_file" .md)

    # Default output directory
    if [[ -z "$output_dir" ]]; then
        output_dir="${prp_file%/*}/.check-${prp_name}"
    fi

    mkdir -p "$output_dir"

    local prp_content
    prp_content=$(cat "$prp_file")

    # =========================================================================
    # Domain Detection
    # =========================================================================
    local domain_result
    domain_result=$(resolve_domain_invariants "$prp_content")

    local total_invariants domain_count domain_name
    total_invariants=$(echo "$domain_result" | grep "^TOTAL_INVARIANTS=" | cut -d= -f2)
    domain_count=$(echo "$domain_result" | grep "^DOMAIN_COUNT=" | cut -d= -f2)
    domain_name=$(echo "$domain_result" | grep "^DOMAIN_NAME=" | cut -d= -f2)

    # =========================================================================
    # Source Spec Detection
    # =========================================================================
    local source_spec=""
    local source_spec_content=""
    local has_source_spec="false"

    # Try to extract source_spec from PRP meta block
    source_spec=$(echo "$prp_content" | grep -E "^source_spec:" | head -1 | sed 's/source_spec://' | xargs)

    if [[ -z "$source_spec" ]]; then
        # Try alternative format: Source Spec Reference in appendix
        source_spec=$(echo "$prp_content" | grep -E "Spec Path:" | head -1 | sed 's/.*Spec Path://' | xargs)
    fi

    if [[ -n "$source_spec" && -f "$source_spec" ]]; then
        source_spec_content=$(cat "$source_spec")
        has_source_spec="true"
        cp "$source_spec" "$output_dir/source-spec.md"
    fi

    # =========================================================================
    # Structural Checks (same as check_prp_structure)
    # =========================================================================
    local issues=()
    local warnings=()
    local checks=()

    # Required PRP sections
    local required_sections=("overview" "success criteria" "timeline" "risk" "validation")

    for section in "${required_sections[@]}"; do
        if echo "$prp_content" | grep -qiE "^#+.*$section"; then
            checks+=("{\"check\": \"section_${section// /_}\", \"passed\": true, \"label\": \"$section section found\"}")
        else
            checks+=("{\"check\": \"section_${section// /_}\", \"passed\": false, \"label\": \"Missing section: $section\"}")
            issues+=("Missing section: $section")
        fi
    done

    # Check for unfilled placeholders
    local placeholder_count
    placeholder_count=$(grep -cE '\[FILL|\[TODO|\[TBD|\{\{' "$prp_file" 2>/dev/null) || placeholder_count=0
    if [[ $placeholder_count -gt 0 ]]; then
        checks+=("{\"check\": \"placeholders\", \"passed\": false, \"label\": \"Found $placeholder_count unfilled placeholders\"}")
        issues+=("Found $placeholder_count unfilled placeholders")
    else
        checks+=("{\"check\": \"placeholders\", \"passed\": true, \"label\": \"No unfilled placeholders\"}")
    fi

    # Check for LLM reasoning that shouldn't be in output
    if head -30 "$prp_file" | grep -qiE "let me|I'll|I will|here's my|thinking"; then
        checks+=("{\"check\": \"llm_reasoning\", \"passed\": false, \"label\": \"PRP may contain LLM reasoning\"}")
        warnings+=("PRP may contain LLM reasoning that should be removed")
    else
        checks+=("{\"check\": \"llm_reasoning\", \"passed\": true, \"label\": \"No LLM reasoning artifacts\"}")
    fi

    # =========================================================================
    # Source Spec Comparison (if available)
    # =========================================================================
    local comparison_checks=()
    local comparison_preserved=0
    local comparison_missing=0

    if [[ "$has_source_spec" == "true" ]]; then
        # Check for SQL/schema preservation
        if echo "$source_spec_content" | grep -qiE "CREATE TABLE|ALTER TABLE|SQL"; then
            if echo "$prp_content" | grep -qiE "CREATE TABLE|ALTER TABLE|Database Schema"; then
                comparison_checks+=("{\"check\": \"database_schema\", \"preserved\": true, \"label\": \"Database schema content preserved\"}")
                ((comparison_preserved++))
            else
                comparison_checks+=("{\"check\": \"database_schema\", \"preserved\": false, \"label\": \"Source has SQL/schema but PRP may be missing it\"}")
                ((comparison_missing++))
            fi
        fi

        # Check for API endpoint preservation
        if echo "$source_spec_content" | grep -qiE "GET /|POST /|PUT /|DELETE /|/api/"; then
            if echo "$prp_content" | grep -qiE "GET /|POST /|PUT /|DELETE /|/api/|API Spec"; then
                comparison_checks+=("{\"check\": \"api_endpoints\", \"preserved\": true, \"label\": \"API endpoints preserved\"}")
                ((comparison_preserved++))
            else
                comparison_checks+=("{\"check\": \"api_endpoints\", \"preserved\": false, \"label\": \"Source has API endpoints but PRP may be missing them\"}")
                ((comparison_missing++))
            fi
        fi

        # Check for wireframe/ASCII art preservation
        if echo "$source_spec_content" | grep -qE "┌|└|├|│|─"; then
            if echo "$prp_content" | grep -qE "┌|└|├|│|─"; then
                comparison_checks+=("{\"check\": \"ascii_wireframes\", \"preserved\": true, \"label\": \"ASCII wireframes preserved\"}")
                ((comparison_preserved++))
            else
                comparison_checks+=("{\"check\": \"ascii_wireframes\", \"preserved\": false, \"label\": \"Source has ASCII wireframes but PRP may be missing them\"}")
                ((comparison_missing++))
            fi
        fi

        # Check for error messages preservation
        if echo "$source_spec_content" | grep -qiE "error message|Error:|\".*not found\""; then
            if echo "$prp_content" | grep -qiE "error message|Error Catalog|\".*not found\""; then
                comparison_checks+=("{\"check\": \"error_messages\", \"preserved\": true, \"label\": \"Error messages preserved\"}")
                ((comparison_preserved++))
            else
                comparison_checks+=("{\"check\": \"error_messages\", \"preserved\": false, \"label\": \"Source has error messages - verify PRP includes them\"}")
                ((comparison_missing++))
            fi
        fi
    fi

    # =========================================================================
    # Determine Grade
    # =========================================================================
    local structural_grade
    if [[ ${#issues[@]} -gt 0 ]]; then
        structural_grade="FAIL"
    elif [[ ${#warnings[@]} -gt 0 ]]; then
        structural_grade="NEEDS_WORK"
    else
        structural_grade="PASS"
    fi

    # =========================================================================
    # Generate Manifest
    # =========================================================================
    local prp_hash
    prp_hash=$(git hash-object "$prp_file" 2>/dev/null | head -c 7 || md5 -q "$prp_file" 2>/dev/null | head -c 7 || echo "unknown")

    local manifest_file="$output_dir/.manifest.json"

    # Build checks JSON array
    local checks_json="["
    local first=true
    for check in "${checks[@]}"; do
        if [[ "$first" == "true" ]]; then
            checks_json+="$check"
            first=false
        else
            checks_json+=",$check"
        fi
    done
    checks_json+="]"

    # Build issues JSON array
    local issues_json="["
    first=true
    for issue in "${issues[@]}"; do
        if [[ "$first" == "true" ]]; then
            issues_json+="\"$issue\""
            first=false
        else
            issues_json+=",\"$issue\""
        fi
    done
    issues_json+="]"

    # Build warnings JSON array
    local warnings_json="["
    first=true
    for warning in "${warnings[@]}"; do
        if [[ "$first" == "true" ]]; then
            warnings_json+="\"$warning\""
            first=false
        else
            warnings_json+=",\"$warning\""
        fi
    done
    warnings_json+="]"

    # Build comparison checks JSON array
    local comparison_json="["
    first=true
    for check in "${comparison_checks[@]}"; do
        if [[ "$first" == "true" ]]; then
            comparison_json+="$check"
            first=false
        else
            comparison_json+=",$check"
        fi
    done
    comparison_json+="]"

    cat > "$manifest_file" << EOF
{
  "prp_file": "$prp_file",
  "prp_hash": "$prp_hash",
  "output_dir": "$output_dir",
  "check_date": "$(date +%Y-%m-%d)",
  "structural_checks": {
    "checks": $checks_json,
    "issues": $issues_json,
    "warnings": $warnings_json,
    "grade": "$structural_grade",
    "placeholder_count": $placeholder_count
  },
  "source_spec": {
    "found": $has_source_spec,
    "path": "${source_spec:-null}",
    "comparison": {
      "checks": $comparison_json,
      "preserved": $comparison_preserved,
      "missing": $comparison_missing
    }
  },
  "domain_info": {
    "domain_name": "${domain_name:-universal}",
    "domain_count": ${domain_count:-0},
    "total_invariants": ${total_invariants:-11}
  },
  "llm_analysis_prompt": {
    "context": "prp_quality_check",
    "focus": "Implementation readiness and extraction completeness",
    "check_for": [
      "Confidence score sanity check",
      "NOT_SPECIFIED_IN_SPEC flags indicating extraction gaps",
      "Thinking level appropriateness for complexity",
      "Appendix content verification (schemas, code blocks)",
      "Implementation blockers"
    ],
    "output_schema": {
      "summary": "One sentence on PRP readiness",
      "blockers": "Things that block implementation (max 5)",
      "confidence_assessment": "Is stated confidence score reasonable?",
      "extraction_gaps": "Content from spec not found in PRP (max 5)",
      "suggestions": "Improvements to make PRP more actionable (max 5)"
    }
  }
}
EOF

    # Save PRP content for Claude Code to analyze
    cp "$prp_file" "$output_dir/prp-content.md"

    # =========================================================================
    # Output Summary
    # =========================================================================
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  CHECK-PREPARE COMPLETE                                       ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "PRP:        ${CYAN}$prp_file${NC}"
    echo -e "Output:     ${CYAN}$output_dir${NC}"
    echo -e "Manifest:   ${CYAN}$manifest_file${NC}"
    echo ""
    echo -e "${BLUE}Structural Checks:${NC}"
    echo -e "  Grade:        ${CYAN}$structural_grade${NC}"
    echo -e "  Issues:       ${CYAN}${#issues[@]}${NC}"
    echo -e "  Warnings:     ${CYAN}${#warnings[@]}${NC}"
    echo -e "  Placeholders: ${CYAN}$placeholder_count${NC}"
    echo ""
    if [[ "$has_source_spec" == "true" ]]; then
        echo -e "${BLUE}Source Spec Comparison:${NC}"
        echo -e "  Source:       ${CYAN}$source_spec${NC}"
        echo -e "  Preserved:    ${CYAN}$comparison_preserved${NC}"
        echo -e "  Missing:      ${CYAN}$comparison_missing${NC}"
        echo ""
    else
        echo -e "${YELLOW}Source spec not found or not accessible${NC}"
        echo ""
    fi
    echo -e "${BLUE}Domain Info:${NC}"
    echo -e "  Domain:       ${CYAN}${domain_name:-universal}${NC}"
    echo -e "  Invariants:   ${CYAN}${total_invariants:-11}${NC}"
    echo ""
    echo -e "${YELLOW}Ready for Claude Code LLM analysis.${NC}"
    echo -e "Run: ${CYAN}/check ${prp_file}${NC}"
}

cmd_ralph_check() {
    local prp_file="$1"
    local steps_dir="$2"
    local quick="$3"

    [[ ! -f "$prp_file" ]] && { echo -e "${RED}PRP file not found: $prp_file${NC}"; exit 1; }
    [[ ! -d "$steps_dir" ]] && { echo -e "${RED}Steps directory not found: $steps_dir${NC}"; exit 1; }

    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  RALPH PRP COMPLIANCE CHECK (v$VERSION)                         ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "PRP:   ${CYAN}$prp_file${NC}"
    echo -e "Steps: ${CYAN}$steps_dir${NC}"
    echo ""

    # Deterministic checks
    local struct_output struct_grade
    struct_output=$(check_ralph_deterministic "$prp_file" "$steps_dir")
    echo "$struct_output" | sed '$d'
    struct_grade=$(echo "$struct_output" | tail -1)

    local llm_grade="SKIPPED"
    if [[ "$quick" != "true" ]]; then
        echo ""
        local llm_output
        llm_output=$(get_ralph_llm_assessment "$prp_file" "$steps_dir")
        echo "$llm_output" | sed '$d'
        llm_grade=$(echo "$llm_output" | tail -1)
    fi

    # Count issues and warnings from the output
    local issue_count warning_count
    issue_count=$(echo "$struct_output" | grep -c "✗" 2>/dev/null || true)
    warning_count=$(echo "$struct_output" | grep -c "!" 2>/dev/null || true)
    # Default to 0 if empty
    issue_count=${issue_count:-0}
    warning_count=${warning_count:-0}

    # Summary with explicit review checklist
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  THE PRP IS THE CONTRACT. Implementation must match PRP exactly.${NC}"
    echo -e "${BLUE}───────────────────────────────────────────────────────────────${NC}"

    if [[ "$struct_grade" == "FAIL" ]]; then
        echo -e "  Status: ${RED}COMPLIANCE ISSUES${NC}"
        echo -e "  Implementation deviates from PRP definitions."
    elif [[ "$struct_grade" == "NEEDS_WORK" ]]; then
        echo -e "  Status: ${YELLOW}ITEMS TO REVIEW${NC}"
        echo -e "  Found potential compliance gaps."
    else
        echo -e "  Status: ${GREEN}COMPLIANT${NC}"
        echo -e "  Implementation appears to match PRP definitions."
    fi

    # Explicit review checklist - ALL items require acknowledgment
    echo ""
    echo -e "${BLUE}───────────────────────────────────────────────────────────────${NC}"
    echo -e "  ${YELLOW}HUMAN REVIEW CHECKLIST (all items require acknowledgment):${NC}"
    echo ""

    local review_count=0
    if [[ $issue_count -gt 0 ]]; then
        echo -e "  ${RED}[  ] $issue_count COMPLIANCE ISSUE(S)${NC} - Must fix before execution"
        review_count=$((review_count + issue_count))
    fi
    if [[ $warning_count -gt 0 ]]; then
        echo -e "  ${YELLOW}[  ] $warning_count WARNING(S)${NC} - Review and acknowledge each"
        review_count=$((review_count + warning_count))
    fi
    if [[ $issue_count -eq 0 && $warning_count -eq 0 ]]; then
        echo -e "  ${GREEN}[  ] All checks passed${NC} - Confirm implementation is ready"
        review_count=1
    fi

    echo ""
    echo -e "  Total items requiring human review: ${CYAN}$review_count${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

    [[ "$quick" != "true" ]] && show_cost_summary

    # ALWAYS require human acknowledgment - no exceptions
    require_review_acknowledgment "ralph-check" "$prp_file"

    echo ""
}

# ============================================================================
# DELEGATED COMMANDS (pass-through to external scripts)
# ============================================================================

# Get the root design-ops directory (parent of enforcement/)
DESIGNOPS_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

delegate_command() {
    local script_path="$1"
    local command_name="$2"
    shift 2

    if [[ ! -f "$script_path" ]]; then
        echo -e "${RED}Error: '$command_name' requires $(basename "$script_path")${NC}" >&2
        echo -e "${YELLOW}Expected at: $script_path${NC}" >&2
        exit 1
    fi

    if [[ ! -x "$script_path" ]]; then
        chmod +x "$script_path"
    fi

    exec "$script_path" "$@"
}

cmd_orchestrate() {
    delegate_command "$DESIGNOPS_ROOT/tools/multi-agent-orchestrator.sh" "orchestrate" "$@"
}

cmd_watch() {
    delegate_command "$DESIGNOPS_ROOT/tools/watch-mode.sh" "watch" "$@"
}

cmd_dashboard() {
    delegate_command "$DESIGNOPS_ROOT/tools/validation-dashboard.sh" "dashboard" "$@"
}

cmd_retro() {
    delegate_command "$DESIGNOPS_ROOT/agents/retrospective.sh" "retro" "$@"
}

cmd_conventions() {
    delegate_command "$DESIGNOPS_ROOT/tools/conventions-generator.sh" "conventions" "$@"
}

# ============================================================================
# MAIN
# ============================================================================

# Handle commands that don't require a file argument
if [[ $# -eq 1 ]]; then
    case "$1" in
        dashboard) cmd_dashboard ;;
        -h|--help|help) usage ;;
        *) usage ;;
    esac
fi

[[ $# -lt 2 ]] && usage

COMMAND="$1"
FILE="$2"
shift 2

QUICK=false
VERBOSE=false
SKIP_REVIEW=false
REQUIREMENTS=""
JOURNEYS=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --quick) QUICK=true; shift ;;
        --skip-review) SKIP_REVIEW=true; shift ;;
        --verbose) VERBOSE=true; shift ;;
        --output) OUTPUT="$2"; shift 2 ;;
        --requirements) REQUIREMENTS="$2"; shift 2 ;;
        --journeys) JOURNEYS="$2"; shift 2 ;;
        --steps) STEPS_DIR="$2"; shift 2 ;;
        --phase) PHASE="$2"; shift 2 ;;
        *) echo -e "${RED}Unknown option: $1${NC}"; usage ;;
    esac
done

# Check dependencies
command -v claude &> /dev/null || { echo -e "${RED}ERROR: Claude CLI not found${NC}"; exit 1; }
command -v python3 &> /dev/null || { echo -e "${RED}ERROR: Python3 not found${NC}"; exit 1; }

case "$COMMAND" in
    # Core commands (built-in)
    stress-test) cmd_stress_test "$FILE" "$REQUIREMENTS" "$JOURNEYS" "$QUICK" ;;
    stress-test-prepare) cmd_stress_test_prepare "$FILE" "$REQUIREMENTS" "$JOURNEYS" "$OUTPUT" ;;
    validate) cmd_validate "$FILE" "$QUICK" ;;
    validate-prepare) cmd_validate_prepare "$FILE" "$OUTPUT" ;;
    spec-prepare) cmd_spec_prepare "$FILE" "$OUTPUT" "" "" ;;
    generate) cmd_generate "$FILE" "$OUTPUT" ;;
    generate-prepare) cmd_generate_prepare "$FILE" "$OUTPUT" ;;
    check) cmd_check "$FILE" "$QUICK" ;;
    check-prepare) cmd_check_prepare "$FILE" "$OUTPUT" ;;
    implement) cmd_implement "$FILE" "$OUTPUT" "$PHASE" ;;
    implement-prepare) cmd_implement_prepare "$FILE" "$OUTPUT" ;;
    ralph-check) cmd_ralph_check "$FILE" "$STEPS_DIR" "$QUICK" ;;
    # Advanced commands (delegated)
    orchestrate) cmd_orchestrate "$FILE" "$@" ;;
    watch) cmd_watch "$FILE" "$@" ;;
    dashboard) cmd_dashboard "$@" ;;
    retro) cmd_retro "$FILE" "$@" ;;
    conventions) cmd_conventions "$FILE" "$@" ;;
    *) echo -e "${RED}Unknown command: $COMMAND${NC}"; usage ;;
esac
