---
name: debug
description: Systematic debugging workflow with root cause verification before fixing
user_invocable: true
---

# Debug Workflow

Root cause verification workflow: understand the bug, prove the cause, then fix.

## Initialize (REQUIRED FIRST STEP)

```bash
python3 ~/.claude/plugins/agent-swarm/lib/debug_workflow.py start "$ARGUMENTS"
```

This creates the workflow state and sets you to the TRIAGE phase.

## Flow

```
TRIAGE → REPRODUCE → HYPOTHESIZE → [adversary] → PROVE → [adversary] → FIX → [adversary] → VERIFY → PUSH → CHECK_STATUS → DONE
   ↑                      ↑                         ↑
   └── can't reproduce ───┴── prediction fails ─────┴── verification fails
```

## Phases

| Phase | Purpose | Allowed Tools | Blocked | Required Outputs |
|-------|---------|---------------|---------|------------------|
| **TRIAGE** | Understand bug context | Read, Glob, Grep, WebSearch, WebFetch | Edit, Write | severity, affected_components, error_artifacts |
| **REPRODUCE** | Create failing test | Read, Glob, Grep, Edit, Write, Bash | - | failing_test |
| **HYPOTHESIZE** | Form root cause theory | Read, Glob, Grep | Edit, Write | hypothesis, prediction |
| **PROVE** | Verify hypothesis | Read, Glob, Grep, Bash | Edit, Write | prediction_confirmed, mechanism_traced, alternative_ruled_out |
| **FIX** | Implement fix | Read, Glob, Grep, Edit, Write, Bash | - | - |
| **VERIFY** | Run tests/lint | Read, Glob, Grep, Bash | Edit, Write | tests_pass, lint_pass |
| **PUSH** | Push changes | Bash | - | - |
| **CHECK_STATUS** | Verify CI/reviews | Read, Bash | Edit, Write | ci_pass, no new_review_comments |
| **DONE** | Complete | - | - | - |

## File Restrictions

In **REPRODUCE** phase, editing is limited to test files:
- `tests/**`, `*_test.py`, `test_*.py`
- `conftest.py`, `fixtures/**`, `mocks/**`

This prevents "fixing" the bug before proving you understand it.

## Adversary Gates

Three phases have adversary gates that challenge your work:

1. **HYPOTHESIZE** - Adversary challenges your hypothesis
   - "What alternative explanations exist?"
   - "How does your prediction distinguish this from X?"

2. **PROVE** - Adversary verifies your proof
   - "Did the prediction actually confirm the mechanism?"
   - "What other evidence supports this?"

3. **FIX** - Adversary checks fix matches proof
   - "Does this fix address the proven root cause?"
   - "Could this fix work for the wrong reason?"

## Kickback Logic

| From | To | Trigger |
|------|-----|---------|
| REPRODUCE | TRIAGE | Can't reproduce bug |
| PROVE | HYPOTHESIZE | Prediction not confirmed |
| VERIFY | PROVE | Tests/lint fail |
| CHECK_STATUS | PROVE | CI fails or new review comments |

Kickbacks force you to re-examine your understanding rather than repeatedly tweaking the fix.

## CLI Commands

```bash
# Start workflow
python3 lib/debug_workflow.py start "bug description"

# Check status
python3 lib/debug_workflow.py status

# Get current phase
python3 lib/debug_workflow.py phase

# Set phase manually (recovery)
python3 lib/debug_workflow.py set-phase <phase>

# Record triage outputs
python3 lib/debug_workflow.py triage <severity> "<components>" "<artifacts>"

# Record hypothesis
python3 lib/debug_workflow.py hypothesis "<hypothesis>" "<prediction>"

# Record verification results
python3 lib/debug_workflow.py verify <tests_pass> <lint_pass>
# Example: python3 lib/debug_workflow.py verify 1 1

# Advance to next phase
python3 lib/debug_workflow.py advance

# Stop workflow
python3 lib/debug_workflow.py stop
```

## Example Session

```bash
# 1. Start
python3 lib/debug_workflow.py start "Login fails with 500 error"

# 2. TRIAGE - Read logs, identify affected components
# Record findings:
python3 lib/debug_workflow.py triage "high" "auth,session" "stacktrace,error_log"

# 3. REPRODUCE - Write a failing test
# (Edit only test files in this phase!)
python3 lib/debug_workflow.py advance

# 4. HYPOTHESIZE - Form theory
python3 lib/debug_workflow.py hypothesis \
  "Session token validation fails on expired refresh tokens" \
  "Adding logging at validate_token() will show 'expired' before 500"

# 5. PROVE - Verify prediction
# Run the test with logging, confirm prediction
python3 lib/debug_workflow.py advance

# 6. FIX - Implement the fix
python3 lib/debug_workflow.py advance

# 7. VERIFY - Run tests
pytest && ruff check .
python3 lib/debug_workflow.py verify 1 1
python3 lib/debug_workflow.py advance

# 8. PUSH
git add -A && git commit -m "fix: handle expired refresh tokens"
git push
python3 lib/debug_workflow.py advance

# 9. CHECK_STATUS - Wait for CI, check reviews
python3 lib/debug_workflow.py advance

# 10. DONE
```

## DO NOT

- Skip REPRODUCE (no test = no proof the bug exists)
- Edit production code in HYPOTHESIZE or PROVE phases
- Fix before proving the root cause
- Ignore kickbacks - they exist because your understanding was wrong
- Bypass adversary gates - they catch flawed reasoning

## Why This Matters

Without root cause verification:
- Fixes often address symptoms, not causes
- Same bug resurfaces in different form
- Time wasted on trial-and-error fixes

This workflow forces you to **prove understanding before acting**.

## Permission Awareness

At task start, check workflow state for active permissions:

1. **Check active workflow**: `get_active_workflow_id()` returns current workflow
2. **Get permissions**: `get_permissions(workflow_id)` returns PermissionStore
3. **Verify tool access**: `is_tool_allowed(tool_name, **context)` before operations

**Self-enforcement**: The phase table above shows allowed/blocked tools per phase. Do not attempt blocked operations - they exist to enforce the "understand before fixing" discipline.

**Programmatic check** (lib/permission_query.py):
```python
from permission_query import get_permissions, is_tool_allowed

# Check if Edit is allowed in current phase
allowed, reason = is_tool_allowed("Edit", file_path="src/auth.py")
if not allowed:
    print(f"Blocked: {reason}")  # e.g., "Edit blocked in HYPOTHESIZE phase"
```

**File restrictions**: In REPRODUCE phase, editing is limited to test files. The permission system enforces this via file path patterns.
