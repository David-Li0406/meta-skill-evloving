---
name: dynamodb-single-table
description: Single table design patterns for DynamoDB with SST - modeling complex data relationships in a single table for optimal performance and cost
---

# DynamoDB Single Table Design

This skill covers single table design patterns for DynamoDB, the AWS-recommended approach for modeling complex relationships in a single table.

## Core Philosophy

Single table design principles:
- **One table to rule them all**: Model all entities in a single table
- **Overload keys**: Use generic pk/sk for flexibility
- **Optimize for access patterns**: Design around how you query data
- **Denormalize when needed**: Duplicate data to avoid joins
- **Use GSIs strategically**: Add secondary indexes for alternate access patterns

## Why Single Table Design?

**Benefits:**
- ✅ Consistent performance across all queries
- ✅ Lower costs (fewer tables to provision)
- ✅ Atomic transactions across entity types
- ✅ Simpler infrastructure management
- ✅ Better suited for serverless architectures

**Trade-offs:**
- ❌ More complex to design initially
- ❌ Requires understanding access patterns upfront
- ❌ Less intuitive than relational databases

## Key Concepts

### Generic Key Names

Use generic partition (pk) and sort (sk) keys instead of entity-specific names:

```typescript
// ✅ Good - Generic and flexible
{
  pk: "USER#123",
  sk: "PROFILE",
  // ... entity data
}

// ❌ Bad - Entity-specific
{
  userId: "123",
  // ... entity data
}
```

### Composite Keys

Build keys from multiple attributes:

```typescript
// User entity
pk: "USER#userId"
sk: "PROFILE"

// User's posts
pk: "USER#userId"
sk: "POST#postId"

// Post details
pk: "POST#postId"
sk: "METADATA"

// Post comments
pk: "POST#postId"
sk: "COMMENT#commentId"
```

### Item Collections

Group related items under the same partition key:

```typescript
// All items with pk="USER#123" form an "item collection"
// Can retrieve in a single query

// User profile
{ pk: "USER#123", sk: "PROFILE", name: "John", email: "..." }

// User's posts
{ pk: "USER#123", sk: "POST#post1", title: "...", content: "..." }
{ pk: "USER#123", sk: "POST#post2", title: "...", content: "..." }

// User's subscriptions
{ pk: "USER#123", sk: "SUB#sub1", plan: "pro", ... }
```

## Access Pattern Design

### Pattern 1: Get Single Item

```typescript
// Get user profile
{
  pk: "USER#123",
  sk: "PROFILE"
}

// DynamoDB operation
await client.send(new GetCommand({
  TableName: Resource.Database.name,
  Key: {
    pk: "USER#123",
    sk: "PROFILE"
  }
}));
```

### Pattern 2: Query Item Collection

```typescript
// Get all posts by user
await client.send(new QueryCommand({
  TableName: Resource.Database.name,
  KeyConditionExpression: "pk = :pk AND begins_with(sk, :sk)",
  ExpressionAttributeValues: {
    ":pk": "USER#123",
    ":sk": "POST#"
  }
}));
```

### Pattern 3: Query with Sort

```typescript
// Get user's recent posts (sorted by timestamp)
{
  pk: "USER#123",
  sk: "POST#2025-01-02T10:30:00Z#post1"  // ISO timestamp for sorting
}

await client.send(new QueryCommand({
  TableName: Resource.Database.name,
  KeyConditionExpression: "pk = :pk AND begins_with(sk, :sk)",
  ExpressionAttributeValues: {
    ":pk": "USER#123",
    ":sk": "POST#"
  },
  ScanIndexForward: false  // Descending order
}));
```

### Pattern 4: Global Secondary Index (GSI)

```typescript
// GSI for querying posts by status across all users
// GSI: gsi1pk = "POST#STATUS#published", gsi1sk = timestamp

// In SST config
const table = new sst.aws.Dynamo("Database", {
  fields: {
    pk: "string",
    sk: "string",
    gsi1pk: "string",
    gsi1sk: "string"
  },
  primaryIndex: { hashKey: "pk", rangeKey: "sk" },
  globalIndexes: {
    gsi1: { hashKey: "gsi1pk", rangeKey: "gsi1sk" }
  }
});

// Query all published posts
await client.send(new QueryCommand({
  TableName: Resource.Database.name,
  IndexName: "gsi1",
  KeyConditionExpression: "gsi1pk = :pk",
  ExpressionAttributeValues: {
    ":pk": "POST#STATUS#published"
  }
}));
```

## Common Patterns

### Pattern: User with Posts and Comments

```typescript
// User profile
{
  pk: "USER#userId",
  sk: "PROFILE",
  name: "John",
  email: "john@example.com",
  createdAt: "2025-01-01T00:00:00Z"
}

// User's post
{
  pk: "USER#userId",
  sk: "POST#postId",
  title: "My Post",
  content: "...",
  createdAt: "2025-01-02T00:00:00Z"
}

// Post metadata (for reverse lookup)
{
  pk: "POST#postId",
  sk: "METADATA",
  userId: "userId",
  title: "My Post",
  content: "...",
  commentCount: 5
}

// Post comments
{
  pk: "POST#postId",
  sk: "COMMENT#2025-01-02T10:00:00Z#commentId",
  userId: "commenterId",
  text: "Great post!",
  createdAt: "2025-01-02T10:00:00Z"
}

// Commenter profile (denormalized for display)
{
  pk: "POST#postId",
  sk: "COMMENT#2025-01-02T10:00:00Z#commentId",
  userId: "commenterId",
  userName: "Jane",  // Denormalized!
  userAvatar: "https://...",  // Denormalized!
  text: "Great post!"
}
```

**Access Patterns:**
1. Get user profile: `GetItem(pk="USER#userId", sk="PROFILE")`
2. Get user's posts: `Query(pk="USER#userId", sk begins_with "POST#")`
3. Get post with comments: `Query(pk="POST#postId")`
4. Get recent comments: Sort by timestamp in sk

### Pattern: Many-to-Many (Users and Groups)

```typescript
// User membership in group
{
  pk: "USER#userId",
  sk: "GROUP#groupId",
  groupName: "Developers",  // Denormalized
  role: "admin",
  joinedAt: "2025-01-01"
}

// Group membership list
{
  pk: "GROUP#groupId",
  sk: "USER#userId",
  userName: "John",  // Denormalized
  role: "admin",
  joinedAt: "2025-01-01"
}

// Group metadata
{
  pk: "GROUP#groupId",
  sk: "METADATA",
  name: "Developers",
  description: "...",
  memberCount: 42
}
```

**Access Patterns:**
1. Get user's groups: `Query(pk="USER#userId", sk begins_with "GROUP#")`
2. Get group's members: `Query(pk="GROUP#groupId", sk begins_with "USER#")`
3. Check membership: `GetItem(pk="USER#userId", sk="GROUP#groupId")`

### Pattern: Hierarchical Data (Folders and Files)

```typescript
// Folder
{
  pk: "FOLDER#folderId",
  sk: "METADATA",
  name: "Documents",
  parentId: "parentFolderId",
  path: "/Documents"
}

// Files in folder
{
  pk: "FOLDER#folderId",
  sk: "FILE#2025-01-02#fileId",  // Sorted by date
  name: "report.pdf",
  size: 1024000,
  uploadedAt: "2025-01-02T10:00:00Z"
}

// File metadata (for direct access)
{
  pk: "FILE#fileId",
  sk: "METADATA",
  name: "report.pdf",
  folderId: "folderId",
  size: 1024000
}
```

### Pattern: Time Series Data

```typescript
// Metrics by date
{
  pk: "METRICS#resourceId",
  sk: "2025-01-02T10:00:00Z",
  cpu: 45.2,
  memory: 67.8,
  requests: 1234
}

// Query metrics for a time range
await client.send(new QueryCommand({
  TableName: Resource.Database.name,
  KeyConditionExpression: "pk = :pk AND sk BETWEEN :start AND :end",
  ExpressionAttributeValues: {
    ":pk": "METRICS#resourceId",
    ":start": "2025-01-01T00:00:00Z",
    ":end": "2025-01-02T00:00:00Z"
  }
}));
```

## Implementation with SST

### Basic Setup

```typescript
// sst.config.ts
const table = new sst.aws.Dynamo("Database", {
  fields: {
    pk: "string",
    sk: "string",
    gsi1pk: "string",
    gsi1sk: "string",
    gsi2pk: "string",
    gsi2sk: "string"
  },
  primaryIndex: { hashKey: "pk", rangeKey: "sk" },
  globalIndexes: {
    gsi1: { hashKey: "gsi1pk", rangeKey: "gsi1sk" },
    gsi2: { hashKey: "gsi2pk", rangeKey: "gsi2sk" }
  },
  stream: "new-and-old-images"  // For event-driven updates
});
```

### Type-Safe Helpers

```typescript
// src/lib/db.ts
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb";
import { Resource } from "sst";

export const dynamodb = DynamoDBDocumentClient.from(new DynamoDBClient({}), {
  marshallOptions: {
    removeUndefinedValues: true
  }
});

export const TableName = Resource.Database.name;

// Key builders
export const keys = {
  user: (userId: string) => ({
    profile: { pk: `USER#${userId}`, sk: "PROFILE" },
    post: (postId: string) => ({ pk: `USER#${userId}`, sk: `POST#${postId}` })
  }),
  post: (postId: string) => ({
    metadata: { pk: `POST#${postId}`, sk: "METADATA" },
    comment: (commentId: string, timestamp: string) => ({
      pk: `POST#${postId}`,
      sk: `COMMENT#${timestamp}#${commentId}`
    })
  })
};
```

### CRUD Operations

```typescript
import { GetCommand, PutCommand, UpdateCommand, DeleteCommand, QueryCommand } from "@aws-sdk/lib-dynamodb";
import { dynamodb, TableName, keys } from "./db";

// Create user
export async function createUser(userId: string, data: UserData) {
  await dynamodb.send(new PutCommand({
    TableName,
    Item: {
      ...keys.user(userId).profile,
      ...data,
      createdAt: new Date().toISOString()
    }
  }));
}

// Get user
export async function getUser(userId: string) {
  const result = await dynamodb.send(new GetCommand({
    TableName,
    Key: keys.user(userId).profile
  }));
  return result.Item as User | undefined;
}

// Update user
export async function updateUser(userId: string, updates: Partial<UserData>) {
  await dynamodb.send(new UpdateCommand({
    TableName,
    Key: keys.user(userId).profile,
    UpdateExpression: "SET #name = :name, #email = :email",
    ExpressionAttributeNames: {
      "#name": "name",
      "#email": "email"
    },
    ExpressionAttributeValues: {
      ":name": updates.name,
      ":email": updates.email
    }
  }));
}

// Get user's posts
export async function getUserPosts(userId: string) {
  const result = await dynamodb.send(new QueryCommand({
    TableName,
    KeyConditionExpression: "pk = :pk AND begins_with(sk, :sk)",
    ExpressionAttributeValues: {
      ":pk": `USER#${userId}`,
      ":sk": "POST#"
    }
  }));
  return result.Items as Post[];
}
```

## Best Practices

### 1. Design for Access Patterns First

❌ **Don't design entities first:**
```
Users table, Posts table, Comments table...
```

✅ **Do design access patterns first:**
```
1. Get user profile
2. Get user's posts
3. Get post with comments
4. Get all published posts
// Then design keys to support these
```

### 2. Use Sparse Indexes

Only items with GSI keys appear in the index:

```typescript
// Only published posts have gsi1pk
{
  pk: "POST#123",
  sk: "METADATA",
  status: "published",
  gsi1pk: "POST#STATUS#published",  // Only published posts have this
  gsi1sk: "2025-01-02T10:00:00Z"
}
```

### 3. Denormalize Strategically

Duplicate data to avoid secondary queries:

```typescript
// Comment with user info denormalized
{
  pk: "POST#postId",
  sk: "COMMENT#commentId",
  userId: "userId",
  userName: "John",  // From users table
  userAvatar: "...",  // From users table
  text: "Great post!"
}
```

### 4. Use Transactions for Related Items

```typescript
import { TransactWriteCommand } from "@aws-sdk/lib-dynamodb";

await dynamodb.send(new TransactWriteCommand({
  TransactItems: [
    {
      Put: {
        TableName,
        Item: { pk: "POST#123", sk: "METADATA", ... }
      }
    },
    {
      Update: {
        TableName,
        Key: { pk: "USER#userId", sk: "PROFILE" },
        UpdateExpression: "SET postCount = postCount + :inc",
        ExpressionAttributeValues: { ":inc": 1 }
      }
    }
  ]
}));
```

### 5. Handle Hot Partitions

Distribute writes using suffixes:

```typescript
// Instead of: pk: "METRICS"
// Use: pk: "METRICS#0", "METRICS#1", ..., "METRICS#9"
const suffix = Math.floor(Math.random() * 10);
const pk = `METRICS#${suffix}`;
```

## Common Gotchas

### 1. Sort Key is Required for Queries

```typescript
// ❌ This won't work
Query(pk = "USER#123")

// ✅ Use begins_with
Query(pk = "USER#123" AND sk begins_with "POST#")
```

### 2. GSI Consistency is Eventually Consistent

```typescript
// After writing to main table
await putItem({ pk: "USER#123", gsi1pk: "ACTIVE" });

// GSI query might not see it immediately
const result = await query({ IndexName: "gsi1", gsi1pk: "ACTIVE" });
// May not include the item yet!
```

### 3. Item Size Limit is 400KB

```typescript
// Don't store large data in items
❌ { pk: "POST#123", content: "<10MB of text>" }

// Store large data in S3
✅ { pk: "POST#123", contentUrl: "s3://bucket/key" }
```

### 4. Projection of GSI Matters

```typescript
// GSI with ALL projection (expensive)
globalIndexes: {
  gsi1: {
    hashKey: "gsi1pk",
    projection: "all"  // Copies all attributes
  }
}

// GSI with KEYS_ONLY (cheaper)
globalIndexes: {
  gsi1: {
    hashKey: "gsi1pk",
    projection: "keys_only"  // Only pk, sk, gsi keys
  }
}
```

## Testing Single Table Design

```typescript
// Use local DynamoDB for tests
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({
  endpoint: "http://localhost:8000"
});

describe("User operations", () => {
  test("creates user and retrieves profile", async () => {
    await createUser("123", { name: "John", email: "john@example.com" });
    const user = await getUser("123");
    expect(user?.name).toBe("John");
  });
  
  test("queries user posts", async () => {
    await createPost("123", "post1", { title: "First Post" });
    await createPost("123", "post2", { title: "Second Post" });
    
    const posts = await getUserPosts("123");
    expect(posts).toHaveLength(2);
  });
});
```

## Migration Strategy

If migrating from multiple tables:

1. **Identify access patterns** in existing code
2. **Design new key structure** to support patterns
3. **Create migration scripts** to transform data
4. **Run in parallel** (dual writes during transition)
5. **Verify data integrity** before cutover
6. **Switch to single table** atomically

## Further Reading

- AWS DynamoDB Best Practices: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html
- Alex DeBrie's "DynamoDB Book": https://www.dynamodbbook.com/
- Rick Houlihan's re:Invent talks on YouTube
- SST DynamoDB docs: https://sst.dev/docs/component/aws/dynamo
