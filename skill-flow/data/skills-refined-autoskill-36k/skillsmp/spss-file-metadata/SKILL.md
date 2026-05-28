---
name: spss-file-metadata
description: Extract metadata from SPSS .sav files as JSON using pyreadstat
license: MIT
compatibility: opencode
metadata:
  audience: data-analysts
  language: python
---

## Usage

**DO NOT CREATE A NEW SCRIPT!** Use the pre-installed script:

```bash
.opencode/skills/spss-file-metadata/run.sh <path_to_sav_file> [output_json_file]
```

Examples:

```bash
# Output to stdout
.opencode/skills/spss-file-metadata/run.sh blueprint.sav

# Save to file
.opencode/skills/spss-file-metadata/run.sh blueprint.sav metadata.json
```

## What it does

Extracts metadata from SPSS `.sav` files without loading data rows (fast, memory efficient):

- Column names, labels, types, formats
- Value labels for categorical variables
- File properties (encoding, row/column counts)
- Missing value ranges

Uses `pyreadstat` with `metadataonly=True`. All dependencies pre-installed in virtual environment at `.opencode/skills/spss-file-metadata/venv/`.
