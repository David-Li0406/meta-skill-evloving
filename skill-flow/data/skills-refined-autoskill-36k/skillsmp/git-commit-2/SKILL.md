---
name: git-commit
description: Git コミットのベストプラクティス。意味のある変更単位でのコミット、Conventional Commits ルール、コミットメッセージの書き方を定義。
---

# Git コミットガイドライン

意味のある変更単位ごとにコミットを行うことは、コードの履歴を明確にし、将来の変更を追跡しやすくするために重要です。

## Instructions

### 1. 変更を確認する

まず、現在のワーキングディレクトリでの変更を確認します：

```bash
git status
```

### 2. 変更をステージングする

変更をコミットする前に、ステージングエリアに追加する必要があります：

```bash
git add 対象ファイルやディレクトリ
```

**重要**：意味のある変更単位ごとにファイルを指定すること。無条件にすべての変更を追加しないでください。

### 3. コミットメッセージを作成する

コミットメッセージは、変更内容を簡潔に説明する重要な部分です：

```bash
git commit -m "コミットメッセージをここに入力"
```

#### コミットメッセージのルール

- コミットメッセージは日本語で記述
- Conventional Commits のルールに従う
- co-author やコミットメッセージに "Claude Code" のキーワードは含めない

#### Conventional Commits フォーマット

```
<type>(<scope>): <subject>

<body>

<footer>
```

**type の種類**：
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードの意味に影響しない変更（空白、フォーマット等）
- `refactor`: バグ修正や機能追加ではないコード変更
- `test`: テストの追加・修正
- `chore`: ビルドプロセスやツールの変更

### 4. コミットを確認する

コミットが正しく行われたかを確認：

```bash
git log --oneline
```

## Examples

### 機能追加のコミット

```bash
git add src/features/user-auth.ts
git commit -m "feat(auth): ユーザー認証機能を追加"
```

### バグ修正のコミット

```bash
git add src/utils/validation.ts
git commit -m "fix(validation): メールアドレスのバリデーションエラーを修正"
```

### ドキュメント更新のコミット

```bash
git add README.md docs/setup.md
git commit -m "docs: セットアップ手順を更新"
```

### リファクタリングのコミット

```bash
git add src/services/api.ts
git commit -m "refactor(api): API クライアントの共通処理を抽出"
```

## ベストプラクティス

- **1 コミット 1 目的**：構造変更と動作変更を同一コミットに含めない
- **小さく頻繁に**：大きな変更は小さなコミットに分割
- **テスト通過後にコミット**：壊れたコードをコミットしない
- **明確なメッセージ**：何を、なぜ変更したかを簡潔に記述
