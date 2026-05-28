#!/usr/bin/env bash
set -euo pipefail

# Codex レビューセッションを終了
# Usage: close_codex_session.sh <output_dir>

OUTPUT_DIR="$1"

CODEX_PANE_ID=$(cat "$OUTPUT_DIR/codex_pane_id" 2>/dev/null || echo "")

if [ -z "$CODEX_PANE_ID" ]; then
    echo "No Codex pane ID found"
    exit 0
fi

# ペインが存在するか確認
if tmux list-panes -a -F '#{pane_id}' | grep -q "^$CODEX_PANE_ID$"; then
    # Codex プロセスを終了
    tmux send-keys -t "$CODEX_PANE_ID" C-c C-m
    sleep 1

    # ペインを閉じる
    tmux kill-pane -t "$CODEX_PANE_ID"
    echo "Codex pane $CODEX_PANE_ID closed"
else
    echo "Codex pane $CODEX_PANE_ID not found (may already be closed)"
fi

# クリーンアップ（オプション）
# rm -rf "$OUTPUT_DIR"
