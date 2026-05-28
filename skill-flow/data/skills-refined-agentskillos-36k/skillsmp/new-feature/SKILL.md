---
name: new-feature
description: Complete guide for implementing new features in RentPath. Covers the full workflow from planning to testing. Auto-triggers on "implement feature", "add new feature", "build this feature", "create new functionality", "new endpoint".
---

# New Feature Implementation Guide

You are helping implement a new feature in RentPath following established patterns and conventions.

## Arguments

This skill accepts optional arguments to specify the feature:

| Usage                                  | Behavior                                     |
| -------------------------------------- | -------------------------------------------- |
| `/new-feature`                         | Interactive - ask for requirements           |
| `/new-feature visit scheduling`        | Implement feature with that name/description |
| `/new-feature VisitSchedule`           | Create model/CRUD for that entity            |
| `/new-feature backend only`            | Skip frontend, focus on API/backend          |
| `/new-feature frontend only`           | Skip backend, focus on UI components         |
| `/new-feature like PropertyController` | Use that as a template/reference             |

**Argument interpretation:**

- **Feature name/description** - What to build
- **Model name** (PascalCase) - Create full CRUD for that entity
- **Scope** (`backend`, `frontend`, `fullstack`) - Limit implementation scope
- **Reference** (`like X`) - Use existing feature as template

## Before You Start

1. **Clarify requirements**: What exactly should this feature do?
2. **Identify scope**: Backend, frontend, or full-stack?
3. **Check existing patterns**: Find similar features to use as templates

## Tools to Use

| Task            | Tool                                 | Command/Action                |
| --------------- | ------------------------------------ | ----------------------------- |
| Search codebase | `Grep`, `Glob`                       | Find similar patterns         |
| Read docs       | `Read`                               | Check `docs/` for patterns    |
| Create files    | `Bash`                               | `php artisan make:*` commands |
| Database schema | `laravel-boost` -> `database-schema` | Check existing tables         |
| Run tests       | `Bash`                               | `php artisan test`            |
| Type check      | `Bash`                               | `npm run types`               |

## Feature Implementation Checklist

### Phase 1: Planning

```
[ ] Requirements clearly understood
[ ] Similar feature identified as template
[ ] Database changes identified
[ ] API/routes designed
[ ] Frontend components planned
[ ] Test scenarios listed
```

### Phase 2: Backend

```
[ ] Migration created and run
[ ] Model created/updated
[ ] Factory created/updated
[ ] Form Request created
[ ] Controller methods added
[ ] Routes registered
[ ] Authorization (policy) added
```

### Phase 3: Frontend

```
[ ] TypeScript types updated
[ ] Page component created
[ ] UI components created
[ ] Hooks created (if needed)
[ ] Translations added
```

### Phase 4: Testing & Polish

```
[ ] Feature tests written
[ ] Manual testing done
[ ] Edge cases handled
[ ] Error states handled
[ ] Loading states added
[ ] Documentation updated (if needed)
```

## Quick Reference Commands

```bash
# Create all backend files
php artisan make:model FeatureItem -mf --no-interaction
php artisan make:controller FeatureItemController --no-interaction
php artisan make:request StoreFeatureItemRequest --no-interaction
php artisan make:policy FeatureItemPolicy --model=FeatureItem --no-interaction
php artisan make:test FeatureItemTest --no-interaction

# Run checks
php artisan migrate
php artisan wayfinder:generate
npm run types
php artisan test --filter=FeatureItem
```

## Detailed Implementation Guides

For step-by-step instructions, see the supporting files in this skill folder:

- **[BACKEND.md](BACKEND.md)** - Database, Model, FormRequest, Controller, Routes, Policy
- **[FRONTEND.md](FRONTEND.md)** - TypeScript types, Page components, UI patterns
- **[TESTING.md](TESTING.md)** - Feature tests, Factory patterns

## Documentation References

- `docs/architecture/overview.md` - Architecture patterns
- `docs/patterns/validation.md` - Validation strategy (Laravel Precognition)
- `docs/patterns/wizard.md` - Wizard patterns (if applicable)
- `.claude/rules/laravel-boost.md` - Laravel conventions

## Related Skills

- `/wizard-field` - If adding wizard fields
- `/test-feature` - For test writing patterns
- `/refactor` - If extracting to services

## Related Agents

- **feature-analyst** - Map existing features before changes
- **architect** - System design decisions
- **testing-expert** - Test strategy planning
