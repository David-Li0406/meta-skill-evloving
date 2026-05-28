---
name: create-beads-orchestration
description: Use this skill to bootstrap lean multi-agent orchestration with beads task tracking for projects needing agent delegation without heavy MCP overhead.
---

# Create Beads Orchestration

Set up lightweight multi-agent orchestration with git-native task tracking and mandatory code review gates.

## What This Skill Does

This skill bootstraps a complete multi-agent workflow where:

- **Orchestrator** (you) investigates issues, manages tasks, and delegates implementation.
- **Supervisors** (specialized agents) execute fixes in isolated worktrees.
- **Beads CLI** tracks all work with git-native task management.
- **Hooks** enforce workflow discipline automatically.

Each task gets its own worktree at `.worktrees/bd-{BEAD_ID}/`, keeping the main branch clean and enabling parallel work.

## Recommended: Beads Kanban UI

For the best experience, use this orchestration with **[Beads Kanban UI](https://github.com/AvivK5498/Beads-Kanban-UI)** - a visual task management interface that provides:

- Kanban board for beads (tasks, epics, subtasks)
- Dependency visualization
- Worktree management via API
- Branch status tracking
- PR integration

The setup wizard will ask if you're using the Kanban UI to configure the optimal worktree workflow.

---

## Mandatory 4-Step Workflow

You MUST follow ALL 4 steps below in exact order. Missing ANY step is a CATASTROPHIC FAILURE.

| Step | Action | Checkpoint |
|------|--------|------------|
| 1 | Get project info from user | Have project name, directory, AND provider choice |
| 2 | Clone repo and run bootstrap | Bootstrap completes successfully |
| 3 | **STOP** - Instruct user to restart | User confirms they will restart |
| 4 | After restart: Run discovery agent | Supervisors created in .claude/agents/ |

**The setup is NOT complete until Step 4 (discovery) has run.**

---

## Step 0: Detect Setup State (ALWAYS RUN FIRST)

**Before doing anything else, detect if this is a fresh setup or a resume after restart.**

Check for bootstrap artifacts:
```bash
ls .claude/agents/scout.md 2>/dev/null && echo "BOOTSTRAP_COMPLETE" || echo "FRESH_SETUP"
```

**If `BOOTSTRAP_COMPLETE`:**
- Bootstrap already ran in a previous session.
- Skip directly to **Step 4: Run Discovery**.
- Do NOT ask for project info or run bootstrap again.

**If `FRESH_SETUP`:**
- This is a new installation.
- Proceed to **Step 1: Get Project Info**.

---

## Step 1: Get Project Info (Fresh Setup Only)

**YOU MUST GET PROJECT INFO AND ASK THE KANBAN UI QUESTION BEFORE PROCEEDING TO STEP 2.**

1. **Project directory**: Where to install (default: current working directory).
2. **Project name**: For agent templates (will auto-infer from package.json/pyproject.toml if not provided).
3. **Provider delegation**: MANDATORY - You MUST use AskUserQuestion for this choice.

### 1.1 Get Project Directory and Name

Ask the user or auto-detect from package.json/pyproject.toml.

### 1.2 MANDATORY: Ask Provider Delegation Choice

**YOU MUST CALL AskUserQuestion WITH THIS EXACT QUESTION BEFORE RUNNING BOOTSTRAP.**

Do NOT skip this. Do NOT assume a default. Do NOT proceed without the user's explicit choice.

```
AskUserQuestion(
  questions=[{
    "question": "How should read-only agents (scout, detective, architect, scribe, code-reviewer) be executed?",
    "header": "Providers",
    "options": [
      {"label": "Claude only (Recommended)", "description": "All agents run via Claude Task(). Simpler setup, no external dependencies."},
      {"label": "External providers", "description": "Delegate to Codex CLI (with Gemini fallback). Requires configuration."}
    ]
  }]
)
```

---

## Step 2: Clone Repo and Run Bootstrap

Proceed to clone the repository and run the bootstrap process.

---

## Step 3: Instruct User to Restart

After bootstrap, instruct the user to restart Claude Code.

---

## Step 4: Run Discovery Agent

After the user restarts, run the discovery agent to create supervisors in `.claude/agents/`.