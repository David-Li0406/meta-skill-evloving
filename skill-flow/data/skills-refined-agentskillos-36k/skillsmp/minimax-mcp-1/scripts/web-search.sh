#!/usr/bin/env bash
# Perform web search using MiniMax API
# Usage: ./web-search.sh "search query"

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 \"search query\""
    echo "Example: $0 \"Godot engine features\""
    exit 1
fi

QUERY="$1"
API_KEY="${MINIMAX_API_KEY:-sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c}"
API_HOST="${MINIMAX_API_HOST:-https://api.minimax.io}"

# Trusted domains for restricted search
TRUSTED_DOMAINS="site:docs.anthropic.com OR site:platform.claude.com OR site:docs.cursor.com OR site:cursor.com OR site:cookbook.openai.com OR site:godotengine.org OR site:api.minimax.io"

# Combine user query with trusted domain filter
RESTRICTED_QUERY="($TRUSTED_DOMAINS) $QUERY"

echo "Searching (trusted domains only): $QUERY"
echo ""

# Perform search with domain restriction
RESPONSE=$(curl -s -X POST "${API_HOST}/v1/coding_plan/search" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -H "MM-API-Source: Minimax-MCP" \
    -d "{\"q\":\"$RESTRICTED_QUERY\"}")

# Check for errors
if echo "$RESPONSE" | grep -q "base_resp"; then
    # Parse and display results
    echo "$RESPONSE" | python3 -c "
import sys
import json

data = json.load(sys.stdin)

if 'organic' in data:
    results = data['organic']
    print(f'Found {len(results)} results:\n')

    for i, result in enumerate(results, 1):
        title = result.get('title', 'No title')
        link = result.get('link', '')
        snippet = result.get('snippet', '')
        date = result.get('date', '')

        print(f'{i}. {title}')
        print(f'   {link}')
        if snippet:
            print(f'   {snippet[:150]}...')
        if date:
            print(f'   Date: {date}')
        print()
else:
    print('No results found')
"
else
    echo "Error: $RESPONSE"
    exit 1
fi
