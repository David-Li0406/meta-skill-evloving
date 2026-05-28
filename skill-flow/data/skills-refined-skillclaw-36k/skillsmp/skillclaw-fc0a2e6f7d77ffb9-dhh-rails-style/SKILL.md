---
name: dhh-rails-style
description: Use this skill when writing Ruby and Rails code in DHH's distinctive 37signals style, applying conventions for models, controllers, and views.
---

# Skill body

## Objective
Apply 37signals/DHH Rails conventions to Ruby and Rails code, leveraging domain expertise from analyzing production 37signals codebases.

## Essential Principles

### Core Philosophy
"The best code is the code you don't write. The second best is the code that's obviously correct."

**Vanilla Rails is plenty:**
- Rich domain models over service objects
- CRUD controllers over custom actions
- Concerns for horizontal code sharing
- Records as state instead of boolean columns
- Database-backed everything (no Redis)
- Build solutions before reaching for gems

**What they deliberately avoid:**
- devise (custom ~150-line auth instead)
- pundit/cancancan (simple role checks in models)
- sidekiq (Solid Queue uses database)
- redis (database for everything)
- view_component (partials work fine)
- GraphQL (REST with Turbo sufficient)
- factory_bot (fixtures are simpler)
- rspec (Minitest ships with Rails)
- Tailwind (native CSS with layers)

### Development Philosophy
- Ship, Validate, Refine - prototype-quality code to production to learn
- Fix root causes, not symptoms
- Write-time operations over read-time computations
- Database constraints over ActiveRecord validations

## Intake
What are you working on?
1. **Controllers** - REST mapping, concerns, Turbo responses
2. **Models** - Concerns, state records, callbacks, scopes
3. **Views & Frontend** - Turbo, Stimulus, CSS, partials
4. **Architecture** - Routing, multi-tenancy, authentication, jobs
5. **Testing** - Minitest, fixtures, integration tests
6. **Code Review** - Review code against DHH style
7. **General Guidance** - Philosophy and conventions

**Specify a number or describe your task.**

## Quick Reference

### Naming Conventions
**Verbs:** `card.close`, `card.gild`, `board.publish` (not `set_style`)

### Controller Actions
- **Only 7 REST actions**: `index`, `show`, `new`, `create`, `edit`, `update`, `destroy`
- **New behavior?** Create a new controller, not a custom action
- **Action length**: 1-5 lines maximum
- **Empty actions are fine**: Let Rails convention handle rendering

### Model Design (Fat Models)
Models own business logic, authorization, and broadcasting.

### Current Attributes
Use `Current` for request context, never pass `current_user` everywhere.