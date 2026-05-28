#!/bin/bash
# confidence-calculator.sh - Calculate confidence scores for specs and PRPs
#
# Calculates weighted confidence score based on 5 factors:
#   - Requirement Clarity (30%)
#   - Pattern Availability (25%)
#   - Test Coverage Plan (20%)
#   - Edge Case Handling (15%)
#   - Tech Familiarity (10%)
#
# Usage:
#   ./confidence-calculator.sh <clarity> <patterns> <tests> <edges> <tech>
#
# Parameters (each 0.0 to 1.0):
#   clarity   - Requirement clarity score
#   patterns  - Pattern availability score
#   tests     - Test coverage plan score
#   edges     - Edge case handling score
#   tech      - Tech familiarity score
#
# Output:
#   - Weighted confidence score (1-10)
#   - Risk level (Low/Medium/High/Perfect)
#   - Recommendation (STOP/CAUTION/PROCEED)
#
# Examples:
#   ./confidence-calculator.sh 0.8 0.7 0.7 0.6 0.8
#   # Output: Confidence Score: 7.2 (High/Green) - PROCEED
#
#   ./confidence-calculator.sh 0.4 0.3 0.2 0.2 0.7
#   # Output: Confidence Score: 3.5 (Low/Red) - STOP
#
#   ./confidence-calculator.sh --interactive
#   # Prompts for each score with guidance

set -e

# ============================================================================
# Dependency Check
# ============================================================================

# Check for bc (required for floating point math)
if ! command -v bc &> /dev/null; then
    echo "ERROR: 'bc' is required but not installed." >&2
    echo "" >&2
    echo "Install it with:" >&2
    echo "  macOS:        brew install bc" >&2
    echo "  Ubuntu/Debian: sudo apt-get install bc" >&2
    echo "  RHEL/CentOS:   sudo yum install bc" >&2
    echo "  Alpine:        apk add bc" >&2
    exit 1
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Weights (must sum to 1.0)
WEIGHT_CLARITY=0.30
WEIGHT_PATTERNS=0.25
WEIGHT_TESTS=0.20
WEIGHT_EDGES=0.15
WEIGHT_TECH=0.10

# Version
VERSION="1.0.0"

# Usage function
usage() {
    echo "Usage: $0 <clarity> <patterns> <tests> <edges> <tech>"
    echo "       $0 --interactive"
    echo "       $0 --json <clarity> <patterns> <tests> <edges> <tech>"
    echo ""
    echo "Parameters (each 0.0 to 1.0):"
    echo "  clarity    Requirement clarity score"
    echo "  patterns   Pattern availability score"
    echo "  tests      Test coverage plan score"
    echo "  edges      Edge case handling score"
    echo "  tech       Tech familiarity score"
    echo ""
    echo "Options:"
    echo "  --interactive   Prompt for each score with guidance"
    echo "  --json          Output result as JSON"
    echo "  --verbose       Show weighted breakdown"
    echo "  --version       Show version"
    echo "  --help          Show this help"
    echo ""
    echo "Score Ranges:"
    echo "  1-3  (Low/Red)     - STOP: Address gaps before proceeding"
    echo "  4-6  (Medium/Yellow) - CAUTION: Proceed with risk mitigation"
    echo "  7-9  (High/Green)  - PROCEED: Normal execution path"
    echo "  10   (Perfect)     - PROCEED: Rare, verify nothing is missed"
    echo ""
    echo "Examples:"
    echo "  $0 0.8 0.7 0.7 0.6 0.8"
    echo "  $0 --interactive"
    echo "  $0 --json 0.5 0.5 0.5 0.5 0.5"
    exit 1
}

# Validate score is between 0.0 and 1.0
validate_score() {
    local score="$1"
    local name="$2"

    # Check if it's a valid number
    if ! [[ "$score" =~ ^[0-9]*\.?[0-9]+$ ]]; then
        echo -e "${RED}ERROR: Invalid $name score: '$score' (must be a number 0.0-1.0)${NC}" >&2
        exit 1
    fi

    # Check range using bc for floating point comparison
    local valid=$(echo "$score >= 0.0 && $score <= 1.0" | bc -l)
    if [[ "$valid" != "1" ]]; then
        echo -e "${RED}ERROR: $name score $score out of range (must be 0.0-1.0)${NC}" >&2
        exit 1
    fi
}

# Calculate confidence score
calculate_confidence() {
    local clarity="$1"
    local patterns="$2"
    local tests="$3"
    local edges="$4"
    local tech="$5"

    # Calculate weighted score
    local score=$(echo "scale=2; ($clarity * $WEIGHT_CLARITY + $patterns * $WEIGHT_PATTERNS + $tests * $WEIGHT_TESTS + $edges * $WEIGHT_EDGES + $tech * $WEIGHT_TECH) * 10" | bc -l)

    # Round to 1 decimal place
    score=$(printf "%.1f" "$score")

    echo "$score"
}

# Get risk level and color
get_risk_level() {
    local score="$1"
    local score_int=$(printf "%.0f" "$score")

    if (( $(echo "$score < 4" | bc -l) )); then
        echo "Low/Red"
    elif (( $(echo "$score < 7" | bc -l) )); then
        echo "Medium/Yellow"
    elif (( $(echo "$score < 10" | bc -l) )); then
        echo "High/Green"
    else
        echo "Perfect"
    fi
}

# Get recommendation
get_recommendation() {
    local score="$1"

    if (( $(echo "$score < 4" | bc -l) )); then
        echo "STOP"
    elif (( $(echo "$score < 7" | bc -l) )); then
        echo "CAUTION"
    else
        echo "PROCEED"
    fi
}

# Get recommendation details
get_recommendation_detail() {
    local score="$1"

    if (( $(echo "$score < 4" | bc -l) )); then
        echo "Address gaps before proceeding. Review requirements and patterns."
    elif (( $(echo "$score < 7" | bc -l) )); then
        echo "Proceed with explicit risk mitigation plan documented."
    elif (( $(echo "$score < 10" | bc -l) )); then
        echo "Normal execution path. Standard validation gates apply."
    else
        echo "Rare perfect score. Verify nothing is overlooked."
    fi
}

# Color output based on score
color_score() {
    local score="$1"

    if (( $(echo "$score < 4" | bc -l) )); then
        echo -e "${RED}$score${NC}"
    elif (( $(echo "$score < 7" | bc -l) )); then
        echo -e "${YELLOW}$score${NC}"
    else
        echo -e "${GREEN}$score${NC}"
    fi
}

# Interactive mode
run_interactive() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Confidence Score Calculator - Interactive Mode${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Rate each factor from 0.0 (lowest) to 1.0 (highest)"
    echo ""

    # Requirement Clarity
    echo -e "${CYAN}1. Requirement Clarity (30% weight)${NC}"
    echo "   0.1-0.3: Vague or missing requirements"
    echo "   0.4-0.5: Partial requirements with gaps"
    echo "   0.6-0.7: Complete but some ambiguity"
    echo "   0.8-0.9: Clear, measurable requirements"
    echo "   1.0:     Unambiguous, testable, complete"
    echo -n "   Score: "
    read -r clarity
    validate_score "$clarity" "clarity"
    echo ""

    # Pattern Availability
    echo -e "${CYAN}2. Pattern Availability (25% weight)${NC}"
    echo "   0.1-0.3: No patterns exist, greenfield"
    echo "   0.4-0.5: Partial patterns available"
    echo "   0.6-0.7: Good patterns with adaptation needed"
    echo "   0.8-0.9: Strong patterns, minor customization"
    echo "   1.0:     Exact pattern match"
    echo -n "   Score: "
    read -r patterns
    validate_score "$patterns" "patterns"
    echo ""

    # Test Coverage Plan
    echo -e "${CYAN}3. Test Coverage Plan (20% weight)${NC}"
    echo "   0.1-0.3: No test plan"
    echo "   0.4-0.5: Incomplete test plan"
    echo "   0.6-0.7: Good coverage with gaps"
    echo "   0.8-0.9: Comprehensive test plan"
    echo "   1.0:     TDD-ready with full coverage"
    echo -n "   Score: "
    read -r tests
    validate_score "$tests" "tests"
    echo ""

    # Edge Case Handling
    echo -e "${CYAN}4. Edge Case Handling (15% weight)${NC}"
    echo "   0.1-0.3: No edge cases identified"
    echo "   0.4-0.5: Some edge cases noted"
    echo "   0.6-0.7: Edge cases identified with partial mitigation"
    echo "   0.8-0.9: Comprehensive edge case handling"
    echo "   1.0:     Edge cases tested and validated"
    echo -n "   Score: "
    read -r edges
    validate_score "$edges" "edges"
    echo ""

    # Tech Familiarity
    echo -e "${CYAN}5. Tech Familiarity (10% weight)${NC}"
    echo "   0.1-0.3: Completely new technology"
    echo "   0.4-0.5: Limited exposure"
    echo "   0.6-0.7: Moderate experience"
    echo "   0.8-0.9: Strong experience"
    echo "   1.0:     Deep expertise"
    echo -n "   Score: "
    read -r tech
    validate_score "$tech" "tech"
    echo ""

    # Calculate and display
    CLARITY="$clarity"
    PATTERNS="$patterns"
    TESTS="$tests"
    EDGES="$edges"
    TECH="$tech"
    VERBOSE=true
}

# Parse arguments
INTERACTIVE=false
JSON_OUTPUT=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --interactive|-i)
            INTERACTIVE=true
            shift
            ;;
        --json|-j)
            JSON_OUTPUT=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --version)
            echo "confidence-calculator.sh version $VERSION"
            exit 0
            ;;
        --help|-h)
            usage
            ;;
        *)
            break
            ;;
    esac
done

# Get scores
if [[ "$INTERACTIVE" == "true" ]]; then
    run_interactive
else
    # Check argument count
    if [[ $# -ne 5 ]]; then
        echo -e "${RED}ERROR: Expected 5 scores, got $#${NC}" >&2
        usage
    fi

    CLARITY="$1"
    PATTERNS="$2"
    TESTS="$3"
    EDGES="$4"
    TECH="$5"

    # Validate all scores
    validate_score "$CLARITY" "clarity"
    validate_score "$PATTERNS" "patterns"
    validate_score "$TESTS" "tests"
    validate_score "$EDGES" "edges"
    validate_score "$TECH" "tech"
fi

# Calculate
SCORE=$(calculate_confidence "$CLARITY" "$PATTERNS" "$TESTS" "$EDGES" "$TECH")
RISK_LEVEL=$(get_risk_level "$SCORE")
RECOMMENDATION=$(get_recommendation "$SCORE")
DETAIL=$(get_recommendation_detail "$SCORE")

# Calculate weighted contributions
CLARITY_CONTRIB=$(echo "scale=2; $CLARITY * $WEIGHT_CLARITY * 10" | bc -l)
PATTERNS_CONTRIB=$(echo "scale=2; $PATTERNS * $WEIGHT_PATTERNS * 10" | bc -l)
TESTS_CONTRIB=$(echo "scale=2; $TESTS * $WEIGHT_TESTS * 10" | bc -l)
EDGES_CONTRIB=$(echo "scale=2; $EDGES * $WEIGHT_EDGES * 10" | bc -l)
TECH_CONTRIB=$(echo "scale=2; $TECH * $WEIGHT_TECH * 10" | bc -l)

# Output
if [[ "$JSON_OUTPUT" == "true" ]]; then
    cat << EOF
{
  "confidence_score": $SCORE,
  "risk_level": "$RISK_LEVEL",
  "recommendation": "$RECOMMENDATION",
  "detail": "$DETAIL",
  "breakdown": {
    "requirement_clarity": {
      "raw": $CLARITY,
      "weight": $WEIGHT_CLARITY,
      "contribution": $CLARITY_CONTRIB
    },
    "pattern_availability": {
      "raw": $PATTERNS,
      "weight": $WEIGHT_PATTERNS,
      "contribution": $PATTERNS_CONTRIB
    },
    "test_coverage_plan": {
      "raw": $TESTS,
      "weight": $WEIGHT_TESTS,
      "contribution": $TESTS_CONTRIB
    },
    "edge_case_handling": {
      "raw": $EDGES,
      "weight": $WEIGHT_EDGES,
      "contribution": $EDGES_CONTRIB
    },
    "tech_familiarity": {
      "raw": $TECH,
      "weight": $WEIGHT_TECH,
      "contribution": $TECH_CONTRIB
    }
  }
}
EOF
else
    # Standard output
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Confidence Score Result${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo ""

    # Score with color
    COLORED_SCORE=$(color_score "$SCORE")
    echo -e "  Confidence Score: $COLORED_SCORE / 10"
    echo -e "  Risk Level: $RISK_LEVEL"
    echo -e "  Recommendation: ${CYAN}$RECOMMENDATION${NC}"
    echo ""
    echo -e "  ${DETAIL}"
    echo ""

    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}Weighted Breakdown:${NC}"
        echo ""
        printf "  %-22s %5s x %-5s = %5s\n" "Requirement Clarity" "$CLARITY" "0.30" "$CLARITY_CONTRIB"
        printf "  %-22s %5s x %-5s = %5s\n" "Pattern Availability" "$PATTERNS" "0.25" "$PATTERNS_CONTRIB"
        printf "  %-22s %5s x %-5s = %5s\n" "Test Coverage Plan" "$TESTS" "0.20" "$TESTS_CONTRIB"
        printf "  %-22s %5s x %-5s = %5s\n" "Edge Case Handling" "$EDGES" "0.15" "$EDGES_CONTRIB"
        printf "  %-22s %5s x %-5s = %5s\n" "Tech Familiarity" "$TECH" "0.10" "$TECH_CONTRIB"
        echo "  ─────────────────────────────────────────"
        printf "  %-22s %17s %5s\n" "TOTAL" "" "$SCORE"
        echo ""
    fi

    # Actionable suggestions for low scores
    if (( $(echo "$SCORE < 7" | bc -l) )); then
        echo -e "${YELLOW}Improvement Suggestions:${NC}"

        if (( $(echo "$CLARITY < 0.7" | bc -l) )); then
            echo "  - Requirement Clarity: Define metrics and acceptance criteria"
        fi
        if (( $(echo "$PATTERNS < 0.7" | bc -l) )); then
            echo "  - Pattern Availability: Find reference implementations"
        fi
        if (( $(echo "$TESTS < 0.7" | bc -l) )); then
            echo "  - Test Coverage: Write test cases before implementation"
        fi
        if (( $(echo "$EDGES < 0.7" | bc -l) )); then
            echo "  - Edge Cases: Conduct pre-mortem analysis"
        fi
        if (( $(echo "$TECH < 0.7" | bc -l) )); then
            echo "  - Tech Familiarity: Identify experts, allocate learning time"
        fi
        echo ""
    fi
fi

# Exit with code based on recommendation
case "$RECOMMENDATION" in
    "STOP")
        exit 2
        ;;
    "CAUTION")
        exit 1
        ;;
    "PROCEED")
        exit 0
        ;;
esac
