#!/bin/bash
# Create new MCP Hub user
# Usage: create-user.sh <username> [role] [mode]
# Example: create-user.sh iris user whitelist

set -e

USERNAME="$1"
ROLE="${2:-user}"
MODE="${3:-whitelist}"

if [[ -z "$USERNAME" ]]; then
  echo "Usage: create-user.sh <username> [role] [mode]"
  echo "  username: lowercase name (e.g., iris, mercury)"
  echo "  role: user (default) or admin"
  echo "  mode: whitelist (default) or blacklist"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HUB_DIR="${SCRIPT_DIR}/../../../.."
CLIENTS_DIR="${HUB_DIR}/clients"
CLIENT_DIR="${CLIENTS_DIR}/${USERNAME}"

# Check if already exists
if [[ -d "$CLIENT_DIR" ]]; then
  echo "Error: Client ${USERNAME} already exists at ${CLIENT_DIR}"
  exit 1
fi

echo "Creating user: ${USERNAME}"
echo "  Role: ${ROLE}"
echo "  Mode: ${MODE}"
echo ""

# Create directory
mkdir -p "$CLIENT_DIR"

# Determine tools config based on role/mode
if [[ "$ROLE" == "admin" ]]; then
  TOOLS_CONFIG='"mode": "blacklist",
    "allowed": [],
    "denied": []'
elif [[ "$MODE" == "whitelist" ]]; then
  TOOLS_CONFIG='"mode": "whitelist",
    "allowed": [
      "ping",
      "list_tools",
      "get_service_health"
    ],
    "denied": ["admin_*"]'
else
  TOOLS_CONFIG='"mode": "blacklist",
    "allowed": [],
    "denied": ["admin_*"]'
fi

# Create config
cat > "${CLIENT_DIR}/client.config.json" << EOF
{
  "user": "${USERNAME}",
  "endpoint": "${USERNAME}-sse",
  "tools": {
    ${TOOLS_CONFIG}
  },
  "jwt": {
    "sub": "${USERNAME}",
    "role": "${ROLE}"
  },
  "enabled": true
}
EOF

echo "Created: ${CLIENT_DIR}/client.config.json"
echo ""
echo "Next steps:"
echo "1. Generate JWT:"
echo "   node scripts/generate-token.js ${USERNAME} --days 90"
echo ""
echo "2. Add tools to whitelist as needed"
echo ""
echo "3. Restart hub to pick up new user"
echo "   docker compose restart hub"
echo ""
echo "4. Send onboarding info to user"
