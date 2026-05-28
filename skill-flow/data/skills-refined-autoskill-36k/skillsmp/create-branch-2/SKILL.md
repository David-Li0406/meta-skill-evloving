---
name: create-branch
description: 変更内容を分析し、適切なGitブランチを作成する
allowed-tools: Read, Grep, Glob
disable-model-invocation: true
---

# create-branch

## Context

- Status: !`git status --short`
- Changes: !`git diff --stat`
- Staged: !`git diff --staged --stat`

## 概要

変更内容を分析し、適切なGitブランチを作成する。

## ブランチ名規則

[git-conventions.md](../_shared/git-conventions.md) の以下を参照:

- Branch Prefix
- Branch Name Format

## 実行手順

### 1. 変更内容の確認

Contextセクションを確認。変更がない場合は会話履歴から作業内容を推測。

変更がある場合は、詳細な差分を取得。

```bash
git diff --ignore-all-space --ignore-blank-lines
git diff --staged --ignore-all-space --ignore-blank-lines
```

### 2. ブランチの選択

ブランチ名の候補を提示。

- **MUST**: すべてのブランチ名に必ず変更対象を含める
- **MUST**: 番号が小さいほど推奨度が高い
- **SHOULD**: 1〜3グループの候補を提示し、各グループに簡潔版と詳細版を用意する

```text
🤖 ブランチの選択
────────────────────────────────────────
[ステージされた変更、未ステージの変更、または会話履歴からの推測内容]
[会話履歴からの推測の場合は「※ 会話履歴から推測」と明記]

🔀 ブランチ名
────────────────────────────────────────
理由: [選定理由1]

1. fix/auth-bug (簡潔版)
2. fix/user-authentication-session-timeout (詳細版)

理由: [選定理由2]

3. feature/dark-mode (簡潔版)
4. feature/settings-page-dark-mode-toggle (詳細版)

(1-4):
```

### 3. ブランチの作成

ユーザーが番号を選択したら以下を実行。

- 有効な番号が選択された場合
  - ブランチ名の妥当性を検証: `git check-ref-format --branch [branch-name]`
    - ブランチ名が不正な場合
      - エラーメッセージを出力して再入力を促す
  - ブランチが既に存在するか確認: `git branch --list [branch-name]`
    - ブランチが既に存在する場合
      - 「ブランチは既に存在します。別の番号を選択してください。」と再入力を促す
    - ブランチが存在しない場合
      - 選択されたブランチ名でブランチを作成して切り替え: `git switch -c [branch-name]`
- 無効な番号が選択された場合
  - 「無効な番号です。もう一度番号を選択してください。」と再入力を促す
