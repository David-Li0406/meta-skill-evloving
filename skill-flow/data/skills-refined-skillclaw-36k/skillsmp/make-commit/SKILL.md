---
name: make-commit
description: 変更内容を分析し、Conventional Commits形式でコミットを作成する
allowed-tools: Read, Grep, Glob
disable-model-invocation: true
---

# make-commit

## Context

- Status: !`git status --short`
- Staged: !`git diff --staged --stat`

## 概要

変更内容を分析し、Conventional Commits形式でコミットを作成する。

## Conventional Commits規則

[git-conventions.md](../_shared/git-conventions.md) の以下を参照:

- Commit Type
- Commit Message Format

## 実行手順

### 1. 変更内容の確認

Contextセクションを確認し、ステージされた変更がない場合は「ステージされた変更がありません。」と出力して処理を終了。

変更がある場合は、詳細な差分を取得。

```bash
git diff --staged --ignore-all-space --ignore-blank-lines
```

### 2. 言語の選択

```text
🌐 言語の選択
────────────────────────────────────────
1. 英語
2. 日本語

(1-2):
```

ユーザーが番号を選択したら以下を実行。

- 有効な番号が選択された場合
  - 選択された言語を記録
- 無効な番号が選択された場合
  - 「無効な番号です。もう一度番号を選択してください。」と再入力を促す

### 3. コミットメッセージの選択

コミットメッセージの候補を提示。

- **MUST**: 番号が小さいほど推奨度が高い
- **SHOULD**: 1〜3グループの候補を提示し、各グループに簡潔版と詳細版を用意する

```text
🤖 コミットメッセージの選択
────────────────────────────────────────
[ステージされた変更]

💬 コミットメッセージ
────────────────────────────────────────
理由: [選定理由1]

1. type: concise description (簡潔版)
2. type: detailed descriptive message (詳細版)

理由: [選定理由2]

3. type: alternative concise (簡潔版)
4. type: alternative detailed message (詳細版)

(1-4):
```

### 4. コミットの作成

- 有効な番号が選択された場合
  - 選択されたメッセージでコミットを作成
- 無効な番号が選択された場合
  - 「無効な番号です。もう一度番号を選択してください。」と再入力を促す
