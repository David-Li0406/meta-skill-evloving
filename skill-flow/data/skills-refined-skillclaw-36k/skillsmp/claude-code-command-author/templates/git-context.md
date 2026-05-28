# Git Context Command Template

git status/diff/log を事前に埋め込むコマンドテンプレート。
コミットメッセージ生成、差分レビューなどに最適。

## Template

```md
---
description: <短い説明>
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*)
argument-hint: [optional-args]
---

# <Command Title>

## Context
- status: !`git status`
- diff: !`git diff HEAD`
- recent commits: !`git log --oneline -10`

## Your task
<このコンテキストを使ってやること>

## Constraints
- Do not run destructive git commands (push, reset --hard, etc.)
- If changes are unclear, ask for clarification

## Output
- <出力形式>
```

## allowed-tools の調整

### 最小限（status のみ）
```yaml
allowed-tools: Bash(git status:*)
```

### 標準（status + diff）
```yaml
allowed-tools: Bash(git status:*), Bash(git diff:*)
```

### フル（status + diff + log）
```yaml
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*)
```

## Example: Commit Message Generator

```md
---
description: Generate commit message from staged changes
allowed-tools: Bash(git status:*), Bash(git diff:*)
---

# Generate Commit Message

## Context
- status: !`git status`
- staged diff: !`git diff --cached`

## Your task
- Analyze the staged changes
- Generate a concise, conventional commit message
- Follow the format: type(scope): description

## Constraints
- Do not actually commit (only generate the message)
- Keep the message under 72 characters for the first line

## Output
- Suggested commit message in a code block
- Brief explanation of why this message fits
```

## Example: Diff Review

```md
---
description: Review uncommitted changes
allowed-tools: Bash(git status:*), Bash(git diff:*)
---

# Review Changes

## Context
- status: !`git status`
- all changes: !`git diff HEAD`

## Your task
- Review all uncommitted changes
- Check for: bugs, security issues, incomplete code
- Identify files that might need more attention

## Constraints
- Do not edit files
- Focus on potential issues, not style

## Output
- Summary of changes by file
- List of concerns (if any)
- Recommendation: ready to commit / needs work
```
