#!/usr/bin/env bash
set -euo pipefail

# Codex の返答が完了したか確認
# Usage: check_codex_status.sh <output_dir>

OUTPUT_DIR="$1"
CODEX_PANE_ID_FILE="$OUTPUT_DIR/codex_pane_id"
LAST_OUTPUT_FILE="$OUTPUT_DIR/last_output"

# Codex ペイン ID を取得
if [ ! -f "$CODEX_PANE_ID_FILE" ]; then
    echo "waiting"
    exit 0
fi

CODEX_PANE_ID=$(cat "$CODEX_PANE_ID_FILE")

# ペインが存在するか確認
if ! tmux list-panes -a -F '#{pane_id}' | grep -q "^$CODEX_PANE_ID$"; then
    echo "pane_closed"
    exit 0
fi

# 現在のペイン内容をキャプチャ
CURRENT_OUTPUT=$(tmux capture-pane -t "$CODEX_PANE_ID" -p -S -100)

# 初回実行時は最終出力を保存して終了
if [ ! -f "$LAST_OUTPUT_FILE" ]; then
    echo "$CURRENT_OUTPUT" > "$LAST_OUTPUT_FILE"
    echo "waiting"
    exit 0
fi

LAST_OUTPUT=$(cat "$LAST_OUTPUT_FILE")

# 出力に変化があるか確認
if [ "$CURRENT_OUTPUT" != "$LAST_OUTPUT" ]; then
    # 新しい内容を保存
    echo "$CURRENT_OUTPUT" > "$LAST_OUTPUT_FILE"

    # 新しい内容を返す
    echo "new_output"
    echo "$CURRENT_OUTPUT"
else
    echo "waiting"
fi
