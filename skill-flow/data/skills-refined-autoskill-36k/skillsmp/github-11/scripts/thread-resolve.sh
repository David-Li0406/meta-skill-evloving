#!/bin/bash
# レビュースレッドをresolveするスクリプト
#
# 使用方法:
#   ./scripts/resolve-review-thread.sh <スレッドID>
#
# 例:
#   ./scripts/resolve-review-thread.sh "xxxxxxxxxxxxxxxxxxxx"

set -euo pipefail

# 必要なコマンドの存在確認
for cmd in gh jq; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "エラー: $cmd コマンドが見つかりません。インストールしてください。" >&2
        exit 1
    fi
done

# 使用方法を表示
usage() {
    echo "使用方法: $0 <スレッドID>" >&2
    echo "" >&2
    echo "例:" >&2
    echo "  $0 \"xxxxxxxxxxxxxxxxxxxx\"" >&2
    exit 1
}

# 引数チェック
if [[ $# -ne 1 ]]; then
    echo "エラー: スレッドIDを指定してください。" >&2
    usage
fi

THREAD_ID="$1"

# スレッドIDが空でないかチェック
if [[ -z "$THREAD_ID" ]]; then
    echo "エラー: スレッドIDが空です。" >&2
    exit 1
fi

echo "レビュースレッドをresolve中..." >&2
echo "スレッドID: $THREAD_ID" >&2

# レビュースレッドをresolve
RESULT=$(gh api graphql \
  -F threadId="$THREAD_ID" \
  -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread {
      id
      isResolved
    }
  }
}')

# 結果を確認
IS_RESOLVED=$(echo "$RESULT" | jq -r '.data.resolveReviewThread.thread.isResolved')

if [[ "$IS_RESOLVED" == "true" ]]; then
    echo "" >&2
    echo "✓ レビュースレッドをresolveしました。" >&2
    echo "スレッドID: $(echo "$RESULT" | jq -r '.data.resolveReviewThread.thread.id')" >&2
    exit 0
else
    echo "" >&2
    echo "✗ レビュースレッドのresolveに失敗しました。" >&2
    echo "エラー詳細:" >&2
    echo "$RESULT" | jq >&2
    exit 1
fi

