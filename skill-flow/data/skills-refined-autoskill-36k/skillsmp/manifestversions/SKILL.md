---
name: manifest:versions
description: Show the version roadmap with release planning context. Use when the user asks about versions, releases, or milestones.
disable-model-invocation: true
---

Display version roadmap for the current project.

## Steps

1. Get the project for the current working directory:
   - Call `list_projects` with `directory_path` set to the current working directory
   - If no project found, tell the user to run `init_project` first

2. List versions:
   - Call `list_versions` with the project ID

3. Format the output as a table showing:
   - Version name
   - Status: "released", "now" (current focus), "next" (queued), or "later"
   - Feature count

Example output:
```
Version    Status    Features
─────────────────────────────
v0.1.0     released  5
v0.2.0     now       3
v0.3.0     next      1
v1.0.0     later     0
```
