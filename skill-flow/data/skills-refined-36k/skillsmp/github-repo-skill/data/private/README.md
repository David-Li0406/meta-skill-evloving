# Private Data

This directory contains private/unpublished data from the CMM research team.

**All contents (except READMEs) are gitignored.**

## Directory Structure

```
data/private/
├── *.tsv                    # Raw Google Sheets downloads (purgeable)
├── derived/                 # Normalized and enriched data (preserve)
└── norm-2026-01-07/         # Snapshot from normalized Google Sheet
```

## Root TSV Files

**Source:** Downloaded from "BER CMM Data for AI - for editing" Google Sheet

**Regeneration:**
```bash
uv run python -m cmm_ai_automation.scripts.download_sheets
```

These files can be safely deleted and re-downloaded. They are the raw input data.

## Subdirectories

- **derived/** - Normalized/enriched data with added value (see derived/README.md)
- **norm-2026-01-07/** - Snapshot from separate normalized Google Sheet (see norm-2026-01-07/README.md)

## Privacy Policy

Files in this directory contain:
- Custom media compositions (proprietary)
- Strain-media growth relationships (unpublished research)
- Lab-specific annotations

**Do NOT commit to public repositories.**
