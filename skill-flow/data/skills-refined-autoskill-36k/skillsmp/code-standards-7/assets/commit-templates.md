# Commit Message Templates for Refactoring

Use these templates for consistent, informative commit messages during refactoring.

## Format

```
refactor(<scope>): <short description>

<body - optional but recommended for MEDIUM/DEEP>

<footer - for breaking changes>
```

## Scope Values

Use the phase level as scope:
- `small` - Phase 1 changes
- `medium` - Phase 2 changes  
- `deep` - Phase 3 changes

Or be more specific:
- `naming` - Renamed variables/functions
- `format` - Formatting/whitespace changes
- `dead-code` - Removed unused code
- `extract` - Extracted functions/modules
- `structure` - File/folder reorganization

## Examples by Phase

### Phase 1 (SMALL)

```
refactor(small): rename ambiguous variables in UserService

- userId → visitorId (clarifies this is the page visitor, not logged-in user)
- data → userProfileData
- x → retryCount
```

```
refactor(dead-code): remove unused imports in auth module
```

```
refactor(small): extract magic numbers to named constants

- 86400 → SECONDS_PER_DAY
- 5 → MAX_RETRY_ATTEMPTS
- 1000 → DEFAULT_TIMEOUT_MS
```

### Phase 2 (MEDIUM)

```
refactor(medium): extract validation logic from handleSubmit

Split 67-line function into focused helpers:
- validateInput() - input sanitization and validation
- preparePayload() - transform data for API
- handleSubmit() - orchestration only (now 23 lines)
```

```
refactor(extract): consolidate duplicate date formatting

Merged formatDate(), formatDateTime(), and formatTimestamp()
into single formatDate(date, options) function.

Affected files: utils/date.ts, components/*, services/*
```

```
refactor(medium): replace nested conditionals with guard clauses

processOrder() now uses early returns instead of 4-level nesting.
Reduces cognitive complexity from 15 to 6.
```

### Phase 3 (DEEP)

```
refactor(deep): reorganize user module by responsibility

BREAKING CHANGE: UserService split into separate services

Before:
  src/services/user-service.ts (800 lines, 15 methods)

After:
  src/users/
    auth/auth-service.ts (authentication)
    profile/profile-service.ts (profile CRUD)
    preferences/preferences-service.ts (settings)
    index.ts (public API unchanged)

Migration: Import paths unchanged due to barrel export.
Internal imports need updating - see migration notes.
```

```
refactor(deep): replace callback pattern with async/await

Converted entire data layer from callbacks to async/await.

BREAKING CHANGE: All repository methods now return Promises.

Before:
  userRepo.findById(id, (err, user) => { ... })

After:
  const user = await userRepo.findById(id)

Migration: Update all callers to use await or .then()
```

## Footer Conventions

### Breaking Changes

```
BREAKING CHANGE: <description of what breaks>

Migration: <how to update dependent code>
```

### Related Issues

```
Refs: #123, #456
Closes: #789
```

### Co-authors

```
Co-authored-by: Name <email@example.com>
```

## Quick Reference

| Change Type | Example Subject |
|-------------|-----------------|
| Rename | `refactor(naming): rename userId to visitorId` |
| Remove dead code | `refactor(dead-code): remove unused formatters` |
| Extract function | `refactor(extract): extract validateEmail from submitForm` |
| Simplify logic | `refactor(medium): simplify conditional in authCheck` |
| Move files | `refactor(structure): move utils to shared/` |
| Split module | `refactor(deep): split UserService into domain services` |
| Change pattern | `refactor(deep): replace observer with event emitter` |
