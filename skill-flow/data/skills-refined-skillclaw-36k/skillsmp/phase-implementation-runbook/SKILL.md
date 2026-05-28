---
name: phase-implementation-runbook
description: Enforce the Palette Kit v0.4 small-phase workflow. Use when working on any v0.4 phase implementation, validating docs/tests, packaging a patch, or preparing a commit/PR tied to the playbook.
---

# Phase Implementation Runbook

Use this skill whenever following the Palette Kit v0.4 Implementation Playbook (`planning/v0.4/v0.4-implementation-playbook.md`). It keeps the work aligned with the playbook’s 16 small phases, the v0.4 SPEC (`planning/v0.4/v0.4-palette-kit-spec.md`), and the related axis/reference docs under `planning/v0.4/`. Always favor the playbook order over convenience and prefer stubs that the playbook permits instead of adding heuristics.

## Key references (read before coding)

1. `planning/v0.4/v0.4-implementation-playbook.md` – linear phases, goals, stubs, “must nots,” and guardrails.
2. `planning/v0.4/v0.4-palette-kit-spec.md` – normative contracts, axes, and resolver guarantees.
3. The axis-specific doc for the phase you are working on (usage, relational, resolver pipeline, etc.).

## Workflow (must follow in order)

1. **Preflight and scope**

- Identify the numbered phase (0–16) from the playbook and review its “Goal,” “Must implement,” “May stub,” and “Must NOT” sections.
- Confirm the branch name format `phase-<number>-<short-slug>` and that you start from `v0.3` (or current release branch).
- Run `git status -sb` and surface any unrelated changes before making edits; pause if their presence needs clarification.
- Check the prior phase is complete; never merge or skip phases. If blocked, stop rather than reordering.

2. **Branch creation**

- Create a new branch from `v0.3` using `git switch -c phase-<number>-<short-slug>` (or `git checkout -b …`) and double-check `git status -sb`.
- Keep the phase number/slug visible so reviewers can confirm ordering.

3. **Implement the phase**

- Make only the changes explicitly required by the phase. Keep scope minimal, aligned with the playbook’s topological ordering, and avoid mixing axes or inferring behavior.
- Follow markdownlint rules (use `markdownlint-writer` skill) and keep TypeScript contracts intact (use `type-contract-auditor` when unsure).
- If an improvement is outside the current phase, note it (issue, TODO, or phase reference) and defer it rather than sneaking it in.
- Prefer adding new files for the phase; avoid modifying earlier layers unless the phase explicitly lists those files.
- When the playbook allows stubs (e.g., gamut, advanced curves), stub cleanly with TODO comments tied to the target phase; do not add heuristic logic.

4. **Validation (in order)**

- Run commands sequentially, stopping at the first failure:
  1. `npm run lint:md` (only when docs touched)
  2. `npm run lint`
  3. `npm run typecheck`
  4. `npm run test`
  5. `npm run build`
- If a step fails, fix and rerun starting from that step. If you intentionally skip a command, annotate “not run (\<reason\>)” in your report.

5. **Document, summarize, produce patch**

- Update any phase documentation that references the files you touched (e.g., resolver reference, axis deep dive) so diagrams/spec links stay accurate.
- Capture a summary (`git diff --stat`) and produce a patch file for reviewers: `git diff > /tmp/phase-<number>-<short-slug>.patch` (or equivalent) and note its path.

6. **Post-patch (after explicit approval)**

- Commit only the phase-related changes using Conventional Commit format and English.
- Push the branch and open a PR targeting `v0.3`, referencing the phase title and playbook step.
- In the PR, list the phase(s) effected, confirm no future phases were merged, and cite the implementation checklist (tests run, docs updated, guardrails satisfied).

## DX Quality Gates

- All new public APIs must provide exact TypeScript autocomplete and clear JSDoc describing intent, defaults, and which behaviors are explicit versus inferred.
- If an API seems awkward or hard to discover, pause and improve the developer DX before proceeding.
- DX regressions count as phase failures even when tests pass.

## Guardrails

- Never amend commits unless explicitly requested.
- Avoid destructive Git commands (`git reset --hard`, `git checkout --`, etc.).
- Do not reinterpret or redesign the SPEC; the playbook already defines the contract.
- Respect the small-phase linear ordering; merging future phases or skipping back is not allowed.
- If you encounter unexpected changes you didn’t make, stop and ask before continuing.
- If a spec detail is unclear, re-read the playbook/spec and ask rather than improvising.

## Output checklist (pre-approval)

Before asking for confirmation, document:

- The validation summary (commands run + “not run” notes).
- Patch path (e.g., `/tmp/phase-<number>-<short-slug>.patch`).
- A question prompting the reviewer for commit/push/PR approval.
- Confirmation the phase goals are met without extra features.
- Confirmation no architectural/API decisions were altered.
- A brief note mapping how the implementation satisfies the playbook requirements (phase number + goal) and where any stubs are intentionally left for future phases.
