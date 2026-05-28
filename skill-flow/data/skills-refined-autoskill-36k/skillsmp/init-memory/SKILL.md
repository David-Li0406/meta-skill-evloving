---
name: init-memory
description: "Initialize project memory for the current project. Creates context.json, sessions.json, and decisions.json. Triggers on: init memory, setup memory, initialize project memory, start tracking this project."
---

# Initialize Project Memory

Set up memory structure for a new project.

---

## The Job

1. Determine project name (from git remote, folder name, or ask user)
2. Create memory directory at `~/aiconfig/memory/projects/{project-name}/`
3. Initialize three JSON files with project context

---

## Steps

### 1. Get Project Name

```bash
# Try git remote first
git remote get-url origin 2>/dev/null | sed 's/.*\/\([^\/]*\)\.git/\1/'

# Fall back to current directory name
basename $(pwd)
```

Or ask the user: "What should I call this project?"

### 2. Create Directory

```bash
mkdir -p ~/aiconfig/memory/projects/{project-name}
```

### 3. Create context.json

```json
{
  "project": "{project-name}",
  "created": "{ISO-date}",
  "tech_stack": [],
  "architecture": {
    "pattern": "",
    "key_modules": [],
    "data_flow": ""
  },
  "current_focus": "",
  "known_issues": []
}
```

Ask user to fill in tech_stack and architecture if they want.

### 4. Create sessions.json

```json
{
  "sessions": []
}
```

### 5. Create decisions.json

```json
{
  "decisions": []
}
```

---

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

---

## Checklist

- [ ] Project name determined
- [ ] Directory created
- [ ] context.json initialized
- [ ] sessions.json initialized
- [ ] decisions.json initialized
- [ ] User informed of location
