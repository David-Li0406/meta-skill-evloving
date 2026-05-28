---
name: test_gate_bivio
description: Manages test gate interaction respecting the required depth
version: 1.1.0
author: Antigravity
---

# Operational Instructions

## Trigger
- Within `tech_rag` (Step 5 Test Gate).
- Whenever interactive validation is needed before proceeding.

## Inputs
- **User Config**: `<SmokeTestCmd>` in `.agent/project/PROJECT_AGENT_CONFIG.md`.
- **User Choice**: Direct interaction (Easy/Deep/Debug).

## Steps
1. **Interrupt**: ASK the user for the desired test level.
2. **Easy/Smoke**:
   - Execute `<SmokeTestCmd>` command.
3. **Deep**:
   - Execute complete regression tests (`pytest`, `npm test`, etc).
   - Execute `<DeepTestCmd>` (e.g., `uv run pytest -q`).
   - If `<NegativeTestMarkers>` are present, also run negative tests (e.g., `uv run pytest -m "negative or fuzz"`).
4. **Debug**:
   - Activate `sequential-thinking` to isolate the case.
   - Execute `<DebugTestCmd>` (e.g., `uv run pytest -q -vv --maxfail=1 --pdb`).

## Outputs
- **Result**: `PASS` (proceed) or `FAIL` (fix required).

## Configuration
Check `.agent/project/PROJECT_AGENT_CONFIG.md` for the default Smoke command.
