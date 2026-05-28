---
description: Document reusable design patterns with structure and examples
---

# Pattern - Design Pattern Library

Document reusable design patterns with structure, examples, and usage guidelines.

## Usage

```
/pattern [name]
/pattern retry-with-backoff
/pattern worker-coordination
```

**Output:** `$PROJECT_ROOT/docs/patterns/[name].md`

## Instructions

1. **Parse name** → kebab-case filename
2. **Ask user** about the pattern:
   - What type? (behavioral/structural/creational)
   - What problem does it solve?
   - What language for the example?
3. **Generate** pattern document
4. **Save** to `docs/patterns/[name].md`

## Template

```markdown
# [Pattern Name]

| Field | Value |
|-------|-------|
| Type | Behavioral / Structural / Creational |
| Language | [primary language] |
| Tags | [tag1, tag2] |
| Created | YYYY-MM-DD |

## Intent

> One sentence describing what this pattern solves.

## Problem

What situation triggers the need for this pattern?

## Solution

How the pattern addresses the problem.

## Structure

```[language]
// Key interfaces/types
```

## Example

```[language]
// Complete working example
```

## When to Use

- Situation 1
- Situation 2

## When NOT to Use

- Anti-situation 1
- Anti-situation 2

## Trade-offs

| Pro | Con |
|-----|-----|
| [benefit] | [cost] |

## Related Patterns

- [Pattern A] - [relationship]
- [Pattern B] - [relationship]

## References

- [link or source]
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/distill` | Extract patterns from learnings |
| `/example` | Save code examples |
| `/pattern` | Document patterns (you are here) |
| `/search` | Find existing patterns |
