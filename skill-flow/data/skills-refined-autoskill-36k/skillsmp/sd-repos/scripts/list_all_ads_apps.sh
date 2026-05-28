#!/bin/bash
# List all ADS apps in the local SD directory

set -e

SD_DIR="/Users/kevin/git/glcp/sd"

if [ ! -d "$SD_DIR" ]; then
    echo "Error: SD directory not found at $SD_DIR"
    exit 1
fi

echo "ADS Applications in $SD_DIR:"
echo "======================================"

cd "$SD_DIR"
for repo in sd-*/; do
    repo_name=$(basename "$repo")
    topics=$(gh api "repos/glcp/$repo_name/topics" --jq '.names[]' 2>/dev/null)
    if echo "$topics" | grep -q "ads-app"; then
        echo "  ✅ $repo_name"
    fi
done
