# Writing Good Acceptance Criteria

Acceptance criteria define when an issue is complete. Good criteria are specific, testable, and unambiguous.

## The INVEST Principle

Good acceptance criteria follow INVEST:

- **I**ndependent - Can be completed without other stories
- **N**egotiable - Details can be discussed
- **V**aluable - Delivers value to users
- **E**stimable - Can estimate effort
- **S**mall - Completable in one sprint
- **T**estable - Can verify completion

## Format: Given-When-Then

The most rigorous format for acceptance criteria:

```
Given [precondition/context]
When [action is taken]
Then [expected result]
```

### Examples

```markdown
## User Login

Given a registered user with valid credentials
When they enter their email and password and click "Login"
Then they are redirected to the dashboard

Given a user with invalid credentials
When they attempt to login
Then they see "Invalid email or password" error
And they remain on the login page
And the attempt is logged for security

Given a user who is locked out
When they attempt to login
Then they see "Account locked. Try again in 15 minutes."
```

## Format: Checkbox List

Simpler format for most issues:

```markdown
## Acceptance Criteria

- [ ] User can log in with email and password
- [ ] Error message shown for invalid credentials
- [ ] Session expires after 24 hours of inactivity
- [ ] "Remember me" extends session to 30 days
- [ ] Failed attempts are rate-limited (5/minute)
```

## Good vs Bad Criteria

### ❌ Bad: Vague

```markdown
- [ ] It works
- [ ] Users are happy
- [ ] Fast enough
- [ ] Looks good
- [ ] No bugs
```

### ✅ Good: Specific and Testable

```markdown
- [ ] Page loads in under 2 seconds on 3G connection
- [ ] Form validation errors appear within 100ms
- [ ] All text meets WCAG AA contrast requirements
- [ ] Works on Chrome, Firefox, Safari (latest 2 versions)
- [ ] Zero console errors in normal usage flow
```

## Categories of Criteria

### Functional Criteria

What the feature must DO:

```markdown
- [ ] User can upload files up to 10MB
- [ ] Supported formats: PDF, PNG, JPG
- [ ] Upload progress shown during transfer
- [ ] Files are virus-scanned before storage
- [ ] Uploaded files appear in user's file list
```

### Performance Criteria

How fast/efficient it must be:

```markdown
- [ ] API response time < 200ms (p95)
- [ ] Page load time < 3s on 3G
- [ ] Memory usage < 100MB
- [ ] Supports 1000 concurrent users
- [ ] Database queries < 50ms
```

### Security Criteria

How it must protect data:

```markdown
- [ ] Input validated against injection attacks
- [ ] Files scanned for malware
- [ ] Access logged for audit trail
- [ ] Sensitive data encrypted at rest
- [ ] Authentication required for all endpoints
```

### Accessibility Criteria

How it must be accessible:

```markdown
- [ ] All images have alt text
- [ ] Keyboard navigation works
- [ ] Screen reader announces changes
- [ ] Color contrast meets WCAG AA
- [ ] Focus states are visible
```

### Documentation Criteria

What documentation is needed:

```markdown
- [ ] API endpoints documented in OpenAPI spec
- [ ] README updated with new feature
- [ ] Inline code comments for complex logic
- [ ] Changelog entry added
- [ ] User guide updated
```

### Testing Criteria

What tests are required:

```markdown
- [ ] Unit tests for all new functions
- [ ] Integration tests for API endpoints
- [ ] E2E test for happy path
- [ ] Edge cases covered
- [ ] Test coverage > 80%
```

## Templates by Issue Type

### Bug Fix

```markdown
## Acceptance Criteria

- [ ] Bug no longer reproducible with original steps
- [ ] Root cause identified and documented
- [ ] Regression test added
- [ ] No new bugs introduced
- [ ] Fix works on all supported platforms
```

### New Feature

```markdown
## Acceptance Criteria

### Functional
- [ ] [Core functionality works]
- [ ] [Edge cases handled]

### Quality
- [ ] Unit tests added (coverage > 80%)
- [ ] Integration tests for API changes
- [ ] No accessibility violations

### Documentation
- [ ] API documentation updated
- [ ] User-facing docs updated
- [ ] Changelog entry added
```

### Refactoring

```markdown
## Acceptance Criteria

- [ ] All existing tests pass
- [ ] No functional changes (behavior identical)
- [ ] Performance equal or better
- [ ] Code complexity reduced (measured by [tool])
- [ ] Technical debt documented if remaining
```

### Performance Improvement

```markdown
## Acceptance Criteria

- [ ] [Metric] improved by [X]%
- [ ] Before/after benchmarks documented
- [ ] No functional regressions
- [ ] Improvement verified in production-like environment
- [ ] Monitoring in place to track metric
```

## Anti-Patterns to Avoid

### Too Many Criteria

If you have 20+ acceptance criteria, the issue is too big. Split it.

### Implementation Details

```markdown
# ❌ Bad - Specifies HOW
- [ ] Use Redis for caching
- [ ] Implement with React hooks
- [ ] Query uses LEFT JOIN

# ✅ Good - Specifies WHAT
- [ ] Response cached for 5 minutes
- [ ] UI updates without page reload
- [ ] Query returns in < 50ms
```

### Obvious Criteria

```markdown
# ❌ Bad - Stating the obvious
- [ ] Code is written
- [ ] Code is committed
- [ ] PR is created

# ✅ Good - Meaningful criteria
- [ ] Code reviewed and approved
- [ ] CI pipeline passes
- [ ] Deployed to staging
```

## Review Checklist

Before finalizing acceptance criteria, verify:

- [ ] Each criterion is independently testable
- [ ] No criterion requires interpretation
- [ ] Criteria cover happy path AND error cases
- [ ] Performance expectations are specific
- [ ] Security implications are addressed
- [ ] Documentation needs are included
- [ ] Testing requirements are clear
