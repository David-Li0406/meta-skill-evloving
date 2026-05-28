---
name: init-memory
description: Use this skill to initialize project memory for a new project, creating necessary JSON files to track context, sessions, and decisions.
---

# Initialize Project Memory

Set up the memory structure for a new project by creating essential JSON files.

---

## The Job

1. Determine project name and details.
2. Create memory directory structure.
3. Initialize `context.json` with project information.
4. Create empty `sessions.json` and `decisions.json`.

---

## Steps

### 1. Gather Project Info

Determine the project name from the git remote, folder name, or ask the user. Optionally, infer additional details such as tech stack and description.

```bash
# Try git remote first
git remote get-url origin 2>/dev/null | sed 's/.*\/\([^\/]*\)\.git/\1/'

# Fall back to current directory name
basename $(pwd)
```

Or ask the user: "What should I call this project?"

### 2. Create Directory Structure

```bash
mkdir -p ~/aiconfig/memory/projects/{project-name}
```

### 3. Initialize context.json

Use atomic writes to ensure file integrity. The content should include project details, tech stack, and architecture.

```json
{
  "project": "{project-name}",
  "created": "{ISO-date}",
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
    "key_modules": [],
    "data_flow": ""
  },
  "current_focus": "",
  "active_branches": [],
  "known_issues": [],
  "team_conventions": {
    "commit_format": "conventional",
    "branch_naming": "type/description",
    "pr_template": true
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

Look for existing architectural decisions in common documentation directories. If found, offer to import them.

---

## Output

```
Initialized memory for project: {project-name}
Location: ~/aiconfig/memory/projects/{project-name}/

Created:
  - context.json (project overview and tech stack)
  - sessions.json (session history - empty)
  - decisions.json (architectural decisions - empty)

Next steps:
1. Review context.json and add any missing details.
2. Use /log-session at the end of coding sessions.
3. Memory will be available in future sessions.
```

---

## Checklist

- [ ] Project name determined
- [ ] Directory created
- [ ] context.json initialized
- [ ] sessions.json initialized
- [ ] decisions.json initialized
- [ ] User informed of location
- [ ] Checked for existing ADRs to import