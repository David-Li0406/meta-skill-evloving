# Module: Backlog Reprioritization (Merge-First)

## Objective

Reorder backlog items to maximize:
- Mergeability
- Risk reduction / enablement
- Incremental value

## Procedure

1) **Normalize backlog items** (ensure each has: ID, title, description).

2) **Tag each item** with:
   - `surface_area`: {low, medium, high}
   - `coupling_risk`: {low, medium, high}
   - `contract_touch`: {none, api, schema, shared-types, config}
   - `merge_conflict_likelihood`: {low, medium, high}
   - `dependency_hints`: {depends_on, conflicts_with}
   - `llm_complexity`: {trivial, simple, moderate, complex, very_complex}
   - `estimated_tokens`: <number> (estimated token consumption, apply category multipliers)

3) **Cluster items**:
   - "contract-first" items (schema/API/types)
   - "consumers" (UI/features relying on contracts)
   - "isolated" items (low coupling)

4) **Reprioritize** using rules:
   - Enablement first (unblocks others)
   - Contract-producers before consumers
   - High-coupling items only when phase-integrated

5) **Output**:
   - Reprioritized list (with rationale per item)
   - Identified conflicts and suggested clustering

## Output format

Markdown table:

| ID | Title | Priority | LLM Complexity | Est. Tokens | Rationale | Dependencies | Conflicts |
|----|-------|----------|----------------|-------------|-----------|--------------|-----------|
| ... | ... | ... | ... | ... | ... | ... | ... |

## LLM Complexity Guide

| Complexity | Description | Typical Tokens |
|------------|-------------|----------------|
| trivial | Single file change, clear pattern | ~5-15K |
| simple | Few files, well-defined scope | ~15-30K |
| moderate | Multiple files, some exploration needed | ~30-60K |
| complex | Cross-cutting changes, research required | ~60-120K |
| very_complex | Architectural changes, multi-phase | ~120K+ |

**Note**: Apply category multipliers from `.claude/docs/shared/metrics-templates.md`.

## Red flags

Stop and clarify if you observe:
- Two high-coupling tasks touching the same contract in parallel
- Tasks requiring refactors without explicit scope approval
- Circular dependencies
- Tasks without clear acceptance criteria
