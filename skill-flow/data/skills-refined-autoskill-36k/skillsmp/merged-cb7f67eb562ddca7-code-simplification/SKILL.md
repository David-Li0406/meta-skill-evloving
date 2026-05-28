---
name: code-simplification
description: Use this skill to simplify and refine recently modified code for clarity and maintainability while preserving its exact functionality.
---

# Code Simplification

Simplify and refine code to enhance clarity, consistency, and maintainability without altering its behavior. This skill is applicable when you are asked to "simplify", "clean up", or "refactor" code.

## Philosophy

**Simple code is not short code.** Simplicity means:

- Easy to read sequentially without mental backtracking
- Intent is obvious from structure, not comments
- Each function/block does one thing
- Control flow is linear where possible
- No cleverness that requires explanation

Compression that hurts readability is not simplification.

## Scope

Focus on **recently modified code** in the current session. To identify the scope:

1. Check staged changes: `git diff --staged`
2. Fall back to unstaged: `git diff`
3. Use user-provided file paths if specified

Avoid broad refactors unless explicitly requested.

## Process

### 1. Identify Target Code

```bash
git diff --staged --name-only  # or git diff --name-only
```

Read the modified files, focusing only on changed sections and their immediate context.

### 2. Establish Constraints

Before making changes, confirm these preservation requirements:

- **Behavior**: All outputs, side effects, and observable behavior unchanged
- **API surface**: Public functions, exports, and interfaces unchanged
- **Error handling**: All error paths and messages preserved
- **Performance**: No algorithmic complexity regressions

If unsure whether a change preserves behavior, do not make it.

### 3. Apply Simplifications

Work through the code applying transformations in priority order. 

**Priority order** (highest first):

1. **Flatten control flow**: Use guard clauses and early returns to reduce nesting depth.
2. **Remove redundancy**: Eliminate dead code, duplicate logic, and unused variables.
3. **Clarify names**: Rename variables and functions within the modified surface area for better understanding.
4. **Decompose**: Split functions only when it reduces cognitive load.
5. **Normalize patterns**: Align with existing conventions.

### 4. Avoid Anti-Patterns

Do **not** introduce:

- Nested ternaries (use if/else or early returns)
- Dense one-liners that hide control flow
- Abstractions that exist only to reduce line count
- Clever solutions that require explanation
- Changes outside the touched surface area

### 5. Validate

1. Run the narrowest available test/check for the modified area.
2. Review the diff to confirm only intended changes.
3. Verify no new dependencies or imports added unnecessarily.

### 6. Report

After completing simplification, provide a summary of changes made and why they simplify the code.

```markdown
## Simplification Summary

**Scope**: {files or areas modified}

### Changes Made

- {Change 1}: {what was done and why it's simpler}
- {Change 2}: {what was done and why it's simpler}
- ...

### Why Simpler

- {Reduced nesting from N to M levels}
- {Eliminated N lines of duplicate logic}
- {Clearer control flow via guard clauses}

### Preserved

- {Confirm behavior unchanged}
- {Confirm API unchanged}
- {Note any intentional complexity retained and why}

### Verification

- {Tests/checks run, or "none available"}
- {Diff reviewed: yes/no}
```

## Guidelines

- **Preserve first**: When in doubt, don't change it.
- **Small changes**: Multiple small improvements > one large rewrite.
- **Explain tradeoffs**: If you leave complexity in place, note why.
- **Local conventions**: Follow patterns already in the codebase.
- **No feature creep**: Simplification is not the time to add functionality.