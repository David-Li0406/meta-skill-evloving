---
name: refactor-code
description: "[lint] [naming] [simplify] [types] [all] - Refactors code in the current branch. Fixes linting, enforces naming conventions, simplifies verbose code, and strengthens TypeScript types."
---

# Refactoring Code

Refactors code changes in the current branch to improve quality and consistency.

## Subcommands

| Command | Description |
|---------|-------------|
| `/refactoring-code lint` | Run project linters/formatters and fix auto-fixable issues |
| `/refactoring-code naming` | Rename identifiers to match project naming conventions |
| `/refactoring-code simplify` | Simplify verbose or nested code while preserving behavior |
| `/refactoring-code types` | Replace loose types (`any`, `unknown`) with proper types |
| `/refactoring-code all` | Run all refactoring checks in sequence |

## Workflow

1. **Get changed files**
   ```bash
   git diff main...HEAD --name-only
   ```

2. **For each file, analyze the diff**
   ```bash
   git diff main...HEAD -- <file>
   ```

3. **Apply refactoring based on subcommand** (see detailed guides below)

4. **Verify changes**
   ```bash
   npx tsc --noEmit  # TypeScript check
   npm test          # Run tests
   ```

5. **Summarize** what was refactored in 1-3 sentences

## Refactoring Guides

- **Linting and formatting**: See [lint.md](lint.md)
- **Naming conventions**: See [naming.md](naming.md)
- **Code simplification**: See [simplify.md](simplify.md)
- **Type strengthening**: See [types.md](types.md)

## Guidelines

- **Only refactor new code**: Check git blame; don't modify code that predates the branch
- **Preserve behavior exactly**: Refactoring should not change functionality
- **Match project style**: Follow existing patterns in the codebase
- **Don't over-refactor**: Keep changes focused on the specific issue
