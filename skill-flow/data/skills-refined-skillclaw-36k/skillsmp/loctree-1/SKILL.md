---
name: loctree
description: Codex skill for semantic codebase navigation with loct CLI (find, slice, impact, health, for-ai).
---

# Loctree - Codebase Intelligence Skill (Codex)

Loctree provides AST-aware codebase understanding. Unlike text search (grep/rg), loct understands symbols, imports, exports, dependencies, and dead code.

## When to use
Trigger when the user asks for:
- “find where this is defined/used”
- “what breaks if I change this file”
- “show minimal context for this file”
- “health/dead code/cycles/duplicates”
- onboarding to a new repo

## First-shot flow
1) `loct --for-ai` (overview + priorities)
2) `loct find <symbol>` (definitions + semantic matches)
3) `loct slice <file>` (minimal context)
4) `loct impact <file>` (blast radius)
5) `loct health` (dead code, cycles, duplicates)

## Explicit commands
### `loct find <symbol|pattern>`
Search for symbol definitions across the codebase.

```
loct find "MyComponent"
loct find "SymbolA|SymbolB"
```

### `loct impact <file>`
Analyze what would break if you change a file.

```
loct impact src/utils/helpers.ts
```

### `loct slice <file>`
Get the minimal dependency slice for a file.

```
loct slice src/components/Button.tsx
```

### `loct health`
Codebase health report: dead code, cycles, duplicates, health score.

```
loct health
```

### `loct focus <dir>`
Analyze a specific directory's structure.

```
loct focus src/api/
```

### `loct --for-ai`
Comprehensive overview optimized for agents.

```
loct --for-ai
```

## Best practices
- Start with `loct --for-ai` when entering a new repo.
- Prefer `loct find` over raw rg/grep for symbol discovery.
- Use `loct impact` before refactors.
- Use `loct slice` for quick context when editing.

## Prerequisites
Install loctree CLI:

```
cargo install loctree
# or
brew install loctree
```

Initialize in your project (creates `.loctree/` cache):

```
loct scan
```
