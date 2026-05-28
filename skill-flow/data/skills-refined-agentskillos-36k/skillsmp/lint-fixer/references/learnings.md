# Lint Fixer Learnings

Domain-specific corrections and gotchas for lint/format fixes.

## Gotchas

### Biome vs ESLint Rule Names
- **Pattern:** Looking up rule documentation
- **Wrong:** Searching ESLint docs for Biome errors
- **Right:** Biome rules are different - check biomejs.dev
- **Why:** Biome reimplemented rules with different names/behaviors

### useCallback vs Inline Functions
- **Pattern:** Biome warns about dependency arrays
- **Wrong:** Adding inline function to deps: `[() => doThing()]`
- **Right:** Wrap in useCallback: `const handler = useCallback(() => doThing(), [deps])`
- **Why:** Inline functions create new reference each render → infinite loops

### Unused Import Removal Order
- **Pattern:** Multiple unused imports in one file
- **Wrong:** Remove imports one by one (triggers multiple saves)
- **Right:** Remove all unused imports in single edit
- **Why:** Each save triggers format check; batch is efficient

## Anti-Patterns

| Don't | Do Instead | Reason |
|-------|------------|--------|
| `// biome-ignore` without comment | Add explanation after rule | Future maintainers need context |
| Fix lint by changing logic | Fix the lint issue directly | Lint fix shouldn't change behavior |
| Add type assertion `as any` | Fix the actual type | Hides type errors |

## Sticky Fixes

- **`noExplicitAny` with third-party types:** Import proper types from library's type package
- **`useConst` with reassignment needed:** Use `let` only when value actually changes
- **Accessibility warnings:** Add `aria-label` or use semantic HTML element

---

*Update when discovering lint-specific issues that would trip up future fixes.*
