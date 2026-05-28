# PDF-RAG API Reference

*Auto-generated from OpenAPI spec. See SKILL.md for cheat sheet and gotchas.*

## Endpoint Details

### GET /api/documents/{document_id}/parties

Get Document Parties

**Query Parameters:**
- `debug`: boolean [default: False] - Include full extraction data (L0, normalized, extraction_context)

**Response:** `PartiesExtractionResponse`
```
.resolved: PartiesResolved | null
  .canonical_parties[]: CanonicalPartyResolved
    .party_id: string
    .canonical_name: string
    .role: "grantor" | "grantee" | "lessor" | "lessee"
    .entity_type: "individual" | "company" | "unknown"
    .raw_name: string
    .spouse_party_id: string | null
    .household_id: string | null
    .confidence: number
    .capacity: string | null
    .capacity_principal: string | null
    .capacity_principal_type: string | null
    .fiduciary_cohort_id: string | null
    .fiduciary_of_party_id: string | null
    .is_synthesized: boolean
    .provenance: PartyProvenance | null
      .source: string
      .original_value: string | null
      .override_id: string | null
  .households: array | null
  .validation_flags: array | null
  .runsheet_alignment: object | null
.metadata: ExtractionMetadata | null
  .current_run: CurrentRunMetadata | null
  ...
```

### GET /api/documents/{document_id}/dates

Get Document Dates

**Query Parameters:**
- `debug`: boolean [default: False] - Include full extraction data (L0, normalized, extraction_context)

**Response:** `DatesExtractionResponse`
```
.resolved: DatesResolved | null
  .dates[]: ExtractedDate
    .date_type: "execution" | "acknowledgment" | "filing" | "effective"
    .raw_text: string
    .normalized: string | null
    .confidence: number
    .needs_review: boolean
    .source_context: string | null
    .provenance: DateProvenance | null
      .source: string
      .from_field: string | null
      .original_value: string | null
      .override_id: string | null
  .governing_date: string | null
  .governing_date_type: string | null
  .governing_date_provenance: DateProvenance | null
    .source: string
    .from_field: string | null
    .original_value: string | null
    .override_id: string | null
.metadata: ExtractionMetadata | null
  .current_run: CurrentRunMetadata | null
    .job_id: string | null
    .calls[]: LLMCallDetail
      .pass_name: string | null
  ...
```

### GET /api/documents/{document_id}/land

Get Document Land

**Query Parameters:**
- `debug`: boolean [default: False] - Include full extraction data (L0, normalized, extraction_context)

**Response:** `LandExtractionResponse`
```
.resolved: LandResolved | null
  .canonical_tracts[]: CanonicalTract
    .tract_id: string | null
    .tract_identity_phrase: string | null
    .survey: string | null
    .survey_raw: string | null
    .survey_keys[]: string[]
    .is_multi_survey: boolean
    .parentage_type: "all" | "part" | "remainder" | "unknown"
    .parent_tract_name: string | null
    .parent_tract_type: string | null
    .parent_tract_label: string | null
    .parent_tract_raw_text: string | null
    .acreage_declared: number | null
    .acreage_effective: number | null
    .acreage_phrase: string | null
    .depth_limitations[]: string[]
    .depth_limitations_raw[]: string[]
    .depth_limitations_normalized[]: object[]
    .formation_limitations[]: string[]
    .formation_limitations_raw[]: string[]
    .formation_limitations_normalized[]: string[]
    .linkage_clauses[]: object[]
    .prior_tract_refs[]: object[]
    .remainder_context: object | null
  ...
```

### GET /api/documents/{document_id}/conveyance

Get Document Conveyance

**Query Parameters:**
- `debug`: boolean [default: False] - Include full extraction data (L0, normalized, extraction_context)

**Response:** `ConveyanceExtractionResponse`
```
.resolved: ConveyanceResolved | null
  .conveys_fee: boolean
  .conveys_fee_provenance: FieldProvenance | null
    .source: string
  .conveyance_summary_notes: string | null
  .conveyance_summary_notes_provenance: FieldProvenance | null
    .source: string
  .summary_notes: string | null
  .validation_flags[]: string | object[]
  .doc_category_source: string | null
  .doc_category_normalized: string | null
  .grantor_canonical: string | null
  .grantee_canonical: string | null
  .primary_term_years: integer | null
  .royalty_rate: string | null
  .primary_term_end_date: string | null
  .mineral_rights: MineralRightsResolved | null
    .interest_kind: string | null
    .is_npmi: boolean | null
    .is_term_mineral: boolean | null
    .executive_rights: string
    .fraction_raw: string | null
    .fraction_scope_raw: string | null
    .interest_kind_provenance: FieldProvenance | null
      .source: string
  ...
```

### GET /api/documents/{document_id}/doc_type

Get Document Doc Type

**Query Parameters:**
- `debug`: boolean [default: False] - Include full extraction data (L0, normalized, extraction_context)

**Response:** `ClassificationExtractionResponse`
```
.resolved: ClassificationResolved | null
  .doc_category: string
  .confidence: number
  .runsheet_match: boolean | null
  .runsheet_instrument_type: string | null
.metadata: ExtractionMetadata | null
  .current_run: CurrentRunMetadata | null
    .job_id: string | null
    .calls[]: LLMCallDetail
      .pass_name: string | null
      .model: string
      .cost_usd: number
      .prompt_tokens: integer
      .completion_tokens: integer
      .total_tokens: integer
      .created_at: string | null
    .total_cost_usd: number
    .total_tokens: integer
  .history: HistoryMetadata
    .call_count: integer
    .total_cost_usd: number
  .calls: array | null
  .total_cost_usd: number | null
  .total_tokens: integer | null
.extracted_at: string | null
  ...
```

### GET /api/documents/{document_id}/extractions

*Endpoint not found in spec*

### GET /api/packages/{package_id}

Get Package

**Query Parameters:**
- `include`: string | null - Comma-separated fields to include (e.g., 'meta')

**Response:** `PackageDetailResponse`
```
.id: string
.name: string
.description: string | null
.meta: object | null
.document_count: integer
.documents[]: DocumentResponse
  .file_name: string
  .file_path: string
  .file_type: string
  .page_count: integer | null
  .id: string
  .file_hash: string
  .status: DocumentStatus | null
  .created_at: string
  .updated_at: string
  .doc_category: string | null
  .deleted_at: string | null
  .deleted_by: string | null
  .deleted_reason: string | null
  .pipeline_stages: object | null
  .sequence_number: integer | null
  .volume_page_key: string | null
  .recording_date: string | null
  .packages: array | null
.created_at: string
  ...
```

### GET /api/packages/{package_id}/chain-analysis

*Endpoint not found in spec*

### POST /api/packages/{package_id}/chain-analysis

*Endpoint not found in spec*

### GET /api/packages/{package_id}/l2/parties

Get L2 party clustering results

**Response:** `L2PartiesResponse`
```
.package_id: string
.created_at: string
.doc_count: integer
.cluster_count: integer
.singleton_count: integer
.multi_member_clusters: integer
.party_clusters[]: PartyCluster
  .cluster_id: string
  .canonical_name: string
  .confidence: number
  .members[]: ClusterMember
    .doc_id: string
    .party_id: string
    .canonical_name: string
    .role: string
    .confidence: number
    .entity_type: string | null
    .capacity: string | null
    .is_synthesized: boolean
    .fiduciary_of_party_id: string | null
  .rationale[]: string[]
  .ambiguous: boolean
  .override: object | null
.unmatched_parties[]: UnmatchedParty
  .doc_id: string
  ...
```

### POST /api/packages/{package_id}/l2/parties

Run L2 party clustering on package documents

**Query Parameters:**
- `limit`: integer | null

**Request Body:** `L2PartiesRequest`
```
.doc_ids: array | null
.options: object | null
```

**Response:** `L2PartiesResponse`
```
.package_id: string
.created_at: string
.doc_count: integer
.cluster_count: integer
.singleton_count: integer
.multi_member_clusters: integer
.party_clusters[]: PartyCluster
  .cluster_id: string
  .canonical_name: string
  .confidence: number
  .members[]: ClusterMember
    .doc_id: string
    .party_id: string
    .canonical_name: string
    .role: string
    .confidence: number
    .entity_type: string | null
    .capacity: string | null
    .is_synthesized: boolean
    .fiduciary_of_party_id: string | null
  .rationale[]: string[]
  .ambiguous: boolean
  .override: object | null
.unmatched_parties[]: UnmatchedParty
  .doc_id: string
  ...
```

### GET /api/packages/{package_id}/l2/tracts

Get L2 tract clustering results

**Response:** `L2TractsResponse`
```
.package_id: string
.created_at: string
.doc_count: integer
.cluster_count: integer
.singleton_count: integer
.multi_member_clusters: integer
.tract_clusters[]: TractCluster
  .cluster_id: string
  .canonical_description: string
  .confidence: number
  .members[]: TractClusterMember
    .doc_id: string
    .tract_id: string
    .tract_slice_id: string
    .tract_identity_phrase: string
    .parent_tract_label: string | null
    .parentage_type: string
    .acreage_declared: number | null
    .confidence: number
    .depth_limitations_normalized[]: object[]
    .formation_limitations_normalized[]: string[]
    .candidate_parents[]: CandidateParent
      .tract_id: string
      .doc_id: string
      .similarity: number
  ...
```

### POST /api/packages/{package_id}/l2/tracts

Run L2 tract clustering on package documents

**Query Parameters:**
- `limit`: integer | null

**Request Body:** `L2TractsRequest`
```
.doc_ids: array | null
.options: object | null
```

**Response:** `L2TractsResponse`
```
.package_id: string
.created_at: string
.doc_count: integer
.cluster_count: integer
.singleton_count: integer
.multi_member_clusters: integer
.tract_clusters[]: TractCluster
  .cluster_id: string
  .canonical_description: string
  .confidence: number
  .members[]: TractClusterMember
    .doc_id: string
    .tract_id: string
    .tract_slice_id: string
    .tract_identity_phrase: string
    .parent_tract_label: string | null
    .parentage_type: string
    .acreage_declared: number | null
    .confidence: number
    .depth_limitations_normalized[]: object[]
    .formation_limitations_normalized[]: string[]
    .candidate_parents[]: CandidateParent
      .tract_id: string
      .doc_id: string
      .similarity: number
  ...
```

### GET /api/packages/{package_id}/estate-graph

Get stored estate graph

**Query Parameters:**
- `version`: string [default: 1.1]

**Response:** `EstateGraphResponse`
```
.id: string
.package_id: string
.created_at: string
.version: string
.dag: EstateDAG
  .nodes[]: EstateNode
    .estate_id: string
    .estate_key: string
    .estate_type: "fee" | "surface" | "mineral" | "leasehold" | "royalty" | "overriding_royalty"
    .tract_id: string
    .l1_tract_ids[]: string[]
    .tract_description: string | null
    .tract_survey: string | null
    .tract_acreage: number | null
    .acreage_declared: number | null
    .canonical_tract_key: string | null
    .owner_party_id: string
    .owner_display_name: string | null
    .fractional_interest: string
    .fractional_interest_raw: string | null
    .interest_kind: string | null
    .fraction_numerator: integer | null
    .fraction_denominator: integer | null
    .interest_division_type: string | null
    .interest_of: InterestOfRef | null
  ...
```

### POST /api/packages/{package_id}/estate-graph

Build estate-centric DAG (V2)

**Request Body:** `EstateGraphRequest`
```
.doc_ids: array | null
.version: string
.explore_all_layers: boolean
.options: object | null
```

**Response:** `EstateGraphResponse`
```
.id: string
.package_id: string
.created_at: string
.version: string
.dag: EstateDAG
  .nodes[]: EstateNode
    .estate_id: string
    .estate_key: string
    .estate_type: "fee" | "surface" | "mineral" | "leasehold" | "royalty" | "overriding_royalty"
    .tract_id: string
    .l1_tract_ids[]: string[]
    .tract_description: string | null
    .tract_survey: string | null
    .tract_acreage: number | null
    .acreage_declared: number | null
    .canonical_tract_key: string | null
    .owner_party_id: string
    .owner_display_name: string | null
    .fractional_interest: string
    .fractional_interest_raw: string | null
    .interest_kind: string | null
    .fraction_numerator: integer | null
    .fraction_denominator: integer | null
    .interest_division_type: string | null
    .interest_of: InterestOfRef | null
  ...
```

### GET /api/packages/{package_id}/estate-graph/gaps

Query estate graph gaps with filters

**Query Parameters:**
- `doc_id`: string | null
- `tract_id`: string | null
- `gap_reason`: string | null
- `estate_type`: string | null

**Response:** `GapQueryResponse`
```
.gaps[]: EstateGap
  .gap_id: string
  .tract_id: string
  .estate_type: "fee" | "surface" | "mineral" | "leasehold" | "royalty" | "overriding_royalty"
  .gap_type: "MISSING_PARENT" | "AMBIGUOUS_PARENTS" | "PARTY_MISMATCH"
  .orphan_node_id: string | null
  .candidate_parent_ids[]: string[]
  .message: string
  .match_trace: MatchTrace | null
    .trace_id: string
    .doc_id: string
    .source_engine: "operative" | "exploratory" | "exploratory_signals"
    .tract_cluster_id: string
    .tract_slice_id: string | null
    .estate_type: string
    .grantor_names[]: string[]
    .grantor_cluster_ids[]: string[]
    .conveyance_date: string | null
    .layer_traces[]: LayerTrace
      .layer: integer
      .layer_name: string
      .searched: {[key]: any}
      .candidates_found: integer
      .candidates[]: CandidateTrace
        .estate_id: string
  ...
```

### GET /api/packages/{package_id}/estate-graph/diagnostics

Get estate graph diagnostics for systemic issue detection

**Response:** `EstateGraphDiagnostics`
```
.package_id: string
.generated_at: string
.summary: EstateGraphSummary
  .total_estates: integer
  .fee_estates: integer
  .surface_estates: integer
  .mineral_estates: integer
  .leasehold_estates: integer
  .royalty_estates: integer
  .orri_estates: integer
  .total_conveyances: integer
  .total_severances: integer
  .total_lease_grants: integer
  .total_burdens: integer
  .total_gaps: integer
  .unique_tracts: integer
  .unique_owners: integer
.gap_patterns[]: GapPattern
  .pattern_key: string
  .count: integer
  .estate_type: string
  .gap_reason: string
  .example_grantors[]: string[]
  .suggested_investigation: string
.doc_category_outcomes[]: DocCategoryOutcome
  ...
```

### GET /api/documents

List documents with pagination

**Query Parameters:**
- `limit`: integer [default: 50] - Number of items per page
- `offset`: integer [default: 0] - Number of items to skip
- `order_by`: string [default: created_at:desc] - Sort field and direction (e.g., 'created_at:desc', 'file_name:asc')
- `status`: DocumentStatus | null - Filter by document status
- `file_type`: string | null - Filter by file type (pdf, docx, xlsx)
- `package_id`: string | null - Filter by package membership
- `has_stage`: StageName | null - Filter by completed stage
- `missing_stage`: StageName | null - Filter by missing stage
- `min_pages`: integer | null - Minimum page count (inclusive)
- `max_pages`: integer | null - Maximum page count (inclusive)
- `include_deleted`: boolean [default: False] - Include soft-deleted documents (default: false)

**Response:** `PaginatedDocumentsResponse`
```
.total: integer
.items[]: DocumentResponse
  .file_name: string
  .file_path: string
  .file_type: string
  .page_count: integer | null
  .id: string
  .file_hash: string
  .status: DocumentStatus | null
  .created_at: string
  .updated_at: string
  .doc_category: string | null
  .deleted_at: string | null
  .deleted_by: string | null
  .deleted_reason: string | null
  .pipeline_stages: object | null
  .sequence_number: integer | null
  .volume_page_key: string | null
  .recording_date: string | null
  .packages: array | null
.limit: integer
.offset: integer
.has_more: boolean
```

### GET /api/documents/{document_id}

Get Document

**Query Parameters:**
- `include_deleted`: boolean [default: False] - Allow retrieving deleted documents (default: false)

**Response:** `DocumentResponse`
```
.file_name: string
.file_path: string
.file_type: string
.page_count: integer | null
.id: string
.file_hash: string
.status: DocumentStatus | null
.created_at: string
.updated_at: string
.doc_category: string | null
.deleted_at: string | null
.deleted_by: string | null
.deleted_reason: string | null
.pipeline_stages: object | null
.sequence_number: integer | null
.volume_page_key: string | null
.recording_date: string | null
.packages: array | null
```

### GET /api/documents/{document_id}/stages

Get Document Stages

**Response:** `DocumentStagesResponse`
```
.document_id: string
.stages["<key>"]: StageInfo
  .stage: "markdown" | "segmentation" | "instrument_boundary_detection" | "runsheet" | "runtime_linking" | "assembly" | "extract_parties" | "extract_conveyance" | "extract_land_description" | "extract_dates" | "extract_document_classification" | "extract_land_v2"
  .status: "in_progress" | "completed" | "failed"
  .started_at: string | null
  .completed_at: string | null
  .metadata: object | null
  .error: string | null
```

### POST /api/process

Submit documents for processing

**Request Body:** `JobCreate`
```
.document_ids: array | null
.process_all_missing: boolean
.min_pages: integer | null
.max_pages: integer | null
.limit: integer | null
.stages[]: StageName
.priority: "low" | "normal" | "high"
.force: boolean
.dry_run: boolean
.enrich_only: boolean
```

**Response:** `BatchJobResponse | DryRunResponse`

### GET /api/jobs/{job_id}

Get Job


## All Endpoints Index

| Method | Path | jq hint |
|--------|------|---------|
| GET | `/` | ``.`` |
| GET | `/api/batches` | ``.`` |
| POST | `/api/batches` | ``.id`` |
| GET | `/api/batches/{batch_id}` | ``.id`` |
| DELETE | `/api/batches/{batch_id}` | ``.`` |
| POST | `/api/batches/{batch_id}/cancel` | ``.`` |
| POST | `/api/documents/llm_costs` | ``.`` |
| DELETE | `/api/documents/{document_id}` | ``.`` |
| GET | `/api/documents/{document_id}/chunks` | ``.`` |
| GET | `/api/documents/{document_id}/corrections` | ``.`` |
| POST | `/api/documents/{document_id}/corrections` | ``.id`` |
| DELETE | `/api/documents/{document_id}/corrections/{correction_id}` | ``.`` |
| GET | `/api/documents/{document_id}/instruments` | ``.`` |
| GET | `/api/documents/{document_id}/landv2` | ``.`` |
| GET | `/api/documents/{document_id}/llm_cost` | ``.`` |
| GET | `/api/documents/{document_id}/markdown` | ``.`` |
| GET | `/api/documents/{document_id}/ocr-metrics` | ``.`` |
| GET | `/api/documents/{document_id}/packages` | ``.`` |
| GET | `/api/documents/{document_id}/page_density` | ``.`` |
| GET | `/api/documents/{document_id}/pdf` | ``.`` |
| POST | `/api/documents/{document_id}/recover` | ``.packages[]`` |
| GET | `/api/documents/{document_id}/runsheet_link` | ``.`` |
| GET | `/api/documents/{document_id}/runtime_linking` | ``.`` |
| DELETE | `/api/documents/{document_id}/stages/{stage}` | ``.`` |
| GET | `/api/documents/{document_id}/{stage}/versions` | ``.`` |
| GET | `/api/jobs` | ``.`` |
| POST | `/api/jobs/{job_id}/cancel` | ``.id`` |
| GET | `/api/jobs/{job_id}/manifest` | ``.`` |
| POST | `/api/jobs/{job_id}/recover` | ``.`` |
| POST | `/api/monitoring/cleanup-dead-workers` | ``.`` |
| POST | `/api/monitoring/clear-bytecode-cache` | ``.`` |
| GET | `/api/monitoring/health` | ``.`` |
| POST | `/api/monitoring/kill-stale-workers` | ``.`` |
| POST | `/api/monitoring/recover-all` | ``.`` |
| POST | `/api/monitoring/recover-orphaned` | ``.`` |
| POST | `/api/monitoring/recover-stale` | ``.`` |
| POST | `/api/monitoring/recover-stale-stages` | ``.`` |
| GET | `/api/monitoring/scheduler` | ``.`` |
| GET | `/api/monitoring/snapshot` | ``.`` |
| GET | `/api/monitoring/snapshots/history` | ``.`` |
| GET | `/api/monitoring/stale-jobs` | ``.`` |
| GET | `/api/monitoring/workers` | ``.`` |
| DELETE | `/api/monitoring/workers/{worker_id}` | ``.`` |
| POST | `/api/monitoring/workers/{worker_id}/drain` | ``.`` |
| GET | `/api/packages` | ``.packages[]`` |
| POST | `/api/packages` | ``.id`` |
| PUT | `/api/packages/{package_id}` | ``.id`` |
| DELETE | `/api/packages/{package_id}` | ``.`` |
| GET | `/api/packages/{package_id}/assertions` | ``.`` |
| POST | `/api/packages/{package_id}/assertions` | ``.id`` |
| DELETE | `/api/packages/{package_id}/assertions/{assertion_id}` | ``.`` |
| POST | `/api/packages/{package_id}/assertions/{assertion_id}/restore` | ``.id`` |
| GET | `/api/packages/{package_id}/chain-settings` | ``.`` |
| PATCH | `/api/packages/{package_id}/chain-settings` | ``.`` |
| GET | `/api/packages/{package_id}/document-graph` | ``.`` |
| POST | `/api/packages/{package_id}/document-graph` | ``.`` |
| POST | `/api/packages/{package_id}/document-graph/multi` | ``.`` |
| POST | `/api/packages/{package_id}/documents` | ``.id`` |
| GET | `/api/packages/{package_id}/documents/{doc_id}/observations` | ``.`` |
| DELETE | `/api/packages/{package_id}/documents/{document_id}` | ``.`` |
| GET | `/api/packages/{package_id}/estate-graph/debug/compare` | ``.`` |
| GET | `/api/packages/{package_id}/estate-graph/debug/documents/{doc_id}` | ``.`` |
| GET | `/api/packages/{package_id}/estate-graph/debug/edges/{edge_id}` | ``.`` |
| GET | `/api/packages/{package_id}/estate-graph/debug/estates/{estate_id}` | ``.`` |
| GET | `/api/packages/{package_id}/estate-graph/debug/gap-state` | ``.`` |
| GET | `/api/packages/{package_id}/estate-graph/debug/gaps/{gap_id}` | ``.`` |
| GET | `/api/packages/{package_id}/estate-graph/debug/hypotheses` | ``.`` |
| GET | `/api/packages/{package_id}/estate-graph/debug/hypothesis` | ``.`` |
| GET | `/api/packages/{package_id}/estate-graph/debug/sequence/{seq_num}` | ``.`` |
| GET | `/api/packages/{package_id}/estate-graph/debug/slices` | ``.`` |
| GET | `/api/packages/{package_id}/estate-graph/debug/trace-keys` | ``.`` |
| GET | `/api/packages/{package_id}/estate-graph/{estate_id}/evidence` | ``.`` |
| GET | `/api/packages/{package_id}/observations` | ``.`` |
| GET | `/api/packages/{package_id}/observations/flagged` | ``.`` |
| GET | `/api/packages/{package_id}/title-chart` | ``.id`` |
| POST | `/api/packages/{package_id}/title-chart` | ``.id`` |
| GET | `/api/packages/{package_id}/title-chart/transactions/{transaction_id}` | ``.`` |
| GET | `/api/packages/{package_id}/title-engine` | ``.`` |
| POST | `/api/packages/{package_id}/title-engine` | ``.`` |
| GET | `/api/packages/{package_id}/title-engine/assertions` | ``.`` |
| GET | `/api/packages/{package_id}/title-engine/assumptions` | ``.`` |
| GET | `/api/packages/{package_id}/title-engine/burdens` | ``.`` |
| GET | `/api/packages/{package_id}/title-engine/effects` | ``.`` |
| GET | `/api/packages/{package_id}/title-engine/effects/{effect_id}` | ``.`` |
| GET | `/api/packages/{package_id}/title-engine/estates` | ``.`` |
| GET | `/api/packages/{package_id}/title-engine/gaps` | ``.`` |
| GET | `/api/packages/{package_id}/title-engine/instruments` | ``.`` |
| GET | `/api/packages/{package_id}/title-engine/interests` | ``.`` |
| GET | `/api/packages/{package_id}/title-engine/issues` | ``.`` |
| GET | `/api/packages/{package_id}/title-engine/ownerships` | ``.`` |
| GET | `/api/packages/{package_id}/title-engine/tract-contexts` | ``.`` |
| POST | `/api/upload` | ``.`` |
| GET | `/db-profile` | ``.`` |
| POST | `/db-profile/reset` | ``.`` |
| GET | `/health` | ``.`` |
| POST | `/internal/worker_stopped` | ``.`` |
| GET | `/stats` | ``.documents[]`` |

---
*For cheat sheet and common mistakes, see SKILL.md*