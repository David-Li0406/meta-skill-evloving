---
name: quick-push
description: 変更を素早くコミット＆プッシュして日常作業を効率化
user-invocable: true
allowed-tools:
  - Bash(git:*)
  - Bash(gh:*)
---

# /quick-push - 変更を素早くコミット＆プッシュ

## 目的
現在の変更を素早くコミットしてリモートにプッシュします。日常的な作業の効率化に最適です。

## 動作
1. `git status`で現在の変更を表示
2. 未追跡ファイルと変更ファイルをリスト化
3. 危険なファイル（.env、secrets、credentials等）を除外
4. 安全なファイルのみを`git add`
5. 変更内容を分析して適切なprefixを選択：
   - `feat:` 新機能追加
   - `fix:` バグ修正
   - `docs:` ドキュメント変更
   - `style:` フォーマット修正
   - `refactor:` リファクタリング
   - `test:` テスト追加・修正
   - `chore:` その他の変更
6. コミットメッセージを表示して確認
7. PRマージ済みチェック（push前）
8. 現在のブランチをリモートにプッシュ
9. mainブランチ以外の場合、PR作成を提案

## PRマージ済みチェックの実装手順

コミット後、push前に以下のチェックを必ず実行：

```bash
current_branch=$(git rev-parse --abbrev-ref HEAD)

if [[ "$current_branch" != "main" ]] && [[ "$current_branch" != "master" ]]; then
    pr_info=$(gh pr list --head "$current_branch" --state all --json number,state,title 2>/dev/null)

    if [[ -n "$pr_info" ]] && [[ "$pr_info" != "[]" ]]; then
        pr_state=$(echo "$pr_info" | jq -r '.[0].state')
        pr_number=$(echo "$pr_info" | jq -r '.[0].number')
        pr_title=$(echo "$pr_info" | jq -r '.[0].title')

        if [[ "$pr_state" == "MERGED" ]]; then
            echo "Warning: このブランチのPRはすでにマージ済みです"
            echo "  ブランチ: $current_branch"
            echo "  PR #$pr_number: $pr_title"
            # ユーザーに確認を求める
        fi
    fi
fi
```

## 安全機能
- 機密ファイルの自動除外
- mainブランチへの直接プッシュ時は警告
- PRマージ済みブランチへのpush防止
- force pushが必要な場合は確認
- 大量のファイル変更時は要確認

## 使用例
```
/quick-push
```

## 注意事項
PRマージ後にエラーが発生した場合:
- マージ済みのブランチにはpushしない
- 新しいブランチを作成して、そこで修正を行う
