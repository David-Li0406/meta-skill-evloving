---
name: openevent-email-change-checklist
description: Review and testing checklist for OpenEvent email workflow changes (intake, offers, availability, confirmation).
---

## When to use
- Any change to workflow steps, detours, NLU, Q&A, or HIL behavior.
- Updating offer composition, availability replies, confirmations, or email templates.

## Checklist (minimal but consistent)
- Touched steps: confirm changes live under `backend/workflows/steps/step*/` and align with `backend/workflow/state.py` step labels.
- Orchestrator/routing: verify `backend/workflow_email.py` + `backend/workflows/runtime/*.py` still reflect the expected path.
- Schema changes: if you add fields, update `backend/workflows/io/database.py` (`ensure_event_defaults`) and any fixtures used in tests.
- Prompts/templates: check `backend/workflows/common/prompts.py` and step-specific `llm/` modules.
- HIL rules: validate `backend/workflows/runtime/hil_tasks.py` and the invariants in `docs/guides/workflow_test_requirements.md`.

## Tests to run (pick the smallest lane that fits)
- Fast lane: `./scripts/tests/test-smoke.sh`.
- Workflow harness: `pytest tests/workflows -n auto`.
- Backend regression lane: `pytest backend/tests -m "not integration"`.
- Use `tests/TEST_MATRIX_detection_and_flow.md` + `tests/TEST_INVENTORY.md` to pick targeted suites.

## E2E Browser Testing - CRITICAL
- **ALWAYS use proper email format** when testing via the browser UI, NOT plain text messages.
- The frontend expects email-like input with From/Subject headers for proper session tracking.
- Example format:
  ```
  From: test@example.com
  Subject: Room Booking Request

  Hi, I'd like to book a room for 25 people on 15.02.2026...
  ```
- Plain text without email headers causes session/state issues and unreliable test results.

## Edge cases to re-check
- Detours (date/room/products) return to the caller step and do not skip required gates.
- Q&A replies do not mutate workflow state and include a resume prompt.
- Sequential workflow requests (confirm step + ask next step) do not route to general Q&A.
- Step 3 does not create HIL tasks (`docs/guides/workflow_test_requirements.md`).

## Docs and changelog
- If behavior or suite status changes, add a short entry in `DEV_CHANGELOG.md` (see `tests/TEST_INVENTORY.md`).

## Retrospective Notes
- Add durable learnings here via `scripts/skills/retrospective.py`.
