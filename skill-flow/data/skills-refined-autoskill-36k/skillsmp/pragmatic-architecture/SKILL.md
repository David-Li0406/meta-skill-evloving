---
name: pragmatic-architecture
description: |
  Prevents over-engineering by enforcing industry-proven principles: AHA (Avoid Hasty Abstractions),
  YAGNI, Colocation, and Rule of Three. Use when designing features, planning architecture,
  "architect this", "design the structure", or when the code-architect agent is dispatched.
  Triggers: file structure, module organization, abstraction decisions, component splitting.
allowed-tools: []
---

# Pragmatic Architecture

Design for today's requirements. Let complexity grow incrementally as needed.

## The Four Principles

### 1. Rule of Three (Don Roberts)

> "The first time, just do it. The second time, wince at duplication but do it anyway. The third time, refactor."

**Abstract on the 3rd occurrence, not before.**

| Occurrences | Action |
|-------------|--------|
| 1 | Implement directly |
| 2 | Duplicate, note similarity |
| 3+ | Now extract abstraction |

### 2. AHA - Avoid Hasty Abstractions (Kent C. Dodds)

> "Prefer duplication over the wrong abstraction." — Sandi Metz

**Duplication is cheaper than the wrong abstraction.** Wrong abstractions accumulate parameters and conditionals until unmaintainable.

Signs of wrong abstraction:
- Adding parameters to handle "just one more case"
- Conditional paths through shared code
- Comments explaining which caller uses which path

**Recovery:** Inline the abstraction, re-duplicate, let the right pattern emerge.

### 3. YAGNI - You Ain't Gonna Need It (Ron Jeffries)

> "Always implement things when you actually need them, never when you just foresee that you need them."

**No hooks for future features.** No "we might need this someday."

| ❌ Speculative | ✅ Pragmatic |
|----------------|--------------|
| `options?: ExtensionConfig` unused | Add when extension exists |
| Abstract factory for one impl | Direct instantiation |
| Event system for single listener | Direct call |
| Plugin architecture for no plugins | Hardcoded behavior |

### 4. Colocation (Kent C. Dodds)

> "Place code as close to where it's relevant as possible."

**Minimize file splitting. Keep related code together.**

| ❌ Over-split | ✅ Colocated |
|---------------|--------------|
| `types/user.ts`, `utils/user.ts`, `constants/user.ts` | Single `user.ts` with all |
| Separate `styles/`, `hooks/`, `utils/` folders | Component folder with all related |
| 10 files for one feature | 1-3 files max per feature |

## Decision Framework

Before creating abstraction, ask:

```text
1. Does this exist 3+ times? → No? Don't abstract
2. Are the use cases truly identical? → No? Don't abstract
3. Would someone unfamiliar understand this? → No? Simpler design
4. Am I solving today's problem? → No? YAGNI
```

## File Organization Rules

**Prefer:**
- Feature-based folders over type-based folders
- Fewer, larger files over many tiny files
- Colocated tests (`foo.test.ts` next to `foo.ts`)
- Single source of truth per concept

**Avoid:**
- `types/`, `utils/`, `constants/`, `helpers/` folders that scatter related code
- Files under 50 lines (usually should be merged)
- More than 3 files per feature (unless genuinely complex)

## Anti-Patterns to Block

### Speculative Generality (Fowler)

> "Oh, I think we'll need the ability to do this someday"

Symptoms: Abstract classes doing nothing, unused parameters, delegation that could be direct.

**Block:** Any "for future use" justification.

### Shotgun Surgery (Fowler)

> "One change requires modifications across many files"

Caused by over-splitting. Fix by consolidating related code.

**Block:** Designs requiring 5+ file changes for simple features.

### Premature Abstraction

Creating `BaseHandler`, `AbstractService`, `GenericRepository` before concrete needs exist.

**Block:** Any abstract class without 2+ concrete implementations in the plan.

## Output Requirements

When designing architecture:

1. **Justify every new file** — Why can't this live in an existing file?
2. **Justify every abstraction** — Where are the 3 concrete uses?
3. **Prefer boring** — Standard patterns over clever solutions
4. **Count the files** — If feature needs 5+ files, reconsider

## References

For detailed patterns and examples:
- `references/file-organization.md` — Colocated vs scattered patterns
- `references/abstraction-examples.md` — Good vs bad abstraction decisions
