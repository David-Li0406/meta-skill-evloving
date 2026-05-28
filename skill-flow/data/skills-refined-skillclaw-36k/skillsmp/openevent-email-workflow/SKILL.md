---
name: openevent-email-workflow
description: Canonical OpenEvent email workflow architecture (intake, date confirmation, room availability, offer review, negotiation, confirmation) and file map.
---

## When to use
- Implementing or modifying OpenEvent email workflow steps (intake through confirmation).
- Changing routing, detours, HIL gating, or workflow state transitions.
- Updating step-specific prompts/templates or Q&A behavior that affects client emails.

## Canonical steps and subflows
Step names and labels come from `backend/workflow/state.py`.
- Step 1: Intake (subflow_group: `intake`)
- Step 2: Date Confirmation (subflow_group: `date_confirmation`)
- Step 3: Room Availability (subflow_group: `room_availability`)
- Step 4: Offer Review (subflow_group: `offer_review`)
- Step 5: Negotiation (subflow_group: `negotiation`)
- Step 6: Transition Checkpoint (subflow_group: `transition_checkpoint`)
- Step 7: Confirmation (subflow_group: `confirmation`)

## File map (authoritative sources)
- Orchestrator entrypoint: `backend/workflow_email.py`
- Routing pipeline: `backend/workflows/runtime/router.py`, `backend/workflows/runtime/pre_route.py`
- Step 1: `backend/workflows/steps/step1_intake/`
- Step 2: `backend/workflows/steps/step2_date_confirmation/`
- Step 3: `backend/workflows/steps/step3_room_availability/`
- Step 4: `backend/workflows/steps/step4_offer/`
- Step 5: `backend/workflows/steps/step5_negotiation/`
- Step 6: `backend/workflows/steps/step6_transition/`
- Step 7: `backend/workflows/steps/step7_confirmation/`
- Shared logic (prompts, pricing, capture, gating): `backend/workflows/common/`
- NLU + change detection: `backend/workflows/nlu/`, `backend/workflows/change_propagation.py`
- Q&A engine: `backend/workflows/qna/`
- HIL tasks: `backend/workflows/runtime/hil_tasks.py`, `backend/workflows/io/tasks.py`
- Frontend workflow surfaces (HIL, deposit, debug): `atelier-ai-frontend/app/`

## Data contracts and invariants
- Workflow state types: `backend/workflows/common/types.py` (`IncomingMessage`, `WorkflowState`).
- Event schema defaults: `backend/workflows/io/database.py` (`ensure_event_defaults`).
- Stage metadata: `backend/workflow/state.py` (`WorkflowStep`, `write_stage`).
- Workflow rules and invariants: `docs/guides/workflow_rules.md`, `docs/guides/workflow_test_requirements.md`.
- Architecture reference: `docs/reference/ARCHITECTURE_DIAGRAMS.md` and `backend/README.md`.

## Change discipline
- Prefer updating `backend/workflows/steps/*` over legacy `backend/workflows/groups/*` re-exports.
- If you change step behavior, update matching tests in `tests/specs/` and `tests/workflows/`.
- Use `tests/TEST_MATRIX_detection_and_flow.md` + `tests/TEST_INVENTORY.md` to pick the right suites.
- Run `./scripts/tests/test-smoke.sh` for the fast workflow lane; expand to `pytest tests/workflows -n auto` or `pytest backend/tests -m "not integration"` when deeper coverage is needed.

## Retrospective Notes
- Add durable learnings here via `scripts/skills/retrospective.py`.
