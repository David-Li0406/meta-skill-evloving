---
name: Skill Generator
description: Create complete Claude Skills from a short brief, with templates and checks.
version: 1.0.0
allowed-tools: [Read, Write, Glob]
---

## Overview
This Skill helps you rapidly author high‑quality Claude Skills from a short prompt. It converts a brief into a complete Skill folder structure that follows official guidelines, including correct YAML frontmatter, focused scope, clear instructions, examples, and optional resources/scripts. It enforces naming and description limits so Claude selects and loads generated Skills appropriately.

## When to Use
- Drafting a new Skill from a one‑to‑two paragraph brief
- Converting existing SOPs or playbooks into a Claude Skill
- Standardizing Skills across a team with consistent structure, language, and checks

## Inputs
- Working brief: purpose, audience, and the repeatable workflow this Skill will cover
- Triggers: when to apply the Skill; clear “in vs out of scope” boundaries
- Constraints: security, compliance, and privacy notes (no secrets)
- Optional resources: links/files to include as references
- Optional scripts: languages/dependencies if executable helpers are needed

## Outputs
- A new Skill folder named after the Skill
- Skill.md with valid YAML frontmatter and structured body
- Optional `resources/` files (templates, references, examples, checklists)
- Optional stub scripts and declared dependencies

## Guardrails and Rules
- Name: ≤ 64 chars; Description: ≤ 200 chars (succinct, specific triggers)
- Always start with YAML frontmatter containing `name` and `description`
- Keep one workflow per Skill; split multi‑workflow briefs into separate Skills
- Don’t hardcode secrets; list dependencies in frontmatter if scripts are included
- Prefer reference files under `resources/` for long or situational content
- Provide at least one concrete example input and output
- Include a short "When to Apply" section so Claude can load this Skill correctly

## Generation Steps (what to do when invoked)
1) Parse the brief and propose a clear Skill `name` (≤64 chars) and `description` (≤200 chars) that explicitly states when to use it.
2) Draft `Skill.md` using the structure in `resources/SKILL_TEMPLATE.md`:
   - Overview, When to Apply, Inputs, Outputs, Instructions for Claude, Examples, Testing Checklist, Security/Privacy.
3) Create `resources/` files if they increase clarity:
   - References (REFERENCE.md), CHECKLIST.md, EXAMPLES.md, or domain snippets.
4) If scripts are requested, add stubs and list dependencies in frontmatter `dependencies:`.
5) Validate against the checklist (see `resources/CHECKLIST.md`).
6) Output a folder plan (paths + filenames) followed by the complete file contents.

## Instructions for Claude (authoring voice)
- Use imperative, testable instructions; avoid vague language.
- Prefer short sections and bullets; add examples where ambiguity is likely.
- State explicit "in-scope" and "out-of-scope" to keep the Skill focused.
- Embed only essential context in `Skill.md`; move long details to `resources/`.

## Examples
- Prompt → “Create a ‘Meeting Notetaker’ Skill that extracts action items and owners from transcripts. Trigger: after a meeting transcript is provided.”
  - The generator produces a `Meeting Notetaker/Skill.md` with clear description, extraction rules, and examples; includes `resources/EXAMPLES.md` with annotated samples.

## Testing Checklist (summary)
- Name/description limits respected; YAML frontmatter present
- Description clearly states when to use the Skill
- Includes at least one input/output example
- Optional resources referenced and present
- If scripts exist, dependencies listed; no secrets hardcoded

## References
- Based on Claude Skills guidance and best practices: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills


