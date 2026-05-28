---
name: create-beads-orchestration
description: Bootstrap lean multi-agent orchestration with beads task tracking. Use for projects needing agent delegation without heavy MCP overhead.
---

# Create Beads Orchestration

Set up lightweight multi-agent orchestration with git-native task tracking and mandatory code review gates.

## What This Skill Does

This skill bootstraps a complete multi-agent workflow where:

- **Orchestrator** (you) investigates issues, manages tasks, delegates implementation
- **Supervisors** (specialized agents) execute fixes in isolated worktrees
- **Beads CLI** tracks all work with git-native task management
- **Hooks** enforce workflow discipline automatically

Each task gets its own worktree at `.worktrees/bd-{BEAD_ID}/`, keeping the main branch clean and enabling parallel work.

## CRITICAL: Mandatory 4-Step Workflow

You MUST follow ALL 4 steps below in exact order. Missing ANY step is a CATASTROPHIC FAILURE.

| Step | Action | Checkpoint |
|------|--------|------------|
| 1 | Get project info from user | Have project name, directory, AND provider choice |
| 2 | Clone repo and run bootstrap | Bootstrap completes successfully |
| 3 | **STOP** - Instruct user to restart Claude Code | User confirms they will restart |
| 4 | After restart: Run discovery agent | Supervisors created in .claude/agents/ |

**DO NOT:**
- Skip asking for project info
- Skip asking about provider delegation (Claude-only vs External providers)
- Continue after bootstrap without telling user to restart
- Forget to run discovery after restart
- Consider setup complete until discovery has run

## Step 1: Get Project Info

**YOU MUST ASK ALL THREE QUESTIONS BEFORE PROCEEDING TO STEP 2 using AskUserQuestion.**

1. **Project directory**: Where to install (default: current working directory)
2. **Project name**: For agent templates (will auto-infer from package.json/pyproject.toml if not provided)
3. **Provider delegation**: MANDATORY - You MUST use AskUserQuestion for this choice

<mandatory-question>
```
AskUserQuestion(
  questions=[{
    "question": "How should read-only agents (scout, detective, architect, scribe, code-reviewer) be executed?",
    "header": "Providers",
    "options": [
      {"label": "Claude only (Recommended)", "description": "All agents run via Claude Task(). Simpler setup, no external dependencies."},
      {"label": "External providers", "description": "Delegate to Codex CLI (with Gemini fallback). Requires codex login and optional gemini CLI."}
    ],
    "multiSelect": false
  }]
)
```
</mandatory-question>

## Step 2: Clone and Run Bootstrap

```bash
git clone --depth=1 https://github.com/AvivK5498/Claude-Code-Beads-Orchestration "${TMPDIR:-/tmp}/beads-orchestration-setup"
```

```bash
# If user selected "Claude only":
python3 "${TMPDIR:-/tmp}/beads-orchestration-setup/bootstrap.py" \
  --project-name "{{PROJECT_NAME}}" \
  --project-dir "{{PROJECT_DIR}}" \
  --claude-only

# If user selected "External providers":
python3 "${TMPDIR:-/tmp}/beads-orchestration-setup/bootstrap.py" \
  --project-name "{{PROJECT_NAME}}" \
  --project-dir "{{PROJECT_DIR}}"
```

The bootstrap script will:
1. Install beads CLI (via brew, npm, or go)
2. Initialize `.beads/` directory
3. Copy agent templates to `.claude/agents/`
4. Copy hooks to `.claude/hooks/`
5. Configure `.claude/settings.json`
6. Set up `.mcp.json` for provider_delegator
7. Create `CLAUDE.md` with orchestrator instructions
8. Update `.gitignore`

**Verify bootstrap completed successfully before proceeding.**

## Step 3: STOP - User Must Restart

**YOU MUST STOP HERE AND INSTRUCT THE USER TO RESTART CLAUDE CODE.**

Tell the user:

> **Setup phase complete. You MUST restart Claude Code now.**
>
> The new hooks and MCP configuration will only load after restart.
>
> After restarting:
> 1. Open this same project directory
> 2. Tell me "Continue orchestration setup" or run `/create-beads-orchestration` again
> 3. I will run the discovery agent to complete setup
> 4. **Do not skip this restart - the orchestration will not work without it.**

## Step 4: Run Discovery (After Restart)

If the user returns after restart and says "continue setup" or similar:

1. Verify bootstrap completed (check for `.claude/agents/scout.md`)
2. Run the discovery agent:

```python
Task(
    subagent_type="discovery",
    prompt="Detect tech stack and create supervisors for this project"
)
```

Discovery will:
- Scan package.json, requirements.txt, Dockerfile, etc.
- Fetch specialist agents from external directory
- Inject beads workflow into each supervisor
- Write supervisors to `.claude/agents/`

3. After discovery completes, tell the user:

> **Orchestration setup complete!**
>
> Created supervisors: [list what discovery created]
>
> You can now use the orchestration workflow:
> - Create tasks with `bd create "Task name" -d "Description"`
> - The orchestrator will delegate to appropriate supervisors
> - All work requires code review before completion

## Cleanup (Optional)

```bash
rm -rf "${TMPDIR:-/tmp}/beads-orchestration-setup"
```

## What This Creates

- **Beads CLI** for git-native task tracking (one bead = one branch = one task)
- **Core agents**: scout, detective, architect, scribe, code-reviewer
- **Discovery agent**: Auto-detects tech stack and creates specialized supervisors
- **Hooks**: Enforce orchestrator discipline, code review gates, concise responses
- **Branch-per-task workflow**: Parallel development with automated merge conflict handling

**With `--claude-only` (default):**
- All agents run via Claude Task() - no external dependencies

**With external providers:**
- MCP Provider Delegator enables Codex→Gemini→Claude fallback chain
- Additional enforcement hooks for provider delegation

## Requirements

**Claude only mode (default):**
- **beads CLI**: Installed automatically (or manually via brew/npm/go)
- **uv**: Python package manager (only if using external providers)

**External providers mode:**
- **Codex CLI**: `codex login` for authentication (primary provider)
- **Gemini CLI**: Optional fallback when Codex hits rate limits
- **uv**: Python package manager for MCP server

## More Information

See the full documentation: https://github.com/AvivK5498/Claude-Code-Beads-Orchestration