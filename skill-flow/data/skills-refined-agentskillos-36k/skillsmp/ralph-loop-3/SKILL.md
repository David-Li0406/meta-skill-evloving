---
name: ralph-loop
description: Ralph Loop autonomous iteration plugin - enables self-referential development loops with multi-ralph support. Forked from ralph-loop@claude-plugins-official for persistence.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Ralph Loop Plugin (Forked)

This is a forked version of the `ralph-loop@claude-plugins-official` plugin, stored in the skills folder for persistence and version control.

## Why Forked?

The original plugin lives in `~/.claude/plugins/cache/` which:
- Is in a Docker named volume (not git-tracked)
- Can be lost on volume deletion
- Is not backed up to GitHub

This fork ensures multi-ralph changes persist across container rebuilds.

## Features

- **Multi-Ralph**: Run concurrent loops with different `--task-id` values
- **Session Binding**: Each loop binds to the first Claude session that claims it
- **Completion Promises**: Exit loops by outputting `<promise>TEXT</promise>`
- **Progress Tracking**: State files at `.claude/ralph-loop-{task-id}.local.md`
- **Review Mode**: Ask user questions at decision points with `--mode review`
- **Fresh Context**: Clear history between iterations using `/ralph-fresh` or `setup-fresh-loop.sh`

## Usage

Use via the `ralph-invoke` skill or directly:

```bash
/ralph-loop "Your task description" --task-id myloop --max-iterations 50 --completion-promise "DONE"
```

## Review Mode

Use `--mode review` when you want Ralph to ask questions at decision points instead of making autonomous choices.

```bash
/ralph-loop "Build feature X" --mode review --task-id myfeature --max-iterations 20
```

### How It Works

1. Ralph writes a steering question to `.claude/ralph-steering-{task-id}.md` with `status: pending`
2. On next iteration, the stop hook detects the pending question
3. Ralph uses `AskUserQuestion` tool to wait for user response
4. Ralph updates the steering file with `status: answered` and the response
5. Ralph continues with the user's decision

### Steering File Format

```markdown
---
status: pending
---

## Question

What approach should I use for the database layer?

**Options:**
1. PostgreSQL - robust, feature-rich
2. SQLite - simple, portable
3. MongoDB - document-based

## Response

(awaiting user response)
```

## Files

- `scripts/setup-ralph-loop.sh` - Initializes a ralph loop (persistent context)
- `scripts/setup-fresh-loop.sh` - Initializes a ralph loop (fresh context per iteration)
- `hooks/stop-hook.sh` - Stop hook that intercepts exit and re-injects prompt
- `commands/ralph-loop.md` - Slash command definition
- `commands/ralph-fresh.md` - Slash command definition for fresh loops
- `commands/cancel-ralph.md` - Cancel command definition
