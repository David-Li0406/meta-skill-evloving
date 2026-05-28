---
name: implementation-plan
description: This skill should be used when working with IMPLEMENTATION_PLAN.md files, parsing markdown checklists, reading verification commands from AGENTS.md, or tracking task completion status. Essential for agents like Ralph that follow structured implementation plans.
version: 0.1.0
---

# Implementation Plan Skill

This skill provides knowledge for working with structured implementation plans that use markdown checklist format and verification-based task completion.

## Purpose

Implementation plans organize work into trackable tasks with verification gates. This skill covers:

- Parsing markdown checklist format (`- [ ]` for incomplete, `- [x]` for complete)
- Reading verification commands from AGENTS.md
- Updating task completion status
- Handling continuous execution workflows

## Implementation Plan Format

IMPLEMENTATION_PLAN.md uses standard markdown checklist syntax:

```markdown
# Implementation Plan

## Description
Brief description of the plan objectives.

## Prerequisites
- [ ] Dependency or setup step
- [ ] Another prerequisite

## Tasks
- [ ] Task 1: First task description
- [ ] Task 2: Second task description
- [x] Task 3: Already completed task

## Verification
Commands that verify implementation (also in AGENTS.md):
- `pytest tests/`
- `npm run test`

## Notes
Additional context or reminders.
```

## Parsing Task Lists

To find the next unchecked task:

1. Read IMPLEMENTATION_PLAN.md using the Read tool
2. Search for lines starting with `- [ ]` (unchecked tasks)
3. The first unchecked task is the next task to complete
4. Lines starting with `- [x]` are already complete

**Grep pattern for unchecked tasks:**
```bash
grep '^\- \[ \]' IMPLEMENTATION_PLAN.md
```

**Grep pattern for completed tasks:**
```bash
grep '^\- \[x\]' IMPLEMENTATION_PLAN.md
```

## Marking Tasks Complete

When a task is verified, update the checklist:

**Before:**
```markdown
- [ ] Task 1: Implement feature
```

**After:**
```markdown
- [x] Task 1: Implement feature
```

Use the Edit tool to make this change, replacing `- [ ]` with `- [x]` for the specific task line.

## Verification Commands

AGENTS.md contains verification commands used to validate work:

```markdown
# Verification Commands

## General
- `pytest tests/` - Run all tests
- `npm test` - Run test suite

## Language-Specific
- Python: `python -m pytest`
- JavaScript: `npm run test`
- Go: `go test ./...`
```

### Reading Verification Commands

1. Read AGENTS.md to find the verification section
2. Extract commands from the list
3. Run ALL commands using Bash tool
4. Only mark task complete when ALL commands pass

### Handling Multiple Commands

When multiple verification commands exist:
- Run each command sequentially
- ALL must pass (exit code 0) before proceeding
- If any fail, fix the issue and re-run ALL commands

## Continuous Execution Pattern

For persistent agents like Ralph:

1. Find first unchecked task
2. Implement the task
3. Run verification commands
4. If verification passes: mark task complete, continue to next
5. If verification fails: fix code, re-run verification
6. Repeat until all tasks are complete
7. Report final status

## Task Completion Status

Check completion status by counting:

```bash
# Count incomplete tasks
grep -c '^\- \[ \]' IMPLEMENTATION_PLAN.md

# Count completed tasks
grep -c '^\- \[x\]' IMPLEMENTATION_PLAN.md
```

When incomplete count is zero, all tasks are complete.

## Additional Resources

### Reference Files

For detailed patterns and examples, consult:
- **`references/task-examples.md`** - Common task patterns by language
- **`references/verification-patterns.md`** - Verification command patterns

### Example Files

Working examples in `examples/`:
- **`IMPLEMENTATION_PLAN.md.template`** - Standard template
- **`AGENTS.md.example`** - Verification command examples

### Scripts

Utilities in `scripts/`:
- **`parse-tasks.sh`** - Parse and display task status

## Edge Cases

### Empty Task List

If no `- [ ]` or `- [x]` patterns found:
- Inform user the plan has no tasks
- Suggest adding tasks or using `/ralph-agent:ralph-init` to create a template

### Malformed Checklist

If checklist formatting is inconsistent:
- Attempt to parse common variations (`- [ ]`, `-[]`, `* [ ]`)
- Report parsing issues to user
- Suggest standardizing format

### Missing AGENTS.md

If AGENTS.md doesn't exist:
- Inform user verification file is missing
- Ask for verification command to use
- Create AGENTS.md with provided command for future use

### No Verification Commands

If AGENTS.md exists but has no verification section:
- Ask user what command to run for verification
- Add command to AGENTS.md for future tasks
- Proceed with provided verification

## Best Practices

- Keep task descriptions clear and specific
- Each task should be independently verifiable
- Break large tasks into smaller, checkable chunks
- Update verification commands when project changes
- Use consistent markdown checklist format
- Always verify before marking complete
