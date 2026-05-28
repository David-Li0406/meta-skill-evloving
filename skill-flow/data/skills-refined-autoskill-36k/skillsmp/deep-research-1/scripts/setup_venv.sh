#!/bin/bash
# Setup virtual environment for deep-research skill
# Creates an isolated venv within the skill directory
#
# Usage:
#   ./setup_venv.sh [--force]
#
# Options:
#   --force  Remove existing venv and recreate

set -e

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
SKILL_DIR=$(dirname "$SCRIPT_DIR")
VENV_DIR="$SKILL_DIR/.venv"
REQUIREMENTS="$SKILL_DIR/requirements.txt"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Deep Research Skill - Virtual Environment Setup ===${NC}"
echo -e "${BLUE}Skill directory: $SKILL_DIR${NC}"
echo -e "${BLUE}Venv directory: $VENV_DIR${NC}"

# Check for --force flag
if [ "$1" = "--force" ] && [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Removing existing venv...${NC}"
    rm -rf "$VENV_DIR"
fi

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: Failed to create virtual environment${NC}"
        exit 1
    fi
    echo -e "${GREEN}Virtual environment created successfully${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
fi

# Activate venv and install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
source "$VENV_DIR/bin/activate"

# Upgrade pip first
pip install --upgrade pip -q

# Install from requirements.txt
if [ -f "$REQUIREMENTS" ]; then
    pip install -r "$REQUIREMENTS" -q
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Dependencies installed successfully${NC}"
    else
        echo -e "${RED}ERROR: Failed to install some dependencies${NC}"
        deactivate
        exit 1
    fi
else
    echo -e "${YELLOW}No requirements.txt found, installing minimal dependencies...${NC}"
    pip install duckduckgo-search beautifulsoup4 requests google-genai openai -q
fi

# Show installed packages
echo -e "${BLUE}Installed packages:${NC}"
pip list | grep -E "(duckduckgo|beautifulsoup|requests|google-genai|openai)"

deactivate

echo ""
echo -e "${GREEN}=== Setup Complete ===${NC}"
echo -e "${GREEN}To activate: source $VENV_DIR/bin/activate${NC}"
echo -e "${GREEN}To run research: ./scripts/run_research.sh \"your topic\"${NC}"
