#!/bin/bash
# Template for processing meeting minutes

# Configuration
MEETING_ID="${1:-}"  # First argument or empty

# Validate input
if [ -z "$MEETING_ID" ]; then
    echo "Usage: $0 <meeting_id>"
    echo "Example: $0 123"
    exit 1
fi

# Process minutes
echo "Processing meeting ID: $MEETING_ID"
just exec uv run sagebase process-minutes --meeting-id "$MEETING_ID"

# Extract speakers
echo "Extracting speakers..."
just exec uv run sagebase extract-speakers

# Match speakers with politicians
echo "Matching speakers with politicians..."
just exec uv run sagebase update-speakers --use-llm

echo "Processing complete for meeting ID: $MEETING_ID"
