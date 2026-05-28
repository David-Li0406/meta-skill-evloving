---
name: prd-skill
description: Normalize and refine an existing PRD (PDF/GDoc/MD text) into a structured PRD packet and a clean handoff for the User Story Mapper, especially when preparing downstream story mapping and architecture work.
metadata:
  short-description: Refine PRDs into normalized artifacts and story handoffs.
---

# PRD Skill (PRD Refiner + Handoff Generator)

## Purpose
Given an existing PRD (often messy, incomplete, or unstructured), produce:
1) A **Normalized PRD** in consistent Markdown sections
2) A **PRD Packet (JSON)** that conforms to `assets/prd_packet.schema.json`
3) A **User Story Mapper Handoff** embedded in the PRD Packet (and optionally as a Markdown section)

## Position in the Flow (Iterations)
This skill is the **entry-point** for the workflow: it produces the canonical PRD artifacts that downstream skills consume.
It must align with the User Story and Architecture skills by emitting a stable PRD packet and a handoff contract that map cleanly into story mapping and architecture briefs.

However, it may be invoked multiple times across iterations (either by the user or as part of an iterative refinement loop). Each run must:
- read any existing PRD artifacts (prior normalized PRD, prior PRD packet JSON, prior Q&A),
- reconcile changes (what is new/removed/modified),
- preserve stable IDs when possible (FR/NFR),
- update the handoff accordingly.

## Invocation Cases
- First pass: only raw PRD text exists.
- Refinement pass: raw PRD + previous PRD packet(s) exist.
- Repair pass: downstream skill reports missing/conflicting info; PRD skill re-runs to patch the PRD packet and re-issue handoff.

## Core Behavior: Ask Clarifying Questions When Uncertain
This skill must actively identify uncertainty and ask the user targeted questions whenever:
- a requirement cannot be made testable without guessing,
- a policy/behavior choice exists (e.g., retries vs fail-fast, partial results),
- the PRD contains ambiguity or conflicting statements,
- a field is missing that materially affects downstream design.

Questions must be:
- specific (not generic “tell me more”),
- grouped (max ~10 per iteration),
- prioritized by impact on downstream mapping and implementation.

When asking, provide 2–3 proposed options with **pros/cons** for each and ask the user to pick or refine an option.

The skill must still produce usable outputs in the same run by marking TBDs, **but it should explicitly ask the questions** instead of silently guessing.

## When to Use
Use when the user provides (or references) a PRD and asks to:
- refine it / make it clearer
- make it “agent-ready”
- prepare a handoff for user stories
- convert a PRD into a structured schema / markdown

## Non-Goals
This skill does **not**:
- define architecture, system design, or technology choices
- create UI/UX designs or wireframes
- write implementation-ready technical specs beyond PRD-level requirements
- prioritize a delivery roadmap beyond rough MVP vs later slice hints
- replace the downstream User Story Mapper, Architecture, or Tech Spec skills

## Inputs
- `raw_prd_text` (required): pasted text extracted from PDF/GDoc/MD or a summarized PRD.
- `optional_context` (optional): product constraints, team conventions, target platforms, deadlines, etc.
- Optional upstream artifacts (if available): prior normalized PRD, architecture notes, existing user stories.
- prior_artifacts (optional): previous normalized PRD markdown, previous PRD packet JSON, prior Q&A answers, downstream feedback.


## Outputs
### A) Normalized PRD Markdown
A Markdown document with these top-level headings (always output, even if some sections are TBD):
1. Overview
2. Problem
3. Users & Personas
4. Goals & Success Metrics
5. Scope (In / Out)
6. Assumptions & Constraints
7. User Journeys / Key Flows
8. Requirements
   - Functional Requirements (FR-###)
   - Non-Functional Requirements (NFR-###)
9. Edge Cases & Error States
10. Dependencies
11. Risks
12. Open Questions (TBDs)
13. User Story Mapper Handoff (summary)

### B) PRD Packet JSON
Emit JSON that validates against `assets/prd_packet.schema.json`, including:
- `tbd.missing_fields`
- `tbd.assumptions_made`
- `tbd.questions` (always present; empty list allowed)
- `handoff_user_story_mapper` (the User Story Mapper contract embedded inside the PRD packet)

### C) Handoff Contract for User Story Mapper
Provide a contract that downstream User Story Mapper should consume:
- `actors`: list of actors (personas/roles) with goals captured in the normalized PRD
- `epics`: grouped by journey/goal with stable IDs
- `stories`: candidate stories with `as_a`, `i_want`, `so_that`, priority, and acceptance criteria if available
- `linkage.story_to_requirements`: story → FR/NFR IDs for traceability
- `release_slices`: MVP vs later (if inferable, otherwise TBD)
- `open_questions`: unanswered items that could block story mapping
This contract must be embedded at `prd_packet_json.handoff_user_story_mapper` and may optionally be summarized in the Markdown output.

### D) Flow Alignment Notes (Required)
Include a short note in the normalized PRD (User Story Mapper Handoff section) that:
- the User Story skill **must** consume `docs/prd.packet.json` and the embedded `handoff_user_story_mapper`,
- the Architecture skill **must** consume `docs/prd.normalized.md`, `docs/prd.packet.json`, and `docs/story-map.json` once generated.

### Artifact Locations & Naming
When writing files to a repo, ensure they live under a `docs/` directory. If it does not exist, create it.
- `docs/prd.normalized.md` (Normalized PRD Markdown)
- `docs/prd.packet.json` (PRD Packet JSON with `handoff_user_story_mapper`)

## Procedure
1. **Ingest & Triage**
   - Identify: product, users, goals, scope, key flows, requirements, constraints.
   - Detect missing/contradictory info.

2. **Normalize Structure**
   - Rebuild the PRD into the standard Markdown section set.
   - Keep phrasing crisp and testable where possible.
   - Prefer concise bullet lists over long paragraphs to reduce verbosity and make downstream story mapping deterministic; only include narrative where it adds necessary context.
   - Preserve any **explicit lists** provided by the user (e.g., mandatory sources, required URLs, named vendors, or fixed constraints) **verbatim**. Do not paraphrase, re-label, or compress these items into broader category names.

3. **Requirements Extraction**
   - Convert vague statements into explicit requirements.
   - Assign IDs:
     - FR-001, FR-002… for functional
     - NFR-001… for non-functional
   - Add acceptance criteria when possible.
   - If acceptance criteria cannot be derived, mark as TBD and add a precise question.
   - If acceptance criteria cannot be derived without guessing, mark as TBD AND generate a clarifying question.

4. **Quality Checks**
   - Requirements should be: unambiguous, testable/verifiable where possible.
   - Flag anything that is:
     - ambiguous (“fast”, “easy”, “secure” with no measure)
     - missing actors/roles
     - missing success metrics
     - missing error-handling expectations
   - For any ambiguous term (“fast”, “secure”, “easy”), do BOTH:
     - flag it as ambiguous
     - ask a clarifying question to make it measurable/testable

5. **Generate User Story Mapper Handoff**
   - Provide:
     - actors (personas/roles)
     - epics (grouped by journey/goal)
     - candidate stories (as a starting point)
     - acceptance criteria link-back to FR/NFR IDs
     - release slices (MVP vs later), if inferable

6. **Standalone Fallback Rules**
   If the PRD lacks critical info, do not stall. Instead:
   - Create a minimal best-effort draft with clearly labeled:
     - `tbd` fields
     - `assumptions_made`
     - `open_questions`
   - Prefer asking **targeted** questions (not generic ones).
   - Keep the handoff usable even if incomplete.

7. **Sync With Downstream Feedback**
   - If the User Story or Architecture skills identify missing requirements, acceptance criteria, or conflicts, re-run this skill to:
     - update `docs/prd.packet.json` (`tbd.questions`, `tbd.missing_fields`, `tbd.assumptions_made`),
     - update `docs/prd.normalized.md` to reflect resolved clarifications,
     - preserve stable FR/NFR IDs and any explicit user-provided lists verbatim.

## Failure Modes & What To Do
When proposing resolutions or assumptions, include 2–3 options with pros/cons and ask the user to choose.
- **PRD is too high-level:** produce a normalized PRD + a list of “precision questions” needed to make it implementable.
- **PRD conflicts with itself:** list conflicts explicitly and propose 1–2 plausible resolutions as options.
- **Missing user personas:** infer minimal actors (e.g., Admin/User/Guest) and mark as assumptions.

## Output Formatting Rules
- Always output:
  1) Normalized PRD Markdown
  2) PRD Packet JSON (separate fenced block)
- In the JSON, include `confidence` per section (0–1) if uncertain.
- Keep IDs stable and consistent across outputs.

## Example Prompt That Should Trigger This Skill
“Here’s my PRD from Google Docs. Please refine it and generate the best handoff for the user story mapper.”
