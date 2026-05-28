#!/bin/bash
# =============================================================================
# extract-linear-issue-id.sh
# =============================================================================
# Extracts a Linear ticket ID from a ticket ID string or Linear URL.
#
# Usage:
#   ./extract-linear-issue-id.sh <ticket-id-or-url>
#
# Arguments:
#   $1 - Ticket ID (e.g., "ENG-123") or Linear URL
#        (e.g., "https://linear.app/team/issue/ENG-123/title")
#
# Outputs:
#   Prints extracted uppercase ticket ID to stdout
#
# Exit codes:
#   0 - Success
#   1 - Invalid format (no ticket ID found)
#
# Examples:
#   ./extract-linear-issue-id.sh ENG-123        # Returns: ENG-123
#   ./extract-linear-issue-id.sh eng-123        # Returns: ENG-123 (case-insensitive)
#   ./extract-linear-issue-id.sh https://linear.app/myteam/issue/ENG-456/fix-bug
# =============================================================================

TICKET_INPUT="$1"
# Convert to uppercase and extract ticket ID pattern
TICKET_ID=$(echo "$TICKET_INPUT" | tr '[:lower:]' '[:upper:]' | grep -oE '[A-Z]+-[0-9]+' | head -n 1)

if [ -z "$TICKET_ID" ]; then
  echo "Error: Invalid ticket ID or URL format" >&2
  exit 1
fi

echo "$TICKET_ID"
