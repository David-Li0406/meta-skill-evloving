#!/bin/bash
# Export n8n workflow to JSON file
# Usage: ./export-workflow.sh <workflow-id-or-name> [output-file.json]

source "$(dirname "$0")/_config.sh"

WORKFLOW_ID_OR_NAME="$1"
OUTPUT_FILE="$2"

if [ -z "$WORKFLOW_ID_OR_NAME" ]; then
  echo "Usage: $0 <workflow-id-or-name> [output-file.json]"
  echo ""
  echo "Examples:"
  echo "  $0 abc123def456                    # Export by ID to stdout"
  echo "  $0 abc123def456 workflow.json      # Export by ID to file"
  echo "  $0 \"My Workflow Name\" backup.json  # Export by name to file"
  exit 1
fi

# If input looks like an ID, use it directly. Otherwise, search by name.
if [[ "$WORKFLOW_ID_OR_NAME" =~ ^[a-zA-Z0-9_-]+$ ]] && [[ ${#WORKFLOW_ID_OR_NAME} -gt 10 ]]; then
  WORKFLOW_ID="$WORKFLOW_ID_OR_NAME"
else
  echo "Searching for workflow by name: $WORKFLOW_ID_OR_NAME"
  WORKFLOW_ID=$(n8n_api GET "/workflows" | \
    jq -r ".data[] | select(.name==\"$WORKFLOW_ID_OR_NAME\") | .id")

  if [ -z "$WORKFLOW_ID" ] || [ "$WORKFLOW_ID" == "null" ]; then
    error "Workflow not found: $WORKFLOW_ID_OR_NAME"
    exit 1
  fi
  success "Found workflow ID: $WORKFLOW_ID"
fi

echo "Exporting workflow: $WORKFLOW_ID"
echo "Source: $N8N_BASE_URL"

# Fetch workflow
WORKFLOW_JSON=$(n8n_api GET "/workflows/$WORKFLOW_ID")

# Check for errors
ERROR=$(echo "$WORKFLOW_JSON" | jq -r '.message // empty')
if [ -n "$ERROR" ]; then
  error "API Error: $ERROR"
  exit 1
fi

WORKFLOW_NAME=$(echo "$WORKFLOW_JSON" | jq -r '.name')
echo "Workflow name: $WORKFLOW_NAME"

# Output to file or stdout
if [ -n "$OUTPUT_FILE" ]; then
  echo "$WORKFLOW_JSON" | jq '.' > "$OUTPUT_FILE"
  success "Exported to: $OUTPUT_FILE"
  echo "$(wc -l < "$OUTPUT_FILE" | tr -d ' ') lines"
else
  echo ""
  echo "$WORKFLOW_JSON" | jq '.'
fi
