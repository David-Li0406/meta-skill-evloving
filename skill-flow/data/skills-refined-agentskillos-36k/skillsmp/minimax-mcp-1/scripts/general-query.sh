#!/usr/bin/env bash
# Send general queries to MiniMax
# Usage: ./general-query.sh "your question"

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 \"your question\""
    echo "Example: $0 \"Explain quantum computing basics\""
    exit 1
fi

QUERY="$1"
API_KEY="${MINIMAX_API_KEY:-sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c}"
API_HOST="${MINIMAX_API_HOST:-https://api.minimax.io}"

echo "Query: $QUERY"
echo ""

# Query MiniMax via web search (using search as a general query mechanism)
RESPONSE=$(curl -s -X POST "${API_HOST}/v1/coding_plan/search" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -H "MM-API-Source: Minimax-MCP" \
    -d "{\"q\":\"$QUERY\"}" 2>&1)

# Process and display results
if echo "$RESPONSE" | grep -q "base_resp"; then
    echo "$RESPONSE" | python3 -c "
import sys
import json

data = json.load(sys.stdin)

if 'organic' in data:
    results = data['organic']
    print(f'MiniMax found {len(results)} relevant results:\n')

    for i, result in enumerate(results, 1):
        title = result.get('title', 'No title')
        link = result.get('link', '')
        snippet = result.get('snippet', '')

        print(f'{i}. {title}')
        print(f'   {link}')
        if snippet:
            print(f'   {snippet}')
        print()
else:
    print('MiniMax Response:')
    print(json.dumps(data, indent=2))
"
else
    echo "Response: $RESPONSE"
fi
