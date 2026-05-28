---
name: init-memory
description: "Initialize project memory for the current project. Creates context.json, sessions.json, and decisions.json. Triggers on: init memory, setup memory, initialize project memory, start tracking this project."
---

# Memory Initializer

Set up project memory structure for a new project.

---

## The Job

1. Determine project name and details
2. Create memory directory structure
3. Initialize context.json with project info
4. Create empty sessions.json and decisions.json

---

## Step 1: Gather Project Info

Ask the user or infer from codebase:

```
Setting up project memory. Please confirm:

1. Project name: {inferred from package.json or directory}
2. Tech stack: {inferred from dependencies}
3. Brief description: {from README or ask}
```

Use AskUserQuestion if needed to clarify.

---

## Step 2: Create Directory Structure

```bash
mkdir -p ~/aiconfig/memory/projects/{project-name}
```

---

## Step 3: Initialize context.json

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
    "languages": ["TypeScript"],
    "frameworks": ["Next.js", "React"],
    "databases": ["PostgreSQL"],
    "infrastructure": ["Vercel"]
  },
  "architecture": {
    "pattern": "{monolith|microservices|serverless}",
    "key_directories": {
      "src/components": "React components",
      "src/lib": "Shared utilities",
      "src/app": "Next.js app router"
    }
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

---

## Step 4: Initialize sessions.json

```json
{
  "project": "{project-name}",
  "sessions": []
}
```

---

## Step 5: Initialize decisions.json

```json
{
  "project": "{project-name}",
  "decisions": []
}
```

---

## Step 6: Scan for Existing Decisions

Look for existing architectural decisions in:

- `docs/adr/` or `docs/decisions/`
- `ARCHITECTURE.md`
- `README.md` technical sections

If found, offer to import them:

```
Found existing ADRs in docs/adr/. Import to memory?
```

---

## Output

```
Project memory initialized: ~/aiconfig/memory/projects/{project-name}/

Created:
  - context.json (project overview and tech stack)
  - sessions.json (session history - empty)
  - decisions.json (architectural decisions - empty)

Next steps:
1. Review context.json and add any missing details
2. Use /log-session at end of coding sessions
3. Memory will be available in future sessions
```

---

## Checklist

- [ ] Confirmed project name with user
- [ ] Created memory directory
- [ ] Populated context.json with tech stack
- [ ] Created empty sessions.json
- [ ] Created empty decisions.json
- [ ] Checked for existing ADRs to import
