#!/bin/bash
# Run deep research with isolated venv and environment variables
#
# This script:
# 1. Loads API keys from multiple sources (secure)
# 2. Activates the skill-specific virtual environment
# 3. Executes the research with proper isolation
#
# Usage:
#   ./run_research.sh "research topic" [options]
#
# Options:
#   --depth N         URLs to fetch per step (default: 3)
#   --breadth N       URLs per step (enables iterative mode)
#   --output-dir DIR  Custom output directory
#   --check-only      Only verify system readiness
#   --setup           Setup venv before running
#
#   # Phase 2 Options
#   --parallel        Enable parallel scraping (5-10x faster)
#   --token-budget N  Set token budget limit (default: 100000)
#   --min-trust N     Minimum source trust score (0.0-1.0, default: 0.3)
#
# Examples:
#   ./run_research.sh "AI trends in 2026"
#   ./run_research.sh "Climate change" --depth 5
#   ./run_research.sh --check-only

set -e

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
SKILL_DIR=$(dirname "$SCRIPT_DIR")
VENV_DIR="$SKILL_DIR/.venv"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse --setup flag before other processing
for arg in "$@"; do
    if [ "$arg" = "--setup" ]; then
        echo -e "${BLUE}Setting up virtual environment...${NC}"
        "$SCRIPT_DIR/setup_venv.sh"
        # Remove --setup from arguments
        set -- "${@/--setup/}"
        break
    fi
done

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    "$SCRIPT_DIR/setup_venv.sh"
fi

# ===== Load Environment Variables (API Keys) =====
echo -e "${BLUE}Loading environment variables...${NC}"

# Function to safely load and export API keys
load_api_keys() {
    local key_loaded=false
    
    # Priority 1: Check if already in environment
    if [ -n "$GEMINI_API_KEY" ] || [ -n "$OPENAI_API_KEY" ]; then
        key_loaded=true
        [ -n "$GEMINI_API_KEY" ] && echo -e "${GREEN}  GEMINI_API_KEY: from environment${NC}"
        [ -n "$OPENAI_API_KEY" ] && echo -e "${GREEN}  OPENAI_API_KEY: from environment${NC}"
    fi
    
    # Priority 2: ~/.config/opencode/.env
    if [ -f "$HOME/.config/opencode/.env" ]; then
        while IFS='=' read -r key value; do
            [[ $key =~ ^[[:space:]]*# ]] && continue
            [[ -z $key ]] && continue
            key=$(echo "$key" | xargs)
            value=$(echo "$value" | sed 's/^[\"'\'']//' | sed 's/[\"'\'']$//' | xargs)
            
            case "$key" in
                GEMINI_API_KEY|OPENAI_API_KEY|LLM_PROVIDER)
                    if [ -z "$(eval echo \$$key)" ] && [ -n "$value" ]; then
                        export "$key"="$value"
                        echo -e "${GREEN}  $key: from ~/.config/opencode/.env${NC}"
                        key_loaded=true
                    fi
                    ;;
            esac
        done < "$HOME/.config/opencode/.env"
    fi
    
    # Priority 3: ~/.bashrc
    if [ -f "$HOME/.bashrc" ]; then
        while IFS= read -r line; do
            if [[ $line =~ ^[[:space:]]*export[[:space:]]+(GEMINI_API_KEY|OPENAI_API_KEY)=(.+)$ ]]; then
                key="${BASH_REMATCH[1]}"
                value="${BASH_REMATCH[2]}"
                value=$(echo "$value" | sed 's/^[\"'\'']//' | sed 's/[\"'\'']$//')
                
                if [ -z "$(eval echo \$$key)" ] && [ -n "$value" ]; then
                    export "$key"="$value"
                    echo -e "${GREEN}  $key: from ~/.bashrc${NC}"
                    key_loaded=true
                fi
            fi
        done < <(grep -E '^[[:space:]]*export[[:space:]]+(GEMINI|OPENAI)_API_KEY' "$HOME/.bashrc" 2>/dev/null || true)
    fi
    
    if [ "$key_loaded" = false ]; then
        echo -e "${YELLOW}  No API keys found - will run in mock mode${NC}"
    fi
}

load_api_keys

# ===== Activate Virtual Environment =====
echo -e "${BLUE}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Verify Python environment
PYTHON_PATH=$(which python)
echo -e "${GREEN}  Python: $PYTHON_PATH${NC}"

# ===== Execute Research =====
echo -e "${BLUE}Starting deep research...${NC}"
echo ""

# Pass all arguments to the Python script
python "$SCRIPT_DIR/run.py" "$@"
exit_code=$?

# Deactivate venv
deactivate

exit $exit_code
