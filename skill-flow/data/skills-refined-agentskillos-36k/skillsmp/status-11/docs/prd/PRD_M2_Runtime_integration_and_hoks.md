# Product Requirements Document

## Introduction

### One-liner
Runtime Integration & Hooks: formalize AI-branch injection with a 12-state integration state machine, atomic checkpoints and rollback, and save/load compatibility so AI branches persist safely across sessions.

### Problem statement
The existing M2 work defines proposal lifecycle and Director/Writer behavior, but runtime integration is underspecified. Without a formal state machine, transactional checkpoints, and clear persistence rules, AI branch injection can lead to inconsistent runtime state, save corruption, or unreproducible playthroughs. This PRD (ge-hch.5.16) defines the runtime contract, deliverables, and acceptance criteria for safe integration of AI-generated branches into live play sessions.

### Goals
- Define a deterministic 12-state integration state machine and transition rules for branch injection.
- Implement atomic checkpoint/commit/rollback semantics that prevent save corruption.
- Persist branch integration metadata and audit logs to support reproducibility and debugging.
- Ensure save/load resumes in-progress branches or safely roll back corrupted ones with a clear player-facing message.

### Non-goals
- This PRD does not redefine Director heuristics, policy rules, or Writer prompts (those remain in M2 core PRD). It focuses only on runtime integration mechanics and persistence.

## Users

### Primary users
- Players (desktop/mobile) who must experience robust save/load and no corruption when AI branches are integrated.

### Secondary users
- Engineers implementing runtime, save, and persistence systems.
- QA and playtesters validating save/load, rollback, and replay behavior.
- Producers needing audit logs to investigate incidents.

## Requirements

### Functional requirements (MVP)
- Integration state machine
  - Formalize a 12-state state machine covering: ProposalAccepted, PreInjectCheckpoint, Injecting, Executing, CheckpointOnBeat, CommitPending, Committed, RollbackPending, RollingBack, RolledBack, TerminalSuccess, TerminalFailure. Define allowable transitions and idempotency guarantees.
- Atomic checkpoint/rollback
  - Checkpoints capture necessary runtime state (player inventory, variables, scene index, branch progress markers). Checkpoints must be verifiable (checksums) and restorable deterministically.
  - Rollback restores to the last valid checkpoint and clears transient branch markers.
- Save/load compatibility
- Save files must include `branch_history` metadata that records in-progress branches and a minimal resume payload. Required fields (types):
  - `schema_version` (integer) — branch_history schema version.
  - `branch_id` (string) — unique branch instance id.
  - `proposal_hash` (string|null) — content hash of the proposal, if available.
  - `created_at` (string, date-time)
  - `updated_at` (string, date-time)
  - `integration_state` (string, enum: ProposalAccepted, PreInjectCheckpoint, Injecting, Executing, CheckpointOnBeat, CommitPending, Committed, RollbackPending, RollingBack, RolledBack, TerminalSuccess, TerminalFailure)
  - `last_checkpoint_id` (string|null)
  - `last_checkpoint_ts` (string, date-time|null)
  - `resume_payload` (object|null) — small engine-specific payload required to resume (for example: next scene index, pending actions). Keep this minimal to avoid large save files.
- Minimal resume payload rule: the save should embed only the small, deterministic information required to resume or rollback (ids, timestamps, and a compact `resume_payload`). Full audit logs (detailed transition records, validation reports, director decisions) must not be embedded by default.
- Audit logs and diagnostics: send full integration logs to the telemetry/external store with configurable retention. Saves may carry `branch_history.audit_ref` (string) which references the external audit id when telemetry is available; loader falls back to embedded data if external logs are unavailable.
- Privacy & security: embedded `branch_history` must redact PII. Prefer storing sensitive details in the external telemetry store where access control and encryption at rest can be enforced. Document what is considered PII in `docs/dev/`.
- Migration & versioning: include `schema_version` and a migration strategy. Loaders must accept older `schema_version` values and either migrate them or conservatively rollback if migration is unsafe.
- Resume policy (deterministic & conservative): when loading, resume a branch only if `last_checkpoint_id` exists and the checkpoint's checksum/version matches the expected value. If a deterministic resume cannot be guaranteed, perform an automatic rollback to the last valid checkpoint, log the decision, and notify the player with the graceful recovery message.
- Resume timing: resumption should occur at the next safe beat (see hook points `pre_checkpoint`/`post_checkpoint`) so the runtime can re-establish transient systems before continuing execution.
- Suggested canonical artifacts: provide a canonical JSON Schema and examples to live at `docs/dev/branch-history.schema.json` and `docs/dev/examples/branch-history-example.json` so implementers have an exact reference.
- Audit logging and persistence
  - Record transitions, decisions, validation references, and rollback causes in an append-only integration log associated with a save id and player id (redact PII).
- Hook manager API
  - Provide `src/runtime/hook-manager` with events: `pre_inject`, `post_inject`, `pre_checkpoint`, `post_checkpoint`, `pre_commit`, `post_commit`, `on_rollback` and allow subscribers for telemetry, persistence, and UI.

### Non-functional requirements
- Determinism
  - Checkpoint/restore must be deterministic; running the same sequence from the same checkpoint reproduces state.
- Reliability
  - No save file corruption allowed; recoverable errors must trigger a rollback path and be logged.
- Performance
  - Checkpoint and commit operations must complete within a reasonable window (configurable), default target 2s.
- Security & privacy
  - Integration logs must redact PII; access to logs must be access-controlled and encrypted at rest.

### Integrations
- Ink runtime save/load system (must be extended to carry `branch_history` metadata). Suggest adding `src/runtime/save-adapter.js` / `src/runtime/load-adapter.js` hooks.
- Telemetry system (emit integration events and lifecycle transitions).

## Release & Operations

### Rollout plan
- Phase A — Design & tests
  - Finalize state machine; add unit tests for each transition and idempotency.
  - Create a save metadata schema and migration plan.
- Phase B — Internal pilot
  - Implement hook manager and checkpoint/rollback primitives; run pilot on internal demo story with feature flag enabled.
- Phase C — Soft launch
  - Expose to small subset of users with monitoring and operator alerts for frequent rollbacks or save issues.
- Phase D — General availability
  - Remove pilot flags and extend to more stories.

### Quality gates
- Unit tests covering state machine transitions and checkpoint/rollback logic (≥ 80% coverage for new runtime module).
- Fuzzed save/load test suite that generates corrupted checkpoints and validates rollback behavior.
- End-to-end Playwright smoke tests: save mid-branch, reload, and verify either resume or graceful rollback.

### Risks & mitigations
- Risk: Partial checkpoint writes corrupt saves
  - Mitigation: write checkpoints to temporary file and atomically rename on success; include checksums and versioned migration support.
- Risk: Inconsistent branch resumption logic leads to subtle divergences
  - Mitigation: conservative resume policy — prefer rollback unless deterministic resume conditions are met; log decisions for audit.

## Open Questions
- Exact fields and formats for `branch_history` (I can propose a schema).
- Where to store integration logs (local file vs telemetry warehouse) and retention policy.
- Whether to expose an operator tooling endpoint to force rollback or replay a branch for debugging.

---

Change log:
- 2026-01-19: Created dedicated PRD `docs/prd/ge-hch.5.16.md` focusing runtime integration, state machine, checkpoint/rollback, and save/load behavior. This complements the broader M2 PRD which remains unchanged.
