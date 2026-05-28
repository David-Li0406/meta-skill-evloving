# Adding a New External Repository

Follow these steps to grant Claude Code read access to another local repository.

## Step 1: Add to settings.json

Edit `.claude/settings.json` and add the repository path to `additionalDirectories`:

```json
{
  "permissions": {
    "additionalDirectories": [
      "/Users/cygoerdt/unamentis",
      "/path/to/NEW_REPO_HERE"
    ]
  }
}
```

Use absolute paths (e.g., `/Users/yourname/dev/my-repo`).

## Step 2: Document in SKILL.md

Add a row to the "Available External Repos" table in `SKILL.md`:

```markdown
| new-repo | /path/to/new-repo | What this repo contains |
```

## Step 3: Restart Claude Code

Changes to settings.json require a Claude Code restart to take effect.

## Step 4: Test Access

Ask Claude to read a file from the new repo:

```
"Read the README.md from /path/to/new-repo/"
```

## Step 5: Optionally Configure Bi-directional Access

For bi-directional access, repeat this process in the other repository's `.claude/settings.json` pointing back to this repo.

## Notes

- Paths must be absolute (start with `/`)
- Access is read-only when `/read-external` skill is invoked
- Normal access allows full tool use; use `/read-external` for guaranteed read-only
