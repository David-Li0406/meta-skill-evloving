#!/bin/bash
# Unified Deployment Script - Cloudflare Workers & Supabase Edge Functions
# Supports: Unix/Mac/Linux

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the script's directory and navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

# Load environment variables from .env
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
else
    echo -e "${RED}Error: .env file not found in project root${NC}"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# ═══════════════════════════════════════════════════════════════════════════════
# Branch-Based Deployment Functions
# ═══════════════════════════════════════════════════════════════════════════════

# Sanitize branch name for resource naming (DNS-safe, max 59 chars to leave room for "api-" prefix)
sanitize_branch_name() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[/_]/-/g' | sed 's/[^a-z0-9-]//g' | sed 's/^-*//;s/-*$//' | sed 's/-\+/-/g' | cut -c1-59 | sed 's/-$//'
}

# Get current git branch
get_git_branch() {
    git -C "$PROJECT_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo ""
}

# Check if branch is protected (deploys to production)
is_protected_branch() {
    local branch="$1"
    [ "$branch" = "main" ] || [ "$branch" = "master" ] || [ -z "$branch" ]
}

# Get worker name based on branch
get_worker_name() {
    local branch="$1"
    if is_protected_branch "$branch"; then
        echo "api"
    else
        local sanitized=$(sanitize_branch_name "$branch")
        [ -n "$sanitized" ] && echo "api-${sanitized}" || echo "api"
    fi
}

# Check if Supabase preview branch exists
check_supabase_branch_exists() {
    local branch_name="$1"
    local sanitized=$(sanitize_branch_name "$branch_name")

    # List branches and check if our branch exists
    local branch_list=$(supabase branches list --project-ref "$SUPABASE_PROJECT_REF" 2>/dev/null)
    if echo "$branch_list" | grep -q "$sanitized"; then
        return 0  # Branch exists
    else
        return 1  # Branch does not exist
    fi
}

# Get Supabase preview branch details (ref, URL, keys)
# Returns: ref|url|anon_key|service_role_key (pipe-separated)
get_supabase_branch_details() {
    local branch_name="$1"
    local sanitized=$(sanitize_branch_name "$branch_name")

    # Get branch details - this returns JSON with branch info
    local branch_info=$(supabase branches get "$sanitized" --project-ref "$SUPABASE_PROJECT_REF" 2>/dev/null)

    # Try to parse the branch ref and other details
    # The output format may vary, so we try multiple approaches
    local branch_ref=$(echo "$branch_info" | grep -oE '[a-z]{20}' | head -1)

    echo "$branch_ref"
}

# Display Supabase branch credentials info
display_supabase_branch_info() {
    local branch_name="$1"
    local sanitized=$(sanitize_branch_name "$branch_name")

    echo -e "\n${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}  Supabase Preview Branch Credentials${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Branch:${NC} ${sanitized}"
    echo ""
    echo -e "${YELLOW}Note:${NC} Preview branches have their own API credentials."
    echo -e "To get the branch-specific credentials, run:"
    echo -e "  ${GREEN}supabase branches get ${sanitized} --project-ref $SUPABASE_PROJECT_REF${NC}"
    echo ""
    echo -e "${YELLOW}If your Cloudflare Worker connects to Supabase, update its"
    echo -e "environment with the branch-specific SUPABASE_URL and keys.${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# Create Supabase preview branch
create_supabase_branch() {
    local branch_name="$1"
    local sanitized=$(sanitize_branch_name "$branch_name")

    echo -e "${YELLOW}Creating Supabase preview branch: ${sanitized}${NC}"
    supabase branches create "$sanitized" --project-ref "$SUPABASE_PROJECT_REF"
    return $?
}

# ═══════════════════════════════════════════════════════════════════════════════
# Deployment Functions
# ═══════════════════════════════════════════════════════════════════════════════

# Function to deploy to Cloudflare Workers
deploy_cloudflare() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  Deploying to Cloudflare Workers${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

    # Check if bun is installed
    if ! command_exists bun; then
        echo -e "${RED}Error: bun is not installed or not in PATH${NC}"
        echo -e "${YELLOW}Install from: https://bun.sh${NC}"
        return 1
    fi

    # Navigate to API directory
    cd "$PROJECT_ROOT/apps/api"

    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo -e "${RED}Error: node_modules not found. Run 'bun install' first.${NC}"
        return 1
    fi

    # Check required environment variables
    if [ -z "$CLOUDFLARE_API" ] || [ -z "$CLOUDFLARE_ACCOUNT_ID" ]; then
        echo -e "${RED}Error: Missing required environment variables${NC}"
        echo -e "${YELLOW}Required: CLOUDFLARE_API, CLOUDFLARE_ACCOUNT_ID${NC}"
        return 1
    fi

    # Detect git branch and compute worker name
    local git_branch=$(get_git_branch)
    local worker_name=$(get_worker_name "$git_branch")

    # Display branch info
    if is_protected_branch "$git_branch"; then
        echo -e "${GREEN}Branch:${NC} ${git_branch:-detached HEAD} (production)"
        echo -e "${GREEN}Worker:${NC} ${worker_name}"
    else
        echo -e "${YELLOW}Branch:${NC} ${git_branch} (preview)"
        echo -e "${YELLOW}Worker:${NC} ${worker_name}"
    fi
    echo ""

    # Run deployment with branch-specific worker name
    echo -e "${GREEN}Starting Cloudflare deployment...${NC}"
    if is_protected_branch "$git_branch"; then
        # Production deployment uses default wrangler.jsonc name
        bun run deploy
    else
        # Feature branch deployment uses custom worker name
        bunx wrangler deploy --minify --name "$worker_name"
    fi

    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}✓ Cloudflare Workers deployment successful!${NC}"
        echo -e "${BLUE}URL: https://${worker_name}.*.workers.dev${NC}"
        return 0
    else
        echo -e "\n${RED}✗ Cloudflare Workers deployment failed${NC}"
        return 1
    fi
}

# Function to deploy to Supabase Edge Functions
deploy_supabase() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  Deploying to Supabase Edge Functions${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

    # Check if supabase CLI is installed
    if ! command_exists supabase; then
        echo -e "${RED}Error: Supabase CLI is not installed or not in PATH${NC}"
        echo -e "${YELLOW}Install from: https://supabase.com/docs/guides/cli${NC}"
        echo -e "${YELLOW}  npm install -g supabase${NC}"
        echo -e "${YELLOW}  or: brew install supabase/tap/supabase${NC}"
        return 1
    fi

    # Navigate to project root
    cd "$PROJECT_ROOT"

    # Check if supabase directory exists
    if [ ! -d "supabase/functions" ]; then
        echo -e "${RED}Error: supabase/functions directory not found${NC}"
        return 1
    fi

    # Check required environment variables
    if [ -z "$SUPABASE_PROJECT_REF" ]; then
        echo -e "${RED}Error: Missing SUPABASE_PROJECT_REF environment variable${NC}"
        echo -e "${YELLOW}Add to .env: SUPABASE_PROJECT_REF=your-project-ref${NC}"
        return 1
    fi

    # Detect git branch
    local git_branch=$(get_git_branch)
    local deploy_ref="$SUPABASE_PROJECT_REF"
    local functions_url="https://$SUPABASE_PROJECT_REF.supabase.co/functions/v1/"

    # Display branch info and track if deploying to preview
    local is_preview_branch=false

    if is_protected_branch "$git_branch"; then
        echo -e "${GREEN}Branch:${NC} ${git_branch:-detached HEAD} (production)"
        echo -e "${GREEN}Project:${NC} ${SUPABASE_PROJECT_REF}"
    else
        local sanitized_branch=$(sanitize_branch_name "$git_branch")
        echo -e "${YELLOW}Branch:${NC} ${git_branch} (preview)"
        echo -e "${YELLOW}Supabase Branch:${NC} ${sanitized_branch}"

        # Check if preview branch exists
        is_preview_branch=true
        echo -e "\n${BLUE}Checking for existing Supabase preview branch...${NC}"
        if check_supabase_branch_exists "$git_branch"; then
            echo -e "${GREEN}✓ Preview branch '${sanitized_branch}' exists${NC}"
            # Get the branch's project ref for the URL
            local branch_ref=$(get_supabase_branch_details "$git_branch")
            if [ -n "$branch_ref" ]; then
                functions_url="https://${branch_ref}.supabase.co/functions/v1/"
            fi
        else
            echo -e "${YELLOW}Preview branch '${sanitized_branch}' does not exist${NC}"
            echo ""
            read -p "Create Supabase preview branch '${sanitized_branch}'? [y/N]: " create_branch

            if [ "$create_branch" = "y" ] || [ "$create_branch" = "Y" ]; then
                if create_supabase_branch "$git_branch"; then
                    echo -e "${GREEN}✓ Preview branch created successfully${NC}"
                    # Get the new branch's project ref
                    local branch_ref=$(get_supabase_branch_details "$git_branch")
                    if [ -n "$branch_ref" ]; then
                        functions_url="https://${branch_ref}.supabase.co/functions/v1/"
                    fi
                else
                    echo -e "${RED}✗ Failed to create preview branch${NC}"
                    echo -e "${YELLOW}You may need to enable branching in your Supabase project settings${NC}"
                    echo -e "${YELLOW}Or deploy to production instead${NC}"
                    return 1
                fi
            else
                echo -e "${YELLOW}Skipping preview branch creation. Deploying to production instead.${NC}"
                is_preview_branch=false
            fi
        fi
    fi
    echo ""

    # Check if project is linked
    if [ ! -f "supabase/.temp/project-ref" ]; then
        echo -e "${YELLOW}Project not linked. Linking now...${NC}"
        supabase link --project-ref "$SUPABASE_PROJECT_REF"
        if [ $? -ne 0 ]; then
            echo -e "${RED}✗ Failed to link Supabase project${NC}"
            echo -e "${YELLOW}Run manually: supabase login && supabase link${NC}"
            return 1
        fi
    fi

    # Deploy all functions
    echo -e "${GREEN}Starting Supabase Edge Functions deployment...${NC}"
    supabase functions deploy

    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}✓ Supabase Edge Functions deployment successful!${NC}"
        echo -e "${BLUE}Functions available at: ${functions_url}${NC}"

        # Display branch credentials info if deploying to a preview branch
        if [ "$is_preview_branch" = "true" ]; then
            display_supabase_branch_info "$git_branch"
        fi
        return 0
    else
        echo -e "\n${RED}✗ Supabase Edge Functions deployment failed${NC}"
        return 1
    fi
}

# Main script logic
main() {
    # Get git branch info for display
    local git_branch=$(get_git_branch)
    local branch_type="production"
    if ! is_protected_branch "$git_branch"; then
        branch_type="preview"
    fi

    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════════╗"
    echo "║   Unified Deployment - Select Platform   ║"
    echo "╚═══════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${BLUE}Git Branch:${NC} ${git_branch:-detached HEAD} (${branch_type})"
    echo ""

    # Check if DEPLOY_TARGET is set (for automated deployments)
    if [ ! -z "$DEPLOY_TARGET" ]; then
        PLATFORM_CHOICE="$DEPLOY_TARGET"
        echo -e "${BLUE}Using automated target: $DEPLOY_TARGET${NC}"
    else
        # Interactive platform selection
        echo "Select deployment platform:"
        echo "  1) Cloudflare Workers"
        echo "  2) Supabase Edge Functions"
        echo "  3) Both platforms"
        echo ""
        read -p "Enter choice [1-3]: " choice

        case $choice in
            1) PLATFORM_CHOICE="cloudflare" ;;
            2) PLATFORM_CHOICE="supabase" ;;
            3) PLATFORM_CHOICE="both" ;;
            *)
                echo -e "${RED}Invalid choice. Exiting.${NC}"
                exit 1
                ;;
        esac
    fi

    # Track deployment results
    CF_SUCCESS=0
    SB_SUCCESS=0

    # Deploy based on selection
    case $PLATFORM_CHOICE in
        cloudflare)
            deploy_cloudflare
            CF_SUCCESS=$?
            ;;
        supabase)
            deploy_supabase
            SB_SUCCESS=$?
            ;;
        both)
            deploy_cloudflare
            CF_SUCCESS=$?
            deploy_supabase
            SB_SUCCESS=$?
            ;;
    esac

    # Summary
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  Deployment Summary${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    if [ "$PLATFORM_CHOICE" = "cloudflare" ] || [ "$PLATFORM_CHOICE" = "both" ]; then
        if [ $CF_SUCCESS -eq 0 ]; then
            echo -e "${GREEN}✓ Cloudflare Workers: SUCCESS${NC}"
        else
            echo -e "${RED}✗ Cloudflare Workers: FAILED${NC}"
        fi
    fi

    if [ "$PLATFORM_CHOICE" = "supabase" ] || [ "$PLATFORM_CHOICE" = "both" ]; then
        if [ $SB_SUCCESS -eq 0 ]; then
            echo -e "${GREEN}✓ Supabase Edge Functions: SUCCESS${NC}"
        else
            echo -e "${RED}✗ Supabase Edge Functions: FAILED${NC}"
        fi
    fi

    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

    # Exit with error if any deployment failed
    if [ $CF_SUCCESS -ne 0 ] || [ $SB_SUCCESS -ne 0 ]; then
        exit 1
    fi

    exit 0
}

# Run main function
main
