---
name: architecture-skill
description: Translate PRD + story map artifacts into a high-level system architecture brief, component boundaries, interfaces, data flows, and designer-ready handoffs (frontend, backend, data, agentic). Use when moving from PRD/story outputs to architecture planning without detailed implementation.
metadata:
  short-description: Convert PRD/story maps into architecture briefs and handoffs.
---

# Architecture Skill

## Purpose
Produce a high-level architecture package that bridges PRD/story artifacts to designer-ready handoffs. Preserve traceability to FR/NFR and story IDs, avoid implementation detail, and surface uncertainty with targeted questions instead of guessing. When uncertainty requires a decision, propose options with pros/cons so the user can confirm quickly.

## Position in the Flow (Boundary)
This skill sits **after** PRD and User Story skills and **before** designer-specific technical specs. Do not pick frameworks, SDKs, database engines, or UI/UX details unless explicitly specified in input artifacts or optional context.

## Inputs
Use artifacts from `docs/` as authoritative inputs:
- `docs/prd.normalized.md`
- `docs/prd.packet.json` (authoritative FR/NFR IDs and handoff contract)
- `docs/story-map.json`
- `docs/story-map.summary.md`
- `optional_context` (stack constraints, target platforms, existing systems)

If any required artifact is missing, ask targeted questions immediately and proceed with placeholders labeled TBD.
When asking, include 2–3 possible approaches with pros/cons and ask the user to choose or clarify.

## Outputs
Always write under `docs/`:

### A) Architecture Brief (Markdown)
`docs/architecture.brief.md` with these headings:
1. Overview & Goals
2. System Context (actors + external systems)
3. Component Boundaries
4. Key Data Flows (mapped to epics/stories)
5. Interface Map (API/event/UI boundary contracts)
6. NFR Mapping (performance/security/reliability)
7. Risks & Mitigations
8. Assumptions & Open Questions
9. Designer Handoff Summary

### B) Architecture Packet (JSON) — Authoritative
`docs/architecture.packet.json` with stable structure and traceability:
- `meta`: skill_name, version, generated_at, source_artifacts
- `components[]`: id, purpose, responsibilities, dependencies
- `interfaces[]`: type, direction, inputs/outputs, linked stories/FR/NFR
- `data_flows[]`: source → target, trigger, linked story IDs
- `nfr_mapping[]`: NFR ID → architectural response
- `traceability`: story IDs ↔ FR/NFR IDs ↔ components
- `handoff_designers`: `frontend`, `backend`, `data`, `agentic`
- `agentic_architecture`: `enabled`, `orchestration`, `agents`, `memory`, `tools`, `flows`, `frameworks`
- `tbd.questions[]`, `assumptions_made[]`, `confidence[]`

### C) Designer Handoff Markdown (Derived)
Derived from `architecture.packet.json` (do not diverge):
- `docs/architecture.handoff.frontend.md`
- `docs/architecture.handoff.backend.md`
- `docs/architecture.handoff.data.md`
- `docs/architecture.handoff.agentic.md` (only if agentic_architecture.enabled = true)

### Upstream Sync Expectations (Required)
The Architecture skill must keep upstream artifacts aligned by:
- consuming `docs/prd.packet.json` and `docs/story-map.json` as authoritative for IDs and traceability,
- pushing gaps or conflicts back into those artifacts when they affect flow integrity or requirement completeness.

## Procedure
1. **Ingest artifacts** from `docs/`. If missing, ask targeted questions and proceed with TBD placeholders.
2. **Preserve explicit lists verbatim** (personas, epics, release slices, named constraints).
3. **Define system context**: actors, external systems, boundaries.
4. **Partition components**: UI/FE, API/backend, data layer, external services. Keep at architecture level.
5. **Map flows to components**: for each key user flow, define data flows and interfaces.
6. **Map NFRs** to architectural responses; do not assign implementation choices unless specified.
7. **Agentic architecture (if applicable)**:
   - Set `agentic_architecture.enabled` to true only when inputs mention agents, orchestration, tools, or memory.
   - Define roles, orchestration, memory boundaries, tool categories, and flow sequencing.
   - Do not choose frameworks/SDKs unless explicitly provided; list as TBD otherwise.
8. **Emit outputs**: JSON first (authoritative), then Markdown derived summaries.

## Updating Upstream Artifacts (PRD / Story Map)
Update upstream artifacts **only when required** to preserve traceability:
- If architecture uncovers missing requirements or acceptance criteria, update:
  - `docs/prd.packet.json` → `tbd.questions`, `tbd.missing_fields`, or `open_questions`
- If architecture introduces new story mapping needs (e.g., missing flow step), update:
  - `docs/story-map.json` → `ambiguities[]` or `unmapped_inputs[]`
Keep IDs stable and avoid paraphrasing user-provided lists.

## End-to-End Flow Compatibility
This skill must remain compatible with the preceding PRD and User Story skills by ensuring:
- `source_artifacts` in `docs/architecture.packet.json` references the exact PRD and story map files consumed,
- traceability links stay intact (story IDs ↔ FR/NFR IDs ↔ components/interfaces),
- any corrections are fed back upstream (PRD packet or story map) so the flow can be rerun deterministically.

## Backend ↔ Agentic Handoff Sync
Ensure backend and agentic handoffs stay aligned:
1. **Shared boundary summary**: include a short “shared responsibilities” section in both handoffs.
2. **Interface sync**: list any API/event contracts that cross backend ↔ agentic boundaries in both handoffs.
3. **Change propagation**: if an agentic change affects backend data flows or NFRs, update both handoff sections and the JSON traceability.
4. **Single source of truth**: JSON is authoritative; Markdown handoffs are derived.

## Failure Modes & Required Questions
- Missing artifacts → ask for missing docs immediately.
- Ambiguous flows → ask for entry points and expected system responses.
- Conflicting IDs → preserve inputs and ask which ID is canonical.
- Unclear NFR expectations → ask for measurable targets.
- Unclear agentic scope → ask whether agents are in scope and their primary responsibilities.
When any question has multiple plausible directions, propose 2–3 options with pros/cons to speed up user confirmation.
