---
name: permanent-capture
description: "Create and store Obsidian permanent notes under permanent based on user-provided fields (title, summary, domain, kind, topics, status, content). Use when the user says; capture this as a permanent note, add this to permanent, create a hub/leaf/howto/decision/glossary note, or when an agent needs to file structured knowledge into permanent with standardized frontmatter and tags."
---

# Permanent Note Capture

Create a new note in `permanent/` from structured user input.

## Collect Inputs

Read `references/input-schema.md` and collect the required fields.

If any required field is missing, ask a focused follow-up question.

## Decide Destination

- Default destination is based on `kind`:
  - `hub` → `permanent/10_hub/`
  - `glossary` → `permanent/30_glossary/`
  - otherwise → `permanent/20_leaf/`
- If the user cannot provide a meaningful `summary`, route to `permanent/00_inbox/`.
- If the user explicitly requests a folder, honor it.

## Create the Note

**Important: All note content must be written in Japanese.**

### Method 1: Python Script (Preferred)

Run the Python script from workspace root:

- `.claude/skills/permanent-capture/scripts/create_permanent_note.py`

Pass parameters:

- `--title` (required)
- `--summary` (recommended; if empty, the script routes to inbox)
- `--domain` (`work` or `learning`)
- `--kind` (`hub|leaf|howto|principle|decision|glossary`)
- `--status` (`seed|draft|evergreen|deprecated`)
- `--topics` (comma-separated; keep <= 3)
- `--related` (comma-separated wiki links)
- `--aliases` (comma-separated)
- `--content` or `--content-file`

Prefer not to overwrite existing notes; let the script choose a unique filename.

**Note**: If script execution fails due to encoding issues (especially with Japanese text), use Method 2.

### Method 2: Direct File Creation (Fallback)

If the script cannot run, create the note directly using `create_file`:

1. Determine target folder based on `kind`:
   - `hub` → `permanent/10_hub/`
   - `glossary` → `permanent/30_glossary/`
   - others → `permanent/20_leaf/`
   - no summary → `permanent/00_inbox/`

2. Create file with frontmatter:
   ```yaml
   ---
   title: <title>
   summary: <summary>
   tags: [d/<domain>, t/<topic1>, t/<topic2>, k/<kind>, s/<status>]
   status: <status>
   created: <current-date>
   updated: <current-date>
   ---
   ```

3. Append the content body.

4. Use filename: `<title>.md` (sanitize special characters)

## Post-Create Checks

- Confirm the created path.
- If the user provides related hub/MOC notes, propose adding links manually or as a follow-up task.

## Templates (Optional)

If the user asks for a specific structure, refer to the templates in `assets/templates/`.
