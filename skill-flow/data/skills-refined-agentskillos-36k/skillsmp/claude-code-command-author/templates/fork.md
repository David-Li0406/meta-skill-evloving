# Fork Command Template

会話を汚したくない、または重い処理を分離したいコマンド向けテンプレート。
実行が別コンテキストで行われ、結果だけが返される。

## Template

```md
---
description: <短い説明>
context: fork
agent: general-purpose
argument-hint: [optional-args]
---

# <Command Title>

## Your task
<やること。必要なら $ARGUMENTS や $1.. を使う>

## Constraints
- <制約>

## Output
- <出力形式>
```

## agent の選択肢

| agent | 用途 |
|-------|------|
| `general-purpose` | 汎用タスク（デフォルト） |
| `explore` | コードベース探索 |
| `Bash` | コマンド実行特化 |

## 使いどころ

- **重い分析タスク**: 大量のファイルを読む、複雑な調査
- **会話を汚したくない**: 途中経過を見せたくない
- **独立した作業**: メインの会話と関係ない調査

## Example: Deep Analysis

```md
---
description: Deep analysis of codebase architecture
context: fork
agent: general-purpose
argument-hint: [area]
---

# Deep Architecture Analysis

## Your task
- Analyze the architecture of the specified area: $ARGUMENTS
- Identify patterns, dependencies, and potential issues
- Create a comprehensive report

## Constraints
- Read-only analysis
- Focus on architecture, not implementation details

## Output
- Markdown report with:
  - Overview
  - Key components
  - Dependency graph (Mermaid)
  - Recommendations
```

## Example: Research Task

```md
---
description: Research and summarize a topic
context: fork
agent: general-purpose
argument-hint: [topic]
---

# Research Task

## Your task
- Research the topic: $ARGUMENTS
- Gather information from the codebase
- Summarize findings

## Constraints
- Do not modify any files
- Focus on facts, not opinions

## Output
- Summary of findings
- Relevant file references
- Open questions (if any)
```

## 注意点

- fork されたコンテキストは **元の会話履歴を引き継がない**
- 結果のみが返され、途中経過は見えない
- 長時間実行の場合、ユーザーは待つことになる
