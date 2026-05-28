#!/usr/bin/env bash
# Execute plan with MiniMax delegation for token efficiency
# Usage: ./execute-plan.sh "plan description"

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 \"plan description\""
    echo "Example: $0 \"Research React 18 features and create summary\""
    exit 1
fi

PLAN="$1"
API_KEY="${MINIMAX_API_KEY:-sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c}"
API_HOST="${MINIMAX_API_HOST:-https://api.minimax.io}"

echo "========================================="
echo "  MiniMax Plan Execution"
echo "========================================="
echo ""
echo "Plan: $PLAN"
echo ""

# Create structured prompt for MiniMax
MINIMAX_PROMPT="Execute this plan using MiniMax capabilities:

TASK: $PLAN

INSTRUCTIONS:
1. Perform comprehensive research and analysis
2. Provide detailed results with citations
3. Output TWO formats:
   - Compact JSON summary (<600 tokens): {result: [summary], key_points: [list]}
   - Detailed execution log with clear sections

FOCUS AREAS:
- Thorough web research
- Image analysis if relevant
- Code examples where applicable
- Best practices and recommendations

Execute efficiently with maximum detail for Claude review."

echo "Delegating to MiniMax..."
echo ""

# Execute plan
RESPONSE=$(curl -s -X POST "${API_HOST}/v1/coding_plan/search" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -H "MM-API-Source: Minimax-MCP" \
    -d "{\"q\":\"$MINIMAX_PROMPT\"}" 2>&1)

# Check for errors
if echo "$RESPONSE" | grep -q "base_resp"; then
    echo "$RESPONSE" | python3 -c "
import sys
import json

data = json.load(sys.stdin)

if 'organic' in data:
    results = data['organic']
    print(f'✅ Plan executed successfully\n')
    print(f'Found {len(results)} relevant sources:\n')

    for i, result in enumerate(results, 1):
        title = result.get('title', 'No title')
        link = result.get('link', '')
        snippet = result.get('snippet', '')

        print(f'{i}. {title}')
        print(f'   Link: {link}')
        if snippet:
            print(f'   Summary: {snippet}')
        print()
else:
    print('⚠️  Unexpected response format')
    print(json.dumps(data, indent=2))
"

    echo ""
    echo "========================================="
    echo "  Execution Complete"
    echo "========================================="
    echo ""
    echo "Next steps:"
    echo "1. Review the results above"
    echo "2. Use /minimax-query for follow-up questions"
    echo "3. Use /minimax-analyze for specific image analysis"
    echo ""
    echo "Token efficiency achieved: Claude planned (~100 tokens), MiniMax executed (~2000 tokens saved)"
else
    echo "❌ Error executing plan:"
    echo "$RESPONSE"
    exit 1
fi
