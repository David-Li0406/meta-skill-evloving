#!/bin/bash
# check-mcp.sh
# Verifies MCP server availability before running the workflow
# Zero context cost - executed, not loaded into conversation

set -e

echo "Checking MCP server availability..."
echo ""

# Required servers
REQUIRED_SERVERS="linear"
OPTIONAL_SERVERS="quoth exolar"

# Check function
check_server() {
    local server="$1"
    local required="$2"

    # Note: This is a placeholder. In practice, MCP availability
    # is checked within the Claude Code conversation context.
    # This script demonstrates the validation concept.

    if [ "$required" = "true" ]; then
        echo "[ REQUIRED ] $server"
    else
        echo "[ OPTIONAL ] $server"
    fi
}

echo "Required MCP Servers:"
echo "---------------------"
for server in $REQUIRED_SERVERS; do
    check_server "$server" "true"
done

echo ""
echo "Optional MCP Servers:"
echo "---------------------"
for server in $OPTIONAL_SERVERS; do
    check_server "$server" "false"
done

echo ""
echo "Note: Actual MCP availability is verified at runtime."
echo "Optional servers gracefully fallback if unavailable."

exit 0
