#!/bin/bash
# deep-search.sh - Advanced Git Forensics Helper
# Usage: ./deep-search.sh <pattern>

if [ -z "$1" ]; then
    echo "Usage: $0 <search_pattern>"
    exit 1
fi

PATTERN=$1

echo "--- Searching all branches for: $PATTERN ---"

# 1. Search commit messages
echo "[1/3] Searching commit messages..."
git log --all --oneline --grep="$PATTERN"

# 2. Search code additions/deletions (Pickaxe)
echo "[2/3] Searching code history (Pickaxe)..."
git log --all --oneline -S "$PATTERN"

# 3. Search code with Regex (G-regex)
echo "[3/3] Searching code with Regex..."
git log --all --oneline -G "$PATTERN"

echo "--- Search Complete ---"
echo "Use 'git show <hash>' to view details of a specific commit."
