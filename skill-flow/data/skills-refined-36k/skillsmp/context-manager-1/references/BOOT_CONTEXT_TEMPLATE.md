# BOOT_CONTEXT | <PROJECT_NAME> | <TIMESTAMP>

## Architecture

[Dense overview - 2-4 sentences describing what this project IS, not what it does]

**Type:** [webapp | cli | library | service | monorepo]
**Stack:** [key technologies]
**Entry:** [main entry point file]

## Invariants

Rules that must never be broken:

- [Invariant 1 - e.g., "All API responses use standard envelope format"]
- [Invariant 2 - e.g., "Auth middleware runs before all protected routes"]
- [Invariant 3 - e.g., "State mutations only through designated actions"]

## Key Flows

### [Flow 1 Name - e.g., "Request Handling"]
```
[Input] → [Step 1] → [Step 2] → [Output]
```
Key file: `path/to/file.ts`

### [Flow 2 Name - e.g., "Data Persistence"]
```
[Input] → [Step 1] → [Step 2] → [Output]
```
Key file: `path/to/file.ts`

## File Map

Critical files only - NOT every file:

| Path | Purpose |
|------|---------|
| `src/index.ts` | Entry point |
| `src/api/routes.ts` | Route definitions |
| `src/core/engine.ts` | Core business logic |
| `config/` | Configuration files |

## Conventions

**Naming:**
- Files: `kebab-case.ts`
- Components: `PascalCase`
- Functions: `camelCase`

**Patterns:**
- [Pattern 1 - e.g., "Use dependency injection for services"]
- [Pattern 2 - e.g., "Prefer composition over inheritance"]

**Testing:**
- [Where tests live]
- [How to run tests]

## How to Work Here

**Before making changes:**
1. Check DELTA_CONTEXT for recent changes
2. If working on a feature, load FEATURES/<feature>.md
3. Only read files referenced in these docs

**When adding code:**
- [Guidance specific to this codebase]
- [Common pitfalls to avoid]

**When debugging:**
- [Where to look first]
- [Common issues and solutions]

---
*Compiled: <TIMESTAMP> | Baseline: <COMMIT_HASH>*
