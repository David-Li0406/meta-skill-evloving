#!/bin/bash
# Test a webhook endpoint
# Usage: ./test-webhook.sh <webhook-url> [payload.json]

source "$(dirname "$0")/_config.sh"

WEBHOOK_URL="$1"
PAYLOAD_FILE="$2"

if [ -z "$WEBHOOK_URL" ]; then
  echo "Usage: $0 <webhook-url> [payload.json]"
  echo ""
  echo "Examples:"
  echo "  $0 https://n8n.example.com/webhook/abc123"
  echo "  $0 https://n8n.example.com/webhook/abc123 payload.json"
  echo "  $0 /webhook/abc123                    # Uses N8N_BASE_URL"
  echo ""
  echo "If webhook-url starts with /, N8N_BASE_URL is prepended."
  exit 1
fi

# Handle relative URLs
if [[ "$WEBHOOK_URL" == /* ]]; then
  WEBHOOK_URL="${N8N_BASE_URL}${WEBHOOK_URL}"
fi

echo "Testing webhook: $WEBHOOK_URL"
echo ""

# Determine payload
if [ -n "$PAYLOAD_FILE" ]; then
  if [ ! -f "$PAYLOAD_FILE" ]; then
    error "Payload file not found: $PAYLOAD_FILE"
    exit 1
  fi
  PAYLOAD=$(cat "$PAYLOAD_FILE")
  echo "Payload from: $PAYLOAD_FILE"
else
  PAYLOAD='{"test": true, "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}'
  echo "Using default test payload"
fi

echo ""
echo "Request:"
echo "$PAYLOAD" | jq '.'
echo ""

# Send request
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

# Split response body and status code
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

echo "Response (HTTP $HTTP_CODE):"
if [ -n "$BODY" ]; then
  echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
else
  echo "(empty)"
fi

# Check status
if [[ "$HTTP_CODE" =~ ^2 ]]; then
  echo ""
  success "Webhook responded successfully"
else
  echo ""
  error "Webhook returned HTTP $HTTP_CODE"
  exit 1
fi
