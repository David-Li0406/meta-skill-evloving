---
name: loctree
description: Claude-specific loctree skill with PostToolUse hook augmentation for rg/grep results and explicit loct commands.
---

# Loctree - Codebase Intelligence Skill (Claude)

Loctree provides AST-aware codebase understanding. Unlike text search (grep/ripgrep), loctree understands code structure: symbol definitions, exports, imports, dependencies, and dead code.

## When This Skill Activates

This skill is **automatically active** through the PostToolUse hook. When you use Grep or Bash with rg/grep, loctree automatically augments results with semantic context.

You can also **explicitly invoke** loctree for deeper analysis.

## Automatic Augmentation (Zero Friction)

When you search for code patterns, the hook automatically:

1. **Detects symbol-like patterns** (PascalCase, camelCase, snake_case)
2. **Transforms regex to multi-query** (`A.*B` → `A|B`)
3. **Runs `loct find`** to get semantic matches
4. **Adds context**: definitions, usages, cross-match files, dead code status

**Example**: You grep for `ApiClient.*request` → Hook transforms to `request|ApiClient` → Returns symbol definitions + semantic matches + cross-match files showing where both terms appear together.

## Explicit Commands

### `loct find <symbol|pattern>`

Search for symbol definitions across the codebase.

```bash
loct find "MyComponent"           # Single symbol
loct find "SymbolA|SymbolB"       # Multi-query (OR)
loct find "canonical_model|vision" # Find related symbols
```

**Output includes:**
- Symbol matches (definitions)
- Semantic matches (similar names)
- Parameter matches (function args)
- Dead code status

### `loct impact <file>`

Analyze what would break if you change a file.

```bash
loct impact src/utils/helpers.ts
```

**Use before refactoring** to understand ripple effects.

### `loct slice <file>`

Get the minimal dependency slice for a file.

```bash
loct slice src/components/Button.tsx
```

Shows only the files needed to understand this file.

### `loct health`

Codebase health report: dead code, cycles, duplicates.

```bash
loct health
```

**Output includes:**
- Dead exports (unused code)
- Circular dependencies
- Duplicate exports (twins)
- Health score (0-100)

### `loct focus <directory>`

Analyze a specific directory's structure.

```bash
loct focus src/api/
```

### `loct query who-imports <file>`

Find all files that import a given file.

```bash
loct query who-imports src/hooks/useAuth.ts
```

### `loct --for-ai`

Get a comprehensive codebase overview optimized for AI understanding.

```bash
loct --for-ai
```

**Run this first** when starting work on a new codebase.

## Best Practices

1. **Start with `loct --for-ai`** to understand codebase structure
2. **Use `loct find` instead of grep** for symbol searches (10x better results)
3. **Check `loct impact` before refactoring** to avoid breaking changes
4. **Run `loct health` periodically** to catch dead code and cycles

## Pattern Recognition

The hook automatically recognizes these patterns:

| Pattern Type | Example | Action |
|-------------|---------|--------|
| PascalCase | `MyComponent` | `loct find` |
| camelCase | `handleClick` | `loct find` |
| snake_case | `user_service` | `loct find` or Tauri command |
| File path | `src/utils.ts` | `loct slice` |
| Directory | `src/api/` | `loct focus` |
| Multi-term | `A\|B` or `A.*B` | `loct find "A\|B"` |
| Health keywords | `dead`, `unused`, `cycle` | `loct health` |

## Cross-Match Files

When searching multiple terms, loctree identifies files containing 2+ different terms - these are often the most relevant files for understanding relationships.

## Prerequisites

Install loctree CLI:

```bash
cargo install loctree
# or
brew install loctree
```

Verify installation:

```bash
loct --version
```

Initialize in your project (creates `.loctree/` cache):

```bash
loct scan
```

---

**Made with (งಠ_ಠ)ง by the ⌜ Loctree ⌟ 𝖙𝖊𝖆𝖒 (c) 2026
Maciej & Monika + Klaudiusz (AI)**
