---
name: electrodb
description: ElectroDB patterns for DynamoDB single-table design with full type safety and optimized access patterns
---

# ElectroDB Patterns

This skill covers ElectroDB v2+ patterns for building type-safe, performant DynamoDB applications with single-table design.

## Core Concepts

**ElectroDB Benefits:**
- Type-safe queries and mutations
- Automatic key generation
- Collection queries (fetch related entities)
- Composite attributes and computed keys
- Built-in validation
- Query building with IntelliSense

**Key Terms:**
- **Entity**: Table schema definition
- **Service**: Multiple entities working together
- **Collection**: Group related entities for efficient queries
- **Access Pattern**: How you retrieve data (GSI, queries)
- **Composite Attributes**: Combine fields into keys

## Installation

```bash
npm install electrodb
```

## Entity Definition

### Basic Entity

```typescript
// src/entities/user.entity.ts
import { Entity } from "electrodb";
import { dynamoDBClient } from "../lib/db";

export const UserEntity = new Entity(
  {
    model: {
      entity: "user",
      version: "1",
      service: "myapp",
    },
    attributes: {
      userId: {
        type: "string",
        required: true,
      },
      email: {
        type: "string",
        required: true,
      },
      name: {
        type: "string",
        required: true,
      },
      role: {
        type: ["ADMIN", "TEACHER", "STUDENT"] as const,
        required: true,
        default: "STUDENT",
      },
      verified: {
        type: "boolean",
        default: false,
      },
      createdAt: {
        type: "string",
        required: true,
        default: () => new Date().toISOString(),
        readOnly: true,
      },
      updatedAt: {
        type: "string",
        required: true,
        default: () => new Date().toISOString(),
        set: () => new Date().toISOString(),
        watch: "*", // Update on any attribute change
      },
    },
    indexes: {
      primary: {
        pk: {
          field: "pk",
          composite: ["userId"],
        },
        sk: {
          field: "sk",
          composite: [],
        },
      },
      byEmail: {
        index: "gsi1",
        pk: {
          field: "gsi1pk",
          composite: ["email"],
        },
        sk: {
          field: "gsi1sk",
          composite: [],
        },
      },
      byRole: {
        index: "gsi2",
        pk: {
          field: "gsi2pk",
          composite: ["role"],
        },
        sk: {
          field: "gsi2sk",
          composite: ["createdAt"],
        },
      },
    },
  },
  { client: dynamoDBClient, table: "MyAppTable" }
);

// Type inference
export type User = typeof UserEntity.model.schema;
export type UserItem = ReturnType<typeof UserEntity.parse>;
```

### Advanced Attributes

```typescript
export const SessionEntity = new Entity({
  model: {
    entity: "session",
    version: "1",
    service: "myapp",
  },
  attributes: {
    sessionId: {
      type: "string",
      required: true,
    },
    userId: {
      type: "string",
      required: true,
    },
    courseId: {
      type: "string",
      required: true,
    },
    // Composite attribute (virtual)
    userCourse: {
      type: "string",
      hidden: true, // Not returned in queries
      readOnly: true,
      get: (_, item) => `${item.userId}#${item.courseId}`,
    },
    // Date as string
    scheduledDate: {
      type: "string",
      required: true,
      validate: (value) => {
        const date = new Date(value);
        if (isNaN(date.getTime())) {
          throw new Error("Invalid date format");
        }
      },
    },
    // Duration in minutes
    durationMinutes: {
      type: "number",
      required: true,
      validate: (value) => {
        if (value < 15 || value > 480) {
          throw new Error("Duration must be between 15 and 480 minutes");
        }
      },
    },
    // Enum-like status
    status: {
      type: ["SCHEDULED", "IN_PROGRESS", "COMPLETED", "CANCELLED"] as const,
      required: true,
      default: "SCHEDULED",
    },
    // Optional nested object
    metadata: {
      type: "map",
      properties: {
        zoomMeetingId: { type: "string" },
        recordingUrl: { type: "string" },
        notes: { type: "string" },
      },
    },
    // Array of strings
    tags: {
      type: "list",
      items: {
        type: "string",
      },
    },
    // Set attribute (for watch)
    watchedAttributes: {
      type: "set",
      items: "string",
    },
  },
  indexes: {
    primary: {
      pk: {
        field: "pk",
        composite: ["sessionId"],
      },
      sk: {
        field: "sk",
        composite: [],
      },
    },
    byCourse: {
      index: "gsi1",
      pk: {
        field: "gsi1pk",
        composite: ["courseId"],
      },
      sk: {
        field: "gsi1sk",
        composite: ["scheduledDate"],
      },
    },
    byUser: {
      index: "gsi2",
      pk: {
        field: "gsi2pk",
        composite: ["userId"],
      },
      sk: {
        field: "gsi2sk",
        composite: ["scheduledDate"],
      },
    },
  },
});
```

## CRUD Operations

### Create

```typescript
// Create single item
const user = await UserEntity.create({
  userId: "user_123",
  email: "john@example.com",
  name: "John Doe",
  role: "STUDENT",
}).go();

// Create with custom options
const user = await UserEntity.create({
  userId: "user_123",
  email: "john@example.com",
  name: "John Doe",
}).go({
  response: "all_new", // Return all attributes
});

// Conditional create (fail if exists)
const user = await UserEntity.create({
  userId: "user_123",
  email: "john@example.com",
  name: "John Doe",
}).go({
  conditions: { exists: false }, // Only create if doesn't exist
});
```

### Read (Get)

```typescript
// Get single item
const user = await UserEntity.get({
  userId: "user_123",
}).go();

// user.data contains the item or null if not found
if (!user.data) {
  throw new Error("User not found");
}

// Get with specific attributes
const user = await UserEntity.get({
  userId: "user_123",
}).go({
  attributes: ["name", "email"], // Only fetch these fields
});

// Get with consistent read
const user = await UserEntity.get({
  userId: "user_123",
}).go({
  consistent: true, // Consistent read (costs more)
});
```

### Update

```typescript
// Update specific attributes
const updated = await UserEntity.update({
  userId: "user_123",
}).set({
  name: "Jane Doe",
  verified: true,
}).go();

// Add to number
await SessionEntity.update({
  sessionId: "session_123",
}).add({
  attendeeCount: 1, // Increment by 1
}).go();

// Remove attribute
await UserEntity.update({
  userId: "user_123",
}).remove(["temporaryToken"]).go();

// Conditional update
await UserEntity.update({
  userId: "user_123",
}).set({
  verified: true,
}).go({
  conditions: { verified: false }, // Only update if not already verified
});

// Update with custom condition expression
await UserEntity.update({
  userId: "user_123",
}).set({
  name: "New Name",
}).go({
  conditions: {
    attr: "role",
    eq: "ADMIN", // Only update if role is ADMIN
  },
});
```

### Delete

```typescript
// Delete item
await UserEntity.delete({
  userId: "user_123",
}).go();

// Conditional delete
await UserEntity.delete({
  userId: "user_123",
}).go({
  conditions: { role: "STUDENT" }, // Only delete if student
});

// Return deleted item
const deleted = await UserEntity.delete({
  userId: "user_123",
}).go({
  response: "all_old", // Return the deleted item
});
```

## Queries

### Basic Queries

```typescript
// Query by primary key
const users = await UserEntity.query
  .primary({
    userId: "user_123",
  })
  .go();

// users.data is an array of items

// Query with begins_with
const sessions = await SessionEntity.query
  .byCourse({
    courseId: "course_123",
  })
  .begins({
    scheduledDate: "2025-01", // All sessions in January 2025
  })
  .go();

// Query with between
const sessions = await SessionEntity.query
  .byCourse({
    courseId: "course_123",
  })
  .between(
    { scheduledDate: "2025-01-01" },
    { scheduledDate: "2025-01-31" }
  )
  .go();

// Query with gt/gte/lt/lte
const sessions = await SessionEntity.query
  .byCourse({
    courseId: "course_123",
  })
  .gt({ scheduledDate: "2025-01-01" }) // Greater than
  .go();
```

### Query Options

```typescript
// Limit results
const users = await UserEntity.query
  .byRole({
    role: "STUDENT",
  })
  .go({
    limit: 10, // Only return 10 items
  });

// Pagination
const firstPage = await UserEntity.query
  .byRole({
    role: "STUDENT",
  })
  .go({
    limit: 10,
  });

// Get next page using cursor
if (firstPage.cursor) {
  const secondPage = await UserEntity.query
    .byRole({
      role: "STUDENT",
    })
    .go({
      limit: 10,
      cursor: firstPage.cursor,
    });
}

// Scan index forward/backward
const latest = await SessionEntity.query
  .byCourse({
    courseId: "course_123",
  })
  .go({
    order: "desc", // Most recent first (ScanIndexForward: false)
  });

// Filter after query
const activeSessions = await SessionEntity.query
  .byCourse({
    courseId: "course_123",
  })
  .where(
    ({ status }, { eq }) => eq(status, "IN_PROGRESS")
  )
  .go();

// Select specific attributes
const users = await UserEntity.query
  .byRole({
    role: "STUDENT",
  })
  .go({
    attributes: ["userId", "name", "email"],
  });
```

### Complex Filters

```typescript
// Multiple conditions (AND)
const sessions = await SessionEntity.query
  .byCourse({
    courseId: "course_123",
  })
  .where(
    ({ status, durationMinutes }, { eq, gte }) => `
      ${eq(status, "COMPLETED")} AND ${gte(durationMinutes, 60)}
    `
  )
  .go();

// OR conditions
const sessions = await SessionEntity.query
  .byCourse({
    courseId: "course_123",
  })
  .where(
    ({ status }, { eq }) => `
      ${eq(status, "SCHEDULED")} OR ${eq(status, "IN_PROGRESS")}
    `
  )
  .go();

// NOT condition
const users = await UserEntity.query
  .byRole({
    role: "STUDENT",
  })
  .where(
    ({ verified }, { eq }) => `NOT ${eq(verified, true)}`
  )
  .go();

// Contains (for strings)
const users = await UserEntity.scan
  .where(
    ({ email }, { contains }) => contains(email, "@gmail.com")
  )
  .go();

// Between (in filter)
const sessions = await SessionEntity.query
  .byCourse({
    courseId: "course_123",
  })
  .where(
    ({ durationMinutes }, { between }) => 
      between(durationMinutes, 30, 120)
  )
  .go();
```

## Scan Operations

```typescript
// Scan entire table (use sparingly!)
const allUsers = await UserEntity.scan.go();

// Scan with filter
const verifiedUsers = await UserEntity.scan
  .where(
    ({ verified }, { eq }) => eq(verified, true)
  )
  .go();

// Scan with pagination
const firstPage = await UserEntity.scan.go({
  limit: 100,
});

if (firstPage.cursor) {
  const secondPage = await UserEntity.scan.go({
    cursor: firstPage.cursor,
  });
}

// Parallel scan for large tables
const segment1 = await UserEntity.scan.go({
  segments: { total: 4, segment: 0 },
});
const segment2 = await UserEntity.scan.go({
  segments: { total: 4, segment: 1 },
});
// ... segments 2 and 3
```

## Batch Operations

### Batch Get

```typescript
// Batch get multiple items
const results = await UserEntity.get([
  { userId: "user_1" },
  { userId: "user_2" },
  { userId: "user_3" },
]).go();

// results.data is an array of items (nulls for not found)

// Batch get with options
const results = await UserEntity.get([
  { userId: "user_1" },
  { userId: "user_2" },
]).go({
  unprocessed: "raw", // Return unprocessed keys
  consistent: true,
});
```

### Batch Write

```typescript
// Batch put
await UserEntity.put([
  {
    userId: "user_1",
    email: "user1@example.com",
    name: "User 1",
    role: "STUDENT",
  },
  {
    userId: "user_2",
    email: "user2@example.com",
    name: "User 2",
    role: "STUDENT",
  },
]).go();

// Batch delete
await UserEntity.delete([
  { userId: "user_1" },
  { userId: "user_2" },
]).go();

// Note: Batch operations support up to 25 items
// For more, chunk them:
const chunks = chunk(items, 25);
for (const chunk of chunks) {
  await UserEntity.put(chunk).go();
}
```

## Transactions

```typescript
import { Entity, Service } from "electrodb";

// Define entities first
const service = new Service({
  user: UserEntity,
  session: SessionEntity,
});

// Transactional write
await service
  .transaction
  .write(({ user, session }) => [
    user.create({
      userId: "user_123",
      email: "john@example.com",
      name: "John Doe",
      role: "STUDENT",
    }),
    session.create({
      sessionId: "session_456",
      userId: "user_123",
      courseId: "course_789",
      scheduledDate: "2025-01-15",
      durationMinutes: 60,
      status: "SCHEDULED",
    }),
  ])
  .go();

// Conditional transaction
await service
  .transaction
  .write(({ user, session }) => [
    user.update({ userId: "user_123" })
      .set({ verified: true })
      .commit({ conditions: { verified: false } }),
    session.create({
      sessionId: "session_456",
      userId: "user_123",
      courseId: "course_789",
      scheduledDate: "2025-01-15",
      durationMinutes: 60,
    }).commit({ conditions: { exists: false } }),
  ])
  .go();

// Transactional get (requires primary keys)
const results = await service
  .transaction
  .get([
    { user: { userId: "user_123" } },
    { session: { sessionId: "session_456" } },
  ])
  .go();
```

## Collections

Collections allow querying multiple entity types together:

```typescript
export const UserEntity = new Entity({
  model: {
    entity: "user",
    version: "1",
    service: "myapp",
  },
  attributes: {
    userId: { type: "string", required: true },
    email: { type: "string", required: true },
    name: { type: "string", required: true },
  },
  indexes: {
    primary: {
      pk: { field: "pk", composite: ["userId"] },
      sk: { field: "sk", composite: [] },
    },
    byOrg: {
      index: "gsi1",
      pk: { field: "gsi1pk", composite: ["orgId"] },
      sk: { field: "gsi1sk", composite: ["userId"] },
      collection: "organization", // Collection name
    },
  },
});

export const CourseEntity = new Entity({
  model: {
    entity: "course",
    version: "1",
    service: "myapp",
  },
  attributes: {
    courseId: { type: "string", required: true },
    orgId: { type: "string", required: true },
    title: { type: "string", required: true },
  },
  indexes: {
    primary: {
      pk: { field: "pk", composite: ["courseId"] },
      sk: { field: "sk", composite: [] },
    },
    byOrg: {
      index: "gsi1",
      pk: { field: "gsi1pk", composite: ["orgId"] },
      sk: { field: "gsi1sk", composite: ["courseId"] },
      collection: "organization", // Same collection
    },
  },
});

// Create service
const service = new Service({
  user: UserEntity,
  course: CourseEntity,
});

// Query collection (gets both users and courses for an org)
const orgData = await service.collections
  .organization({ orgId: "org_123" })
  .go();

// orgData.data contains { user: [...], course: [...] }
```

## Service Patterns

```typescript
// Create a service with multiple entities
const AppService = new Service(
  {
    user: UserEntity,
    session: SessionEntity,
    course: CourseEntity,
    enrollment: EnrollmentEntity,
  },
  { client: dynamoDBClient, table: "MyAppTable" }
);

// Use service for transactions
await AppService.transaction.write(({ user, enrollment }) => [
  user.update({ userId: "user_123" }).set({ verified: true }),
  enrollment.create({
    enrollmentId: "enroll_456",
    userId: "user_123",
    courseId: "course_789",
    enrolledAt: new Date().toISOString(),
  }),
]).go();

// Collections query
const userData = await AppService.collections
  .userCourses({ userId: "user_123" })
  .go();
```

## Advanced Patterns

### Optimistic Locking

```typescript
// Add version attribute
export const UserEntity = new Entity({
  model: { entity: "user", version: "1", service: "myapp" },
  attributes: {
    userId: { type: "string", required: true },
    name: { type: "string", required: true },
    version: {
      type: "number",
      required: true,
      default: 0,
      watch: "*", // Increment on any change
      set: (_, item) => (item.version ?? 0) + 1,
    },
  },
  indexes: {
    primary: {
      pk: { field: "pk", composite: ["userId"] },
      sk: { field: "sk", composite: [] },
    },
  },
});

// Update with version check
const user = await UserEntity.get({ userId: "user_123" }).go();

await UserEntity.update({ userId: "user_123" })
  .set({ name: "New Name" })
  .go({
    conditions: { version: user.data!.version }, // Only update if version matches
  });
```

### Soft Delete

```typescript
export const UserEntity = new Entity({
  model: { entity: "user", version: "1", service: "myapp" },
  attributes: {
    userId: { type: "string", required: true },
    name: { type: "string", required: true },
    deletedAt: { type: "string" }, // ISO timestamp or null
  },
  indexes: {
    primary: {
      pk: { field: "pk", composite: ["userId"] },
      sk: { field: "sk", composite: [] },
    },
    active: {
      index: "gsi1",
      pk: { field: "gsi1pk", composite: ["deletedAt"] },
      sk: { field: "gsi1sk", composite: ["userId"] },
    },
  },
});

// Soft delete
await UserEntity.update({ userId: "user_123" })
  .set({ deletedAt: new Date().toISOString() })
  .go();

// Query only active users (where deletedAt is not set)
// Use sparse index - items without gsi1pk won't appear
const activeUsers = await UserEntity.query
  .active({ deletedAt: "__ACTIVE__" }) // Special marker
  .go();
```

### Sparse Indexes

```typescript
// Only index published posts
export const PostEntity = new Entity({
  model: { entity: "post", version: "1", service: "myapp" },
  attributes: {
    postId: { type: "string", required: true },
    title: { type: "string", required: true },
    published: { type: "boolean", default: false },
    publishedAt: { type: "string" }, // Only set when published
  },
  indexes: {
    primary: {
      pk: { field: "pk", composite: ["postId"] },
      sk: { field: "sk", composite: [] },
    },
    published: {
      index: "gsi1",
      pk: {
        field: "gsi1pk",
        composite: [], // No composite, just a constant
        template: "PUBLISHED#POST", // All published posts
      },
      sk: {
        field: "gsi1sk",
        composite: ["publishedAt"],
      },
    },
  },
});

// Only items with gsi1pk set will appear in the index
await PostEntity.create({
  postId: "post_123",
  title: "My Post",
  published: true,
  publishedAt: new Date().toISOString(),
}).go();

// Query only published posts
const publishedPosts = await PostEntity.query
  .published({})
  .go();
```

### Time-to-Live (TTL)

```typescript
export const SessionTokenEntity = new Entity({
  model: { entity: "sessionToken", version: "1", service: "myapp" },
  attributes: {
    token: { type: "string", required: true },
    userId: { type: "string", required: true },
    expiresAt: {
      type: "number", // Unix timestamp in seconds
      required: true,
      default: () => Math.floor(Date.now() / 1000) + 86400, // 24 hours
    },
  },
  indexes: {
    primary: {
      pk: { field: "pk", composite: ["token"] },
      sk: { field: "sk", composite: [] },
    },
  },
});

// Configure TTL on the table (do this once)
// Table attribute: expiresAt
// DynamoDB will automatically delete expired items
```

## Type Helpers

```typescript
// Extract types from entity
type User = typeof UserEntity.model.schema;
type UserItem = ReturnType<typeof UserEntity.parse>;
type UserKeys = Parameters<typeof UserEntity.get>[0];

// Infer return types
type QueryResult = Awaited<ReturnType<typeof UserEntity.query.byRole>>;
type CreateResult = Awaited<ReturnType<typeof UserEntity.create>>;

// Custom typed helpers
export async function getUser(userId: string): Promise<UserItem | null> {
  const result = await UserEntity.get({ userId }).go();
  return result.data;
}

export async function requireUser(userId: string): Promise<UserItem> {
  const user = await getUser(userId);
  if (!user) {
    throw new Error("User not found");
  }
  return user;
}
```

## Error Handling

```typescript
import { ElectroError } from "electrodb";

try {
  await UserEntity.create({
    userId: "user_123",
    email: "john@example.com",
    name: "John Doe",
    role: "STUDENT",
  }).go();
} catch (error) {
  if (error instanceof ElectroError) {
    // ElectroDB-specific error
    console.error("ElectroDB error:", error.message);
    
    // Check error codes
    if (error.code === 4001) {
      // Validation error
    } else if (error.code === 5003) {
      // Item already exists (conditional check failed)
    }
  } else {
    // DynamoDB SDK error
    console.error("DynamoDB error:", error);
  }
}

// Common error codes:
// 4001: Invalid/missing required attribute
// 4002: Invalid attribute value
// 5001: DynamoDB operation failed
// 5003: Conditional check failed
```

## Best Practices

### 1. Use Type Exports

```typescript
// Export types for reuse
export type User = typeof UserEntity.model.schema;
export type UserItem = ReturnType<typeof UserEntity.parse>;
```

### 2. Validate Complex Data

```typescript
attributes: {
  email: {
    type: "string",
    required: true,
    validate: (email) => {
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        throw new Error("Invalid email format");
      }
    },
  },
}
```

### 3. Use Readonly for Timestamps

```typescript
createdAt: {
  type: "string",
  required: true,
  default: () => new Date().toISOString(),
  readOnly: true, // Cannot be updated
}
```

### 4. Watch for Auto-Updates

```typescript
updatedAt: {
  type: "string",
  required: true,
  default: () => new Date().toISOString(),
  set: () => new Date().toISOString(),
  watch: "*", // Update on any attribute change
}
```

### 5. Use Hidden Attributes for Computed Values

```typescript
fullName: {
  type: "string",
  hidden: true, // Not stored in DB
  get: (_, item) => `${item.firstName} ${item.lastName}`,
}
```

### 6. Design Access Patterns First

Before creating entities, list your access patterns:
1. Get user by ID
2. Get user by email
3. List users by role
4. List sessions by course
5. List sessions by user

Then design indexes to support these patterns.

### 7. Use Collections for Related Entities

Group related entities under the same partition key for efficient queries.

### 8. Check .data Before Using

```typescript
const result = await UserEntity.get({ userId }).go();
if (!result.data) {
  throw new Error("Not found");
}
const user = result.data; // Now TypeScript knows it's not null
```

### 9. Use Services for Related Operations

```typescript
const service = new Service({
  user: UserEntity,
  session: SessionEntity,
});

// Better for transactions and collections
```

### 10. Leverage Composite Attributes

```typescript
sk: {
  field: "sk",
  composite: ["courseId", "userId"], // Creates: COURSE#123#USER#456
}
```

## Common Gotchas

1. **Batch size limit**: Max 25 items per batch operation
2. **Transaction limit**: Max 100 items per transaction (across all tables)
3. **Cursor is opaque**: Don't parse or modify cursors
4. **Consistent reads**: Cost more, use sparingly
5. **Scan is expensive**: Avoid scanning large tables
6. **Index projections**: Consider what attributes you need in GSIs
7. **Type inference**: Let TypeScript infer types from entity definitions
8. **Hidden attributes**: Not stored in DB, computed on read
9. **ReadOnly attributes**: Can't be updated after creation
10. **Watch attribute**: Triggers on specified attribute changes

## Testing

```typescript
import { describe, test, expect, beforeAll } from "vitest";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { UserEntity } from "./user.entity";

// Use local DynamoDB for tests
const localClient = new DynamoDBClient({
  endpoint: "http://localhost:8000",
});

describe("UserEntity", () => {
  beforeAll(async () => {
    // Create test table
    await createTestTable();
  });

  test("creates user", async () => {
    const result = await UserEntity.create({
      userId: "user_123",
      email: "test@example.com",
      name: "Test User",
      role: "STUDENT",
    }).go();

    expect(result.data).toMatchObject({
      userId: "user_123",
      email: "test@example.com",
      name: "Test User",
    });
  });

  test("queries users by role", async () => {
    const result = await UserEntity.query
      .byRole({ role: "STUDENT" })
      .go();

    expect(result.data.length).toBeGreaterThan(0);
  });
});
```

## Resources

- [ElectroDB Documentation](https://electrodb.dev)
- [ElectroDB GitHub](https://github.com/tywalch/electrodb)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
