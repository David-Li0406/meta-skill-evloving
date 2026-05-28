---
name: error-handling
description: Use this skill when you need to determine the appropriate error handling strategy in your code, considering whether failures are expected or exceptional.
---

# Error Handling

> **Layer 1: Language Mechanics**

## Core Question

**Is this failure expected or a bug?**

Before choosing an error handling strategy, consider:
- Can this fail in normal operation?
- Who should handle this failure?
- What context does the caller need?

---

## Error → Design Question

| Pattern | Don't Just Say | Ask Instead |
|---------|----------------|-------------|
| unwrap panics | "Use ?" | Is None/Err actually possible here? |
| Type mismatch on ? | "Use anyhow" | Are error types designed correctly? |
| Lost error context | "Add .context()" | What does the caller need to know? |
| Too many error variants | "Use Box<dyn Error>" | Is error granularity right? |

---

## Thinking Prompt

Before handling an error:

1. **What kind of failure is this?**
   - Expected → `Result<T, E>`
   - Absence normal → `Option<T>`
   - Bug/invariant → `panic!`
   - Unrecoverable → `panic!`

2. **Who handles this?**
   - Caller → propagate with `?`
   - Current function → match/if-let
   - User → friendly error message
   - Programmer → panic with message

3. **What context is needed?**
   - Type of error → `thiserror` variants
   - Call chain → `anyhow::Context`
   - Debug info → `anyhow` or `tracing`

---

## Trace Up ↑

When error strategy is unclear:

```
"Should I return Result or Option?"
    ↑ Ask: Is absence/failure normal or exceptional?
    ↑ Check: m09-domain (what does domain say?)
    ↑ Check: domain-* (error handling requirements)
```

| Situation | Trace To | Question |
|-----------|----------|----------|
| Too many unwraps | m09-domain | Is the data model right? |
| Error context design | m13-domain-error | What recovery is needed? |
| Library vs app errors | m11-ecosystem | Who are the consumers? |

---

## Trace Down ↓

From design to implementation:

```
"Expected failure, library code"
    ↓ Use: `thiserror` for typed errors

"Expected failure, application code"
    ↓ Use: `anyhow` for ergonomic errors

"Absence is normal (find, get, lookup)"
    ↓ Use: `Option<T>`

"Bug or invariant violation"
    ↓ Use: `panic!`, `assert!`, `unreachable!`

"Need to propagate with context"
    ↓ Use: `.context("what was happening")`
```

---

## Quick Reference

| Pattern | When | Example |
|---------|------|---------|
| `Result<T, E>` | When the failure is expected and can be handled | `let result: Result<T, E> = ...;` |
| `Option<T>` | When absence is normal | `let option: Option<T> = ...;` |
| `panic!` | When a bug or invariant violation occurs | `panic!("This should never happen!");` |
| `anyhow` | For ergonomic error handling in application code | `let err = anyhow!("An error occurred: {}", e);` |
| `thiserror` | For typed error handling in library code | `#[derive(thiserror::Error)]` |