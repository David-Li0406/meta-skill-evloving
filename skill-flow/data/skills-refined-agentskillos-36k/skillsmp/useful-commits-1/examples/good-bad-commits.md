# Good vs Bad Commit Messages: Real-World Examples

## Purpose

This document provides side-by-side comparisons of bad and good commit messages across common scenarios. Each example shows what makes a commit message ineffective and how to improve it.

## Example 1: Bug Fix

### ❌ Bad

```
Fix bug
```

**Problems:**
- No type prefix
- Doesn't specify what bug
- No context about the fix
- Generic and not distinctive

### ✅ Good

```
fix: prevent race condition in event handlers

Add mutex lock around event processing to ensure handlers execute
sequentially. Rapid events could trigger handlers out of order,
causing inconsistent state updates.

Fixes #234
```

**Why good:**
- Conventional Commits format
- Specific problem (race condition)
- Clear solution (mutex lock)
- Explains impact (sequential execution prevents inconsistent state)
- References issue

---

## Example 2: New Feature

### ❌ Bad

```
feat: Added new feature to the app.
```

**Problems:**
- Capitalized description
- Ends with period
- Doesn't specify what feature
- Past tense ("Added" instead of "add")
- Generic and vague

### ✅ Good

```
feat(auth): add JWT token refresh mechanism

Implement automatic token refresh when tokens expire within 5 minutes
of API calls. This prevents users from being logged out during active
sessions. Refresh happens transparently in the background.

Users no longer experience unexpected logouts when their session is
close to expiring but they're actively using the app.
```

**Why good:**
- Proper format (lowercase, no period, imperative)
- Specific feature (JWT token refresh)
- Explains behavior (automatic refresh within 5 minutes)
- States user benefit (no unexpected logouts)
- Provides context (transparent background operation)

---

## Example 3: Refactoring

### ❌ Bad

```
refactor: Refactored code
```

**Problems:**
- Capitalized
- Not imperative mood ("Refactored" vs "refactor")
- Doesn't explain what was refactored
- Doesn't explain why
- No indication of benefits

### ✅ Good

```
refactor: extract user validation logic to separate service

Move validation logic from UserComponent to UserValidationService
to enable reuse across registration and profile edit flows. This
eliminates 150 lines of duplicated validation code and ensures
consistent validation rules.

No functional changes to validation behavior.
```

**Why good:**
- Clear what was refactored (validation logic)
- Explains why (code reuse)
- States benefits (eliminates duplication, consistency)
- Clarifies no behavior change
- Quantifies impact (150 lines eliminated)

---

## Example 4: Performance Improvement

### ❌ Bad

```
perf: make it faster
```

**Problems:**
- Too vague ("it")
- No specifics about what or how
- No measurable improvement
- Doesn't explain why speed was an issue

### ✅ Good

```
perf(api): cache user preferences to reduce database queries

User preferences were being fetched on every page load, causing
unnecessary database queries and slowing initial render by ~300ms.

Implement in-memory cache with 5-minute TTL. Cache is invalidated
when preferences are updated.

Performance impact:
- Page load time: 800ms → 500ms (37% reduction)
- Database load: ~80% reduction in preference queries
```

**Why good:**
- Specific component (api) and area (user preferences)
- Explains the problem (repeated queries, slow render)
- Describes solution (in-memory cache with TTL)
- Provides measurable results (37% faster, 80% fewer queries)
- Notes invalidation strategy

---

## Example 5: Documentation

### ❌ Bad

```
docs: updated docs
```

**Problems:**
- Past tense
- Doesn't specify which docs
- Doesn't explain what changed or why

### ✅ Good

```
docs: update authentication flow documentation

Add sequence diagrams for OAuth flow and clarify token refresh
behavior. Previous documentation was missing the refresh token
exchange step, causing confusion for integrators.

Also add troubleshooting section for common auth errors.
```

**Why good:**
- Specific documentation area (authentication flow)
- Lists what was added (diagrams, clarification, troubleshooting)
- Explains the problem being solved (missing refresh token step)
- States who benefits (integrators)

---

## Example 6: Style Changes

### ❌ Bad

```
style: formatting
```

**Problems:**
- Too vague
- Doesn't indicate scope of changes
- No explanation of what formatter or rules

### ✅ Good

```
style: apply Prettier formatting to TypeScript files

Run Prettier with new configuration across all TypeScript files in
src/. This establishes consistent code style for the project.

No functional changes. Only whitespace, indentation, and quote
style affected.

Config: .prettierrc.json (80 char line width, 2-space indent, single quotes)
```

**Why good:**
- Specifies tool (Prettier) and scope (TypeScript files)
- Clarifies no functional impact
- Notes what changed (whitespace, indentation, quotes)
- Documents configuration

---

## Example 7: Breaking Change

### ❌ Bad

```
feat: change API format
```

**Problems:**
- Missing `!` for breaking change
- No `BREAKING CHANGE:` footer
- Doesn't explain what changed in API
- No migration guidance

### ✅ Good

```
feat(api)!: change authentication response format

Modify login endpoint to return token object instead of plain string.
This provides additional metadata (expiry time, refresh token) that
clients need for proper token management.

BREAKING CHANGE: AuthService.login() now returns {token: string,
expiresIn: number, refreshToken: string} instead of just the token
string. Update all clients to access response.token instead of using
response directly.

Migration example:
  // Before
  const token = await authService.login(username, password)

  // After
  const {token} = await authService.login(username, password)
```

**Why good:**
- Has `!` in type prefix
- Has `BREAKING CHANGE:` footer
- Explains what changed (plain string → object)
- Explains why (need metadata)
- Provides migration example
- Clear before/after code

---

## Example 8: Build System

### ❌ Bad

```
update package.json
```

**Problems:**
- No type prefix
- Doesn't explain what was updated or why
- Command-like message, not conventional commit

### ✅ Good

```
build(deps): upgrade webpack from 4 to 5

Upgrade webpack to v5 for improved build performance and tree
shaking. Build time reduced from 45s to 28s (38% faster).

Breaking changes in webpack config:
- Updated output.filename syntax
- Replaced optimization.splitChunks config
- Updated devServer configuration

Config changes tested across development and production builds.
```

**Why good:**
- Proper type (build) and scope (deps)
- Specific versions (4 → 5)
- States benefits (performance, tree shaking)
- Quantifies improvement (38% faster)
- Lists breaking config changes
- Notes testing performed

---

## Example 9: CI Configuration

### ❌ Bad

```
ci: fix
```

**Problems:**
- Too vague (fix what?)
- No context about the problem
- Doesn't explain solution

### ✅ Good

```
ci: increase workflow timeout to prevent failures on large PRs

GitHub Actions workflows were timing out after 20 minutes when
running full test suite on PRs with many changed files. Increase
timeout to 45 minutes to accommodate worst-case scenarios.

Also split integration tests into separate workflow to parallelize
execution and reduce overall CI time.

Average CI time remains ~15 minutes for typical PRs.
```

**Why good:**
- Specific problem (timeouts on large PRs)
- Clear solution (increase timeout to 45 minutes)
- Additional optimization (parallel workflows)
- Reassures normal case still fast (15 minutes typical)

---

## Example 10: Testing

### ❌ Bad

```
test: add tests
```

**Problems:**
- Doesn't specify what is tested
- No indication of coverage improvement
- Too generic

### ✅ Good

```
test(auth): add integration tests for token refresh flow

Add tests covering:
- Successful token refresh
- Expired refresh token handling
- Concurrent refresh request race conditions
- Token refresh failure with retry logic

Coverage for auth module: 72% → 89%

These tests catch the race condition bug that caused #234 and
prevent regression.

Refs: #234
```

**Why good:**
- Scope specified (auth)
- Lists specific test scenarios
- Shows coverage improvement (72% → 89%)
- Connects to bug that prompted tests (#234)
- Explains value (prevent regression)

---

## Example 11: Chore

### ❌ Bad

```
chore: misc changes
```

**Problems:**
- "misc" is too vague
- Doesn't list what changed
- Reads like a catch-all for unrelated changes

### ✅ Good

```
chore: update code owner assignments for API team

Update CODEOWNERS to reflect new API team structure after org
changes. Route /api and /integrations paths to @api-team instead
of individual reviewers.

This ensures PRs automatically request review from the right team
and reduces review assignment friction.
```

**Why good:**
- Specific chore (CODEOWNERS update)
- Explains context (org changes)
- Describes what changed (team vs individuals)
- States benefit (automatic review requests)

---

## Example 12: Multiple Concerns (Bad Separation)

### ❌ Bad

```
feat: add login and fix navbar and update docs

Add user login functionality. Also fix the navbar alignment bug.
Also update the API documentation. Also refactor the user model.
```

**Problems:**
- Multiple unrelated changes in one commit
- Mixes feat, fix, docs, and refactor
- Hard to review
- Difficult to revert if one part is problematic
- Violates single responsibility

### ✅ Good (Split into separate commits)

```
feat(auth): add user login functionality

Implement login form with email/password authentication. Support
remember-me option that extends session to 30 days instead of 24
hours.

---

fix(ui): correct navbar alignment on mobile

Navigation items were overlapping the logo on screens <768px wide.
Adjust flex layout and add 16px margin to prevent overlap.

Fixes #123

---

docs(api): update authentication endpoints documentation

Add examples for login, logout, and token refresh endpoints. Include
error codes and response formats.

---

refactor(models): extract user validation to separate class

Move validation logic from User model to UserValidator for reuse
in registration and profile edit flows.
```

**Why good:**
- Each concern in its own commit
- Each has appropriate type
- Each can be reviewed independently
- Each can be reverted independently
- Each has focused, clear message

---

## Example 13: Vague Scope

### ❌ Bad

```
fix: fix bug in code
```

**Problems:**
- "bug in code" is redundant and vague
- No indication of what code or what bug
- Not distinctive or helpful in git log

### ✅ Good

```
fix(parser): handle nested objects in JSON input

Parser was throwing TypeError when encountering objects nested
more than 2 levels deep. Add recursive parsing to handle arbitrary
nesting depth.

This fixes parsing failures for complex configuration files.

Fixes #456
```

**Why good:**
- Specific component (parser)
- Specific issue (nested object handling)
- Clear solution (recursive parsing)
- States impact (fixes complex config files)
- References issue

---

## Example 14: No Context

### ❌ Bad

```
feat: add feature
```

**Problems:**
- Redundant (feat already means feature)
- No indication of what feature
- No explanation of why or for whom

### ✅ Good

```
feat(billing): add subscription pause functionality

Allow users to pause subscriptions for 1-12 months without
cancelling. During pause period:
- No charges are made
- Access to premium features is suspended
- Subscription resumes automatically after pause period
- User can manually resume early

This was the #2 most requested feature in Q4 2024 user survey and
reduces cancellation rate by allowing temporary breaks.
```

**Why good:**
- Specific feature (subscription pause)
- Detailed behavior (bullet list of what happens)
- Explains benefit (reduces cancellation)
- Provides context (user survey request)

---

## Example 15: Local Spec References (Prohibited)

### ❌ Bad

```
feat: implement SPEC-234 requirements per DOC-456
```

**Problems:**
- References local spec files (./specs/SPEC-234.md)
- Readers without access to specs can't understand the change
- Local IDs won't be meaningful in the future
- Doesn't describe what was actually implemented

### ✅ Good

```
feat(api): add pagination to user list endpoint

Implement cursor-based pagination for /api/users endpoint to handle
large user bases efficiently. Endpoints now accept limit (max 100)
and cursor parameters.

This prevents timeouts when fetching user lists for organizations
with 10,000+ users.

Refs: #789 (GitHub issue)
```

**Why good:**
- Describes what was implemented (pagination)
- Explains how it works (cursor-based, limit parameter)
- States the problem solved (timeouts for large orgs)
- References GitHub issue (public, accessible)
- No local spec file references

---

## Pattern Recognition

### Pattern 1: "Update X"

**Bad patterns:**
```
update user service
update config
update tests
```

**Good patterns:**
```
refactor(users): extract validation to separate service
feat(config): add environment-based configuration loading
test(api): add coverage for error handling paths
```

Use specific types (refactor, feat, test) instead of generic "update"

### Pattern 2: Missing Subject

**Bad patterns:**
```
fix: null pointer exception
fix: undefined variable
fix: typo
```

**Good patterns:**
```
fix(parser): prevent null pointer when input is empty
fix(ui): handle undefined user avatar in profile component
docs: correct typo in installation instructions (s/installl/install/)
```

Add context about where the issue occurred

### Pattern 3: Past Tense

**Bad patterns:**
```
feat: added login
fix: fixed bug
refactor: refactored code
```

**Good patterns:**
```
feat: add login functionality
fix: prevent race condition
refactor: extract validation logic
```

Use imperative mood (command form)

---

## Summary Checklist

Use this checklist when reviewing commit messages:

**Format:**
- [ ] Type prefix present (feat, fix, docs, etc.)
- [ ] Scope included when appropriate
- [ ] Description in lowercase
- [ ] No period at end of subject
- [ ] Subject ≤70 characters
- [ ] Imperative mood ("add" not "added")

**Content:**
- [ ] Specific, not vague ("add JWT refresh" not "update auth")
- [ ] Explains what changed
- [ ] Explains why it changed
- [ ] Includes user-visible impact if applicable
- [ ] No local spec file references
- [ ] Breaking changes properly noted with ! and footer

**Structure:**
- [ ] Body present for non-trivial changes
- [ ] Body wraps at 90 characters
- [ ] Body ≤700 characters (excluding footers)
- [ ] Bullet points ≤8 if using bullets
- [ ] References to issues/PRs included when relevant

**Separation:**
- [ ] Single logical change
- [ ] Not mixing types (feat + fix + refactor)
- [ ] Can be reverted independently
- [ ] Has focused, clear purpose
