#!/bin/bash
# pending-guard.sh - post-loop-pending ファイルを検出し、post-loop 実行を強制
#
# 発火条件: PreToolUse(Edit|Write)
# 目的: playbook 完了後、post-loop Skill を呼び出すまで Edit/Write をブロック
#
# 設計思想:
#   - archive-playbook.sh が pending ファイルを作成
#   - このガードが pending を検出して BLOCK
#   - Claude が post-loop を実行すると pending が削除される
#   - Hook → Skill チェーンを維持しつつ強制力を持たせる
#
# 許可リスト（デッドロック防止）:
#   - state.md（状態管理に必要）
#   - post-loop-pending 自体
#   - .claude/session-state/ 配下

set -e

SESSION_STATE_DIR=".claude/session-state"
PENDING_FILE="$SESSION_STATE_DIR/post-loop-pending"

# pending ファイルが存在しない場合はスキップ
if [ ! -f "$PENDING_FILE" ]; then
    exit 0
fi

# ==============================================================================
# main ブランチ例外（副防御: デッドロック防止）
# See: fix/post-loop-pending-deadlock
# Reason: main にいる = アーカイブ完了後 = pending の役割は終了
# ==============================================================================
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "")
if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
    # main ブランチでは pending があっても許可（アーカイブ完了済みのため）
    exit 0
fi

# stdin から JSON を読み込む
INPUT=$(cat)

# jq がない場合はブロック（fail-closed）
if ! command -v jq &> /dev/null; then
    echo "[FAIL-CLOSED] jq not found - blocking for security" >&2
    exit 2
fi

# ツール名を取得
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""')

# Edit/Write 以外はスキップ
if [ "$TOOL_NAME" != "Edit" ] && [ "$TOOL_NAME" != "Write" ]; then
    exit 0
fi

# ファイルパスを取得
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

# ==============================================================================
# 許可リスト（これらのファイルは常に許可）
# ==============================================================================
ALLOWLIST=(
    "state.md"
    ".claude/session-state/"
    "post-loop-pending"
)

for ALLOWED in "${ALLOWLIST[@]}"; do
    if [[ "$FILE_PATH" == *"$ALLOWED"* ]]; then
        exit 0  # 許可
    fi
done

# ==============================================================================
# pending ファイルの内容を読み取り
# ==============================================================================
PENDING_STATUS=$(jq -r '.status // "unknown"' "$PENDING_FILE" 2>/dev/null || echo "unknown")
PENDING_PLAYBOOK=$(jq -r '.playbook // "unknown"' "$PENDING_FILE" 2>/dev/null || echo "unknown")

# ==============================================================================
# BLOCK 出力
# ==============================================================================
echo "" >&2
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >&2
echo "  🚨 post-loop 未実行 - Edit/Write ブロック中" >&2
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >&2
echo "" >&2
echo "  playbook: $PENDING_PLAYBOOK" >&2
echo "  status: $PENDING_STATUS" >&2
echo "  tool: $TOOL_NAME" >&2
echo "  file: $FILE_PATH" >&2
echo "" >&2

if [ "$PENDING_STATUS" = "success" ]; then
    echo "  ✅ 自動処理は成功しました。" >&2
    echo "" >&2
    echo "  必須アクション:" >&2
    echo "    Skill(skill='post-loop') を呼び出してください。" >&2
    echo "" >&2
    echo "  post-loop が実行する処理:" >&2
    echo "    1. pending ファイル削除（ブロック解除）" >&2
    echo "    2. 次タスクの導出（pm SubAgent 経由）" >&2
elif [ "$PENDING_STATUS" = "partial" ]; then
    echo "  ⚠️ 自動処理が一部失敗しました。" >&2
    echo "" >&2
    echo "  手動確認が必要な項目:" >&2
    echo "    - PR 作成/マージ状態を確認: gh pr list" >&2
    echo "    - ブランチ状態を確認: git branch -vv" >&2
    echo "" >&2
    echo "  確認後、以下を実行:" >&2
    echo "    Skill(skill='post-loop') を呼び出してください。" >&2
else
    echo "  ❓ ステータス不明です。" >&2
    echo "" >&2
    echo "  pending ファイルを確認: cat $PENDING_FILE" >&2
    echo "" >&2
    echo "  問題がなければ:" >&2
    echo "    Skill(skill='post-loop') を呼び出してください。" >&2
fi

echo "" >&2
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >&2

# exit 2 = ブロック（Claude Code 公式仕様）
exit 2
