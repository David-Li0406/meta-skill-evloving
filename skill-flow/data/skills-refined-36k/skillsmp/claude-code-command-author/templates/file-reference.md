# File Reference Command Template

`@path` でファイルを参照するコマンドテンプレート。
ファイル分析、説明、リファクタ提案などに最適。

## Template

```md
---
description: <短い説明>
argument-hint: [file-path]
---

# <Command Title>

## Target
@$ARGUMENTS

## Your task
<ファイルに対してやること>

## Constraints
- <制約>

## Output
- <出力形式>
```

## @ 参照の書き方

### 固定ファイル
```md
Review the config: @src/config.ts
```

### 引数で受け取り
```md
Review the file: @$ARGUMENTS
```

### 複数ファイル
```md
Compare these files:
- @$1
- @$2
```

## Example: File Explainer

```md
---
description: Explain what a file does
argument-hint: [file-path]
---

# Explain File

## Target
@$ARGUMENTS

## Your task
- Read and understand the file
- Explain its purpose and functionality
- Describe key functions/classes

## Constraints
- Do not edit the file
- Keep explanation concise (under 500 words)

## Output
- Purpose (1-2 sentences)
- Key components (bullet list)
- How it fits in the codebase
```

## Example: Refactor Suggester

```md
---
description: Suggest refactoring for a file
argument-hint: [file-path]
---

# Suggest Refactoring

## Target
@$ARGUMENTS

## Your task
- Analyze the file structure and code quality
- Identify refactoring opportunities
- Provide concrete suggestions with code examples

## Constraints
- Do not edit the file (suggestions only)
- Focus on high-impact improvements

## Output
- Current issues (bullet list)
- Suggested refactorings with:
  - What to change
  - Why it improves the code
  - Example code snippet
```

## Example: Compare Files

```md
---
description: Compare two files
argument-hint: [file1] [file2]
---

# Compare Files

## Files
- File 1: @$1
- File 2: @$2

## Your task
- Compare the two files
- Identify similarities and differences
- Suggest if they can be unified or refactored

## Constraints
- Do not edit files
- Be objective in comparison

## Output
- Similarities (bullet list)
- Differences (bullet list)
- Recommendation
```

## 注意点

- `@` 参照はコンテキストを消費する
- 大きなファイルは避けるか、必要な部分だけ参照
- 存在しないファイルを参照するとエラーになる
