---
name: repo-scout
description: Scan repository to find existing patterns, conventions, and related code paths for a feature or change. Use when you need to understand codebase conventions, find similar implementations, or identify reusable code before planning or implementation.
---

# Repo Scout

Fast repository scout to find existing patterns and conventions that should guide implementation.

**Role**: Pattern finder
**Purpose**: Find what already exists in the codebase - NOT to plan or implement
**Output**: Conventions, related code, and reusable components

## Tool Requirements

**Required tools**: Grep, Glob, Read

**Degradation strategy** (if tools unavailable):
```
Manual execution required:

1. Search for patterns:
   grep -r '<pattern>' .

2. Find files by type:
   find . -name '*.ts' | head -20

3. Read project docs:
   cat README.md CONTRIBUTING.md CLAUDE.md
```

## Search Strategy

### 1. Project docs first (fast context)
- CLAUDE.md, README.md, CONTRIBUTING.md, ARCHITECTURE.md
- Any docs/ or documentation/ folders
- package.json/pyproject.toml for deps and scripts

### 2. Find similar implementations
- Grep for related keywords, function names, types
- Look for existing features that solve similar problems
- Note file organization patterns (where do similar things live?)

### 3. Identify conventions
- Naming patterns (camelCase, snake_case, prefixes)
- File structure (co-location, separation by type/feature)
- Import patterns, module boundaries
- Error handling patterns
- Test patterns (location, naming, fixtures)

### 4. Surface reusable code
- Shared utilities, helpers, base classes
- Existing validation, error handling
- Common patterns that should NOT be duplicated

## Output Format

```markdown
## Repo Scout Findings

### Project Conventions
- [Convention]: [where observed]

### Related Code
- `path/to/file.ts:42` - [what it does, why relevant]
- `path/to/other.ts:15-30` - [pattern to follow]

### Reusable Code (DO NOT DUPLICATE)
- `lib/utils/validation.ts` - existing validation helpers
- `lib/errors/` - error classes to extend

### Test Patterns
- Tests live in: [location]
- Naming: [pattern]
- Fixtures: [if any]

### Gotchas
- [Thing to watch out for]
```

## Rules

- Speed over completeness - find the 80% fast
- Always include file:line references
- Flag code that MUST be reused (do not reinvent)
- Note any CLAUDE.md rules that apply
- Skip deep analysis - that is for other agents
- Show signatures, not full implementations
- Keep code snippets to <10 lines illustrating the pattern shape

## Verification

````bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo"
  exit 1
fi

ls "$REPO_ROOT/.factory/skills/repo-scout/SKILL.md"
# Expected: file exists, exit code 0
````
