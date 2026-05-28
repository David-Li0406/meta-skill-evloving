---
name: architecture-review
description: |
  Architecture design review skill for reviewer agents.
  Component boundaries, separation of concerns, modularity, and design pattern validation.
  Use during PLANNING phase to validate design decisions and VERIFICATION to ensure adherence.
---

# Architecture Review

Architecture and design pattern validation for ultrawork planning and verification phases.

## What This Skill Provides

Structured approach to evaluating:
- Component boundaries and separation of concerns
- Modularity and coupling
- Design patterns and architectural principles
- Scalability and maintainability
- API design and interfaces

## When to Use This Skill

**During PLANNING phase:**
- Reviewing planner's task decomposition
- Validating design documents
- Assessing technical approach
- Identifying architectural risks

**During VERIFICATION phase:**
- Ensuring implementation matches design
- Checking component boundaries
- Validating separation of concerns
- Reviewing integration points

## Core Principles

### 1. Separation of Concerns (SoC)

**Checklist:**

```
[ ] Business logic separated from presentation
[ ] Data access layer isolated
[ ] Authentication/authorization in dedicated modules
[ ] Configuration separate from code
[ ] API routes separate from business logic
[ ] Validation logic reusable across layers
[ ] Error handling centralized
[ ] Logging abstracted
```

**Red Flags:**
- Business logic in React components
- Database queries in route handlers
- Authentication mixed with business logic
- Configuration hardcoded in multiple files

**Examples:**

```javascript
// ❌ Bad: Mixed concerns
app.post('/api/users', async (req, res) => {
  // Authentication + validation + business logic + DB access in one place
  if (!req.headers.authorization) return res.status(401).json({ error: 'Unauthorized' });
  if (!req.body.email) return res.status(400).json({ error: 'Email required' });
  const user = await db.users.create(req.body);
  res.json(user);
});

// ✅ Good: Separated concerns
app.post('/api/users',
  authenticate,           // Auth middleware
  validateCreateUser,     // Validation middleware
  createUserHandler       // Route handler delegates to service
);

async function createUserHandler(req, res) {
  const user = await userService.createUser(req.body); // Business logic in service
  res.json(user);
}
```

### 2. Component Boundaries

**Checklist:**

```
[ ] Components have clear, single responsibilities
[ ] Component interfaces are well-defined
[ ] Dependencies flow in one direction (no circular deps)
[ ] Components are independently testable
[ ] Public APIs are minimal (principle of least exposure)
[ ] Internal implementation details are hidden
[ ] Components can be replaced without breaking others
```

**Red Flags:**
- Circular dependencies (A imports B, B imports A)
- God objects (classes with 10+ responsibilities)
- Tight coupling (changes in A always require changes in B)
- Leaky abstractions (internal details exposed)

**Dependency Flow:**

```
Presentation → Business Logic → Data Access → Database
     ↓              ↓                ↓
   UI Layer    Service Layer    Repository Layer

NEVER: Data Access → Presentation (wrong direction!)
```

### 3. Modularity and Coupling

**Checklist:**

```
[ ] Modules are cohesive (related functionality grouped)
[ ] Low coupling between modules
[ ] Shared code in libraries/utilities
[ ] Feature folders group related files
[ ] Module exports are explicit and minimal
[ ] Dependencies are injected (not hardcoded)
[ ] Configuration passed from outside
```

**Cohesion vs Coupling:**

| Good Modularity | Bad Modularity |
|-----------------|----------------|
| High cohesion (related code together) | Low cohesion (unrelated code mixed) |
| Low coupling (minimal dependencies) | High coupling (everything depends on everything) |
| Clear interfaces | Implicit contracts |
| Dependency injection | Hardcoded dependencies |

**Examples:**

```javascript
// ❌ Bad: High coupling, hardcoded dependencies
class UserService {
  constructor() {
    this.db = new PostgresDB(); // Hardcoded!
    this.logger = console;       // Hardcoded!
  }
}

// ✅ Good: Low coupling, dependency injection
class UserService {
  constructor(database, logger) {
    this.db = database;
    this.logger = logger;
  }
}

// Usage: dependencies injected
const userService = new UserService(
  new PostgresDB(config.db),
  new Logger(config.logging)
);
```

### 4. Design Patterns

**Checklist:**

```
[ ] Patterns used appropriately (not overengineered)
[ ] Consistent patterns across codebase
[ ] Standard patterns preferred over custom solutions
[ ] Patterns documented in code
```

**Common Patterns:**

| Pattern | Use When | Example |
|---------|----------|---------|
| Repository | Data access abstraction | `userRepository.findById(id)` |
| Service | Business logic encapsulation | `orderService.placeOrder()` |
| Factory | Object creation complexity | `PaymentFactory.create(type)` |
| Strategy | Swappable algorithms | `ShippingStrategy.calculate()` |
| Middleware | Request/response processing | Express middleware |
| Observer | Event-driven updates | Event emitters, pub/sub |

**Red Flags:**
- Patterns used incorrectly
- Over-abstraction (patterns for simple problems)
- Mixing patterns inconsistently
- Custom patterns when standard ones exist

### 5. API Design

**Checklist:**

```
[ ] RESTful conventions followed (GET/POST/PUT/DELETE)
[ ] Consistent URL structure
[ ] Proper HTTP status codes
[ ] Versioning strategy defined
[ ] Request/response schemas documented
[ ] Error responses are consistent
[ ] Pagination for collections
[ ] Filtering and sorting supported where needed
```

**REST Conventions:**

| HTTP Method | Purpose | Idempotent? |
|-------------|---------|-------------|
| GET | Retrieve resource | Yes |
| POST | Create resource | No |
| PUT | Update/replace resource | Yes |
| PATCH | Partial update | No |
| DELETE | Remove resource | Yes |

**Examples:**

```javascript
// ❌ Bad: Inconsistent, non-RESTful
POST /getUser
POST /deleteUser
GET /updateUser?id=123&name=John

// ✅ Good: RESTful, consistent
GET    /api/users/:id      (retrieve)
POST   /api/users          (create)
PUT    /api/users/:id      (update)
DELETE /api/users/:id      (delete)
```

### 6. Scalability Considerations

**Checklist:**

```
[ ] Stateless design (no server-side state)
[ ] Database queries optimized (indexes, joins)
[ ] Caching strategy defined
[ ] Async operations for I/O
[ ] Rate limiting implemented
[ ] Pagination on large datasets
[ ] Background jobs for heavy processing
[ ] CDN for static assets
```

**Red Flags:**
- Storing state in memory (server-side sessions)
- Synchronous blocking operations
- No caching for expensive operations
- Loading entire tables
- Missing indexes on query columns

## Layer Architecture Patterns

### 3-Tier Architecture

```
┌─────────────────────┐
│  Presentation Layer │  (UI, API routes)
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│   Business Layer    │  (Services, logic)
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│    Data Layer       │  (Repositories, DB)
└─────────────────────┘
```

**Rules:**
- Upper layers can call lower layers
- Lower layers CANNOT call upper layers
- Layers communicate via interfaces

### Feature-Based Structure

```
src/
├── features/
│   ├── auth/
│   │   ├── auth.service.ts
│   │   ├── auth.controller.ts
│   │   ├── auth.repository.ts
│   │   └── auth.test.ts
│   ├── users/
│   │   ├── user.service.ts
│   │   ├── user.controller.ts
│   │   └── user.repository.ts
├── shared/
│   ├── utils/
│   ├── middleware/
│   └── types/
```

**Benefits:**
- Related code together
- Easy to find files
- Scalable structure
- Clear ownership

## Review Process

### Step 1: High-Level Assessment

Answer:
- What is the overall architecture pattern?
- Are responsibilities clearly separated?
- Is the dependency flow correct?
- Can components be tested independently?

### Step 2: Component Analysis

For each component:
- What is its single responsibility?
- What are its dependencies?
- Is its interface minimal and clear?
- Is it properly abstracted?

### Step 3: Integration Review

Check:
- How do components communicate?
- Are interfaces well-defined?
- Is error handling consistent?
- Are transactions handled correctly?

### Step 4: Design Document Review

Verify:
- Design rationale is documented
- Trade-offs are explained
- Alternative approaches considered
- Scalability addressed
- Security considered

## Architecture Smells

| Smell | Description | Fix |
|-------|-------------|-----|
| Big Ball of Mud | No clear structure | Refactor into layers |
| God Object | Class does everything | Split into focused classes |
| Spaghetti Code | Tangled dependencies | Extract interfaces, dependency injection |
| Circular Dependencies | A depends on B, B depends on A | Introduce abstraction layer |
| Tight Coupling | Changes cascade everywhere | Loose coupling via interfaces |
| Anemic Domain | Logic scattered, not in models | Move logic to domain models |

## Design Principles (SOLID)

### S - Single Responsibility Principle

Each class/module has one reason to change.

```javascript
// ❌ Bad: Multiple responsibilities
class UserManager {
  createUser() { /* ... */ }
  sendEmail() { /* ... */ }
  logActivity() { /* ... */ }
}

// ✅ Good: Single responsibility
class UserService {
  createUser() { /* ... */ }
}
class EmailService {
  sendEmail() { /* ... */ }
}
```

### O - Open/Closed Principle

Open for extension, closed for modification.

```javascript
// ❌ Bad: Must modify for new types
function calculateShipping(order) {
  if (order.type === 'standard') return 5;
  if (order.type === 'express') return 15;
  // Must modify function for new types
}

// ✅ Good: Extend via strategy pattern
class StandardShipping {
  calculate() { return 5; }
}
class ExpressShipping {
  calculate() { return 15; }
}
```

### L - Liskov Substitution Principle

Subtypes must be substitutable for base types.

### I - Interface Segregation Principle

Many small interfaces better than one large interface.

### D - Dependency Inversion Principle

Depend on abstractions, not concrete implementations.

## Evidence Collection

When reviewing architecture:

```bash
# Add architecture assessment to evidence
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id verify \
  --add-evidence "Architecture Review: PASS" \
  --add-evidence "- Clear separation of concerns" \
  --add-evidence "- Proper component boundaries" \
  --add-evidence "- No circular dependencies" \
  --add-evidence "- RESTful API design"
```

## Common Issues and Fixes

| Issue | Impact | Fix |
|-------|--------|-----|
| Business logic in controllers | Hard to test, hard to reuse | Extract to service layer |
| No repository layer | Direct DB coupling | Introduce repository pattern |
| Circular dependencies | Build errors, tight coupling | Introduce abstraction layer |
| God classes | Unmaintainable | Split by responsibility |
| No interfaces | Tight coupling | Define clear interfaces |
| Mixed layers | Confusion, bugs | Enforce layer boundaries |

## Integration with Ultrawork

### During PLANNING Phase

```bash
# Review design document
Read("$SESSION_DIR/docs/plans/design.md")

# Check task decomposition aligns with architecture
bun "{SCRIPTS_PATH}/task-list.js" --session ${CLAUDE_SESSION_ID}

# Validate component boundaries in plan
```

### During VERIFICATION Phase

```bash
# Check implementation matches design
git diff

# Verify component boundaries maintained
# Check for circular dependencies
# Validate layer separation
```

## Quick Reference

**Must-have architecture standards:**
- Clear layer separation (presentation/business/data)
- Single responsibility per component
- Dependency injection for flexibility
- RESTful API conventions
- No circular dependencies

**Red flags:**
- Business logic in presentation layer
- Circular dependencies
- God objects/classes
- Tight coupling
- Inconsistent patterns
