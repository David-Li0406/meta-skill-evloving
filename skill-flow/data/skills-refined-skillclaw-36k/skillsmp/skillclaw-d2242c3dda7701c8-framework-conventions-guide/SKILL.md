---
name: framework-conventions-guide
description: Use this skill when writing code in any opinionated framework's distinctive style, applying framework-native conventions to enhance code quality and maintainability.
---

# Skill body

## Objective
Apply framework-native conventions to code in ANY opinionated framework. This skill teaches the universal principles that framework creators follow, regardless of language or framework.

## Essential Principles

### Core Philosophy
"The best code is the code you don't write. The second best is the code that's obviously correct."

**Embrace the framework:**
- Rich domain models over service layers
- Framework routing over custom routing
- Built-in patterns over imported patterns
- Framework's database tools, not external ORMs
- Build solutions before reaching for packages
- Trust the framework's opinions - they exist for good reasons

**What to avoid (universal anti-patterns):**
- External auth libraries when framework auth exists
- Complex permission systems over simple role checks
- External job queues when framework has one
- External caching when framework provides it
- Component libraries when templates work
- GraphQL when REST is sufficient
- Factory patterns in tests when fixtures/seeds work
- Microservices when a monolith suffices

### Development Philosophy
- Ship, Validate, Refine - get to production to learn
- Fix root causes, not symptoms
- Write-time operations over read-time computations
- Database constraints over application validations
- Simple code that works > clever code that impresses

## Intake
What are you working on?
1. **Controllers/Views** - Request handling, routing, responses
2. **Models/Data** - Domain logic, state management, queries
3. **Frontend** - Templates, components, interactivity
4. **Architecture** - Routing, auth, jobs, caching
5. **Testing** - Unit tests, integration tests, fixtures
6. **Dependencies** - What to use vs avoid
7. **Code Review** - Review against framework conventions
8. **General Guidance** - Philosophy and conventions

**Specify a number or describe your task and your framework (Django, Laravel, Next.js, etc.).**

## Routing
| Response | Reference to Read |
|----------|-------------------|
|          |                   |