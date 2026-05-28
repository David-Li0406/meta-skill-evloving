# Code Review Checklist

Comprehensive checklist for PR authors and reviewers.

## For PR Authors

### Before Requesting Review

- [ ] Self-reviewed all changes
- [ ] Tests pass locally
- [ ] No debugging code left
- [ ] No commented-out code
- [ ] Commit messages follow convention
- [ ] Branch is up to date with base

### Code Quality

- [ ] No code duplication
- [ ] Functions are small and focused
- [ ] Variable names are descriptive
- [ ] Complex logic has comments
- [ ] Error handling is appropriate

### Security

- [ ] No secrets in code
- [ ] Input validation present
- [ ] SQL injection prevented
- [ ] XSS prevention in place
- [ ] Authentication/authorization checked

### Documentation

- [ ] README updated if needed
- [ ] API documentation updated
- [ ] Code comments for complex logic
- [ ] Changelog entry added

## For Reviewers

### Functionality

| Check | Status |
|-------|--------|
| Does it solve the stated problem? | |
| Are edge cases handled? | |
| Is error handling appropriate? | |
| Are there any race conditions? | |
| Does it work with existing features? | |

### Code Quality

| Check | Status |
|-------|--------|
| Is the code readable? | |
| Are functions well-named? | |
| Is there unnecessary complexity? | |
| Are there any code smells? | |
| Does it follow project patterns? | |

### Testing

| Check | Status |
|-------|--------|
| Are there sufficient tests? | |
| Do tests cover edge cases? | |
| Are tests maintainable? | |
| Is test coverage acceptable? | |

### Performance

| Check | Status |
|-------|--------|
| Any N+1 queries? | |
| Unnecessary loops? | |
| Memory leaks possible? | |
| Large payload handling? | |

### Security

| Check | Status |
|-------|--------|
| Input validated? | |
| Output escaped? | |
| Auth/authz correct? | |
| No sensitive data logged? | |

## Review Comments

### Comment Types

**Question**: Ask for clarification
```
❓ Why is this check needed here? Couldn't we rely on the upstream validation?
```

**Suggestion**: Propose improvement
```
💡 Consider using `useMemo` here to avoid recalculating on every render.
```

**Issue**: Must be fixed
```
🚫 This will cause a null pointer exception when `user` is undefined.
```

**Nitpick**: Optional improvement
```
🔍 Nit: Could rename `x` to `userCount` for clarity.
```

**Praise**: Acknowledge good work
```
✨ Nice refactor! This is much cleaner than the previous implementation.
```

## Approval Guidelines

### Approve When

- All blocking issues resolved
- Tests pass
- Code meets quality standards
- Security concerns addressed

### Request Changes When

- Security vulnerabilities present
- Critical bugs found
- Missing error handling
- Breaking changes without migration

### Comment Only When

- Minor suggestions
- Questions need answers
- Non-blocking improvements

## Review Etiquette

### For Authors

- Respond to all comments
- Don't take feedback personally
- Ask for clarification if needed
- Update PR based on feedback

### For Reviewers

- Be constructive and specific
- Explain the "why" behind suggestions
- Acknowledge good practices
- Review promptly (within 24h)
