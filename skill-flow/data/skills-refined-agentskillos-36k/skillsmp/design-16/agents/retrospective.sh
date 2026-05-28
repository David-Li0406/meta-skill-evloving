#!/bin/bash
#
# retrospective.sh - Extract learnings and propose system improvements
#
# Usage: ./agents/retrospective.sh <prp-file> --outcome <summary> [--domain <domain>] [--output <dir>]
#
# Outputs:
#   - retrospective.md following the template
#   - invariant-proposals.json for domain module updates

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
PRP_FILE=""
OUTCOME=""
DOMAIN="general"
OUTPUT_DIR="."
INTERACTIVE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --outcome)
            OUTCOME="$2"
            shift 2
            ;;
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --interactive|-i)
            INTERACTIVE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 <prp-file> --outcome <summary> [options]"
            echo ""
            echo "Options:"
            echo "  --outcome <summary>  Brief description of implementation outcome"
            echo "  --domain <domain>    Target domain for invariant proposals"
            echo "  --output <dir>       Output directory"
            echo "  --interactive, -i    Prompt for retrospective answers"
            exit 0
            ;;
        -*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            PRP_FILE="$1"
            shift
            ;;
    esac
done

if [[ -z "$PRP_FILE" ]] || [[ ! -f "$PRP_FILE" ]]; then
    echo -e "${RED}Error: Valid PRP file required${NC}"
    exit 1
fi

if [[ -z "$OUTCOME" ]]; then
    echo -e "${RED}Error: Outcome summary required (--outcome)${NC}"
    exit 1
fi

echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  RETROSPECTIVE - Learning Extraction & System Improvement${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}PRP:${NC}     $PRP_FILE"
echo -e "${BLUE}Domain:${NC}  $DOMAIN"
echo -e "${BLUE}Outcome:${NC} $OUTCOME"
echo ""

PRP_CONTENT=$(cat "$PRP_FILE")
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Extract project name from PRP
PROJECT_NAME=$(echo "$PRP_CONTENT" | grep -m1 "^# PRP:" | sed 's/# PRP: //' || basename "$PRP_FILE" .md)

# Extract confidence from PRP
ORIGINAL_CONFIDENCE=$(echo "$PRP_CONTENT" | grep -oE "Confidence.*[0-9]+%" | head -1 | grep -oE "[0-9]+" || echo "N/A")

# ============================================================================
# Analyze Implementation
# ============================================================================
echo -e "${YELLOW}[1/4] Analyzing implementation...${NC}"

# Count sections completed (look for checkboxes)
TOTAL_CHECKBOXES=$(echo "$PRP_CONTENT" | grep -c '\[.\]' || true)
CHECKED_BOXES=$(echo "$PRP_CONTENT" | grep -c '\[x\]' || true)

if [[ $TOTAL_CHECKBOXES -gt 0 ]]; then
    COMPLETION_RATE=$((CHECKED_BOXES * 100 / TOTAL_CHECKBOXES))
else
    COMPLETION_RATE="N/A"
fi

echo -e "  Completion: $CHECKED_BOXES/$TOTAL_CHECKBOXES tasks ($COMPLETION_RATE%)"

# Look for risks that materialized
RISKS_SECTION=$(echo "$PRP_CONTENT" | sed -n '/## 7\. Risk Assessment/,/## 8\./p' || true)

# ============================================================================
# Generate Retrospective Questions
# ============================================================================
echo -e "${YELLOW}[2/4] Generating retrospective...${NC}"

# Default answers (would be filled interactively or from analysis)
WHAT_WENT_WELL="Implementation completed according to plan."
WHAT_COULD_IMPROVE="Review validation commands earlier in process."
PROCESS_IMPROVEMENT="Consider adding pre-flight checklist."
MISSING_INVARIANTS="None identified."
CONVENTIONS_UPDATE="No updates needed."
DOMAIN_UPDATE="No updates needed."
VALIDATION_COMMANDS="Existing commands sufficient."

# ============================================================================
# Identify Invariant Proposals
# ============================================================================
echo -e "${YELLOW}[3/4] Identifying invariant proposals...${NC}"

declare -a PROPOSALS

# Analyze outcome for potential invariants
case "$OUTCOME" in
    *"error"*|*"bug"*|*"fix"*)
        PROPOSALS+=("Add validation for error scenarios in $DOMAIN domain")
        ;;
    *"security"*|*"auth"*)
        PROPOSALS+=("Strengthen security invariants for $DOMAIN domain")
        ;;
    *"performance"*|*"slow"*)
        PROPOSALS+=("Add performance threshold invariants")
        ;;
esac

# Check if there were issues mentioned in PRP
if echo "$PRP_CONTENT" | grep -qiE "violation|warning|issue"; then
    PROPOSALS+=("Review and strengthen validation rules that generated warnings")
fi

PROPOSAL_COUNT=${#PROPOSALS[@]}
echo -e "  Generated $PROPOSAL_COUNT invariant proposals"

# ============================================================================
# Generate Output Files
# ============================================================================
echo -e "${YELLOW}[4/4] Generating output files...${NC}"

# Retrospective markdown
RETRO_FILE="$OUTPUT_DIR/retrospective-${PROJECT_NAME// /-}.md"

cat > "$RETRO_FILE" << EOF
# Retrospective: ${PROJECT_NAME}

> Post-implementation learning capture

| Field | Value |
|-------|-------|
| Date | ${DATE} |
| Domain | ${DOMAIN} |
| Original Confidence | ${ORIGINAL_CONFIDENCE}% |
| Outcome | ${OUTCOME} |

---

## 1. Summary

### Implementation Outcome
${OUTCOME}

### Completion Status
- Tasks completed: ${CHECKED_BOXES}/${TOTAL_CHECKBOXES}
- Completion rate: ${COMPLETION_RATE}%

---

## 2. What Went Well

${WHAT_WENT_WELL}

---

## 3. What Could Be Improved

${WHAT_COULD_IMPROVE}

---

## 4. Lessons Learned

### Technical Learnings
<!-- What technical insights were gained? -->

- Lesson 1
- Lesson 2

### Process Learnings
<!-- What process improvements are needed? -->

- Lesson 1
- Lesson 2

---

## 5. System Improvements (MANDATORY)

> This section feeds back into the Design Ops system.

### 5.1 Process Improvements Needed

**Question**: What process improvements should be made for similar future tasks?

${PROCESS_IMPROVEMENT}

### 5.2 Missing Invariants

**Question**: Were there any validation rules that SHOULD have caught issues but didn't exist?

${MISSING_INVARIANTS}

### 5.3 CONVENTIONS.md Updates

**Question**: Should any new conventions be added based on this implementation?

${CONVENTIONS_UPDATE}

### 5.4 Domain Module Updates

**Question**: Should the \`${DOMAIN}.md\` invariant file be updated?

${DOMAIN_UPDATE}

### 5.5 Validation Commands

**Question**: Were the validation commands sufficient? What should be added?

${VALIDATION_COMMANDS}

---

## 6. Invariant Proposals

$(if [[ ${#PROPOSALS[@]} -gt 0 ]]; then
    echo "The following invariants are proposed based on this implementation:"
    echo ""
    for proposal in "${PROPOSALS[@]}"; do
        echo "- [ ] $proposal"
    done
else
    echo "No new invariants proposed."
fi)

---

## 7. Action Items

- [ ] Review and finalize invariant proposals
- [ ] Update domain module if needed
- [ ] Share learnings with team
- [ ] Archive this retrospective

---

## 8. Reference

### Source PRP
\`${PRP_FILE}\`

### Related Files
<!-- List any related files, PRs, issues -->

- Related file 1
- Related file 2

---

## Metadata

\`\`\`json
{
  "generated": "${TIMESTAMP}",
  "generator": "retrospective.sh",
  "prp_file": "${PRP_FILE}",
  "domain": "${DOMAIN}"
}
\`\`\`
EOF

echo -e "  Created: $RETRO_FILE"

# Invariant proposals JSON
PROPOSALS_FILE="$OUTPUT_DIR/invariant-proposals.json"

PROPOSALS_JSON=$(printf '%s\n' "${PROPOSALS[@]}" 2>/dev/null | jq -R '{description: ., domain: env.DOMAIN, status: "proposed"}' | jq -s . || echo "[]")

cat > "$PROPOSALS_FILE" << EOF
{
  "timestamp": "${TIMESTAMP}",
  "source_prp": "${PRP_FILE}",
  "domain": "${DOMAIN}",
  "outcome": "${OUTCOME}",
  "proposals": ${PROPOSALS_JSON}
}
EOF

echo -e "  Created: $PROPOSALS_FILE"

# ============================================================================
# Output Summary
# ============================================================================
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Retrospective complete!${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"

echo ""
echo -e "${BLUE}Generated Files:${NC}"
echo -e "  Retrospective: $RETRO_FILE"
echo -e "  Proposals:     $PROPOSALS_FILE"

echo ""
echo -e "${BLUE}Summary:${NC}"
echo -e "  Project:       $PROJECT_NAME"
echo -e "  Completion:    ${COMPLETION_RATE}%"
echo -e "  Proposals:     $PROPOSAL_COUNT"

echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Review and complete the retrospective answers"
echo -e "  2. Finalize invariant proposals"
echo -e "  3. Run: ./tools/spec-delta-to-invariant.sh $RETRO_FILE"

exit 0
