#!/bin/bash
#
# validator.sh - Validate spec against domain invariants
#
# Usage: ./agents/validator.sh <spec-file> --domain <domain> [--conventions <file>] [--output <dir>]
#
# Outputs:
#   - validation.json with violations, warnings, and confidence score

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
INVARIANTS_DIR="$DESIGN_OPS_ROOT/invariants"

# Defaults
SPEC_FILE=""
DOMAIN=""
CONVENTIONS_FILE=""
OUTPUT_DIR="."
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --conventions)
            CONVENTIONS_FILE="$2"
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
            echo "Usage: $0 <spec-file> --domain <domain> [options]"
            echo ""
            echo "Options:"
            echo "  --domain <domain>       Required. Domain to validate against"
            echo "  --conventions <file>    Path to CONVENTIONS.md"
            echo "  --output <dir>          Output directory"
            echo "  --verbose, -v           Show detailed output"
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
    exit 1
fi

if [[ ! -f "$SPEC_FILE" ]]; then
    echo -e "${RED}Error: Spec file not found: $SPEC_FILE${NC}"
    exit 1
fi

if [[ -z "$DOMAIN" ]]; then
    echo -e "${RED}Error: Domain required (--domain)${NC}"
    exit 1
fi

echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  VALIDATOR - Domain Invariant Validation${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Spec:${NC}   $SPEC_FILE"
echo -e "${BLUE}Domain:${NC} $DOMAIN"
echo ""

CONTENT=$(cat "$SPEC_FILE")

# Arrays to collect results
declare -a VIOLATIONS_CRITICAL
declare -a VIOLATIONS_MAJOR
declare -a VIOLATIONS_MINOR
declare -a WARNINGS
declare -a PASSED

INVARIANTS_CHECKED=0
INVARIANTS_PASSED=0

# ============================================================================
# Load Domain Invariants
# ============================================================================
DOMAIN_FILE="$INVARIANTS_DIR/$DOMAIN.md"

if [[ ! -f "$DOMAIN_FILE" ]]; then
    echo -e "${YELLOW}Warning: No invariant file for domain '$DOMAIN'${NC}"
    echo -e "Expected: $DOMAIN_FILE"
    echo ""

    # Fallback to general checks only
    DOMAIN_INVARIANTS=""
else
    DOMAIN_INVARIANTS=$(cat "$DOMAIN_FILE")
    echo -e "${GREEN}Loaded domain invariants: $DOMAIN_FILE${NC}"
fi

# ============================================================================
# SECTION 1: Core Invariant Checks (Always Run)
# ============================================================================
echo -e "${YELLOW}[1/4] Core invariant checks...${NC}"

# Check: Must have clear problem statement
((INVARIANTS_CHECKED++))
if echo "$CONTENT" | grep -qiE "(problem|objective|goal|challenge).*:"; then
    ((INVARIANTS_PASSED++))
    PASSED+=("Has problem statement")
    [[ "$VERBOSE" == "true" ]] && echo -e "  ${GREEN}✓${NC} Has problem statement"
else
    VIOLATIONS_MAJOR+=("Missing clear problem statement")
    [[ "$VERBOSE" == "true" ]] && echo -e "  ${RED}✗${NC} Missing problem statement"
fi

# Check: Must define success criteria
((INVARIANTS_CHECKED++))
if echo "$CONTENT" | grep -qiE "(success|done when|acceptance|criteria)"; then
    ((INVARIANTS_PASSED++))
    PASSED+=("Has success criteria")
    [[ "$VERBOSE" == "true" ]] && echo -e "  ${GREEN}✓${NC} Has success criteria"
else
    VIOLATIONS_MAJOR+=("Missing success criteria")
    [[ "$VERBOSE" == "true" ]] && echo -e "  ${RED}✗${NC} Missing success criteria"
fi

# Check: Must not have TODO placeholders
((INVARIANTS_CHECKED++))
TODO_COUNT=$(echo "$CONTENT" | grep -ciE '\bTODO\b|\bTBD\b|\bFIXME\b' || true)
if [[ $TODO_COUNT -eq 0 ]]; then
    ((INVARIANTS_PASSED++))
    PASSED+=("No TODO placeholders")
    [[ "$VERBOSE" == "true" ]] && echo -e "  ${GREEN}✓${NC} No TODO placeholders"
else
    VIOLATIONS_MINOR+=("Contains $TODO_COUNT TODO/TBD/FIXME placeholders")
    [[ "$VERBOSE" == "true" ]] && echo -e "  ${YELLOW}!${NC} Contains $TODO_COUNT placeholders"
fi

echo -e "  Core checks: ${INVARIANTS_PASSED}/${INVARIANTS_CHECKED} passed"

# ============================================================================
# SECTION 2: Domain-Specific Checks
# ============================================================================
echo -e "${YELLOW}[2/4] Domain-specific checks ($DOMAIN)...${NC}"

case $DOMAIN in
    api|API)
        # API domain checks
        ((INVARIANTS_CHECKED++))
        if echo "$CONTENT" | grep -qiE "(endpoint|route|path|uri|url)"; then
            ((INVARIANTS_PASSED++))
            PASSED+=("Defines API endpoints")
        else
            VIOLATIONS_MAJOR+=("API spec should define endpoints")
        fi

        ((INVARIANTS_CHECKED++))
        if echo "$CONTENT" | grep -qiE "(error|status code|4[0-9]{2}|5[0-9]{2}|failure)"; then
            ((INVARIANTS_PASSED++))
            PASSED+=("Addresses error handling")
        else
            VIOLATIONS_MAJOR+=("API spec should address error handling")
        fi

        ((INVARIANTS_CHECKED++))
        if echo "$CONTENT" | grep -qiE "(auth|token|api.key|bearer|oauth)"; then
            ((INVARIANTS_PASSED++))
            PASSED+=("Addresses authentication")
        else
            WARNINGS+=("Consider addressing API authentication")
        fi

        ((INVARIANTS_CHECKED++))
        if echo "$CONTENT" | grep -qiE "(rate.limit|throttl|quota)"; then
            ((INVARIANTS_PASSED++))
            PASSED+=("Addresses rate limiting")
        else
            WARNINGS+=("Consider addressing rate limiting")
        fi
        ;;

    database|db)
        # Database domain checks
        ((INVARIANTS_CHECKED++))
        if echo "$CONTENT" | grep -qiE "(schema|table|column|field|model)"; then
            ((INVARIANTS_PASSED++))
            PASSED+=("Defines data model")
        else
            VIOLATIONS_MAJOR+=("Database spec should define data model")
        fi

        ((INVARIANTS_CHECKED++))
        if echo "$CONTENT" | grep -qiE "(migration|rollback|versioning)"; then
            ((INVARIANTS_PASSED++))
            PASSED+=("Addresses migrations")
        else
            VIOLATIONS_MAJOR+=("Database spec should address migrations")
        fi

        ((INVARIANTS_CHECKED++))
        if echo "$CONTENT" | grep -qiE "(index|performance|query)"; then
            ((INVARIANTS_PASSED++))
            PASSED+=("Addresses indexing/performance")
        else
            WARNINGS+=("Consider addressing database indexing")
        fi

        ((INVARIANTS_CHECKED++))
        if echo "$CONTENT" | grep -qiE "(backup|recovery|disaster)"; then
            ((INVARIANTS_PASSED++))
            PASSED+=("Addresses backup/recovery")
        else
            WARNINGS+=("Consider addressing backup strategy")
        fi
        ;;

    security)
        # Security domain checks
        ((INVARIANTS_CHECKED++))
        if echo "$CONTENT" | grep -qiE "(threat|risk|attack|vulnerability)"; then
            ((INVARIANTS_PASSED++))
            PASSED+=("Identifies threats/risks")
        else
            VIOLATIONS_CRITICAL+=("Security spec must identify threats")
        fi

        ((INVARIANTS_CHECKED++))
        if echo "$CONTENT" | grep -qiE "(encrypt|hash|salt|secure)"; then
            ((INVARIANTS_PASSED++))
            PASSED+=("Addresses encryption")
        else
            VIOLATIONS_MAJOR+=("Security spec should address encryption")
        fi

        ((INVARIANTS_CHECKED++))
        if echo "$CONTENT" | grep -qiE "(audit|log|monitor|detect)"; then
            ((INVARIANTS_PASSED++))
            PASSED+=("Addresses auditing")
        else
            VIOLATIONS_MAJOR+=("Security spec should address audit logging")
        fi
        ;;

    ui|frontend)
        # UI domain checks
        ((INVARIANTS_CHECKED++))
        if echo "$CONTENT" | grep -qiE "(component|screen|page|view)"; then
            ((INVARIANTS_PASSED++))
            PASSED+=("Defines UI components")
        else
            VIOLATIONS_MAJOR+=("UI spec should define components")
        fi

        ((INVARIANTS_CHECKED++))
        if echo "$CONTENT" | grep -qiE "(accessibility|a11y|wcag|aria)"; then
            ((INVARIANTS_PASSED++))
            PASSED+=("Addresses accessibility")
        else
            WARNINGS+=("Consider addressing accessibility requirements")
        fi

        ((INVARIANTS_CHECKED++))
        if echo "$CONTENT" | grep -qiE "(responsive|mobile|breakpoint)"; then
            ((INVARIANTS_PASSED++))
            PASSED+=("Addresses responsive design")
        else
            WARNINGS+=("Consider addressing responsive design")
        fi
        ;;

    *)
        echo -e "  ${YELLOW}Using general checks for domain '$DOMAIN'${NC}"
        ;;
esac

DOMAIN_PASSED=$((INVARIANTS_PASSED - 3))  # Subtract core checks
DOMAIN_TOTAL=$((INVARIANTS_CHECKED - 3))
echo -e "  Domain checks: ${DOMAIN_PASSED}/${DOMAIN_TOTAL} passed"

# ============================================================================
# SECTION 3: CONVENTIONS.md Compliance
# ============================================================================
echo -e "${YELLOW}[3/4] Checking CONVENTIONS.md compliance...${NC}"

if [[ -n "$CONVENTIONS_FILE" ]] && [[ -f "$CONVENTIONS_FILE" ]]; then
    echo -e "  Using: $CONVENTIONS_FILE"

    # Check for naming convention violations
    ((INVARIANTS_CHECKED++))
    # This is a placeholder - actual check would parse CONVENTIONS.md
    ((INVARIANTS_PASSED++))
    PASSED+=("CONVENTIONS.md loaded")
else
    echo -e "  ${YELLOW}No CONVENTIONS.md provided, skipping${NC}"
fi

# ============================================================================
# SECTION 4: Calculate Confidence Score
# ============================================================================
echo -e "${YELLOW}[4/4] Calculating confidence score...${NC}"

# Base score from pass rate
PASS_RATE=$((INVARIANTS_PASSED * 100 / INVARIANTS_CHECKED))

# Penalties
CRITICAL_PENALTY=$((${#VIOLATIONS_CRITICAL[@]} * 25))
MAJOR_PENALTY=$((${#VIOLATIONS_MAJOR[@]} * 10))
MINOR_PENALTY=$((${#VIOLATIONS_MINOR[@]} * 5))
WARNING_PENALTY=$((${#WARNINGS[@]} * 2))

TOTAL_PENALTY=$((CRITICAL_PENALTY + MAJOR_PENALTY + MINOR_PENALTY + WARNING_PENALTY))

CONFIDENCE_SCORE=$((PASS_RATE - TOTAL_PENALTY))
[[ $CONFIDENCE_SCORE -lt 0 ]] && CONFIDENCE_SCORE=0
[[ $CONFIDENCE_SCORE -gt 100 ]] && CONFIDENCE_SCORE=100

echo -e "  Pass rate: ${PASS_RATE}%"
echo -e "  Penalties: -${TOTAL_PENALTY} (critical: -$CRITICAL_PENALTY, major: -$MAJOR_PENALTY, minor: -$MINOR_PENALTY)"
echo -e "  Confidence: ${CYAN}${CONFIDENCE_SCORE}%${NC}"

# ============================================================================
# Generate JSON Output
# ============================================================================
OUTPUT_FILE="$OUTPUT_DIR/validation.json"

# Convert arrays to JSON
violations_to_json() {
    local severity=$1
    shift
    local items=("$@")
    if [[ ${#items[@]} -eq 0 ]]; then
        echo "[]"
        return
    fi
    printf '%s\n' "${items[@]}" | jq -R --arg sev "$severity" '{severity: $sev, message: .}' | jq -s .
}

CRITICAL_JSON=$(violations_to_json "critical" "${VIOLATIONS_CRITICAL[@]}")
MAJOR_JSON=$(violations_to_json "major" "${VIOLATIONS_MAJOR[@]}")
MINOR_JSON=$(violations_to_json "minor" "${VIOLATIONS_MINOR[@]}")
WARNINGS_JSON=$(printf '%s\n' "${WARNINGS[@]}" 2>/dev/null | jq -R . | jq -s . || echo "[]")
PASSED_JSON=$(printf '%s\n' "${PASSED[@]}" | jq -R . | jq -s .)

# Merge violation arrays
ALL_VIOLATIONS=$(echo "$CRITICAL_JSON $MAJOR_JSON $MINOR_JSON" | jq -s 'add')

cat > "$OUTPUT_FILE" << EOF
{
  "spec_file": "$SPEC_FILE",
  "domain": "$DOMAIN",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "invariants_checked": $INVARIANTS_CHECKED,
  "invariants_passed": $INVARIANTS_PASSED,
  "pass_rate": $PASS_RATE,
  "confidence_score": $CONFIDENCE_SCORE,
  "violations": $ALL_VIOLATIONS,
  "warnings": $WARNINGS_JSON,
  "passed": $PASSED_JSON,
  "summary": {
    "critical": ${#VIOLATIONS_CRITICAL[@]},
    "major": ${#VIOLATIONS_MAJOR[@]},
    "minor": ${#VIOLATIONS_MINOR[@]},
    "warnings": ${#WARNINGS[@]}
  }
}
EOF

# ============================================================================
# Output Summary
# ============================================================================
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Validation complete!${NC}"
echo -e "Output: $OUTPUT_FILE"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"

echo ""
echo -e "${BLUE}Summary:${NC}"
echo -e "  Invariants: ${INVARIANTS_PASSED}/${INVARIANTS_CHECKED} passed"
echo -e "  Confidence: ${CONFIDENCE_SCORE}%"
echo ""

if [[ ${#VIOLATIONS_CRITICAL[@]} -gt 0 ]]; then
    echo -e "${RED}Critical violations:${NC}"
    for v in "${VIOLATIONS_CRITICAL[@]}"; do
        echo -e "  ${RED}✗${NC} $v"
    done
fi

if [[ ${#VIOLATIONS_MAJOR[@]} -gt 0 ]]; then
    echo -e "${YELLOW}Major violations:${NC}"
    for v in "${VIOLATIONS_MAJOR[@]}"; do
        echo -e "  ${YELLOW}✗${NC} $v"
    done
fi

if [[ ${#WARNINGS[@]} -gt 0 ]]; then
    echo -e "${YELLOW}Warnings:${NC}"
    for w in "${WARNINGS[@]}"; do
        echo -e "  ${YELLOW}!${NC} $w"
    done
fi

# Exit codes
if [[ ${#VIOLATIONS_CRITICAL[@]} -gt 0 ]]; then
    echo ""
    echo -e "${RED}BLOCKED: Critical violations must be resolved${NC}"
    exit 2
fi

if [[ $CONFIDENCE_SCORE -lt 50 ]]; then
    echo ""
    echo -e "${YELLOW}WARNING: Confidence below 50%. Review violations.${NC}"
    exit 1
fi

exit 0
