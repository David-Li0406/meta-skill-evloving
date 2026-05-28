# Context-Aware Option Generation

## Core Principle

**CRITICAL**: Options marked `[...]` in interview templates MUST be generated from exploration context, NOT generic templates.

Generic options lead to irrelevant decisions. Context-aware options reflect actual codebase patterns and make interview decisions actionable.

---

## Generation Process

### Step 1: Read Exploration Context

```bash
# Read summary first
context.json → patterns, key_files, tech_stack

# Read detailed findings
exploration/*.md → implementations, naming conventions, relationships
```

### Step 2: Extract Patterns

Identify existing patterns that should influence options:

| Context Type | What to Extract |
|-------------|-----------------|
| Architecture | Repository pattern, layered architecture, microservices |
| Libraries | npm packages, framework versions, plugin ecosystems |
| Data Models | Schema definitions, naming conventions, relationships |
| Error Handling | Error classes, response formats, logging patterns |
| Testing | Test frameworks, coverage tools, fixture patterns |
| Security | Auth methods, validation libraries, encryption usage |
| UI/UX | Component library, design system, styling approach |

### Step 3: Generate Options

For each question, create 3-4 options:
1. **Recommended option** - Follows existing pattern (mark with "Recommended")
2. **Alternative 1** - Compatible but different approach
3. **Alternative 2** - New pattern (requires justification)
4. **Other** - Always include for freeform input

---

## Option Generation Rules

### Architecture Questions

**Generate from**: Existing architectural patterns found in codebase

| Pattern Found | Generate Options Like |
|--------------|----------------------|
| Repository pattern | "Follow UserRepository pattern", "Direct data access", "New pattern" |
| Service layer | "Add to existing service", "Create new service", "Inline logic" |
| MVC structure | "Follow MVC", "Component-based", "Hybrid" |

**Example**:
```python
# After reading: "Found src/repositories/UserRepository.ts using Prisma"
"options": [
  {"label": "Prisma Repository (Recommended)", "description": "Follows UserRepository pattern, created in src/repositories/"},
  {"label": "Prisma Direct", "description": "Use Prisma client directly without Repository pattern"},
  {"label": "Introduce new pattern", "description": "Propose different approach (explain in Other)"}
]
```

---

### Tech Stack Questions

**Generate from**: Dependencies in package.json, imports in code

| Found | Generate Options Like |
|-------|----------------------|
| Prisma installed | "Prisma (already used)", "TypeORM", "Sequelize" |
| Jest in package.json | "Jest (existing setup)", "Vitest", "Both" |
| Zod for validation | "Zod (current standard)", "Joi", "class-validator" |

**Example**:
```python
# After reading: "package.json has zod@3.21.4"
"options": [
  {"label": "Zod (Recommended)", "description": "Already used in the project"},
  {"label": "Joi", "description": "Different validation library"},
  {"label": "Native validation", "description": "Without external dependencies"}
]
```

---

### Data Model Questions

**Generate from**: Schema files, model definitions, naming conventions

| Pattern Found | Generate Options Like |
|--------------|----------------------|
| Camel case fields | Follow "userId, createdAt" convention |
| Snake case | Follow "user_id, created_at" convention |
| UUID primary keys | Use UUID for consistency |
| Auto-increment IDs | Use integer IDs |

**Example**:
```python
# After reading: "Prisma schema uses camelCase, UUID IDs"
"options": [
  {"label": "UUID + camelCase (Recommended)", "description": "Consistent with existing User, Post models"},
  {"label": "Auto-increment ID", "description": "Use integer IDs"},
  {"label": "Different approach", "description": "Explain in Other"}
]
```

---

### Error Handling Questions

**Generate from**: Existing error classes, response formats, try-catch patterns

| Pattern Found | Generate Options Like |
|--------------|----------------------|
| Custom error classes | Extend existing error hierarchy |
| HTTP status codes | Follow existing response format |
| Error middleware | Use existing middleware |

**Example**:
```python
# After reading: "Found src/errors/AppError.ts base class"
"options": [
  {"label": "Extend AppError (Recommended)", "description": "Add like ValidationError, AuthError"},
  {"label": "New error pattern", "description": "Different error handling approach"},
  {"label": "Throw directly", "description": "Without error classes"}
]
```

---

### Concurrency Questions

**Generate from**: Async patterns, locks, queues, worker pools

| Pattern Found | Generate Options Like |
|--------------|----------------------|
| Bull queue | Use existing queue system |
| file-lock.js | Use project's locking utility |
| Promise.all() | Follow existing async pattern |

---

### Security Questions

**Generate from**: Auth implementation, validation patterns, middleware

| Pattern Found | Generate Options Like |
|--------------|----------------------|
| NextAuth.js | Continue with NextAuth |
| JWT tokens | Follow JWT pattern |
| Input validation | Use existing validation middleware |

---

### UI/UX Questions

**Generate from**: Component library, design system, styling approach

| Pattern Found | Generate Options Like |
|--------------|----------------------|
| Tailwind CSS | Follow Tailwind utility classes |
| Shadcn/ui | Use Shadcn components |
| Custom components | Follow existing component structure |

---

### Observability Questions

**Generate from**: Logging setup, metrics, tracing

| Pattern Found | Generate Options Like |
|--------------|----------------------|
| Winston logger | Use existing logger |
| console.log only | Add proper logging |
| No monitoring | Add monitoring setup |

---

## Bad vs Good Examples

### BAD: Generic Options (Don't Do This)

```python
# Generic, not useful
"options": [
  {"label": "Repository Pattern", "description": "Data access abstraction"},
  {"label": "Active Record", "description": "ORM pattern"},
  {"label": "Raw SQL", "description": "Direct queries"}
]
```

**Why bad**: These options don't reflect the actual codebase. User has to guess what fits.

---

### GOOD: Context-Aware Options (Do This)

```python
# After reading: "Found src/repositories/UserRepository.ts using Prisma"
"options": [
  {"label": "Prisma Repository (Recommended)", "description": "Follows UserRepository pattern, creates src/repositories/ProductRepository"},
  {"label": "Prisma Direct", "description": "Use directly in app/api/products/route.ts without Repository"},
  {"label": "Introduce new pattern", "description": "Different approach (explain in Other)"}
]
```

**Why good**:
- References existing pattern (UserRepository)
- Provides exact file paths
- Explains compatibility with current codebase
- Gives user actionable choices

---

## Validation Checklist

Before presenting options to user, verify:

- [ ] Options reference actual files/patterns from exploration
- [ ] At least one option follows existing codebase pattern
- [ ] Option descriptions mention specific files or conventions
- [ ] Recommended option is marked clearly
- [ ] "Other" option is included for flexibility
