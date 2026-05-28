#!/bin/bash
set -euo pipefail

# jira-attach.sh - Attach files to Jira issues via REST API
#
# jira-cli does NOT support attachments, so this script uses the REST API directly.
# Reads server/login from existing jira-cli config (~/.config/.jira/.config.yml).
#
# Usage:
#   ./jira-attach.sh <issue-key> <file-path>
#   ./jira-attach.sh PROJ-123 /path/to/spec.md
#
# Requirements:
#   - JIRA_API_TOKEN environment variable set
#   - jira-cli configured (~/.config/.jira/.config.yml with server and login)
#   - curl and grep installed

JIRA_CONFIG="${JIRA_CONFIG_FILE:-$HOME/.config/.jira/.config.yml}"

# Check arguments
if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <issue-key> <file-path>" >&2
    echo "Example: $0 PROJ-123 /path/to/spec.md" >&2
    exit 1
fi

ISSUE_KEY="$1"
FILE_PATH="$2"

# Validate file exists
if [[ ! -f "$FILE_PATH" ]]; then
    echo "ERROR: File not found: $FILE_PATH" >&2
    exit 1
fi

# Check for API token
if [[ -z "${JIRA_API_TOKEN:-}" ]]; then
    echo "ERROR: JIRA_API_TOKEN environment variable not set" >&2
    echo "Set it with: export JIRA_API_TOKEN=your_token" >&2
    exit 1
fi

# Check for config file
if [[ ! -f "$JIRA_CONFIG" ]]; then
    echo "ERROR: jira-cli config not found at $JIRA_CONFIG" >&2
    echo "Run 'jira init' to configure jira-cli first" >&2
    exit 1
fi

# Read server and login from jira-cli config
SERVER=$(grep '^server:' "$JIRA_CONFIG" | awk '{print $2}')
LOGIN=$(grep '^login:' "$JIRA_CONFIG" | awk '{print $2}')

if [[ -z "$SERVER" ]]; then
    echo "ERROR: Could not read 'server' from $JIRA_CONFIG" >&2
    exit 1
fi

if [[ -z "$LOGIN" ]]; then
    echo "ERROR: Could not read 'login' from $JIRA_CONFIG" >&2
    exit 1
fi

# Make the API request
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
    "${SERVER}/rest/api/3/issue/${ISSUE_KEY}/attachments" \
    -u "${LOGIN}:${JIRA_API_TOKEN}" \
    -H "X-Atlassian-Token: no-check" \
    -F "file=@${FILE_PATH}")

# Parse response
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

# Check result
if [[ "$HTTP_CODE" -eq 200 ]]; then
    FILENAME=$(basename "$FILE_PATH")
    echo "Attached '$FILENAME' to $ISSUE_KEY"
    echo "Link in Jira: [^$FILENAME]"
    exit 0
else
    echo "ERROR: Failed to attach file (HTTP $HTTP_CODE)" >&2
    echo "$BODY" >&2
    exit 1
fi
