# Pull Request Description Templates

Comprehensive PR templates for different types of changes.

## Standard Feature PR Template

```markdown
## Summary

[Brief description of what this PR does and why]

## Changes

- [List key changes]
- [Be specific about what was added/modified]
- [Include architectural decisions]

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [x] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring
- [ ] Dependency update

## Testing

- [x] Unit tests added/updated
- [x] Integration tests added/updated
- [x] Manual testing completed
- [ ] Performance testing completed
- [ ] Accessibility testing completed

## Test Plan

1. [Step-by-step testing instructions]
2. [How to verify the changes work]
3. [What to look for in testing]

## Screenshots / Videos

[If UI changes, add screenshots or videos]

## Performance Impact

[Describe any performance implications]
- Before: [metric]
- After: [metric]

## Breaking Changes

[Describe any breaking changes and migration path]

## Related Issues

Closes #[issue number]
Related to #[issue number]

## Checklist

- [x] Code follows project style guidelines
- [x] Self-review completed
- [x] Comments added for complex logic
- [x] Documentation updated
- [x] No new warnings generated
- [x] Tests pass locally
- [x] Dependent changes merged
- [x] Ready for production deployment
```

## Bug Fix PR Template

```markdown
## Bug Description

[Describe the bug that this PR fixes]

## Root Cause

[Explain the root cause of the bug]

## Solution

[Describe how the bug is fixed]

## Testing

- [x] Added regression test to prevent recurrence
- [x] Verified fix in development environment
- [x] Tested edge cases
- [x] Verified no side effects

## Steps to Reproduce Original Bug

1. [Step 1]
2. [Step 2]
3. [Expected vs actual behavior]

## Verification Steps

1. [How to verify the bug is fixed]
2. [What to check]
3. [Expected behavior after fix]

## Impact

- **Severity**: [Critical / High / Medium / Low]
- **Users Affected**: [Number or percentage]
- **Workaround**: [Any existing workaround]

## Related Issues

Fixes #[issue number]

## Checklist

- [x] Root cause identified and documented
- [x] Regression test added
- [x] Edge cases tested
- [x] No side effects introduced
- [x] Ready for hotfix deployment (if critical)
```

## Refactoring PR Template

```markdown
## Refactoring Summary

[Describe what code is being refactored and why]

## Motivation

[Explain the reasoning behind this refactoring]
- [Improved maintainability]
- [Better performance]
- [Clearer code structure]
- [Reduced duplication]

## Changes

- [List structural changes]
- [Highlight any patterns introduced]
- [Note any dependencies changed]

## Before/After Comparison

### Before
```
[Code snippet or structure before]
```

### After
```
[Code snippet or structure after]
```

## Impact

- **Lines Changed**: +[X] -[Y]
- **Files Changed**: [N]
- **Performance**: [Improved / Same / N/A]
- **Bundle Size**: [Changed by X KB or N/A]

## Validation

- [x] All existing tests pass
- [x] No functional changes (behavior identical)
- [x] Code coverage maintained or improved
- [x] Performance benchmarks run

## Breaking Changes

None (this is a refactoring with no functional changes)

## Checklist

- [x] All tests pass
- [x] No functional changes
- [x] Code is more maintainable
- [x] Documentation updated if needed
- [x] Performance validated
```

## Documentation PR Template

```markdown
## Documentation Changes

[Summary of documentation updates]

## Type of Documentation

- [x] API documentation
- [ ] User guide
- [ ] Developer guide
- [ ] README
- [ ] Code comments
- [ ] Architecture documentation
- [ ] Changelog

## Changes

- [List specific documentation changes]
- [Note any new sections added]
- [Highlight any corrections made]

## Motivation

[Why these documentation changes are needed]

## Verification

- [x] Documentation builds without errors
- [x] All links are valid
- [x] Code examples are tested and working
- [x] Screenshots/diagrams are up to date
- [x] Spelling and grammar checked

## Related Code Changes

[Link to related PRs if documentation is for new features]

## Checklist

- [x] Documentation is accurate
- [x] Examples are tested
- [x] Links are valid
- [x] Images/diagrams included
- [x] Clear and understandable
```

## Performance Improvement PR Template

```markdown
## Performance Improvement

[Describe the performance optimization]

## Problem

[Explain the performance bottleneck]
- [What was slow]
- [Impact on users]
- [Metrics before optimization]

## Solution

[Describe the optimization approach]
- [What was changed]
- [Why this approach]
- [Any trade-offs]

## Benchmarks

### Before
- [Metric 1]: [Value]
- [Metric 2]: [Value]
- [Metric 3]: [Value]

### After
- [Metric 1]: [Value] ([% improvement])
- [Metric 2]: [Value] ([% improvement])
- [Metric 3]: [Value] ([% improvement])

### Test Environment
- [Hardware specs]
- [Test data size]
- [Methodology]

## Changes

- [List technical changes]
- [Database indexes added]
- [Caching implemented]
- [Algorithm optimized]

## Trade-offs

[Describe any trade-offs made]
- [Memory vs speed]
- [Complexity vs performance]
- [Accuracy vs speed]

## Testing

- [x] Performance benchmarks run
- [x] Load testing completed
- [x] Memory profiling done
- [x] No regression in functionality
- [x] Edge cases tested

## Checklist

- [x] Benchmarks show improvement
- [x] No functional regression
- [x] Trade-offs documented
- [x] Monitoring added for metrics
```

## Security Fix PR Template

```markdown
## 🚨 Security Fix

[Brief description of the security issue]

## Severity

**CVSS Score**: [X.X]
**Severity**: [Critical / High / Medium / Low]

## Vulnerability Description

[Describe the security vulnerability]
- **Type**: [SQL Injection / XSS / CSRF / etc.]
- **Attack Vector**: [How it could be exploited]
- **Impact**: [What an attacker could do]

## Root Cause

[Explain the root cause of the vulnerability]

## Fix

[Describe how the vulnerability is patched]

## Affected Versions

- **Vulnerable**: [v1.0.0 - v1.2.3]
- **Fixed in**: [v1.2.4]

## Security Testing

- [x] Exploit attempt blocked
- [x] Security tests added
- [x] Penetration testing performed
- [x] Security team reviewed

## Disclosure

- **CVE**: [CVE-YYYY-XXXXX or Pending]
- **Disclosed to**: [Security team]
- **Public disclosure date**: [Date or After patch deployment]

## Deployment Priority

**URGENT**: This fix should be deployed immediately.

## Breaking Changes

[Any breaking changes required for security]

## Migration Guide

[If breaking changes, provide migration steps]

## Checklist

- [x] Security team notified
- [x] Fix verified by security expert
- [x] Regression tests added
- [x] Documentation updated
- [x] Security advisory prepared
```

## Breaking Change PR Template

```markdown
## ⚠️ Breaking Change

[Brief description of the breaking change]

## Motivation

[Why is this breaking change necessary]
- [Technical debt]
- [New architecture]
- [Security]
- [Performance]

## Breaking Changes

### Change 1: [Description]

**Before**:
```
[Code example before]
```

**After**:
```
[Code example after]
```

**Impact**: [Who is affected and how]

### Change 2: [Description]

[Repeat for each breaking change]

## Migration Guide

### Automated Migration

```bash
[Script or command to automate migration if available]
```

### Manual Migration

1. [Step 1]
2. [Step 2]
3. [Step 3]

### Example Migration

**Before**:
```
[Full example before]
```

**After**:
```
[Full example after]
```

## Deprecation Plan

- **Deprecation Notice**: [Version where deprecated]
- **Removal**: [Version where removed]
- **Support Period**: [How long old version is supported]

## Affected Users

- **Estimated Impact**: [% of users or specific features]
- **Notification Plan**: [How users will be notified]

## Testing

- [x] Migration path tested
- [x] Backward compatibility verified (if applicable)
- [x] Documentation updated
- [x] Changelog updated
- [x] Communication plan ready

## Checklist

- [x] Breaking changes documented
- [x] Migration guide complete
- [x] Version bumped appropriately (major version)
- [x] Users will be notified
- [x] Support plan in place
```

## Dependency Update PR Template

```markdown
## Dependency Update

[Description of dependency updates]

## Updated Dependencies

### Production Dependencies

- [package-name]: [old-version] → [new-version]
  - [Release notes link]
  - [Key changes]

### Development Dependencies

- [package-name]: [old-version] → [new-version]

## Motivation

- [ ] Security vulnerability fix
- [x] New features needed
- [ ] Bug fixes
- [ ] Performance improvements
- [ ] Keep dependencies current

## Changes Required

[Any code changes needed due to updated dependencies]

## Breaking Changes

[Any breaking changes in the dependencies]

## Testing

- [x] All tests pass
- [x] Manual testing completed
- [x] No regression
- [x] New features verified (if applicable)

## Security

- [x] No known vulnerabilities
- [x] Security audit passed
- [x] Dependencies from trusted sources

## Checklist

- [x] Lock file updated
- [x] Tests pass
- [x] No breaking changes (or documented)
- [x] Security verified
```

## Hotfix PR Template

```markdown
## 🔥 Hotfix

[Brief description of the critical issue being fixed]

## Severity

**Priority**: URGENT
**Severity**: [Critical / High]
**Affected Users**: [Number or percentage]

## Issue

[Describe the production issue]
- **Symptom**: [What users are experiencing]
- **Impact**: [Business/user impact]
- **Started**: [When issue started]

## Root Cause

[Explain what caused the issue]

## Fix

[Describe the fix]

## Testing

- [x] Fix verified in development
- [x] Fix verified in staging
- [x] Tested edge cases
- [x] No side effects found

## Rollback Plan

[How to rollback if fix causes issues]

## Deployment Plan

1. [Step 1]
2. [Step 2]
3. [Verification step]

## Monitoring

[What to monitor after deployment]
- [Metric 1]
- [Metric 2]
- [Error rates]

## Communication

- [x] Stakeholders notified
- [x] Users notified (if applicable)
- [x] Post-mortem scheduled

## Related Issues

Fixes #[issue number]

## Checklist

- [x] Fix verified
- [x] Minimal changes (focused fix only)
- [x] Deployment plan ready
- [x] Rollback plan ready
- [x] Monitoring in place
```

## UI/UX Change PR Template

```markdown
## UI/UX Changes

[Description of UI/UX changes]

## Motivation

[Why these changes are being made]
- [User feedback]
- [Usability improvements]
- [Design system alignment]
- [Accessibility]

## Changes

- [List visual changes]
- [Interaction changes]
- [Layout changes]

## Screenshots / Videos

### Before
[Screenshot/video of old UI]

### After
[Screenshot/video of new UI]

### Mobile View
[Mobile screenshots if responsive]

## Accessibility

- [x] Keyboard navigation works
- [x] Screen reader compatible
- [x] Color contrast meets WCAG AA
- [x] Focus indicators visible
- [x] ARIA labels added

## Browser Compatibility

- [x] Chrome
- [x] Firefox
- [x] Safari
- [x] Edge
- [x] Mobile browsers

## Responsive Design

- [x] Desktop (1920px)
- [x] Laptop (1366px)
- [x] Tablet (768px)
- [x] Mobile (375px)

## Testing

- [x] Visual regression tests updated
- [x] Cross-browser testing completed
- [x] Mobile testing completed
- [x] Accessibility testing completed

## Checklist

- [x] Design approved
- [x] Responsive design verified
- [x] Accessibility standards met
- [x] Cross-browser compatible
```

## Usage Guidelines

### Choosing the Right Template

1. **Feature PR**: New functionality being added
2. **Bug Fix PR**: Fixing existing issues
3. **Refactoring PR**: Code restructuring without functional changes
4. **Documentation PR**: Documentation updates only
5. **Performance PR**: Optimization and performance improvements
6. **Security PR**: Security vulnerabilities and fixes
7. **Breaking Change PR**: Changes that break backward compatibility
8. **Dependency Update PR**: Updating third-party dependencies
9. **Hotfix PR**: Critical production issues
10. **UI/UX PR**: User interface and experience changes

### Customization

Templates should be customized for your project:
- Add project-specific sections
- Remove sections that don't apply
- Adjust checklists for your workflow
- Add required approvers or reviewers

### Automation

Many platforms support PR templates:

**GitHub**: `.github/pull_request_template.md`
**GitLab**: `.gitlab/merge_request_templates/`
**Bitbucket**: Pull request templates in repository settings

### Best Practices

1. **Be thorough**: Complete all relevant sections
2. **Be specific**: Provide concrete details
3. **Add context**: Explain the "why" not just "what"
4. **Include testing**: Show what was tested
5. **Link issues**: Reference related issues/tickets
6. **Self-review**: Review your own PR before requesting review
7. **Keep updated**: Update PR as changes are made
