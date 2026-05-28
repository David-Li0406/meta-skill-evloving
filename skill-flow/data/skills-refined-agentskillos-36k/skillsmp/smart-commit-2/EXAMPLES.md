# Commit Message Examples

## Feature

```
feat(auth): add OAuth2 login support

Implement OAuth2 flow with Google and GitHub providers.
Includes token refresh and session management.

Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Bug Fix

```
fix(api): handle null response in user endpoint

The /api/users endpoint was crashing when the database
returned null for deleted users. Now returns 404.

Fixes #234

Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Documentation

```
docs(readme): update installation instructions

Add prerequisites section and troubleshooting guide.

Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Refactor

```
refactor(core): simplify error handling

Replace nested try-catch blocks with Result type pattern.
No behavior change, improves readability.

Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Test

```
test(auth): add login integration tests

Cover success, invalid credentials, and rate limiting cases.

Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Chore (Simple)

```
chore(deps): update dependencies to latest versions

Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Breaking Change

```
feat(api)!: change authentication to JWT

BREAKING CHANGE: Session-based auth removed. All clients must
update to use Bearer token authentication.

Migration guide: https://docs.example.com/auth-migration

Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Multi-Scope Change

When changes span multiple areas, use the primary area as scope:

```
feat(checkout): add payment processing with Stripe

- Add Stripe SDK integration
- Create payment form component
- Add webhook handler for confirmations

Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```
