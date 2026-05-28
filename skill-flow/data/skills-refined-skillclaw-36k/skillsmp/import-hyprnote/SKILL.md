---
name: import-hyprnote
description: Import Hyprnote meeting transcripts to project-specific context repositories
---

# Import Hyprnote

Import Hyprnote meeting transcripts from the local app to the appropriate project context repositories.

## When to Use

- After recording meetings in Hyprnote
- When transcripts need to be sorted to project-specific data directories
- Periodically to keep context repos up to date

## Configuration

Requires `.entourage/config.json` with project definitions:

```json
{
  "projects": [
    {
      "name": "entourage-context",
      "path": "~/Documents/code/@orgs/my-entourage/entourage-context",
      "description": "AI agent development and product specs",
      "keywords": ["agent", "spec", "inbox", "timeline", "Jared"]
    }
  ]
}
```

## Workflow

### Step 1: Load Configuration

1. Read `.entourage/config.json` from current working directory
2. If not found, prompt user to create configuration:
   - Scan `~/Documents/` for `*-context/` directories
   - Present found projects for confirmation
   - Ask for description and keywords for each
   - Save to `.entourage/config.json`

### Step 2: Discover Hyprnote Sessions

1. List all sessions in `~/Library/Application Support/hyprnote/sessions/`
2. For each session, check for:
   - `_meta.json` (required)
   - `_transcript.json` (required)
   - `_memo.md` (optional)

3. Skip sessions that are empty (no transcript content)

### Step 3: Classify Sessions

For each session:

1. Read `_transcript.json` and reconstruct text:
   ```
   words.map(w => w.text).join('').trim()
   ```

2. Read `_memo.md` if exists

3. Match against project keywords (case-insensitive)

4. Assign to best matching project, or "unclassified" if no match

### Step 4: Present Classification for Approval

Present a table to the user:

```markdown
## Session Classification

| Session | Date | Title | Assigned To | Confidence |
|---------|------|-------|-------------|------------|
| abc123 | 2026-01-14 | Team standup | entourage-context | High (5 keywords) |
| def456 | 2026-01-13 | Procurement call | viran-context | Medium (2 keywords) |
| ghi789 | 2026-01-12 | Personal notes | unclassified | Low (0 keywords) |

Proceed with this classification? (You can reassign any session)
```

Wait for user confirmation or adjustments.

### Step 5: Execute Import

For each confirmed session:

1. Create destination directory: `{project_path}/data/transcripts/hyprnote/{session_id}/`

2. Copy files:
   - `_meta.json`
   - `_transcript.json`
   - `_memo.md` (if exists)

3. Do NOT delete source files (user can clean up manually)

### Step 6: Commit Changes (Optional)

For each affected project:

1. Ask user if they want to commit the changes

2. If yes:
   ```bash
   git -C {project_path} add data/transcripts/hyprnote/
   git -C {project_path} commit -m "Import Hyprnote transcripts from {date}"
   ```

## Output

Summary of what was imported:

```markdown
## Import Complete

Imported 3 sessions:
- entourage-context: 2 sessions
- viran-context: 1 session

Skipped:
- 1 unclassified session (ghi789)
- 2 empty sessions

Run `/update-timeline` in each context repo to process these transcripts.
```

## Error Handling

- **No config found**: Guide user through setup wizard
- **No Hyprnote sessions**: Report "No sessions found in Hyprnote"
- **Project path doesn't exist**: Warn and skip that project
- **Git not available**: Skip commit step, warn user

## Execution Behavior

This skill returns results to the calling context and does NOT stop execution.
