---
name: git-workflow
description: gitを使用する際に使用。Conventional Commits、ブランチ命名、1機能1PRルールをカバー。
---

# Git Workflow

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] コミット、ブランチ作成、マージ、リベースを行う?
- [ ] コミットメッセージを書く?
- [ ] PRを作成する?

### 前提条件
- [ ] 現在のブランチを確認したか?(`git branch --show-current`)
- [ ] mainブランチで作業していないか?
- [ ] 作業内容とブランチ名が一致しているか?

### 禁止事項の確認
- [ ] `git commit` / `git push` を自分で実行しようとしていないか?(ユーザーのみ操作可能)
- [ ] mainブランチに直接変更を加えようとしていないか?
- [ ] 「ついでに」別の修正を混ぜようとしていないか?
- [ ] 共有ブランチで `--force` push しようとしていないか?

---

## トリガー

- コミット作成時
- ブランチ作成時
- マージ・リベース時
- コミットメッセージ記述時

---

## 🚨 1機能1PRルール

**1つのブランチでは1つの機能のみ実装すること。**

- 1ブランチ = 1機能 = 1PR を厳守
- 作業中に別の問題・改善点を発見したら:
  1. TODOリストに追記して記録
  2. 現在の作業を完了させる
  3. 新しいブランチで対応する
- 「ついでに」の修正は禁止
- 関連性の薄い変更を1つのPRに混ぜない

**違反例:**
- `feat/add-auth` ブランチでREADMEのtypoも修正 → NG
- バグ修正中にリファクタリングも実施 → NG

**正しい対応:**
- 発見した問題はTODOに追記
- 現在のPRをマージ後、別ブランチで対応

---

## ⛔ git操作の制限

- **🚫 絶対禁止**: `git commit`, `git push`(ユーザーのみ操作可能)
- **許可**: その他の操作(checkout, fetch, branch -d 等)はユーザーに確認を取れば実行可能

---

## ブランチ保護ルール

main ブランチへの直接 push は GitHub のブランチ保護ルールで禁止されている。
必ず PR 経由でマージすること。

---

## 機能ブランチの作成

新しい機能を実装する際は `git-new-feature` コマンドを使用:

```bash
git-new-feature 機能名       # feat/機能名 ブランチを作成
git-new-feature -f バグ名    # fix/バグ名 ブランチを作成
git-new-feature -d 内容      # docs/内容 ブランチを作成
git-new-feature -r 対象      # refactor/対象 ブランチを作成
git-new-feature -c 内容      # chore/内容 ブランチを作成
```

---

## マージ後のブランチ削除

PR がマージされたら `git-cleanup-branch` コマンドを使用:

```bash
git-cleanup-branch           # 現在のブランチを削除
git-cleanup-branch feat/foo  # 指定したブランチを削除
```

このコマンドは以下を自動で実行:
1. main ブランチに移動
2. ローカルブランチを削除
3. リモートブランチを削除

**注意事項:**
- マージされていないブランチは `-d` で削除できない(安全のため)
- ユーザーの許可なしに削除しない

---

## Conventional Commits

```
<type>(<scope>): <description>
```

| タイプ | 用途 | バージョン |
|--------|------|-----------|
| feat | 新機能 | MINOR |
| fix | バグ修正 | PATCH |
| docs | ドキュメント | - |
| refactor | リファクタリング | - |
| test | テスト | - |
| chore | 雑務 | - |

### 例

```bash
feat(auth): add JWT refresh endpoint
fix(api): prevent race condition
feat!: change auth to OAuth 2.0  # ⚠️ 破壊的変更
```

---

## ブランチ命名

```
feat/user-authentication
fix/login-redirect
docs/update-readme
refactor/cleanup-utils
chore/update-dependencies
```

---

## コミット粒度

**1コミット = 1つの論理的変更**

---

## ロックファイル

⚠️ 必ずコミット: `package-lock.json`, `yarn.lock`, `poetry.lock`, `Cargo.lock`, `composer.lock`

---

## 🚫 禁止事項まとめ

```bash
# Claude Codeでの実行禁止
git commit   # ❌
git push     # ❌

# 共有ブランチでの --force は禁止
git push --force  # ❌

# mainブランチでの直接作業禁止
# mainにいる状態でコード変更 # ❌
```
