#!/usr/bin/env bash
#
# server-client.sh - Proof-of-concept for e3 remote URL support
#
# This script demonstrates running e3-api-server with OIDC authentication
# and using e3 CLI commands against remote HTTP URLs.
#
# Usage: ./contrib/server-client.sh
#
# Run from the e3 monorepo root directory.
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory and e3 root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
E3_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# CLI tools (assumes npm link has been run)
E3_CLI="e3"
E3_SERVER="e3-api-server"

# Temp directory for test data
TEMP_DIR=""
SERVER_PID=""
CREDENTIALS_PATH=""

cleanup() {
    echo -e "\n${YELLOW}Cleaning up...${NC}"

    # Stop server if running
    if [[ -n "$SERVER_PID" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "Stopping server (PID: $SERVER_PID)"
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi

    # Remove temp directory
    if [[ -n "$TEMP_DIR" ]] && [[ -d "$TEMP_DIR" ]]; then
        echo "Removing temp directory: $TEMP_DIR"
        rm -rf "$TEMP_DIR"
    fi

    echo -e "${GREEN}Cleanup complete${NC}"
}

trap cleanup EXIT

header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

step() {
    echo -e "\n${GREEN}▶ $1${NC}"
}

run_cmd() {
    echo -e "${YELLOW}\$ $*${NC}"
    E3_CREDENTIALS_PATH="$CREDENTIALS_PATH" "$@"
}

# Check we're in the right directory
if [[ ! -f "$E3_ROOT/package.json" ]]; then
    echo -e "${RED}Error: Must run from e3 monorepo root${NC}"
    exit 1
fi

# Check CLI tools are available
if ! command -v e3 &> /dev/null || ! command -v e3-api-server &> /dev/null; then
    echo -e "${RED}Error: e3 and e3-api-server must be in PATH${NC}"
    echo -e "Run: ${YELLOW}npm run build && npm link -w @elaraai/e3-cli -w @elaraai/e3-api-server${NC}"
    exit 1
fi

header "e3 Server-Client Proof of Concept"

# Create temp directory structure
step "Creating test environment..."
TEMP_DIR=$(mktemp -d)
REPOS_DIR="$TEMP_DIR/repos"
REPO_NAME="demo-repo"
CREDENTIALS_PATH="$TEMP_DIR/credentials.json"

mkdir -p "$REPOS_DIR"
echo "Created: $REPOS_DIR"
echo "Credentials: $CREDENTIALS_PATH"

# Start server with OIDC authentication enabled and auto-approve for CI
step "Starting e3-api-server with OIDC (auto-approve enabled)..."
PORT=9876
SERVER_LOG="$TEMP_DIR/server.log"
E3_AUTH_AUTO_APPROVE=1 $E3_SERVER --repos "$REPOS_DIR" --port $PORT --oidc > "$SERVER_LOG" 2>&1 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"
echo "Server log: $SERVER_LOG"
echo "OIDC: enabled (auto-approve: true)"

# Wait for server to be ready
echo "Waiting for server to start..."
for i in {1..30}; do
    if curl -s "http://localhost:$PORT/api/repos" > /dev/null 2>&1; then
        echo -e "${GREEN}Server ready!${NC}"
        break
    fi
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
        echo -e "${RED}Server failed to start. Log:${NC}"
        cat "$SERVER_LOG"
        exit 1
    fi
    sleep 0.1
done

# Server base URL and repo URL
SERVER_URL="http://localhost:$PORT"
REMOTE_URL="$SERVER_URL/repos/$REPO_NAME"
echo -e "\nServer URL: ${YELLOW}$SERVER_URL${NC}"

header "Authenticating with OIDC"

step "Logging in (server auto-approves, no browser needed)..."
E3_CREDENTIALS_PATH="$CREDENTIALS_PATH" $E3_CLI login --no-browser "$SERVER_URL"

header "Testing Repository Commands"

step "Create repository via remote API..."
run_cmd $E3_CLI repo create "$REMOTE_URL"

step "Check repository status..."
run_cmd $E3_CLI repo status "$REMOTE_URL"

header "Testing Workspace Commands"

step "List workspaces (empty)..."
run_cmd $E3_CLI workspace list "$REMOTE_URL"

step "Create workspace 'dev'..."
run_cmd $E3_CLI workspace create "$REMOTE_URL" dev

step "Create workspace 'staging'..."
run_cmd $E3_CLI workspace create "$REMOTE_URL" staging

step "List workspaces..."
run_cmd $E3_CLI workspace list "$REMOTE_URL"

step "Remove workspace 'staging'..."
run_cmd $E3_CLI workspace remove "$REMOTE_URL" staging

step "List workspaces (after remove)..."
run_cmd $E3_CLI workspace list "$REMOTE_URL"

header "Testing Package Commands"

step "List packages (empty)..."
run_cmd $E3_CLI package list "$REMOTE_URL"

# Create a simple package using the e3 SDK
# Note: Must run from E3_ROOT to resolve @elaraai/* packages
step "Creating a test package..."
PACKAGE_ZIP="$TEMP_DIR/demo-pkg.zip"
(cd "$E3_ROOT" && node --input-type=module -e "
import e3 from '@elaraai/e3';
import { IntegerType, East } from '@elaraai/east';

const input = e3.input('value', IntegerType, 42n);
const task = e3.task(
  'double',
  [input],
  East.function([IntegerType], IntegerType, (\$, x) => x.multiply(2n))
);
const pkg = e3.package('demo-pkg', '1.0.0', task);

await e3.export(pkg, '$PACKAGE_ZIP');
console.log('Created: $PACKAGE_ZIP');
")

step "Import package via remote URL..."
run_cmd $E3_CLI package import "$REMOTE_URL" "$PACKAGE_ZIP"

step "List packages..."
run_cmd $E3_CLI package list "$REMOTE_URL"

header "Testing Full Workflow"

step "Deploy package to workspace..."
run_cmd $E3_CLI workspace deploy "$REMOTE_URL" dev demo-pkg@1.0.0

step "List workspaces (shows deployed package)..."
run_cmd $E3_CLI workspace list "$REMOTE_URL"

header "Summary"

echo -e "
${GREEN}Success!${NC} The proof-of-concept demonstrates:

  1. ${YELLOW}e3-api-server${NC} running on port $PORT with OIDC
     - Serving repositories at: $REPOS_DIR
     - API prefix: /api/repos/:repo/...
     - OIDC authentication enabled

  2. ${YELLOW}OIDC Device Flow${NC} authentication
     - Auto-approved login (E3_AUTH_AUTO_APPROVE=1)
     - Credentials stored in: $CREDENTIALS_PATH
     - JWTs for access and refresh tokens

  3. ${YELLOW}e3 CLI${NC} using remote URLs
     - Server URL: $SERVER_URL
     - Repository URL: $REMOTE_URL
     - Works exactly like local paths (after login)

  4. ${YELLOW}Operations tested:${NC}
     - login (OIDC device flow)
     - repo create/status (via remote API)
     - workspace list/create/remove/deploy
     - package list/import

The same CLI commands work with both local paths and remote URLs:
  ${YELLOW}e3 login $SERVER_URL${NC}                   # authenticate
  ${YELLOW}e3 repo create .${NC}                       # local (no auth)
  ${YELLOW}e3 repo create $REMOTE_URL${NC}  # remote (uses token)
  ${YELLOW}e3 workspace list .${NC}                    # local (no auth)
  ${YELLOW}e3 workspace list $REMOTE_URL${NC}  # remote (uses token)
"

echo -e "${BLUE}Press Enter to cleanup and exit...${NC}"
read -r

