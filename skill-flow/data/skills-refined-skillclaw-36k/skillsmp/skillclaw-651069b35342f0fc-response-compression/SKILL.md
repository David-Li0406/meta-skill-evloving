---
name: response-compression
description: Use this skill when you need to eliminate unnecessary verbosity in responses to save tokens while maintaining clarity.
---

# Response Compression

Eliminate response bloat to save 200-400 tokens per response while maintaining clarity.

## Elimination Rules

### ELIMINATE

| Category                   | Examples                                               | Replacement             |
| -------------------------- | ------------------------------------------------------ | ----------------------- |
| **Decorative Emojis**      | `--`                                                   | (remove entirely)       |
| **Filler Words**           | "just", "simply", "basically", "essentially"           | (remove or rephrase)    |
| **Hedging Language**       | "might", "could", "perhaps", "potentially", "I think"  | Use factual statements  |
| **Hype Words**             | "powerful", "amazing", "seamless", "robust", "elegant" | Use precise descriptors |
| **Conversational Framing** | "Let's dive in", "Now that we've", "Moving forward"    | Start with content      |
| **Transitions**            | "Furthermore", "Additionally", "In conclusion"         | (remove, use structure) |
| **Call-to-Action**         | "Feel free to", "Don't hesitate to", "Let me know if"  | (remove from endings)   |

### PRESERVE (When Appropriate)

| Category                | Example                       | When to Use                      |
| ----------------------- | ----------------------------- | -------------------------------- |
| **Status Indicators**   | `[pass] [fail] [warn]`        | In structured output, checklists |
| **Technical Precision** | Exact error messages          | When debugging                   |
| **Safety Warnings**     | Critical info about data loss | Always preserve                  |
| **Context Setting**     | Brief necessary background    | When user lacks context          |

## Before/After Transformations

### Example 1: Opening Bloat

**Before** (68 tokens):
```
Great question! I'd be happy to help you understand how this works.
The bloat detector is a powerful tool that analyzes your codebase
and provides comprehensive insights into potential issues...
```

**After** (28 tokens):
```
The bloat detector analyzes codebases using three tiers: quick scan
(heuristics), static analysis (tools), and deep audit (git history).
```

### Example 2: Closing Bloat

**Before** (45 tokens):
```
I've completed the task. Here's what I did:
- Deleted 5 files
- Saved 18k tokens

Next steps:
1. Review the changes
2. Run tests
3. Commit if satisfied

Let me know if you need anything else!
```

**After** (15 tokens):
```
Done. Deleted 5 files, saved 18k tokens.
```