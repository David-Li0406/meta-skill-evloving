---
name: init-memory
description: Use this skill to initialize the memory structure for a new project, creating essential JSON files to track context, sessions, and decisions.
---

# Initialize Project Memory

Set up memory structure for a new project.

## The Job

1. Determine project name and details.
2. Create memory directory structure.
3. Initialize context.json with project info.
4. Create empty sessions.json and decisions.json.

## Steps

### 1. Gather Project Info

Ask the user or infer from the codebase:

```
Setting up project memory. Please confirm:

1. Project name: {inferred from git remote or directory}
2. Tech stack: {inferred from dependencies}
3. Brief description: {from README or ask}
```

### 2. Create Directory Structure

```bash
mkdir -p ~/aiconfig/memory/projects/{project-name}
```

### 3. Initialize context.json

Use atomic writes to ensure file integrity:

```bash
# Atomic write with JSON validation
~/aiconfig/scripts/atomic-write.sh ~/aiconfig/memory/projects/{project-name}/context.json
```

Content:

```json
{
  "project": "{project-name}",
  "created": "{ISO date}",
  "description": "{brief description}",
  "repository": "{git remote URL if available}",
  "tech_stack": {
    "languages": [],
    "frameworks": [],
    "databases": [],
    "infrastructure": []
  },
  "architecture": {
    "pattern": "",
    "key_directories": {}
  },
  "current_focus": "",
  "active_branches": [],
  "known_issues": [],
  "team_conventions": {
    "commit_format": "",
    "branch_naming": "",
    "pr_template": false
  }
}
```

### 4. Initialize sessions.json

```json
{
  "project": "{project-name}",
  "sessions": []
}
```

### 5. Initialize decisions.json

```json
{
  "project": "{project-name}",
  "decisions": []
}
```

### 6. Scan for Existing Decisions

Look for existing architectural decisions in:

- `docs/adr/` or `docs/decisions/`
- `ARCHITECTURE.md`
- `README.md` technical sections

If found, offer to import them:

```
Found existing ADRs in docs/adr/. Import to memory?
```

## Output

```
Initialized memory for project: {project-name}
Location: ~/aiconfig/memory/projects/{project-name}/

Created:
  - context.json (project context)
  - sessions.json (session history)
  - decisions.json (architectural decisions)

Use /log-session at end of sessions to record progress.
Use /recall to search past context.
```

## Checklist

- [ ] Project name determined
- [ ] Directory created
- [ ] context.json initialized
- [ ] sessions.json initialized
- [ ] decisions.json initialized
- [ ] User informed of location