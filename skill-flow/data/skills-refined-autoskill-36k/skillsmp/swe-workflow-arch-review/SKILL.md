---
name: swe-workflow-arch-review
version: 1.0.0
description: Review architecture compliance before execution
workflow:
  aware: true
  callable_from:
    - WF_LOAD_FEATURE
    - WF_CONTINUE
  default_return: WF_ASK_PERMISSION
  supports_standalone: false
  auto_transition: true
---

# Workflow Architecture Review Skill

Review proposed changes against architecture standards.

## Purpose

- Verify changes align with existing architecture
- Check layer boundaries respected
- Validate naming conventions
- Ensure patterns are followed

## Actions

1. **Read ARCH_INDEX** - Understand current architecture
2. **Read FEATURE_* memories** - Get feature context
3. **Check patterns** - Verify against established patterns
4. **Validate approach** - Ensure implementation plan is sound

## Review Criteria

- [ ] Layer boundaries respected
- [ ] Naming conventions followed
- [ ] Dependencies flow correctly
- [ ] No circular dependencies introduced
- [ ] Consistent with existing patterns

## Skill Return Format

```markdown
## Skill Return
- **Skill**: swe-workflow-arch-review
- **Status**: [success|success_with_findings|blocked]
- **Findings Summary**: [architecture compliance assessment]
- **Artifacts**: [patterns checked, issues found]
- **Next Step Hint**: [WF_ASK_PERMISSION if approved, WF_PLAN_ARCHITECTURE if revision needed]
```

## Exit

On approval: `> **Skill /swe-workflow-arch-review passed** - returning to WF_ASK_PERMISSION`
On revision needed: `> **Skill /swe-workflow-arch-review needs revision** - returning to WF_PLAN_ARCHITECTURE`
