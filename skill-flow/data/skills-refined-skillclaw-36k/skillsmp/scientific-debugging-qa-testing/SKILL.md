---
name: Scientific Debugging (QA & Testing)
description: The Unified Testing Constitution and "Junie-Mode" protocol for reproducing, fixing, and verifying bugs.
---

# Unified Testing Protocol ("Junie-Mode")

This skill activates when the user mentions "Junie-mode", "Debug this", "Test this", or reports a bug. It enforces strict evidence-based debugging and compliant test architecture.

## 1. The Constitution (Rules of Law)

### The Law of Separation
*   **Logic Tests (`test_{comp}.py`)**: Happy path, polite failures, spec compliance. (Fast)
*   **Robustness Tests (`test_{comp}_mutation.py`)**: Garbage input, security injections, fuzzing. (Slow)
*   **Integrity Tests (`integrity/`)**: Schema validation (Yellberus).
*   **Conflict Resolution**: Always split logic and robustness into separate files.

### The Law of Mirroring
*   Tests must mirror `src/` exactly.
*   `src/data/repositories/song.py` -> `tests/unit/data/repositories/test_song.py`

### The Law of Silence
*   **No Interactivity**: Tests never block. 
*   **Mock Popups**: Always patch `QMessageBox` to auto-accept.

## 2. The Debug Loop ("Junie-Mode")

### Phase 1: Reproduce (Red Phase)
*   **Goal**: Prove the bug exists.
*   **Action**: Create a standalone reproduction script in `tests/repro/` (e.g., `tests/repro/repro_issue_123.py`).
*   **Requirement**: The script **MUST FAIL** initially.

### Phase 2: Investigate (Print Phase)
*   **Goal**: Find the root cause.
*   **Action**: Use `grep_search` and temporary `print()`/`logging` to trace. 
*   **Constraint**: Do not "lint" or clean code. Just find the bug.

### Phase 3: Surgical Fix (Green Phase)
*   **Goal**: Fix the bug with minimal changes.
*   **Action**: Apply the fix.
*   **Constraint**: Fix only what is broken.

### Phase 4: Verify
*   **Action**:
    1.  Run the repro script (Must PASS).
    2.  Run related Logic/Integrity tests to check for regressions.
*   **The Hard Revert**: If the fix fails, **revert immediately**. Do not patch the patch.

### Phase 5: Cleanup
*   **Action**: Delete the manual reproduction script and debug prints.

## 3. Tooling
*   **Wrapper**: Use `python tools/run_tests.py` instead of raw `pytest` to handle PowerShell encoding issues.
    *   `python tools/run_tests.py tests/unit/test_my_feature.py`
