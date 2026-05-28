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

FILE_PATH="$1"
ALT_TEXT="${2:-}"

if [ -z "$FILE_PATH" ]; then
  echo "Usage: upload-file.sh <file-path> [alt-text]"
  echo ""
  echo "Supported formats: jpg, png, gif, webp, svg, mp4, mov, webm, pdf"
  exit 1
fi

if [ ! -f "$FILE_PATH" ]; then
  echo "Error: File not found: $FILE_PATH"
  exit 1
fi

API_VERSION="2024-10"
ENDPOINT="https://${STORE}.myshopify.com/admin/api/${API_VERSION}/graphql.json"

# Get file info
FILENAME=$(basename "$FILE_PATH")
FILESIZE=$(stat -f%z "$FILE_PATH" 2>/dev/null || stat -c%s "$FILE_PATH")
EXTENSION="${FILENAME##*.}"
EXTENSION_LOWER=$(echo "$EXTENSION" | tr '[:upper:]' '[:lower:]')

# Determine MIME type and resource type
case "$EXTENSION_LOWER" in
  jpg|jpeg) MIME_TYPE="image/jpeg"; RESOURCE="IMAGE" ;;
  png) MIME_TYPE="image/png"; RESOURCE="IMAGE" ;;
  gif) MIME_TYPE="image/gif"; RESOURCE="IMAGE" ;;
  webp) MIME_TYPE="image/webp"; RESOURCE="IMAGE" ;;
  svg) MIME_TYPE="image/svg+xml"; RESOURCE="IMAGE" ;;
  mp4) MIME_TYPE="video/mp4"; RESOURCE="VIDEO" ;;
  mov) MIME_TYPE="video/quicktime"; RESOURCE="VIDEO" ;;
  webm) MIME_TYPE="video/webm"; RESOURCE="VIDEO" ;;
  pdf) MIME_TYPE="application/pdf"; RESOURCE="FILE" ;;
  *) MIME_TYPE="application/octet-stream"; RESOURCE="FILE" ;;
esac

echo "Uploading: $FILENAME ($FILESIZE bytes, $MIME_TYPE)"
echo ""

# Step 1: Create staged upload
echo "Step 1: Creating staged upload target..."

STAGED_QUERY=$(cat <<EOF
mutation {
  stagedUploadsCreate(input: [{
    filename: \"$FILENAME\",
    mimeType: \"$MIME_TYPE\",
    fileSize: \"$FILESIZE\",
    resource: $RESOURCE,
    httpMethod: POST
  }]) {
    stagedTargets {
      url
      resourceUrl
      parameters {
        name
        value
      }
    }
    userErrors {
      field
      message
    }
  }
}
EOF
)

STAGED_QUERY_LINE=$(echo "$STAGED_QUERY" | tr '\n' ' ' | sed 's/  */ /g')

STAGED_RESPONSE=$(curl -s -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "X-Shopify-Access-Token: $ADMIN_API_TOKEN" \
  -d "{\"query\": \"$STAGED_QUERY_LINE\"}")

# Check for errors
if echo "$STAGED_RESPONSE" | grep -q "userErrors.*message"; then
  echo "Error creating staged upload:"
  echo "$STAGED_RESPONSE" | python3 -m json.tool
  exit 1
fi

# Extract upload URL and parameters
UPLOAD_URL=$(echo "$STAGED_RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d['data']['stagedUploadsCreate']['stagedTargets'][0]['url'])")
RESOURCE_URL=$(echo "$STAGED_RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d['data']['stagedUploadsCreate']['stagedTargets'][0]['resourceUrl'])")

echo "   Upload URL: $UPLOAD_URL"
echo ""

# Step 2: Upload file to staged target
echo "Step 2: Uploading file..."

# Build form data from parameters
FORM_PARAMS=""
while IFS= read -r line; do
  NAME=$(echo "$line" | cut -d'|' -f1)
  VALUE=$(echo "$line" | cut -d'|' -f2)
  FORM_PARAMS="$FORM_PARAMS -F \"$NAME=$VALUE\""
done < <(echo "$STAGED_RESPONSE" | python3 -c "
import sys, json
d = json.load(sys.stdin)
params = d['data']['stagedUploadsCreate']['stagedTargets'][0]['parameters']
for p in params:
    print(f\"{p['name']}|{p['value']}\")
")

# Execute upload with form params
eval "curl -s -X POST \"$UPLOAD_URL\" $FORM_PARAMS -F \"file=@$FILE_PATH\"" > /dev/null

echo "   File uploaded to staging"
echo ""

# Step 3: Create the file in Shopify
echo "Step 3: Creating file in Shopify..."

# Escape alt text for GraphQL
ALT_ESCAPED=$(echo "$ALT_TEXT" | sed 's/"/\\"/g')

CREATE_QUERY=$(cat <<EOF
mutation {
  fileCreate(files: [{
    alt: \"$ALT_ESCAPED\",
    contentType: $RESOURCE,
    originalSource: \"$RESOURCE_URL\"
  }]) {
    files {
      id
      alt
      createdAt
      fileStatus
      ... on MediaImage {
        image {
          url
        }
      }
      ... on Video {
        sources {
          url
        }
      }
    }
    userErrors {
      field
      message
    }
  }
}
EOF
)

CREATE_QUERY_LINE=$(echo "$CREATE_QUERY" | tr '\n' ' ' | sed 's/  */ /g')

CREATE_RESPONSE=$(curl -s -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "X-Shopify-Access-Token: $ADMIN_API_TOKEN" \
  -d "{\"query\": \"$CREATE_QUERY_LINE\"}")

echo ""
echo "Result:"
echo "$CREATE_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$CREATE_RESPONSE"
