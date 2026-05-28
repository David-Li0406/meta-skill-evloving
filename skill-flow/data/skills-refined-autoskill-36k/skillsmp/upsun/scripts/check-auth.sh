#!/usr/bin/env bash
#
# check-auth.sh - Verify Upsun authentication status
#
# Usage: ./check-auth.sh
#
# Returns:
#   0 - Authenticated successfully
#   1 - Not authenticated
#
# Description:
#   Checks if the user is currently authenticated to Upsun.
#   If not authenticated, provides guidance on how to log in.
#

set -euo pipefail

# Check authentication status
if upsun auth:info --no-interaction >/dev/null 2>&1; then
    echo "✅ Authenticated to Upsun"
    upsun auth:info --no-interaction
    exit 0
else
    echo "❌ Not authenticated to Upsun"
    echo ""
    echo "To authenticate, run one of the following commands:"
    echo ""
    echo "  Browser-based login (recommended):"
    echo "    upsun auth:browser-login"
    echo ""
    echo "  API token login:"
    echo "    upsun auth:api-token-login"
    echo ""
    exit 1
fi
