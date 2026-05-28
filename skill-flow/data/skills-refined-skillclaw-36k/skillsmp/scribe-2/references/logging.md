# Logging Reference

Detailed examples and formats for the logging mode.

## Example Interaction

> **User:** scribe, log this
>
> **Claude:** Here's what I'll log:
>
> ---
> **14:35 — Fixed null handling in ETL pipeline**
>
> Found that nulls originated from the 2019 migration. Updated `etl.py` to coalesce nulls to zero for pre-2019 records. Validated on test dataset.
>
> **Files touched:** `etl.py`, `exploration.ipynb`
>
> **Status:** Ready for full validation
>
> ---
>
> **Archive these files?** (optional)
> - [ ] `etl.py`
> - [ ] `exploration.ipynb`
>
> Let me know if this looks right, or any changes.

Then the user might say:
- "looks good" → Claude writes the entry
- "also snapshot etl.py" → Claude writes entry + archives the file
- "no, the issue was timezone handling not nulls" → Claude revises and re-proposes

## Entry Format (Input)

Provide the title without a timestamp — the script adds the current time automatically.

(Legacy format `## HH:MM — Title` is also accepted; the script will use the provided time instead of current time.)

```markdown
## [Brief title]

[Narrative paragraph describing what happened]

**Files touched:** (if applicable)
- `path/to/file.py` — Added retry logic; increased timeout to 30s
- `config.yaml` — Bumped max_retries from 3 to 5

**Status:** [Current state, next steps, or open questions]

---
```

## Entry Format (Output)

The script prepends the timestamp, so the written entry looks like:

```markdown
## 14:35 — [Brief title]
<!-- id: 2026-01-23-14-35 -->

...
```

## Writing the Entry

Use Claude's Write tool to create a temp file, then pass it to `entry.py`:

**Step 1:** Use the Write tool to create `/tmp/scribe_entry_${CLAUDE_SESSION_ID}.md`:

```markdown
## Fixed null handling in ETL pipeline

Found that nulls originated from the 2019 migration.

**Files touched:**
- `etl.py` — Added coalesce logic

**Status:** Ready for validation

---
```

**Step 2:** Run the script with `--file`:

```bash
python {SKILL_DIR}/scripts/entry.py write --file /tmp/scribe_entry_${CLAUDE_SESSION_ID}.md
```

Output: `Entry written: 2026-01-23-14-35`

The script automatically:
- Gets the current system time (24-hour local time)
- Prepends the timestamp to the title (`## Title` → `## HH:MM — Title`)
- Generates the entry ID from the date + time
- Handles collisions (adds `-02`, `-03` suffix if needed)
- Injects the `<!-- id: ... -->` comment
- Creates today's log file if it doesn't exist
- Appends the entry
- Validates the entry (unless `--no-validate` is passed)

## What to Capture

- The question, problem, or goal being worked on
- Approaches tried
- What worked, what failed, and why
- Files created or modified, with brief descriptions of changes
- Key discoveries, surprises, or turning points
- Current status — where things stand now

## User Annotations

The user may add context: `scribe — this was a dead end`. Incorporate their editorial judgment.

## After Writing

Display a brief summary so the user can verify:

> Logged:
>
> **14:35 — [Title]**
>
> [First sentence or two of the narrative]
>
> *Files touched: `file1.py`, `file2.py`*
