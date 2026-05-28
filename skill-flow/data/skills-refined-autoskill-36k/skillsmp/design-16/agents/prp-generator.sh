#!/bin/bash
#
# prp-generator.sh - Generate PRP from validated spec
#
# Usage: ./agents/prp-generator.sh <spec-file> --analysis <file> --validation <file> [--output <dir>]
#
# Outputs:
#   - prp-draft.md following the PRP template

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
TEMPLATE_DIR="$DESIGN_OPS_ROOT/templates"

# Defaults
SPEC_FILE=""
ANALYSIS_FILE=""
VALIDATION_FILE=""
OUTPUT_DIR="."
TEMPLATE_FILE="$TEMPLATE_DIR/prp-base.md"
PROJECT_NAME=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --analysis)
            ANALYSIS_FILE="$2"
            shift 2
            ;;
        --validation)
            VALIDATION_FILE="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --template)
            TEMPLATE_FILE="$2"
            shift 2
            ;;
        --name)
            PROJECT_NAME="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 <spec-file> --analysis <file> --validation <file> [options]"
            echo ""
            echo "Options:"
            echo "  --analysis <file>     Analysis JSON from spec-analyst"
            echo "  --validation <file>   Validation JSON from validator"
            echo "  --output <dir>        Output directory"
            echo "  --template <file>     PRP template to use"
            echo "  --name <name>         Project name (auto-detected if not provided)"
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

# Validate inputs
if [[ -z "$SPEC_FILE" ]] || [[ ! -f "$SPEC_FILE" ]]; then
    echo -e "${RED}Error: Valid spec file required${NC}"
    exit 1
fi

if [[ -z "$ANALYSIS_FILE" ]] || [[ ! -f "$ANALYSIS_FILE" ]]; then
    echo -e "${RED}Error: Analysis file required (--analysis)${NC}"
    exit 1
fi

if [[ -z "$VALIDATION_FILE" ]] || [[ ! -f "$VALIDATION_FILE" ]]; then
    echo -e "${RED}Error: Validation file required (--validation)${NC}"
    exit 1
fi

echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  PRP GENERATOR - Creating Implementation Plan${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Spec:${NC}       $SPEC_FILE"
echo -e "${BLUE}Analysis:${NC}   $ANALYSIS_FILE"
echo -e "${BLUE}Validation:${NC} $VALIDATION_FILE"
echo ""

# ============================================================================
# Load Inputs
# ============================================================================
SPEC_CONTENT=$(cat "$SPEC_FILE")
ANALYSIS=$(cat "$ANALYSIS_FILE")
VALIDATION=$(cat "$VALIDATION_FILE")

# Extract key values from JSON
COMPLETENESS_SCORE=$(echo "$ANALYSIS" | jq -r '.completeness_score')
COMPLEXITY_SCORE=$(echo "$ANALYSIS" | jq -r '.complexity.score')
COMPLEXITY_FACTORS=$(echo "$ANALYSIS" | jq -r '.complexity.factors | join(", ")')
THINKING_LEVEL=$(echo "$ANALYSIS" | jq -r '.thinking_level.recommended')
THINKING_REASON=$(echo "$ANALYSIS" | jq -r '.thinking_level.reason')

CONFIDENCE_SCORE=$(echo "$VALIDATION" | jq -r '.confidence_score')
DOMAIN=$(echo "$VALIDATION" | jq -r '.domain')
INVARIANTS_PASSED=$(echo "$VALIDATION" | jq -r '.invariants_passed')
INVARIANTS_CHECKED=$(echo "$VALIDATION" | jq -r '.invariants_checked')

# Auto-detect project name from spec filename
if [[ -z "$PROJECT_NAME" ]]; then
    PROJECT_NAME=$(basename "$SPEC_FILE" | sed 's/\.[^.]*$//' | sed 's/-spec$//' | sed 's/_spec$//')
fi

echo -e "${GREEN}Loaded analysis and validation data${NC}"
echo -e "  Completeness: ${COMPLETENESS_SCORE}%"
echo -e "  Confidence: ${CONFIDENCE_SCORE}%"
echo -e "  Thinking level: $THINKING_LEVEL"

# ============================================================================
# Extract Requirements from Spec
# ============================================================================
echo -e "${YELLOW}[1/4] Extracting requirements...${NC}"

# Extract lines that look like requirements
REQUIREMENTS=$(echo "$SPEC_CONTENT" | grep -iE '^\s*[-*•]\s*(must|shall|should|will)' | head -20 || true)
if [[ -z "$REQUIREMENTS" ]]; then
    REQUIREMENTS=$(echo "$SPEC_CONTENT" | grep -iE '\bmust\b|\bshall\b' | head -10 || true)
fi

REQ_COUNT=$(echo "$REQUIREMENTS" | grep -c '.' || echo "0")
echo -e "  Found $REQ_COUNT requirement statements"

# ============================================================================
# Determine File Structure
# ============================================================================
echo -e "${YELLOW}[2/4] Determining file structure...${NC}"

# Look for file/path mentions in spec
FILES_MENTIONED=$(echo "$SPEC_CONTENT" | grep -oE '`[^`]+\.(ts|js|py|go|rs|java|rb|sh|md)`' | sort -u | head -15 || true)
FILE_COUNT=$(echo "$FILES_MENTIONED" | grep -c '.' || echo "0")

if [[ $FILE_COUNT -gt 0 ]]; then
    echo -e "  Found $FILE_COUNT files mentioned"
else
    echo -e "  No specific files mentioned in spec"
fi

# ============================================================================
# Build PRP Content
# ============================================================================
echo -e "${YELLOW}[3/4] Generating PRP content...${NC}"

DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Determine patterns to reference based on domain
PATTERNS=""
case $DOMAIN in
    api|API)
        PATTERNS="- [API Client Pattern](../examples/api-client.md)
- [Error Handling Pattern](../examples/error-handling.md)"
        ;;
    database|db)
        PATTERNS="- [Database Patterns](../examples/database-patterns.md)
- [Config Loading](../examples/config-loading.md)"
        ;;
    security)
        PATTERNS="- [Error Handling Pattern](../examples/error-handling.md)
- [Config Loading](../examples/config-loading.md)"
        ;;
    *)
        PATTERNS="- [Error Handling Pattern](../examples/error-handling.md)
- [Test Fixtures](../examples/test-fixtures.md)"
        ;;
esac

# Map thinking level to display
THINKING_DISPLAY=""
case $THINKING_LEVEL in
    normal)     THINKING_DISPLAY="Normal" ;;
    think)      THINKING_DISPLAY="Think" ;;
    think_hard) THINKING_DISPLAY="Think Hard" ;;
    ultrathink) THINKING_DISPLAY="Ultrathink" ;;
    *)          THINKING_DISPLAY="Normal" ;;
esac

# ============================================================================
# Generate PRP File
# ============================================================================
OUTPUT_FILE="$OUTPUT_DIR/prp-${PROJECT_NAME}.md"

cat > "$OUTPUT_FILE" << EOF
# PRP: ${PROJECT_NAME}

> Implementation plan generated from spec analysis

| Field | Value |
|-------|-------|
| Status | Draft |
| Confidence | ${CONFIDENCE_SCORE}% |
| Thinking Level | ${THINKING_DISPLAY} |
| Domain | ${DOMAIN} |
| Created | ${DATE} |

---

## 1. Context

### 1.1 Problem Statement

<!-- Extracted from spec - review and refine -->
$(echo "$SPEC_CONTENT" | grep -A5 -iE "^#.*problem|^#.*objective|^#.*goal" | head -10 || echo "See original spec for problem statement.")

### 1.2 Source Spec

- **File**: \`$SPEC_FILE\`
- **Completeness**: ${COMPLETENESS_SCORE}%
- **Analysis**: \`$ANALYSIS_FILE\`
- **Validation**: \`$VALIDATION_FILE\`

### 1.3 Relevant Patterns

$PATTERNS

---

## 2. Validation Summary

### 2.1 Invariant Compliance

- **Checked**: $INVARIANTS_CHECKED invariants
- **Passed**: $INVARIANTS_PASSED invariants
- **Pass Rate**: $((INVARIANTS_PASSED * 100 / INVARIANTS_CHECKED))%

### 2.2 Confidence Score Breakdown

| Factor | Value | Impact |
|--------|-------|--------|
| Invariant pass rate | $((INVARIANTS_PASSED * 100 / INVARIANTS_CHECKED))% | Base |
| Spec completeness | ${COMPLETENESS_SCORE}% | +/- adjustment |
| Complexity factors | ${COMPLEXITY_SCORE} | Risk factor |

**Final Confidence**: ${CONFIDENCE_SCORE}%

### 2.3 Warnings/Violations

$(echo "$VALIDATION" | jq -r '.violations[]? | "- **\(.severity)**: \(.message)"' 2>/dev/null || echo "None detected")

$(echo "$VALIDATION" | jq -r '.warnings[]? | "- ⚠️ \(.)"' 2>/dev/null || echo "")

---

## 3. Requirements

### 3.1 Extracted Requirements

$( if [[ -n "$REQUIREMENTS" ]]; then echo "$REQUIREMENTS"; else echo "<!-- No explicit requirements extracted - review spec manually -->"; fi )

### 3.2 Acceptance Criteria

<!-- Define specific, testable acceptance criteria -->

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

---

## 4. Scope

### 4.1 In Scope

<!-- List what this implementation covers -->

- Item 1
- Item 2

### 4.2 Out of Scope

<!-- Explicitly list what is NOT covered -->

- Item 1
- Item 2

### 4.3 Dependencies

<!-- External dependencies, prerequisites -->

- None identified

---

## 5. Implementation Plan

### 5.1 Files to Modify/Create

$( if [[ -n "$FILES_MENTIONED" ]]; then
    echo "| File | Action | Description |"
    echo "|------|--------|-------------|"
    echo "$FILES_MENTIONED" | while read -r f; do
        f_clean=$(echo "$f" | tr -d '`')
        echo "| \`$f_clean\` | TBD | <!-- Description --> |"
    done
else
    echo "| File | Action | Description |"
    echo "|------|--------|-------------|"
    echo "| \`TBD\` | Create/Modify | <!-- Add files --> |"
fi )

### 5.2 Implementation Steps

1. **Step 1**: <!-- Description -->
2. **Step 2**: <!-- Description -->
3. **Step 3**: <!-- Description -->

### 5.3 Rollback Plan

<!-- How to revert if issues arise -->

1. Revert commits
2. Restore database (if applicable)
3. Notify stakeholders

---

## 6. Testing Strategy

### 6.1 Unit Tests

- [ ] Test case 1
- [ ] Test case 2

### 6.2 Integration Tests

- [ ] Integration test 1

### 6.3 Manual Testing

- [ ] Manual verification step

---

## 7. Risk Assessment

### 7.1 Identified Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| <!-- Risk 1 --> | Medium | High | <!-- Mitigation --> |

### 7.2 Complexity Factors

$(if [[ -n "$COMPLEXITY_FACTORS" ]]; then
    echo "Detected complexity factors: **${COMPLEXITY_FACTORS}**"
else
    echo "No significant complexity factors detected."
fi)

---

## 8. Validation Commands

### 8.1 Test Commands

\`\`\`bash
# Run tests
npm test
# or
pytest tests/
\`\`\`

### 8.2 Code Quality

\`\`\`bash
# Lint
npm run lint
# or
ruff check .
\`\`\`

### 8.3 Integration Check

\`\`\`bash
# Health check
curl -s http://localhost:3000/health | jq .
\`\`\`

### 8.4 Build Verification

\`\`\`bash
# Build
npm run build
# or
go build ./...
\`\`\`

---

## 9. Recommended Thinking Level

| Factor | Assessment |
|--------|------------|
| Complexity score | ${COMPLEXITY_SCORE} |
| Complexity factors | ${COMPLEXITY_FACTORS:-"None"} |
| Invariants checked | ${INVARIANTS_CHECKED} |
| Confidence score | ${CONFIDENCE_SCORE}% |

**Recommendation**: **${THINKING_DISPLAY}**

**Rationale**: ${THINKING_REASON}

---

## 10. State Transitions

| State | Entry Criteria | Exit Criteria |
|-------|---------------|---------------|
| Draft | PRP created | Review complete |
| In Review | Draft complete | Approved/Rejected |
| Approved | Review passed | Implementation started |
| In Progress | Approved | Tests passing |
| Complete | All tests pass | Deployed |

**Current State**: Draft

---

## 11. Execution Log

| Date | Action | Notes |
|------|--------|-------|
| ${DATE} | PRP generated | From spec-analyst and validator output |

---

## Appendix A: Generation Metadata

\`\`\`json
{
  "generator": "prp-generator.sh",
  "version": "1.0.0",
  "timestamp": "${TIMESTAMP}",
  "inputs": {
    "spec": "$SPEC_FILE",
    "analysis": "$ANALYSIS_FILE",
    "validation": "$VALIDATION_FILE"
  }
}
\`\`\`
EOF

# ============================================================================
# Output Summary
# ============================================================================
echo -e "${YELLOW}[4/4] Finalizing...${NC}"

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}PRP generated successfully!${NC}"
echo -e "Output: $OUTPUT_FILE"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"

echo ""
echo -e "${BLUE}Summary:${NC}"
echo -e "  Project:     $PROJECT_NAME"
echo -e "  Confidence:  ${CONFIDENCE_SCORE}%"
echo -e "  Thinking:    $THINKING_DISPLAY"
echo -e "  Domain:      $DOMAIN"

echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Review and refine generated PRP"
echo -e "  2. Fill in placeholder sections"
echo -e "  3. Run: ./agents/reviewer.sh $OUTPUT_FILE"

exit 0
