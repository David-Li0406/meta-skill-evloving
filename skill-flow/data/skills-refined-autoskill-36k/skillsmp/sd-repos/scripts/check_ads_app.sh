#!/bin/bash
# Check if a repository is an ADS app by checking for the ads-app GitHub topic

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <repo-name>"
    echo "Example: $0 sd-data-service"
    exit 1
fi

REPO_NAME=$1

# Check if the repo has the ads-app topic
if gh api "repos/glcp/${REPO_NAME}/topics" --jq '.names[]' 2>/dev/null | grep -q "ads-app"; then
    echo "✅ ${REPO_NAME} is an ADS app"
    exit 0
else
    echo "❌ ${REPO_NAME} is NOT an ADS app"
    exit 1
fi
