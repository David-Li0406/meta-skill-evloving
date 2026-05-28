---
title: Concise is Key
impact: CRITICAL
impactDescription: Context window is a scarce public good
tags: principles, context-window
---

## Concise is Key

**Impact: CRITICAL (Context window is a scarce public good)**

Skills share the context window with the system prompt, conversation history, and user requests. Assume Claude is smart. Only add context Claude doesn't have. Challenge every paragraph: "Does this justify its token cost?"

**Incorrect (verbose explanation):**

```markdown
# Instructions

It is very important to understand that when you are writing code, you should make sure that the code is clean and readable. This is because clean code is easier to maintain and debug. If you write messy code, it will be hard for others to understand simple concepts. Therefore, always strive to write code that is simple and direct.
```

**Correct (concise directive):**

```markdown
# Instructions

Write clean, readable code. Prioritize maintainability and clarity.
```
