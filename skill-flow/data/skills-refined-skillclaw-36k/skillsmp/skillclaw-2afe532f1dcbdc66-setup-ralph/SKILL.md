---
name: setup-ralph
description: Use this skill when you want to set up the Ralph autonomous AI coding loop in a project to facilitate feature development.
---

# Skill body

## Objective
Set up the Ralph autonomous coding loop in any project. Ralph runs AI agents in a loop, picking tasks from a PRD, implementing one at a time, committing after each, and accumulating learnings until all tasks are complete.

**This skill ONLY sets up Ralph - you run the commands yourself.**

## Quick Start
**Setup Ralph interactively (recommended):**
```bash
/setup-ralph -i
```

**Setup for specific feature:**
```bash
/setup-ralph -f 01-add-authentication
```

**What this does:**
1. Creates `.claude/ralph/` structure in your project.
2. Runs setup script to create all Ralph files.
3. (If -i): Brainstorms PRD with you interactively.
4. Transforms PRD into user stories (prd.json).
5. Shows you the command to run Ralph (you run it yourself).

**After setup, you run:**
```bash
bun run .claude/ralph/ralph.sh -f <feature-name>
```

## Critical Rules
🛑 NEVER run ralph.sh or any execution commands automatically.  
🛑 NEVER execute the loop - only set up files and show instructions.  
✅ ALWAYS let the user copy and run commands themselves.  
✅ ALWAYS end by showing the exact command to run.  

## When to Use
**Use this skill when:**
- Starting a new feature that can be broken into small stories.
- Setting up Ralph in a new project.
- Creating a new feature PRD interactively.

**Don't use for:**
- Simple single-file changes.
- Exploratory work without clear requirements.
- Major refactors without acceptance criteria.

## Parameters
| Flag | Description |
|------|-------------|
| `<project-path>` | Path to the project (defaults to current directory). |
| `-i, --interactive` | Interactive mode: brainstorm PRD with AI assistance. |
| `-f, --feature <name>` | Feature folder name (e.g., `01-add-auth`). |

**Examples:**
```bash
/setup-ralph /path/to/project -i              # Interactive PRD creation
/setup-ralph . -f 01-add-auth                 # Setup for specific feature
/setup-ralph -i -f 02-user-dashboard          # Interactive with specific name
```

## State Variables
| Variable | Type | Description |
|----------|------|-------------|
| `{project_path}` | string | Absolute path to target project. |
| `{ralph_dir}` | string | Path to .claude/ralph in project. |
| `{feature_name}` | string | Feature folder name (e.g., `01-add-auth`). |