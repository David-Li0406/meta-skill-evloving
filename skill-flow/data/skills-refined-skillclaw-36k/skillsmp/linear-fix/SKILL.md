---
name: linear-fix
description: Autonomously completes Linear tickets via git worktrees. Use when user says "fix ENG-123", "complete LIN-456", "work on linear ticket", provides a linear.app URL, or mentions a ticket ID pattern like ABC-1234. Creates git worktree, implements fix via autonomous planning/review loop, opens GitHub PR with full reasoning.
allowed-tools: Read, Bash, Grep, Glob, Task
---

# Linear Fix

Autonomous Linear ticket completion: fetch issue → create worktree → plan → review → implement → PR.

**CRITICAL**: Create git worktree BEFORE implementation. Use ticket ID as worktree folder/branch name.

## Usage

```bash
/linear-fix <ticket-id-or-url>
```

## Workflow

Follow 6 steps (see `./references/workflow.md` for full details):

1. **Gather Context** - Extract ticket ID, fetch comprehensive details via `linear-cli`:
   - **Always use `--output json`** for all Linear CLI commands
   - Fetch issue details: `linear-cli i get <id> --output json` (title, description)
   - Fetch issue comments: `linear-cli cm list <id> --output json`
   - Check for uploaded files/attachments in both issue description AND comments
   - Use `/linear-uploads` skill to download any attachments (images, screenshots, files)
2. **Create Worktree** - Run `./scripts/create-git-worktree.sh`, cd into it, install deps
3. **Plan** - Task tool with `subagent_type=Plan`, read `./references/planner-prompt.md` for template
4. **Review** - Task tool with `subagent_type=feature-dev:code-architect`, read `./references/reviewer-prompt.md` for template
5. **Implement & Review** - Execute approved plan, then `subagent_type=feature-dev:code-reviewer`, read `./references/code-reviewer-prompt.md`
6. **Create PR** - Commit, prepare PR body (fill template if exists), create PR. Read `./references/workflow.md` Step 6 for PR body format

## Autonomous Loops

**Planning Loop (Steps 3-4):**

- Planner proposes 2-3 approaches → Architect reviews → revise if needed
- Max 3 iterations; then select best available with caveats

**Implementation Loop (Step 5):**

- Implement → Code reviewer reviews → fix if needed
- Max 2 iterations; then proceed with caveats

**IMPORTANT**: Only proceed to Step 6 (Create PR) after code review is APPROVED.

**PR Body Requirements** (see workflow.md for details):

1. Extract variables from Step 4 "Extract from approved review" section
2. **Always append** the "🤖 Autonomous Planning Reasoning" collapsible section from Step 6b — use the EXACT template format
