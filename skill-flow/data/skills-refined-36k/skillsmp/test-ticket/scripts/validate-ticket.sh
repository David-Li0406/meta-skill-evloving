#!/bin/bash
# validate-ticket.sh
# Validates ticket ID format before running the workflow
# Zero context cost - executed, not loaded into conversation

set -e

TICKET_ID="$1"

if [ -z "$TICKET_ID" ]; then
    echo "Error: No ticket ID provided"
    echo "Usage: ./validate-ticket.sh ENG-123"
    exit 1
fi

# Validate format: PREFIX-NUMBER (e.g., ENG-123, PROJ-456, LIN-789)
if ! [[ "$TICKET_ID" =~ ^[A-Z]+-[0-9]+$ ]]; then
    echo "Error: Invalid ticket ID format: $TICKET_ID"
    echo "Expected format: PREFIX-NUMBER (e.g., ENG-123, PROJ-456)"
    exit 1
fi

echo "Valid ticket ID: $TICKET_ID"

# Extract prefix and number
PREFIX="${TICKET_ID%-*}"
NUMBER="${TICKET_ID##*-}"

echo "  Prefix: $PREFIX"
echo "  Number: $NUMBER"

exit 0
