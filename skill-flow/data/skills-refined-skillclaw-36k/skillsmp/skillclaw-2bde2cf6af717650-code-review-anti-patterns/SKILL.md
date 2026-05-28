---
name: code-review-anti-patterns
description: Use this skill when reviewing code to identify and address common anti-patterns that may indicate deeper design issues.
---

# Anti-Patterns

> **Layer 2: Design Choices**

## Core Question

**Is this pattern hiding a design problem?**

When reviewing code:
- Is this solving the symptom or the cause?
- Is there a more idiomatic approach?
- Does this fight or flow with Rust?

---

## Anti-Pattern → Better Pattern

| Anti-Pattern | Why Bad | Better |
|--------------|---------|--------|
| `.clone()` everywhere | Hides ownership issues | Proper references or ownership |
| `.unwrap()` in production | Runtime panics | Use `?`, `expect`, or proper error handling |
| `Rc` when single owner | Unnecessary overhead | Use simple ownership |
| `unsafe` for convenience | Risk of undefined behavior | Find a safe pattern |
| OOP via `Deref` | Misleading API | Prefer composition and traits |
| Giant match arms | Unmaintainable | Extract to methods for clarity |
| `String` everywhere | Wasteful allocations | Use `&str` or `Cow<str>` |
| Ignoring `#[must_use]` | Potentially lost errors | Handle or use `let _ =` |

---

## Thinking Prompts

When encountering suspicious code:

1. **Is this symptom or cause?**
   - Clone to avoid borrow? → Indicates an ownership design issue.
   - Unwrap "because it won't fail"? → Suggests an unhandled case.

2. **What would idiomatic code look like?**
   - Use references instead of clones.
   - Prefer iterators over index loops.
   - Utilize pattern matching instead of flags.

3. **Does this fight Rust?**
   - Restructure code that fights the borrow checker.
   - Avoid excessive use of `unsafe` and find safe alternatives.

---

## Trace Up ↑

To enhance design understanding:

```
"Why does my code have so many clones?"
    ↑ Ask: Is the ownership model correct?
    ↑ Check: m09-domain (data flow design)
    ↑ Check: m01-ownership (reference patterns)
```

| Anti-Pattern | Trace To | Question |
|--------------|----------|----------|
| Clone everywhere | m01-ownership | Who should own this data? |
| Unwrap everywhere | m06-error-handling | What's the error strategy? |
| Rc everywhere | m09-domain | Is ownership clear? |
| Fighting lifetimes | m09-domain | Should the data structure change? |

---

## Trace Down ↓

To implementation (Layer 1):

```
"Replace clone with proper ownership"
    ↓ m01-ownership: Reference patterns
```