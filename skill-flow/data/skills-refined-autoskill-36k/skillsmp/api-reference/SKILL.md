---
name: api-reference
description: PDF-RAG API reference. REQUIRED after any failed curl/jq to localhost:8000 (404, null, jq error). Also use when uncertain about endpoint path or response shape.
---

# API Reference Router

**On failure, read the right cheatsheet based on URL pattern:**

| URL Pattern | Read This |
|-------------|-----------|
| `/title-engine` | TITLE_ENGINE_PATHS.md |
| `/documents/{id}/parties\|conveyance\|land\|dates\|doc_type` | EXTRACTION_PATHS.md |
| `/l2/parties\|tracts` | EXTRACTION_PATHS.md (L2 section) |
| `/estate-graph` | See Estate Graph section below |
| Other endpoints | API_REFERENCE.md |

## Quick Wins (memorize these)

| Need | jq |
|------|----|
| Title Engine effects | `.result.effects[]` |
| Title Engine issues | `.result.issues[]` |
| Title Engine traces | `.result.traces["eff-xxx"][]` |
| Extraction resolved | `.resolved.{field}` |
| Documents list | `.items[]` |
| Packages list | `.packages[]` |
| Package docs | `.documents[]` |

## Shell Command Rule

**NEVER use shell variable interpolation.** Inline values directly:

```bash
# WRONG - variable interpolation can fail
DOC_ID="abc123" && curl -s "http://localhost:8000/api/documents/$DOC_ID/parties"

# RIGHT - inline the value directly
curl -s "http://localhost:8000/api/documents/abc123/parties"
```

## Estate Graph Gotchas

- **GET vs POST**: GET retrieves stored graph, POST rebuilds from L0-L2 data
- **estate_type is lowercase**: `"fee"`, `"mineral"`, `"leasehold"` (not uppercase)
- **Version 1.1**: `POST {"version": "1.1"}` for exploratory signals mode
- **Nodes by type**: `.dag.nodes[] | select(.estate_type == "mineral")`
- **Gaps**: `.dag.gaps[]`
- **Summary**: `.summary.mineral_estates` for counts

```bash
# Rebuild estate graph
curl -s -X POST "http://localhost:8000/api/packages/{package_id}/estate-graph" \
  -H "Content-Type: application/json" \
  -d '{"version": "1.1"}'
```

## Processing Gotchas

- **Stages array**: `stages: ["extract_parties", "extract_dates", ...]`
- **Stage names**: `markdown`, `extract_parties`, `extract_dates`, `extract_land_description`, `extract_conveyance`, `extract_document_classification`
- **Poll jobs**: GET /api/jobs/{job_id} until status is "completed" or "failed"
- **enrich_only=true**: Re-run L1 enrichment without L0 (saves LLM cost)

---

## Cheatsheet Drift Detection

**If you encounter ANY of these, regenerate the relevant cheatsheet:**

1. **jq path from cheatsheet returns null/error** but data clearly exists
2. **Field exists in API response** but not documented in cheatsheet
3. **Type mismatch** between cheatsheet and actual response

**Regenerate commands:**
```bash
source .venv/bin/activate
python scripts/generate_title_engine_cheatsheet.py   # /title-engine drift
python scripts/generate_extraction_cheatsheet.py    # /documents/{id}/* drift
```

**After regenerating:** Re-read the updated cheatsheet, then retry the failed operation.

---

*Auto-generated cheatsheets:*
- `TITLE_ENGINE_PATHS.md` — Title Engine response paths
- `EXTRACTION_PATHS.md` — Extraction endpoint paths (L0-L2)

*Full OpenAPI spec: API_REFERENCE.md*
