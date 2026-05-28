---
name: safe-editing
description: Best practices for making safe, verified code edits
tags: [editing, code, safety, validation]
---

# Safe Code Editing Skill

Use this skill when making code changes that need verification.

## Shadow Workspace Pattern

The Smart Edit plugin uses a "shadow workspace" approach:

1. **Copy**: Create a temporary copy of the file
2. **Edit**: Apply changes to the shadow copy
3. **Validate**: Run linters/type checkers on the shadow
4. **Apply**: Only apply changes if validation passes

## When to Use

- Making structural code changes
- Refactoring existing code
- Editing files with type annotations
- Changes that need syntax validation

## Workflow

1. Identify the file and changes needed
2. Use `smart-edit` tool with:
   - `file_path`: Target file
   - `changes`: Description of changes
3. Tool validates before applying
4. Review the diff and confirm

## Benefits

- **Safety**: Changes validated before applying
- **Rollback**: Original preserved until confirmed
- **Validation**: Catch errors before they happen
