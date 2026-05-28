# Branded Types

> **When to use:** To prevent mixing up incompatible types, such as different kinds of IDs (e.g., `UserId` vs `OrderId`), units of measurement (e.g., `Meters` vs `Feet`), or validated strings (e.g., `Email`, `UUID`).

Use branded types to create nominal types that prevent accidental mixing. **Avoid using `as` for branding** — use Zod or type-fest instead for proper runtime validation.

## With Zod (Recommended)

```typescript
import { z } from 'zod';

// Define branded schemas (Schema suffix for clarity)
const UserIdSchema = z.string().uuid().brand('UserId');
const OrderIdSchema = z.string().uuid().brand('OrderId');

// Infer branded types
type UserId = z.infer<typeof UserIdSchema>;  // string & { __brand: 'UserId' }
type OrderId = z.infer<typeof OrderIdSchema>;

// Parse and validate with branding
const userId = UserIdSchema.parse('550e8400-e29b-41d4-a716-446655440000');
// userId is now typed as UserId, not just string

// Use in functions
function getUser(id: UserId): User { /* ... */ }

getUser(userId);                        // OK - properly branded
getUser('raw-string');                  // Error - not branded
getUser(OrderIdSchema.parse('...'));    // Error - wrong brand
```

## With type-fest

[type-fest](https://github.com/sindresorhus/type-fest) provides `Tagged` for branding without runtime validation:

```typescript
import type { Tagged } from 'type-fest';

type UserId = Tagged<string, 'UserId'>;
type OrderId = Tagged<string, 'OrderId'>;

// Create branded values through validated functions
function createUserId(id: string): UserId {
  if (!isValidUuid(id)) throw new Error('Invalid UUID');
  return id as UserId;  // as is acceptable inside factory functions
}

const userId = createUserId('550e8400-e29b-41d4-a716-446655440000');
```

## DON'T: Use `as` directly

```typescript
// DON'T: Direct casting bypasses validation
const userId = 'invalid-string' as UserId;  // No validation!
```

## When to Use Branded Types

| Use Case | Example |
|----------|---------|
| IDs that shouldn't be mixed | `UserId`, `OrderId`, `ProductId` |
| Units that shouldn't be mixed | `Meters`, `Feet`, `Celsius`, `Fahrenheit` |
| Validated strings | `Email`, `URL`, `UUID` |
| Money with different currencies | `USD`, `EUR`, `JPY` |
