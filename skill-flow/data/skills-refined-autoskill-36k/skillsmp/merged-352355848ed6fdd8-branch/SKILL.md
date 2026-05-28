---
name: branch
description: Use this skill when creating branches, starting new work, or switching to feature branches with proper naming conventions.
---

# Branch Naming

Use `type/short-description` format.

## Types

- `feat`: User-facing features or behavior changes (must change production code)
- `fix`: Bug fixes (must change production code)
- `docs`: Documentation only
- `style`: Code style/formatting (no logic changes)
- `refactor`: Code restructuring without behavior change
- `test`: Adding or updating tests
- `chore`: CI/CD, tooling, dependency bumps, configs (no production code)

## Examples

```text
feat/search-pagination
fix/year-search-bug
chore/pre-commit-hooks
docs/update-readme
refactor/simplify-dynamo-queries
test/integration-coverage
feat/infinite-scroll
fix/album-path-validation
refactor/state-management
test/e2e-login-flow
```

## Instructions

1. Determine the type based on what the work will accomplish.
2. Choose a short, descriptive slug (2-4 words, hyphenated).
3. Create the branch: `git checkout -b type/short-description`.