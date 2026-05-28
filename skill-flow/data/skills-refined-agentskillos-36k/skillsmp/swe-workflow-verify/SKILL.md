---
name: swe-workflow-verify
version: 1.0.0
description: Verify implementation against requirements and standards
workflow:
  aware: true
  callable_from:
    - WF_EXECUTE
    - WF_CHECKPOINT
  default_return: WF_DONE
  supports_standalone: false
  auto_transition: true
---

# Workflow Verify Skill

Verify implementation completeness and quality.

## Purpose

- Run test suites
- Check against requirements
- Verify coding standards compliance
- Ensure no regressions

## Actions

1. **Run tests** - Execute relevant test commands
2. **Check requirements** - Compare implementation to documented requirements
3. **Verify standards** - Check against CLAUDE_OBLIGATIONS and REF_DEV_STANDARDS
4. **Lint/format check** - Run linters if configured

## Verification Checklist

- [ ] All tests pass
- [ ] Requirements met
- [ ] Coding standards followed
- [ ] No security vulnerabilities introduced
- [ ] Documentation updated if needed

## Skill Return Format

```markdown
## Skill Return
- **Skill**: swe-workflow-verify
- **Status**: [success|success_with_findings|blocked]
- **Findings Summary**: [verification results]
- **Artifacts**: [test results, lint output]
- **Next Step Hint**: [WF_DONE if passed, WF_EXECUTE if failed]
```

## Exit

On success: `> **Skill /swe-workflow-verify complete** - returning to WF_DONE`
On failure: `> **Skill /swe-workflow-verify failed** - returning to WF_EXECUTE for fixes`
