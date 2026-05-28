---
name: sync-default-branch-and-clean
description: デフォルトブランチを最新化して不要なローカルブランチを削除
user-invocable: true
allowed-tools:
  - Bash(git:*)
---

# /sync-default-branch-and-clean - デフォルトブランチの同期とクリーニング

デフォルトブランチ（main/master）に切り替えて最新状態に同期し、不要なローカルブランチを安全に削除します。

## 現在の状態確認
```bash
git status --porcelain
git branch --show-current
git branch -vv
git remote -v
```

## 実行プロセス

### フェーズ1: デフォルトブランチの同期

1. デフォルトブランチを検出
```bash
DEFAULT_BRANCH=$(git remote show origin 2>/dev/null | grep 'HEAD branch' | cut -d' ' -f5)

if [ -z "$DEFAULT_BRANCH" ]; then
  if git show-ref --verify --quiet refs/heads/main; then
    DEFAULT_BRANCH="main"
  elif git show-ref --verify --quiet refs/heads/master; then
    DEFAULT_BRANCH="master"
  fi
fi
```

2. リモート名を検出
```bash
REMOTE=$(git remote | grep -E '^origin$' || git remote | head -n1)
```

3. 未コミットの変更を確認
4. デフォルトブランチに切り替え: `git checkout $DEFAULT_BRANCH`
5. リモートから最新の変更を取得: `git fetch $REMOTE --prune`
6. 最新状態に更新: `git pull --rebase $REMOTE $DEFAULT_BRANCH`

### フェーズ2: 不要なローカルブランチの削除

7. 削除対象ブランチの分析
```bash
# マージ済みブランチを確認
MERGED_BRANCHES=$(git branch --merged | grep -v "\*" | grep -v "^  main$" | grep -v "^  master$" | sed 's/^ *//')

# リモートで削除されたブランチを確認（gone）
GONE_BRANCHES=$(git branch -vv | grep ': gone]' | awk '{print $1}')
```

8. 削除候補の分類と表示
   - 安全に削除可能: マージ済みまたはリモートで削除済み（gone）
   - 注意が必要: 未マージだがリモートに存在しないブランチ
   - 保持: デフォルトブランチ、現在のブランチ

9. 段階的な削除実行
```bash
# マージ済みブランチを削除
for branch in $MERGED_BRANCHES; do
  git branch -d "$branch"
done

# リモートで削除されたブランチを削除
for branch in $GONE_BRANCHES; do
  git branch -D "$branch"
done
```

## 安全性の考慮

- 保護されるブランチ: main、master、現在のブランチ
- 未コミット変更: 実行前に警告を表示、続行確認
- 削除方針:
  - マージ済みブランチ: `-d` で安全に削除
  - gone ブランチ: `-D` で強制削除

## 注意事項

- デフォルトブランチが検出できない場合はエラーを表示
- 未コミット変更がある場合は、事前にコミットまたはstash推奨
- gone ブランチは `-D` で強制削除されるため、未push のコミットがある場合は注意
