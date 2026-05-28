---
name: codex-review
description: Use this skill when you need to perform a code review using OpenAI Codex, focusing on code quality, performance, and security aspects before merging changes.
---

# Skill body

## 概要

このスキルは、OpenAI Codex CLI (GPT-5) を使用して、コードの変更をレビューします。特に、Goベースの高性能SSP（Supply Side Platform）広告サーバーのプロジェクトに最適化されています。

## ワークフロー

### 1. 親ブランチの特定

まず、親ブランチを特定します。以下のコマンドを実行してください。

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
4. セキュリティ（SQLインジェクション、認証/認可、入力検証など）
5. 改善提案

コンテキスト: これはGoとEchoフレームワークで構築された高性能SSP広告サーバーです。"
```

**例**: 親ブランチが `develop` の場合、`git diff develop...HEAD` となります。

### 3. 結果の表示

Codexのレビュー結果を日本語で表示します。

### 4. 要約

主要な発見事項と実行可能な推奨事項を日本語で要約します。

## 注意事項

- 差分が空の場合は、レビューする変更がないことを通知してください。
- 差分が非常に大きい場合は、主要な変更点に絞ってレビューを依頼することを検討してください。
- Codex CLI (`codex`) がインストールされていない場合は、インストール方法を案内してください。

## トラブルシューティング

### Codex CLI が見つからない

```bash
# npm でインストール
npm install -g @openai/codex
```

### 認証エラー

OpenAI APIキーが設定されているか確認してください。