# Speckit command (single entrypoint)

Use this file for all Speckit commands. Do not reference any other command docs.

## Setup

- Resolve repo root and set `SPECKIT_ROOT` to the absolute path of `speckit/`.
- Use templates from `assets/templates/` and scripts from `scripts/`.

## Core artifacts (exactly four per feature)

Feature folders live at `specs/###-slug/` and MUST contain only:

- `spec.md`
- `decisions.md`
- `plan.md`
- `tasks.md`

Do not create `research.md`, `data-model.md`, `quickstart.md`, `checklist.md`, agent files, or contracts.

## Command routing (based on `$ARGUMENTS`)

If `$ARGUMENTS` starts with a subcommand, run that flow. If `$ARGUMENTS` is just a feature description, treat it as `new <feature description>`.

### A) `new <feature description>`

1. Run `scripts/create-new-feature.sh` with the feature description.
2. Ask up to 5 clarification questions (single message) ONLY for `spec.md`.
3. Write `spec.md` (see required content below).
4. Without further questions, write:
   - `decisions.md` (ADR-001 only)
   - `plan.md`
   - `tasks.md`
5. Stop.

### B) `spec <feature folder>`

1. Ask up to 5 clarification questions (single message) ONLY for `spec.md`.
2. Update only `spec.md`.
3. Stop.

### C) `plan <feature folder>`

1. No questions.
2. Update `decisions.md` (ADR-001) derived from `spec.md` + repo conventions.
3. Update `plan.md` derived from `spec.md` (light repo scan allowed).
4. Stop.

### D) `tasks <feature folder>`

1. No questions.
2. Update only `tasks.md` derived from `spec.md` + `plan.md` + `decisions.md`.
3. Stop.

### E) `implement <feature folder>`

1. No questions.
2. Implement tasks in order.
3. Mark tasks complete with `[x]` in `tasks.md`.
4. Stop.

## Question policy (strict)

- Questions are ONLY for building `spec.md`.
- Ask up to 5 questions total, all at once in a single message.
- After `spec.md` is written, do NOT ask any more questions.
- If spec info is missing, add explicit entries under **Assumptions** in `spec.md` and proceed.

## Artifact requirements (must follow)

### `spec.md` (contract; questions only here)

Include all of the following, concrete and testable:

- Problem statement (why)
- Goals and Non-goals
- Primary user flow (happy path)
- 1–5 user stories, prioritized (P1/P2/…); each with Given/When/Then acceptance scenarios
- Requirements: functional + non-functional
- Edge cases (top ones)
- Success criteria (measurable)
- Assumptions (explicit if info missing)
- Open questions (ONLY if truly blocking; otherwise use Assumptions)

Avoid vague words like “fast” without numbers if relevant.

### `decisions.md` (ADR-001 only)

Exactly one ADR:

- Context
- Options considered (at least 2)
- Decision (clear “we choose X because …”)
- Consequences (good + bad)

Derive from spec + repo conventions. If no big decision exists, choose a small but real one (e.g., API shape, error handling, storage location, auth method).

### `plan.md` (design + verification)

Must include:

- Summary
- Technical context from repo (stack, key modules/files likely touched; light scan allowed)
- Approach (mapped to primary user flow)
- Interfaces/APIs (contract)
- Data model/migrations (if any)
- Security/privacy considerations (if any)
- Observability (logs/metrics)
- Test strategy mapped explicitly to acceptance scenarios
- Rollout plan (feature flag/deploy steps) if user-facing
- Risks + mitigations (2–5)

No questions allowed. If spec is ambiguous, add an “Assumption:” line here and proceed.

### `tasks.md` (executable checklist)

Must include:

- Tasks grouped by user story priority (P1 then P2…)
- Every acceptance scenario covered by at least one implementation task AND one verification task (tests/manual)
- Explicit test tasks + a final “Verify all acceptance scenarios” task
- Tasks sized to ~30–90 minutes

No questions allowed. If missing info, reference assumptions from `spec.md`/`plan.md`.
