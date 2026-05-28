---
name: project-plan
description: Creates project plan documents for tracking implementation work. Use when the user asks to create a project plan, implementation plan, or wants to document a new feature or refactoring task.
---

# Project Plan

Create structured project plan documents for tracking implementation work.

## Instructions

1. Ask the user for:
   - **Project name**: Short descriptive title
   - **Summary**: One paragraph describing what needs to be done and why
   - **Location**: Where to save the file (default: `docs/projects/` with kebab-case filename)

2. Explore the codebase to understand:
   - Current state relevant to the project
   - Files that will need changes
   - Existing patterns to follow

3. Get the author name from `git config user.name`

4. Create a markdown file following the template structure below

## Template

```markdown
# {Project Name}

- **Status**: Planning
- **Author**: {author from git config}
- **Created**: {YYYY-MM-DD}

## Summary

{One paragraph summary of what needs to be done and why}

## Background

{Context explaining the motivation and any relevant history}

### Current State

{Description of how things work today, with specific file paths and line numbers}

### Existing Pattern

{If applicable, show code examples of patterns to follow}

## Implementation Tasks

### Phase 1: {Phase Name}

- [ ] **Task 1.1**: {Specific task description}
- [ ] **Task 1.2**: {Specific task description}

### Phase 2: {Phase Name}

- [ ] **Task 2.1**: {Specific task description}

### Phase N: Verification

- [ ] **Task N.1**: Run tests to verify no regressions

## File Changes

| File | Change |
|------|--------|
| `path/to/file` | {Brief description of changes} |

## Notes

- {Any caveats, edge cases, or decisions to document}
```

## Guidelines

- Use specific file paths and line numbers when referencing code
- Break work into logical phases (usually by component or layer)
- Each task should be small enough to complete in one session
- Include a verification phase with test commands
- Add code templates if there's a repetitive pattern to follow
- Keep the File Changes table focused on files with significant modifications
