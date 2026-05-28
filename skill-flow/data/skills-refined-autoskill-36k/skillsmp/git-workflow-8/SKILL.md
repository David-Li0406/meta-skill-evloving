---
name: git-workflow
description: ファイル修正前にブランチを確認・作成する。コードを編集する前、ファイルを変更する前、バグ修正や機能追加を行う前に使用。mainブランチへの直接コミットを防ぐ。
---

# Git ワークフロー

ファイルを修正する前に、必ず適切なブランチにいることを確認する。

## 修正前の必須チェック

**ファイルを編集する前に必ず実行:**

```bash
# 1. 現在のブランチを確認
git branch --show-current

# 2. mainまたはmasterにいる場合は、新しいブランチを作成
git checkout -b <type>/<description>
```

## ブランチ命名規則

```
<type>/<description>
```

| Type | 用途 | 例 |
|------|------|-----|
| `feat` | 新機能 | `feat/add-chart-zoom` |
| `fix` | バグ修正 | `fix/calculation-error` |
| `refactor` | リファクタリング | `refactor/split-components` |
| `docs` | ドキュメント | `docs/update-readme` |
| `chore` | 雑務・設定 | `chore/update-deps` |
| `test` | テスト追加 | `test/add-unit-tests` |

## チェックリスト

1. ✅ `main` / `master` にいないか確認
2. ✅ 適切なブランチ名を付けたか
3. ✅ `git pull` で最新を取得したか

## コミット＆プッシュ

```bash
# ステージング
git add <files>

# コミット（Conventional Commits形式）
git commit -m "<type>(<scope>): <description>"

# プッシュ（新規ブランチ）
git push -u origin <branch-name>

# プッシュ（既存ブランチ）
git push
```

## Conventional Commits

- `feat(frontend): 資産チャートにズーム機能を追加`
- `fix(backend): 支出計算の丸め誤差を修正`
- `docs: READMEを更新`
- `chore: 依存関係を更新`

## 禁止事項

❌ `main` ブランチに直接コミットしない
❌ ブランチを切らずにファイルを編集しない
❌ 意味のないブランチ名を付けない（`fix/fix`, `test/test`）
