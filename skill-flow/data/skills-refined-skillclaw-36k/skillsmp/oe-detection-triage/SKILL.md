---
name: oe-detection-triage
description: Debug detection and routing misclassifications in OpenEvent-AI (LLM vs regex, qna_types, confirmations, OOC drops, site-visit triggers). Use when intent seems wrong, Q&A is ignored, confirmations route to the wrong step, or site visit/date change triggers unexpectedly.
---

# Detection Triage

## Quick start

- Collect a minimal repro: message text, current_step, thread_id, event state (date_confirmed, locked_room_id, site_visit_state).
- If logs are needed: run with WF_DEBUG_STATE=1 and DETECTION_MODE=unified.

## Workflow

1. Confirm unified detection ran
   - Check state.extras["unified_detection"] in logs.
   - Verify pre-route logs: [UNIFIED_DETECTION] intent=...
2. Check OOC drops
   - If action is out_of_context_ignored, review check_out_of_context evidence gating.
3. Compare LLM vs regex signals
   - LLM: UnifiedDetectionResult (intent, signals, qna_types)
   - Regex: _detect_qna_types, pre_filter signals, step-specific keyword classifiers
4. Find the trigger in code (fast paths)
   - Site visit intercept: workflows/runtime/router.py and workflows/common/site_visit_handler.py
   - Step 7 classification: workflows/steps/step7_confirmation/trigger/classification.py
   - Step 5 classification: workflows/steps/step5_negotiation/trigger/classification.py
   - Step 2 confirmation heuristics: workflows/steps/step2_date_confirmation/trigger/step2_handler.py
   - Change detection: workflows/change_propagation.py
   - Room shortcut heuristics: workflows/steps/step1_intake/trigger/room_detection.py
5. Patch safely
   - Prefer unified detection signals; keep regex as fallback.
   - Strip email/URLs before keyword matching.
   - Use word-boundary regex for explicit phrases.
6. Add tests
   - Use tests/detection/ for detection changes.
   - Add regression tests when adding a new keyword or guard.

## Useful commands

- Enable verbose workflow debug: WF_DEBUG_STATE=1
- Run a deterministic trace: scripts/manual_ux/manual_ux_scenario_I.py
- Run detection tests: pytest tests/detection/ -q

## References

- docs/architecture/MASTER_ARCHITECTURE_SHEET.md (Detection Hot Spots)
- docs/guides/TEAM_GUIDE.md (Regex bug magnets)
