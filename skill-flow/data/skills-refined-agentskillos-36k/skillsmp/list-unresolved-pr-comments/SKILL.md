---
name: list-unresolved-pr-comments
description: 指定したPRの未解決レビューコメントを一覧表示
args:
  pr_number:
    description: PR番号（省略時は現在のブランチに紐づくPR）
    required: false
---


指定されたPR {{pr_number}} の未解決レビューコメントを取得して**日本語で**表示してください。

## 処理手順

1. **PR番号とリポジトリ情報の取得**

   `gh pr view --json number,url -q '{number: .number, url: .url}'` を実行:
   - {{pr_number}} が指定されている場合: `gh pr view {{pr_number}}` で取得
   - {{pr_number}} が未指定の場合: `gh pr view` で現在のブランチのPRを取得

   取得した JSON から:
   - PR番号: `.number`
   - owner: `.url` を `/` で分割し4番目の要素
   - repo: `.url` を `/` で分割し5番目の要素

   PR番号が取得できない（コマンドが失敗する）場合はエラー終了。

2. **GraphQL クエリの実行**

   以下のbashスクリプトを**一時ファイルに書き出してから実行**します:

   ```bash
   cat > /tmp/fetch_pr_comments.sh << 'SCRIPT_EOF'
   #!/bin/bash
   owner="手順1で取得したowner"
   repo="手順1で取得したrepo"
   pr_number="手順1で取得したPR番号"

   cursor=""
   all_results="[]"

   while true; do
     if [ -z "$cursor" ]; then
       result=$(gh api graphql -F pr="$pr_number" -f query="
         query(\$pr: Int!) {
           repository(owner: \"$owner\", name: \"$repo\") {
             pullRequest(number: \$pr) {
               reviewThreads(first: 100) {
                 pageInfo { hasNextPage endCursor }
                 nodes {
                   isResolved
                   isOutdated
                   line
                   path
                   comments(first: 1) {
                     nodes {
                       databaseId
                       body
                       author { login }
                     }
                   }
                 }
               }
             }
           }
         }")
     else
       result=$(gh api graphql -F pr="$pr_number" -F cursor="$cursor" -f query="
         query(\$pr: Int!, \$cursor: String) {
           repository(owner: \"$owner\", name: \"$repo\") {
             pullRequest(number: \$pr) {
               reviewThreads(first: 100, after: \$cursor) {
                 pageInfo { hasNextPage endCursor }
                 nodes {
                   isResolved
                   isOutdated
                   line
                   path
                   comments(first: 1) {
                     nodes {
                       databaseId
                       body
                       author { login }
                     }
                   }
                 }
               }
             }
           }
         }")
     fi

     threads=$(echo "$result" | jq -r '.data.repository.pullRequest.reviewThreads.nodes')
     all_results=$(echo "$all_results" | jq ". + $threads")

     has_next=$(echo "$result" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.hasNextPage')
     if [ "$has_next" != "true" ]; then
       break
     fi
     cursor=$(echo "$result" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.endCursor')
   done

   echo "$all_results"
   SCRIPT_EOF

   bash /tmp/fetch_pr_comments.sh
   ```

   **理由**: Claude Code の Bash tool では複数行のwhile loopを含む複雑なスクリプトを直接実行すると構文エラーが発生することがあるため、一時ファイル経由での実行を推奨します。

3. **結果の処理**

   手順2で取得した `all_results` を処理:
   - `jq 'map(select(.isResolved == false)) | sort_by(.path // "", .line // 0)'` で未解決コメントのみ抽出しソート
   - 各スレッドの `.comments.nodes[0]` から最初のコメントを取得
   - コメント本文（`.body`）を以下の方針で要約:
     * 100文字以内: そのまま表示
     * 100文字超過: 冒頭の主要な指摘内容を50-80文字程度に要約し、具体的な提案や質問を含める
     * コード例が含まれる場合: 「〜の修正を提案」のように要約

## 出力フォーマット

```
PR #{pr_number} の未解決コメント: {total}件

---

{path}:{line}
著者: {author.login} | Outdated: {isOutdated}
要約: {コメント本文の内容をわかりやすく要約した説明}
→ https://github.com/{owner}/{repo}/pull/{pr_number}#discussion_r{databaseId}

---

(繰り返し)
```

## エラーハンドリング

- gh CLI が利用不可の場合: "エラー: gh CLI がインストールされていないか、認証されていません。'gh auth login' を実行してください"
- PR番号が未指定かつ現在のブランチにPRがない場合: "エラー: 現在のブランチにPRが見つかりません。PR番号を指定してください"
- PR が見つからない場合: "エラー: PR #{pr_number} が見つかりません"
- 未解決コメントが0件の場合: "エラー: PR #{pr_number} のコメントはすべて解決済みです"
- GraphQL APIエラーの場合: "エラー: " に続けてエラー内容を日本語で表示

## 注意事項

- パスが null の場合は "全般的なコメント" と表示
- 行番号が null の場合は行番号を省略
- すべての出力は日本語で行う
