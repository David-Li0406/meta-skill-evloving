#!/bin/bash
# Ralph State Machine Project Initialization
# Creates .ralph/ directory and RALPH_TASK.md for state machine mode

set -e

DESIGN_OPS_DIR="${DESIGN_OPS_DIR:-$HOME/.claude/design-ops}"
RALPH_DIR="$DESIGN_OPS_DIR/ralph"
PROJECT_DIR="${1:-.}"
SPEC_FILE="${2:-}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     Ralph State Machine - Project Initialization        ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Project: ${GREEN}$PROJECT_DIR${NC}"

# Create .ralph directory
mkdir -p "$PROJECT_DIR/.ralph"

# Check for existing RALPH_TASK.md
if [[ -f "$PROJECT_DIR/RALPH_TASK.md" ]]; then
    echo -e "${YELLOW}Warning: RALPH_TASK.md already exists${NC}"
    read -p "Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Keeping existing RALPH_TASK.md${NC}"
    else
        cp "$RALPH_DIR/RALPH_TASK_TEMPLATE.md" "$PROJECT_DIR/RALPH_TASK.md"
        echo -e "${GREEN}✓ Copied RALPH_TASK.md template${NC}"
    fi
else
    cp "$RALPH_DIR/RALPH_TASK_TEMPLATE.md" "$PROJECT_DIR/RALPH_TASK.md"
    echo -e "${GREEN}✓ Created RALPH_TASK.md${NC}"
fi

# Update spec_file if provided
if [[ -n "$SPEC_FILE" ]]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s|spec_file:.*|spec_file: $SPEC_FILE|" "$PROJECT_DIR/RALPH_TASK.md"
    else
        sed -i "s|spec_file:.*|spec_file: $SPEC_FILE|" "$PROJECT_DIR/RALPH_TASK.md"
    fi
    echo -e "${GREEN}✓ Set spec_file to: $SPEC_FILE${NC}"
fi

# Copy ralph-loop.sh to project
cp "$RALPH_DIR/ralph-loop.sh" "$PROJECT_DIR/ralph-loop.sh"
chmod +x "$PROJECT_DIR/ralph-loop.sh"
echo -e "${GREEN}✓ Copied ralph-loop.sh${NC}"

# Copy ralph-common.sh to .ralph/
cp "$RALPH_DIR/ralph-common.sh" "$PROJECT_DIR/.ralph/ralph-common.sh"
chmod +x "$PROJECT_DIR/.ralph/ralph-common.sh"
echo -e "${GREEN}✓ Copied ralph-common.sh${NC}"

# Update ralph-loop.sh to source from local .ralph/
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' 's|source "$SCRIPT_DIR/ralph-common.sh"|source "$SCRIPT_DIR/.ralph/ralph-common.sh"|' "$PROJECT_DIR/ralph-loop.sh"
else
    sed -i 's|source "$SCRIPT_DIR/ralph-common.sh"|source "$SCRIPT_DIR/.ralph/ralph-common.sh"|' "$PROJECT_DIR/ralph-loop.sh"
fi

# Copy state template
cp "$RALPH_DIR/state-template.md" "$PROJECT_DIR/.ralph/"
echo -e "${GREEN}✓ Copied state-template.md${NC}"

# Create guardrails.md if not exists
if [[ ! -f "$PROJECT_DIR/.ralph/guardrails.md" ]]; then
    cat > "$PROJECT_DIR/.ralph/guardrails.md" << 'EOF'
# Ralph Guardrails

These are the invariants and lessons learned that guide autonomous development.

## Core Principles

1. **State lives in files** - .ralph/state.md is the source of truth
2. **Gates are commands** - Each state has a validation command and pass condition
3. **Retries are bounded** - Max retries per gate prevents infinite loops
4. **Fresh context per retry** - Each gate retry is a new agent invocation

## Project-Specific Invariants

Add your project's invariants here...

EOF
    echo -e "${GREEN}✓ Created guardrails.md${NC}"
fi

# Create progress.md if not exists
if [[ ! -f "$PROJECT_DIR/.ralph/progress.md" ]]; then
    cat > "$PROJECT_DIR/.ralph/progress.md" << 'EOF'
# Ralph Progress

## Current Status

Initialized. Ready to run state machine loop.

## History

- Initialized state machine mode

EOF
    echo -e "${GREEN}✓ Created progress.md${NC}"
fi

echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Init Complete!${NC}"
echo ""
echo -e "Next steps:"
echo -e "  1. ${YELLOW}Edit RALPH_TASK.md${NC} - Set your spec_file path"
echo -e "  2. ${YELLOW}Create your spec${NC} - docs/specs/my-feature.spec.md"
echo -e "  3. ${YELLOW}Run the loop:${NC}"
echo ""
echo -e "     ${CYAN}./ralph-loop.sh --state-machine -n 30 --max-gate-retries 5 -y${NC}"
echo ""
echo -e "  To resume after GUTTER:"
echo -e "     ${CYAN}./ralph-loop.sh --state-machine --resume -y${NC}"
echo ""
