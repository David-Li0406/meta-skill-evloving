#!/bin/bash
# Create an epistemic belief file with validation
# Usage: create-belief.sh --id ID --statement "..." --persona PERSONA --confidence 0.X --evidence "..." [--facets "..."]

set -e

# Default values
BELIEFS_DIR="layer/surface/epistemic/beliefs"
ENTRENCHMENT="medium"
STATUS="active"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --id)
            ID="$2"
            shift 2
            ;;
        --statement)
            STATEMENT="$2"
            shift 2
            ;;
        --persona)
            PERSONA="$2"
            shift 2
            ;;
        --confidence)
            CONFIDENCE="$2"
            shift 2
            ;;
        --evidence)
            EVIDENCE="$2"
            shift 2
            ;;
        --facets)
            FACETS="$2"
            shift 2
            ;;
        --entrenchment)
            ENTRENCHMENT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validation
ERRORS=""

if [ -z "$ID" ]; then
    ERRORS="${ERRORS}Error: --id is required\n"
elif ! [[ "$ID" =~ ^[a-z][a-z0-9-]*$ ]]; then
    ERRORS="${ERRORS}Error: --id must be lowercase letters, numbers, and hyphens (start with letter)\n"
fi

if [ -z "$STATEMENT" ]; then
    ERRORS="${ERRORS}Error: --statement is required\n"
fi

if [ -z "$PERSONA" ]; then
    ERRORS="${ERRORS}Error: --persona is required\n"
fi

if [ -z "$CONFIDENCE" ]; then
    ERRORS="${ERRORS}Error: --confidence is required\n"
elif ! [[ "$CONFIDENCE" =~ ^0\.[0-9]+$ ]] && [ "$CONFIDENCE" != "1.0" ]; then
    ERRORS="${ERRORS}Error: --confidence must be between 0.0 and 1.0\n"
fi

if [ -z "$EVIDENCE" ]; then
    ERRORS="${ERRORS}Error: --evidence is required (at least one source)\n"
fi

if [ -n "$ERRORS" ]; then
    echo -e "$ERRORS"
    echo "Usage: create-belief.sh --id ID --statement \"...\" --persona PERSONA --confidence 0.X --evidence \"...\" [--facets \"...\"]"
    exit 1
fi

# Check if file already exists
OUTPUT_FILE="${BELIEFS_DIR}/${ID}.md"
if [ -f "$OUTPUT_FILE" ]; then
    echo "Error: Belief file already exists: $OUTPUT_FILE"
    echo "To update an existing belief, edit the file directly."
    exit 1
fi

# Ensure directory exists
mkdir -p "$BELIEFS_DIR"

# Format facets as YAML array
if [ -n "$FACETS" ]; then
    FACETS_YAML="[$(echo "$FACETS" | sed 's/,/, /g')]"
else
    FACETS_YAML="[]"
fi

# Get current date
TODAY=$(date +%Y-%m-%d)

# Calculate confidence signals (simple heuristic based on overall confidence)
# In practice, these would be provided separately
EVIDENCE_SIGNAL=$(printf "%.2f" $(echo "$CONFIDENCE + 0.05" | bc))
SOURCE_SIGNAL="$CONFIDENCE"
RECENCY_SIGNAL="0.80"
SURVIVAL_SIGNAL="0.50"  # New belief, low survival
ENDORSEMENT_SIGNAL="0.50"  # Not yet endorsed

# Cap evidence signal at 1.0
if (( $(echo "$EVIDENCE_SIGNAL > 1.0" | bc -l) )); then
    EVIDENCE_SIGNAL="1.00"
fi

# Create the belief file
cat > "$OUTPUT_FILE" << EOF
---
type: belief
id: ${ID}
persona: ${PERSONA}
facets: ${FACETS_YAML}
confidence:
  score: ${CONFIDENCE}
  signals:
    evidence: ${EVIDENCE_SIGNAL}
    source_reliability: ${SOURCE_SIGNAL}
    recency: ${RECENCY_SIGNAL}
    survival: ${SURVIVAL_SIGNAL}
    user_endorsement: ${ENDORSEMENT_SIGNAL}
entrenchment: ${ENTRENCHMENT}
status: ${STATUS}
extracted: ${TODAY}
revised: ${TODAY}
---

# ${ID}

${STATEMENT}

## Statement

${STATEMENT}

## Evidence

- ${EVIDENCE}

## Supports

<!-- Add beliefs this supports -->

## Attacks

<!-- Add beliefs this defeats -->

## Attacked-By

<!-- Add beliefs that challenge this -->

## Applied-In

<!-- Add concrete applications -->

## Revision Log

- ${TODAY}: Created (confidence: ${CONFIDENCE})
EOF

echo "✓ Belief created: $OUTPUT_FILE"
echo ""
echo "Next steps:"
echo "  1. Review and edit the file to add:"
echo "     - Additional evidence links"
echo "     - Support/attack relationships"
echo "     - Applied-in examples"
echo "  2. Update layer/surface/epistemic/_index.md"
echo "  3. Commit: git add $OUTPUT_FILE && git commit -m 'belief: add ${ID}'"
