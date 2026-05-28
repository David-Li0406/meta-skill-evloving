---
name: ralph
description: "Run iterative task execution using Claude in a loop to complete PRD tasks. Use when: (1) Executing multi-step PRDs autonomously, (2) Running Claude in a loop until tasks complete, (3) Automating incremental task completion with progress tracking, (4) User says 'run ralph' or 'ralph loop'."
---

# Ralph Loop

Iterative task execution that runs Claude in a loop to complete PRD tasks autonomously.

## Usage

```bash
~/.claude/skills/ralph/ralph <iterations> <prd_file> [progress_file]
```

**Arguments:**
- `iterations` - Maximum loop iterations
- `prd_file` - Path to PRD markdown file
- `progress_file` - Path to progress file (default: progress.txt in PRD directory)

## Examples

```bash
~/.claude/skills/ralph/ralph 10 scripts/prd.md
~/.claude/skills/ralph/ralph 10 scripts/prd.md scripts/progress.txt
```

## Each Iteration

1. Find highest-priority task and implement it
2. Run tests and type checks
3. Update PRD with what was done
4. Append progress to progress file
5. Commit changes

**Exit conditions:**
- PRD outputs `<promise>COMPLETE</promise>`
- Max iterations reached

## PRD Format

```markdown
# PRD: Feature Name

## Goal
Brief description of objective.

## Tasks
- [ ] Task 1
- [ ] Task 2

## Success Criteria
1. Criterion 1
2. Criterion 2
```
