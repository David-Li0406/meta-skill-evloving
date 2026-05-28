---
name: remove-ai-code-slop
description: Use this skill to clean up AI-generated code by removing unnecessary comments, defensive checks, type hacks, and style inconsistencies from the current branch.
---

# Remove AI Code Slop

Your task is to review the diff against the main branch and remove all AI-generated "slop" introduced in this branch.

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
- `@ts-ignore`, `# type: ignore`, or similar suppression comments
- Overly permissive types where specific types exist

### Style Inconsistencies
- Naming conventions that differ from the rest of the file
- Formatting or structure that doesn't match surrounding code
- Abstractions or patterns not used elsewhere in the codebase
- Over-engineered solutions for simple problems

## Process

1. Get the diff against main: 
   ```
   git diff main...HEAD
   ```

2. For each modified file, read the full file to understand its existing style and patterns.

3. Identify and remove the specified types of slop while preserving legitimate changes.

4. Report with only a 1-3 sentence summary of what you changed. Be specific but concise.