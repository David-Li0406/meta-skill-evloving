#!/bin/bash
# n8n-ops shared configuration
# Source this file in all n8n scripts: source "$(dirname "$0")/_config.sh"
#
# ADAPTATION REQUIRED:
# Set these environment variables before using any n8n scripts:
#   N8N_BASE_URL - Your n8n instance URL (e.g., https://n8n.example.com)
#   N8N_API_KEY  - Your n8n API key
#
# You can set these in:
#   - .env file in repo root
#   - Shell environment
#   - CI/CD secrets

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Load .env if present
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"

if [ -f "$REPO_ROOT/.env" ]; then
  set -a
  source "$REPO_ROOT/.env"
  set +a
fi

# Validate required environment variables
check_config() {
  local missing=0

  if [ -z "$N8N_BASE_URL" ]; then
    echo -e "${RED}ERROR: N8N_BASE_URL not set${NC}"
    echo ""
    echo "Please set your n8n instance URL:"
    echo "  export N8N_BASE_URL=https://n8n.your-domain.com"
    echo ""
    echo "Or add to .env file in repo root:"
    echo "  N8N_BASE_URL=https://n8n.your-domain.com"
    echo ""
    missing=1
  fi

  if [ -z "$N8N_API_KEY" ]; then
    echo -e "${RED}ERROR: N8N_API_KEY not set${NC}"
    echo ""
    echo "Please set your n8n API key:"
    echo "  export N8N_API_KEY=your-api-key"
    echo ""
    echo "Or add to .env file in repo root:"
    echo "  N8N_API_KEY=your-api-key"
    echo ""
    echo "To create an API key in n8n:"
    echo "  Settings → API → Create API Key"
    echo ""
    missing=1
  fi

  if [ $missing -eq 1 ]; then
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}This script requires configuration before first use.${NC}"
    echo -e "${YELLOW}See .claude/skills/n8n-ops/scripts/README.md for setup guide.${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 1
  fi

  # Validate URL format
  if [[ ! "$N8N_BASE_URL" =~ ^https?:// ]]; then
    echo -e "${RED}ERROR: N8N_BASE_URL must start with http:// or https://${NC}"
    echo "Current value: $N8N_BASE_URL"
    exit 1
  fi

  # Remove trailing slash if present
  N8N_BASE_URL="${N8N_BASE_URL%/}"
}

# API helper function
n8n_api() {
  local method="${1:-GET}"
  local endpoint="$2"
  local data="$3"

  local url="${N8N_BASE_URL}/api/v1${endpoint}"

  if [ -n "$data" ]; then
    curl -s -X "$method" "$url" \
      -H "X-N8N-API-KEY: $N8N_API_KEY" \
      -H "Content-Type: application/json" \
      -d "$data"
  else
    curl -s -X "$method" "$url" \
      -H "X-N8N-API-KEY: $N8N_API_KEY"
  fi
}

# Success/error output helpers
success() {
  echo -e "${GREEN}✓ $1${NC}"
}

error() {
  echo -e "${RED}✗ $1${NC}"
}

warn() {
  echo -e "${YELLOW}! $1${NC}"
}

# Run config check by default when sourced
check_config
