#!/usr/bin/env bash
set -euo pipefail

# Codex レビューセッションを tmux ペインで開始
# Usage: start_codex_review.sh <prompt> <output_dir>

PROMPT="$1"
OUTPUT_DIR="$2"
SESSION_ID="${3:-codex-review-$$}"

# 出力ディレクトリを作成
mkdir -p "$OUTPUT_DIR"

# セッション情報を保存
echo "$SESSION_ID" > "$OUTPUT_DIR/session_id"

# tmux が実行中か確認
if ! tmux info &> /dev/null; then
    echo "Error: tmux is not running or no session exists"
    exit 1
fi

# 現在のペインを取得
CURRENT_PANE=$(tmux display-message -p '#{pane_id}')
echo "$CURRENT_PANE" > "$OUTPUT_DIR/claude_pane_id"

# 横分割で新しいペインを作成し、そのペイン ID を取得
NEW_PANE=$(tmux split-window -h -P -F '#{pane_id}')
echo "$NEW_PANE" > "$OUTPUT_DIR/codex_pane_id"

# Codex の出力を記録するためのログファイル
LOG_FILE="$OUTPUT_DIR/codex_output.log"
CONVERSATION_ID_FILE="$OUTPUT_DIR/conversation_id"

# 新しいペインで Codex を起動
# シングルクォートでエスケープしてプロンプトを送信
tmux send-keys -t "$NEW_PANE" "codex '$(echo "$PROMPT" | sed "s/'/'\"'\"'/g")'" C-m

# Codex が起動するまで少し待つ
sleep 3

# 初期の出力をキャプチャしてログファイルに保存
tmux capture-pane -t "$NEW_PANE" -p > "$LOG_FILE"

# Conversation ID は後続のやり取りで必要な場合のみ取得
# （現在のcodexは会話IDを明示的に表示しないため、ペインIDで管理）
echo "managed-by-pane" > "$CONVERSATION_ID_FILE"

echo "Codex review session started in pane $NEW_PANE"
echo "Session ID: $SESSION_ID"
echo "Output: $LOG_FILE"
