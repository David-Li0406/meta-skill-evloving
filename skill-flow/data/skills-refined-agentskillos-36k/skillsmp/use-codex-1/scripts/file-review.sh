#!/bin/bash
# file-review.sh - Execute file review via Codex CLI
# Usage: ./file-review.sh <file-path> [review-focus]

set -euo pipefail

if [ $# -eq 0 ]; then
    echo "Usage: $0 <file-path> [review-focus]" >&2
    exit 1
fi

file_path="$1"
review_focus="${2:-}"

if [ ! -f "$file_path" ]; then
    echo "Error: File not found: $file_path" >&2
    exit 1
fi

if [ -n "$review_focus" ]; then
    prompt="以下のファイルを「${review_focus}」の観点でレビューしてください: ${file_path}"
else
    prompt="以下のファイルをレビューしてください。バグ、改善点、ベストプラクティスへの準拠を確認してください: ${file_path}"
fi

codex exec --sandbox read-only "${prompt}"
