---
name: generate-factory
description: Use this skill when you need to auto-generate test data factories from schemas, types, or models to streamline test data infrastructure and reduce boilerplate.
---

# Generate Factory Skill

## Purpose

Auto-generate test data factories from database schemas, TypeScript interfaces, or model definitions. Factories produce realistic test data using Faker.js patterns, significantly reducing test setup time.

## Research Foundation

| Pattern | Source | Reference |
|---------|--------|-----------|
| Factory Pattern | ThoughtBot | [FactoryBot](https://github.com/thoughtbot/factory_bot) |
| Faker.js | Open Source | [fakerjs.dev](https://fakerjs.dev/) |
| Test Data Management | ISTQB | CT-TAS Test Automation Strategy |
| Synthetic Data | Tonic.ai | [Faker Best Practices](https://www.tonic.ai/blog/how-to-generate-simple-test-data-with-faker) |

## When This Skill Applies

- You need to create test data factories.
- Setting up test infrastructure for a new project.
- Existing tests use hard-coded data.
- Schema/model changes require test data updates.
- You need realistic but deterministic test data.

## Trigger Phrases

| Natural Language | Action |
|------------------|--------|
| "Generate factory for User model" | Create user factory |
| "Create test data factories" | Generate factories for all models |
| "Add faker to tests" | Integrate faker with existing tests |
| "Make test data realistic" | Convert hard-coded to factory |
| "Generate fixtures from schema" | Schema-aware factory generation |

## Factory Concepts

### Factory vs Fixture vs Mock

| Type | Purpose | When to Use |
|------|---------|-------------|
| **Factory** | Generate dynamic test data | When you need many variations |
| **Fixture** | Static, predefined data | When exact values matter |
| **Mock** | Fake external dependencies | When isolating units |

### Factory Features

```typescript
// Basic factory
const user = userFactory.build();
// { id: 'uuid-1', name: 'John Doe', email: 'john@example.com' }

// With overrides
const admin = userFactory.build({ role: 'admin' });
// { id: 'uuid-2', name: 'Jane Doe', email: 'jane@example.com', role: 'admin' }

// Build multiple
const users = userFactory.buildList(5);
// Array of 5 users

// With traits
const inactiveUser = userFactory.build({}, { trait: 'inactive' });
// { id: 'uuid-3', ..., status: 'inactive', deactivatedAt: Date }

// With relationships
const userWithOrders = userFactory.build({}, { with: ['orders'] });
```