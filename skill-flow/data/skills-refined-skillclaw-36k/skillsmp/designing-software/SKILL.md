---
name: designing-software
description: Use when planning features, designing APIs, or making architectural decisions. Covers property discovery, C4 modeling, and SOLID principles.
---

# Designing Software

## Overview

Design happens before code. Good design surfaces edge cases, clarifies contracts, and reveals hidden assumptions before they become bugs. This skill provides frameworks for thinking through designs systematically.

## When to Use

- Planning a new feature or module
- Designing an API or interface
- Making architectural decisions
- Reviewing a design document or proposal
- Refactoring existing code

## Property Discovery

Before implementation, ask discovery questions to surface the properties your code must satisfy. Properties caught during design are cheaper than properties caught during testing.

### Discovery Questions

| Property | Discovery Question | If Yes, Document |
|----------|-------------------|------------------|
| **Roundtrip** | Does an inverse operation exist? | `decode(encode(x)) == x` |
| **Idempotence** | Is applying twice the same as once? | `f(f(x)) == f(x)` |
| **Invariants** | What quantities are preserved? | Length, count, sum, ordering |
| **Commutativity** | Is argument order irrelevant? | `f(a,b) == f(b,a)` |
| **Associativity** | Can operations be regrouped? | `f(f(a,b),c) == f(a,f(b,c))` |
| **Identity** | Does a neutral element exist? | `f(x, identity) == x` |
| **Oracle** | Is there a reference implementation? | `new_impl(x) == old_impl(x)` |
| **Verifiability** | Can output correctness be easily checked? | `is_sorted(sort(x))` |

### Design Questions Surfaced

Property discovery often reveals implicit decisions:

- **Deleted/deactivated entities** — Soft delete or hard delete? Filter by default?
- **Case sensitivity** — Case-insensitive matching? Normalized storage?
- **Sort stability** — Preserve original order for ties?
- **Null handling** — Nullable fields? Default values? Explicit vs implicit nulls?
- **Concurrency** — Thread-safe? Atomic operations needed?
- **Idempotency keys** — Retry-safe? Duplicate detection?

Document these decisions explicitly rather than discovering them during implementation.

### Example: File Sync Feature

Before coding, ask:

1. **Roundtrip** — Can we reconstruct local state from remote? Remote from local?
2. **Idempotence** — Is syncing twice the same as syncing once?
3. **Invariants** — Is file count preserved? File contents?
4. **Commutativity** — Does sync order matter (A then B vs B then A)?

Answers reveal design requirements:
- Need conflict resolution strategy (commutativity fails)
- Need checksums for verification (invariant checking)
- Need sync state tracking (idempotence requires knowing what's already synced)

## Architecture Levels

Use C4 Model abstractions to discuss systems at appropriate detail levels.

| Level | Abstraction | Audience | Shows |
|-------|-------------|----------|-------|
| 1 | System Context | Everyone | System, users, external dependencies |
| 2 | Container | Technical | Deployable units, communication protocols |
| 3 | Component | Developers | Internal modules, responsibilities |
| 4 | Code | Developers | Classes, functions (rarely needed) |

**Start at Level 1.** Most discussions need only Levels 1-2. Component diagrams go stale quickly; automate or skip them.

**Diagram format:** Use Mermaid syntax for all diagrams. Mermaid renders natively in most markdown viewers and is more maintainable than ASCII art.

See [c4-model-reference.md](c4-model-reference.md) for detailed guidance.

## Design Principles

Apply SOLID principles with Python pragmatism:

| Principle | Core Idea | Apply When |
|-----------|-----------|------------|
| **Single Responsibility** | One reason to change | Always |
| **Open/Closed** | Extend without modifying | Plugin systems, stable APIs |
| **Liskov Substitution** | Subtypes are substitutable | Class hierarchies, Protocols |
| **Interface Segregation** | Small, focused interfaces | Large Protocols, testability |
| **Dependency Inversion** | Depend on abstractions | Testability, flexibility |

**Python nuance**: Duck typing and composition reduce the need for formal abstractions. Don't over-engineer; wait for patterns to emerge before abstracting.

See [solid-principles-reference.md](solid-principles-reference.md) for examples and anti-patterns.

## Design Checklist

Before implementation:

- [ ] Properties identified and documented
- [ ] Edge cases surfaced through discovery questions
- [ ] Appropriate abstraction level chosen (system/container/component)
- [ ] Dependencies flow toward abstractions, not concretions
- [ ] Each module has a single, clear responsibility

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Skipping property discovery | Edge cases found late, in production | Ask discovery questions upfront |
| Over-detailed diagrams | Go stale, aren't maintained | Use Level 1-2; Level 3 only if valuable |
| Premature abstraction | Complexity without benefit | Wait for three use cases |
| Designing for hypotheticals | YAGNI violation | Design for current requirements |
| Implicit decisions | Inconsistent implementation | Document case sensitivity, null handling, etc. |

## Anti-Rationalizations

- "I'll figure out edge cases during implementation" — You'll ship bugs. Ask discovery questions now.
- "We might need this flexibility later" — Add flexibility when you need it, not before.
- "A diagram will clarify this" — Only if it's the right level of detail. Start with Level 1.
- "This is too simple to design" — Simple features have hidden complexity. Spend 5 minutes on discovery questions.

## Supporting References

- [c4-model-reference.md](c4-model-reference.md) — C4 Model abstractions and diagram types
- [solid-principles-reference.md](solid-principles-reference.md) — SOLID principles with Python examples

## Summary

1. **Ask property discovery questions before coding.** Roundtrip, idempotence, invariants — surface edge cases early.
2. **Document implicit decisions.** Case sensitivity, null handling, sort stability — make them explicit.
3. **Start at the right abstraction level.** System Context for most discussions; Container for technical detail.
4. **Wait for patterns before abstracting.** Three use cases, then generalize.
