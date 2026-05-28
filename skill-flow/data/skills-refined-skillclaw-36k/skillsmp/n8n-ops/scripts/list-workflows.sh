#!/bin/bash
# List all n8n workflows
# Usage: ./list-workflows.sh [--active|--inactive]

source "$(dirname "$0")/_config.sh"

FILTER=""
while [[ $# -gt 0 ]]; do
  case $1 in
    --active)
      FILTER="active"
      shift
      ;;
    --inactive)
      FILTER="inactive"
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [--active|--inactive]"
      echo ""
      echo "Options:"
      echo "  --active    Show only active workflows"
      echo "  --inactive  Show only inactive workflows"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

echo "Fetching workflows from: $N8N_BASE_URL"
echo ""

RESPONSE=$(n8n_api GET "/workflows")

# Check for errors
ERROR=$(echo "$RESPONSE" | jq -r '.message // empty')
if [ -n "$ERROR" ]; then
  error "API Error: $ERROR"
  exit 1
fi

# Apply filter if specified
if [ "$FILTER" == "active" ]; then
  echo "$RESPONSE" | jq -r '.data[] | select(.active == true) | "\(.id)\t\(.active)\t\(.name)"' | column -t -s $'\t'
elif [ "$FILTER" == "inactive" ]; then
  echo "$RESPONSE" | jq -r '.data[] | select(.active == false) | "\(.id)\t\(.active)\t\(.name)"' | column -t -s $'\t'
else
  echo "$RESPONSE" | jq -r '.data[] | "\(.id)\t\(.active)\t\(.name)"' | column -t -s $'\t'
fi

TOTAL=$(echo "$RESPONSE" | jq '.data | length')
echo ""
echo "Total: $TOTAL workflows"
