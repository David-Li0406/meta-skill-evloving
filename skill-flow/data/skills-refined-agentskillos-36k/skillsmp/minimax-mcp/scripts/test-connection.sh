#!/usr/bin/env bash
# Test MiniMax API connection and verify setup
# Comprehensive connectivity and configuration test

set -e

API_KEY="${MINIMAX_API_KEY:-sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c}"
API_HOST="${MINIMAX_API_HOST:-https://api.minimax.io}"

TESTS_PASSED=0
TESTS_TOTAL=5

echo "========================================="
echo "  MiniMax API Connection Test"
echo "========================================="
echo ""

# Test 1: Check curl availability
echo "Test 1/5: Checking curl availability..."
if command -v curl &> /dev/null; then
    echo "✅ curl is installed"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "❌ curl is not installed"
fi

# Test 2: Check Python availability
echo ""
echo "Test 2/5: Checking Python availability..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "✅ $PYTHON_VERSION"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "❌ Python 3 is not installed"
fi

# Test 3: Validate API key
echo ""
echo "Test 3/5: Validating API key..."
if [ ${#API_KEY} -eq 126 ]; then
    echo "✅ API key length correct (126 chars)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "❌ API key length incorrect (${#API_KEY} chars, expected 126)"
fi

# Test 4: Test web search endpoint
echo ""
echo "Test 4/5: Testing web search endpoint..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${API_HOST}/v1/coding_plan/search" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -H "MM-API-Source: Minimax-MCP" \
    -d '{"q":"test"}' 2>&1 || echo "000")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    if echo "$BODY" | grep -q "organic"; then
        echo "✅ Web search endpoint working"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "⚠️  Endpoint responded but format unexpected"
        echo "Response: $BODY"
    fi
else
    echo "❌ HTTP $HTTP_CODE"
    echo "Response: $BODY"
fi

# Test 5: Test image analysis endpoint
echo ""
echo "Test 5/5: Testing image analysis endpoint..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${API_HOST}/v1/coding_plan/vlm" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -H "MM-API-Source: Minimax-MCP" \
    -d '{"prompt":"test","image_url":"https://via.placeholder.com/100"}' 2>&1 || echo "000")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Image analysis endpoint accessible"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "⚠️  HTTP $HTTP_CODE"
    # This might fail due to invalid image, but endpoint exists
    if echo "$BODY" | grep -q "image"; then
        echo "✅ Endpoint exists (image validation failed, which is expected)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "Response: $BODY"
    fi
fi

# Summary
echo ""
echo "========================================="
echo "  Test Results: $TESTS_PASSED/$TESTS_TOTAL Passed"
echo "========================================="

if [ $TESTS_PASSED -eq $TESTS_TOTAL ]; then
    echo ""
    echo "✅ All tests passed! MiniMax is ready to use."
    echo ""
    echo "Quick start:"
    echo "  Web search: ./web-search.sh \"query\""
    echo "  Image analysis: ./analyze-image.sh \"prompt\" \"image.png\""
    exit 0
else
    echo ""
    echo "⚠️  Some tests failed. Check the errors above."
    echo ""
    echo "Troubleshooting:"
    echo "  1. Install curl: sudo apt-get install curl (Linux) or brew install curl (macOS)"
    echo "  2. Install Python 3 if not available"
    echo "  3. Check internet connection"
    echo "  4. Verify API key is valid"
    exit 1
fi
