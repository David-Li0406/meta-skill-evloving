---
name: task
description: Use when creating a task file, or when the user says "create task", "new task", "task file", or similar.
---

# Create Task File

Task files document work to be done and provide context for AI implementation.

## Location

```
<repository>/tasks/YYYY/MM/XX/YYYY.MM.DD-short-description.md
```

Where `XX` = developer initials (ask if unknown).

## Process

1. **Clarify scope** - Ask up to 5 questions to understand what's needed
2. **Search codebase** - Find related code, patterns, and ADRs
3. **Create task file** - Use the structure below

## Task File Structure

```markdown
# Task: [Title]

**Date**: YYYY-MM-DD
**Author**: [Initials]
**Status**: Planning | In Progress | Testing | Complete
**PR**: (link when created)

## Goal
One sentence describing the outcome.

## Context
Why this is needed.

## Scope
### In Scope
- [ ] Item 1
- [ ] Item 2

### Out of Scope
- Item not addressed

## Implementation Plan
### 1. [Step Name]
Description.

**Files to modify:**
- `path/to/file.ts` — What changes

## Testing Strategy
- [ ] Unit tests for X
- [ ] Integration tests for Y

## Notes / Decisions Made
(Log changes from original plan during implementation)
```

## Quality Checklist

- [ ] Goal is clear in one sentence
- [ ] Scope explicitly lists in/out items
- [ ] Implementation plan has concrete steps
- [ ] Files to modify are identified
- [ ] Testing strategy is defined
