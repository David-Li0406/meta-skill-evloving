#!/bin/bash
# complete.sh - post-loop 完了処理
#
# 目的: pending ファイルを削除し、ブロックを解除する
#
# 呼び出し元: post-loop Skill（Claude が最初に実行）
#
# 処理:
#   1. pending ファイルの存在確認
#   2. pending ファイルの削除
#   3. 成功メッセージの出力

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
SESSION_STATE_DIR="$REPO_ROOT/.claude/session-state"
PENDING_FILE="$SESSION_STATE_DIR/post-loop-pending"

mkdir -p "$SESSION_STATE_DIR"

# 色定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'
SEP="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "$SEP"
echo "  📋 post-loop 完了処理"
echo "$SEP"
echo ""

# pending ファイルが存在しない場合
if [ ! -f "$PENDING_FILE" ]; then
    echo -e "${YELLOW}[INFO]${NC} pending ファイルが見つかりません。"
    echo "  既に削除されているか、playbook 完了処理が未実行です。"
    echo ""
    exit 0
fi

# pending ファイルの内容を表示
echo "  pending ファイル: $PENDING_FILE"
if command -v jq &> /dev/null; then
    echo "  内容:"
    jq '.' "$PENDING_FILE" 2>/dev/null | sed 's/^/    /'
fi
echo ""

# pending ファイルを削除
rm -f "$PENDING_FILE"

echo -e "${GREEN}✓${NC} pending ファイルを削除しました"
echo ""
echo "  Edit/Write のブロックが解除されました。"
echo ""
echo "$SEP"
echo ""
echo "  次のステップ:"
echo "    - 残タスクがある場合: pm SubAgent で次の playbook を作成"
echo "    - 残タスクがない場合: 「全タスク完了。次の指示を待ちます。」"
echo ""
echo "$SEP"

exit 0
