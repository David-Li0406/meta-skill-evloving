#!/bin/bash
# List available PRD files from wip and backlog directories

echo "=== PRDs in Progress (wip) ==="
if [ -d ".local/prds/wip" ] && [ "$(ls -A .local/prds/wip 2>/dev/null)" ]; then
    ls -1 .local/prds/wip/
else
    echo "(none)"
fi

echo ""
echo "=== PRDs in Backlog ==="
if [ -d ".local/prds/backlog" ] && [ "$(ls -A .local/prds/backlog 2>/dev/null)" ]; then
    ls -1 .local/prds/backlog/
else
    echo "(none)"
fi

echo ""
echo "=== Completed PRDs (done) ==="
if [ -d ".local/prds/done" ] && [ "$(ls -A .local/prds/done 2>/dev/null)" ]; then
    ls -1 .local/prds/done/
else
    echo "(none)"
fi
