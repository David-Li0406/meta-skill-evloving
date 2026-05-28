---
name: remove-ai-code-slop
description: Use this skill when you need to clean up AI-generated code in your branch by removing unnecessary elements and ensuring consistency with human-written code.
---

# Remove AI Code Slop

Check the diff against the main branch and remove all AI-generated slop introduced in this branch.

## What to Remove

### Unnecessary Comments
- Comments explaining obvious code that a human wouldn't add
- Comments inconsistent with the rest of the file's commenting style
- Redundant JSDoc/docstrings when the function signature is self-explanatory
- Inline comments that just restate what the code does

### Over-Defensive Code
- Extra try/catch blocks that are abnormal for that area of the codebase
- Defensive null/undefined checks on trusted/validated codepaths
- Redundant validation that's already handled upstream
- Error handling that swallows errors silently

### Type Hacks
- Casts to `any`, `unknown`, or language-equivalent dynamic types to bypass type errors
- Type assertions that shouldn't be necessary
- Suppression comments like `@ts-ignore` or `# type: ignore`

### Style Inconsistencies
- Naming conventions that differ from the rest of the file
- Formatting or structure that doesn't match surrounding code
- Over-abstraction or unnecessary indirection

## Process

1. Get the diff against main: `git diff main...HEAD`
2. For each modified file, read the full file to understand its existing style and patterns.
3. Identify and remove the above types of slop while preserving legitimate changes.
4. Make surgical edits to ensure minimal disruption to functionality.

## Output

After completing all changes, provide ONLY a 1-3 sentence summary of what you changed. Be specific but concise.