---
name: deslop
description:
  Remove AI-generated code slop from recent changes. Checks the diff against main and removes
  unnecessary comments, defensive code, type hacks, and other patterns inconsistent with
  human-written code.
---

# Remove AI Code Slop

Check the diff against main and remove all AI-generated slop introduced in this branch.

## What to Remove

### Unnecessary Comments

- Comments explaining obvious code that a human wouldn't add
- Comments inconsistent with the rest of the file's style
- Inline comments that just restate what the code does
- Section dividers or decorative comments not used elsewhere in the codebase

### Over-Defensive Code

- Extra try/catch blocks that are abnormal for that area of the codebase
- Defensive null/undefined checks on trusted/validated codepaths
- Redundant validation that's already handled upstream
- Error handling that swallows errors silently

### Type Hacks

- Casts to `any` to work around type issues
- Type assertions (`as Type`) that hide real problems
- `@ts-ignore` or `@ts-expect-error` comments
- Overly permissive types (`any`, `unknown`, `object`) where specific types exist

### Style Inconsistencies

- Naming conventions that don't match the file
- Different formatting patterns
- Abstractions or patterns not used elsewhere in the codebase
- Over-engineered solutions for simple problems

## Process

1. Get the diff: `git diff main...HEAD`
2. For each changed file, compare the new code against:
   - The rest of that same file
   - Similar files in the codebase
3. Remove patterns that don't match the existing style
4. Keep changes minimal—only remove clear slop

## Output

Report with only a 1-3 sentence summary of what you changed. No lengthy explanations.
