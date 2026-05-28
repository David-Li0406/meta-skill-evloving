---
name: typescript-strict
description: TypeScript strict mode patterns. Use when writing any TypeScript code.
---

# TypeScript Strict Mode

## Core Rules

1. **No `any`** - ever. Use `unknown` if type is truly unknown.
2. **No type assertions** (`as Type`) without justification.
3. **Prefer `type` over `interface`** for data structures.
4. **Reserve `interface`** for behavior contracts only.

---

## Schema Organization

### Organize Schemas by Usage

**Common patterns:**
- Centralized: `src/schemas/` for shared schemas.
- Co-located: Near the modules that use them.
- Layered: Separate by architectural layer (if using layered/hexagonal architecture).

**Key principle:** Avoid duplicating the same validation logic across multiple files.

### Gotcha: Schema Duplication

**Common anti-pattern:**

Defining the same schema in multiple places:
- Validation logic duplicated across endpoints.
- Same business rules defined in multiple adapters.
- Type definitions not shared.

**Why This Is Wrong:**
- ❌ Duplication creates multiple sources of truth.
- ❌ Changes require updating multiple files.
- ❌ Breaks DRY principle at the knowledge level.
- ❌ Domain logic leaks into infrastructure code.

**Solution:**

```typescript
// ✅ CORRECT - Define schema once, import everywhere
import { z } from 'zod';

export const CreateUserRequestSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
});

export type CreateUserRequest = z.infer<typeof CreateUserRequestSchema>;
```

```typescript
// Use in multiple places
import { CreateUserRequestSchema } from '../schemas/user-requests.js';

// Express endpoint
app.post('/users', (req, res) => {
  const result = CreateUserRequestSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ error: result.error });
  }
  // Use result.data (validated)
});

// GraphQL resolver
const createUser = (input: unknown) => {
  const validated = CreateUserRequestSchema.parse(input);
  return userService.create(validated);
};
```

**Key Benefits:**
- ✅ Single source of truth for validation.
- ✅ Schema changes propagate everywhere automatically.
- ✅ Type safety maintained across codebase.
- ✅ DRY principle at knowledge level.

**Remember:** If validation logic is duplicated, extract it into a shared schema.

---

## Dependency Injection Pattern

### Inject Dependencies, Don't Create Them

**The Rule:**
- Dependencies are always injected via parameters.
- Never use `new` to create dependencies inside functions.
- Factory functions accept dependencies as parameters.

### Why This Matters

Without dependency injection:
- ❌ Only one implementation possible.
- ❌ Can't test with mocks (poor testability).
- ❌ Tight coupling to specific implementations.
- ❌ Violates dependency inversion principle.
- ❌ Can't swap implementations.

With dependency injection:
- ✅ Any implementation works (in-memory, database, remote API).
- ✅ Fully testable (inject mocks for testing).
- ✅ Loose coupling.
- ✅ Follows dependency inversion principle.
- ✅ Runtime flexibility (configure implementation).

### Example: Order Processor

**❌ WRONG - Creating implementation internally**

```typescript
export const createOrderProcessor = ({
  paymentGateway,
}: {
  paymentGateway: PaymentGateway;
}): OrderProcessor => {
  // ❌ Hardcoded implementation!
  const orderRepository = new InMemoryOrderRepository();

  return {
    processOrder(order) {
      const payment = paymentGateway.charge(order.total);
      if (!payment.success) {
        return { success: false, error: payment.error };
      }

      orderRepository.save(order); // Using hardcoded repository
      return { success: true, data: order };
    },
  };
};
```

**✅ CORRECT - Injecting all dependencies**

```typescript
export const createOrderProcessor = ({
  paymentGateway,  // ✅ Injected
  orderRepository, // ✅ Injected
}: {
  paymentGateway: PaymentGateway;
  orderRepository: OrderRepository;
}): OrderProcessor => {
  return {
    processOrder(order) {
      const payment = paymentGateway.charge(order.total);
      if (!payment.success) {
        return { success: false, error: payment.error };
      }

      orderRepository.save(order); // Delegate to injected dependency
      return { success: true, data: order };
    },
  };
};
```

---

## Type vs Interface - Understanding WHY

The choice between `type` and `interface` is architectural, not stylistic.

### Behavior Contracts → Use `interface`

**When to use:** Interfaces define contracts that must be implemented.

**Examples**: `UserRepository`, `PaymentGateway`, `EmailService`, `CacheProvider`.

**Why `interface` for behavior contracts?**
1. **Signals implementation contracts clearly.**
2. **Better TypeScript errors when implementing.**
3. **Conventional for dependency injection.**
4. **Class-friendly for implementations.**

### Data Structures → Use `type`

**When to use:** Types define immutable data structures.

**Examples**: `User`, `Order`, `Config`, `ApiResponse`.

**Why `type` for data?**
1. **Emphasizes immutability.**
2. **Better for unions, intersections, mapped types.**
3. **Prevents accidental mutations.**
4. **More flexible composition.**

---

## Strict Mode Configuration

### tsconfig.json Settings

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,
    "forceConsistentCasingInFileNames": true,
    "allowUnusedLabels": false
  }
}
```

### What Each Setting Does

**Core strict flags:**
- **`strict: true`** - Enables all strict type checking options.
- **`noImplicitAny`** - Error on expressions/declarations with implied `any` type.
- **`strictNullChecks`** - `null` and `undefined` have their own types (not assignable to everything).
- **`noUnusedLocals`** - Error on unused local variables.
- **`noUnusedParameters`** - Error on unused function parameters.
- **`noImplicitReturns`** - Error when not all code paths return a value.
- **`noFallthroughCasesInSwitch`** - Error on fallthrough cases in switch statements.

**Additional safety flags (CRITICAL):**
- **`noUncheckedIndexedAccess`** - Array/object access returns `T | undefined`.
- **`exactOptionalPropertyTypes`** - Distinguishes `property?: T` from `property: T | undefined`.
- **`noPropertyAccessFromIndexSignature`** - Requires bracket notation for index signature properties.
- **`forceConsistentCasingInFileNames`** - Prevents case sensitivity issues across operating systems.
- **`allowUnusedLabels`** - Error on unused labels.

### Additional Rules

- **No `@ts-ignore`** without explicit comments explaining why.
- **These rules apply to test code as well as production code.**

---

## Immutability Patterns

### Use `readonly` on All Data Structures

```typescript
// ✅ CORRECT - Immutable data structure
type ApiRequest = {
  readonly method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  readonly url: string;
  readonly headers?: {
    readonly [key: string]: string;
  };
  readonly body?: unknown;
};
```

### ReadonlyArray vs Array

```typescript
// ✅ CORRECT - Immutable array
type ShoppingCart = {
  readonly id: string;
  readonly items: ReadonlyArray<CartItem>;
};
```

### Result Type Pattern for Error Handling

Prefer `Result<T, E>` types over exceptions for expected errors:

```typescript
export type Result<T, E = Error> =
  | { readonly success: true; readonly data: T }
  | { readonly success: false; readonly error: E };

// Usage
export const findUser = (
  userId: string,
): Result<User> => {
  const user = database.findById(userId);
  if (!user) {
    return { success: false, error: new Error('User not found') };
  }

  return { success: true, data: user };
};
```

---

## Factory Pattern for Object Creation

### Use Factory Functions (Not Classes)

```typescript
// ✅ CORRECT - Factory function
export const createOrderService = (
  orderRepository: OrderRepository,
  paymentGateway: PaymentGateway,
): OrderService => {
  return {
    async createOrder(order) {
      const validation = validateOrder(order);
      if (!validation.success) {
        return validation;
      }
      await orderRepository.save(order);
      return { success: true, data: order };
    },
    async processPayment(orderId, paymentInfo) {
      const order = await orderRepository.findById(orderId);
      if (!order) {
        return { success: false, error: new Error('Order not found') };
      }
      return paymentGateway.charge(order.total, paymentInfo);
    },
  };
};
```

---

## Location Guidance

### Suggested File Organization

These are common patterns, not strict rules. Adapt to your project's needs.

**Interfaces (Behavior Contracts)**
- Common locations: `src/interfaces/`, `src/contracts/`, `src/ports/`.

**Types (Data Structures)**
- Common locations: `src/types/`, `src/models/`, co-located with features.

**Schemas (Validation)**
- Common locations: `src/schemas/`, `src/validation/`, co-located with features.

**Business Logic**
- Common locations: `src/services/`, `src/domain/`, `src/use-cases/`.

**Implementation Details**
- Common locations: `src/adapters/`, `src/infrastructure/`, `src/repositories/`.

---

## Schema-First at Trust Boundaries

### When Schemas ARE Required

- Data crosses trust boundary (external → internal).
- Type has validation rules (format, constraints).
- Shared data contract between systems.
- Used in test factories (validate test data completeness).

### When Schemas AREN'T Required

- Pure internal types (utilities, state).
- Result/Option types (no validation needed).
- TypeScript utility types (`Partial<T>`, `Pick<T>`, etc.).
- Behavior contracts (interfaces - structural, not validated).
- Component props (unless from URL/API).

---

## Functional Programming Principles

These principles support immutability and type safety:

### Pure Functions

- No side effects (don't mutate external state).
- Deterministic (same input → same output).

### No Data Mutation

- Use spread operators for immutable updates.
- Return new objects/arrays instead of modifying.

### Composition Over Complex Logic

- Compose small functions into larger ones.
- Each function does one thing well.

### Use Array Methods Over Loops

- Prefer `map`, `filter`, `reduce` for transformations.
- Declarative (what, not how).

---

## Branded Types

For type-safe primitives:

```typescript
type UserId = string & { readonly brand: unique symbol };
type PaymentAmount = number & { readonly brand: unique symbol };

// Type-safe at compile time
const processPayment = (userId: UserId, amount: PaymentAmount) => {
  // Implementation
};
```

---

## Summary Checklist

When writing TypeScript code, verify:

- [ ] No `any` types - using `unknown` where type is truly unknown.
- [ ] No type assertions without justification.
- [ ] Using `type` for data structures with `readonly`.
- [ ] Using `interface` for behavior contracts (ports).
- [ ] Schemas defined in core, not duplicated in adapters.
- [ ] Ports injected via parameters, never created internally.
- [ ] Factory functions for object creation (not classes).
- [ ] `readonly` on all data structure properties.
- [ ] Pure functions wherever possible (no mutations).
- [ ] Result types for expected errors (not exceptions).
- [ ] Strict mode enabled with all checks passing.
- [ ] Artifacts in correct locations (ports/, types/, schemas/, domain/).