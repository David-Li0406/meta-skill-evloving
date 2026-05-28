#!/bin/bash
# Check Yandex Wordstat API connection

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

load_config

echo "Checking Wordstat API connection..."
echo ""

# Test with a simple regions request
response=$(wordstat_request "regions" '{"phrase":"тест"}')

if echo "$response" | grep -q '"regions"'; then
    echo "Wordstat API: OK"
    echo ""

    # Count regions in response
    region_count=$(echo "$response" | grep -o '"regionId"' | wc -l | tr -d ' ')
    echo "Test query 'тест' returned data for $region_count regions"
else
    echo "Wordstat API: Error"
    echo "$response"
    exit 1
fi

echo ""
echo "=== API Limits ==="
echo "- Rate limit: 10 requests/second"
echo "- Daily quota: 1000 requests"
echo ""
echo "=== Available endpoints ==="
echo "- /v1/topRequests - top search phrases"
echo "- /v1/dynamics   - search volume over time"
echo "- /v1/regions    - regional distribution"
echo ""
echo "Token is valid and API is accessible."
