#!/bin/bash
# Ralph v2 Project Initialization
# Creates ralph-steps/ directory structure and copies utilities

set -e

DESIGN_OPS_DIR="${DESIGN_OPS_DIR:-$HOME/.claude/design-ops}"
PROJECT_DIR="${1:-.}"
RALPH_STEPS="$PROJECT_DIR/ralph-steps"

echo "=== Ralph v2 Init ==="
echo "Project: $PROJECT_DIR"

# Create ralph-steps directory
if [ -d "$RALPH_STEPS" ]; then
    echo "Warning: ralph-steps/ already exists"
    read -p "Reinitialize? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

mkdir -p "$RALPH_STEPS"

# Copy test utilities
if [ -f "$DESIGN_OPS_DIR/templates/test-utils.sh" ]; then
    cp "$DESIGN_OPS_DIR/templates/test-utils.sh" "$RALPH_STEPS/"
    echo "✓ Copied test-utils.sh"
else
    echo "Warning: test-utils.sh not found at $DESIGN_OPS_DIR/templates/"
fi

# Initialize ralph-state.json
cat > "$RALPH_STEPS/ralph-state.json" << 'EOF'
{
  "version": "2.0",
  "prp": null,
  "current_step": 0,
  "total_steps": 0,
  "mode": "default",
  "steps": {},
  "gates": {},
  "dev_server": null,
  "learnings": [],
  "regenerations": 0,
  "max_regenerations": 3
}
EOF
echo "✓ Created ralph-state.json"

# Create PRP-COVERAGE.md template
cat > "$RALPH_STEPS/PRP-COVERAGE.md" << 'EOF'
# PRP Coverage Tracker

## PRP: [Link to PRP]

## Deliverables → Steps Mapping

| Deliverable | Step(s) | Status |
|-------------|---------|--------|
| | | |

## Gates

| Gate | After Step | Criteria | Status |
|------|------------|----------|--------|
| 1 | | | pending |

## Notes

EOF
echo "✓ Created PRP-COVERAGE.md"

echo ""
echo "=== Init Complete ==="
echo "Next steps:"
echo "  1. Link PRP in PRP-COVERAGE.md"
echo "  2. Run /design implement to generate steps"
echo "  3. Run /design run to execute"
