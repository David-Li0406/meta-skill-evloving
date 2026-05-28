---
name: setup-ralph
description: Use this skill to set up the Ralph autonomous AI coding loop in your project, enabling feature development while you sleep.
---

# Objective
Set up the Ralph autonomous coding loop in any project. Ralph runs AI agents in a loop, picking tasks from a PRD, implementing one at a time, committing after each, and accumulating learnings until all tasks are complete.

**This skill ONLY sets up Ralph - you run the commands yourself.**

# Quick Start
**Setup Ralph interactively (recommended):**
```bash
/setup-ralph -i
```

**Setup for specific feature:**
```bash
/setup-ralph -f <feature-name>
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

# Critical Rule
🛑 NEVER run ralph.sh or any execution commands automatically.  
🛑 NEVER execute the loop - only set up files and show instructions.  
✅ ALWAYS let the user copy and run commands themselves.  
✅ ALWAYS end by showing the exact command to run.

# When to Use
**Use this skill when:**
- Starting a new feature that can be broken into small stories.
- Setting up Ralph in a new project.
- Creating a new feature PRD interactively.

**Don't use for:**
- Simple single-file changes.
- Exploratory work without clear requirements.
- Major refactors without acceptance criteria.

# Parameters
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

# State Variables
| Variable | Type | Description |
|----------|------|-------------|
| `{project_path}` | string | Absolute path to target project. |
| `{ralph_dir}` | string | Path to .claude/ralph in project. |
| `{feature_name}` | string | Feature folder name (e.g., `01-add-auth`). |
| `{feature_dir}` | string | Path to task folder. |
| `{interactive_mode}` | boolean | Whether to brainstorm PRD interactively. |
| `{prd_content}` | string | PRD markdown content. |
| `{user_stories}` | array | User stories extracted from PRD. |
| `{branch_name}` | string | Git branch for the feature. |

# Entry Point
Load `steps/step-00-init.md`.

# Step Files
| Step | File | Purpose |
|------|------|---------|
| 00 | `step-00-init.md` | Parse flags, run setup script, create structure. |
| 01 | `step-01-interactive-prd.md` | Interactive PRD brainstorming and creation. |
| 02 | `step-02-create-stories.md` | Transform PRD into user stories (prd.json). |
| 03 | `step-03-finish.md` | Show run command (user runs it themselves). |

# Scripts
| Script | Purpose |
|--------|---------|
| `scripts/setup.sh` | Creates all Ralph files in the project. |

# Execution Rules
1. **Progressive Loading**: Load one step at a time.
2. **Script Execution**: Use scripts/setup.sh to create files atomically.
3. **Interactive Mode**: If -i flag, run brainstorming conversation.
4. **State Persistence**: Track progress in feature_dir/progress.txt.
5. **Resume Support**: Detect existing PRD.md and resume from there.
6. **NEVER RUN RALPH**: Only setup and show commands - user runs them.

# Success Criteria
✅ Ralph structure created at {project_path}/.claude/ralph.  
✅ Feature folder created with PRD.md, prd.json, progress.txt.  
✅ User stories properly formatted in prd.json.  
✅ Clear run command provided to user (they run it themselves).