#!/usr/bin/env bash
set -euo pipefail

# Codex セッションに追加メッセージを送信
# Usage: send_to_codex.sh <output_dir> <message>

OUTPUT_DIR="$1"
MESSAGE="$2"

CODEX_PANE_ID=$(cat "$OUTPUT_DIR/codex_pane_id")

# 既存のペインが存在するか確認
if ! tmux list-panes -a -F '#{pane_id}' | grep -q "^$CODEX_PANE_ID$"; then
    echo "Error: Codex pane $CODEX_PANE_ID not found"
    exit 1
fi

# メッセージを Codex のインタラクティブセッションに直接入力
# tmux send-keys はそのまま文字列を送信
tmux send-keys -t "$CODEX_PANE_ID" "$MESSAGE" C-m

echo "Message sent to Codex session"
