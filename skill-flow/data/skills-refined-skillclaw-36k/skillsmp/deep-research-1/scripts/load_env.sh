#!/bin/bash
# Enhanced Environment loader for deep-research skill
# Loads API keys from multiple sources with proper priority handling
#
# Usage:
#   source ~/.config/opencode/skill/deep-research/scripts/load_env.sh
#
# Priority (high → low):
# 1. Direct environment variables
# 2. ~/.local/bin/env script
# 3. ~/.bashrc export statements
# 4. ~/.config/opencode/.env file

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Loading environment for deep-research skill...${NC}"

# Track which sources provided keys
gemini_source=""
openai_source=""

# Function to safely export and track
safe_export() {
    local key="$1"
    local value="$2"
    local source="$3"
    
    if [ -n "$value" ] && [ -z "$(eval echo \$$key)" ]; then
        export "$key"="$value"
        case "$key" in
            GEMINI_API_KEY) gemini_source="$source" ;;
            OPENAI_API_KEY) openai_source="$source" ;;
        esac
    fi
}

# 1. Check ~/.config/opencode/.env file (highest priority after direct env)
if [ -f ~/.config/opencode/.env ]; then
    echo -e "${BLUE}   Reading from ~/.config/opencode/.env${NC}"
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ $key =~ ^[[:space:]]*# ]] && continue
        [[ -z $key ]] && continue
        
        # Remove quotes and spaces
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | sed 's/^["'\'']//' | sed 's/["'\'']$//' | xargs)
        
        safe_export "$key" "$value" "~/.config/opencode/.env"
    done < ~/.config/opencode/.env
fi

# 2. Source ~/.local/bin/env if available
if [ -f "$HOME/.local/bin/env" ]; then
    echo -e "${BLUE}   Sourcing ~/.local/bin/env${NC}"
    # Capture exports without affecting current shell
    eval "$(grep -E '^[[:space:]]*export[[:space:]]+' "$HOME/.local/bin/env" | sed 's/^export /safe_export /')"
fi

# 3. Extract from ~/.bashrc if no keys found yet
if ([ -z "$GEMINI_API_KEY" ] || [ -z "$OPENAI_API_KEY" ]) && [ -f ~/.bashrc ]; then
    echo -e "${BLUE}   Checking ~/.bashrc for API keys${NC}"
    # Use a simpler approach to extract exports
    while read -r line; do
        if [[ $line =~ ^[[:space:]]*export[[:space:]]+([A-Z_]+)=(.+)$ ]]; then
            key="${BASH_REMATCH[1]}"
            value="${BASH_REMATCH[2]}"
            # Remove surrounding quotes if present
            value=$(echo "$value" | sed 's/^["'\'']//' | sed 's/["'\'']$//')
            safe_export "$key" "$value" "~/.bashrc"
        fi
    done < <(grep -E '^[[:space:]]*export[[:space:]]+(GEMINI|OPENAI)_API_KEY' ~/.bashrc)
fi

# Report loaded keys
echo -e "${GREEN}✅ Environment loading complete${NC}"

if [ -n "$GEMINI_API_KEY" ]; then
    key_preview="${GEMINI_API_KEY:0:4}****${GEMINI_API_KEY: -4}"
    echo -e "${GREEN}   GEMINI_API_KEY loaded from $gemini_source ($key_preview)${NC}"
fi

if [ -n "$OPENAI_API_KEY" ]; then
    key_preview="${OPENAI_API_KEY:0:4}****${OPENAI_API_KEY: -4}"
    echo -e "${GREEN}   OPENAI_API_KEY loaded from $openai_source ($key_preview)${NC}"
fi

if [ -z "$GEMINI_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  WARNING: No API keys found${NC}"
    echo -e "${YELLOW}   LLM features will use mock responses${NC}"
    echo -e "${YELLOW}   Set up API keys:${NC}"
    echo -e "${YELLOW}   export GEMINI_API_KEY='your-key'${NC}"
    echo -e "${YELLOW}   export OPENAI_API_KEY='your-key'${NC}"
fi

echo -e "${BLUE}🔍 Ready to run deep-research skill${NC}"
