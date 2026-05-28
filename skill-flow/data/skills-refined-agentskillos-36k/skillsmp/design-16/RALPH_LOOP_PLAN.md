---
name: State-Aware RALPH Loop for Claude Code
version: 1.0
date: 2026-01-26
description: RALPH loop specification for Claude Code CLI - takes user journey spec to working code via state machine
---

# RALPH Loop Plan — Claude Code Edition

## Overview

RALPH (Requirement-Assisted Loop For Hybrid agents) is a state-aware loop that takes a spec from user journey to working code.

**Core Flow:**
```
STRESS_TEST → VALIDATE → GENERATE_PRP → CHECK_PRP → GENERATE_TESTS → CHECK_TESTS → IMPLEMENT → COMPLETE
```

Each state is a gate. Gate must pass before moving to next state. If gate fails, retry (max `--max-gate-retries` times) before entering GUTTER.

## Architecture

```mermaid
flowchart LR
    A["1. STRESS_TEST<br/>Check completeness"] --> B["2. VALIDATE<br/>Check clarity"]
    B --> C["3. GENERATE_PRP<br/>Extract from spec"]
    C --> D["4. CHECK_PRP<br/>Validate structure"]
    D --> E["5. GENERATE_TESTS<br/>Extract from PRP"]
    E --> F["6. CHECK_TESTS<br/>Validate tests match PRP"]
    F --> G["7. IMPLEMENT<br/>Claude codes to pass tests"]
    G --> H["✅ COMPLETE"]

    style A fill:#e1f5ff
    style B fill:#e1f5ff
    style C fill:#fff3e0
    style D fill:#fff3e0
    style E fill:#f3e5f5
    style F fill:#f3e5f5
    style G fill:#e8f5e9
    style H fill:#c8e6c9
```

## State Definitions

### STRESS_TEST (order: 1)
**Command:** `~/.claude/design-ops/enforcement/design-ops-v3-refactored.sh stress-test {{spec_file}}`
**Pass Condition:** Instruction generated successfully
**On Fail:** Review stress-test-instruction.md, fix completeness gaps in spec
**On Pass:** Transition to VALIDATE

### VALIDATE (order: 2)
**Command:** `~/.claude/design-ops/enforcement/design-ops-v3-refactored.sh validate {{spec_file}}`
**Pass Condition:** Structure validation passed
**On Fail:** Review validate-instruction.md, fix ambiguities in spec
**On Pass:** Transition to GENERATE_PRP

### GENERATE_PRP (order: 3)
**Command:** `~/.claude/design-ops/enforcement/design-ops-v3-refactored.sh generate {{spec_file}}`
**Pass Condition:** generate-instruction.md created
**On Fail:** Ensure spec meets validation gates, retry
**On Pass:** Transition to CHECK_PRP

### CHECK_PRP (order: 4)
**Command:** `~/.claude/design-ops/enforcement/design-ops-v3-refactored.sh check {{prp_file}}`
**Pass Condition:** PRP validation passed
**On Fail:** Fix PRP structure based on error output
**On Pass:** Transition to GENERATE_TESTS

### GENERATE_TESTS (order: 5)
**Command:** `~/.claude/design-ops/enforcement/design-ops-v3-refactored.sh implement {{prp_file}}`
**Pass Condition:** implement-instruction.md created
**On Fail:** Ensure PRP meets all requirements
**On Pass:** Transition to CHECK_TESTS

### CHECK_TESTS (order: 6)
**Command:** `./validate-tests.sh tests/` (custom script in project root)
**Pass Condition:** All tests valid and match PRP criteria
**On Fail:** Regenerate tests from PRP, ensure 1:1 mapping to success criteria
**On Pass:** Transition to IMPLEMENT

### IMPLEMENT (order: 7)
**Command:** `pytest tests/ -v` (or `npm test`, `cargo test`, etc.)
**Pass Condition:** All tests passed (exit code 0)
**On Fail:** Fix code to pass failing tests
**On Pass:** Transition to COMPLETE

### COMPLETE (order: 8)
**Terminal State** — Pipeline finished successfully

## GUTTER Escalation

When max retries exceeded:
```bash
echo "🚨 GUTTER REACHED: Max retries exhausted for state: {{current_state}}"
echo "Last output saved to: .ralph/gutter-{{current_state}}.log"
git diff > .ralph/gutter-diff.patch
exit 1
```

Manual recovery: Fix issues, then `claude --resume` to continue from that state.

## Usage with Claude Code

```bash
# One-shot: entire pipeline
claude exec ralph-loop.sh --state-machine specs/my-feature.md --max-gate-retries 5

# Resume after manual fix
claude exec ralph-loop.sh --resume --max-gate-retries 5

# Dry-run to preview states
claude exec ralph-loop.sh --state-machine --dry-run specs/my-feature.md
```

## State Machine Implementation Details

### `.ralph/state.md` Format
```markdown
# RALPH State

current_state: STRESS_TEST
retry_count: 0
history:
  - 2026-01-26T18:55:00 | INIT -> STRESS_TEST
  - 2026-01-26T18:55:05 | STRESS_TEST -> VALIDATE (gate passed)
```

### State Persistence
- State lives in files, survives agent crashes
- Each gate retry increments retry counter
- Transitions reset counter to 0
- History logged for audit trail

### Retry Mechanics
1. Gate command runs
2. Output checked against `pass_condition`
3. If PASS → transition to next state (reset retry_count to 0)
4. If FAIL → increment retry_count
5. If retry_count >= max_gate_retries → GUTTER
6. Otherwise → re-run gate with fresh agent context

## Design Philosophy

| Principle | Why |
|-----------|-----|
| **State in Files** | Survives restarts, auditable history |
| **Fresh Context Per Retry** | No context corruption across attempts |
| **Explicit Gates** | Every transition requires proof (pass condition) |
| **Bounded Retries** | Prevents infinite loops while allowing complexity |
| **Resume Capability** | Recover from GUTTER without restarting |

## Example: Full Pipeline Run

```
$ claude exec ralph-loop.sh --state-machine specs/recipe-saver.md --max-gate-retries 3

State: STRESS_TEST (retry 0/3)
Running: design-ops-v3-refactored.sh stress-test specs/recipe-saver.md
Output: ✅ Instruction generated
Gate: PASS
Transition: STRESS_TEST → VALIDATE

State: VALIDATE (retry 0/3)
Running: design-ops-v3-refactored.sh validate specs/recipe-saver.md
Output: ✅ Structure validation passed
Gate: PASS
Transition: VALIDATE → GENERATE_PRP

State: GENERATE_PRP (retry 0/3)
Running: design-ops-v3-refactored.sh generate specs/recipe-saver.md
Output: ✅ Instruction generated
Gate: PASS
Transition: GENERATE_PRP → CHECK_PRP

State: CHECK_PRP (retry 0/3)
Running: design-ops-v3-refactored.sh check PRPs/recipe-saver.prp.md
Output: ✅ PRP validation passed
Gate: PASS
Transition: CHECK_PRP → GENERATE_TESTS

State: GENERATE_TESTS (retry 0/3)
Running: design-ops-v3-refactored.sh implement PRPs/recipe-saver.prp.md
Output: ✅ Instruction generated
Gate: PASS
Transition: GENERATE_TESTS → CHECK_TESTS

State: CHECK_TESTS (retry 0/3)
Running: ./validate-tests.sh tests/
Output: ✅ All tests valid and match PRP criteria
Gate: PASS
Transition: CHECK_TESTS → IMPLEMENT

State: IMPLEMENT (retry 0/3)
Running: pytest tests/ -v
Output: FAILED tests/test_extraction.py::test_duplicate_detection
Gate: FAIL
Retry: 1/3

State: IMPLEMENT (retry 1/3)
[Claude writes code to fix failing test]
Running: pytest tests/ -v
Output: ✅ All tests passed
Gate: PASS
Transition: IMPLEMENT → COMPLETE

✅ PIPELINE COMPLETE
```

## Next Steps

1. Build ralph-loop.sh with state machine support
2. Add to design-ops as executable
3. Create validate-tests.sh template for projects
4. Use in Cursor/Claude Code to automate spec → code pipeline
