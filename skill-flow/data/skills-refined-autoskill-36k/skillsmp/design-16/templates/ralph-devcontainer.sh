#!/bin/bash
# ==============================================================================
# Ralph v2 Runner for Devcontainers
# ==============================================================================
# Executes Ralph v2 in dangerous mode with full autonomy.
#
# Prerequisites:
#   1. Enter devcontainer: devcontainer exec --workspace-folder . bash
#   2. Login to Claude: claude login
#   3. Run this script
#
# Usage:
#   ./ralph-devcontainer.sh                              # Run all steps
#   ./ralph-devcontainer.sh docs/plans/my-prp.md         # Specific PRP
#   ./ralph-devcontainer.sh docs/plans/my-prp.md 5       # With max 5 regenerations
# ==============================================================================

set -e

# Configuration
PRP_PATH="${1:-}"
MAX_REGEN="${2:-3}"
STEPS_DIR="${3:-ralph-steps}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           RALPH v2 - Dangerous Mode Runner                    ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check Claude CLI is available
if ! command -v claude &> /dev/null; then
    echo -e "${RED}Error: Claude CLI not found.${NC}"
    echo "Install with: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

# Check login status
if ! claude --version &> /dev/null; then
    echo -e "${YELLOW}Warning: Claude may not be logged in.${NC}"
    echo "Run 'claude login' first."
fi

# Find PRP if not specified
if [[ -z "$PRP_PATH" ]]; then
    # Look for most recent PRP file
    PRP_PATH=$(ls -t docs/plans/*-prp.md 2>/dev/null | head -1)
    if [[ -z "$PRP_PATH" ]]; then
        echo -e "${RED}Error: No PRP file found.${NC}"
        echo "Specify path: ./ralph-devcontainer.sh docs/plans/my-prp.md"
        exit 1
    fi
fi

# Validate PRP exists
if [[ ! -f "$PRP_PATH" ]]; then
    echo -e "${RED}Error: PRP file not found: $PRP_PATH${NC}"
    exit 1
fi

# Check for ralph-steps directory
if [[ ! -d "$STEPS_DIR" ]]; then
    echo -e "${YELLOW}Warning: $STEPS_DIR not found.${NC}"
    echo "Run '/design implement' first to generate steps."
    exit 1
fi

# Display configuration
echo -e "PRP:              ${GREEN}$PRP_PATH${NC}"
echo -e "Steps directory:  ${GREEN}$STEPS_DIR${NC}"
echo -e "Max regenerations: ${GREEN}$MAX_REGEN${NC}"
echo -e "Mode:             ${YELLOW}DANGEROUS (autonomous)${NC}"
echo ""

# Confirm in non-CI environment
if [[ -t 0 ]]; then
    echo -e "${YELLOW}This will run Ralph in dangerous mode with full autonomy.${NC}"
    read -p "Continue? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

echo ""
echo -e "${BLUE}Starting Ralph v2 execution...${NC}"
echo ""

# Execute Ralph in dangerous mode
claude --dangerously-skip-permissions \
    -p "/design run --dangerous --max-regen $MAX_REGEN"

EXIT_CODE=$?

echo ""
if [[ $EXIT_CODE -eq 0 ]]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║           RALPH EXECUTION COMPLETE                            ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
else
    echo -e "${RED}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║           RALPH EXECUTION FAILED (exit code: $EXIT_CODE)              ║${NC}"
    echo -e "${RED}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Check ralph-state.json for details."
fi

exit $EXIT_CODE
