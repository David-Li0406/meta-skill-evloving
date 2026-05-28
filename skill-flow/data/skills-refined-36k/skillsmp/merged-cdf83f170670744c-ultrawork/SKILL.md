---
name: ultrawork
description: Activate maximum performance mode with parallel agent orchestration for high-throughput task completion.
---

# Ultrawork Skill

Activates maximum performance mode with parallel agent orchestration.

## When Activated

This skill enhances capabilities by:

1. **Parallel Execution**: Running multiple agents simultaneously for independent tasks.
2. **Aggressive Delegation**: Routing tasks to specialist agents immediately.
3. **Background Operations**: Using `run_in_background: true` for long operations.
4. **Persistence Enforcement**: Never stopping until all tasks are verified complete.
5. **Smart Model Routing**: Using tiered agents to save tokens.

## Smart Model Routing (CRITICAL - SAVE TOKENS)

**Choose tier based on task complexity: LOW (haiku) → MEDIUM (sonnet) → HIGH (opus)**

### Available Agents by Tier

| Domain | LOW (Haiku) | MEDIUM (Sonnet) | HIGH (Opus) |
|--------|-------------|-----------------|-------------|
| **Analysis** | `architect-low` / `oracle-low` | `architect-medium` / `oracle-medium` | `architect` / `oracle` |
| **Execution** | `executor-low` / `olympian-low` | `executor` / `olympian` | `executor-high` / `olympian-high` |
| **Search** | `explore` | `explore-medium` | - |
| **Research** | `researcher-low` / `librarian-low` | `researcher` / `librarian` | - |
| **Frontend** | `designer-low` / `frontend-engineer-low` | `designer` / `frontend-engineer` | `designer-high` / `frontend-engineer-high` |
| **Docs** | `writer` / `document-writer` | - | - |
| **Visual** | - | `vision` / `multimodal-looker` | - |
| **Planning** | - | - | `planner`, `prometheus`, `momus`, `metis` |
| **Testing** | - | `qa-tester` | - |

### Tier Selection Guide

| Task Complexity | Tier | Examples |
|-----------------|------|----------|
| Simple lookups | LOW | "What does this function return?", "Find where X is defined" |
| Standard work | MEDIUM | "Add error handling", "Implement this feature" |
| Complex analysis | HIGH | "Debug this race condition", "Refactor auth module across 5 files" |

### Routing Examples

**CRITICAL: Always pass `model` parameter explicitly - Claude Code does NOT auto-apply models from agent definitions!**

```
// Simple question → LOW tier (saves tokens!)
Task(subagent_type="oh-my-claudecode:architect-low", prompt="What does this function return?")

// Standard implementation → MEDIUM tier
Task(subagent_type="oh-my-claudecode:executor", prompt="Add error handling to login")

// Complex refactoring → HIGH tier
Task(subagent_type="oh-my-claudecode:executor-high", prompt="Refactor auth module using JWT across 5 files")

// Quick file lookup → LOW tier
Task(subagent_type="oh-my-claudecode:explore", prompt="Find where UserService is defined")

// Thorough search → MEDIUM tier
Task(subagent_type="oh-my-claudecode:explore-medium", prompt="Find all authentication patterns in the codebase")
```

## Background Execution Rules

**Run in Background** (set `run_in_background: true`):
- Package installation: npm install, pip install, cargo build
- Build processes: npm run build, make, tsc
- Test suites: npm test, pytest, cargo test
- Docker operations: docker build, docker pull

**Run Blocking** (foreground):
- Quick status checks: git status, ls, pwd
- File reads, edits
- Simple commands

## Verification Checklist

Before stopping, verify:
- [ ] TODO LIST: Zero pending/in_progress tasks
- [ ] FUNCTIONALITY: All requested features work
- [ ] TESTS: All tests pass (if applicable)
- [ ] ERRORS: Zero unaddressed errors

**If ANY checkbox is unchecked, CONTINUE WORKING.**