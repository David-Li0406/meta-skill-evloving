#!/bin/bash
# Quick status check for HelixDB memory system

HELIX_BIN="${HELIX_BIN:-$(which helix 2>/dev/null || echo "$HOME/.local/bin/helix")}"
HELIX_URL="http://localhost:6969"

echo "=== HelixDB Memory Status ==="
echo ""

# Check if helix CLI exists
if [[ ! -x "$HELIX_BIN" ]]; then
    echo "ERROR: Helix CLI not found at $HELIX_BIN"
    exit 1
fi

# Check DB status
if curl -s --connect-timeout 2 "$HELIX_URL/GetAllMemories" -X POST -H "Content-Type: application/json" -d '{}' > /dev/null 2>&1; then
    echo "Status: RUNNING"

    # Get memory count
    MEMORIES=$(curl -s "$HELIX_URL/GetAllMemories" -X POST -H "Content-Type: application/json" -d '{}' 2>/dev/null)
    MEM_COUNT=$(echo "$MEMORIES" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('memories',[])))" 2>/dev/null || echo "?")

    # Get context count
    CONTEXTS=$(curl -s "$HELIX_URL/GetAllContexts" -X POST -H "Content-Type: application/json" -d '{}' 2>/dev/null)
    CTX_COUNT=$(echo "$CONTEXTS" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('contexts',[])))" 2>/dev/null || echo "?")

    echo "Memories: $MEM_COUNT"
    echo "Contexts: $CTX_COUNT"
    echo ""

    # Show category breakdown
    echo "By category:"
    echo "$MEMORIES" | python3 -c "
import sys, json
from collections import Counter
data = json.load(sys.stdin)
cats = Counter(m.get('category','unknown') for m in data.get('memories',[]))
for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
    print(f'  {cat}: {count}')
" 2>/dev/null

    echo ""

    # Show recent memories (last 3)
    echo "Recent memories:"
    echo "$MEMORIES" | python3 -c "
import sys, json
data = json.load(sys.stdin)
memories = data.get('memories', [])[-3:]
for m in memories:
    cat = m.get('category','?').upper()[:4]
    imp = m.get('importance','?')
    content = m.get('content','')[:60]
    print(f'  [{cat}-{imp}] {content}...')
" 2>/dev/null

else
    echo "Status: NOT RUNNING"
    echo ""
    echo "Start with:"
    echo "  memory start"
    exit 1
fi
