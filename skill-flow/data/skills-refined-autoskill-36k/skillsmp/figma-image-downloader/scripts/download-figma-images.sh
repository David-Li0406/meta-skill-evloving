#!/bin/bash
set -euo pipefail

# Check for required arguments
if [[ -z "${FIGMA_API_KEY:-}" ]] || [[ $# -eq 0 ]]; then
    echo "ERROR: Missing FIGMA_API_KEY or URL argument" >&2
    echo "Usage: FIGMA_API_KEY=your_key $0 <figma_url>" >&2
    exit 1
fi

FIGMA_URL="$1"

# Extract file key from URL (e.g., https://www.figma.com/design/ABC123/...)
FILE_KEY=$(echo "$FIGMA_URL" | sed -n 's|.*figma.com/design/\([^/]*\).*|\1|p')
if [[ -z "$FILE_KEY" ]]; then
    echo "ERROR: Invalid Figma URL - could not extract file key" >&2
    exit 1
fi

# Extract node-id if present and convert format (123-456 -> 123:456)
NODE_ID=$(echo "$FIGMA_URL" | grep -oP 'node-id=\K[^&]*' | tr '-' ':' || echo "")

# Create output directory
OUTPUT_DIR=".devorch/artifacts/figma-screenshots/$FILE_KEY"
mkdir -p "$OUTPUT_DIR"

# Fetch file data from Figma API
echo "Fetching Figma file data..."
FILE_DATA=$(curl -s -H "X-Figma-Token: $FIGMA_API_KEY" \
    "https://api.figma.com/v1/files/$FILE_KEY")

# Check for API errors
if echo "$FILE_DATA" | jq -e '.err' > /dev/null 2>&1; then
    echo "ERROR: Figma API error: $(echo "$FILE_DATA" | jq -r '.err')" >&2
    exit 1
fi

# Find the search node (either specific node-id or first page)
if [[ -n "$NODE_ID" ]]; then
    # Search for specific node recursively
    SEARCH_NODE=$(echo "$FILE_DATA" | jq --arg id "$NODE_ID" '
        def find_node:
            if .id == $id then .
            elif .children then .children[] | find_node
            else empty
            end;
        .document | find_node
    ')
else
    # Use first page
    SEARCH_NODE=$(echo "$FILE_DATA" | jq '.document.children[0]')
fi

if [[ "$SEARCH_NODE" == "null" ]] || [[ -z "$SEARCH_NODE" ]]; then
    echo "ERROR: Node not found" >&2
    exit 1
fi

# Extract all FRAME children
SCREEN_IDS=$(echo "$SEARCH_NODE" | jq -r '.children[] | select(.type == "FRAME") | .id' | paste -sd "," -)
SCREEN_NAMES=$(echo "$SEARCH_NODE" | jq -r '.children[] | select(.type == "FRAME") | .name')
SCREEN_COUNT=$(echo "$SEARCH_NODE" | jq '[.children[] | select(.type == "FRAME")] | length')

if [[ "$SCREEN_COUNT" -eq 0 ]]; then
    echo "ERROR: No screens found" >&2
    exit 1
fi

echo "Found $SCREEN_COUNT screens"

# Get image URLs from Figma
echo "Generating image URLs..."
IMAGES_DATA=$(curl -s -H "X-Figma-Token: $FIGMA_API_KEY" \
    "https://api.figma.com/v1/images/$FILE_KEY?ids=$SCREEN_IDS&format=png&scale=2")

# Check for API errors
if echo "$IMAGES_DATA" | jq -e '.err' > /dev/null 2>&1; then
    echo "ERROR: Figma Images API error: $(echo "$IMAGES_DATA" | jq -r '.err')" >&2
    exit 1
fi

# Download each screen
DOWNLOADED=0
while IFS= read -r screen_name; do
    # Get corresponding ID (same index)
    screen_id=$(echo "$SEARCH_NODE" | jq -r --arg name "$screen_name" \
        '.children[] | select(.type == "FRAME" and .name == $name) | .id')

    # Get image URL for this ID
    image_url=$(echo "$IMAGES_DATA" | jq -r --arg id "$screen_id" '.images[$id]')

    if [[ "$image_url" == "null" ]] || [[ -z "$image_url" ]]; then
        echo "⚠ Skipping '$screen_name' - no image URL" >&2
        continue
    fi

    # Sanitize filename
    file_name=$(echo "$screen_name" | tr -cs '[:alnum:]' '_' | tr '[:upper:]' '[:lower:]').png

    # Download image
    curl -s -o "$OUTPUT_DIR/$file_name" "$image_url"
    echo "✓ $screen_name"
    ((DOWNLOADED++))
done <<< "$SCREEN_NAMES"

echo ""
echo "✅ Downloaded $DOWNLOADED screens to $OUTPUT_DIR"
