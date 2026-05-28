#!/bin/bash
# spec-to-prp.sh - Generate PRP from validated spec
#
# Automates PRP generation by:
# 1. Validating the spec first
# 2. Extracting project information
# 3. Loading appropriate template
# 4. Substituting variables
# 5. Running quality check on output

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
VALIDATOR="$SCRIPT_DIR/validator.sh"
PRP_CHECKER="$SCRIPT_DIR/prp-checker.sh"
TEMPLATES_DIR="$SCRIPT_DIR/../templates"
OUTPUT_DIR="$SCRIPT_DIR/../output"

# Default values
TEMPLATE="base"
DOMAIN=""
INTERACTIVE=false
SKIP_VALIDATION=false

# Usage
usage() {
    echo "Usage: $0 <spec-file.md> [options]"
    echo ""
    echo "Options:"
    echo "  --template <name>    Template to use: base, api-integration, user-feature, data-migration"
    echo "  --domain <file>      Domain file for validation"
    echo "  --output <file>      Output file path (default: output/<spec-name>-prp.md)"
    echo "  --interactive        Ask for missing information interactively"
    echo "  --skip-validation    Skip spec validation (use if already validated)"
    echo ""
    echo "Templates:"
    echo "  base            - Generic PRP template"
    echo "  api-integration - Technical API/integration projects"
    echo "  user-feature    - Consumer-facing features"
    echo "  data-migration  - Database/data infrastructure projects"
    echo ""
    echo "Example:"
    echo "  $0 specs/my-feature.md --template user-feature"
    echo "  $0 specs/api-spec.md --template api-integration --domain domains/integration.md"
    exit 1
}

# Check arguments
if [[ $# -lt 1 ]]; then
    usage
fi

SPEC_FILE="$1"
shift

# Parse options
while [[ $# -gt 0 ]]; do
    case "$1" in
        --template)
            TEMPLATE="$2"
            shift 2
            ;;
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --interactive)
            INTERACTIVE=true
            shift
            ;;
        --skip-validation)
            SKIP_VALIDATION=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# Validate spec file exists
if [[ ! -f "$SPEC_FILE" ]]; then
    echo -e "${RED}ERROR: Spec file not found: $SPEC_FILE${NC}"
    exit 1
fi

# Get spec filename for output
SPEC_BASENAME=$(basename "$SPEC_FILE" .md)

# Set default output if not specified
if [[ -z "$OUTPUT_FILE" ]]; then
    mkdir -p "$OUTPUT_DIR"
    OUTPUT_FILE="$OUTPUT_DIR/${SPEC_BASENAME}-prp.md"
fi

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Spec-to-PRP Generator${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

# ============================================================================
# Step 1: Validate Spec
# ============================================================================

echo -e "${BLUE}📄 Reading spec:${NC} $SPEC_FILE"

if [[ "$SKIP_VALIDATION" == "false" ]]; then
    echo -e "${BLUE}🔍 Validating spec...${NC}"

    # Build validator args as array to handle paths with spaces
    VALIDATOR_ARGS=()
    if [[ -n "$DOMAIN" ]]; then
        VALIDATOR_ARGS+=(--domain "$DOMAIN")
    fi

    # Run validator
    VALIDATION_OUTPUT=$("$VALIDATOR" "$SPEC_FILE" "${VALIDATOR_ARGS[@]}" 2>&1) || VALIDATION_EXIT=$?

    # Check for violations
    VIOLATIONS=$(echo "$VALIDATION_OUTPUT" | grep -c "❌ VIOLATION" 2>/dev/null || true)
    VIOLATIONS=${VIOLATIONS:-0}
    WARNINGS=$(echo "$VALIDATION_OUTPUT" | grep -c "⚠️  WARNING" 2>/dev/null || true)
    WARNINGS=${WARNINGS:-0}

    if [[ "$VIOLATIONS" -gt 0 ]]; then
        echo -e "${RED}❌ Spec has $VIOLATIONS violations. Cannot generate PRP.${NC}"
        echo ""
        echo "Validation output:"
        echo "$VALIDATION_OUTPUT" | head -30
        echo ""
        echo -e "${YELLOW}Fix spec violations before generating PRP.${NC}"
        exit 1
    fi

    if [[ "$WARNINGS" -gt 0 ]]; then
        echo -e "${GREEN}✅ Spec passed validation${NC} (${YELLOW}$WARNINGS warnings${NC})"
    else
        echo -e "${GREEN}✅ Spec passed validation${NC} (0 violations, 0 warnings)"
    fi
else
    echo -e "${YELLOW}⚠ Skipping validation (--skip-validation)${NC}"
fi

echo ""

# ============================================================================
# Step 2: Extract Project Information
# ============================================================================

echo -e "${BLUE}📋 Extracting project information...${NC}"

# Read spec content
SPEC_CONTENT=$(cat "$SPEC_FILE")

# Extract project name (from first heading or filename)
PROJECT_NAME=$(echo "$SPEC_CONTENT" | grep -m1 "^# " | sed 's/^# //' || echo "$SPEC_BASENAME")
PROJECT_NAME=${PROJECT_NAME:-$SPEC_BASENAME}

# Detect project type based on content
detect_project_type() {
    local content="$1"

    if echo "$content" | grep -qiE "API|integration|endpoint|webhook|third.party"; then
        echo "api-integration"
    elif echo "$content" | grep -qiE "database|migration|postgres|mysql|aurora|data.warehouse"; then
        echo "data-migration"
    elif echo "$content" | grep -qiE "user|feature|UI|UX|mobile|app|consumer"; then
        echo "user-feature"
    else
        echo "base"
    fi
}

DETECTED_TYPE=$(detect_project_type "$SPEC_CONTENT")

# Use detected type if template is base
if [[ "$TEMPLATE" == "base" ]]; then
    TEMPLATE="$DETECTED_TYPE"
    echo -e "   ${CYAN}Auto-detected project type: $TEMPLATE${NC}"
fi

# Extract timeline hints
TIMELINE=$(echo "$SPEC_CONTENT" | grep -oiE "[0-9]+ *(week|day|month|sprint)s?" | head -1 || echo "[FILL_TIMELINE]")

# Extract key requirements (lines starting with - or *)
REQUIREMENTS=$(echo "$SPEC_CONTENT" | grep -E "^[[:space:]]*[-*] " | head -10)

# Detect domain if not specified
if [[ -z "$DOMAIN" ]]; then
    DETECTED_DOMAIN="universal"
    if echo "$SPEC_CONTENT" | grep -qiE "consumer|user|mobile|app"; then
        DETECTED_DOMAIN="consumer"
    elif echo "$SPEC_CONTENT" | grep -qiE "database|migration|data|warehouse"; then
        DETECTED_DOMAIN="data-architecture"
    elif echo "$SPEC_CONTENT" | grep -qiE "API|integration|service|endpoint"; then
        DETECTED_DOMAIN="integration"
    elif echo "$SPEC_CONTENT" | grep -qiE "construction|build|physical|material"; then
        DETECTED_DOMAIN="physical-construction"
    fi
fi

echo "   Project: $PROJECT_NAME"
echo "   Type: $TEMPLATE"
echo "   Timeline hint: $TIMELINE"
echo ""

# ============================================================================
# Step 3: Load Template
# ============================================================================

echo -e "${BLUE}🔧 Loading template:${NC} $TEMPLATE"

# Map template name to file
# NOTE: All template types use prp-base.md with variable placeholders
# The example files in prp-examples/ are for reference only, not for templating
case "$TEMPLATE" in
    "base"|"api-integration"|"user-feature"|"data-migration")
        TEMPLATE_FILE="$TEMPLATES_DIR/prp-base.md"
        ;;
    *)
        echo -e "${RED}ERROR: Unknown template: $TEMPLATE${NC}"
        echo "Available templates: base, api-integration, user-feature, data-migration"
        exit 1
        ;;
esac

if [[ ! -f "$TEMPLATE_FILE" ]]; then
    echo -e "${RED}ERROR: Template file not found: $TEMPLATE_FILE${NC}"
    exit 1
fi

# Read template
TEMPLATE_CONTENT=$(cat "$TEMPLATE_FILE")

echo ""

# ============================================================================
# Step 4: Variable Substitution
# ============================================================================

echo -e "${BLUE}📝 Substituting variables...${NC}"

# Generate PRP ID
PRP_ID="PRP-$(date +%Y-%m-%d)-$(printf "%03d" $((RANDOM % 1000)))"

# Get today's date
TODAY=$(date +%Y-%m-%d)

# Substitute common variables
OUTPUT_CONTENT="$TEMPLATE_CONTENT"

# Basic substitutions
OUTPUT_CONTENT=$(echo "$OUTPUT_CONTENT" | sed "s|{{PRP_ID}}|$PRP_ID|g")
OUTPUT_CONTENT=$(echo "$OUTPUT_CONTENT" | sed "s|{{PROJECT_NAME}}|$PROJECT_NAME|g")
OUTPUT_CONTENT=$(echo "$OUTPUT_CONTENT" | sed "s|{{SOURCE_SPEC_PATH}}|$SPEC_FILE|g")
OUTPUT_CONTENT=$(echo "$OUTPUT_CONTENT" | sed "s|{{VALIDATION_DATE}}|$TODAY|g")
OUTPUT_CONTENT=$(echo "$OUTPUT_CONTENT" | sed "s|{{VALIDATION_STATUS}}|PASSED|g")
OUTPUT_CONTENT=$(echo "$OUTPUT_CONTENT" | sed "s|{{DOMAIN}}|${DETECTED_DOMAIN:-universal}|g")
OUTPUT_CONTENT=$(echo "$OUTPUT_CONTENT" | sed "s|{{VERSION}}|1.0|g")
OUTPUT_CONTENT=$(echo "$OUTPUT_CONTENT" | sed "s|{{AUTHOR}}|[FILL_AUTHOR]|g")

# Timeline substitution
if [[ "$TIMELINE" != "[FILL_TIMELINE]" ]]; then
    OUTPUT_CONTENT=$(echo "$OUTPUT_CONTENT" | sed "s|{{PHASE_1_DURATION}}|$TIMELINE|g")
fi

# Mark remaining variables as needing fill
OUTPUT_CONTENT=$(echo "$OUTPUT_CONTENT" | sed 's|{{[A-Z_]*}}|[FILL_THIS_IN]|g')

# Count substitutions needed
FILL_COUNT=$(echo "$OUTPUT_CONTENT" | grep -c "\[FILL_" 2>/dev/null || true)
FILL_COUNT=${FILL_COUNT:-0}

echo "   Substituted core variables"
echo "   Remaining placeholders: $FILL_COUNT"
echo ""

# ============================================================================
# Step 5: Interactive Mode (Optional)
# ============================================================================

if [[ "$INTERACTIVE" == "true" ]]; then
    echo -e "${BLUE}📝 Interactive mode - filling key values...${NC}"
    echo ""

    # Ask for problem statement
    echo -n "Problem statement (1 line): "
    read -r PROBLEM_STATEMENT
    if [[ -n "$PROBLEM_STATEMENT" ]]; then
        OUTPUT_CONTENT=$(echo "$OUTPUT_CONTENT" | sed "s|\[FILL_THIS_IN\]|$PROBLEM_STATEMENT|" | head -1)
    fi

    # Ask for primary metric
    echo -n "Primary success metric: "
    read -r PRIMARY_METRIC
    if [[ -n "$PRIMARY_METRIC" ]]; then
        OUTPUT_CONTENT=$(echo "$OUTPUT_CONTENT" | sed "s|\[FILL_THIS_IN\]|$PRIMARY_METRIC|" | head -1)
    fi

    # Ask for author
    echo -n "Author/Team: "
    read -r AUTHOR
    if [[ -n "$AUTHOR" ]]; then
        OUTPUT_CONTENT=$(echo "$OUTPUT_CONTENT" | sed "s|\[FILL_AUTHOR\]|$AUTHOR|g")
    fi

    echo ""
fi

# ============================================================================
# Step 6: Identify Relevant Patterns
# ============================================================================

echo -e "${BLUE}📚 Identifying relevant patterns...${NC}"

EXAMPLES_DIR="$SCRIPT_DIR/../examples"
RELEVANT_PATTERNS=()

# Check for API patterns
if echo "$SPEC_CONTENT" | grep -qiE "API|endpoint|REST|GraphQL|fetch|request"; then
    RELEVANT_PATTERNS+=("api-client.md")
    echo "   → API Client Pattern"
fi

# Check for error handling patterns
if echo "$SPEC_CONTENT" | grep -qiE "error|exception|failure|catch|try|recover"; then
    RELEVANT_PATTERNS+=("error-handling.md")
    echo "   → Error Handling Pattern"
fi

# Check for database patterns
if echo "$SPEC_CONTENT" | grep -qiE "database|db|postgres|mysql|query|repository|transaction"; then
    RELEVANT_PATTERNS+=("database-patterns.md")
    echo "   → Database Patterns"
fi

# Check for config patterns
if echo "$SPEC_CONTENT" | grep -qiE "config|environment|secret|credential|setting"; then
    RELEVANT_PATTERNS+=("config-loading.md")
    echo "   → Config Loading Pattern"
fi

# Check for test patterns
if echo "$SPEC_CONTENT" | grep -qiE "test|fixture|mock|stub|factory|spec"; then
    RELEVANT_PATTERNS+=("test-fixtures.md")
    echo "   → Test Fixtures Pattern"
fi

if [[ ${#RELEVANT_PATTERNS[@]} -eq 0 ]]; then
    echo "   (No specific patterns matched - check examples/ for available patterns)"
fi

# Build pattern links for PRP
PATTERN_LINKS=""
for pattern in "${RELEVANT_PATTERNS[@]}"; do
    PATTERN_LINKS+="- [$(echo "$pattern" | sed 's/-/ /g' | sed 's/\.md//' | sed 's/\b\w/\u&/g')](../examples/$pattern)
"
done

echo ""

# ============================================================================
# Step 7: Analyze Thinking Level
# ============================================================================

echo -e "${BLUE}🧠 Analyzing recommended thinking level...${NC}"

# Count domains involved
DOMAIN_COUNT=1
if [[ -n "$DOMAIN" ]]; then
    DOMAIN_COUNT=$((DOMAIN_COUNT + 1))
fi

# Estimate invariant count based on domain
INVARIANT_COUNT=10  # Universal invariants
case "$DETECTED_DOMAIN" in
    "consumer")
        INVARIANT_COUNT=$((INVARIANT_COUNT + 5))
        ;;
    "data-architecture")
        INVARIANT_COUNT=$((INVARIANT_COUNT + 5))
        ;;
    "integration")
        INVARIANT_COUNT=$((INVARIANT_COUNT + 4))
        ;;
    "physical-construction")
        INVARIANT_COUNT=$((INVARIANT_COUNT + 6))
        ;;
esac

# Estimate complexity based on spec content
COMPLEXITY_INDICATORS=0
if echo "$SPEC_CONTENT" | grep -qiE "security|authentication|authorization"; then
    COMPLEXITY_INDICATORS=$((COMPLEXITY_INDICATORS + 3))
fi
if echo "$SPEC_CONTENT" | grep -qiE "migration|database|data"; then
    COMPLEXITY_INDICATORS=$((COMPLEXITY_INDICATORS + 2))
fi
if echo "$SPEC_CONTENT" | grep -qiE "integration|third.party|external|API"; then
    COMPLEXITY_INDICATORS=$((COMPLEXITY_INDICATORS + 2))
fi
if echo "$SPEC_CONTENT" | grep -qiE "production|critical|financial"; then
    COMPLEXITY_INDICATORS=$((COMPLEXITY_INDICATORS + 2))
fi

# Determine thinking level
THINKING_LEVEL="Normal"
THINKING_REASON=""
if [[ $COMPLEXITY_INDICATORS -ge 7 ]]; then
    THINKING_LEVEL="Ultrathink"
    THINKING_REASON="High complexity: security/critical systems involved"
elif [[ $COMPLEXITY_INDICATORS -ge 4 ]]; then
    THINKING_LEVEL="Think Hard"
    THINKING_REASON="Moderate-high complexity: multiple integration points or data concerns"
elif [[ $COMPLEXITY_INDICATORS -ge 2 ]] || [[ $INVARIANT_COUNT -gt 15 ]]; then
    THINKING_LEVEL="Think"
    THINKING_REASON="Moderate complexity: multiple domains or validation concerns"
else
    THINKING_LEVEL="Normal"
    THINKING_REASON="Standard complexity: well-understood patterns"
fi

echo "   Recommended level: $THINKING_LEVEL"
echo "   Reason: $THINKING_REASON"
echo ""

# ============================================================================
# Step 8: Add Source Spec Reference, Patterns, and Thinking Level
# ============================================================================

# Append reference to source spec
SPEC_REFERENCE="
---

## Source Spec Reference

**Generated from**: \`$SPEC_FILE\`
**Generated on**: $TODAY
**Generator**: spec-to-prp.sh v1.1

### Thinking Level Analysis

| Factor | Value | Assessment |
|--------|-------|------------|
| Complexity indicators | $COMPLEXITY_INDICATORS | $(if [[ $COMPLEXITY_INDICATORS -ge 4 ]]; then echo "Elevated"; else echo "Normal"; fi) |
| Domains involved | $DOMAIN_COUNT | $(if [[ $DOMAIN_COUNT -gt 1 ]]; then echo "Multiple"; else echo "Single"; fi) |
| Invariants applicable | $INVARIANT_COUNT | $(if [[ $INVARIANT_COUNT -gt 15 ]]; then echo "Many"; else echo "Standard"; fi) |

**Recommended Thinking Level**: $THINKING_LEVEL
**Reason**: $THINKING_REASON

### Relevant Patterns

${PATTERN_LINKS:-"No specific patterns identified - see examples/ directory for available patterns"}

### Extracted Requirements

\`\`\`
$REQUIREMENTS
\`\`\`

---

*This PRP was auto-generated. Review and fill in all [FILL_THIS_IN] placeholders before execution.*
"

OUTPUT_CONTENT="$OUTPUT_CONTENT$SPEC_REFERENCE"

# ============================================================================
# Step 9: Write Output
# ============================================================================

echo -e "${BLUE}💾 Writing output:${NC} $OUTPUT_FILE"

# Create output directory if needed
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Write the file
echo "$OUTPUT_CONTENT" > "$OUTPUT_FILE"

echo -e "${GREEN}✅ PRP generated${NC}"
echo ""

# ============================================================================
# Step 10: Run Quality Check
# ============================================================================

echo -e "${BLUE}🔍 Running quality check...${NC}"
echo ""

# Make checker executable
chmod +x "$PRP_CHECKER"

# Run checker
"$PRP_CHECKER" "$OUTPUT_FILE" || CHECKER_EXIT=$?

echo ""

# ============================================================================
# Summary
# ============================================================================

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Generation Complete${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Output: ${CYAN}$OUTPUT_FILE${NC}"
echo ""
echo -e "${BLUE}📝 Next steps:${NC}"
echo "   1. Review $OUTPUT_FILE"
echo "   2. Fill in all [FILL_THIS_IN] placeholders ($FILL_COUNT remaining)"
echo "   3. Customize for your specific context"
echo "   4. Run prp-checker.sh again to verify"
echo ""

if [[ $FILL_COUNT -gt 0 ]]; then
    echo -e "${YELLOW}Placeholders to fill:${NC}"
    grep -n "\[FILL_" "$OUTPUT_FILE" | head -10 | while read -r line; do
        echo "   $line"
    done
    if [[ $FILL_COUNT -gt 10 ]]; then
        echo "   ... and $((FILL_COUNT - 10)) more"
    fi
fi

echo ""
echo -e "${GREEN}Done!${NC}"
