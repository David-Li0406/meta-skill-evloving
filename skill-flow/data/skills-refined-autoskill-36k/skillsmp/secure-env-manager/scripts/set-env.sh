#!/bin/bash

# Configuration
DEFAULT_ENV_FILE=".env.local"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Secure Environment Variable Manager ===${NC}"
echo "This script allows you to securely set environment variables without exposing them in history or logs."
echo ""

# Always use .env.local for security - no prompts needed
TARGET_FILE=".env.local"
echo -e "Using secure file: ${BLUE}$TARGET_FILE${NC}"

# Ensure file exists
if [ ! -f "$TARGET_FILE" ]; then
    read -p "File '$TARGET_FILE' does not exist. Create it? (y/n) " create_confirm
    if [[ "$create_confirm" =~ ^[Yy]$ ]]; then
        touch "$TARGET_FILE"
        echo -e "${GREEN}Created $TARGET_FILE${NC}"
    else
        echo -e "${RED}Aborted.${NC}"
        exit 1
    fi
fi

echo -e "Updating: ${YELLOW}$TARGET_FILE${NC}"
echo "Press Ctrl+C to exit."

# Function to prompt and save
prompt_and_save() {
    local VAR_NAME=$1
    echo ""
    # Read value securely
    echo -n "Enter Value for $VAR_NAME (input hidden): "
    read -s VAR_VALUE
    echo "" # Newline after silent input

    # Check if value is empty
    if [ -z "$VAR_VALUE" ]; then
         read -p "Value is empty. Do you want to set it to empty string? (y/n) " empty_confirm
         if [[ ! "$empty_confirm" =~ ^[Yy]$ ]]; then
             return
         fi
    fi
    
    # Escape double quotes in value
    ESCAPED_VALUE=${VAR_VALUE//\"/\\\"}

    # Process the file
    TMP_FILE="${TARGET_FILE}.tmp"
    
    # Check if var exists (checking for both plain VAR= and export VAR=)
    if grep -q "^export ${VAR_NAME}=" "$TARGET_FILE" || grep -q "^${VAR_NAME}=" "$TARGET_FILE"; then
        echo -e "${YELLOW}Variable $VAR_NAME exists. Updating...${NC}"
        # Remove existing line(s) - excluding the variable we are updating
        grep -v "^export ${VAR_NAME}=" "$TARGET_FILE" | grep -v "^${VAR_NAME}=" > "$TMP_FILE"
        
        # Append new value
        echo "${VAR_NAME}=\"$ESCAPED_VALUE\"" >> "$TMP_FILE"
        mv "$TMP_FILE" "$TARGET_FILE"
        echo -e "${GREEN}Updated $VAR_NAME${NC}"
    else
        echo -e "${BLUE}Variable $VAR_NAME Not found. Adding...${NC}"
        echo "${VAR_NAME}=\"$ESCAPED_VALUE\"" >> "$TARGET_FILE"
        echo -e "${GREEN}Added $VAR_NAME${NC}"
    fi
}

# Main Logic
if [ "$1" == "--all" ]; then
    # Reset All Mode
    echo -e "${BLUE}Starting RESET ALL mode for: $TARGET_FILE${NC}"
    echo "Scanning for existing variables..."
    
    # Get list of vars. 
    # 1. Grep regular lines (VAR=...) or export lines (export VAR=...)
    # 2. Filter out comments
    # 3. Extract name
    EXISTING_VARS=$(grep -E '^export [a-zA-Z0-9_]+=|^[a-zA-Z0-9_]+=' "$TARGET_FILE" | sed -E 's/^export //;s/=.*//')
    
    if [ -z "$EXISTING_VARS" ]; then
        echo -e "${YELLOW}No variables found in $TARGET_FILE to reset.${NC}"
        exit 0
    fi
    
    for var in $EXISTING_VARS; do
        prompt_and_save "$var"
    done

elif [ $# -gt 0 ]; then
    # Arguments provided: Guided Mode
    echo -e "${BLUE}Starting guided setup for: $@${NC}"
    for var in "$@"; do
        prompt_and_save "$var"
    done
else
    # No arguments: Interactive Mode
    while true; do
        echo ""
        read -p "Enter Variable Name (e.g. API_KEY) or ENTER to quit: " USER_VAR
        
        # Trim whitespace
        USER_VAR=$(echo "$USER_VAR" | xargs)
        
        if [ -z "$USER_VAR" ]; then
            break
        fi
        
        prompt_and_save "$USER_VAR"
    done
fi

echo ""
# Function to verify keys if they are PayPal keys
verify_keys() {
    # Check if we just set PayPal keys
    if grep -q "PAYPAL_CLIENT_ID_SANDBOX" "$TARGET_FILE" && grep -q "PAYPAL_CLIENT_SECRET_SANDBOX" "$TARGET_FILE"; then
        echo ""
        echo -e "${BLUE}=== Verifying PayPal Sandbox Credentials ===${NC}"
        
        # Source the file to get the keys
        source "$TARGET_FILE"
        
        if [ -z "$PAYPAL_CLIENT_ID_SANDBOX" ] || [ -z "$PAYPAL_CLIENT_SECRET_SANDBOX" ]; then
            echo -e "${YELLOW}Skipping verification: One or both keys are empty.${NC}"
            return
        fi

        echo "Testing keys against https://api.sandbox.paypal.com/v1/oauth2/token..."
        
        # Base64 encode credentials
        AUTH=$(echo -n "${PAYPAL_CLIENT_ID_SANDBOX}:${PAYPAL_CLIENT_SECRET_SANDBOX}" | base64)
        
        RESPONSE=$(curl -s -X POST "https://api.sandbox.paypal.com/v1/oauth2/token" \
            -H "Authorization: Basic $AUTH" \
            -H "Content-Type: application/x-www-form-urlencoded" \
            -d "grant_type=client_credentials")

        if echo "$RESPONSE" | grep -q "access_token"; then
             echo -e "${GREEN}✅ SUCCESS: Credentials are valid!${NC}"
        else
             echo -e "${RED}❌ FAILURE: Credentials rejected by PayPal.${NC}"
             echo "Response: $RESPONSE"
             echo -e "${YELLOW}Please double-check your Sandbox Client ID and Secret.${NC}"
        fi
    fi
}

echo ""
echo -e "${GREEN}Done. Your keys have been securely saved to $TARGET_FILE${NC}"
verify_keys
