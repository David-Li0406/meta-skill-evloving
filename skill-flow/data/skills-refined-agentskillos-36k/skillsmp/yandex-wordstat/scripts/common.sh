#!/bin/bash
# Common functions for Yandex Wordstat API

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../config/.env"
CACHE_DIR="$SCRIPT_DIR/../cache"
API_URL="https://api.direct.yandex.com/json/v5/"

# Load config
load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        # shellcheck disable=SC1090
        source "$CONFIG_FILE"
    fi

    if [[ -z "$YANDEX_WORDSTAT_TOKEN" ]]; then
        echo "Error: YANDEX_WORDSTAT_TOKEN not found."
        echo "Set in config/.env or environment. See config/README.md for instructions."
        exit 1
    fi
}

# Make API request
# Usage: api_request "method" "params_json"
api_request() {
    local method="$1"
    local params="$2"

    local payload
    if [[ -n "$params" ]]; then
        payload="{\"method\":\"$method\",\"params\":$params}"
    else
        payload="{\"method\":\"$method\"}"
    fi

    curl -s -X POST "$API_URL" \
        -H "Authorization: Bearer $YANDEX_WORDSTAT_TOKEN" \
        -H "Content-Type: application/json; charset=utf-8" \
        -H "Accept-Language: ru" \
        -d "$payload"
}

# Make Wordstat API request
# Endpoint: https://api.wordstat.yandex.net/v1/{method}
# Methods: topRequests, dynamics, regions
wordstat_request() {
    local method="$1"
    local params="$2"

    local ws_url="https://api.wordstat.yandex.net/v1/$method"

    curl -s -X POST "$ws_url" \
        -H "Authorization: Bearer $YANDEX_WORDSTAT_TOKEN" \
        -H "Content-Type: application/json; charset=utf-8" \
        -d "$params"
}

# Extract JSON value using grep/sed (no jq dependency)
# Usage: json_value "$json" "key"
json_value() {
    local json="$1"
    local key="$2"
    echo "$json" | grep -o "\"$key\":[^,}]*" | head -1 | sed 's/.*://' | tr -d '"[:space:]'
}

# Extract JSON string value (handles strings with quotes)
json_string() {
    local json="$1"
    local key="$2"
    echo "$json" | grep -o "\"$key\":\"[^\"]*\"" | head -1 | sed 's/.*:"//' | tr -d '"'
}

# Extract JSON array
json_array() {
    local json="$1"
    local key="$2"
    echo "$json" | grep -o "\"$key\":\[[^]]*\]" | head -1 | sed 's/.*:\[/[/'
}

# Wait for async report with polling
# Usage: wait_for_report "report_id" "get_method" [max_attempts]
wait_for_report() {
    local report_id="$1"
    local get_method="$2"
    local max_attempts="${3:-30}"
    local attempt=0

    while [[ $attempt -lt $max_attempts ]]; do
        local response
        response=$(wordstat_request "$get_method" "$report_id")

        # Check if report is ready (has data array)
        if echo "$response" | grep -q '"data":\['; then
            echo "$response"
            return 0
        fi

        # Check for error
        if echo "$response" | grep -q '"error"'; then
            echo "$response"
            return 1
        fi

        echo "Waiting for report... ($((attempt + 1))/$max_attempts)" >&2
        sleep 2
        attempt=$((attempt + 1))
    done

    echo "Error: Timeout waiting for report" >&2
    return 1
}

# Escape string for JSON
json_escape() {
    local str="$1"
    str="${str//\\/\\\\}"
    str="${str//\"/\\\"}"
    str="${str//$'\n'/\\n}"
    str="${str//$'\t'/\\t}"
    echo "$str"
}

# Format number with thousands separator (macOS compatible)
format_number() {
    local num="$1"
    # Use printf for cross-platform compatibility
    printf "%'d" "$num" 2>/dev/null || echo "$num"
}
