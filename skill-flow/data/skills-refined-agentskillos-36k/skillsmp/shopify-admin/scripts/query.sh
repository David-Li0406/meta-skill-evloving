#!/bin/bash
set -e

# Check required env vars
if [ -z "$STORE" ]; then
  echo "Error: STORE environment variable not set"
  exit 1
fi

if [ -z "$ADMIN_API_TOKEN" ]; then
  echo "Error: ADMIN_API_TOKEN environment variable not set"
  exit 1
fi

QUERY="$1"

if [ -z "$QUERY" ]; then
  echo "Usage: query.sh 'GRAPHQL_QUERY'"
  exit 1
fi

API_VERSION="2024-10"
ENDPOINT="https://${STORE}.myshopify.com/admin/api/${API_VERSION}/graphql.json"

curl -s -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "X-Shopify-Access-Token: $ADMIN_API_TOKEN" \
  -d "{\"query\": \"$QUERY\"}"
