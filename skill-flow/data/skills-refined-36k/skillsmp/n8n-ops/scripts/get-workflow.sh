#!/bin/bash
# Get workflow details
# Usage: ./get-workflow.sh <workflow-id> [--full|--nodes|--status]

source "$(dirname "$0")/_config.sh"

WORKFLOW_ID="$1"
OUTPUT_MODE="${2:---status}"

if [ -z "$WORKFLOW_ID" ]; then
  echo "Usage: $0 <workflow-id> [--full|--nodes|--status]"
  echo ""
  echo "Options:"
  echo "  --status  Show basic status (default)"
  echo "  --nodes   Show node summary"
  echo "  --full    Show full workflow JSON"
  exit 1
fi

echo "Fetching workflow: $WORKFLOW_ID"
echo "Source: $N8N_BASE_URL"
echo ""

RESPONSE=$(n8n_api GET "/workflows/$WORKFLOW_ID")

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
  --nodes)
    echo "$RESPONSE" | jq '{
      name,
      active,
      nodeCount: (.nodes | length),
      nodes: [.nodes[] | {name, type}]
    }'
    ;;
  --status|*)
    echo "$RESPONSE" | jq '{
      id,
      name,
      active,
      createdAt,
      updatedAt,
      nodeCount: (.nodes | length),
      triggerNode: .nodes[0].type
    }'
    ;;
esac
