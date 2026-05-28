# Usage Example: fixlog_writer

This skill standardizes the creation of FixLogs to reduce formatting errors and ensure that critical metadata (such as `result` or `files`) are always present.

## Generating Payload (Dry Run)
Use the script to generate the correct JSON to paste into the `chroma_add_documents` tool.

```bash
uv run .agent/skills/fixlog_writer/scripts/write_log.py \
  --project "Antigravity" \
  --desc "Standardized all skill definitions" \
  --files ".agent/skills/resolve_canon_sources/SKILL.md, .agent/skills/test_gate_bivio/SKILL.md" \
  --test "Canary Check passed" \
  --result "pass" \
  --dry-run
```

## Workflow Integration
In `tech_rag.md` (Step 6), instead of writing "Save a document...", now invoke:

> **Skill**: `fixlog_writer` (Standardizes the JSON payload).

## Expected Output
A valid JSON ready for ingestion:
```json
{
  "id": "AG.fix.20260114.a1b2c3d4",
  "document": "Standardized all skill definitions",
  "metadatas": {
    "project": "Antigravity",
    "type": "fix_log",
    "date": "2026-01-14",
    ...
  }
}
```
