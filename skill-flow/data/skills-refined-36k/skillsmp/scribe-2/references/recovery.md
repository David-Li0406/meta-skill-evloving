# Recovery Reference

Commands for fixing mistakes and editing entries.

## Edit Latest Entry Commands

If something goes wrong (validation fails, user wants to change something), use `edit-latest`:

```bash
python {SKILL_DIR}/scripts/entry.py edit-latest show       # Display the latest entry
python {SKILL_DIR}/scripts/entry.py edit-latest delete     # Remove latest entry AND its assets
python {SKILL_DIR}/scripts/entry.py edit-latest replace --file /tmp/scribe_entry_${CLAUDE_SESSION_ID}.md  # Replace latest entry
python {SKILL_DIR}/scripts/entry.py edit-latest rearchive <file>  # Re-archive a file for latest entry
python {SKILL_DIR}/scripts/entry.py edit-latest unarchive  # Delete assets for latest entry (keep entry)
```

## Common Recovery Flows

### Abort After Failed Archive

```bash
python {SKILL_DIR}/scripts/entry.py edit-latest delete
```
Removes entry + all its assets.

### Fix Wrong File Archived

```bash
python {SKILL_DIR}/scripts/entry.py edit-latest rearchive correct_file.py
```

### Fix Entry Content

1. Write corrected entry to `/tmp/scribe_entry_${CLAUDE_SESSION_ID}.md`
2. Run: `python {SKILL_DIR}/scripts/entry.py edit-latest replace --file /tmp/scribe_entry_${CLAUDE_SESSION_ID}.md`

### Remove Archives but Keep Entry

1. `python {SKILL_DIR}/scripts/entry.py edit-latest unarchive`
2. Then replace the entry to remove the **Archived** section

## Validation

Run validation to check for issues:

```bash
python {SKILL_DIR}/scripts/validate.py
```

Validation checks:
- Every entry has an ID
- Entry ID format is valid
- Archived files referenced in entries actually exist
- Related references point to valid entry IDs
- No orphaned assets (files in `assets/` not referenced by any entry)

If validation fails, fix the issue before continuing. Use `edit-latest` commands to fix or remove broken entries.

## Other Entry Commands

```bash
python {SKILL_DIR}/scripts/entry.py new-id              # Generate ID for current time
python {SKILL_DIR}/scripts/entry.py new-id --time 14:35 # Generate ID for specific time
python {SKILL_DIR}/scripts/entry.py last                # Show last entry ID from today's log only
python {SKILL_DIR}/scripts/entry.py last --with-title   # Include title (useful for Related links)
```
