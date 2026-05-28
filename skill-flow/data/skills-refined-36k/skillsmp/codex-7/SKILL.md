---
name: codex
description: OpenAI Codex CLIを使用したコードレビュー、分析、コードベースへの質問を実行する。使用場面: (1) コードレビュー依頼時、(2) コードベース全体の分析、(3) 実装に関する質問、(4) バグの調査、(5) リファクタリング提案、(6) 解消が難しい問題の調査。トリガー: "codex", "コードレビュー", "レビューして", "分析して", "/codex"
allowed-tools: Bash(codex*)
---

# Codex Code Review & Analysis

OpenAI Codex CLIを使用してコードレビュー・分析を実行するスキル。

## Prerequisites

このスキルはOpenAI Codex CLI (`codex`) がシステムにインストールされている必要があります。

```bash
# Installation check
codex --version
```

Codex CLIがインストールされていない場合は、[OpenAI Codex CLI](https://github.com/openai/codex)を参照してください。

## 実行コマンド

```bash
codex exec --full-auto --sandbox read-only --cd <project_directory> "<request>"
```

## パラメータ

| パラメータ | 説明 |
|-----------|------|
| `--full-auto` | 完全自動モードで実行 |
| `--sandbox read-only` | 読み取り専用サンドボックス（安全な分析用） |
| `--cd <dir>` | 対象プロジェクトのディレクトリ |
| `"<request>"` | 依頼内容（日本語可） |

## 使用例

### コードレビュー
```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project "このプロジェクトのコードをレビューして、改善点を指摘してください"
```

### バグ調査
```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project "認証処理でエラーが発生する原因を調査してください"
```

### アーキテクチャ分析
```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project "このプロジェクトのアーキテクチャを分析して、改善提案をしてください"
```

### リファクタリング提案
```bash
codex exec --full-auto --sandbox read-only --cd /path/to/project "重複コードや改善可能な箇所を特定し、リファクタリング案を提示してください"
```

## 実行手順

1. ユーザーから依頼内容を受け取る
2. 対象プロジェクトのディレクトリを特定する（デフォルト: 現在の作業ディレクトリ）
3. 上記コマンド形式でCodexを実行
4. 結果をユーザーに報告

## When This Skill Activates

- "codex"
- "Codexで分析して"
- "コードレビュー"
- "レビューして"
- "分析して"
- "コードベースを調査して"
- "バグの原因を調べて"
- "リファクタリング提案"
- "/codex"
