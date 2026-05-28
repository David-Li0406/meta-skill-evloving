#!/bin/bash
# Environment Variables Checker Script (Unix/Mac/Linux)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the script's directory and navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

# Define required and optional environment variables
REQUIRED_VARS=("CLOUDFLARE_API" "CLOUDFLARE_ACCOUNT_ID")
OPTIONAL_VARS=("SUPABASE_URL" "SUPABASE_ANON_KEY" "SUPABASE_SERVICE_ROLE_KEY" "SUPABASE_PROJECT_REF")

# Counters
REQUIRED_SET=0
REQUIRED_TOTAL=${#REQUIRED_VARS[@]}
OPTIONAL_SET=0
OPTIONAL_TOTAL=${#OPTIONAL_VARS[@]}
HAS_PLACEHOLDERS=0

# Function to check if value is a placeholder
is_placeholder() {
    local value="$1"
    if [[ "$value" =~ (your-.*-here|your_.*_here|<.*>|xxxxx|abcdefg) ]]; then
        return 0
    fi
    return 1
}

# Function to check environment variable
check_env_var() {
    local var_name="$1"
    local is_required="$2"
    local value="${!var_name}"

    if [ -z "$value" ]; then
        echo -e "${RED}❌ $var_name: Not set${NC}"
        if [ "$is_required" = true ]; then
            echo -e "   ${YELLOW}→ This variable is required for deployment${NC}"
        fi
        return 1
    elif is_placeholder "$value"; then
        echo -e "${YELLOW}⚠️  $var_name: Placeholder value detected${NC}"
        echo -e "   ${CYAN}→ Replace with actual value${NC}"
        HAS_PLACEHOLDERS=1
        return 2
    else
        # Mask sensitive values in output
        local display_value="${value:0:20}"
        if [ ${#value} -gt 20 ]; then
            display_value="${display_value}..."
        fi
        echo -e "${GREEN}✅ $var_name: Set${NC}"
        return 0
    fi
}

# Main function
main() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════╗"
    echo "║   Environment Variables Check             ║"
    echo "╚═══════════════════════════════════════════╝"
    echo -e "${NC}\n"

    # Check if .env file exists
    ENV_FILE="$PROJECT_ROOT/.env"
    if [ ! -f "$ENV_FILE" ]; then
        echo -e "${RED}❌ Error: .env file not found in project root${NC}\n"
        echo -e "${YELLOW}To create your .env file:${NC}"
        echo -e "  1. Copy .env.example: ${CYAN}cp .env.example .env${NC}"
        echo -e "  2. Edit .env and add your credentials"
        echo -e "\n${YELLOW}See README.md for instructions on obtaining credentials.${NC}\n"
        exit 1
    fi

    # Load environment variables
    export $(cat "$ENV_FILE" | grep -v '^#' | grep -v '^$' | xargs)

    # Check Cloudflare variables (Required)
    echo -e "${BLUE}Cloudflare Workers (Required)${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    for var in "${REQUIRED_VARS[@]}"; do
        if check_env_var "$var" true; then
            ((REQUIRED_SET++))
        fi
    done

    # Check Supabase variables (Optional)
    echo -e "\n${BLUE}Supabase (Optional)${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    for var in "${OPTIONAL_VARS[@]}"; do
        check_result=0
        if check_env_var "$var" false; then
            check_result=$?
        else
            check_result=$?
        fi

        if [ $check_result -eq 0 ] || [ $check_result -eq 2 ]; then
            ((OPTIONAL_SET++))
        fi
    done

    # Summary
    echo -e "\n${BLUE}Summary${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    if [ $REQUIRED_SET -eq $REQUIRED_TOTAL ]; then
        echo -e "${GREEN}✅ Required variables: $REQUIRED_SET/$REQUIRED_TOTAL configured${NC}"
    else
        echo -e "${RED}❌ Required variables: $REQUIRED_SET/$REQUIRED_TOTAL configured${NC}"
        echo -e "${YELLOW}   Missing: $((REQUIRED_TOTAL - REQUIRED_SET)) required variable(s)${NC}"
    fi

    if [ $OPTIONAL_SET -gt 0 ]; then
        echo -e "${CYAN}ℹ️  Optional variables: $OPTIONAL_SET/$OPTIONAL_TOTAL configured${NC}"
    else
        echo -e "${CYAN}ℹ️  Optional variables: None configured (Supabase features disabled)${NC}"
    fi

    # Setup instructions if needed
    if [ $REQUIRED_SET -lt $REQUIRED_TOTAL ] || [ $HAS_PLACEHOLDERS -eq 1 ]; then
        echo -e "\n${YELLOW}Setup Instructions:${NC}"
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

        if [ $REQUIRED_SET -lt $REQUIRED_TOTAL ]; then
            echo -e "\n${YELLOW}Cloudflare Credentials:${NC}"
            echo -e "  1. Dashboard: ${CYAN}https://dash.cloudflare.com${NC}"
            echo -e "  2. Get Account ID from Workers & Pages section"
            echo -e "  3. API Tokens: ${CYAN}https://dash.cloudflare.com/profile/api-tokens${NC}"
            echo -e "  4. Create token using 'Edit Cloudflare Workers' template"
        fi

        if [ $HAS_PLACEHOLDERS -eq 1 ]; then
            echo -e "\n${YELLOW}Supabase Credentials (if using):${NC}"
            echo -e "  1. Dashboard: ${CYAN}https://supabase.com/dashboard${NC}"
            echo -e "  2. Select your project > Settings > API"
            echo -e "  3. Copy Project URL, Project Ref, and API keys"
        fi

        echo -e "\n${CYAN}After updating .env, run this check again:${NC}"
        echo -e "  ${CYAN}/check-envs${NC}\n"
    fi

    # Exit status
    if [ $REQUIRED_SET -eq $REQUIRED_TOTAL ]; then
        echo -e "\n${GREEN}✅ Environment configuration is valid for deployment!${NC}\n"
        exit 0
    else
        echo -e "\n${RED}❌ Environment configuration is incomplete.${NC}"
        echo -e "${YELLOW}Please configure missing required variables before deploying.${NC}\n"
        exit 1
    fi
}

# Run main function
main
