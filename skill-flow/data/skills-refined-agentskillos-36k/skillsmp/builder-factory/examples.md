# Builder Examples

Complete examples of test-data-bot builders for various use cases.

> **Note:** Check `.claude/project-context.md` for your specific Faker locale and project types.

## Complete Builder with Traits

```typescript
import { build, sequence, perBuild } from "@jackfranklin/test-data-bot";
import { faker } from "@faker-js/faker"; // Check project-context.md for locale
import type { User } from "~/types/user";

export const userBuilder = build<User>({
  fields: {
    id: sequence(),
    email: perBuild(() => faker.internet.email()),
    firstName: perBuild(() => faker.person.firstName()),
    lastName: perBuild(() => faker.person.lastName()),
    role: "user",
    isActive: true
  },
  traits: {
    admin: {
      overrides: {
        role: "admin",
        email: perBuild(() => faker.internet.email({ provider: "company.com" }))
      }
    },
    inactive: {
      overrides: {
        isActive: false
      }
    },
    guest: {
      overrides: {
        role: "guest",
        firstName: "Guest",
        lastName: perBuild(() => faker.string.numeric(4))
      }
    }
  }
});

// Usage examples:
// userBuilder.one()
// userBuilder.one({ traits: ["admin"] })
// userBuilder.one({ traits: ["admin", "inactive"] })
// userBuilder.one({ overrides: { firstName: "Jan" } })
```

## Builder with postBuild Hook

```typescript
import { build, sequence, perBuild } from "@jackfranklin/test-data-bot";
import { faker } from "@faker-js/faker"; // Check project-context.md for locale
import type { Order } from "~/types/order";

export const orderBuilder = build<Order>({
  fields: {
    id: sequence(),
    userId: sequence(),
    products: perBuild(() => Array.from({ length: 3 }, () => productBuilder.one())),
    totalAmount: 0,
    status: perBuild(() => faker.helpers.arrayElement(["pending", "processing"])),
    createdAt: perBuild(() => faker.date.recent()),
    shippingAddress: perBuild(() => addressBuilder.one())
  },
  postBuild: (order) => {
    order.totalAmount = order.products.reduce((sum, p) => sum + p.price, 0);
    return order;
  },
  traits: {
    bigOrder: {
      overrides: {
        products: perBuild(() => Array.from({ length: 10 }, () => productBuilder.one()))
      }
    }
  }
});
```

## Nested Builders

```typescript
// Address builder
export const addressBuilder = build<Address>({
  fields: {
    street: perBuild(() => faker.location.streetAddress()),
    city: perBuild(() => faker.location.city()),
    zipCode: perBuild(() => faker.location.zipCode()),
    country: "USA" // Check project-context.md for your locale
  }
});

// User builder with address
export const userBuilder = build<User>({
  fields: {
    id: sequence(),
    name: perBuild(() => faker.person.fullName()),
    address: perBuild(() => addressBuilder.one())
  }
});

// Override nested
const user = userBuilder.one({
  overrides: {
    address: addressBuilder.one({ overrides: { city: "New York" } })
  }
});
```

## Database Application Type Builder

> **Note:** Check project-context.md for your specific database type patterns (Firestore, PostgreSQL, MongoDB, etc.)

```typescript
import { build, sequence, perBuild } from "@jackfranklin/test-data-bot";
import { faker } from "@faker-js/faker"; // Check project-context.md for locale
import type { Resource, ResourceBase } from "~/features/resource/types/resource";

// Base type builder (for DTOs)
export const resourceBaseBuilder = build<ResourceBase>({
  fields: {
    name: perBuild(() => faker.commerce.productName()),
    status: "active",
    category: perBuild(() => faker.commerce.department())
  },
  traits: {
    inactive: {
      overrides: {
        status: "inactive"
      }
    },
    pending: {
      overrides: {
        status: "pending"
      }
    }
  }
});

// Application type builder (with id and timestamps)
export const resourceBuilder = build<Resource>({
  fields: {
    id: perBuild(() => faker.string.uuid()),
    name: perBuild(() => faker.commerce.productName()),
    status: "active",
    category: perBuild(() => faker.commerce.department()),
    createdAt: perBuild(() => faker.date.past()),
    updatedAt: perBuild(() => faker.date.recent())
  },
  traits: {
    inactive: {
      overrides: {
        status: "inactive"
      }
    },
    pending: {
      overrides: {
        status: "pending"
      }
    }
  }
});
```

## Helper Functions Pattern

```typescript
export const createTestUsers = {
  admin: () => userBuilder.one({ traits: ["admin"] }),
  guest: () => userBuilder.one({ traits: ["guest"] }),
  inactive: () => userBuilder.one({ traits: ["inactive"] }),
  withCustomEmail: (email: string) => userBuilder.one({ overrides: { email } }),
  list: (count: number) => Array.from({ length: count }, () => userBuilder.one())
};

// Usage
const admin = createTestUsers.admin();
const users = createTestUsers.list(5);
```

## Computed Fields with postBuild

```typescript
export const accountBuilder = build<Account>({
  fields: {
    id: sequence(),
    balance: perBuild(() => faker.number.int({ min: 0, max: 10000 })),
    type: "basic",
    creditLimit: 0
  },
  postBuild: (account) => {
    switch (account.type) {
      case "premium":
        account.creditLimit = 5000;
        break;
      case "vip":
        account.creditLimit = 20000;
        break;
      default:
        account.creditLimit = 0;
    }
    return account;
  },
  traits: {
    premium: { overrides: { type: "premium" } },
    vip: { overrides: { type: "vip" } }
  }
});
```
