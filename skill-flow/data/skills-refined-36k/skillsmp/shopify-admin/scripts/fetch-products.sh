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

# Defaults
LIMIT=10
SEARCH_QUERY=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --limit)
      LIMIT="$2"
      shift 2
      ;;
    --query)
      SEARCH_QUERY="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

API_VERSION="2024-10"
ENDPOINT="https://${STORE}.myshopify.com/admin/api/${API_VERSION}/graphql.json"

# Build query filter
QUERY_FILTER=""
if [ -n "$SEARCH_QUERY" ]; then
  QUERY_FILTER="query: \\\"title:*${SEARCH_QUERY}*\\\","
fi

GRAPHQL_QUERY=$(cat <<EOF
{
  products(first: ${LIMIT}, ${QUERY_FILTER} sortKey: TITLE) {
    edges {
      node {
        id
        title
        handle
        status
        vendor
        productType
        createdAt
        updatedAt
        variants(first: 5) {
          edges {
            node {
              id
              title
              sku
              price
              inventoryQuantity
            }
          }
        }
        images(first: 1) {
          edges {
            node {
              url
              altText
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
EOF
)

# Remove newlines for JSON
QUERY_SINGLE_LINE=$(echo "$GRAPHQL_QUERY" | tr '\n' ' ' | sed 's/  */ /g')

curl -s -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "X-Shopify-Access-Token: $ADMIN_API_TOKEN" \
  -d "{\"query\": \"$QUERY_SINGLE_LINE\"}" | python3 -m json.tool 2>/dev/null || cat
