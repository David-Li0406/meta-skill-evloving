#!/bin/bash
#
# Test API Endpoint Script
#
# Tests an API endpoint and reports status code and response time.
#
# Usage:
#   ./test-endpoint.sh <url> [method]
#
# Arguments:
#   url     - Required. The URL of the endpoint to test
#   method  - Optional. HTTP method (GET, POST, etc.). Default: GET
#
# Examples:
#   ./test-endpoint.sh https://api.example.com/health
#   ./test-endpoint.sh https://api.example.com/users POST
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
URL="${1:-}"
METHOD="${2:-GET}"

# Validate URL argument
if [ -z "$URL" ]; then
    echo -e "${RED}Error: URL argument is required${NC}"
    echo "Usage: $0 <url> [method]"
    exit 1
fi

# Convert method to uppercase
METHOD=$(echo "$METHOD" | tr '[:lower:]' '[:upper:]')

# Validate HTTP method
case "$METHOD" in
    GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)
        ;;
    *)
        echo -e "${RED}Error: Invalid HTTP method: $METHOD${NC}"
        echo "Supported methods: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS"
        exit 1
        ;;
esac

echo "============================================"
echo "API Endpoint Test"
echo "============================================"
echo "URL:    $URL"
echo "Method: $METHOD"
echo "Time:   $(date -Iseconds)"
echo "--------------------------------------------"

# Make the request and capture timing/status
START_TIME=$(date +%s.%N)

HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}|%{time_total}|%{size_download}" \
    -X "$METHOD" \
    -H "Accept: application/json" \
    -H "User-Agent: test-endpoint/1.0" \
    --connect-timeout 10 \
    --max-time 30 \
    "$URL" 2>&1) || true

END_TIME=$(date +%s.%N)

# Parse response
HTTP_CODE=$(echo "$HTTP_RESPONSE" | cut -d'|' -f1)
RESPONSE_TIME=$(echo "$HTTP_RESPONSE" | cut -d'|' -f2)
RESPONSE_SIZE=$(echo "$HTTP_RESPONSE" | cut -d'|' -f3)

# Handle curl errors
if [ -z "$HTTP_CODE" ] || [ "$HTTP_CODE" = "000" ]; then
    echo -e "${RED}✗ Connection failed${NC}"
    echo "Could not connect to the endpoint"
    exit 1
fi

# Display results
echo ""
echo "Results:"
echo "--------"
echo "Status Code:   $HTTP_CODE"
echo "Response Time: ${RESPONSE_TIME}s"
echo "Response Size: ${RESPONSE_SIZE} bytes"
echo ""

# Determine status category and display appropriate message
if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
    echo -e "${GREEN}✓ Success${NC} - Endpoint returned $HTTP_CODE"
    EXIT_CODE=0
elif [ "$HTTP_CODE" -ge 300 ] && [ "$HTTP_CODE" -lt 400 ]; then
    echo -e "${YELLOW}→ Redirect${NC} - Endpoint returned $HTTP_CODE"
    EXIT_CODE=0
elif [ "$HTTP_CODE" -ge 400 ] && [ "$HTTP_CODE" -lt 500 ]; then
    echo -e "${RED}✗ Client Error${NC} - Endpoint returned $HTTP_CODE"
    EXIT_CODE=1
elif [ "$HTTP_CODE" -ge 500 ]; then
    echo -e "${RED}✗ Server Error${NC} - Endpoint returned $HTTP_CODE"
    EXIT_CODE=1
else
    echo -e "${YELLOW}? Unknown${NC} - Endpoint returned $HTTP_CODE"
    EXIT_CODE=1
fi

echo "============================================"
exit $EXIT_CODE

