#!/bin/bash
# full-sync.sh - complete sync workflow
# usage: ./full-sync.sh [ip]

set -e

IP="${1:-10.0.0.61}"
EPUB_DIR="${EPUB_DIR:-$HOME/Developer/utils/epub}"

cd "$EPUB_DIR"

echo "=== epub full sync ==="
echo ""

# 1. check device
echo "1. Checking device..."
if ! curl -s --max-time 3 "http://$IP/" | grep -qi "crosspoint\|file"; then
  echo "   X4 not reachable at $IP"
  echo "   Enable file transfer mode on device and retry"
  exit 1
fi
echo "   Device ready"
echo ""

# 2. sync feeds
echo "2. Syncing feeds..."
./bin/run.js feed sync --limit 20
echo ""

# 3. digest agents (last 24h)
echo "3. Digesting agent work..."
./bin/run.js agents digest --since 24h 2>/dev/null || echo "   No recent agent work"
echo ""

# 4. sync to device
echo "4. Syncing to device..."
./bin/run.js device sync --ip "$IP"
echo ""

# 5. verify
echo "5. Device contents:"
./bin/run.js device files --ip "$IP"
echo ""

echo "=== sync complete ==="
