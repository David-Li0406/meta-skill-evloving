---
name: web-graphql
description: GraphQL patterns for Apollo Server + Express + Prisma stack
user-invocable: false
---

# Web GraphQL Skill

**Version:** 1.0
**Stack:** GraphQL + Apollo Server + Express + Prisma

> Schema design, resolver patterns, and Prisma integration for type-safe GraphQL APIs.

---

## Core Principles

1. **Schema-First Thinking** — Design the schema for client needs, not database shape.
2. **Thin Resolvers** — Resolvers orchestrate; business logic lives in services.
3. **Type Safety End-to-End** — Prisma types flow through to GraphQL.
4. **N+1 Prevention** — Use DataLoader for batching.
5. **Explicit Errors** — Structured error responses, not vague messages.

---

## Schema Design

### Schema Organization

```
src/
├── graphql/
│   ├── schema/
│   │   ├── index.ts        # Combines all type defs
│   │   ├── user.graphql    # User types and operations
│   │   ├── product.graphql # Product types and operations
│   │   └── order.graphql   # Order types and operations
│   ├── resolvers/
│   │   ├── index.ts        # Combines all resolvers
│   │   ├── user.ts
│   │   ├── product.ts
│   │   └── order.ts
│   └── context.ts          # Context type and creation
├── services/               # Business logic
│   ├── user.service.ts
│   └── product.service.ts
└── dataloaders/            # DataLoader definitions
    └── index.ts
```

### Type Definitions

```graphql
# ✅ Good - Client-focused types
type Product {
  id: ID!
  name: String!
  description: String
  price: Money!
  images: [Image!]!
  category: Category!
  inStock: Boolean!

  # Computed field - not in database
  formattedPrice: String!
}

type Money {
  amount: Int!       # Cents to avoid float issues
  currency: String!
  formatted: String! # "$19.99"
}

# Input types for mutations
input CreateProductInput {
  name: String!
  description: String
  priceInCents: Int!
  categoryId: ID!
}

input UpdateProductInput {
  name: String
  description: String
  priceInCents: Int
}
```

### Query Design

```graphql
type Query {
  # Single item by ID
  product(id: ID!): Product
  user(id: ID!): User

  # Lists with pagination and filtering
  products(
    first: Int
    after: String
    filter: ProductFilter
    orderBy: ProductOrderBy
  ): ProductConnection!

  # Current user (from auth context)
  me: User
}

# Cursor-based pagination
type ProductConnection {
  edges: [ProductEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type ProductEdge {
  node: Product!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Filtering
input ProductFilter {
  categoryId: ID
  minPrice: Int
  maxPrice: Int
  inStock: Boolean
  search: String
}

enum ProductOrderBy {
  NAME_ASC
  NAME_DESC
  PRICE_ASC
  PRICE_DESC
  CREATED_AT_DESC
}
```

### Mutation Design

```graphql
type Mutation {
  # Returns the created/updated entity
  createProduct(input: CreateProductInput!): CreateProductPayload!
  updateProduct(id: ID!, input: UpdateProductInput!): UpdateProductPayload!
  deleteProduct(id: ID!): DeleteProductPayload!

  # Action-based naming for non-CRUD
  addToCart(productId: ID!, quantity: Int!): AddToCartPayload!
  checkout(input: CheckoutInput!): CheckoutPayload!
}

# Payload pattern - allows for errors and metadata
type CreateProductPayload {
  product: Product
  errors: [UserError!]!
}

type UserError {
  field: String
  message: String!
  code: ErrorCode!
}

enum ErrorCode {
  NOT_FOUND
  VALIDATION_ERROR
  UNAUTHORIZED
  FORBIDDEN
  CONFLICT
}
```

---

## Resolver Patterns

### Thin Resolvers

```typescript
// ✅ Good - Resolver is thin, delegates to service
const resolvers = {
  Query: {
    product: async (_, { id }, { services }) => {
      return services.product.findById(id);
    },

    products: async (_, { first, after, filter, orderBy }, { services }) => {
      return services.product.findMany({ first, after, filter, orderBy });
    },
  },

  Mutation: {
    createProduct: async (_, { input }, { services, user }) => {
      // Auth check in resolver is OK
      if (!user?.isAdmin) {
        return {
          product: null,
          errors: [{ message: 'Unauthorized', code: 'UNAUTHORIZED' }],
        };
      }

      return services.product.create(input);
    },
  },

  Product: {
    // Field resolvers for computed/related data
    formattedPrice: (product) => {
      return `$${(product.price / 100).toFixed(2)}`;
    },

    category: async (product, _, { loaders }) => {
      return loaders.category.load(product.categoryId);
    },
  },
};
```

### Context Setup

```typescript
// graphql/context.ts
import { PrismaClient } from '@prisma/client';
import { createLoaders } from '../dataloaders';
import { createServices } from '../services';

export interface Context {
  prisma: PrismaClient;
  user: User | null;
  loaders: ReturnType<typeof createLoaders>;
  services: ReturnType<typeof createServices>;
}

export async function createContext({ req }): Promise<Context> {
  const prisma = new PrismaClient();
  const user = await getUserFromToken(req.headers.authorization);
  const loaders = createLoaders(prisma);
  const services = createServices(prisma, user);

  return { prisma, user, loaders, services };
}
```

---

## Prisma Integration

### Service Layer

```typescript
// services/product.service.ts
import { PrismaClient, Prisma } from '@prisma/client';

export class ProductService {
  constructor(
    private prisma: PrismaClient,
    private user: User | null
  ) {}

  async findById(id: string) {
    return this.prisma.product.findUnique({
      where: { id },
    });
  }

  async findMany({ first = 20, after, filter, orderBy }) {
    const where = this.buildWhereClause(filter);
    const order = this.buildOrderByClause(orderBy);

    // Cursor-based pagination with Prisma
    const products = await this.prisma.product.findMany({
      where,
      orderBy: order,
      take: first + 1, // Fetch one extra to check hasNextPage
      ...(after && {
        cursor: { id: after },
        skip: 1, // Skip the cursor itself
      }),
    });

    const hasNextPage = products.length > first;
    const edges = products.slice(0, first).map(product => ({
      node: product,
      cursor: product.id,
    }));

    return {
      edges,
      pageInfo: {
        hasNextPage,
        hasPreviousPage: Boolean(after),
        startCursor: edges[0]?.cursor,
        endCursor: edges[edges.length - 1]?.cursor,
      },
      totalCount: await this.prisma.product.count({ where }),
    };
  }

  async create(input: CreateProductInput) {
    try {
      const product = await this.prisma.product.create({
        data: {
          name: input.name,
          description: input.description,
          price: input.priceInCents,
          categoryId: input.categoryId,
        },
      });

      return { product, errors: [] };
    } catch (error) {
      if (error instanceof Prisma.PrismaClientKnownRequestError) {
        if (error.code === 'P2002') {
          return {
            product: null,
            errors: [{
              field: 'name',
              message: 'Product with this name already exists',
              code: 'CONFLICT',
            }],
          };
        }
      }
      throw error;
    }
  }

  private buildWhereClause(filter?: ProductFilter): Prisma.ProductWhereInput {
    if (!filter) return {};

    return {
      ...(filter.categoryId && { categoryId: filter.categoryId }),
      ...(filter.inStock !== undefined && { stock: filter.inStock ? { gt: 0 } : 0 }),
      ...(filter.minPrice && { price: { gte: filter.minPrice } }),
      ...(filter.maxPrice && { price: { lte: filter.maxPrice } }),
      ...(filter.search && {
        OR: [
          { name: { contains: filter.search, mode: 'insensitive' } },
          { description: { contains: filter.search, mode: 'insensitive' } },
        ],
      }),
    };
  }

  private buildOrderByClause(orderBy?: ProductOrderBy): Prisma.ProductOrderByWithRelationInput {
    switch (orderBy) {
      case 'NAME_ASC': return { name: 'asc' };
      case 'NAME_DESC': return { name: 'desc' };
      case 'PRICE_ASC': return { price: 'asc' };
      case 'PRICE_DESC': return { price: 'desc' };
      case 'CREATED_AT_DESC':
      default: return { createdAt: 'desc' };
    }
  }
}
```

---

## DataLoader for N+1 Prevention

### The Problem

```typescript
// ❌ Without DataLoader - N+1 queries
// Query: products { category { name } }
// Executes: 1 query for products + N queries for categories

Product: {
  category: async (product, _, { prisma }) => {
    return prisma.category.findUnique({
      where: { id: product.categoryId },
    });
  },
}
```

### The Solution

```typescript
// dataloaders/index.ts
import DataLoader from 'dataloader';
import { PrismaClient } from '@prisma/client';

export function createLoaders(prisma: PrismaClient) {
  return {
    category: new DataLoader(async (categoryIds: string[]) => {
      const categories = await prisma.category.findMany({
        where: { id: { in: categoryIds } },
      });

      // Map results to match input order
      const categoryMap = new Map(categories.map(c => [c.id, c]));
      return categoryIds.map(id => categoryMap.get(id) ?? null);
    }),

    user: new DataLoader(async (userIds: string[]) => {
      const users = await prisma.user.findMany({
        where: { id: { in: userIds } },
      });

      const userMap = new Map(users.map(u => [u.id, u]));
      return userIds.map(id => userMap.get(id) ?? null);
    }),
  };
}

// In resolver - now batched!
Product: {
  category: async (product, _, { loaders }) => {
    return loaders.category.load(product.categoryId);
  },
}
```

---

## Error Handling

### Structured Errors

```typescript
// ✅ Good - Explicit error handling
async createOrder(input: CreateOrderInput) {
  const errors: UserError[] = [];

  // Validation
  if (input.items.length === 0) {
    errors.push({
      field: 'items',
      message: 'Order must contain at least one item',
      code: 'VALIDATION_ERROR',
    });
  }

  // Check stock
  for (const item of input.items) {
    const product = await this.prisma.product.findUnique({
      where: { id: item.productId },
    });

    if (!product) {
      errors.push({
        field: 'items',
        message: `Product ${item.productId} not found`,
        code: 'NOT_FOUND',
      });
    } else if (product.stock < item.quantity) {
      errors.push({
        field: 'items',
        message: `Insufficient stock for ${product.name}`,
        code: 'VALIDATION_ERROR',
      });
    }
  }

  if (errors.length > 0) {
    return { order: null, errors };
  }

  // Create order...
  const order = await this.prisma.order.create({ ... });
  return { order, errors: [] };
}
```

### Authentication Errors

```typescript
// Use Apollo's built-in errors for auth
import { AuthenticationError, ForbiddenError } from 'apollo-server-express';

const resolvers = {
  Mutation: {
    updateProduct: async (_, { id, input }, { user, services }) => {
      if (!user) {
        throw new AuthenticationError('Must be logged in');
      }

      if (!user.isAdmin) {
        throw new ForbiddenError('Admin access required');
      }

      return services.product.update(id, input);
    },
  },
};
```

---

## Authentication with Cognito

### Token Validation

```typescript
// middleware/auth.ts
import { CognitoJwtVerifier } from 'aws-jwt-verify';

const verifier = CognitoJwtVerifier.create({
  userPoolId: process.env.COGNITO_USER_POOL_ID,
  tokenUse: 'access',
  clientId: process.env.COGNITO_CLIENT_ID,
});

export async function getUserFromToken(authHeader?: string) {
  if (!authHeader?.startsWith('Bearer ')) {
    return null;
  }

  const token = authHeader.slice(7);

  try {
    const payload = await verifier.verify(token);

    // Fetch full user from database
    return prisma.user.findUnique({
      where: { cognitoSub: payload.sub },
    });
  } catch (error) {
    return null;
  }
}
```

---

## File Structure

### GraphQL Type File

```graphql
# graphql/schema/product.graphql

type Product {
  id: ID!
  name: String!
  description: String
  price: Int!
  formattedPrice: String!
  images: [Image!]!
  category: Category!
  inStock: Boolean!
  createdAt: DateTime!
  updatedAt: DateTime!
}

extend type Query {
  product(id: ID!): Product
  products(
    first: Int
    after: String
    filter: ProductFilter
    orderBy: ProductOrderBy
  ): ProductConnection!
}

extend type Mutation {
  createProduct(input: CreateProductInput!): CreateProductPayload!
  updateProduct(id: ID!, input: UpdateProductInput!): UpdateProductPayload!
  deleteProduct(id: ID!): DeleteProductPayload!
}

input ProductFilter {
  categoryId: ID
  minPrice: Int
  maxPrice: Int
  inStock: Boolean
  search: String
}

enum ProductOrderBy {
  NAME_ASC
  NAME_DESC
  PRICE_ASC
  PRICE_DESC
  CREATED_AT_DESC
}

input CreateProductInput {
  name: String!
  description: String
  priceInCents: Int!
  categoryId: ID!
}

input UpdateProductInput {
  name: String
  description: String
  priceInCents: Int
}

type CreateProductPayload {
  product: Product
  errors: [UserError!]!
}

type UpdateProductPayload {
  product: Product
  errors: [UserError!]!
}

type DeleteProductPayload {
  success: Boolean!
  errors: [UserError!]!
}
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Fat resolvers** | Hard to test, mixed concerns | Extract to services |
| **No DataLoader** | N+1 queries kill performance | Use DataLoader for relations |
| **Database-shaped schema** | Exposes internals, hard to evolve | Design for client needs |
| **Generic error messages** | Clients can't handle errors | Structured error payloads |
| **No pagination** | Memory/performance issues | Cursor-based pagination |
| **Returning null for errors** | Silent failures | Return error in payload |
| **Auth in every resolver** | Repetitive, error-prone | Middleware or directive |
| **Prisma in resolvers** | Tight coupling | Service layer abstraction |

---

## Checklist

### Schema
- [ ] Types designed for client needs
- [ ] Cursor-based pagination for lists
- [ ] Input types for mutations
- [ ] Payload pattern with errors
- [ ] Enum for error codes

### Resolvers
- [ ] Thin resolvers, logic in services
- [ ] DataLoader for all relations
- [ ] Proper error handling
- [ ] Auth checks where needed

### Performance
- [ ] DataLoader prevents N+1
- [ ] Pagination limits enforced
- [ ] Complex queries optimized
- [ ] Indices on filtered fields

### Security
- [ ] Auth tokens validated
- [ ] Authorization on sensitive operations
- [ ] Input validation in services
- [ ] Rate limiting configured

---

## When to Consider Alternatives

| Situation | Consider |
|-----------|----------|
| Simple CRUD, no relations | REST might be simpler |
| Real-time requirements | GraphQL Subscriptions |
| Public API with caching needs | REST with HTTP caching |
| File uploads | Separate REST endpoint or signed URLs |
