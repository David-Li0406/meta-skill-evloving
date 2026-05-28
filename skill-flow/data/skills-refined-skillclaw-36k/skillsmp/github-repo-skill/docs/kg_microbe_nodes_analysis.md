# Analysis of `kg_microbe_nodes` Mapping Quality

**Date:** 2026-01-06  
**Context:** CMM-AI / kg-microbe Growth Media Grounding

## Overview

This document analyzes the provenance and quality of the `kg_microbe_nodes` column found in the CMM growth media dataset. These mappings link local media names (e.g., "MP medium") to identifiers in the `kg-microbe` knowledge graph (prefixed with `medium:`).

Our investigation reveals that these mappings were generated using broad keyword matching strategies, resulting in a high rate of false positives that require filtering.

## Provenance Investigation

Code analysis of the sibling `CMM-AI` repository (specifically `src/media_search.py`) identified the likely mechanism for generating these links:

```python
# Query pattern found in CMM-AI/src/media_search.py
query = "SELECT * FROM nodes WHERE id LIKE 'medium:%' AND name LIKE '%{keyword}%'"
```

This approach uses a SQL-style `LIKE` operator on the media name. While effective for recall, it lacks semantic disambiguation, causing common acronyms (like "MP") to match unrelated media that merely contain those letters in their name.

## Quality Audit

We audited the mappings against the **MediaDive** database (the source of `medium:` IDs) and **TogoMedium**.

### 1. High-Confidence Matches (Valid)
Mappings where the keyword match aligned with the intended medium.

| Input Name | Mapped ID | Mapped Name in DB | Verdict |
| :--- | :--- | :--- | :--- |
| **AMS medium** | `medium:921a` | AMS medium | ✅ **Exact Match** |
| **LB medium** | `medium:381` | LB (Luria-Bertani) MEDIUM | ✅ **Exact Match** |
| **NMS medium** | `medium:632` | NMS MEDIUM | ✅ **Exact Match** |

### 2. Low-Confidence Matches (False Positives)
Mappings where the broad keyword search captured unrelated entities.

#### Case Study: "MP medium"
The acronym "MP" (Methylotroph PIPES) is short and non-unique. The keyword search matched any medium containing "MP".

| Input Name | Mapped ID | Mapped Name in DB | Issue |
| :--- | :--- | :--- | :--- |
| MP medium | `medium:1413` | A**MP**HIBACILLUS MEDIUM | Substring match (unrelated) |
| MP medium | `medium:J562` | LA**MP**ROBACTER ROSEUS MEDIUM | Substring match (unrelated) |
| MP medium | `medium:J918` | DESULFA**MP**LUS MEDIUM | Substring match (unrelated) |
| MP medium | `medium:J1168` | LB ... WITH RIFA**MP**ICIN | Substring match (ingredient) |

#### Case Study: "LB medium"
While it found the correct LB (`medium:381`), it also included irrelevant partial matches.

| Input Name | Mapped ID | Mapped Name in DB | Issue |
| :--- | :--- | :--- | :--- |
| LB medium | `medium:J1200` | E**LB**E METHANOTROPH MEDIUM | Substring match (unrelated) |
| LB medium | `medium:J316` | THERMOCRINIS A**LB**US MEDIUM | Substring match (unrelated) |

## Impact on Knowledge Graph

Including these low-quality mappings as `biolink:same_as` or `biolink:xref` edges would introduce significant noise, potentially conflating distinct media (e.g., asserting that "MP medium" is the same as "Amphibacillus Medium").

## Recommended Mitigation

1.  **Strict Filtering:** Do not ingest `kg_microbe_nodes` blindly.
2.  **Validation:** Verify each candidate ID against the MediaDive/TogoMedium database.
3.  **Name Similarity Check:** Only accept mappings where the name in the database matches the input name with high similarity (e.g., exact match or Levenshtein distance > 0.9).
4.  **Prioritize Semantics:** Rely on the Semantic Search (vector embedding) approach implemented in the new `cmm-ai-automation` pipeline, which correctly distinguishes "MP medium" context from simple substrings.
