#!/bin/bash
# Reactivate an n8n workflow (deactivate + wait + activate)
# Useful for refreshing webhook registrations
# Usage: ./reactivate-workflow.sh <workflow-id> [wait-seconds]

source "$(dirname "$0")/_config.sh"

WORKFLOW_ID="$1"
WAIT_SECONDS="${2:-3}"

if [ -z "$WORKFLOW_ID" ]; then
  echo "Usage: $0 <workflow-id> [wait-seconds]"
  echo ""
  echo "Options:"
  echo "  wait-seconds  Seconds to wait between deactivate/activate (default: 3)"
  exit 1
fi

echo "Reactivating workflow: $WORKFLOW_ID"
echo "Target: $N8N_BASE_URL"
echo ""

# Step 1: Deactivate
echo "1. Deactivating..."
RESPONSE=$(n8n_api POST "/workflows/$WORKFLOW_ID/deactivate")
ERROR=$(echo "$RESPONSE" | jq -r '.message // empty')
if [ -n "$ERROR" ]; then
  error "Deactivate failed: $ERROR"
  exit 1
fi
echo "$RESPONSE" | jq '{active}'

# Step 2: Wait
echo ""
echo "2. Waiting ${WAIT_SECONDS}s..."
sleep "$WAIT_SECONDS"

# Step 3: Activate
echo ""
echo "3. Activating..."
RESPONSE=$(n8n_api POST "/workflows/$WORKFLOW_ID/activate")
ERROR=$(echo "$RESPONSE" | jq -r '.message // empty')
if [ -n "$ERROR" ]; then
  error "Activate failed: $ERROR"
  exit 1
fi

ACTIVE=$(echo "$RESPONSE" | jq -r '.active')
if [ "$ACTIVE" == "true" ]; then
  echo ""
  success "Workflow reactivated"
  echo "$RESPONSE" | jq '{id, name, active, triggerCount}'
else
  warn "Workflow may not be active"
  echo "$RESPONSE" | jq '.'
fi
