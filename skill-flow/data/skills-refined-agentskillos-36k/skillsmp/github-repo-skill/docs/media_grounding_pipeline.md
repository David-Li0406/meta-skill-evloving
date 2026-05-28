# Media Grounding Pipeline

**Date:** 2026-01-06  
**Status:** Complete

## Overview

This pipeline transforms growth media data from Google Sheets/TSV into a Biolink-compliant KGX Knowledge Graph. It solves the challenge of grounding "local" or "lab-specific" media (like "Hypho medium") while linking established media to public databases (MediaDive).

## Key Features

1.  **Multi-Stage Grounding Engine:**
    *   **Priority 1:** Local Registry (`data/local_media_registry.tsv`) - for stable, minted IDs.
    *   **Priority 2:** Manual Mappings (`data/media_grounding_mappings.tsv`) - for curated links.
    *   **Priority 3:** Verified MediaDive IDs - checks local MongoDB for existence.
    *   **Priority 4:** Semantic Search - fuzzy matching against local ChromaDB indices (MediaDive).

2.  **Stable ID Minting:**
    *   Uses `BER-CMM-MEDIUM:XXXXXXX` (7-digit zero-padded) for local media.
    *   Example: `BER-CMM-MEDIUM:0000001` for "Hypho medium".
    *   Avoids fragile mnemonic IDs (e.g., `CMM:medium_hypho...`).

3.  **Biolink Compliance:**
    *   **Category:** `biolink:ChemicalMixture` (standard for media/mixtures).
    *   **Provenance:** `infores:cmm-ai-automation`.
    *   **Publications:** `doi:10.xxx` references attached to nodes.

4.  **Data Cleaning:**
    *   Automatic Mojibake repair (MacRoman -> UTF-8 artifacts).
    *   Normalization of names (handling parentheticals and punctuation).

## Files

| File Path | Description |
| :--- | :--- |
| `src/cmm_ai_automation/transform/growth_media_transform.py` | Core Pydantic models & grounding logic |
| `src/cmm_ai_automation/scripts/export_grounded_media_kgx.py` | CLI shim script |
| `data/local_media_registry.tsv` | **Registry of stable local IDs** |
| `data/media_grounding_mappings.tsv` | Manual curation mappings |
| `output/kgx/cmm_grounded_media_nodes.jsonl` | Final KGX Node output |
| `output/kgx/cmm_grounded_media_grounding_report.tsv` | Audit trail of grounding decisions |

## Usage

```bash
# Export grounded media nodes
uv run python -m cmm_ai_automation.scripts.export_grounded_media_kgx \
    --input "/path/to/growth_media.tsv" \
    --output output/kgx
```

## Local ID Registry (`data/local_media_registry.tsv`)

Maintained registry for media that do not exist in public databases.

| Local ID | Name | Source | Description |
| :--- | :--- | :--- | :--- |
| `BER-CMM-MEDIUM:0000001` | Hypho medium | DOI:10.1371... | Minimal medium for AM1 |
| `BER-CMM-MEDIUM:0000003` | MP medium | DOI:10.1371... | PIPES-buffered minimal |
| `BER-CMM-MEDIUM:0000006` | DSMZ Medium 88 | DSMZ:88 | SM medium for Paracoccus |
| ... | ... | ... | ... |

## Dependencies

*   **MongoDB:** Requires local instance with `mediadive` database (for verification).
*   **ChromaDB:** Requires index in `data/chroma_mediadive` (for semantic search).
