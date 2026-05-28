#!/bin/bash
# Nano Banana PRO Image Generation Script
# Usage: ./generate-image.sh "prompt" output.png [options]
#
# Options:
#   --model MODEL    gemini-3-pro-image-preview (default) or gemini-2.5-flash-image
#   --ratio RATIO    Aspect ratio: 1:1, 16:9, 9:16, 4:3, 3:4, etc. (default: 1:1)
#   --size SIZE      Resolution: 1K, 2K, 4K (default: 2K, PRO model only for 4K)
#   --search         Enable Google Search grounding for real-time data
#   --input FILE     Input image for editing (base64 encoded or file path)

set -e

# Check for API key
if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY environment variable not set"
    exit 1
fi

# Default values
MODEL="gemini-3-pro-image-preview"
RATIO="1:1"
SIZE="2K"
SEARCH=""
INPUT_IMAGE=""

# Parse arguments
PROMPT="$1"
OUTPUT="$2"
shift 2 || true

while [[ $# -gt 0 ]]; do
    case $1 in
        --model)
            MODEL="$2"
            shift 2
            ;;
        --ratio)
            RATIO="$2"
            shift 2
            ;;
        --size)
            SIZE="$2"
            shift 2
            ;;
        --search)
            SEARCH="true"
            shift
            ;;
        --input)
            INPUT_IMAGE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [ -z "$PROMPT" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 \"prompt\" output.png [options]"
    echo ""
    echo "Options:"
    echo "  --model MODEL    gemini-3-pro-image-preview (default) or gemini-2.5-flash-image"
    echo "  --ratio RATIO    Aspect ratio: 1:1, 16:9, 9:16, 4:3, 3:4, etc."
    echo "  --size SIZE      Resolution: 1K, 2K, 4K"
    echo "  --search         Enable Google Search grounding"
    echo "  --input FILE     Input image for editing"
    exit 1
fi

# Build the API URL
API_URL="https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent"

# Build parts array
if [ -n "$INPUT_IMAGE" ]; then
    # Check if it's a file path or base64
    if [ -f "$INPUT_IMAGE" ]; then
        MIME_TYPE=$(file --mime-type -b "$INPUT_IMAGE")
        BASE64_DATA=$(base64 -w 0 "$INPUT_IMAGE")
    else
        BASE64_DATA="$INPUT_IMAGE"
        MIME_TYPE="image/png"
    fi
    
    PARTS=$(cat <<EOF
[
    {"text": "$PROMPT"},
    {"inline_data": {"mime_type": "$MIME_TYPE", "data": "$BASE64_DATA"}}
]
EOF
)
else
    PARTS=$(cat <<EOF
[{"text": "$PROMPT"}]
EOF
)
fi

# Build tools array if search is enabled
if [ -n "$SEARCH" ]; then
    TOOLS='"tools": [{"google_search": {}}],'
else
    TOOLS=""
fi

# Build the request body
REQUEST_BODY=$(cat <<EOF
{
    "contents": [{
        "parts": $PARTS
    }],
    $TOOLS
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"],
        "imageConfig": {
            "aspectRatio": "$RATIO",
            "imageSize": "$SIZE"
        }
    }
}
EOF
)

# Make the API call
echo "Generating image with $MODEL..."
echo "Prompt: $PROMPT"
echo "Aspect Ratio: $RATIO, Size: $SIZE"

RESPONSE=$(curl -s -X POST "$API_URL" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$REQUEST_BODY")

# Check for errors
if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
    echo "API Error:"
    echo "$RESPONSE" | jq '.error'
    exit 1
fi

# Extract and save the image
IMAGE_DATA=$(echo "$RESPONSE" | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' 2>/dev/null | head -1)

if [ -z "$IMAGE_DATA" ] || [ "$IMAGE_DATA" = "null" ]; then
    echo "No image data in response"
    echo "Response text:"
    echo "$RESPONSE" | jq -r '.candidates[0].content.parts[] | select(.text) | .text' 2>/dev/null
    exit 1
fi

echo "$IMAGE_DATA" | base64 -d > "$OUTPUT"
echo "Image saved to: $OUTPUT"

# Also output any text response
TEXT_RESPONSE=$(echo "$RESPONSE" | jq -r '.candidates[0].content.parts[] | select(.text) | .text' 2>/dev/null)
if [ -n "$TEXT_RESPONSE" ] && [ "$TEXT_RESPONSE" != "null" ]; then
    echo ""
    echo "Model response:"
    echo "$TEXT_RESPONSE"
fi
