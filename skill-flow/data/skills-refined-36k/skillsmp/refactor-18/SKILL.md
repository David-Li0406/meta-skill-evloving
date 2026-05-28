---
name: refactor
description: Find dead code, duplications, complexity issues, and refactoring opportunities. Use when cleaning up code, removing unused exports, simplifying complex functions, or during tech debt sprints.
---

# Refactor & Dead Code Removal

Analyze and refactor code for clarity, maintainability, and removal of unused code.

## Scope

### 1. Dead Code Detection
- Unused exports (functions, types, constants)
- Unused imports
- Unreachable code paths
- Commented-out code blocks
- Unused CSS classes
- Deprecated code marked for removal
- Unused dependencies in package.json

### 2. Code Duplication
- Repeated logic across files (DRY violations)
- Similar components that should be abstracted
- Copy-pasted utility functions
- Duplicated type definitions

### 3. Complexity Reduction
- Functions exceeding 50 lines
- Deeply nested conditionals (>3 levels)
- Complex boolean expressions
- God components doing too much
- Files approaching 300 lines (per AGENTS.md)

### 4. Naming & Clarity
- Unclear variable/function names
- Misleading names that don't match behavior
- Inconsistent naming conventions
- Magic numbers without constants

### 5. Pattern Consistency
- Inconsistent error handling patterns
- Mixed async patterns (callbacks vs promises vs async/await)
- Inconsistent state management approaches
- Varying component structure patterns

### 6. Type Safety
- `any` types that should be specific
- Missing type annotations
- Overly broad types that could be narrowed
- Type assertions that could be avoided

## Output Format

For each finding:
```
[TYPE: DEAD_CODE|DUPLICATION|COMPLEXITY|NAMING|PATTERN|TYPES]
File: path/to/file.ts:lineNumber
Issue: Brief description
Current: Code snippet or pattern
Recommended: Refactored approach
Risk: LOW|MEDIUM|HIGH (breaking change potential)
```

## Actions

1. Run `npm run lint` to catch obvious issues
2. Run `npm run type-check` for type issues
3. Search for unused exports with grep patterns
4. Identify files over 300 lines
5. Look for duplicated code blocks

## Refactoring Principles

Per AGENTS.md guidelines:
- Single Responsibility Principle
- Reuse > Rebuild
- Abstract only when pattern appears 3+ times
- Keep PRs scoped to single purpose

## Post-Review

Generate:
- Safe deletions (no breaking changes)
- Refactoring candidates with dependency analysis
- Suggested extraction of shared utilities
- Migration path for larger refactors
