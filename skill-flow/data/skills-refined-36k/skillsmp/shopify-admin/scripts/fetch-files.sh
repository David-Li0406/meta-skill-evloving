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
LIMIT=20
FILE_TYPE="ALL"  # ALL, IMAGE, VIDEO, DOCUMENT

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --limit)
      LIMIT="$2"
      shift 2
      ;;
    --type)
      FILE_TYPE="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

API_VERSION="2024-10"
ENDPOINT="https://${STORE}.myshopify.com/admin/api/${API_VERSION}/graphql.json"

# Build query filter based on type
if [ "$FILE_TYPE" = "ALL" ]; then
  QUERY_FILTER=""
else
  QUERY_FILTER="query: \\\"media_type:${FILE_TYPE}\\\","
fi

GRAPHQL_QUERY=$(cat <<EOF
{
  files(first: ${LIMIT}, ${QUERY_FILTER} sortKey: CREATED_AT, reverse: true) {
    edges {
      node {
        id
        alt
        createdAt
        fileStatus
        ... on MediaImage {
          image {
            url
            width
            height
          }
          mimeType
        }
        ... on Video {
          sources {
            url
            mimeType
            width
            height
          }
          duration
        }
        ... on GenericFile {
          url
          mimeType
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
