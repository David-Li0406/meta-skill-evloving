# Structural Mapping

Map capabilities to code structure.

## Mapping Table

```
## Code Structure

| Capability | Module | Key Files | Owner |
|------------|--------|-----------|-------|
| Auth | /src/auth | auth.service.ts, auth.controller.ts | @backend |
| Users | /src/users | user.model.ts, user.service.ts | @backend |
| UI | /src/components | LoginForm.tsx, Profile.tsx | @frontend |
```

## Directory Proposal

For new projects:

```
## Proposed Structure

/src
├── /auth                    # Authentication capability
│   ├── auth.service.ts      # Business logic
│   ├── auth.controller.ts   # API endpoints
│   ├── auth.middleware.ts   # Request validation
│   └── auth.types.ts        # Type definitions
├── /users                   # User management
│   ├── user.model.ts        # Data model
│   ├── user.service.ts      # Business logic
│   └── user.repository.ts   # Data access
└── /shared                  # Cross-cutting
    ├── /utils               # Helper functions
    └── /types               # Shared types
```

## File-to-Feature Mapping

```
## Implementation Map

### Feature: Login
Files to create/modify:
- `src/auth/login.service.ts` - Login logic (new)
- `src/auth/auth.controller.ts` - Add login endpoint (modify)
- `src/components/LoginForm.tsx` - UI component (new)

### Feature: Registration
Files to create/modify:
- `src/auth/register.service.ts` - Registration logic (new)
- `src/auth/auth.controller.ts` - Add register endpoint (modify)
- `src/components/RegisterForm.tsx` - UI component (new)
```

## Existing Codebase

When mapping to existing code:

1. **Audit first** - List relevant existing files
2. **Identify gaps** - What's missing?
3. **Plan changes** - Modify vs create new

```
## Existing Code Impact

| File | Current Purpose | Required Change |
|------|-----------------|-----------------|
| auth.service.ts | Basic auth | Add OAuth support |
| user.model.ts | User schema | Add preferences field |
| index.ts | Routes | Add new endpoints |
```
