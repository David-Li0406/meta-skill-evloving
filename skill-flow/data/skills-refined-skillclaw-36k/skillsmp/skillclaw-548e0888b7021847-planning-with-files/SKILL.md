---
name: planning-with-files
description: Use this skill when starting complex multi-step tasks, research projects, or any task requiring more than five tool calls, leveraging persistent markdown files for effective planning and documentation.
---

# Planning with Files

Work like Manus: Use persistent markdown files as your "working memory on disk."

## Important: Where Files Go

When using this skill:

- **Templates** are stored in the skill directory at `${CLAUDE_PLUGIN_ROOT}/templates/`
- **Your planning files** (`task_plan.md`, `findings.md`, `progress.md`) should be created in **your project directory** — the folder where you're working.

| Location | What Goes There |
|----------|-----------------|
| Skill directory (`${CLAUDE_PLUGIN_ROOT}/`) | Templates, scripts, reference docs |
| Your project directory | `task_plan.md`, `findings.md`, `progress.md` |

This ensures your planning files live alongside your code, not buried in the skill installation folder.

## Quick Start

Before ANY complex task:

1. **Create `task_plan.md`** in your project — Use [templates/task_plan.md](templates/task_plan.md) as reference.
2. **Create `findings.md`** in your project — Use [templates/findings.md](templates/findings.md) as reference.
3. **Create `progress.md`** in your project — Use [templates/progress.md](templates/progress.md) as reference.
4. **Re-read plan before decisions** — Refreshes goals in attention window.
5. **Update after each phase** — Mark complete, log errors.

## Core Principles

- **Context Window = RAM (volatile, limited)**
- **Filesystem = Disk (persistent, unlimited)**

→ Anything important gets written to disk.

## File Purposes

| File | Purpose | When to Update |
|------|---------|----------------|
| `task_plan.md` | Phases, progress, decisions | After each phase |
| `findings.md` | Research, discoveries | After ANY discovery |
| `progress.md` | Session log, test results | Throughout session |

## Critical Rules

1. **Create Plan First**: Never start a complex task without `task_plan.md`. Non-negotiable.
2. **The 2-Action Rule**: After every 2 view/browser/search operations, IMMEDIATELY save key findings to text files.
3. **Read Before Decide**: Before major decisions, read the plan file to keep goals in your attention window.
4. **Update After Act**: After completing any phase, mark phase status and log any errors encountered.
5. **Log ALL Errors**: Every error goes in the plan file to build knowledge and prevent repetition.
6. **Never Repeat Failures**: Track what you tried and mutate the approach if an action fails.

## Session Recovery

Before starting work, check for unsynced context from a previous session:

```bash
# Linux/macOS
$(command -v python3 || command -v python) ${CLAUDE_PLUGIN_ROOT}/scripts/session-catchup.py "$(pwd)"
```

```powershell
# Windows PowerShell
python "$env:USERPROFILE\.codex\skills\planning-with-files\scripts\session-catchup.py" (Get-Location)
```

If catchup report shows unsynced context:
1. Run `git diff --stat` to see actual code changes.
2. Read current planning files.
3. Update planning files based on catchup + git diff.
4. Then proceed with the task.