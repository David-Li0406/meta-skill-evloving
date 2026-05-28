---
name: pr-checklist
description: Generate a PR checklist based on changes
---

# PR Checklist Generator

Generate a comprehensive PR checklist based on the changes:

## Analyze Changes

First, I'll analyze:

1. What files were changed?
2. What type of changes (feature, bugfix, refactor)?
3. What systems are affected?

## Standard Checklist

### Code Quality

- [ ] Code follows project style guidelines
- [ ] No linting errors
- [ ] Types are properly defined
- [ ] No console.log or debug code
- [ ] Complex logic is commented

### Testing

- [ ] Unit tests added/updated
- [ ] Integration tests if needed
- [ ] Edge cases covered
- [ ] All tests passing

### Security

- [ ] No hardcoded secrets
- [ ] Input is validated
- [ ] Authorization checks in place
- [ ] No SQL/XSS vulnerabilities

### Performance

- [ ] No obvious performance issues
- [ ] Database queries optimized
- [ ] Appropriate caching

### Documentation

- [ ] README updated if needed
- [ ] API documentation updated
- [ ] Inline comments for complex code

## Change-Specific Items

Based on the specific changes, add relevant items:

### If Database Changes

- [ ] Migration tested locally
- [ ] Rollback plan exists
- [ ] RLS policies added

### If API Changes

- [ ] API documentation updated
- [ ] Backwards compatible
- [ ] Error responses documented

### If UI Changes

- [ ] Responsive design verified
- [ ] Accessibility checked
- [ ] Loading states handled

Generate the full checklist tailored to this PR.
