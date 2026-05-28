#!/bin/bash
# Import n8n workflow from JSON file
# Usage: ./import-workflow.sh <workflow.json> [--update]

source "$(dirname "$0")/_config.sh"

WORKFLOW_FILE=""
UPDATE_MODE=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --update|-u)
      UPDATE_MODE=true
      shift
      ;;
    -h|--help)
      echo "Usage: $0 <workflow.json> [--update]"
      echo ""
      echo "Options:"
      echo "  --update, -u  Update existing workflow if name matches"
      echo ""
      echo "Without --update, creates new workflow (may duplicate names)."
      exit 0
      ;;
    *)
      WORKFLOW_FILE="$1"
      shift
      ;;
  esac
done

if [ -z "$WORKFLOW_FILE" ]; then
  echo "Usage: $0 <workflow.json> [--update]"
  exit 1
fi

if [ ! -f "$WORKFLOW_FILE" ]; then
  error "File not found: $WORKFLOW_FILE"
  exit 1
fi

# Get workflow name from JSON
WORKFLOW_NAME=$(jq -r '.name' "$WORKFLOW_FILE")
echo "Workflow: $WORKFLOW_NAME"
echo "Target: $N8N_BASE_URL"

if [ "$UPDATE_MODE" = true ]; then
  # Check if workflow exists (by name)
  EXISTING_ID=$(n8n_api GET "/workflows" | \
    jq -r ".data[] | select(.name==\"$WORKFLOW_NAME\") | .id")

  if [ -n "$EXISTING_ID" ] && [ "$EXISTING_ID" != "null" ]; then
    echo "Updating existing workflow: $EXISTING_ID"

    # n8n API requires PUT without read-only fields
    CLEAN_JSON=$(jq '{name, nodes, connections, settings}' "$WORKFLOW_FILE")
    RESPONSE=$(echo "$CLEAN_JSON" | n8n_api PUT "/workflows/$EXISTING_ID" "$(cat)")

    # Check for errors
    ERROR=$(echo "$RESPONSE" | jq -r '.message // empty')
    if [ -n "$ERROR" ]; then
      error "API Error: $ERROR"
      exit 1
    fi

    success "Updated workflow"
    echo "$RESPONSE" | jq '{id, name, active, updatedAt}'
    exit 0
  fi
fi

# Create new workflow
echo "Creating new workflow..."
RESPONSE=$(n8n_api POST "/workflows" "$(cat "$WORKFLOW_FILE")")

# Check for errors
ERROR=$(echo "$RESPONSE" | jq -r '.message // empty')
if [ -n "$ERROR" ]; then
  error "API Error: $ERROR"
  echo "$RESPONSE" | jq '.'
  exit 1
fi

NEW_ID=$(echo "$RESPONSE" | jq -r '.id')
if [ -n "$NEW_ID" ] && [ "$NEW_ID" != "null" ]; then
  success "Created workflow: $NEW_ID"
  echo "$RESPONSE" | jq '{id, name, active, createdAt}'
else
  error "Failed to create workflow"
  echo "$RESPONSE" | jq '.'
  exit 1
fi
