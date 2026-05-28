---
name: chezmoi-sync
description: Sync modified and new files to chezmoi repository and push to GitHub. Use when Claude Code has modified or created files in a chezmoi-managed directory and needs to re-add them to chezmoi, commit changes, and push to the remote repository. Triggers on requests to sync, commit, or push chezmoi changes after file modifications.
---

# Chezmoi Sync Workflow

After modifying or creating files in a chezmoi-managed directory, sync changes to the chezmoi source repository and push to GitHub.

## Quick Start (Recommended)

Use the bundled script (works from any chezmoi-managed directory):

```bash
# Re-add all modified files, commit, and push
~/.claude/skills/chezmoi-sync/scripts/chezmoi-sync-auto.sh "Update config description"

# Also add specific new files
~/.claude/skills/chezmoi-sync/scripts/chezmoi-sync-auto.sh "Add new config" --add-new newfile.lua other.conf
```

**Note:** When adding new files with private permissions (600/700), the script will display a warning and ask for confirmation before proceeding. This prevents accidentally committing files with incorrect permissions.

## Manual Workflow

1. **Re-add modified files** - `chezmoi re-add .`
2. **Add new files** - `chezmoi add <file>` (auto-detects permissions)
3. **Commit and push** - `cd "$(chezmoi source-path)" && git add -A && git commit -m "msg" && git push`

## Commands Reference

### Re-add modified files

```bash
chezmoi re-add <file>
```

Re-adds a single file that chezmoi already tracks. Run from the managed directory (e.g., `~/.config/nvim/`).

### Add new files

Check permissions before adding:

```bash
# Check if file is executable
if [[ -x "$file" ]]; then
    chezmoi add "$file"  # chezmoi auto-detects executable and adds with executable_ prefix
else
    chezmoi add "$file"
fi
```

Chezmoi automatically handles:
- Executable files → `executable_` prefix in source
- Dot files → `dot_` prefix in source
- Private files (600/700) → `private_` prefix in source

For templates (files containing machine-specific values), use:
```bash
chezmoi add --template <file>
```

### Batch operations

To re-add all modified files in current directory:
```bash
chezmoi re-add .
```

### Commit and push

```bash
cd "$(chezmoi source-path)"
git add -A
git commit -m "<descriptive message>"
git push
```

## Example: Full sync after modifications

```bash
# From the managed directory (e.g., ~/.config/nvim/)
chezmoi re-add .

# For any new files created
chezmoi add ./newfile.lua

# Commit and push
cd "$(chezmoi source-path)"
git add -A
git commit -m "Update nvim config: <brief description>"
git push
```

## Notes

- `chezmoi re-add` only works for files already tracked by chezmoi
- Use `chezmoi add` for files not yet in the source state
- `chezmoi managed` lists all files chezmoi tracks in current directory
- `chezmoi status` shows differences between source and destination
- `chezmoi diff` shows detailed diff of pending changes

## Private File Warnings

When adding **new** files (not re-adding existing ones), the script checks for private permissions (600/700). If detected:

1. The script displays a warning with the file path and current permissions
2. Prompts for confirmation before adding
3. Skips the file if not confirmed

This safeguard exists because incorrect file permissions can cause issues when syncing dotfiles across machines. If a file unexpectedly has private permissions, verify it's intentional before adding to chezmoi.

To bypass the check for files you know should be private, confirm when prompted or manually run:
```bash
chezmoi add <file>
```
