---
name: swe-workflow-detect-req
version: 1.0.0
description: Detect implicit requirements from user request
workflow:
  aware: true
  callable_from:
    - WF_CLASSIFY
  default_return: WF_LOAD_FEATURE
  supports_standalone: false
  auto_transition: true
---

# Workflow Detect Requirements Skill

Extract explicit and implicit requirements from user request.

## Purpose

- Parse user request for explicit requirements
- Infer implicit requirements (edge cases, validation, etc.)
- Identify non-functional requirements
- Document for tracking

## Requirement Categories

1. **Functional** - What the code should do
2. **Non-functional** - Performance, security, UX
3. **Edge cases** - Error handling, boundaries
4. **Integration** - How it connects to existing code

## Actions

1. **Parse request** - Extract explicit requirements
2. **Analyze context** - Infer implicit requirements
3. **Check for gaps** - Identify missing information
4. **Document** - Write to WORKING_MEMORY

## Skill Return Format

```markdown
## Skill Return
- **Skill**: swe-workflow-detect-req
- **Status**: [success|needs_clarification]
- **Findings Summary**: [requirements discovered]
- **Artifacts**: [requirement list]
- **Next Step Hint**: WF_LOAD_FEATURE
```

## Exit

`> **Skill /swe-workflow-detect-req complete** - returning to WF_LOAD_FEATURE`
