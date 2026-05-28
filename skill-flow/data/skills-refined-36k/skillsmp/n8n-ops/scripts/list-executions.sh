#!/bin/bash
# List workflow executions
# Usage: ./list-executions.sh [workflow-id] [--limit N] [--status STATUS]

source "$(dirname "$0")/_config.sh"

WORKFLOW_ID=""
LIMIT=10
STATUS=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --limit|-l)
      LIMIT="$2"
      shift 2
      ;;
    --status|-s)
      STATUS="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [workflow-id] [--limit N] [--status STATUS]"
      echo ""
      echo "Options:"
      echo "  --limit, -l   Number of executions to show (default: 10)"
      echo "  --status, -s  Filter by status: success, error, waiting"
      echo ""
      echo "Examples:"
      echo "  $0                           # All recent executions"
      echo "  $0 abc123                    # Executions for specific workflow"
      echo "  $0 --status error --limit 5  # Last 5 failed executions"
      exit 0
      ;;
    *)
      WORKFLOW_ID="$1"
      shift
      ;;
  esac
done

# Build query string
QUERY="?limit=$LIMIT"
if [ -n "$WORKFLOW_ID" ]; then
  QUERY="${QUERY}&workflowId=$WORKFLOW_ID"
fi
if [ -n "$STATUS" ]; then
  QUERY="${QUERY}&status=$STATUS"
fi

echo "Fetching executions from: $N8N_BASE_URL"
if [ -n "$WORKFLOW_ID" ]; then
  echo "Workflow: $WORKFLOW_ID"
fi
echo ""

RESPONSE=$(n8n_api GET "/executions$QUERY")

# Check for errors
ERROR=$(echo "$RESPONSE" | jq -r '.message // empty')
if [ -n "$ERROR" ]; then
  error "API Error: $ERROR"
  exit 1
fi

# Format output
echo "$RESPONSE" | jq -r '.data[] | "\(.id)\t\(.status)\t\(.startedAt)\t\(.workflowId)"' | column -t -s $'\t'

TOTAL=$(echo "$RESPONSE" | jq '.data | length')
echo ""
echo "Showing: $TOTAL executions"
