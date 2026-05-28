# GitHub Pull Request Guidelines (5W1H Principle)

> **Version**: 1.2.0
> **Extracted from**: workflow.md
> **Purpose**: Framework for creating effective pull requests

When creating Pull Requests, follow the **5W1H framework** to ensure reviewers can quickly understand and effectively evaluate your changes.

## Language and Attribution Policy

### Language Requirement

**All PRs MUST be written in English** for:
- Global accessibility and collaboration
- Consistency with codebase and documentation standards
- Integration with automated tools and CI/CD systems
- Effective code review across international teams

```markdown
<!-- ✅ Correct: English PR -->
## Summary
Implements JWT-based authentication for the REST API...

<!-- ❌ Incorrect: Non-English PR -->
## 요약
REST API를 위한 JWT 기반 인증을 구현...
```

### No AI/Claude Attribution

**Exclude all AI-related references** from PRs:

```markdown
<!-- ❌ Do NOT include -->
🤖 Generated with [Claude Code](https://claude.com/claude-code)
Created with AI assistance
Co-Authored-By: Claude <noreply@anthropic.com>

<!-- ❌ Do NOT include in footer -->
---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

This policy ensures:
- Professional appearance in public repositories
- Focus on the technical content
- Compliance with organizational standards

### Correct PR Footer Example

```markdown
## Checklist
- [x] Code follows project style guidelines
- [x] Self-review completed
- [x] Tests added/updated
```

**Do NOT add any AI attribution after the checklist.**

## 1. What

**Describe the changes made**

- **Title**: Use conventional commit format: `type(scope): description`
- **Summary**: Brief overview of changes (2-3 sentences max)
- **Change type**: Feature, bugfix, refactor, docs, test, chore
- **Affected components**: List modified modules, services, or layers

```markdown
## What

### Summary
Implements JWT-based authentication for the REST API, including user registration,
login, and token refresh endpoints.

### Change Type
- [x] Feature (new functionality)
- [ ] Bugfix (fixes an issue)
- [ ] Refactor (no functional changes)
- [ ] Documentation
- [ ] Test

### Affected Components
- `src/auth/` - New authentication service
- `src/middleware/` - Auth middleware added
- `src/routes/` - New auth routes
```

## 2. Why

**Explain the motivation for these changes**

- **Problem solved**: What issue does this PR address?
- **Related issue**: Link to the issue(s) this PR resolves
- **Business value**: How does this benefit users or the project?
- **Alternative approaches**: Why was this approach chosen over others?

```markdown
## Why

### Problem Solved
Users currently cannot securely access their personal data. This PR implements
authentication to protect user resources and enable personalized features.

### Related Issues
- Closes #142 (Implement user authentication)
- Relates to #125 (Frontend login page)

### Alternative Approaches Considered
1. Session-based auth - Rejected due to stateless API requirement
2. OAuth only - Deferred to future PR for social login
```

### Issue Linking Requirements (MANDATORY)

**Every PR MUST link to at least one issue** unless it's a trivial fix (typo, formatting).

#### Required Actions When Creating a PR

1. **In PR Description**: Use closing keywords to link issues
2. **In Related Issue**: Add a comment with PR information

#### Closing Keywords

Use these keywords in PR descriptions to automatically close issues on merge:

| Keyword | Example | Effect |
|---------|---------|--------|
| `Closes` | `Closes #123` | Closes issue when PR merges |
| `Fixes` | `Fixes #123` | Closes issue when PR merges |
| `Resolves` | `Resolves #123` | Closes issue when PR merges |

For related but not closing issues:

| Keyword | Example | Effect |
|---------|---------|--------|
| `Relates to` | `Relates to #123` | Links without closing |
| `Part of` | `Part of #123` | Indicates partial implementation |
| `See also` | `See also #123, #124` | Related references |

#### Issue Update Requirement

**MANDATORY**: After creating a PR, add a comment to the linked issue(s):

```markdown
## 📋 Implementation Update

| Field | Value |
|-------|-------|
| **PR** | #[PR_NUMBER] |
| **Branch** | `[BRANCH_NAME]` |
| **Status** | 👀 In Review |

### Summary
Brief description of the implementation approach.
```

#### Multiple Issues Example

```markdown
## Related Issues

### Primary
- Closes #142 (Implement user authentication)

### Secondary
- Relates to #125 (Frontend login page) - This PR provides backend endpoints
- Part of #100 (Epic: User Management) - First step of the epic

### Blocking
- Blocks #150 (Password reset feature) - Needs auth endpoints from this PR
```

## 3. Who

**Identify reviewers and stakeholders**

- **Reviewers**: Who should review this PR? (code owner, domain expert)
- **Stakeholders**: Who is affected by these changes?
- **Sign-off required**: Does this need approval from specific roles?

```markdown
## Who

### Reviewers
- @security-lead - Security review required
- @backend-team - Code review

### Stakeholders
- Backend team (new patterns introduced)
- Frontend team (new API endpoints to consume)
- QA team (new test scenarios)

### Required Approvals
- [ ] Security team sign-off
- [ ] Backend lead approval
```

## 4. When

**Provide timeline and urgency context**

- **Urgency**: Normal, high priority, or hotfix?
- **Target release**: Which version or sprint?
- **Deployment notes**: Any timing considerations for deployment?
- **Dependencies**: PRs that must be merged before/after this

```markdown
## When

### Urgency
- [x] Normal - Follow standard review process
- [ ] High Priority - Needed for upcoming release
- [ ] Hotfix - Production issue, expedite review

### Target Release
v2.0.0 (Sprint 15)

### Deployment Notes
- Requires database migration before deployment
- Should be deployed during low-traffic window

### Dependencies
- Depends on: #140 (Database schema changes) - Already merged
- Blocks: #145 (Password reset feature)
```

## 5. Where

**Specify scope and impact areas**

- **Files changed**: Summary of file modifications
- **Architecture impact**: Does this change system architecture?
- **API changes**: New, modified, or deprecated endpoints
- **Database changes**: Schema modifications, migrations

```markdown
## Where

### Files Changed
| Directory | Files | Type of Change |
|-----------|-------|----------------|
| `src/auth/` | 5 | New service |
| `src/middleware/` | 2 | New middleware |
| `src/routes/` | 3 | New endpoints |
| `tests/auth/` | 8 | New tests |

### API Changes
| Endpoint | Method | Status |
|----------|--------|--------|
| `/auth/register` | POST | New |
| `/auth/login` | POST | New |
| `/auth/refresh` | POST | New |
| `/auth/logout` | POST | New |

### Database Changes
- New table: `refresh_tokens`
- Migration: `20241201_add_refresh_tokens.sql`
```

## 6. How

**Explain implementation and verification**

- **Implementation details**: Key technical decisions and approach
- **Testing done**: What testing has been performed?
- **Test plan**: How should reviewers verify this works?
- **Screenshots/Demos**: Visual evidence for UI changes
- **Breaking changes**: Any backward incompatibility?
- **Rollback plan**: How to revert if issues arise?

```markdown
## How

### Implementation Details
1. JWT tokens using RS256 algorithm with rotating keys
2. Access tokens expire in 15 minutes, refresh tokens in 7 days
3. Refresh tokens stored in database with device fingerprinting
4. Rate limiting: 5 login attempts per minute per IP

### Testing Done
- [x] Unit tests (47 new, all passing)
- [x] Integration tests (12 new, all passing)
- [x] Manual testing with Postman
- [x] Load testing (1000 concurrent logins)
- [ ] Security penetration testing (scheduled)

### Test Plan for Reviewers
1. Run `npm test` - All tests should pass
2. Start server: `npm run dev`
3. Test registration: `POST /auth/register` with valid payload
4. Test login: `POST /auth/login` and verify JWT returned
5. Test protected route with/without token

### Breaking Changes
- None - New endpoints only

### Rollback Plan
1. Revert this PR
2. Run down migration: `npm run migrate:down`
3. No data loss - new tables only
```

## Pull Request Template

```markdown
## What

### Summary
<!-- Brief description of changes (2-3 sentences) -->

### Change Type
- [ ] Feature
- [ ] Bugfix
- [ ] Refactor
- [ ] Documentation
- [ ] Test
- [ ] Chore

## Why

### Related Issues
<!-- Closes #issue_number -->

### Motivation
<!-- Why are these changes needed? -->

## Who

### Reviewers
<!-- @mention required reviewers -->

### Required Approvals
- [ ] Code owner
- [ ] Security review (if applicable)

## When

### Urgency
- [ ] Normal
- [ ] High Priority
- [ ] Hotfix

### Target Release
<!-- Version or sprint -->

## Where

### Files Changed Summary
<!-- Overview of modified areas -->

### API/Database Changes
<!-- List any interface or schema changes -->

## How

### Implementation Highlights
<!-- Key technical decisions -->

### Testing Done
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

### Test Plan
<!-- Steps for reviewers to verify -->

### Breaking Changes
<!-- List any breaking changes or "None" -->

## Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No sensitive data exposed
- [ ] Commits are atomic and well-described
- [ ] Related issue(s) linked with closing keywords
- [ ] Comment added to related issue(s) with PR information
```

> **Note**: Do NOT add any AI attribution (Claude, GPT, etc.) after this checklist.

## Quick Reference

### PR Title Conventions

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add JWT authentication` |
| `fix` | Bug fix | `fix(api): resolve null pointer in user service` |
| `refactor` | Code refactoring | `refactor(db): optimize query performance` |
| `docs` | Documentation | `docs(readme): update installation guide` |
| `test` | Tests | `test(auth): add integration tests for login` |
| `chore` | Maintenance | `chore(deps): upgrade lodash to 4.17.21` |
| `perf` | Performance | `perf(cache): implement Redis caching layer` |
| `security` | Security fix | `security(auth): patch token validation bypass` |

### PR Size Guidelines

| Size | Lines Changed | Review Time | Recommendation |
|------|---------------|-------------|----------------|
| **XS** | < 50 | < 30 min | Ideal for quick fixes |
| **S** | 50-200 | 30-60 min | Preferred size |
| **M** | 200-500 | 1-2 hours | Consider splitting |
| **L** | 500-1000 | 2-4 hours | Split if possible |
| **XL** | > 1000 | 4+ hours | Must split |

### Reviewer Checklist

- [ ] **What**: Changes match PR description
- [ ] **Why**: Solves the stated problem appropriately
- [ ] **Who**: Correct reviewers involved
- [ ] **When**: No timing/dependency issues
- [ ] **Where**: Changes scoped correctly, no unrelated modifications
- [ ] **How**: Implementation is sound, tests adequate
- [ ] **Issue Link**: Related issue(s) properly linked
- [ ] **Language**: PR written in English
- [ ] **Attribution**: No AI/Claude references in PR

### PR vs Issue: Key Differences

| Aspect | Issue (Problem) | PR (Solution) |
|--------|-----------------|---------------|
| **What** | Describe the problem | Describe the changes |
| **Why** | Impact if not fixed | Why this approach |
| **Who** | Stakeholders affected | Reviewers needed |
| **When** | Deadline/priority | Release target |
| **Where** | Affected areas | Files changed |
| **How** | Acceptance criteria | Implementation details |

---
*Part of the workflow guidelines module*
