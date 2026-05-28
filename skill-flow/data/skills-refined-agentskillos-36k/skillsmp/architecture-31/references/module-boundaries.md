# Module Boundaries Reference

## What is a Module?

A module is a cohesive unit of code with:
- **Clear public API** — What it exposes to the outside world
- **Hidden implementation** — Internal details others shouldn't depend on
- **Defined dependencies** — What it needs from other modules

---

## Module Structure

### Standard Layout

```
module-name/
├── index.ts              # Public API (barrel export)
├── types.ts              # Public types
├── module-name.service.ts    # Internal implementation
├── module-name.repository.ts # Internal implementation
├── helpers/              # Internal utilities
│   └── validation.ts
└── __tests__/            # Tests
    └── module-name.test.ts
```

### The Index File

The `index.ts` file is the **only** entry point:

```typescript
// index.ts - Public API
export { UserService } from './user.service';
export { createUser, updateUser } from './user.operations';
export type { User, UserCreateInput, UserUpdateInput } from './types';

// DO NOT export internal helpers, repositories, or implementation details
```

---

## Boundary Rules

### Rule 1: Single Entry Point

All imports from outside the module MUST go through `index.ts`:

```typescript
// ✅ Correct
import { UserService, User } from '@/modules/users';

// ❌ Wrong - reaching into internals
import { UserService } from '@/modules/users/user.service';
import { validateUser } from '@/modules/users/helpers/validation';
```

### Rule 2: No Circular Dependencies

Modules cannot depend on each other in a cycle:

```
users → orders → users  ❌
```

**Solutions:**
1. Extract shared code to a new module
2. Use events/callbacks instead of direct calls
3. Introduce an interface to break the cycle

### Rule 3: Own Your Data

Each module owns its data exclusively:

```typescript
// UserModule owns the users table
// OrderModule CANNOT directly access users table

// ❌ Wrong
class OrderService {
  async getOrder(id: string) {
    const order = await this.db.orders.find(id);
    const user = await this.db.users.find(order.userId); // NO!
    return { order, user };
  }
}

// ✅ Correct
class OrderService {
  constructor(private userService: UserService) {}

  async getOrder(id: string) {
    const order = await this.db.orders.find(id);
    const user = await this.userService.getById(order.userId); // YES!
    return { order, user };
  }
}
```

---

## Communication Patterns

### Pattern 1: Direct API Call

Use when: Synchronous, request-response needed

```typescript
// OrderService calls UserService directly
const user = await userService.getById(userId);
```

### Pattern 2: Events

Use when: Fire-and-forget, multiple listeners

```typescript
// UserModule emits event
eventBus.emit('user.created', { userId, email });

// OrderModule listens
eventBus.on('user.created', async ({ userId }) => {
  await orderService.initializeCart(userId);
});
```

### Pattern 3: Shared Types

Use when: Common data structures

```typescript
// shared/types/user.ts
export interface UserReference {
  id: string;
  name: string;
}

// Both modules import the same type
import { UserReference } from '@/shared/types/user';
```

---

## Coupling Levels

### Acceptable Coupling

| Type | Example | When OK |
|------|---------|---------|
| Type imports | `import type { User }` | Always |
| Read operations | `userService.getById()` | Usually |
| Stateless transforms | `formatUser(user)` | Usually |

### Dangerous Coupling

| Type | Example | Why Bad |
|------|---------|---------|
| Internal imports | `import { helper } from './internal'` | Breaks encapsulation |
| Shared mutable state | Global variables | Hidden dependencies |
| Deep object access | `user.address.city.zipCode` | Tight coupling |
| Direct DB access | `db.users.find()` across modules | Bypasses ownership |

---

## Refactoring Boundaries

### Signs You Need to Split

- Module has multiple unrelated responsibilities
- Changes in one area always affect another
- Different teams work on different parts
- Different testing/deployment needs

### Signs You Should Merge

- Two modules are always changed together
- Circular dependencies keep appearing
- Communication overhead exceeds benefit
- Very small modules with heavy dependencies

---

## Testing at Boundaries

### Unit Tests (Inside Module)

Test internal logic in isolation:

```typescript
describe('UserService', () => {
  it('validates email format', () => {
    expect(userService.validateEmail('bad')).toBe(false);
    expect(userService.validateEmail('good@email.com')).toBe(true);
  });
});
```

### Integration Tests (At Boundaries)

Test module interactions:

```typescript
describe('Order creation', () => {
  it('reserves inventory when order placed', async () => {
    const order = await orderService.create(orderInput);
    const inventory = await inventoryService.getStock(productId);
    expect(inventory.reserved).toBe(order.quantity);
  });
});
```

### Contract Tests

Verify API contracts between modules:

```typescript
describe('UserService contract', () => {
  it('getById returns user matching UserResponse schema', async () => {
    const user = await userService.getById('123');
    expect(user).toMatchSchema(UserResponseSchema);
  });
});
```

---

## Boundary Checklist

Before adding a new module boundary:

- [ ] Clear single responsibility defined
- [ ] Public API is minimal and stable
- [ ] No circular dependencies introduced
- [ ] Data ownership is clear
- [ ] Communication pattern chosen
- [ ] Tests cover the boundary
