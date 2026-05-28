---
name: user-story-skill
description: Map PRD skill artifacts into user flows and a stable story map with traceability plus a human-readable summary. Use when converting PRD outputs into flow-oriented steps, user stories, release slices, and open questions while preserving IDs and explicit lists.
metadata:
  short-description: Turn PRD outputs into story maps and user flows.
---

# User Story Skill

## Purpose
Translate PRD skill artifacts into **flow-oriented user steps** and a **stable, machine-consumable story map** plus a human-readable summary. Preserve explicit user-provided lists verbatim, keep IDs stable, and surface ambiguities with targeted questions instead of guessing. When uncertain, propose options with pros/cons so the user can decide quickly. Enable downstream planning without making architecture or implementation decisions.

## Position in the Flow (Boundary)
Stay between PRD refinement and architecture/technical design. Do **not** decide components, services, APIs, data models, or infrastructure. Output structured flows, stories, and traceability that downstream architecture skills can consume. The architecture skill should be able to ingest the story map artifacts directly without additional transformation.

## Inputs
Expect **every artifact produced by the PRD skill** and use them as authoritative sources. Explain each input and how it is used:
- `normalized_prd_markdown` (required): produced by the PRD skill. Use it to read narrative context, journeys, and any explicit lists or constraints that must be preserved verbatim.
- `prd_packet_json` (required): produced by the PRD skill (valid against the PRD packet schema). Use it as the structured source of FR/NFR IDs, acceptance criteria, and embedded handoff data.
- `prd_handoff_contract` (required): produced by the PRD skill and located at `prd_packet_json.handoff_user_story_mapper`. Use it as the authoritative list of actors, epics, candidate stories, release slices, and open questions. This contract is embedded inside the PRD packet (not a separate file) unless explicitly emitted by the PRD skill as a standalone section.
- `optional_context` (optional): provided by the user or system. Use it to resolve ambiguities, add constraints, or clarify flow ordering.
- `prior_story_map` (optional): prior story map artifact. Use it to keep story IDs stable across iterations.

If any required artifact is missing or incomplete, **ask the user targeted questions immediately** and proceed with best-effort placeholders labeled as TBD (see Failure Modes).
When asking questions, offer 2–3 concrete options with pros/cons and ask which option should be used.

### Artifact Locations & Naming
When writing files to a repo, ensure they live under a `docs/` directory. If it does not exist, create it.
- `docs/story-map.json` (Story Map JSON)
- `docs/story-map.summary.md` (Story Map Summary)
- Update `docs/prd.packet.json` when story mapping changes require PRD updates.

### Downstream Handoff to Architecture (Required)
Ensure `docs/story-map.json` and `docs/story-map.summary.md` are complete and self-consistent so the Architecture skill can:
- map epics, flows, and stories to components,
- trace stories back to FR/NFR IDs from `docs/prd.packet.json`,
- identify open questions and TBDs without re-reading the raw PRD.

## Outputs
### A) Story Map JSON (machine-consumable)
Emit a deterministic JSON (or YAML) artifact with stable IDs and traceability:
- `meta`: `skill_name`, `version`, `source_contract_id`, `generated_at`
- `personas[]`: copied from PRD artifacts (prefer `handoff_user_story_mapper.actors`, otherwise `normalized_prd.users.personas`)
- `epics[]`: copied or mapped from PRD handoff
- `user_flows[]`: flow-oriented steps (entry point → actions → system responses) per persona/epic
- `story_map`: `persona → activities → steps → stories`
- `stories[]`: each story with a stable ID, story text, linked `fr_ids`/`nfr_ids`, and acceptance criteria
- `release_slices`: MVP vs later (verbatim if provided; inferred only when necessary and labeled)
- `traceability`: story links to epics, personas, FR/NFR IDs
- `ambiguities[]`: targeted questions with impact scope
- `unmapped_inputs[]`: PRD items that could not be mapped, with reason

### B) Story Map Summary (human-readable)
Provide a concise summary:
- Personas covered
- Flow highlights (where users start, key actions, system responses)
- Epics and story breakdown highlights
- MVP vs later coverage
- Ambiguities and targeted questions
- Unmapped PRD items

## Procedure
1. **Ingest PRD Artifacts**
   - Load `normalized_prd_markdown`, `prd_packet_json`, and `prd_handoff_contract`.
   - If any required artifact is missing or incomplete, **ask the user targeted questions immediately** and continue with placeholders labeled TBD.
   - Confirm the handoff contract is sourced from `prd_packet_json.handoff_user_story_mapper`; if missing, treat it as a blocking gap and request it.

2. **Preserve Verbatim Lists**
   - Copy any explicit lists from PRD skill artifacts verbatim (personas, epics, release slices, mandatory items, and explicitly named sources/sites). Do not collapse explicit lists into generic categories.
   - Do not reorder or paraphrase explicit user-provided lists.

3. **Define User Flows First**
   - For each persona and epic, define the user flow: entry point, user action(s), system response(s), and exit/next step.
   - If flows are already stated in the PRD artifacts, preserve them verbatim.
   - If flow steps are missing, **ask targeted questions** about starting page/state, user triggers, and expected system behavior.

4. **Construct the Story Map**
   - Map flows into `activities → steps → stories`.
   - If `handoff_user_story_mapper.stories` are already structured, preserve them verbatim; otherwise map from epics and journeys with minimal transformation.

5. **Maintain Stable IDs**
   - Keep any provided IDs unchanged.
   - If missing, generate deterministic IDs derived from normalized story text + linked FR/NFR IDs + persona.
   - If `prior_story_map` exists, reuse IDs from that artifact.

6. **Create Traceability Links**
   - Link stories to originating epic, persona, and FR/NFR IDs.
   - Record traceability in a dedicated section for auditing.

7. **Apply Release Slicing**
   - Preserve explicit MVP vs later slices verbatim.
   - If release slicing must be inferred, label it as inferred and **ask a targeted question** confirming the assumption.

8. **Detect Ambiguities and Gaps**
   - Identify missing acceptance criteria, unclear persona/story assignments, missing flow steps, or conflicting slices.
   - For each gap, **ask a targeted question** and mark the affected item as TBD.

9. **Emit Outputs**
   - Emit the machine-consumable artifact first, then the human-readable summary.
   - Ensure deterministic ordering of keys and stable IDs.

10. **Propagate Updates Back to PRD Artifacts**
    - If story mapping uncovers new requirements, acceptance criteria, or open questions, update `docs/prd.packet.json`:
      - Add new questions to `tbd.questions` or `normalized_prd.open_questions`.
      - Update `handoff_user_story_mapper` with the finalized story IDs and linkage.
      - Keep all existing IDs stable and avoid rewriting user-provided wording.
    - If updates materially change PRD content, note the change in `meta.change_summary`.

11. **Sync With Architecture Feedback**
    - If Architecture later reveals missing flows, unclear boundaries, or traceability gaps, update:
      - `docs/story-map.json` (`ambiguities[]`, `unmapped_inputs[]`, or missing flow steps),
      - `docs/prd.packet.json` (`tbd.questions` or acceptance criteria gaps),
      - while preserving stable IDs and verbatim lists.

## Failure Modes & Required Questions
For any failure mode, **ask the user targeted questions** that identify the missing or conflicting information and the impacted stories/epics.
Include 2–3 options with pros/cons for each decision point to speed up user confirmation.

- **Missing PRD artifacts:** Ask for the missing artifact(s) and proceed with placeholders marked TBD.
- **Missing personas/epics/stories:** Ask for the missing list(s) explicitly rather than inferring without confirmation.
- **Missing flow steps:** Ask where the user starts, what they click/do, and what the system should do next.
- **Conflicting or duplicated IDs:** Preserve input IDs, flag the conflict, and ask which ID should be canonical.
- **Ambiguous story mapping:** Ask which persona/epic each story should belong to.
- **Inconsistent release slicing:** Preserve explicit slices, flag conflicts, and ask which slice is authoritative.
- **Acceptance criteria gaps:** Ask for testable acceptance criteria rather than guessing.

## Output Formatting Rules
- **Machine Artifact Format:** JSON (preferred) or YAML with stable key ordering.
- **ID Stability:** Never rewrite provided IDs; only generate deterministic IDs when missing.
- **Verbatim Preservation:** Explicit lists from PRD artifacts must appear unchanged.
- **Ambiguities:** Use a structured `ambiguities[]` list with `question`, `reason`, `impact_scope`, `blocking`.
- **Summary:** Keep the summary short, scannable, and aligned to the machine artifact.

## Example Prompt That Should Trigger This Skill
“Use the PRD packet and handoff to produce user flows and a story map with stable IDs.”
