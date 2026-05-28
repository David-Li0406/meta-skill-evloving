#!/bin/bash
# PRレビュースレッドに返信を投稿するスクリプト
#
# 使用方法:
#   echo "コメント内容" | ./scripts/thread-reply.sh <スレッドID>
#   ./scripts/thread-reply.sh <スレッドID> <<EOF
#   複数行の
#   コメント内容
#   EOF
#
# 例:
#   echo "ご指摘ありがとうございます。修正しました。" | ./scripts/thread-reply.sh "xxxxxxxxxxxxxxxxxxxx"
#
# 注意事項:
#   - スレッドIDはGitHub GraphQL APIのNode ID形式で指定してください
#   - コメント本文は標準入力から読み取ります

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
    echo "使用方法: echo \"コメント内容\" | $0 <スレッドID>" >&2
    echo "" >&2
    echo "例:" >&2
    echo "  echo \"ご指摘ありがとうございます。\" | $0 \"xxxxxxxxxxxxxxxxxxxx\"" >&2
    echo "  $0 \"xxxxxxxxxxxxxxxxxxxx\" <<EOF" >&2
    echo "  複数行のコメント" >&2
    echo "  EOF" >&2
    exit 1
}

# 引数チェック
if [[ $# -ne 1 ]]; then
    echo "エラー: 引数が不正です。" >&2
    usage
fi

THREAD_ID="$1"

# スレッドIDが空でないかチェック
if [[ -z "$THREAD_ID" ]]; then
    echo "エラー: スレッドIDが空です。" >&2
    exit 1
fi

# 標準入力からコメント本文を読み取り
COMMENT_BODY=$(cat)
if [[ -z "$COMMENT_BODY" ]]; then
    echo "エラー: コメント本文が空です。" >&2
    exit 1
fi

# リポジトリ情報を取得
OWNER_REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
OWNER="${OWNER_REPO%/*}"
REPO="${OWNER_REPO#*/}"

echo "リポジトリ: $OWNER/$REPO, スレッドID: $THREAD_ID" >&2
echo "返信を投稿中..." >&2

# 返信を投稿
set +e
RESULT=$(gh api graphql \
  -f pullRequestReviewThreadId="$THREAD_ID" \
  -f body="$COMMENT_BODY" \
  -f query='
mutation($pullRequestReviewThreadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {pullRequestReviewThreadId: $pullRequestReviewThreadId, body: $body}) {
    comment {
      id
      body
      createdAt
      author {
        login
      }
    }
  }
}' 2>&1)
GH_POST_EXIT_CODE=$?
set -e

# 結果を確認
if [ "$GH_POST_EXIT_CODE" -ne 0 ]; then
    echo "エラー: 返信の投稿に失敗しました。" >&2
    echo "$RESULT" | jq >&2
    exit 1
fi

COMMENT_ID=$(echo "$RESULT" | jq -r '.data.addPullRequestReviewThreadReply.comment.id // empty')

if [[ -n "$COMMENT_ID" ]]; then
    echo "返信を投稿しました。" >&2
    echo "$RESULT" | jq -r '.data.addPullRequestReviewThreadReply.comment | "コメントID: \(.id), 投稿者: @\(.author.login), 作成日時: \(.createdAt)"' >&2
    exit 0
else
    echo "エラー: 返信の投稿は成功しましたが、レスポンスからコメントIDを取得できませんでした。" >&2
    echo "$RESULT" | jq >&2
    exit 1
fi
