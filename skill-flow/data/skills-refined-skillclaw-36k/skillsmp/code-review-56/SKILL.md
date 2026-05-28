---
name: code-review
description: Validates TypeScript/React code against dev_instruction_v3.md standards. Checks for anti-patterns like export default, onClick usage, wrapper components, and any types. Use before committing or during code review.
---

# Code Review Skill

Validates code against project standards from `dev_instruction_v3.md`.

## Anti-Patterns to Detect

| Pattern | Violation | Correct |
|---------|-----------|---------|
| `export default` | ❌ Forbidden | `export function` |
| `onClick` on HeroUI | ❌ Use onPress | `onPress={handler}` |
| Wrapper imports | ❌ No wrappers | Import from `@heroui/react` |
| `any` type | ❌ Strict typing | Define proper types |
| `"use client"` | ❌ Not for Vite SPA | Remove directive |

## How to Check

Run the standards check script:

```bash
.agent/skills/code-review/scripts/check-standards.sh src/
```

## Manual Review Checklist

- [ ] Named exports only (`export function`)
- [ ] No `any` types
- [ ] No wrapper components
- [ ] `onPress` for HeroUI interactions
- [ ] Mock data in `src/data/`
- [ ] Logic extracted to `src/hooks/`
- [ ] Data fetching uses `useQuery`
- [ ] Tested in both light and dark themes

## Reference

See `dev_instruction_v3.md` for complete coding standards.
