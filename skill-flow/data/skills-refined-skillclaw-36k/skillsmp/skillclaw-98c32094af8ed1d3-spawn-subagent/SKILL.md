---
name: spawn-subagent
description: Use this skill to launch a Claude Code subagent in an isolated git worktree for executing specific tasks independently while the parent agent continues its work.
---

# Skill body

## Purpose

Launch a Claude Code subagent in an isolated git worktree to execute a specific task. The subagent operates independently with its own context window while the parent agent continues coordinating.

## Critical: Unsupervised Execution

**Subagents run without user supervision.** Claude Code does not provide a way for users to view subagent output while it runs. Users cannot:

- See what the subagent is doing
- Correct mistakes in real-time
- Answer questions or clarify requirements
- Provide feedback during execution

**All decision-making MUST happen in the main agent before spawning.** The subagent prompt must be comprehensive enough that execution is purely mechanical - following explicit instructions without judgment calls.

## Hook Inheritance

**Subagents inherit project hooks automatically** when running in the same project directory. However, subagents may not follow hook guidance if not explicitly reminded.

**MANDATORY: Include key requirements in subagent prompt:**

```
CRITICAL REQUIREMENTS (enforced by hooks):
- Always decompose code instead of adding PMD suppression annotations
- Always use git merge --ff-only for linear history
- Always use git-filter-repo instead of git filter-branch
- Preserve .git/refs/original unless user explicitly requests deletion
- Include tests for bugfixes in the SAME commit as the fix

COMMIT SEPARATION:
- .claude/rules/ updates → separate config: commit (not bundled with bugfix/feature)
- STATE.md updates → same commit as implementation
```

**Why explicit in prompt:** Hooks can block commands, but subagents may try alternatives. Stating prohibitions in the prompt prevents wasted effort on blocked approaches.

## When to Use

- Task has a well-defined PLAN.md ready for execution
- **All ambiguities resolved** - main agent has made all decisions
- Task is independent enough to execute in isolation
- Parent agent needs to continue with other work
- Context window management requires task isolation

## Subagent Types and Two-Stage Planning

**Planning Subagent (two stages for token efficiency):**

| Stage | Purpose | Output | Tokens |
|-------|---------|--------|--------|
| Stage 1 | High-level approach outlines | 3 brief options + agent_id | ~5K |
| Stage 2 | Detailed implementation | ... | ... |