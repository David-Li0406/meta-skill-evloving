---
name: intent-migrate
description: Migrate existing local intents from .sejas folder to the global intents folder. Use when transitioning from local to global intent storage.
user-invocable: true
---

# Intent Migrate

You are helping the user migrate existing intents from the local `.sejas/` folder to the global intents folder.

## Workflow

1. Get the current repository info:
   - Repository name: `basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $(pwd)`
   - Git root: `git rev-parse --show-toplevel 2>/dev/null || pwd`

2. Check if `.sejas/` folder exists at the git root:
   - If not found, inform user: "No local .sejas/ folder found. Nothing to migrate."

3. Target intents folder is `~/.claude-intents/`

4. List intents to migrate from both `.sejas/open/` (or `.sejas/in-progress/`) and `.sejas/done/`:
   - Show the user what will be migrated
   - Display old path → new path for each intent

5. For each intent folder, transform the name:
   - **Old format:** `YYYY-MM-DD-description`
   - **New format:** `YYYY-MM-DD-{repository-name}-{description}`
   - Example: `2026-01-15-add-feature` → `2026-01-15-my-repo-add-feature`

6. Ask user for confirmation before proceeding

7. Perform the migration:
   - Create `~/.claude-intents/in-progress/` and `~/.claude-intents/done/` if they don't exist
   - Move each intent folder from `.sejas/open/` (or `.sejas/in-progress/`) to `~/.claude-intents/in-progress/` with new name
   - Move each intent folder from `.sejas/done/` to `~/.claude-intents/done/` with new name
   - Use `mv` command to move folders

8. After successful migration:
   - Ask user if they want to delete the old `.sejas/` folder
   - If yes, remove it: `rm -rf {git_root}/.sejas`
   - If no, leave it in place

9. Show migration summary:
   - Number of open intents migrated
   - Number of done intents migrated
   - New location path

## Example Output

```
## Migration Preview

**Source:** /path/to/repo/.sejas/
**Target:** ~/.claude-intents/
**Repository:** my-repo

### Open Intents (3)
- 2026-01-15-add-feature → 2026-01-15-my-repo-add-feature
- 2026-01-18-fix-bug → 2026-01-18-my-repo-fix-bug
- 2026-01-20-update-docs → 2026-01-20-my-repo-update-docs

### Done Intents (1)
- 2026-01-10-initial-setup → 2026-01-10-my-repo-initial-setup

Proceed with migration? (y/n)
```

## Important Notes

- **Intents folder:** All intents are stored in `~/.claude-intents/`
- **Preserve all files:** Move entire folder contents (spec.md, notes.md, pr.md, and any other files)
- **No overwrites:** If a target folder already exists, warn the user and skip that intent
- **Repository name:** Extracted from git or current folder name
- **Backup suggestion:** Recommend user backs up `.sejas/` before migration if they have important data
