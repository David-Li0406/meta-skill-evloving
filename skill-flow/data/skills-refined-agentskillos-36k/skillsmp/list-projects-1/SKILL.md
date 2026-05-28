---
name: list-projects
description: List all projects and their meeting history. Use when the user asks about projects, wants to see what meetings exist, or needs an overview of the workspace.
---

# List Projects

Show all projects and their meeting history.

## Instructions

1. Scan the `projects/` directory for all project folders
2. For each project, gather:
   - Project name
   - Number of transcripts in `transcripts/`
   - Date range of meetings (earliest to latest)
   - Most recent meeting date
   - Number of dashboards in `dashboards/`
   - Number of analyses in `analysis/`

3. Display in a formatted overview

## Output Format

```
📁 project-alpha
   Meetings: 12 (2025-10-01 to 2026-01-12)
   Latest: 2026-01-12
   Dashboards: 10 generated
   
📁 project-beta
   Meetings: 5 (2025-12-01 to 2026-01-10)
   Latest: 2026-01-10
   Dashboards: 5 generated

📁 client-xyz
   Meetings: 3 (2026-01-05 to 2026-01-12)
   Latest: 2026-01-12
   Dashboards: 2 generated
```

## If No Projects Exist

If the `projects/` directory is empty, inform the user:
"No projects yet. Provide a .vtt transcript to create your first project."
