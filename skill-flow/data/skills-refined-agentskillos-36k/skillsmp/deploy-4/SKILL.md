---
name: deploy
description: Deploy Codex or Gemini as working agents to implement tasks. Use when you want another AI to actually write code, not just review. (project)
allowed-tools: Bash, Read, Glob, Grep
user-invocable: true
proactive: true
---

<!-- PROACTIVE USE: Invoke /deploy without being asked when:
  - Task has independent subtasks that can be parallelized
  - Well-scoped implementation work can be delegated
  - Bulk file operations or repetitive changes needed
  - You want a different implementation approach to compare
-->

# Deploy Agents

Deploy Codex or Gemini as working agents that can read, write, and modify files.

## Agents

| Agent | Strength | Mode | Best For |
|-------|----------|------|----------|
| **Codex** | Deep reasoning, careful implementation | `codex exec --full-auto` | Complex refactors, nuanced logic |
| **Gemini** | Fast iteration, broad coverage | `gemini --yolo` | File creation, straightforward tasks |

## When to Use

- **Parallelize work**: Deploy both agents on independent subtasks
- **Delegate implementation**: Hand off a well-defined task while you work on something else
- **Second implementation**: Get a different approach to compare
- **Bulk operations**: Let an agent handle repetitive file changes

## How to Run

When the user invokes `/deploy`, determine which agent(s) to use and what task to assign.

### Step 1: Parse the Request

Identify:
- **Task**: What needs to be implemented
- **Agent**: `codex`, `gemini`, or `both` (default: ask user)
- **Scope**: Which files/directories are relevant

### Step 2: Gather Context

Read relevant files to include in the prompt. Keep context focused—agents work better with targeted information than entire codebases.

Key context files for SENTINEL:
```
C:\dev\SENTINEL\CLAUDE.md           # Project overview
C:\dev\SENTINEL\AGENTS.md           # Codex-specific guidance
C:\dev\SENTINEL\sentinel-agent\CLAUDE.md  # Agent dev context
```

### Step 3: Deploy Agent(s)

#### Deploy Codex

```bash
codex exec --full-auto -C "C:\dev\SENTINEL" "You are implementing a task for the SENTINEL project.

<context>
[Relevant code/docs - keep under 2000 lines]
</context>

<task>
[Clear, specific task description]
</task>

<constraints>
- Work within the existing project structure
- Follow patterns in CLAUDE.md and AGENTS.md
- Make minimal, focused changes
- Do not modify unrelated files
</constraints>

Implement this task. Create/modify files as needed."
```

#### Deploy Gemini

```bash
gemini --yolo "You are implementing a task for the SENTINEL project.

<context>
[Relevant code/docs - keep under 2000 lines]
</context>

<task>
[Clear, specific task description]
</task>

<constraints>
- Work within the existing project structure
- Follow patterns in CLAUDE.md
- Make minimal, focused changes
- Do not modify unrelated files
</constraints>

Implement this task. Create/modify files as needed."
```

#### Deploy Both (Parallel Tasks)

When tasks are independent, deploy both agents simultaneously on different subtasks:

```bash
# Terminal 1: Codex on subtask A
codex exec --full-auto -C "C:\dev\SENTINEL" "[Subtask A prompt]"

# Terminal 2: Gemini on subtask B
gemini --yolo "[Subtask B prompt]"
```

### Step 4: Review Results

After agent(s) complete:
1. Check `git status` for changes made
2. Review the modified files
3. Run tests if applicable: `cd sentinel-agent && pytest`
4. Report what was done and any issues

## Command Variations

### Codex Options

| Flag | Effect |
|------|--------|
| `--full-auto` | Sandbox + auto-approve (recommended) |
| `-s workspace-write` | Allow file writes in workspace |
| `-s read-only` | Read-only exploration |
| `-m o3` | Use o3 model for harder tasks |

### Gemini Options

| Flag | Effect |
|------|--------|
| `--yolo` | Auto-approve all actions |
| `--approval-mode auto_edit` | Auto-approve edits only |
| `-s` | Run in sandbox |
| `-m gemini-2.5-pro` | Specify model |

## Example Usage

### Single Agent

User: `/deploy codex` Add a /history command to the CLI that shows recent session events

Then:
1. Read `sentinel-agent/src/interface/cli.py` and `commands.py`
2. Deploy Codex with focused context
3. Review changes, run tests

### Parallel Deployment

User: `/deploy both` Create unit tests for the state manager AND add docstrings to schema.py

Then:
1. Assign Codex: unit tests for state manager
2. Assign Gemini: docstrings for schema.py
3. Deploy both simultaneously
4. Merge results, resolve any conflicts

### Quick Task

User: `/deploy gemini` Rename all instances of `get_faction` to `fetch_faction`

Then:
1. Search for `get_faction` occurrences
2. Deploy Gemini with file list
3. Verify renames are complete

## Safety Notes

- Both agents run with file write access—review changes before committing
- Use `git diff` to inspect all modifications
- Agents may interpret tasks differently than expected—be specific
- For destructive operations, consider `--sandbox read-only` first to see the plan

## Differences from /council

| `/council` | `/deploy` |
|------------|-----------|
| Gets opinions | Does work |
| Read-only | Read-write |
| Both agents always | Choose agent(s) |
| Synthesis focus | Execution focus |
