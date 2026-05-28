# Pull Request Templates

Ready-to-use templates for different PR types.

## Standard Feature PR

```markdown
## Summary

Brief description of the feature and its purpose.

## Related Issue

Closes: PROJ-123

## Changes

- Added new component for X
- Updated API endpoint for Y
- Modified database schema for Z

## Screenshots

(if applicable)

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Edge cases covered

## Checklist

- [ ] Code follows project style
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No secrets committed
- [ ] Breaking changes documented
```

## Bug Fix PR

```markdown
## Bug Description

What was the bug and how did it manifest?

## Root Cause

What caused this bug?

## Fix

How does this PR fix the issue?

## Related Issue

Fixes: PROJ-456

## Testing

- [ ] Added regression test
- [ ] Verified fix in local environment
- [ ] Tested related functionality

## Risk Assessment

- [ ] Low risk - isolated change
- [ ] Medium risk - affects related features
- [ ] High risk - core functionality change
```

## Hotfix PR

```markdown
## 🚨 HOTFIX

**Severity**: Critical / High / Medium
**Affected Environment**: Production / Staging

## Issue

Brief description of the production issue.

## Fix

What change resolves the issue?

## Impact

- Users affected: X
- Duration of issue: Y
- Rollback plan: Z

## Verification

- [ ] Fix verified in staging
- [ ] Monitoring in place
- [ ] Rollback tested

## Post-Mortem

Link to incident report: [INCIDENT-XXX]
```

## Refactoring PR

```markdown
## Refactoring Scope

What code is being refactored and why?

## Motivation

- Performance improvement
- Code maintainability
- Technical debt reduction
- Preparation for future feature

## Changes

- Before: [description]
- After: [description]

## Verification

- [ ] No behavior changes
- [ ] All existing tests pass
- [ ] Performance benchmarks (if applicable)

## Migration Notes

Any steps needed for other developers?
```

## Documentation PR

```markdown
## Documentation Update

What documentation is being added/updated?

## Type

- [ ] API documentation
- [ ] User guide
- [ ] Developer guide
- [ ] README update
- [ ] Code comments

## Changes

- Added section on X
- Updated examples for Y
- Fixed typos in Z

## Preview

Link to preview if available.
```

## Dependency Update PR

```markdown
## Dependency Updates

| Package | From | To | Changelog |
|---------|------|-----|-----------|
| package-a | 1.0.0 | 2.0.0 | [link] |
| package-b | 3.1.0 | 3.2.0 | [link] |

## Breaking Changes

List any breaking changes from updated dependencies.

## Testing

- [ ] Build passes
- [ ] All tests pass
- [ ] Manual smoke test

## Rollback

```bash
npm install package-a@1.0.0 package-b@3.1.0
```
```

## Multi-Part PR (Large Feature)

```markdown
## Part X of Y: Feature Name

This PR is part of a larger feature. See epic: PROJ-100

## Previous PRs
- Part 1: #123 (merged)
- Part 2: #124 (merged)

## This PR

What this specific part implements.

## Next Steps

What will be implemented in subsequent PRs.

## Testing

- [ ] This part is independently testable
- [ ] Feature flag enabled: `FEATURE_X`

## Merge Order

Must be merged after: #124
```
