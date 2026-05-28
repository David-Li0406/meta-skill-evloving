---
name: writing-effective-comments
description: Write effective code comments following principles from "A Philosophy of Software Design". Use when documenting code, reviewing comments, or improving existing documentation.
---

# Writing Effective Comments

## When to Use This Skill

- Writing documentation for new code
- Reviewing or improving existing comments
- Documenting interfaces, classes, or modules
- Adding implementation comments for complex logic
- Learning language-specific documentation conventions

## The Golden Rule

> **Comments should describe things that are not obvious from the code.**

If a comment repeats what the code already says, it adds no value. Good comments capture information that exists only in the developer's mind: rationale, intent, constraints, and design decisions.

## Quick Reference

| Need | Go To |
|------|-------|
| Core principles of good comments | [philosophy.md](philosophy.md) |
| What to avoid (bad patterns) | [antipatterns.md](antipatterns.md) |
| Practical workflow for writing comments | [workflow.md](workflow.md) |
| Documenting interfaces/APIs | [interface_comments.md](interface_comments.md) |
| In-code implementation comments | [implementation_comments.md](implementation_comments.md) |
| Good vs bad examples | [examples.md](examples.md) |

## Language-Specific Conventions

| Language | Convention | Guide |
|----------|------------|-------|
| JavaScript/TypeScript | JSDoc | [conventions/jsdoc.md](conventions/jsdoc.md) |
| Ruby | YARD | [conventions/yard.md](conventions/yard.md) |
| Go | godoc | [conventions/godoc.md](conventions/godoc.md) |
| Rust | rustdoc | [conventions/rustdoc.md](conventions/rustdoc.md) |
| Elixir | ExDoc | [conventions/exdoc.md](conventions/exdoc.md) |

## Comment Types at a Glance

### Interface Comments (What and Why)
Document the abstraction for users who won't read the implementation:
- What does it do? (high-level purpose)
- What do parameters mean? (not just types)
- What does it return? (semantic meaning)
- What side effects occur?
- What can go wrong?

### Implementation Comments (How and Why)
Explain non-obvious code for future maintainers:
- Why was this approach chosen?
- What's the algorithm doing at a high level?
- What constraints or edge cases matter?
- What would break if this changed?

## Core Principles Summary

1. **Write comments first** - Document before implementing to clarify thinking
2. **Use different words** - Comments at a different abstraction level than code
3. **Capture intent** - Code shows what, comments explain why
4. **Keep close to code** - Comments near the code they describe stay accurate
5. **Review comments** - Treat comment quality as seriously as code quality
