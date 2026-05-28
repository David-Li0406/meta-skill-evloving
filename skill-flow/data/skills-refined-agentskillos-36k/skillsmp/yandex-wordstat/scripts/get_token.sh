#!/bin/bash
# Get Yandex OAuth token for Wordstat API

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$SCRIPT_DIR/../config"
ENV_FILE="$CONFIG_DIR/.env"

CLIENT_ID=""
CLIENT_SECRET=""

# Parse args
while [[ $# -gt 0 ]]; do
    case $1 in
        --client-id|-i) CLIENT_ID="$2"; shift 2 ;;
        --client-secret|-s) CLIENT_SECRET="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [[ -z "$CLIENT_ID" ]]; then
    echo "Usage: get_token.sh --client-id YOUR_CLIENT_ID [--client-secret YOUR_SECRET]"
    echo ""
    echo "Options:"
    echo "  --client-id, -i      OAuth client ID (required)"
    echo "  --client-secret, -s  OAuth client secret (optional, for code exchange)"
    echo ""
    echo "Get credentials at: https://oauth.yandex.ru/client/new"
    echo ""
    echo "Two modes:"
    echo "  1. Without secret: Opens browser URL, you copy token manually"
    echo "  2. With secret: Exchange authorization code for token"
    exit 1
fi

echo "=== Yandex OAuth Token Setup ==="
echo ""

if [[ -z "$CLIENT_SECRET" ]]; then
    # Simple mode: token in URL fragment
    echo "Step 1: Open this URL in your browser:"
    echo ""
    echo "  https://oauth.yandex.ru/authorize?response_type=token&client_id=$CLIENT_ID"
    echo ""
    echo "Step 2: Authorize the application"
    echo ""
    echo "Step 3: Copy the token from the redirect URL:"
    echo "  https://oauth.yandex.ru/#access_token=YOUR_TOKEN_HERE&..."
    echo ""
    echo -n "Paste your token here: "
    read -r TOKEN

    if [[ -z "$TOKEN" ]]; then
        echo "Error: No token provided"
        exit 1
    fi
else
    # Code exchange mode
    echo "Step 1: Open this URL in your browser:"
    echo ""
    echo "  https://oauth.yandex.ru/authorize?response_type=code&client_id=$CLIENT_ID"
    echo ""
    echo "Step 2: Authorize the application"
    echo ""
    echo "Step 3: Copy the code from the redirect URL or page"
    echo ""
    echo -n "Paste the authorization code here: "
    read -r AUTH_CODE

    if [[ -z "$AUTH_CODE" ]]; then
        echo "Error: No code provided"
        exit 1
    fi

    echo ""
    echo "Exchanging code for token..."

    RESPONSE=$(curl -s -X POST "https://oauth.yandex.ru/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "grant_type=authorization_code" \
        -d "code=$AUTH_CODE" \
        -d "client_id=$CLIENT_ID" \
        -d "client_secret=$CLIENT_SECRET")

    # Extract token
    TOKEN=$(echo "$RESPONSE" | grep -o '"access_token":"[^"]*"' | sed 's/"access_token":"//' | tr -d '"')

    if [[ -z "$TOKEN" ]]; then
        echo "Error: Failed to get token"
        echo "$RESPONSE"
        exit 1
    fi

    # Show expiration
    EXPIRES=$(echo "$RESPONSE" | grep -o '"expires_in":[0-9]*' | sed 's/"expires_in"://')
    if [[ -n "$EXPIRES" ]]; then
        DAYS=$((EXPIRES / 86400))
        echo "Token expires in: $DAYS days"
    fi
fi

echo ""
echo "Token received!"
echo ""

# Save to .env
if [[ -f "$ENV_FILE" ]]; then
    # Update existing file
    if grep -q "^YANDEX_WORDSTAT_TOKEN=" "$ENV_FILE"; then
        # Replace existing token
        sed -i.bak "s/^YANDEX_WORDSTAT_TOKEN=.*/YANDEX_WORDSTAT_TOKEN=$TOKEN/" "$ENV_FILE"
        rm -f "$ENV_FILE.bak"
        echo "Updated token in: $ENV_FILE"
    else
        # Append
        echo "YANDEX_WORDSTAT_TOKEN=$TOKEN" >> "$ENV_FILE"
        echo "Added token to: $ENV_FILE"
    fi
else
    # Create new file
    echo "YANDEX_WORDSTAT_TOKEN=$TOKEN" > "$ENV_FILE"
    echo "Created: $ENV_FILE"
fi

echo ""
echo "Verifying token..."
echo ""

# Test the token
bash "$SCRIPT_DIR/quota.sh"
