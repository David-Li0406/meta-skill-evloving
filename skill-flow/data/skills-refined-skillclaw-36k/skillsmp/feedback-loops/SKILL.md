---
name: feedback-loops
description: TypeScript, lint, test, and build validation before committing
category: development
depends-on: []
---

# Feedback Loops Skill

> "Validate early, validate often – catch errors before they compound."

## When to Use This Skill

Use **before every commit** to ensure code quality and prevent broken builds.

## Quick Start

```bash
# Run all feedback loops in sequence
npm run type-check && npm run lint && npm run test && npm run build
```

## The Feedback Loop

```
┌─────────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ type-check  │───▶│   lint   │───▶│   test   │───▶│  build   │
│   (tsc)     │    │ (eslint) │    │ (vitest) │    │  (vite)  │
└─────────────┘    └──────────┘    └──────────┘    └──────────┘
       │                │                │               │
       ▼                ▼                ▼               ▼
   Type errors     Code style      Test failures   Bundle issues
```

## Progressive Guide

### Level 1: Type Check

```bash
npm run type-check
# or
npx tsc --noEmit
```

**Common Issues:**

- Missing type annotations
- Incompatible types
- Missing imports
- Property doesn't exist

**Solutions:**

```typescript
// ❌ Implicit any
function process(data) { ... }

// ✅ Explicit type
function process(data: PlayerData) { ... }

// ❌ Missing null check
const name = player.name.toUpperCase();

// ✅ Safe access
const name = player?.name?.toUpperCase() ?? 'Unknown';
```

### Level 2: Lint

```bash
npm run lint
# or
npx eslint . --ext .ts,.tsx
```

**Common Issues:**

- Unused variables
- Missing dependencies in useEffect
- Inconsistent formatting
- Import order

**Auto-fix:**

```bash
npm run lint -- --fix
```

### Level 3: Test

```bash
npm run test
# or
npx vitest run
```

**If tests fail:**

1. Read the failure message carefully
2. Check which test failed
3. Review recent changes that could affect it
4. Fix the code (not the test, unless test is wrong)

### Level 4: Build

```bash
npm run build
# or
npx vite build
```

**Common Issues:**

- Import errors not caught by tsc
- Missing environment variables
- Bundle size issues
- Asset loading problems

## Decision Framework

| Step       | Time | What It Catches               |
| ---------- | ---- | ----------------------------- |
| type-check | ~5s  | Type errors, missing imports  |
| lint       | ~3s  | Style issues, potential bugs  |
| test       | ~10s | Logic errors, regressions     |
| build      | ~30s | Bundle issues, runtime errors |

## When to Skip Steps

| Situation         | What to Run                                 |
| ----------------- | ------------------------------------------- |
| Small type change | type-check only (then full before commit)   |
| Styling only      | lint only (then full before commit)         |
| Quick iteration   | type-check + lint (then full before commit) |
| **Before commit** | **Always run ALL four**                     |

## Anti-Patterns

❌ **DON'T:**

- Commit without running feedback loops
- Use `@ts-ignore` or `// eslint-disable` to hide errors
- Skip tests because "it's a small change"
- Use `any` type without justification
- Comment out failing tests

✅ **DO:**

- Run all loops before every commit
- Fix errors properly, don't suppress
- Update tests when behavior changes
- Add types to all public interfaces
- Run `--fix` for auto-fixable issues

## Error Resolution Patterns

### TypeScript Error

```typescript
// Error: Object is possibly 'undefined'
const value = obj.prop; // ❌

// Solution 1: Optional chaining
const value = obj?.prop;

// Solution 2: Nullish coalescing
const value = obj.prop ?? defaultValue;

// Solution 3: Non-null assertion (if you're sure)
const value = obj!.prop; // Use sparingly
```

### ESLint Error

```typescript
// Error: React Hook useEffect has missing dependencies
useEffect(() => {
  doSomething(value);
}, []); // ❌

// Solution: Add dependency
useEffect(() => {
  doSomething(value);
}, [value]); // ✅
```

### Test Failure

```typescript
// If test is correct and code is wrong:
// → Fix the code

// If test is outdated:
// → Update test to match new behavior
// → Add comment explaining the change
```

## Commit Protocol

Only commit when ALL pass:

```bash
# Run all checks
npm run type-check && npm run lint && npm run test && npm run build

# If all pass, commit with Ralph format
git add .
git commit -m "[ralph] [{AGENT}] {TASK-ID}: description"
# Examples:
# [ralph] [developer] feat-001: vehicle physics
# [ralph] [techartist] vis-001: PBR materials
```

## Checklist

Before committing:

- [ ] `npm run type-check` passes with 0 errors
- [ ] `npm run lint` passes with 0 warnings
- [ ] `npm run test` passes (all tests green)
- [ ] `npm run build` succeeds
- [ ] No `@ts-ignore` or `any` without justification
- [ ] Commit message follows Ralph format

## Reference

- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [ESLint Rules](https://eslint.org/docs/rules/)
- [Vitest Documentation](https://vitest.dev/)
