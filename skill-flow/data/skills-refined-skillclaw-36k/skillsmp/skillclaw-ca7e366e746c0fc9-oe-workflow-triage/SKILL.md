---
name: oe-workflow-triage
description: Use this skill when you have a regression or bug report in OpenEvent and need to create a minimal reproduction trace along with a fix plan tied to workflow invariants and tests.
---

# Skill body

## Minimal reproduction first (avoid “guess fixes”)

1. **Pick the closest deterministic scenario:**
   - Site visit: `scripts/manual_ux_scenario_I.py`, `scripts/manual_ux_scenario_H.py`
   - Late changes / detours: `scripts/manual_ux_scenario_E.py`, etc.

2. **Produce a trace:**
   - Run the scenario: 
     ```bash
     python3 scripts/manual_ux_scenario_I.py > /tmp/repro.json
     ```

3. **Validate with invariants:**
   - Check the trace:
     ```bash
     python3 scripts/validate_manual_ux_run.py /tmp/repro.json --require_site_visit
     ```

4. **If the bug is not covered by existing scenarios:**
   - Create a new scenario by copying the closest one:
     - `scripts/manual_ux_scenario_*.py`
   - Ensure it is deterministic (set `AGENT_MODE=stub`, use explicit mapping, and intent overrides).
   - Add or extend validator checks only when they prevent regressions.

## Fix plan outputs

- Create a 1–3 PR ladder:
  - **PR1:** Characterization test / scenario reproduction
  - **PR2:** Fix with minimal blast radius
  - **PR3:** Cleanup/refactor (optional)