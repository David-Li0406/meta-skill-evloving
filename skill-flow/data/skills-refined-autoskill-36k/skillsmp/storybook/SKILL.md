---
name: storybook
description: >-
  Use Storybook to document UI states and design decisions as portable artifacts
  (stories + MDX docs) that engineers and QA can review. Use when: (1) exploring
  a component library interactively, (2) capturing canonical UI states for design
  guidance, (3) providing evidence and references in Beads task comments. This
  skill is tool-focused and does not assume Storybook is installed in the repo.
---

# Storybook

Use Storybook to make UI decisions concrete, reviewable, and reusable (via stories and docs) without coupling to app routing or backend state.

## Repo rules (when present)

If the repo provides Cursor rules for Storybook, follow them.

- Storybook rules: [`.cursor/rules/storybook.mdc`](mdc:.cursor/rules/storybook.mdc)

## Portability rules

- Do **not** assume Storybook exists in the current repo.
- Prefer `package.json` scripts and local repo conventions over hardcoded commands.
- If Storybook is missing, **do not** set it up as part of using this skill; instead file a follow-up task to add Storybook to the target app/package.

## Prerequisites

- A component library or UI surface that can be rendered in isolation (stories)
- Storybook installed in the repo (or a follow-up task exists to add it)

## Quick checks (is Storybook available?)

Use the simplest available signal:

- A Storybook config folder exists (commonly `.storybook/`)
- `package.json` includes a `storybook` script (commonly `storybook`, `storybook:dev`, or `storybook:build`)
- Dependencies include `@storybook/*`

If none are true, treat Storybook as **not available** and file a follow-up task.

## Usage patterns

### 1) Use stories as the “design artifact”

When providing design guidance, prefer updating/adding stories to capture:

- **Key UI states**: empty, loading, error, success, partial data
- **Variants**: size, intent, density, themes, edge cases
- **Interactive behaviors**: focus states, keyboard interactions, hover/pressed, disabled

Stories should be:

- **Deterministic** (no reliance on live network)
- **Representative** (match real-world data shapes)
- **Minimal** (only enough wrapper/context to render)

### 2) Use docs (MDX) for decision rationale

If the decision needs narrative, add or update Storybook docs to include:

- **Decision summary**: what changed and why
- **Do/Don’t guidance** for engineers
- **Accessibility notes** (keyboard, focus order, ARIA expectations)
- **References**: relevant framework/library docs (and internal skill docs when applicable)

### Semantics for mocks (a11y + lint friendly)

- Prefer semantic HTML elements (e.g., `<output>`, `<fieldset>/<legend>`) instead of ARIA-only semantics in story mocks.
- This keeps accessibility linting clean and makes acceptance criteria easier to verify.

## Runbook: local interaction tests (ralph-monitoring)

Use these **exact** local commands for `apps/ralph-monitoring` (verified against `apps/ralph-monitoring/package.json`).

### Start Storybook (Terminal A)

```bash
cd apps/ralph-monitoring
bun run storybook
```

This serves Storybook at `http://127.0.0.1:6006` by default.

### Run interaction tests (Terminal B)

```bash
cd apps/ralph-monitoring
bun run interaction-test
```

Under the hood this runs:

```bash
test-storybook --url http://127.0.0.1:6006 --config-dir .storybook
```

If you change the Storybook port/host, you must update the `--url` accordingly (or run the `test-storybook ...` command directly).

## Evidence + Beads comment format

When you use Storybook to inform an implementation task, leave a Beads comment that links to the Storybook artifact(s) and captures the decision:

### Minimal “design guidance” comment (C6-friendly)

- **Artifact**: `path/to/story-file.tsx` (story name: `<StoryName>`)
- **Decision**: what should change, and why
- **Acceptance**: the observable UI behavior/state
- **References**: links to relevant docs (and/or internal standards)

### Interaction-test evidence (copy/paste friendly)

Paste this into the Beads task as evidence after running interaction tests locally:

```md
Interaction tests (Storybook):
- Command: `(cd apps/ralph-monitoring && bun run interaction-test)`
- Result: PASS | FAIL
- Summary: <e.g., "all interaction tests passed" OR "3 failing stories">
- Failing stories (if any):
  - `<StoryTitle>` (`path/to/story-file.stories.tsx`) — <what failed / key error line>
  - `<StoryTitle>` (`path/to/story-file.stories.tsx`) — <what failed / key error line>
```

### Optional visual evidence

If screenshots are required (e.g., design review), capture them using the standard screenshot policy from the `agent-browser` skill:

- For `ralph-e2e` runs: `.devagent/workspace/tests/ralph-e2e/runs/YYYY-MM-DD_<epic-id>/screenshots/`
- Otherwise: `.devagent/workspace/tasks/active/YYYY-MM-DD_task-slug/screenshots/`

## Common pitfalls

- **Using Storybook as a substitute for requirements**: stories are the artifact, but you still need a clear acceptance statement in the task.
- **Non-deterministic stories**: avoid live network calls; prefer fixtures/mocks.
- **Over-wrapping**: keep stories focused; complex providers should be minimal and explicit.
