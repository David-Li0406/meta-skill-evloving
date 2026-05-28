#!/bin/bash

# Configuration
DEFAULT_ENV_FILE=".env"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Check arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 VAR1 VAR2 ..."
    echo "Checks if specified environment variables are set and non-empty in .env or .env.local"
    exit 1
fi

TARGET_FILE="$DEFAULT_ENV_FILE"
if [ -f ".env.local" ]; then
    TARGET_FILE=".env.local"
fi

if [ ! -f "$TARGET_FILE" ]; then
    echo -e "${RED}Error: No .env or .env.local file found at $TARGET_FILE${NC}"
    exit 1
fi

MISSING_VARS=()
EMPTY_VARS=()

echo "Checking $TARGET_FILE..."

for var in "$@"; do
    # Check if var exists in file (even if empty)
    if grep -q "^export ${var}=" "$TARGET_FILE" || grep -q "^${var}=" "$TARGET_FILE"; then
        # Check if value is empty using grep/sed to extract value
        # This regex looks for VAR=... and grabs content after =
        val=$(grep -E "^(export )?${var}=" "$TARGET_FILE" | head -n 1 | sed -E "s/^(export )?${var}=//")
        
        # Remove quotes if present
        val="${val%\"}"
        val="${val#\"}"
        
        if [ -z "$val" ]; then
            EMPTY_VARS+=("$var")
        fi
    else
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -eq 0 ] && [ ${#EMPTY_VARS[@]} -eq 0 ]; then
    echo -e "${GREEN}All checked variables are present and non-empty.${NC}"
    exit 0
else
    if [ ${#MISSING_VARS[@]} -gt 0 ]; then
        echo -e "${RED}Missing variables:${NC}"
        printf ' - %s\n' "${MISSING_VARS[@]}"
    fi
    
    if [ ${#EMPTY_VARS[@]} -gt 0 ]; then
        echo -e "${RED}Present but empty variables:${NC}"
        printf ' - %s\n' "${EMPTY_VARS[@]}"
    fi
    exit 1
fi
