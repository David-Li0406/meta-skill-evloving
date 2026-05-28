#!/usr/bin/env bash
# Analyze images using MiniMax vision API
# Usage: ./analyze-image.sh "prompt" "image_path_or_url"

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 \"prompt\" \"image_path_or_url\""
    echo "Example: $0 \"What do you see?\" \"screenshot.png\""
    echo "Example: $0 \"Describe this UI\" \"https://example.com/image.png\""
    exit 1
fi

PROMPT="$1"
IMAGE="$2"
API_KEY="${MINIMAX_API_KEY:-sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c}"
API_HOST="${MINIMAX_API_HOST:-https://api.minimax.io}"

# Determine if image is URL or local file
if [[ "$IMAGE" =~ ^https?:// ]]; then
    IMAGE_TYPE="url"
    IMAGE_DATA="{\"prompt\":\"$PROMPT\",\"image_url\":\"$IMAGE\"}"
else
    # For local files, convert to base64
    if [ ! -f "$IMAGE" ]; then
        echo "Error: Image file not found: $IMAGE"
        exit 1
    fi
    IMAGE_TYPE="base64"
    IMAGE_BASE64=$(base64 -w 0 "$IMAGE" 2>/dev/null || base64 "$IMAGE")
    IMAGE_DATA="{\"prompt\":\"$PROMPT\",\"image_base64\":\"$IMAGE_BASE64\"}"
fi

echo "Analyzing image: $IMAGE"
echo "Prompt: $PROMPT"
echo ""

# Perform analysis
RESPONSE=$(curl -s -X POST "${API_HOST}/v1/coding_plan/vlm" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -H "MM-API-Source: Minimax-MCP" \
    -d "$IMAGE_DATA")

# Check for errors and display result
if echo "$RESPONSE" | grep -q "base_resp"; then
    echo "$RESPONSE" | python3 -c "
import sys
import json

data = json.load(sys.stdin)

if 'output' in data:
    output = data['output']
    if 'text' in output:
        print(output['text'])
    else:
        print(json.dumps(output, indent=2))
elif 'error' in data:
    print('Error:', data['error'])
else:
    print('Response:', json.dumps(data, indent=2))
"
else
    echo "Error: $RESPONSE"
    exit 1
fi
