# Conventional Commits: Comprehensive Examples

This document provides extensive examples of commit messages following the Conventional Commits specification.

## Excellent Examples

### Feature Commits (feat)

```
feat(auth): add OAuth2 authentication with Google provider

Implement OAuth2 login flow for Google authentication.
Includes:
- OAuth2 redirect handling
- Token exchange and refresh
- User profile fetching
- Session management

Closes #142
```

```
feat(search): implement fuzzy search with autocomplete

Add fuzzy matching algorithm using Levenshtein distance for product search.
Includes real-time autocomplete suggestions with debouncing (300ms).

Performance: Search 10k products in <50ms
Closes #187
```

```
feat(api)!: migrate to GraphQL from REST

BREAKING CHANGE: All REST endpoints are deprecated and will be removed
in v3.0.0. Use GraphQL API at /graphql endpoint.

Migration guide: https://docs.example.com/migration-graphql

Closes #234
```

### Bug Fix Commits (fix)

```
fix(checkout): calculate tax correctly for international orders

Fix tax calculation bug where international orders used domestic tax rates.
Now correctly applies tax based on shipping address country.

Fixes #298
```

```
fix(api): prevent race condition in concurrent user creation

Add database transaction with pessimistic locking to prevent duplicate
user records when multiple registration requests arrive simultaneously.

Root cause: Two requests could read "user doesn't exist" before either
completed insertion.

Fixes #412
```

```
fix(ui): resolve memory leak in infinite scroll component

Remove event listeners and cancel pending requests on component unmount.
Memory usage no longer grows during extended scrolling sessions.

Fixes #567
```

### Documentation Commits (docs)

```
docs(api): add authentication examples for all endpoints

Include curl, JavaScript, and Python examples for each API endpoint.
Add troubleshooting section for common authentication errors.
```

```
docs(readme): update installation instructions for Windows

Add Windows-specific setup steps including:
- Visual Studio Build Tools installation
- Python path configuration
- Common Windows troubleshooting

Closes #123
```

```
docs(contributing): add code review guidelines

Document expectations for code reviews including:
- Response time SLAs
- Review checklist
- How to request changes
- When to approve vs request changes
```

### Refactoring Commits (refactor)

```
refactor(database): extract query builder into separate module

Improve code organization and testability by separating query
construction from execution. No functional changes.

Benefits:
- Easier to unit test queries
- Query logic reusable across repositories
- Clearer separation of concerns
```

```
refactor(auth): replace JWT library with more secure alternative

Replace jsonwebtoken with jose for better security and TypeScript support.
All tests pass, no API changes.

Security: jose has better JWKS support and is actively maintained.
```

```
refactor(components): convert class components to functional hooks

Convert all remaining class components to functional components with hooks.
Reduces bundle size by 12KB and improves tree-shaking.

No behavioral changes, all tests pass.
```

### Test Commits (test)

```
test(auth): add integration tests for OAuth flow

Add end-to-end tests covering:
- OAuth redirect flow
- Token exchange
- Token refresh
- Session creation
- Error handling

Coverage: auth module 78% → 94%
```

```
test(api): add load tests for user endpoints

Add k6 load tests simulating 1000 concurrent users.
Results: All endpoints maintain <100ms p95 latency.
```

### Performance Commits (perf)

```
perf(search): add database indexes for product queries

Add composite index on (category, price, created_at) for product search.
Add index on name for text search.

Performance:
- Category browse: 250ms → 15ms
- Text search: 180ms → 12ms
- Product listing: 120ms → 8ms
```

```
perf(api): implement response caching with Redis

Cache frequently accessed endpoints with 5-minute TTL.
Reduces database queries by 85% for cached endpoints.

Cache hit rate: 92% in production testing
```

### Chore Commits (chore)

```
chore(deps): upgrade React from 18.2.0 to 18.3.0

Update React and React DOM to latest stable version.
No breaking changes, all tests pass.
```

```
chore(docker): optimize Dockerfile for faster builds

- Use multi-stage build
- Leverage layer caching
- Reduce image size from 1.2GB to 450MB

Build time: 12min → 4min
```

### CI/CD Commits (ci)

```
ci(github): add automated deployment to staging

Add GitHub Actions workflow to deploy to staging environment
on merge to develop branch.

Includes:
- Docker build and push
- Database migration
- Health check verification
- Slack notification
```

```
ci(tests): parallelize test suite across 4 workers

Split test suite into 4 parallel jobs to reduce CI time.
Test duration: 8min → 2min
```

### Build Commits (build)

```
build(webpack): enable tree-shaking for production builds

Configure webpack to eliminate dead code in production.
Bundle size reduced from 850KB to 620KB (-27%).
```

```
build(vite): migrate from webpack to vite

Replace webpack with Vite for faster development experience.
Dev server startup: 45s → 1.2s
HMR: 2-3s → <100ms
```

## Common Mistakes and Corrections

### ❌ Bad: Vague and Non-specific

```
Update files
Fix bug
Change code
WIP
Misc changes
```

### ✅ Good: Specific and Descriptive

```
feat(search): add category filter to product search
fix(checkout): calculate shipping cost for Alaska and Hawaii
refactor(utils): extract date formatting into helper module
docs(api): document rate limiting headers
```

---

### ❌ Bad: Past Tense

```
Added OAuth login
Fixed the bug in checkout
Updated documentation
Changed API endpoint
```

### ✅ Good: Imperative Mood

```
feat(auth): add OAuth login
fix(checkout): resolve tax calculation bug
docs(api): update authentication guide
refactor(api): change endpoint response format
```

---

### ❌ Bad: Multiple Unrelated Changes

```
feat: add search feature, fix login bug, update README

- Implemented new search
- Fixed bug where users couldn't login
- Updated installation docs
```

### ✅ Good: Atomic Commits

```
feat(search): add product search with filters

Implement search functionality with category and price filters.
Includes autocomplete and result highlighting.

Closes #187
```

```
fix(auth): resolve login redirect loop

Fix infinite redirect when session expires during login.
Now correctly redirects to intended page after re-authentication.

Fixes #234
```

```
docs(readme): update installation instructions

Add prerequisites section and troubleshooting guide.
```

---

### ❌ Bad: Missing Type

```
add user authentication
implement search feature
update API documentation
```

### ✅ Good: Proper Type

```
feat(auth): add user authentication
feat(search): implement search feature
docs(api): update API documentation
```

---

### ❌ Bad: Too Long Subject

```
feat(auth): add comprehensive OAuth2 authentication system with support for Google, GitHub, and Microsoft providers including token refresh
```

### ✅ Good: Concise Subject with Details in Body

```
feat(auth): add OAuth2 authentication for multiple providers

Implement OAuth2 login flow supporting:
- Google authentication
- GitHub authentication
- Microsoft authentication

Includes token refresh mechanism and session management.

Closes #142
```

---

### ❌ Bad: Subject Ends with Period

```
feat(search): add search filters.
fix(api): resolve bug.
```

### ✅ Good: No Period

```
feat(search): add search filters
fix(api): resolve bug
```

---

### ❌ Bad: Capitalized Subject

```
feat(auth): Add OAuth Login
fix(api): Fix Bug In Checkout
```

### ✅ Good: Lowercase Subject

```
feat(auth): add OAuth login
fix(api): fix bug in checkout
```

## Real-World Examples from Popular Projects

### React

```
feat(hooks): add useTransition hook

Add experimental useTransition hook for deferring updates.
Allows marking updates as low-priority to keep UI responsive.
```

### Vue.js

```
fix(reactivity): avoid infinite loops with mutating computed getters

Prevent infinite update loops when computed properties mutate reactive state.
Add warning in development mode.

Closes #1234
```

### TypeScript

```
perf(checker): skip checking of types in node_modules

Improve compilation speed by skipping type checking in node_modules.
Reduces compile time by ~40% in large projects.
```

### Next.js

```
feat(router): add middleware support

Add middleware API for running code before request completion.
Enables use cases like authentication, logging, and redirects.
```

## Breaking Changes Examples

### Without Migration Guide

```
feat(api)!: change user endpoint response format

BREAKING CHANGE: User API now returns `userId` instead of `id`.
All clients must update field references.
```

### With Migration Guide

```
feat(database)!: migrate to Prisma from TypeORM

BREAKING CHANGE: Database access layer completely rewritten.

Migration steps:
1. Update imports: `import { db } from '@/lib/db'`
2. Update queries: See migration guide for query syntax changes
3. Run: `npm run db:migrate`

Full migration guide: https://docs.example.com/migration-prisma

Closes #567
```

### Multiple Breaking Changes

```
feat(api)!: v2.0.0 API release

BREAKING CHANGE: Multiple breaking changes in v2.0.0

1. Authentication: Now requires API key in header (not query param)
2. Pagination: Changed from `page/limit` to `offset/limit`
3. Timestamps: All timestamps now in ISO 8601 format (was Unix epoch)
4. Error codes: Standardized error response format

See migration guide: https://docs.example.com/v2-migration

Closes #789
```

## Multi-paragraph Body Examples

### Complex Feature

```
feat(notifications): implement real-time notification system

Add WebSocket-based notification delivery for user actions.

Architecture:
- WebSocket server with connection pooling (max 10k concurrent)
- Client-side notification queue with automatic retry
- Notification preferences stored per-user
- Email fallback for offline users

Performance:
- Handles 10k concurrent connections
- Message delivery latency <100ms p99
- Graceful degradation when Redis unavailable

Implementation details:
- Socket.io for WebSocket management
- Redis pub/sub for horizontal scaling
- PostgreSQL for notification persistence
- Bull queue for email fallback

Closes #156, #187, #234
```

### Security Fix

```
fix(auth)!: patch critical token validation vulnerability

BREAKING CHANGE: Token validation now requires signature verification.

Security issue:
OAuth tokens were not properly validated, allowing token forgery.
Attacker could craft tokens that appeared valid without proper signing.

Fix:
- Add signature validation for all OAuth tokens
- Reject tokens with invalid or missing signatures
- Add comprehensive security tests
- Log all validation failures for monitoring

Impact:
Tokens that were previously accepted without valid signatures will
now be rejected. This may affect clients that were inadvertently
sending malformed tokens.

Security: CVE-2024-XXXXX
Fixes #489
```

## Co-authored Commits

### Multiple Authors

```
feat(search): implement advanced search with filters

Add comprehensive search functionality with multiple filter types.

Implemented by:
- Alice: Search backend and indexing
- Bob: Search UI components
- Charlie: Filter logic and validation

Co-authored-by: Alice Developer <alice@example.com>
Co-authored-by: Bob Engineer <bob@example.com>
Co-authored-by: Charlie Coder <charlie@example.com>
```

### With Claude Code

```
feat(api): add GraphQL API endpoints

Implement GraphQL API alongside existing REST endpoints.
Includes queries, mutations, and subscriptions.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Scope Examples

Common scopes by project type:

### Frontend Application
```
feat(auth): ...
feat(dashboard): ...
feat(profile): ...
feat(settings): ...
fix(navigation): ...
fix(forms): ...
```

### Backend API
```
feat(api): ...
feat(database): ...
feat(auth): ...
fix(validation): ...
fix(middleware): ...
```

### Full-stack Application
```
feat(frontend): ...
feat(backend): ...
feat(database): ...
feat(api): ...
fix(client): ...
fix(server): ...
```

### Library/Package
```
feat(core): ...
feat(utils): ...
feat(types): ...
fix(parser): ...
fix(validator): ...
```

## Footer Examples

### Issue References

```
Closes #123
Fixes #456
Resolves #789
```

```
Closes #123, #456, #789
```

```
Related to #123
See also #456
```

### Multiple Footers

```
feat(api): add new endpoint

BREAKING CHANGE: Old endpoint deprecated.

Closes #123
Reviewed-by: Jane Doe <jane@example.com>
Refs: #456
```

## Summary

**Key Principles**:
1. Use conventional format: `<type>(<scope>): <subject>`
2. Subject in imperative mood, ≤50 chars, no period
3. Body wraps at 72 chars, explains "why"
4. Footer for breaking changes and issue references
5. One logical change per commit (atomic)

**Common Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance
- `perf`: Performance
- `ci`: CI/CD
- `build`: Build system

**Benefits**:
- Clear, searchable history
- Automatic changelog generation
- Easy to understand changes
- Enables semantic versioning
- Facilitates code review
