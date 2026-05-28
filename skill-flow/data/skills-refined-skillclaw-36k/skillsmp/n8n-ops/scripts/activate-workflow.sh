#!/bin/bash
# Activate an n8n workflow
# Usage: ./activate-workflow.sh <workflow-id>

source "$(dirname "$0")/_config.sh"

WORKFLOW_ID="$1"

if [ -z "$WORKFLOW_ID" ]; then
  echo "Usage: $0 <workflow-id>"
  exit 1
fi

echo "Activating workflow: $WORKFLOW_ID"
echo "Target: $N8N_BASE_URL"

RESPONSE=$(n8n_api POST "/workflows/$WORKFLOW_ID/activate")

# Check for errors
ERROR=$(echo "$RESPONSE" | jq -r '.message // empty')
if [ -n "$ERROR" ]; then
  error "API Error: $ERROR"
  exit 1
fi

ACTIVE=$(echo "$RESPONSE" | jq -r '.active')
if [ "$ACTIVE" == "true" ]; then
  success "Workflow activated"
  echo "$RESPONSE" | jq '{id, name, active}'
else
  warn "Workflow may not be active"
  echo "$RESPONSE" | jq '.'
fi
