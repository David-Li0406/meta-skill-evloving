#!/bin/bash
# validate-capability-flow.sh — Validate a capability flow specification
# Part of the AI-Augmented SDLC Framework (build tooling)
# Usage: validate-capability-flow.sh <spec-file>

set -euo pipefail

# Valid values
VALID_CAPABILITIES="Elicit Analyse Synthesise Transform Validate Decide Generate Preserve"
VALID_PATTERNS="Human-Only Human-Led Partnership AI-Led AI-Only"

if [[ $# -lt 1 ]]; then
    echo "Usage: validate-capability-flow.sh <spec-file>" >&2
    echo "  spec-file: Path to YAML capability flow specification" >&2
    exit 1
fi

SPEC_FILE="$1"

if [[ ! -f "$SPEC_FILE" ]]; then
    echo "Error: File not found: $SPEC_FILE" >&2
    exit 1
fi

echo "Validating: $SPEC_FILE"
echo "---"

VIOLATIONS=0
PASS_COUNT=0

# Parse YAML and validate each step
# This is a simplified validator - production would use a proper YAML parser

# Extract steps (looks for lines like "Step PA-1:" or "- step_id:")
while IFS= read -r line; do
    # Look for step definitions
    if [[ "$line" =~ ^[[:space:]]*Step[[:space:]]([A-Z0-9-]+): ]] || \
       [[ "$line" =~ step_id:[[:space:]]*[\"\']?([A-Z0-9-]+) ]]; then
        STEP_ID="${BASH_REMATCH[1]}"
        echo -n "Step $STEP_ID: "

        # For this simplified version, we output guidance
        # A full implementation would parse the YAML structure
        echo "CHECK MANUALLY"
        echo "  □ Capability is valid (one of: $VALID_CAPABILITIES)"
        echo "  □ Pattern is valid (one of: $VALID_PATTERNS)"
        echo "  □ C1: Human-Only → AI Role = None"
        echo "  □ C2: AI-Only → Human Role = None"
        echo "  □ C3: AI Role ≠ None → Pattern ≠ Human-Only"
        echo "  □ C4: Human Role ≠ None → Pattern ≠ AI-Only"
        echo "  □ Escalation triggers defined (if AI participates)"
        echo ""
    fi
done < "$SPEC_FILE"

echo "---"
echo "Manual validation required. Check each step against constraints."
echo ""
echo "Constraint reference:"
echo "  C1: Human-Only pattern requires AI Role = 'None'"
echo "  C2: AI-Only pattern requires Human Role = 'None'"
echo "  C3: Any AI Role requires Pattern ≠ Human-Only"
echo "  C4: Any Human Role requires Pattern ≠ AI-Only"
