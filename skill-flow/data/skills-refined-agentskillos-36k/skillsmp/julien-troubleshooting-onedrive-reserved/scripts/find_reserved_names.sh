#!/bin/bash
# Fast search for Windows reserved filenames using fd (5-10x faster than find)

SEARCH_PATH="${1:-/c/Users/$USER/OneDrive/Coding/_Projets de code}"

echo "Searching with fd (ultra-fast)..."
echo "Path: $SEARCH_PATH"
echo ""

echo "=== Reserved names (nul, null, con, prn, aux) ==="
fd -t f -i "^(nul|null|con|prn|aux)$" "$SEARCH_PATH"

echo ""
echo "=== Short names (0-1 character) ==="
fd -t f "^.$" "$SEARCH_PATH"
