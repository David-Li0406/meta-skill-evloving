---
name: fixlog_writer
description: Standardizes FixLog writing and handles Chrome persistence.
version: 1.0.0
author: Antigravity
---

# Operational Instructions

## Triggers
- At the end of every workflow involving modifications (`tech_rag`, `refactor`).
- When a technical intervention needs to be tracked (Step 6 Persistence).

## Inputs
- **Prefix**: (from `PROJECT_AGENT_CONFIG.md`) Project prefix.
- **ProjectName**: (from `PROJECT_AGENT_CONFIG.md`) Project name.
- **Log Data**: JSON containing `id`, `document` (description), and `metadatas` (project, type, date, files, tests, result).

## CLI Parameters (write_log.py)
```bash
uv run .agent/skills/fixlog_writer/scripts/write_log.py \
  --project "ProjectName" \
  --prefix "PREFIX" \
  --desc "Description of the fix" \
  --files "file1.py,file2.js" \
  --test "Test description" \
  --result "pass"  # ⚠️ VALID VALUES: "pass" or "fail" (NOT "success"!)
```

**Critical Parameter Values:**
- `--result`: **ONLY** accepts `"pass"` or `"fail"` (enforced by argparse choices)
- `--files`: Comma-separated list of file paths (will be split into array)

## Steps
1. **Prepare Data**: Collect intervention data.
2. **Format JSON**: Create a JSON structure compatible with Chroma.
3. **Persist (Dual Write)**:
    - Write to `.agent/fix_logs/<ID>.json`.
    - Upsert to ChromaDB collection `fix_logs`.
4. **Verification**: Confirm file exists and Chroma entry is searchable.

## Usage Example
```bash
uv run .agent/skills/fixlog_writer/scripts/write_log.py \
  --project "Antigravity" \
  --prefix "AG" \
  --desc "Fixed critical bug in authentication flow" \
  --files "src/auth.py,tests/test_auth.py" \
  --test "pytest tests/test_auth.py - all passed" \
  --result "pass"
```

