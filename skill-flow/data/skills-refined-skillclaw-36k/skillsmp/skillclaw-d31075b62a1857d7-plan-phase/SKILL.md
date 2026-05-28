---
name: plan-phase
description: Use this skill when you need to create a detailed execution plan for a specific phase of a project, generating a PLAN.md file.
---

# Skill body

## Objective
Create executable phase prompts with discovery, context injection, and task breakdown. The output will be one or more PLAN.md files in the phase directory (`.planning/phases/XX-name/{phase}-{plan}-PLAN.md`).

## Gap Closure Mode
When invoked with the `--gaps` flag, the skill will address gaps identified by the verifier. It will load `VERIFICATION.md` and create plans to close specific gaps.

## Execution Context
1. Load project state from `.planning/STATE.md`.
2. Load roadmap from `.planning/ROADMAP.md`.
3. Load requirements from `.planning/REQUIREMENTS.md`.

## Steps
1. **Check Directory**: Ensure the `.planning/` directory exists. If not, prompt the user to run `/ag4:new-project`.
2. **Parse Arguments**: Accept phase number as an argument (optional; auto-detects the next unplanned phase if not provided).
3. **Extract Requirements**:
   - Find the phase in `ROADMAP.md` and get its `Requirements:` list (e.g., "PROF-01, PROF-02, PROF-03").
   - Look up each REQ-ID in `REQUIREMENTS.md` to get the full description.
   - Present the requirements for the current phase:
     ```
     Phase [N] Requirements:
     - PROF-01: User can create profile with display name
     - PROF-02: User can upload avatar image
     - PROF-03: User can write bio (max 500 chars)
     ```
4. **Load Phase Context**: If it exists, read `.planning/phases/XX-name/{phase}-CONTEXT.md` for research findings, clarifications, and decisions from phase discussions.
5. **Load Codebase Context**: Check for `.planning/codebase/` and load relevant documents based on phase type.
6. **Handle Gaps**: If the `--gaps` flag is present, also load `@.planning/phases/XX-name/{phase}-VERIFICATION.md`, which contains structured gaps in YAML frontmatter.

## Allowed Tools
- Read
- Bash
- Write
- Glob
- Grep
- AskUserQuestion
- WebFetch
- stormmcpagateway*