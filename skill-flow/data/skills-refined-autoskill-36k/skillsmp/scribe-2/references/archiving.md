# Archiving Reference

Detailed examples for archiving and restoring files.

## Archiving Files

When the user wants to archive a file, they might say:

- "scribe, save this notebook"
- "scribe, remember clustering.ipynb — it's finally working"
- "okay scribe, snapshot the ETL script before I refactor"
- "scribe, archive data.csv"
- "scribe, store this version of the pipeline"

### Archive Flow

1. Get entry ID with `entry.py new-id` (handles minute collisions)
2. Draft entry including **Archived** section using that ID
3. Write entry with `entry.py write`
4. Archive files with `assets.py save <id> <file>`

The asset filename is predictable: `{entry-id}-{filename}`. Include it in your draft before writing.

### Assets Script Usage

```bash
python {SKILL_DIR}/scripts/assets.py save <entry-id> <file> [<file> ...]
```

Example:

```bash
python {SKILL_DIR}/scripts/assets.py save 2026-01-23-14-35 clustering.ipynb
```

The script copies the file to `.scribe/assets/2026-01-23-14-35-clustering.ipynb`.

### Entry Format with Archive

```markdown
## 14:35 — First working clustering pipeline

Finally got k-means working after fixing the normalization issue.

**Files touched:**
- `clustering.ipynb` — Fixed StandardScaler placement; moved before PCA

**Archived:**
- `src/analysis/clustering.ipynb` → [`2026-01-23-14-35-clustering.ipynb`](assets/2026-01-23-14-35-clustering.ipynb) — First working version

**Status:** Ready to test on full dataset.

---
```

The **Archived** format is: `original/path/to/file` → `[asset-filename](asset-link)` — description. This preserves the original location for later reference.

Note: The `<!-- id: ... -->` comment is injected automatically by `entry.py` — don't write it manually.

### After Writing

Display a brief summary:

> Logged:
>
> **14:35 — [Title]**
>
> [First sentence or two of the narrative]
>
> *Archived: `src/analysis/clustering.ipynb` → `2026-01-23-14-35-clustering.ipynb`*

---

## Restoring Files

When the user wants to run or inspect an archived file:

1. Use `Grep` in `.scribe/` to find the relevant asset and its original path
2. Call the restore script to copy it to the original directory
3. Run or inspect from there

### Restore Script Usage

```bash
python {SKILL_DIR}/scripts/assets.py get <asset-filename> --dest <original-directory>
```

Example — if the entry shows:
```
**Archived:**
- `src/pipelines/etl/transform.py` → [`2026-01-23-14-35-transform.py`](assets/...)
```

Then restore with:
```bash
python {SKILL_DIR}/scripts/assets.py get 2026-01-23-14-35-transform.py --dest src/pipelines/etl/
```

The script copies the file to `src/pipelines/etl/_2026-01-23-14-35-transform.py` — next to the current version for easy comparison.

If the original directory no longer exists, create it first:
```bash
mkdir -p src/pipelines/etl/
python {SKILL_DIR}/scripts/assets.py get 2026-01-23-14-35-transform.py --dest src/pipelines/etl/
```

### List Assets

```bash
python {SKILL_DIR}/scripts/assets.py list
python {SKILL_DIR}/scripts/assets.py list 2026-01-23    # filter by date
python {SKILL_DIR}/scripts/assets.py list transform     # filter by name
```

### Important Behaviors

- Never overwrites — if the destination exists, the script fails
- If restore fails because the destination exists, tell the user and offer to delete the existing file or suggest they rename/remove it first
- Underscore prefix makes restored files obvious
- User controls cleanup — the scribe never deletes restored files
- Restored files are easy to gitignore with `_20*-*`
