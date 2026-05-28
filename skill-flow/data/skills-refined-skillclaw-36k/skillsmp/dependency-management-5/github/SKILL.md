---
name: github-pr-review-operation
description: GitHub Pull Requestのレビュー操作を行うスキル。PR情報取得、差分確認、コメント取得・投稿、インラインコメント、コメント返信をghコマンドで実行する。PRレビュー、コードレビュー、PR操作が必要な時に使用。
---

# GitHub PR Review Operation

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] GitHub PRをレビューする?
- [ ] PRにコメントを投稿する?
- [ ] インラインコメントを追加する?
- [ ] PR情報を取得する?

### 前提条件
- [ ] `gh` CLIがインストールされているか?
- [ ] `gh auth login`で認証済みか?
- [ ] PR URLから OWNER/REPO/NUMBER を抽出したか?

### 禁止事項の確認
- [ ] 未認証状態で操作しようとしていないか?
- [ ] 権限のないリポジトリを操作しようとしていないか?

---

## トリガー

- GitHub PRレビュー時
- PRへのコメント投稿時
- インラインコメント時
- PR情報取得時

---

## 前提条件

- `gh` インストール済み
- `gh auth login` で認証済み

---

## PR URLのパース

PR URL `https://github.com/OWNER/REPO/pull/NUMBER` から以下を抽出して使用:
- `OWNER`: リポジトリオーナー
- `REPO`: リポジトリ名
- `NUMBER`: PR番号

---

## 操作一覧

### PR情報取得

```bash
gh pr view NUMBER --repo OWNER/REPO
```

### 差分確認

```bash
gh pr diff NUMBER --repo OWNER/REPO
```

### コメント取得

```bash
gh pr view NUMBER --repo OWNER/REPO --comments
```

### コメント投稿

```bash
gh pr comment NUMBER --repo OWNER/REPO --body "コメント内容"
```

### レビュー投稿

```bash
gh pr review NUMBER --repo OWNER/REPO --approve --body "LGTM"
gh pr review NUMBER --repo OWNER/REPO --request-changes --body "修正をお願いします"
gh pr review NUMBER --repo OWNER/REPO --comment --body "確認中です"
```

---

## 🚫 禁止事項まとめ

- 未認証状態での操作
- 権限のないリポジトリへの操作
