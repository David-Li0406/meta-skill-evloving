---
summary: "Future design notes for memory synthesis (episodic narrative)"
read_when:
  - You are ready to design memory synthesis
  - You need to handle episodic continuity and backfill
---
# Memory Synthesis — Investigation Notes (Deferred)

This document outlines the **future** synthesis layer that turns extracted
signals (facets) into narrative memory. This is not implemented yet. The goal
is to clarify design questions before we commit to a format or storage model.

---

## Why Synthesis Is Different

Extraction is parallel and independent. Synthesis is **sequential and stateful**:

- New memory depends on previous memory
- Backdated events can invalidate prior synthesis
- Output must be consistent over time

This makes synthesis a distinct pipeline with different performance and
correctness requirements.

---

## Candidate Inputs

When synthesizing memory for Day N:

1. **Raw events** for Day N (all channels)
2. **Extracted facets** from Day N
3. **Prior memory state** (Day N-1 summary + long-term memory)
4. **Standing facts** (identity/person facts)
5. **Corrections** (user corrections from AI sessions)

This means synthesis prompts cannot run on a single conversation chunk alone.

---

## Candidate Outputs (TBD)

Possible outputs, in increasing complexity:

1. **Daily narrative** — a short summary of what happened that day
2. **Memory state update** — a delta: add/modify/remove facts
3. **Long-term memory snapshot** — condensed view of stable preferences/knowledge

We do not need to decide the final format yet, but synthesis must be able to:
- preserve provenance
- support overrides
- support backfill

---

## Storage Options (No New Tables Required)

Use existing analysis infrastructure:

- `analysis_types`: `daily_memory_v1`, `weekly_memory_v1`
- `analysis_runs.output_text`: stores the narrative summary
- `facets`: optional secondary extraction from synthesized text (if needed)

This keeps synthesis within the same comms machinery.

---

## Backfill Strategy

If new events arrive for Day K (in the past), synthesis must:

1. Recompute Day K summary
2. Recompute every day from K → present (because state is sequential)

This implies synthesis must be:
- deterministic (given same inputs)
- cacheable (avoid recompute if inputs unchanged)

---

## Episodic Context Injection

Synthesis prompts should include **prior memory** explicitly:

```
Input:
  - Prior day summary
  - Standing memory (long-term)
  - Today's raw events + facets
Task:
  - Produce updated daily narrative
  - Update long-term memory (optional)
```

Without this, the synthesis will re-discover the same facts repeatedly.

---

## Conflict Resolution

Memory synthesis must decide how to handle contradictions:

- **Recency wins** by default
- **Explicit corrections override**
- **Confidence weighting** (frequency + source quality)

This is a synthesis rule set, not an extraction rule.

---

## Evaluation / Tests

Minimum evaluation set:

1. **Correction overwrite** — newer preference supersedes older
2. **Backfill** — add earlier event, ensure downstream memory updates
3. **Stability** — repeated synthesis with same inputs yields same output

---

## Open Questions

1. What is the minimal memory representation we can ship first?
2. Should daily summaries be stored as analysis output, or rendered files?
3. How to maintain provenance for synthesized memory?
4. How much context is enough to avoid drifting narratives?
5. Should synthesis be per-scope (user/agent/workspace) or unified?

---

## Decision: Not Now

We should **not** implement synthesis until extraction is solid and retrieval
use cases are validated. This doc exists to guide future work when that time
comes.
