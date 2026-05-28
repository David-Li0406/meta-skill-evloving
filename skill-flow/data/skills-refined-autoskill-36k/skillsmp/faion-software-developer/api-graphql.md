---
id: api-graphql
name: "GraphQL Patterns"
domain: API
skill: faion-software-developer
category: "api-design"
---

## GraphQL Patterns

### Problem

REST can lead to over-fetching/under-fetching. Complex UIs need flexible data queries.

### Framework

**Schema Definition:**

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  orders: [Order!]!
  createdAt: DateTime!
}

type Order {
  id: ID!
  total: Float!
  status: OrderStatus!
  items: [OrderItem!]!
}

enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}

type Query {
  user(id: ID!): User
  users(first: Int, after: String): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

type Subscription {
  orderStatusChanged(userId: ID!): Order!
}

input CreateUserInput {
  name: String!
  email: String!
}
```

**Query Example:**

```graphql
query GetUserWithOrders($id: ID!) {
  user(id: $id) {
    id
    name
    email
    orders(first: 5) {
      id
      total
      status
      items {
        name
        quantity
      }
    }
  }
}
```

**Mutation Example:**

```graphql
mutation CreateNewUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
  }
}
```

### N+1 Prevention

**Problem:** Fetching related data causes multiple DB queries.

**Solution - DataLoader:**

```typescript
import DataLoader from 'dataloader';

const userLoader = new DataLoader(async (userIds) => {
  const users = await db.users.findMany({ where: { id: { in: userIds } } });
  return userIds.map(id => users.find(u => u.id === id));
});

// In resolver
resolve: (order) => userLoader.load(order.userId)
```

### Pagination (Relay-style)

```graphql
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  cursor: String!
  node: User!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

### Error Handling

```json
{
  "data": null,
  "errors": [
    {
      "message": "User not found",
      "path": ["user"],
      "extensions": {
        "code": "NOT_FOUND",
        "id": "123"
      }
    }
  ]
}
```

### Federation (Microservices)

```graphql
# Users service
type User @key(fields: "id") {
  id: ID!
  name: String!
  email: String!
}

# Orders service
extend type User @key(fields: "id") {
  id: ID! @external
  orders: [Order!]!
}
```

### Best Practices

- Use input types for mutations
- Implement cursor-based pagination
- Use DataLoader for N+1 prevention
- Add depth limiting to prevent DoS
- Implement query complexity analysis
- Use persisted queries in production
- Add field-level authorization

### Agent

faion-api-agent
