#!/bin/bash
# spec-delta-to-invariant.sh - Analyze retrospectives and suggest new invariants
#
# Parses retrospective files for system improvement suggestions and generates
# properly formatted invariant proposals for domain modules.

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
DOMAINS_DIR="$SCRIPT_DIR/../domains"
SYSTEM_INVARIANTS="$SCRIPT_DIR/../system-invariants.md"

# Usage
usage() {
    echo "Usage: $0 <retrospective-file.md> [--output <file>] [--domain <domain>]"
    echo ""
    echo "Options:"
    echo "  --output <file>    Output file for invariant proposal (default: stdout)"
    echo "  --domain <domain>  Target domain module (auto-detected if not specified)"
    echo "  --check            Check retrospective completeness without generating"
    echo ""
    echo "Example:"
    echo "  $0 retrospectives/project-retro.md"
    echo "  $0 retrospectives/project-retro.md --domain integration"
    exit 1
}

# Check arguments
if [[ $# -lt 1 ]]; then
    usage
fi

RETRO_FILE="$1"
shift

OUTPUT_FILE=""
TARGET_DOMAIN=""
CHECK_ONLY=false

# Parse options
while [[ $# -gt 0 ]]; do
    case "$1" in
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --domain)
            TARGET_DOMAIN="$2"
            shift 2
            ;;
        --check)
            CHECK_ONLY=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# Validate file exists
if [[ ! -f "$RETRO_FILE" ]]; then
    echo -e "${RED}ERROR: Retrospective file not found: $RETRO_FILE${NC}"
    exit 1
fi

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Spec-Delta to Invariant Analyzer${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Analyzing: ${CYAN}$RETRO_FILE${NC}"
echo ""

# Read retrospective content
CONTENT=$(cat "$RETRO_FILE")

# ============================================================================
# Check retrospective completeness
# ============================================================================

echo -e "${BLUE}─── Checking Retrospective Completeness ───${NC}"

COMPLETENESS_SCORE=0
COMPLETENESS_ISSUES=()

# Check for System Improvements section
if echo "$CONTENT" | grep -q "## 5. System Improvements"; then
    echo -e "  ${GREEN}✓${NC} System Improvements section found"
    ((COMPLETENESS_SCORE+=20))
else
    echo -e "  ${RED}✗${NC} Missing: System Improvements section"
    COMPLETENESS_ISSUES+=("Missing System Improvements section")
fi

# Check for process improvement answer
if echo "$CONTENT" | grep -A 10 "### 5.1 Process/Template" | grep -qvE "^\s*$|^###|{{"; then
    echo -e "  ${GREEN}✓${NC} Process improvement answered"
    ((COMPLETENESS_SCORE+=20))
else
    echo -e "  ${YELLOW}⚠${NC} Process improvement question not fully answered"
    COMPLETENESS_ISSUES+=("Process improvement needs more detail")
fi

# Check for missing invariant section
if echo "$CONTENT" | grep -A 10 "### 5.2 Missing Invariants" | grep -qvE "^\s*$|^###|{{"; then
    echo -e "  ${GREEN}✓${NC} Missing invariants section answered"
    ((COMPLETENESS_SCORE+=20))
else
    echo -e "  ${YELLOW}⚠${NC} Missing invariants section not fully answered"
    COMPLETENESS_ISSUES+=("Missing invariants needs more detail")
fi

# Check for CONVENTIONS.md update
if echo "$CONTENT" | grep -A 10 "### 5.3 CONVENTIONS" | grep -qvE "^\s*$|^###|{{"; then
    echo -e "  ${GREEN}✓${NC} CONVENTIONS update section answered"
    ((COMPLETENESS_SCORE+=20))
else
    echo -e "  ${YELLOW}⚠${NC} CONVENTIONS update not specified"
    COMPLETENESS_ISSUES+=("CONVENTIONS update needs specification")
fi

# Check for validation command
if echo "$CONTENT" | grep -A 10 "### 5.5 Validation Command" | grep -q '```bash'; then
    echo -e "  ${GREEN}✓${NC} Validation command provided"
    ((COMPLETENESS_SCORE+=20))
else
    echo -e "  ${YELLOW}⚠${NC} No validation command provided"
    COMPLETENESS_ISSUES+=("No validation command specified")
fi

echo ""
echo -e "Completeness score: ${CYAN}${COMPLETENESS_SCORE}/100${NC}"

if [[ ${#COMPLETENESS_ISSUES[@]} -gt 0 ]]; then
    echo ""
    echo -e "${YELLOW}Issues to address:${NC}"
    for issue in "${COMPLETENESS_ISSUES[@]}"; do
        echo -e "  - $issue"
    done
fi

if [[ "$CHECK_ONLY" == "true" ]]; then
    echo ""
    if [[ $COMPLETENESS_SCORE -ge 80 ]]; then
        echo -e "${GREEN}✅ Retrospective is sufficiently complete${NC}"
        exit 0
    else
        echo -e "${RED}❌ Retrospective needs more detail in System Improvements${NC}"
        exit 1
    fi
fi

echo ""

# ============================================================================
# Extract invariant candidates
# ============================================================================

echo -e "${BLUE}─── Extracting Invariant Candidates ───${NC}"

# Get next invariant number
get_next_invariant_number() {
    local current_max=43  # Base system invariants end at 43

    # Check each domain file for higher numbers
    for domain_file in "$DOMAINS_DIR"/*.md; do
        if [[ -f "$domain_file" ]]; then
            local max_in_file=$(grep -oE "Invariant #[0-9]+" "$domain_file" 2>/dev/null | grep -oE "[0-9]+" | sort -n | tail -1)
            if [[ -n "$max_in_file" ]] && [[ "$max_in_file" -gt "$current_max" ]]; then
                current_max=$max_in_file
            fi
        fi
    done

    echo $((current_max + 1))
}

NEXT_NUM=$(get_next_invariant_number)

# Extract proposed invariant from retrospective
extract_invariant() {
    # Look for the proposed invariant section
    local invariant_block=$(echo "$CONTENT" | sed -n '/### 5.2 Missing Invariants/,/### 5.3/p')

    # Extract key parts
    local description=$(echo "$invariant_block" | grep -A 3 "What invariant was missing" | tail -n +2 | head -3 | tr '\n' ' ')
    local condition=$(echo "$invariant_block" | grep -A 1 "CONDITION:" | tail -1)
    local violation=$(echo "$invariant_block" | grep -A 1 "VIOLATION:" | tail -1)
    local fix=$(echo "$invariant_block" | grep -A 1 "FIX:" | tail -1)
    local domain=$(echo "$invariant_block" | grep -A 1 "Applies to:" | tail -1)

    echo "$description|$condition|$violation|$fix|$domain"
}

INVARIANT_DATA=$(extract_invariant)

# Parse extracted data
IFS='|' read -r INV_DESC INV_CONDITION INV_VIOLATION INV_FIX INV_DOMAIN <<< "$INVARIANT_DATA"

# Detect domain if not specified
if [[ -z "$TARGET_DOMAIN" ]]; then
    if [[ "$INV_DOMAIN" =~ "universal" ]]; then
        TARGET_DOMAIN="universal"
    elif [[ "$INV_DOMAIN" =~ "consumer" ]]; then
        TARGET_DOMAIN="consumer-product"
    elif [[ "$INV_DOMAIN" =~ "data" ]]; then
        TARGET_DOMAIN="data-architecture"
    elif [[ "$INV_DOMAIN" =~ "integration" ]]; then
        TARGET_DOMAIN="integration"
    elif [[ "$INV_DOMAIN" =~ "construction" ]]; then
        TARGET_DOMAIN="physical-construction"
    elif [[ "$INV_DOMAIN" =~ "remote" ]]; then
        TARGET_DOMAIN="remote-management"
    else
        TARGET_DOMAIN="universal"
    fi
    echo -e "  Auto-detected domain: ${CYAN}$TARGET_DOMAIN${NC}"
fi

echo -e "  Next invariant number: ${CYAN}#$NEXT_NUM${NC}"
echo ""

# ============================================================================
# Generate invariant proposal
# ============================================================================

echo -e "${BLUE}─── Generating Invariant Proposal ───${NC}"

# Clean up extracted values
clean_value() {
    local val="$1"
    # Remove template markers and trim
    echo "$val" | sed 's/{{[^}]*}}//g' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
}

INV_DESC_CLEAN=$(clean_value "$INV_DESC")
INV_CONDITION_CLEAN=$(clean_value "$INV_CONDITION")
INV_VIOLATION_CLEAN=$(clean_value "$INV_VIOLATION")
INV_FIX_CLEAN=$(clean_value "$INV_FIX")

# Generate invariant name from description
generate_invariant_name() {
    local desc="$1"
    # Extract key concept words and format as invariant name
    echo "$desc" | head -c 50 | sed 's/[^a-zA-Z ]//g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1' | tr -d ' '
}

INV_NAME=$(generate_invariant_name "$INV_DESC_CLEAN")
if [[ -z "$INV_NAME" ]]; then
    INV_NAME="NewInvariantFromRetro"
fi

# Create the proposal
PROPOSAL=$(cat <<EOF
# Invariant Proposal from Retrospective

## Source
- **Retrospective**: $RETRO_FILE
- **Generated**: $(date +%Y-%m-%d)
- **Target Domain**: $TARGET_DOMAIN

---

## Proposed Invariant

### Invariant #$NEXT_NUM: $INV_NAME

**Description**: $INV_DESC_CLEAN

**Condition to Check**:
\`\`\`
$INV_CONDITION_CLEAN
\`\`\`

**Violation Trigger**:
\`\`\`
$INV_VIOLATION_CLEAN
\`\`\`

**Required Fix**:
\`\`\`
$INV_FIX_CLEAN
\`\`\`

---

## Formatted for Domain Module

Add this to \`domains/$TARGET_DOMAIN.md\`:

\`\`\`markdown
### Invariant #$NEXT_NUM: $INV_NAME

**Condition**: $INV_CONDITION_CLEAN

**Violation**: $INV_VIOLATION_CLEAN

**Fix**: $INV_FIX_CLEAN

**Example**:
\`\`\`
[Add concrete example of violation and fix]
\`\`\`
\`\`\`

---

## Validation Command

Add to \`validator.sh\` or domain-specific checker:

\`\`\`bash
# Check for Invariant #$NEXT_NUM
check_invariant_$NEXT_NUM() {
    local spec_file="\$1"
    # TODO: Implement check based on condition
    # Return 0 if passes, 1 if violation
    return 0
}
\`\`\`

---

## Review Checklist

Before adding this invariant:

- [ ] Confirm this issue has occurred more than once
- [ ] Verify the invariant is testable/checkable
- [ ] Review for overlap with existing invariants
- [ ] Add concrete example to the invariant
- [ ] Update validator.sh to check for this invariant
- [ ] Test against existing specs (should not break valid specs)

---

*Generated by spec-delta-to-invariant.sh*
EOF
)

# Output the proposal
if [[ -n "$OUTPUT_FILE" ]]; then
    echo "$PROPOSAL" > "$OUTPUT_FILE"
    echo -e "${GREEN}✅ Invariant proposal written to: $OUTPUT_FILE${NC}"
else
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
    echo ""
    echo "$PROPOSAL"
fi

echo ""
echo -e "${BLUE}─── Summary ───${NC}"
echo ""
echo -e "Proposed: ${CYAN}Invariant #$NEXT_NUM: $INV_NAME${NC}"
echo -e "Domain: ${CYAN}$TARGET_DOMAIN${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Review the proposal for accuracy"
echo "2. Add concrete examples"
echo "3. Add to domains/$TARGET_DOMAIN.md"
echo "4. Update validator.sh to check for this invariant"
echo "5. Test against existing specs"
echo ""
echo -e "${GREEN}Done!${NC}"
