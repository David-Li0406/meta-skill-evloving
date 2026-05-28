---
name: fix-checklist
description: Use when about to fix code, modify implementation, or address errors. MUST read before saying "修正します", "fix", "修正する", "直す", "対処する". Prevents symptom-driven fixes.
allowed-tools: [Read, Glob, Grep]
---

# Before You Fix: Stop and Think

**Read this BEFORE making any code changes.**

## The Rule

```
落ち着け。
じっくり考えて、one by one で確かめろ。
深掘りしろ。
```

## Why This Exists

Symptom-driven fixes are wrong fixes. Seeing an error and immediately "fixing" it without understanding WHY the error occurs leads to:

- Breaking the design
- Introducing new bugs
- Wasting time on wrong solutions

## Checklist (Do Not Skip)

### 1. Stop

Do NOT write code yet. Do NOT edit files yet.

### 2. Ask "Why?"

The error is a symptom. Ask:
- Why is this error occurring?
- What is the system trying to do?
- What did the system expect vs what happened?

### 3. Read the Design

Before changing ANY code:
- Find the relevant design document
- Read it completely
- Understand the intended behavior

Common locations:
- `agents/docs/design/` - Agent architecture
- `docs/` - Project documentation
- Schema files - Structural contracts

### 4. Trace the Flow

Follow the execution path:
1. What triggered this code?
2. What state was expected?
3. Where did it diverge?

### 5. Identify Root Cause

The fix location is often NOT where the error appears.

| Error Location | Root Cause Location |
|----------------|---------------------|
| Runtime validation | Schema definition |
| Intent not allowed | Prompt instruction |
| Type mismatch | Interface contract |
| Test failure | Implementation logic |

### 6. Verify Your Understanding

Before fixing, state:
- What is the root cause?
- Why does the design work this way?
- What is the minimal correct fix?

### 7. Then Fix

Only now: make the smallest change that addresses the root cause.

## Anti-Patterns

**Bad**: "Error says X not in Y, so add X to Y"

**Good**: "Error says X not in Y. Why is code producing X? Is X correct? What does design say about X?"

## Example

```
Error: Intent 'handoff' not in allowedIntents

Bad fix: Add 'handoff' to allowedIntents
  → Doesn't ask WHY handoff is being returned

Good process:
  1. Why is agent returning 'handoff'?
  2. Check design: initial.* steps should NOT use handoff
  3. Root cause: prompt tells agent to use handoff
  4. Correct fix: update prompt to use 'next' instead
```

## Investigation Output: tmp/ Directory

調査・思考結果は `tmp/` 配下に階層を作り整理する。

### Structure

```
tmp/
└── investigation/
    └── <issue-name>/
        ├── overview.md      # 問題の全容（mermaid図必須）
        ├── trace.md         # 実行フロー追跡
        └── root-cause.md    # 根本原因と修正方針
```

### Rules

1. **端的なmermaid図で整理する** - 文章より図で構造を示す
2. **1ファイル500行以内** - 超えたら要約して分割
3. **問題の全容と本質的な構造を見極める**

### Mermaid Example

```markdown
## Problem Structure

\`\`\`mermaid
flowchart TD
    A[Error: X not found] --> B{Where?}
    B --> C[Validation layer]
    B --> D[Schema definition]
    C --> E[Symptom]
    D --> F[Root Cause]
    F --> G[Fix: Update schema]
\`\`\`
```

### When to Use

- 複雑な問題で即座に原因が分からない時
- 複数のコンポーネントが絡む時
- 後で振り返りが必要になりそうな時

### Output Quality

| Bad | Good |
|-----|------|
| 長文の羅列 | mermaid図で構造化 |
| 500行超のファイル | 要約して分割 |
| 症状の列挙のみ | 本質的な構造の特定 |
