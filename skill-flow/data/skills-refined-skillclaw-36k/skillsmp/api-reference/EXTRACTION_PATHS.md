# Extraction API Cheatsheet

*Auto-generated from live API responses.*

---

## Extraction Layer Cascade

All extraction endpoints follow this pattern:

| Level | Path | Purpose |
|-------|------|---------|
| L0 | `.extraction.{field}` | Raw LLM output (debug only) |
| L1 | `.normalized.{field}` | Deterministic enrichment (debug only) |
| Resolved | `.resolved.{field}` | **READ THIS** — canonical + corrections |

Add `?debug=true` to see L0/L1 fields.

---

## Quick Field Lookup

| Looking for | Endpoint | jq Path |
|-------------|----------|---------|
| estate_type | /conveyance | `.resolved.estate_type` |
| governing_date | /dates | `.resolved.governing_date` |
| grantor names | /parties | `.resolved.canonical_parties[].canonical_name` |
| grantee names | /parties | `.resolved.canonical_parties[] \| select(.role=="grantee")` |
| doc category | /doc_type | `.resolved.doc_category` |
| acreage | /land | `.resolved.canonical_tracts[].acreage_effective` |
| survey name | /land | `.resolved.canonical_tracts[].survey` |
| parentage_type | /land | `.resolved.canonical_tracts[].parentage_type` |
| primary_term | /conveyance | `.resolved.primary_term_years` |
| royalty_rate | /conveyance | `.resolved.royalty_rate` |

---

## PARTIES
**Endpoint:** `GET /documents/{doc_id}/parties`

| Path | Type | Example |
|------|------|---------|
| `.resolved._meta.correction_count` | int | `1` |
| `.resolved._meta.last_corrected_at` | str *(PATENT only)* | `"2025-12-26T19:23:09.97428..."` |
| `.resolved._meta.last_resolved_at` | str | `"2025-12-29T02:38:24.487755Z"` |
| `.resolved._provenance.canonical_parties[0].canonical_name.correction_id` | str *(PATENT only)* | - |
| `.resolved._provenance.canonical_parties[0].canonical_name.original_value` | str *(PATENT only)* | - |
| `.resolved._provenance.canonical_parties[0].canonical_name.source` | str *(PATENT only)* | - |
| `.resolved.canonical_parties` | array | `[2 items]` |
| `.resolved.canonical_parties[].canonical_name` | str | `"State of Texas"` |
| `.resolved.canonical_parties[].capacity` | null | - |
| `.resolved.canonical_parties[].capacity_principal` | null | - |
| `.resolved.canonical_parties[].capacity_principal_type` | null | - |
| `.resolved.canonical_parties[].confidence` | float | `0.95` |
| `.resolved.canonical_parties[].entity_type` | str | `"individual"` |
| `.resolved.canonical_parties[].fiduciary_cohort_id` | null | - |
| `.resolved.canonical_parties[].fiduciary_of_party_id` | null | - |
| `.resolved.canonical_parties[].household_id` | null | `"household_f9895054"` |
| `.resolved.canonical_parties[].is_synthesized` | bool | `False` |
| `.resolved.canonical_parties[].party_id` | str | `"party_37bbd4e1"` |
| `.resolved.canonical_parties[].provenance.original_value` | null | - |
| `.resolved.canonical_parties[].provenance.override_id` | null | - |
| `.resolved.canonical_parties[].provenance.source` | str | `"override"` |
| `.resolved.canonical_parties[].raw_name` | str | `"B.R.W. Bill"` |
| `.resolved.canonical_parties[].role` | str | `"grantor"` |
| `.resolved.canonical_parties[].spouse_party_id` | null | `"party_8f97c4f5"` |
| `.resolved.households` | array | `[0 items]` |
| `.resolved.households[].household_id` | str *(DEED only)* | `"household_f9895054"` |
| `.resolved.households[].members` | array *(DEED only)* | `[2 items]` |
| `.resolved.runsheet_alignment` | null *(DEED only)* | - |
| `.resolved.runsheet_alignment.debug.grantee.all_scores` | array | `[1 items]` |
| `.resolved.runsheet_alignment.debug.grantee.all_scores[].candidate` | str | `"Andrew T. Nichols"` |
| `.resolved.runsheet_alignment.debug.grantee.all_scores[].score` | float | `0.9411764705882352` |
| `.resolved.runsheet_alignment.debug.grantee.l1_name` | str | `"Andrew F. Nichols"` |
| `.resolved.runsheet_alignment.debug.grantee.rs_name` | str | `"Andrew T. Nichols"` |
| `.resolved.runsheet_alignment.debug.grantee.score` | float | `0.9411764705882352` |
| `.resolved.runsheet_alignment.debug.grantor.all_scores` | array | `[1 items]` |
| `.resolved.runsheet_alignment.debug.grantor.all_scores[].candidate` | str | `"State of Texas"` |
| `.resolved.runsheet_alignment.debug.grantor.all_scores[].score` | float | `0.14814814814814814` |
| `.resolved.runsheet_alignment.debug.grantor.l1_name` | str | `"B. R. W. Bill"` |
| `.resolved.runsheet_alignment.debug.grantor.rs_name` | str | `"State of Texas"` |
| `.resolved.runsheet_alignment.debug.grantor.score` | float | `0.14814814814814814` |
| `.resolved.runsheet_alignment.discrepancies` | array | `[1 items]` |
| `.resolved.runsheet_alignment.discrepancies[].extracted` | str *(PATENT only)* | `"B. R. W. Bill"` |
| `.resolved.runsheet_alignment.discrepancies[].role` | str *(PATENT only)* | `"grantor"` |
| `.resolved.runsheet_alignment.discrepancies[].runsheet` | str *(PATENT only)* | `"State of Texas"` |
| `.resolved.runsheet_alignment.discrepancies[].score` | float *(PATENT only)* | `0.14814814814814814` |
| `.resolved.runsheet_alignment.grantee_best_score` | float | `0.9411764705882352` |
| `.resolved.runsheet_alignment.grantor_best_score` | float | `0.14814814814814814` |
| `.resolved.runsheet_alignment.has_discrepancy` | bool | `True` |
| `.resolved.validation_flags` | array | `[0 items]` |

## CONVEYANCE
**Endpoint:** `GET /documents/{doc_id}/conveyance`

| Path | Type | Example |
|------|------|---------|
| `.resolved._meta.correction_count` | int | `0` |
| `.resolved._meta.last_resolved_at` | str | `"2025-12-10T23:59:58.48810..."` |
| `.resolved.conveyance_summary_notes` | str | `"patent conveying fee simple"` |
| `.resolved.conveyance_summary_notes_provenance.source` | str | `"l1_stored"` |
| `.resolved.conveys_fee` | bool | `True` |
| `.resolved.conveys_fee_provenance.source` | str | `"l1_stored"` |
| `.resolved.doc_category_normalized` | null | `"DEED"` |
| `.resolved.doc_category_source` | null | `"runsheet"` |
| `.resolved.grantee_canonical` | null | - |
| `.resolved.grantor_canonical` | null | - |
| `.resolved.lease_terms` | null | - |
| `.resolved.mineral_rights` | null | - |
| `.resolved.primary_term_end_date` | null | - |
| `.resolved.primary_term_years` | null | - |
| `.resolved.royalty_rate` | null | - |
| `.resolved.summary_notes` | null | - |
| `.resolved.validation_flags` | array | `[0 items]` |

## LAND
**Endpoint:** `GET /documents/{doc_id}/land`

| Path | Type | Example |
|------|------|---------|
| `.resolved._meta.correction_count` | int | `0` |
| `.resolved._meta.last_resolved_at` | str | `"2026-01-08T01:13:56.53645..."` |
| `.resolved.canonical_tracts` | array | `[1 items]` |
| `.resolved.canonical_tracts[].acreage_declared` | null | `151.0` |
| `.resolved.canonical_tracts[].acreage_effective` | null | `151.0` |
| `.resolved.canonical_tracts[].acreage_phrase` | null | `"one hundred and fifty one..."` |
| `.resolved.canonical_tracts[].depth_limitations` | array | `[0 items]` |
| `.resolved.canonical_tracts[].depth_limitations_normalized` | array | `[0 items]` |
| `.resolved.canonical_tracts[].depth_limitations_raw` | array | `[0 items]` |
| `.resolved.canonical_tracts[].description_anchor` | str | `"In the name of the State ..."` |
| `.resolved.canonical_tracts[].description_snippet` | null | - |
| `.resolved.canonical_tracts[].exception_list` | array | `[0 items]` |
| `.resolved.canonical_tracts[].formation_limitations` | array | `[0 items]` |
| `.resolved.canonical_tracts[].formation_limitations_normalized` | array | `[0 items]` |
| `.resolved.canonical_tracts[].formation_limitations_raw` | array | `[0 items]` |
| `.resolved.canonical_tracts[].is_multi_survey` | bool | `False` |
| `.resolved.canonical_tracts[].land_description_role` | str | `"DEFINING"` |
| `.resolved.canonical_tracts[].linkage_clauses` | array | `[0 items]` |
| `.resolved.canonical_tracts[].linkage_clauses[].text` | str *(DEED only)* | `"a part of Andrew S. Nicho..."` |
| `.resolved.canonical_tracts[].linkage_clauses[].type` | str *(DEED only)* | `"part_of"` |
| `.resolved.canonical_tracts[].parent_tract_acreage` | null | `396.0` |
| `.resolved.canonical_tracts[].parent_tract_label` | null | `"Andrew S. Nichols land"` |
| `.resolved.canonical_tracts[].parent_tract_name` | null | - |
| `.resolved.canonical_tracts[].parent_tract_raw_text` | null | `"a part of Andrew S. Nicho..."` |
| `.resolved.canonical_tracts[].parent_tract_reference` | null | - |
| `.resolved.canonical_tracts[].parent_tract_type` | null | `"survey"` |
| `.resolved.canonical_tracts[].parentage_type` | str | `"unknown"` |
| `.resolved.canonical_tracts[].prior_tract_refs` | array | `[1 items]` |
| `.resolved.canonical_tracts[].prior_tract_refs[].text` | str *(PATENT only)* | `"by virtue of Scrip No. 27..."` |
| `.resolved.canonical_tracts[].prior_tract_refs[].type` | str *(PATENT only)* | `"patent_reference"` |
| `.resolved.canonical_tracts[].provenance.source` | str | `"l1_stored"` |
| `.resolved.canonical_tracts[].references` | array | `[0 items]` |
| `.resolved.canonical_tracts[].remainder_context` | null | - |
| `.resolved.canonical_tracts[].remainder_conveyed` | null | - |
| `.resolved.canonical_tracts[].source_type` | str | `"direct"` |
| `.resolved.canonical_tracts[].survey` | null | `"Andrew S. Nichols land"` |
| `.resolved.canonical_tracts[].survey_keys` | array | `[0 items]` |
| `.resolved.canonical_tracts[].survey_raw` | null | `"Andrew S. Nichols land"` |
| `.resolved.canonical_tracts[].tract_id` | str | `"tract_010b3382"` |
| `.resolved.canonical_tracts[].tract_identity_phrase` | str | `"those lands and rights in..."` |
| `.resolved.validation_flags` | array | `[0 items]` |

## DATES
**Endpoint:** `GET /documents/{doc_id}/dates`

| Path | Type | Example |
|------|------|---------|
| `.resolved._meta.correction_count` | int | `2` |
| `.resolved._meta.last_corrected_at` | str *(PATENT only)* | `"2025-12-12T20:49:59.59956..."` |
| `.resolved._meta.last_resolved_at` | str | `"2025-12-12T20:49:59.625427Z"` |
| `.resolved._provenance.dates[1].normalized.correction_id` | str *(PATENT only)* | - |
| `.resolved._provenance.dates[1].normalized.original_value` | str *(PATENT only)* | - |
| `.resolved._provenance.dates[1].normalized.source` | str *(PATENT only)* | - |
| `.resolved._provenance.governing_date.correction_id` | str *(PATENT only)* | `"cd55ad26-6a58-4efe-85d4-2..."` |
| `.resolved._provenance.governing_date.original_value` | str *(PATENT only)* | `"1859-11-15"` |
| `.resolved._provenance.governing_date.source` | str *(PATENT only)* | `"correction"` |
| `.resolved.dates` | array | `[2 items]` |
| `.resolved.dates[].confidence` | float | `0.9` |
| `.resolved.dates[].date_type` | str | `"filing"` |
| `.resolved.dates[].needs_review` | bool | `False` |
| `.resolved.dates[].normalized` | str | `"1833-10-28"` |
| `.resolved.dates[].provenance.from_field` | null | - |
| `.resolved.dates[].provenance.original_value` | null | - |
| `.resolved.dates[].provenance.override_id` | null | - |
| `.resolved.dates[].provenance.source` | str | `"l1_stored"` |
| `.resolved.dates[].raw_text` | str | `"Filed Oct. 28th 1833 at 8..."` |
| `.resolved.dates[].source_context` | str | `"State of Texas
Filed Oct...."` |
| `.resolved.governing_date` | str | `"1851-11-15"` |
| `.resolved.governing_date_confidence` | float | `0.9` |
| `.resolved.governing_date_provenance.from_field` | null | `"dates[1].normalized"` |
| `.resolved.governing_date_provenance.original_value` | str | `"1859-11-15"` |
| `.resolved.governing_date_provenance.override_id` | str | `"cd55ad26-6a58-4efe-85d4-2..."` |
| `.resolved.governing_date_provenance.source` | str | `"override"` |
| `.resolved.governing_date_source` | str | `"Done at the City of Austi..."` |
| `.resolved.governing_date_type` | str | `"execution"` |
| `.resolved.validation_flags` | array | `[0 items]` |

## DOC_TYPE
**Endpoint:** `GET /documents/{doc_id}/doc_type`

| Path | Type | Example |
|------|------|---------|
| `.resolved.confidence` | float | `0.95` |
| `.resolved.doc_category` | str | `"PATENT"` |
| `.resolved.runsheet_instrument_type` | str | `"Patent"` |
| `.resolved.runsheet_match` | bool | `True` |

---

## Cross-Endpoint Joins

### Title Engine effect → extraction data
```bash
# Get doc_id from effect
DOC_ID=$(curl -s ".../title-engine" | jq -r '.result.effects[0].doc_id')

# Fetch extraction data for that doc
curl -s ".../documents/$DOC_ID/conveyance" | jq '.resolved'
curl -s ".../documents/$DOC_ID/parties" | jq '.resolved.canonical_parties[]'
```

### Package documents → extraction for each
```bash
# List package docs
curl -s ".../packages/{pkg}/documents" | jq '.items[].id'
```

---

## L2 Clustering Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/packages/{id}/l2/parties` | GET | Party clusters across docs |
| `/packages/{id}/l2/tracts` | GET | Tract clusters across docs |

### Party Clusters jq
```bash
# Get all clusters
curl ".../l2/parties" | jq '.party_clusters[]'

# Find cluster containing a doc
curl ".../l2/parties" | jq '.party_clusters[] | select(.members[].doc_id | contains("abc123"))'
```
