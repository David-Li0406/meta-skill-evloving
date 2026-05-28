---
name: swe-workflow-debug-tdd
version: 1.0.0
description: Test-driven debugging for failing tests or bugs
workflow:
  aware: true
  callable_from:
    - WF_CLASSIFY
  default_return: WF_EXECUTE
  supports_standalone: true
  auto_transition: true
---

# Workflow Debug TDD Skill

Test-driven debugging workflow for rapid iteration.

## Purpose

- Reproduce failing tests/bugs
- Identify root cause
- Implement fix
- Verify fix works

## TDD Cycle

1. **RED** - Confirm test fails / bug reproduces
2. **Analyze** - Identify root cause
3. **GREEN** - Implement minimal fix
4. **Verify** - Confirm test passes / bug fixed
5. **Refactor** - Clean up if needed

## Actions

1. **Run failing test** - Confirm reproduction
2. **Read error output** - Understand failure
3. **Trace to source** - Find root cause
4. **Implement fix** - Minimal change
5. **Re-run test** - Verify fix

## Skill Return Format

```markdown
## Skill Return
- **Skill**: swe-workflow-debug-tdd
- **Status**: [success|needs_clarification|blocked]
- **Findings Summary**: [bug description and fix applied]
- **Artifacts**: [files changed, tests affected]
- **Next Step Hint**: WF_EXECUTE
```

## Exit

`> **Skill /swe-workflow-debug-tdd complete** - bug fixed, returning to WF_EXECUTE`
