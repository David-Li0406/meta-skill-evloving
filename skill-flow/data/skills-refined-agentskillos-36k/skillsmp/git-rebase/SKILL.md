---
name: git-rebase
description: git rebaseをノンインタラクティブで実行。「rebase」「リベース」などの依頼で起動。
allowed-tools:
  - Bash
model: claude-haiku-4-5-20251001
user-invocable: true
---

# Git Rebaseスキル

このスキルは、git rebaseをノンインタラクティブに実行する方法を提供します。

**IMPORTANT: このスキルを使用する際は、特に指定が無い限り日本語でユーザーとコミュニケーションを取ってください。**

## ノンインタラクティブrebaseの実行方法

`git rebase`を単純に実行すると、インタラクティブモードになって途中で止まる可能性があります。
これを回避するため、`GIT_EDITOR=true`環境変数を設定して実行します。

### 基本的な使用方法

```bash
# ノンインタラクティブでrebaseを実行
GIT_EDITOR=true git rebase <base-branch>

# 例: mainブランチにrebase
GIT_EDITOR=true git rebase main

# 例: originのmainブランチにrebase
GIT_EDITOR=true git rebase origin/main
```

### rebase中の操作

```bash
# rebaseを続行（コンフリクト解決後）
GIT_EDITOR=true git rebase --continue

# rebaseを中止
git rebase --abort

# rebaseをスキップ
GIT_EDITOR=true git rebase --skip
```

## 重要な注意事項

1. **コンフリクトの確認**: rebase中にコンフリクトが発生した場合は、ユーザーに報告して解決を依頼
2. **履歴の確認**: rebase前に現在の状態を確認し、必要に応じてバックアップブランチを作成
3. **強制プッシュの注意**: rebase後にリモートにプッシュする場合は、force pushが必要になることをユーザーに説明

## エラーハンドリング

- コマンドが失敗した場合は、特に指定が無い限り日本語でエラーメッセージをユーザーに説明
- コンフリクトが発生した場合は、影響を受けるファイルとその内容を報告
- 次のステップに進む前に、問題を解決するための提案を提示
