---
name: using-gambit
description: Use at session start - establishes mandatory workflows for finding and using skills
---

# Using Gambit

## Overview

Gambit provides structured development workflows using native Claude Code Tasks. This skill loads at session start and ensures you check for relevant skills before any task.

**Core principle:** If a skill exists for your task, using it is mandatory, not optional.

**Announce at start:** "I'm using gambit to guide this session."

## When to Use

This skill applies at the start of EVERY conversation and BEFORE every task:

- User asks to implement a feature
- User asks to fix a bug
- User asks to refactor code
- User asks to debug an issue
- User asks to write tests
- User describes a problem to solve

## The Process

### Before Responding to ANY User Message

1. List available gambit skills mentally
2. Ask: "Does ANY skill match this request?"
3. If yes → Load and follow that skill
4. Announce which skill you're using
5. Follow the skill exactly as written

### Mandatory Workflows

**Before writing code:**
- Use `gambit:brainstorm` to refine requirements
- Use `gambit:write-plan` to create Tasks with dependencies

**During implementation:**
- Use `gambit:execute-plan` to work through Tasks one at a time
- Use `gambit:tdd` for RED-GREEN-REFACTOR cycle

**Before claiming done:**
- Use `gambit:verify` to show evidence, not claims

### Task Integration

Gambit uses native Claude Code Tasks (not external tools like beads/bd):

- `TaskCreate` — Create tasks with dependencies
- `TaskUpdate` — Mark in_progress/completed, add blockers
- `TaskList` — Find next ready task
- `TaskGet` — Read full task details

**Tasks are the source of truth.** Don't track work mentally.

## Available Skills

### Phase 1: Core Planning
| Skill | Slash Command | Purpose |
|-------|---------------|---------|
| using-gambit | `/gambit` | Session entry point (this skill) |
| writing-plans | `/gambit:write-plan` | Create Tasks with dependencies |
| executing-plans | `/gambit:execute-plan` | One-task-at-a-time execution |

### Phase 2: Quality Assurance
| Skill | Slash Command | Purpose |
|-------|---------------|---------|
| test-driven-development | `/gambit:tdd` | RED-GREEN-REFACTOR cycle |
| verification | `/gambit:verify` | Evidence before completion |
| testing-quality | `/gambit:test-quality` | Audit test effectiveness |

### Phase 3: Workflow
| Skill | Slash Command | Purpose |
|-------|---------------|---------|
| brainstorming | `/gambit:brainstorm` | Socratic design refinement |
| using-worktrees | `/gambit:worktree` | Git worktrees with devenv support |
| finishing-branch | `/gambit:finish` | Merge/PR/discard workflow |

### Planned (Coming Soon)
| Skill | Slash Command | Purpose |
|-------|---------------|---------|
| debugging | `/gambit:debug` | Systematic root cause analysis |
| refactoring | `/gambit:refactor` | Safe incremental transforms |
| code-review | `/gambit:review` | Request and receive reviews |
| parallel-agents | `/gambit:parallel` | Concurrent investigations |
| task-refinement | `/gambit:refine` | SRE-style corner case analysis |

## Anti-patterns

**Don't:**
- Skip checking for skills ("This is simple, I'll just do it")
- Track work mentally instead of in Tasks
- Claim completion without verification
- Write code before tests
- Batch multiple tasks without checkpoints

**Do:**
- Check for skills before every task
- Create Tasks for multi-step work
- Run verification commands and show output
- Write failing test first, then code
- Stop after each task for human review

## Red Flags

If you catch yourself thinking:
- "This doesn't need a skill" → Check anyway
- "I remember what to do" → Load the skill, don't rely on memory
- "This is almost done" → Run verification first
- "Let me just fix this quickly" → Create a Task, follow the process

## Integration

**This skill is loaded by:** Session start hook

**This skill calls:** All other gambit skills as needed

**Critical workflows this establishes:**
- `gambit:brainstorm` before writing code
- `gambit:tdd` during implementation
- `gambit:verify` before claiming done
