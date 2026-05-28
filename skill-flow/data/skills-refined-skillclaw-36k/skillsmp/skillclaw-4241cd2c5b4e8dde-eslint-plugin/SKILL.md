---
name: eslint-plugin
description: Use this skill when you need to author custom ESLint plugins and rules with test-driven development, supporting both flat and legacy config formats.
---

# Skill body

## Overview

This skill covers the creation, testing, and packaging of custom ESLint rules and plugins using test-driven development (TDD). It includes guidance on rule types, edge case discovery, and project setup detection.

## Important Guidelines

1. Write tests **before** implementing rules (TDD).
2. **Ask** about edge cases before writing any code.
3. Fixes must be **idempotent** (running twice = running once).

## When to Use

- Enforcing project-specific coding standards.
- Creating rules with auto-fix or suggestions.
- Building TypeScript-aware rules using type information.
- Migrating from deprecated rules.

## Workflow

Copy and track the following progress:

```
ESLint Rule Progress:
- [ ] Clarify transformation (before/after examples)
- [ ] Ask edge case questions (see below)
- [ ] Detect project setup (config format, test runner)
- [ ] Write failing tests first
- [ ] Implement rule to pass tests
- [ ] Add edge case tests
- [ ] Document the rule
```

## Edge Case Discovery

**CRITICAL: Ask these BEFORE writing code.**

### Always Ask

1. Should the rule apply to all file types or specific extensions?
2. Should it be auto-fixable, provide suggestions, or just report?
3. Are any patterns exempt (test files, generated code)?

### By Rule Type

| Type | Key Questions |
|------|---------------|
| **Identifiers** | Variables, functions, classes, or all? Destructured? Renamed imports? |
| **Imports** | Re-exports? Dynamic imports? Type-only? Side-effect imports? |
| **Functions** | Arrow vs declaration? Methods vs standalone? Async? Generators? |
| **JSX** | JSX and createElement? Fragments? Self-closing? Spread props? |
| **TypeScript** | Require type info? Handle `any`? Generics? Type assertions? |

## Project Setup Detection

### Config Format

| Files Present | Format |
|---------------|--------|
| `eslint.config.js/mjs/cjs/ts` | Flat config (ESLint 9+) |
| `.eslintrc.*` or `eslintConfig` in package.json | Legacy |

### Test Runner

Check `package.json` devDependencies:
- **Bun**: `bun:test` or `bun`
- **Vitest**: `vitest`
- **Jest**: `jest`

## Rule Template

```typescript
// src/rules/rule-name.ts
import { ESLintUtils } from "@typescript-eslint/utils";

const createRule = ESLintUtils.RuleCreator(name => {
    // Rule implementation here
});
```