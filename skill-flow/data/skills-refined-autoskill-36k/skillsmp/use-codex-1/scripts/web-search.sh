#!/bin/bash
# web-search.sh - Execute web search via Codex CLI
# Usage: ./web-search.sh "search query"

set -euo pipefail

if [ $# -eq 0 ]; then
    echo "Usage: $0 <search query>" >&2
    exit 1
fi

query="$1"

codex exec --sandbox workspace-write --enable web_search_request "Web検索を実行: ${query}"
