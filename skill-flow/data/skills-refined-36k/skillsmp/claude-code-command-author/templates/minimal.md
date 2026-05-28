# Minimal Command Template

最小構成のコマンドテンプレート。読み取り専用・安全な用途向け。

## Template

```md
---
description: <短い説明（/help で表示される）>
argument-hint: [optional-args]
---

# <Command Title>

## Your task
- <やること1>
- <やること2>

## Constraints
- Do not edit files unless explicitly requested.
- If unsure, ask one clarification question.

## Output
- <出力形式（Markdown, チェックリスト, など）>
```

## Usage

```
/command-name [args]
```

## Example

```md
---
description: Review code for best practices
argument-hint: [file-path]
---

# Code Review

## Your task
- Review the specified file for best practices
- Check for common issues: security, performance, readability
- Provide actionable suggestions

## Constraints
- Do not edit files, only provide suggestions
- Focus on the most important issues (max 5)

## Output
- Markdown list of issues with severity (high/medium/low)
- Code snippets showing suggested fixes
```
