---
name: codex-review
description: OpenAI Codex (GPT-5) を使用してブランチの変更をレビュー。「codexレビュー」「ブランチレビュー」「変更レビュー」などの依頼で起動。
allowed-tools:
  - Read
  - Bash
model: claude-haiku-4-5-20251001
user-invocable: true
---

# Codex Review スキル

OpenAI Codex CLI (GPT-5) を使用して、現在のブランチのコード変更を親ブランチと比較してレビューします。

**IMPORTANT: このスキルを使用する際は、特に指定が無い限り日本語でユーザーとコミュニケーションを取ってください。**

## 概要

このスキルは、Goベースの高性能SSP（Supply Side Platform）広告サーバーのコードレビューに最適化されています。Echoフレームワークを使用したプロジェクトを想定しています。

## ワークフロー

### 1. 親ブランチの特定

まず親ブランチを特定します。以下のコマンドを実行してください。

```bash
# 現在のブランチを確認
git branch --show-current

# マージ元のブランチを推測（develop, main, master のいずれか）
git branch -r | grep -E 'origin/(develop|main|master)$' | head -1

# または、直近のマージコミットから親ブランチを確認
git log --oneline --merges -1
```

親ブランチが不明な場合は、ユーザーに確認してください。

### 2. Codex CLI でレビュー実行

特定した親ブランチ名を `<PARENT_BRANCH>` に置き換えて、以下のコマンドを実行します。

```bash
codex exec -m "gpt-5.2-codex" "'git diff <PARENT_BRANCH>...HEAD' を実行してコード変更を取得し、以下の観点でレビューしてください：
1. コード品質とGoのベストプラクティス
2. パフォーマンス（メモリ効率、レイテンシ、スループット）
3. 潜在的な問題やバグ
4. 改善提案

コンテキスト: これはGoとEchoフレームワークで構築された高性能SSP（Supply Side Platform）広告サーバーです。"
```

**例**: 親ブランチが `develop` の場合、`git diff develop...HEAD` となります。

### 3. 結果の表示

Codexのレビュー結果を日本語で表示します。

### 4. 要約

必要に応じて、主要な発見事項を日本語で要約します。

## レビュー観点

1. **コード品質**: Goのベストプラクティスに沿っているか
2. **パフォーマンス**: メモリ効率、レイテンシ、スループット
3. **潜在的な問題**: バグやエッジケース
4. **改善提案**: より良い実装方法

## 注意事項

- 差分が空の場合は、レビューする変更がないことを通知してください
- 差分が非常に大きい場合は、主要な変更点に絞ってレビューを依頼することを検討
- Codex CLI (`codex`) がインストールされていない場合は、インストール方法を案内

## トラブルシューティング

### Codex CLI が見つからない

```bash
# npm でインストール
npm install -g @openai/codex
```

### 認証エラー

OpenAI APIキーが設定されているか確認してください。
