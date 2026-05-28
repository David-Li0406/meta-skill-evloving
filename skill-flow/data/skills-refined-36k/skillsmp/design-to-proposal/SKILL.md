---
name: design-to-proposal
description: Create one or more OpenSpec proposals from an existing design, then run alignment + feasibility review.
---

# Design-to-Proposal

## Overview

Turn an existing, validated design document into one or more OpenSpec change proposals.

This skill is used by:
- `/brainstorm` (optional handoff after design completion)
- `/propose` (create proposals from existing designs)

## Inputs

- A design document path (typically `.workflow/designs/<feature-slug>/design.md`).

## Skills

Load the following skills:
- `memory`
- `openspec`
- `spawn-subagent`

## Process

1. Read memory context (project context, decisions, patterns, anti-patterns).
2. Read the design document.
3. Split assessment (required):
   - If the design contains multiple independent concerns, suggest splitting into multiple proposals.
   - Present the proposed split as a short list (proposal title + scope summary).
   - Ask the user to confirm the split or override it.
4. Draft proposal(s):
   - For each proposal, create `openspec/changes/<change-id>/` with `proposal.md`, `tasks.md`, and spec deltas.
   - Follow `openspec/AGENTS.md` exactly for formats and required files.
5. Validate timing (required):
   - Validate after drafting: `openspec validate <change-id> --strict --no-interactive`.
6. Alignment review:
   - Spawn the Alignment Reviewer subagent using `review-alignment.md`.
   - If output is `GAPS`, apply fixes to proposal/spec deltas/tasks as needed.
   - Re-validate after alignment fixes.
7. Feasibility review:
   - Spawn the Feasibility Reviewer subagent using `review-feasibility.md`.
   - If output is `CONCERNS`, refine `tasks.md` (sequencing/sizing/completeness) and proposal text.
   - Re-validate after feasibility fixes.
8. Update design document:
   - Ensure the design contains a `## OpenSpec Proposals` section.
   - Add an entry for each created proposal in this format:
   - `- \`<change-id>\` — <brief description>`
9. If any significant decisions were made, write them to memory before stopping (be selective).
10. STOP. The user triggers `/implement-change` separately.

## Review Bounds

- Run at most 2 cycles of Alignment Review and 2 cycles of Feasibility Review per proposal.
- If still failing after bounds, summarize the remaining gaps/concerns and STOP.
