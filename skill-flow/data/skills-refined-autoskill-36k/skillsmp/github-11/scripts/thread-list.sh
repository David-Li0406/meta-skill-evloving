#!/bin/bash
# PRの未解決レビューコメントを取得するスクリプト
#
# 使用方法:
#   ./scripts/get-pr-review-comments.sh <PR番号>
#
# 例:
#   ./scripts/get-pr-review-comments.sh 123
#
# 注意事項:
#   - 最大30件のレビュースレッドを取得します
#   - 各スレッドの最後の10件のコメントを取得します

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
    echo -e "使用方法: $0 <PR番号>\n例: $0 123" >&2
    exit 1
}

# 引数チェック
if [[ $# -ne 1 ]]; then
    echo "エラー: PR番号を指定してください。" >&2
    usage
fi

PR_NUMBER="$1"

# PR番号が数値かチェック
if ! [[ "$PR_NUMBER" =~ ^[0-9]+$ ]]; then
    echo "エラー: PR番号は数値で指定してください。" >&2
    exit 1
fi

# リポジトリ情報を取得
OWNER_REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
OWNER="${OWNER_REPO%/*}"
REPO="${OWNER_REPO#*/}"

# set +e で一時的にエラーでの終了を無効化
set +e
RESPONSE=$(gh api graphql \
  -F owner="$OWNER" \
  -F name="$REPO" \
  -F number="$PR_NUMBER" \
  -f query='
query($owner: String!, $name: String!, $number: Int!) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      reviewThreads(first: 30) {
        nodes {
          id
          isResolved
          comments(last: 10) {
            nodes {
              id
              body
              author {
                login
              }
            }
          }
        }
      }
    }
  }
}' 2>&1)
GH_EXIT_CODE=$?
set -e

# gh api コマンドがエラーの場合
if [ $GH_EXIT_CODE -ne 0 ]; then
    echo "エラー: PR番号 '$PR_NUMBER' が見つからないか、アクセス権がありません。" >&2
    exit 1
fi

# PRが存在しない場合（nullの場合）
if echo "$RESPONSE" | jq -e '.data.repository.pullRequest == null' > /dev/null 2>&1; then
    echo "エラー: PR番号 '$PR_NUMBER' が見つからないか、アクセス権がありません。" >&2
    exit 1
fi

echo "$RESPONSE" | jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false) | {thread_id: .id, author: .comments.nodes[-1].author.login, comment: .comments.nodes[-1].body}'

