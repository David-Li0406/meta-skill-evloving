#!/usr/bin/env bash
# Check MiniMax MCP server status and health
# Verifies environment variables and connectivity

set -e

API_KEY="${MINIMAX_API_KEY:-sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c}"
API_HOST="${MINIMAX_API_HOST:-https://api.minimax.io}"

echo "=== MiniMax MCP Server Status Check ==="
echo ""

# Check API key
echo "1. API Key Status:"
if [ -z "$API_KEY" ]; then
    echo "   ❌ MINIMAX_API_KEY not set"
    exit 1
else
    KEY_LENGTH=${#API_KEY}
    echo "   ✅ MINIMAX_API_KEY set (${KEY_LENGTH} chars)"
fi

# Check API host
echo ""
echo "2. API Host Status:"
if [ -z "$API_HOST" ]; then
    echo "   ❌ MINIMAX_API_HOST not set"
    exit 1
else
    echo "   ✅ MINIMAX_API_HOST: $API_HOST"
fi

# Test connectivity
echo ""
echo "3. Connectivity Test:"
TEST_QUERY='{"q":"status check"}'
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${API_HOST}/v1/coding_plan/search" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -H "MM-API-Source: Minimax-MCP" \
    -d "$TEST_QUERY" 2>&1 || echo "000")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✅ API connectivity: OK (HTTP $HTTP_CODE)"
elif [ "$HTTP_CODE" = "000" ]; then
    echo "   ❌ Connection failed"
    echo "   Error: $BODY"
    exit 1
else
    echo "   ⚠️  API returned: HTTP $HTTP_CODE"
    echo "   Response: $BODY"
fi

# Check MCP server
echo ""
echo "4. MCP Server Status:"
if command -v uvx &> /dev/null; then
    echo "   ✅ uvx installed: $(uvx --version 2>&1 | head -n1)"
else
    echo "   ⚠️  uvx not found (required for MCP server)"
fi

echo ""
echo "=== Status Check Complete ==="
echo ""
echo "Environment:"
echo "  API_KEY: ${API_KEY:0:20}..."
echo "  API_HOST: $API_HOST"
echo ""
echo "Ready to use!"
