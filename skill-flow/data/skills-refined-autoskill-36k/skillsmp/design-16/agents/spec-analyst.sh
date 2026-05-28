#!/bin/bash
#
# spec-analyst.sh - Analyze spec completeness and extract requirements
#
# Usage: ./agents/spec-analyst.sh <spec-file> [--domain <domain>] [--output <dir>]
#
# Outputs:
#   - analysis.json with completeness score, requirements, complexity factors
#   - Human-readable summary to stdout

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
SPEC_FILE=""
DOMAIN="general"
OUTPUT_DIR="."
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 <spec-file> [--domain <domain>] [--output <dir>]"
            echo ""
            echo "Options:"
            echo "  --domain <domain>  Target domain (api, database, security, etc.)"
            echo "  --output <dir>     Output directory for analysis.json"
            echo "  --verbose, -v      Show detailed output"
            exit 0
            ;;
        -*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            SPEC_FILE="$1"
            shift
            ;;
    esac
done

# Validate input
if [[ -z "$SPEC_FILE" ]]; then
    echo -e "${RED}Error: Spec file required${NC}"
    echo "Usage: $0 <spec-file> [--domain <domain>] [--output <dir>]"
    exit 1
fi

if [[ ! -f "$SPEC_FILE" ]]; then
    echo -e "${RED}Error: Spec file not found: $SPEC_FILE${NC}"
    exit 1
fi

echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  SPEC ANALYST - Completeness and Requirements Analysis${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Spec:${NC}   $SPEC_FILE"
echo -e "${BLUE}Domain:${NC} $DOMAIN"
echo ""

# Read spec content
CONTENT=$(cat "$SPEC_FILE")

# ============================================================================
# SECTION 1: Check Required Sections
# ============================================================================
echo -e "${YELLOW}[1/5] Checking required sections...${NC}"

declare -A SECTIONS
SECTIONS=(
    ["problem"]="(problem|challenge|issue|objective)"
    ["requirements"]="(requirement|feature|must|shall|need)"
    ["scope"]="(scope|boundary|in scope|out of scope)"
    ["success_criteria"]="(success|criteria|acceptance|done when)"
    ["constraints"]="(constraint|limitation|restriction|cannot)"
    ["dependencies"]="(depend|prerequisite|require|block)"
    ["risks"]="(risk|concern|issue|worry)"
    ["timeline"]="(timeline|deadline|milestone|date|phase)"
)

SECTION_SCORES=()
MISSING_SECTIONS=()
FOUND_SECTIONS=()

for section in "${!SECTIONS[@]}"; do
    pattern="${SECTIONS[$section]}"
    if echo "$CONTENT" | grep -qiE "$pattern"; then
        SECTION_SCORES+=("$section:1")
        FOUND_SECTIONS+=("$section")
        [[ "$VERBOSE" == "true" ]] && echo -e "  ${GREEN}✓${NC} $section"
    else
        SECTION_SCORES+=("$section:0")
        MISSING_SECTIONS+=("$section")
        [[ "$VERBOSE" == "true" ]] && echo -e "  ${RED}✗${NC} $section"
    fi
done

FOUND_COUNT=${#FOUND_SECTIONS[@]}
TOTAL_SECTIONS=${#SECTIONS[@]}
SECTION_SCORE=$((FOUND_COUNT * 100 / TOTAL_SECTIONS))

echo -e "  Found ${GREEN}$FOUND_COUNT${NC}/${TOTAL_SECTIONS} sections (${SECTION_SCORE}%)"

# ============================================================================
# SECTION 2: Extract Requirements
# ============================================================================
echo -e "${YELLOW}[2/5] Extracting requirements...${NC}"

# Count requirement-like statements
MUST_COUNT=$(echo "$CONTENT" | grep -ciE '\bmust\b' || true)
SHALL_COUNT=$(echo "$CONTENT" | grep -ciE '\bshall\b' || true)
SHOULD_COUNT=$(echo "$CONTENT" | grep -ciE '\bshould\b' || true)
WILL_COUNT=$(echo "$CONTENT" | grep -ciE '\bwill\b' || true)

REQUIREMENT_INDICATORS=$((MUST_COUNT + SHALL_COUNT + SHOULD_COUNT + WILL_COUNT))

echo -e "  Found ${GREEN}$REQUIREMENT_INDICATORS${NC} requirement indicators"
echo -e "    must: $MUST_COUNT, shall: $SHALL_COUNT, should: $SHOULD_COUNT, will: $WILL_COUNT"

# Categorize requirements strength
if [[ $REQUIREMENT_INDICATORS -ge 10 ]]; then
    REQ_STRENGTH="strong"
elif [[ $REQUIREMENT_INDICATORS -ge 5 ]]; then
    REQ_STRENGTH="moderate"
else
    REQ_STRENGTH="weak"
fi

# ============================================================================
# SECTION 3: Assess Complexity
# ============================================================================
echo -e "${YELLOW}[3/5] Assessing complexity...${NC}"

COMPLEXITY_FACTORS=()
COMPLEXITY_SCORE=0

# Check for complexity indicators
if echo "$CONTENT" | grep -qiE "security|auth|encrypt|token|credential"; then
    COMPLEXITY_FACTORS+=("security")
    ((COMPLEXITY_SCORE+=2))
fi

if echo "$CONTENT" | grep -qiE "migration|database|schema|sql"; then
    COMPLEXITY_FACTORS+=("database")
    ((COMPLEXITY_SCORE+=2))
fi

if echo "$CONTENT" | grep -qiE "integration|external|api|third.party|webhook"; then
    COMPLEXITY_FACTORS+=("integration")
    ((COMPLEXITY_SCORE+=2))
fi

if echo "$CONTENT" | grep -qiE "production|deploy|release|rollback"; then
    COMPLEXITY_FACTORS+=("deployment")
    ((COMPLEXITY_SCORE+=1))
fi

if echo "$CONTENT" | grep -qiE "performance|scale|throughput|latency"; then
    COMPLEXITY_FACTORS+=("performance")
    ((COMPLEXITY_SCORE+=1))
fi

if echo "$CONTENT" | grep -qiE "concurrent|parallel|async|race"; then
    COMPLEXITY_FACTORS+=("concurrency")
    ((COMPLEXITY_SCORE+=2))
fi

if echo "$CONTENT" | grep -qiE "backward|compatible|legacy|existing"; then
    COMPLEXITY_FACTORS+=("compatibility")
    ((COMPLEXITY_SCORE+=1))
fi

WORD_COUNT=$(echo "$CONTENT" | wc -w | tr -d ' ')
if [[ $WORD_COUNT -gt 2000 ]]; then
    COMPLEXITY_FACTORS+=("large_scope")
    ((COMPLEXITY_SCORE+=1))
fi

echo -e "  Complexity score: ${YELLOW}$COMPLEXITY_SCORE${NC}"
if [[ ${#COMPLEXITY_FACTORS[@]} -gt 0 ]]; then
    echo -e "  Factors: ${COMPLEXITY_FACTORS[*]}"
fi

# ============================================================================
# SECTION 4: Determine Thinking Level
# ============================================================================
echo -e "${YELLOW}[4/5] Determining thinking level...${NC}"

if [[ $COMPLEXITY_SCORE -ge 7 ]]; then
    THINKING_LEVEL="ultrathink"
    THINKING_REASON="High complexity ($COMPLEXITY_SCORE) with factors: ${COMPLEXITY_FACTORS[*]}"
elif [[ $COMPLEXITY_SCORE -ge 4 ]]; then
    THINKING_LEVEL="think_hard"
    THINKING_REASON="Medium-high complexity ($COMPLEXITY_SCORE)"
elif [[ $COMPLEXITY_SCORE -ge 2 ]]; then
    THINKING_LEVEL="think"
    THINKING_REASON="Moderate complexity ($COMPLEXITY_SCORE)"
else
    THINKING_LEVEL="normal"
    THINKING_REASON="Low complexity ($COMPLEXITY_SCORE)"
fi

echo -e "  Recommended: ${CYAN}$THINKING_LEVEL${NC}"
echo -e "  Reason: $THINKING_REASON"

# ============================================================================
# SECTION 5: Calculate Completeness Score
# ============================================================================
echo -e "${YELLOW}[5/5] Calculating completeness score...${NC}"

# Weighted scoring
COMPLETENESS_SCORE=0

# Section coverage (40%)
COMPLETENESS_SCORE=$((COMPLETENESS_SCORE + SECTION_SCORE * 40 / 100))

# Requirements clarity (30%)
case $REQ_STRENGTH in
    strong)   COMPLETENESS_SCORE=$((COMPLETENESS_SCORE + 30)) ;;
    moderate) COMPLETENESS_SCORE=$((COMPLETENESS_SCORE + 20)) ;;
    weak)     COMPLETENESS_SCORE=$((COMPLETENESS_SCORE + 10)) ;;
esac

# Has success criteria (15%)
if echo "$CONTENT" | grep -qiE "success|criteria|acceptance|done when"; then
    COMPLETENESS_SCORE=$((COMPLETENESS_SCORE + 15))
fi

# Has scope boundaries (15%)
if echo "$CONTENT" | grep -qiE "in scope|out of scope|scope|boundary"; then
    COMPLETENESS_SCORE=$((COMPLETENESS_SCORE + 15))
fi

# Cap at 100
[[ $COMPLETENESS_SCORE -gt 100 ]] && COMPLETENESS_SCORE=100

echo -e "  Completeness: ${GREEN}${COMPLETENESS_SCORE}%${NC}"

# ============================================================================
# Generate JSON Output
# ============================================================================
OUTPUT_FILE="$OUTPUT_DIR/analysis.json"

# Convert arrays to JSON format
MISSING_JSON=$(printf '%s\n' "${MISSING_SECTIONS[@]}" | jq -R . | jq -s .)
COMPLEXITY_JSON=$(printf '%s\n' "${COMPLEXITY_FACTORS[@]}" | jq -R . | jq -s . 2>/dev/null || echo "[]")

cat > "$OUTPUT_FILE" << EOF
{
  "spec_file": "$SPEC_FILE",
  "domain": "$DOMAIN",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "completeness_score": $COMPLETENESS_SCORE,
  "section_coverage": {
    "score": $SECTION_SCORE,
    "found": $FOUND_COUNT,
    "total": $TOTAL_SECTIONS,
    "missing": $MISSING_JSON
  },
  "requirements": {
    "strength": "$REQ_STRENGTH",
    "indicators": {
      "must": $MUST_COUNT,
      "shall": $SHALL_COUNT,
      "should": $SHOULD_COUNT,
      "will": $WILL_COUNT,
      "total": $REQUIREMENT_INDICATORS
    }
  },
  "complexity": {
    "score": $COMPLEXITY_SCORE,
    "factors": $COMPLEXITY_JSON
  },
  "thinking_level": {
    "recommended": "$THINKING_LEVEL",
    "reason": "$THINKING_REASON"
  },
  "word_count": $WORD_COUNT
}
EOF

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Analysis complete!${NC}"
echo -e "Output: $OUTPUT_FILE"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"

# Summary
echo ""
echo -e "${BLUE}Summary:${NC}"
echo -e "  Completeness:    ${COMPLETENESS_SCORE}%"
echo -e "  Requirements:    $REQ_STRENGTH ($REQUIREMENT_INDICATORS indicators)"
echo -e "  Complexity:      $COMPLEXITY_SCORE"
echo -e "  Thinking Level:  $THINKING_LEVEL"

if [[ ${#MISSING_SECTIONS[@]} -gt 0 ]]; then
    echo ""
    echo -e "${YELLOW}Missing sections:${NC}"
    for section in "${MISSING_SECTIONS[@]}"; do
        echo -e "  - $section"
    done
fi

# Exit with appropriate code
if [[ $COMPLETENESS_SCORE -lt 50 ]]; then
    echo ""
    echo -e "${RED}WARNING: Spec completeness below 50%. Consider adding more detail.${NC}"
    exit 1
fi

exit 0
