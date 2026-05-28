# Run Milestone Skill

Automates milestone development with an autopilot PR workflow.

## Usage

```
/run-milestone m1
```

## What It Does

1. Reads the implementation plan for the specified milestone
2. Finds the next unblocked issue
3. Implements the issue following the spec
4. Creates a PR with auto-merge enabled
5. Continues to the next issue

## Stop Conditions

**Hard Stops** (requires your attention):
- Database migrations
- Auth/security code changes
- Dependency changes
- Missing/unclear specs

**Soft Stops** (auto-skips to next issue):
- Test failures after attempted fixes
- Large diffs (>8 files or >400 lines)
- Merge conflicts

## Files

- `SKILL.md` - Full skill specification
- `README.md` - This file

## See Also

- [Development Cadence](../../../docs/guides/dev-cadence.md)
- [Implementation Workflow](../../../docs/guides/implementation-workflow.md)
