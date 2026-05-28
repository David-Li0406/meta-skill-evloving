# Title Engine API Response Cheatsheet

*Auto-generated from Pydantic schemas + live API.*

## Quick Reference

### Top-Level Response
```
package_id: string
version: "2.0"
built_at: datetime
result: TitleEngineResult  # <-- Main payload
```

### Entity Counts
| Entity | Path | Count |
|--------|------|-------|
| Instrument | `.result.instruments[]` | `.instruments_count` |
| TractContext | `.result.tract_contexts[]` | `.tract_contexts_count` |
| Assertion | `.result.assertions[]` | `.assertions_count` |
| EffectEvent | `.result.effects[]` | `.effects_count` |
| ExploratoryTrace | `.result.traces["eff-xxx"][]` | - |
| ReasoningOutcome | `.result.outcomes[]` | - |
| Issue | `.result.issues[]` | `.issues_count` |
| Assumption | `.result.assumptions[]` | `.assumptions_count` |
| Interest | `.result.interests[]` | `.interests_count` |
| Gap | `.result.gaps[]` | `.gaps_count` |

---

## Instrument
**Path:** `.result.instruments[]`
**Count:** `.instruments_count`

| Field | Type | Example |
|-------|------|---------|
| instrument_id | string | `"inst-6c4b9932-9526-4969-9..."` |
| doc_id | string | `"6c4b9932-9526-4969-98b1-c..."` |
| vol_page | string | null | `"D:128"` |
| sequence_number | integer | null | `1` |
| raw_grantor | string | null | `"B.R.W. Bill"` |
| raw_grantee | string | null | `"Andrew F. Nichols"` |
| raw_executed_date | string | null | `"1851-11-15"` |
| instrument_type | enum (12 values) | `"PATENT"` |
| executed_date | date | null | `"1851-11-15"` |
| filed_date | date | null | `"1833-10-28"` |
| governing_date | date | null | `"1851-11-15"` |
| governing_date_type | "EXECUTED" | "FILED" | `"EXECUTED"` |
| grantor_party_ids | string[] | `[1 items]` |
| grantee_party_ids | string[] | `[1 items]` |

## TractContext
**Path:** `.result.tract_contexts[]`
**Count:** `.tract_contexts_count`

| Field | Type | Example |
|-------|------|---------|
| tract_context_id | string | `"tc-tract_010b3382"` |
| label | string | `""` |
| effective_date | date | `"1851-11-15"` |
| description_ref | string | null | `"those lands and rights in..."` |
| derivation_type | "ORIGINAL" | "SPLIT" | "MERGE" | "REDEFINITION" | "UNKNOWN" | `"ORIGINAL"` |
| formation_instrument_id | string | `"inst-6c4b9932-9526-4969-9..."` |
| acreage | number | null | - |
| parentage_type | string | null | `"unknown"` |
| parent_tract_label | string | null | - |
| parent_tract_type | string | null | - |
| parent_tract_acreage | number | null | - |
| remainder_context | dict | null | - |
| provenance | "extracted" | "inherited" | `"extracted"` |
| inherited_from_tract_id | string | null | - |

## Assertion
**Path:** `.result.assertions[]`
**Count:** `.assertions_count`

| Field | Type | Example |
|-------|------|---------|
| assertion_id | string | `"asrt-20918223-7429-42b8-9..."` |
| assertion_kind | "STATED_TERM" | "RECITAL" | "CONDITION" | "DEFECT_FLAG" | `"STATED_TERM"` |
| instrument_id | string | `"inst-6c4b9932-9526-4969-9..."` |
| clause_id | string | null | - |
| effect_id | string | null | `"eff-726f847a-ccd8-4532-a5..."` |
| content | dict | `{...}` |
| derivation_mode | "STATED" | "IMPLIED_DEFAULT" | `"IMPLIED_DEFAULT"` |
| legal_basis | string | null | `"Full conveyance implied w..."` |
| reference_status | "KNOWN_IN_PACKAGE" | "NOT_IN_PACKAGE" | "UNKNOWN" | null | - |
| reference_target | ReferenceTarget | null | - |

## EffectEvent
**Path:** `.result.effects[]`
**Count:** `.effects_count`

| Field | Type | Example |
|-------|------|---------|
| effect_id | string | `"eff-726f847a-ccd8-4532-a5..."` |
| effect_type | "TRANSFER" | "SEVER_CREATE" | "BURDEN" | "TERMINATE" | `"TRANSFER"` |
| doc_id | string | `"6c4b9932-9526-4969-98b1-c..."` |
| clause_id | string | null | - |
| effective_date | date | `"1851-11-15"` |
| tract_context_ids | string[] | `[1 items]` |
| tract_id | string | null | `"tract_010b3382"` |
| grantor_party_ids | string[] | `[1 items]` |
| grantee_party_ids | string[] | `[1 items]` |
| fraction | Fraction | null | `{...}` |
| effect_status | "ASSERTED" | "CONTINGENT" | "VESTED" | "UNPROVEN" | "UNPARSED" | `"ASSERTED"` |
| is_root | boolean | `True` |
| subject_to_effect_ids | string[] | `[0 items]` |
| details | dict | `{...}` |
| confidence | "low" | "medium" | "high" | `"high"` |
| notes | string | null | - |

## ExploratoryTrace (Traces)

**IMPORTANT:** Traces is a **dict keyed by effect_id**, not a list.

```bash
# Get all effect IDs with traces
.result.traces | keys

# Get traces for specific effect
.result.traces["eff-c7b86e53-86d1-4505-b86e-a51ceb17ced8"][]

# Count traces per effect
.result.traces | to_entries | map({effect: .key, count: (.value | length)})
```

| Field | Type |
|-------|------|
| trace_id | string |
| effect_id | string |
| tract_context_id | string | null |
| candidate_source_effect_ids | string[] |
| status | "CANDIDATE" | "SELECTED" | "REJECTED" | "UNRESOLVED" |
| candidate_interest_id | string | null |
| plausible_interest_id | string | null |
| is_synthetic | boolean |
| source_tract_id | string | null |
| tract_continuity_hypothesis_id | string | null |
| parent_tract_continuity_hypothesis_id | string | null |
| is_carveout | boolean | null |
| source_is_multi_tract | boolean |
| source_tract_context_id | string | null |
| signals | Signal[] |
| aggregate_score | number |
| rationale | string | null |

## ReasoningOutcome
**Path:** `.result.outcomes[]`

| Field | Type | Example |
|-------|------|---------|
| outcome_id | string | null | `"out-2ddd756c-d8a6-4c2b-9d..."` |
| effect_id | string | `"eff-726f847a-ccd8-4532-a5..."` |
| tract_context_id | string | null | `"tc-tract_010b3382"` |
| status | "RESOLVED" | "AMBIGUOUS" | "AMBIGUOUS_SOURCE_TRACT" | "GAP" | `"RESOLVED"` |
| selected_trace_id | string | null | - |
| rationale | string | null | `"Root effect (patent) — no..."` |
| signals | Signal[] | `[0 items]` |

## Issue
**Path:** `.result.issues[]`
**Count:** `.issues_count`

| Field | Type | Example |
|-------|------|---------|
| issue_id | string | `"iss-6a15f222-84ae-4c66-99..."` |
| issue_type | "GAP" | "OBSERVATION" | `"OBSERVATION"` |
| anchor_type | "INSTRUMENT" | "INTERVAL" | "TRACT" | `"INTERVAL"` |
| severity | "info" | `"info"` |
| tract_context_ids | string[] | `[1 items]` |
| temporal_bounds | TemporalBounds | null | `{...}` |
| anchor_refs | string[] | `[1 items]` |
| description | string | `"Grantor 'Andrew F. Nichol..."` |
| diagnostics | Diagnostics | `{...}` |
| related_issue_ids | string[] | `[0 items]` |

## Assumption
**Path:** `.result.assumptions[]`
**Count:** `.assumptions_count`

| Field | Type | Example |
|-------|------|---------|
| assumption_id | string | `"asmp-8906da05-56bc-4b6f-9..."` |
| assumption_text | string | `"Assumes 'Andrew F. Nichol..."` |
| scope | "GLOBAL" | "TRACT" | "INTERVAL" | "INSTRUMENT" | `"INTERVAL"` |
| tract_context_ids | string[] | `[1 items]` |
| temporal_bounds | TemporalBounds | null | `{...}` |
| instrument_ids | string[] | `[1 items]` |
| related_issue_ids | string[] | `[1 items]` |
| signal_types | string[] | `[1 items]` |
| anchor_refs | string[] | `[1 items]` |
| diagnostics | Diagnostics | `{...}` |

## Interest
**Path:** `.result.interests[]`
**Count:** `.interests_count`

| Field | Type | Example |
|-------|------|---------|
| interest_id | string | `"int-dc9128a3-9f36-481e-b6..."` |
| interest_type | enum (7 values) | `"FEE"` |
| owner_party_id | string | `"party_3aa7c91c"` |
| tract_context_id | string | null | `"tc-tract_010b3382"` |
| tract_id | string | null | `"tc-tract_010b3382"` |
| land_scope | LandScope | `{...}` |
| fraction | Fraction | null | `{...}` |
| effective_date | date | `"1851-11-15"` |
| terminated_at | date | null | - |
| provenance | enum (6 values) | `"PATENT"` |
| source_effect_id | string | null | `"eff-726f847a-ccd8-4532-a5..."` |
| evidence_doc_ids | string[] | `[1 items]` |
| burden_interest_ids | string[] | `[0 items]` |
| confidence | "low" | "medium" | "high" | `"high"` |
| notes | string | null | - |

## Gap
**Path:** `.result.gaps[]`
**Count:** `.gaps_count`

| Field | Type | Example |
|-------|------|---------|
| gap_id | string | `"gap-caaf06b0-a2ca-4a3c-9d..."` |
| gap_type | enum (7 values) | `"MISSING_GRANTOR"` |
| effect_id | string | `"eff-8c215a74-0c6a-4f03-bb..."` |
| tract_id | string | `"tract_743f3eba"` |
| description | string | `"No provable candidate (to..."` |
| missing_party_ids | string[] | `[1 items]` |
| evidence_doc_ids | string[] | `[1 items]` |
| diagnostics | dict | `{...}` |

---

## Entity Relationships

### ID Prefix Conventions
| Prefix | Entity |
|--------|--------|
| `inst-` | Instrument |
| `tc-` | TractContext |
| `eff-` | EffectEvent |
| `out-` | ReasoningOutcome |
| `tr-` | ExploratoryTrace |
| `iss-` | Issue |
| `asmp-` | Assumption |

### Join Patterns
```bash
# Effect -> Instrument (via doc_id, no prefix)
.result.instruments[] | select(.doc_id == "6c4b9932-...")

# Effect -> TractContext(s)
.result.tract_contexts[] | select(.tract_context_id == "tc-xxx")

# Traces for an effect (dict lookup)
.result.traces["eff-xxx"][]

# Outcome -> selected trace
.result.traces["eff-xxx"][] | select(.trace_id == .selected_trace_id)

# Issue -> linked entities
.result.issues[] | .anchor_refs[], .diagnostics.refs[]
```

## Common Operations

```bash
# List all GAP issues
.result.issues[] | select(.issue_type == "GAP")

# List all OBSERVATION issues
.result.issues[] | select(.issue_type == "OBSERVATION")

# Get effects for a specific doc
.result.effects[] | select(.doc_id | contains("6c4b9932"))

# Get instruments by type
.result.instruments[] | select(.instrument_type == "DEED")

# Find outcomes with GAP status
.result.outcomes[] | select(.status == "GAP")

# Get all tract labels
.result.tract_contexts[] | .label

# Count effects per tract
.result.effects | group_by(.tract_context_ids[0]) | map({tract: .[0].tract_context_ids[0], count: length})

# Get signals for a trace
.result.traces["eff-xxx"][] | {tract: .tract_context_id, score: .aggregate_score, signals: [.signals[].signal_type]}
```

## effect.details Inner Schema

The `details` dict contains document-specific metadata:

| Key | Type | When Set | Purpose |
|-----|------|----------|---------|
| `doc_type` | string | Always | Document type (PATENT, DEED, etc.) |
| `estate_type` | string | Deeds | Estate type from conveyance (e.g., "fee_simple") |
| `conveyance_scope` | string | Deeds | Scope of conveyance |
| `generic_slot` | bool | UNPARSED | Flag for generic slot documents |
| `doc_category` | string | UNPARSED | Category for generic slot docs |
| `tract_inherited` | bool | Inherited | Tract was inherited from parent effect |
| `inherited_from_effect_id` | string | Inherited | Source effect ID |

```bash
# Get all effects with estate_type
.result.effects[] | select(.details.estate_type) | {effect_id, estate: .details.estate_type}

# Find inherited tracts
.result.effects[] | select(.details.tract_inherited) | {effect_id, from: .details.inherited_from_effect_id}

# Get UNPARSED/generic slot effects
.result.effects[] | select(.details.generic_slot) | {effect_id, category: .details.doc_category}
```

## Deprecated (v2)

| Old | Use Instead |
|-----|-------------|
| `.result.interests[]` | Derived on-demand (optional) |
| `.result.gaps[]` | `.result.issues[]` with `issue_type == "GAP"` |
| `effect.tract_id` | `effect.tract_context_ids[]` |
| `trace.candidate_interest_id` | `trace.candidate_source_effect_ids[]` |

## AuditorLog (optional)
**Path:** `.result.auditor_log`

| Field | Type |
|-------|------|
| run_id | string |
| timestamp | datetime |
| checks_run | integer |
| checks_skipped | integer |
| checks_errored | integer |
| total_issues | integer |
| duration_ms | integer |
| results | CheckResult[] |
| missing_templates | string[] |
