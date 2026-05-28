#!/bin/bash
# Get execution details
# Usage: ./get-execution.sh <execution-id> [--full]

source "$(dirname "$0")/_config.sh"

EXECUTION_ID="$1"
OUTPUT_MODE="${2:---summary}"

if [ -z "$EXECUTION_ID" ]; then
  echo "Usage: $0 <execution-id> [--full|--summary]"
  echo ""
  echo "Options:"
  echo "  --summary  Show execution summary (default)"
  echo "  --full     Show full execution data including node outputs"
  exit 1
fi

echo "Fetching execution: $EXECUTION_ID"
echo "Source: $N8N_BASE_URL"
echo ""

# For full output, include data
if [ "$OUTPUT_MODE" == "--full" ]; then
  RESPONSE=$(n8n_api GET "/executions/$EXECUTION_ID?includeData=true")
else
  RESPONSE=$(n8n_api GET "/executions/$EXECUTION_ID")
fi

# Check for errors
ERROR=$(echo "$RESPONSE" | jq -r '.message // empty')
if [ -n "$ERROR" ]; then
  error "API Error: $ERROR"
  exit 1
fi

case $OUTPUT_MODE in
  --full)
    echo "$RESPONSE" | jq '.'
    ;;
  --summary|*)
    echo "$RESPONSE" | jq '{
      id,
      status,
      mode,
      startedAt,
      stoppedAt,
      workflowId,
      finished
    }'
    ;;
esac
