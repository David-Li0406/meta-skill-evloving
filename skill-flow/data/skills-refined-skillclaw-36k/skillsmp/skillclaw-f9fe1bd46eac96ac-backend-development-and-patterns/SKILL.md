---
name: backend-development-and-patterns
description: Use this skill when you need to design and implement robust backend systems, covering API design, database interactions, error handling, security, and common backend patterns.
---

# Skill body

## Overview

This skill covers the fundamentals of backend development, including:

- **API Design**: RESTful APIs, GraphQL
- **Authentication & Authorization**: JWT, OAuth, Session management
- **Database Design**: Schema design, migrations
- **Error Handling**: Proper error responses and logging
- **Security**: SQL Injection, XSS, CSRF prevention
- **Performance**: Caching strategies, query optimization
- **Common Patterns**: Repository pattern, service layer, caching strategies

## API Design

### RESTful API

```typescript
// Endpoint design
GET    /api/users          # List users
GET    /api/users/:id      # Get user details
POST   /api/users          # Create user
PUT    /api/users/:id      # Update user
DELETE /api/users/:id      # Delete user
```

### Response Format

```typescript
// Success response
type SuccessResponse<T> = {
  success: true;
  data: T;
};

// Error response
type ErrorResponse = {
  success: false;
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
};

type ApiResponse<T> = SuccessResponse<T> | ErrorResponse;
```

### Error Handling

```typescript
// HTTP Status Codes
200: Success
201: Created
400: Validation Error
401: Authentication Error
403: Authorization Error
404: Resource Not Found
500: Server Error
```

## Repository Pattern

### Interface Definition

```typescript
interface Repository<T, ID> {
  findById(id: ID): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: ID): Promise<void>;
}
```

### Implementation Example (Prisma)

```typescript
class PrismaUserRepository implements UserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { id } });
  }

  async save(user: User): Promise<User> {
    return this.prisma.user.upsert({
      where: { id: user.id },
      create: user,
      update: user,
    });
  }
}
```

## Service Layer

### Use Case Implementation

```typescript
class CreateUserUseCase {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}

  async execute(input: CreateUserInput): Promise<User> {
    // Validation
    const validated = CreateUserSchema.parse(input);

    // Business logic
    const user = User.create(validated);

    // Persistence
    const saved = await this.userRepository.save(user);

    // Side effects
    await this.emailService.sendWelcome(saved.email);

    return saved;
  }
}
```

## Caching Strategies

### Cache-Aside Pattern

```typescript
async function getUser(id: string): Promise<User> {
  // 1. Check cache
  const cached = await cache.get(`user:${id}`);
  if (cached) return cached;

  // 2. Fetch from DB
  const user = await userRepository.findById(id);

  // 3. Save to cache
  await cache.set(`user:${id}`, user, { ttl: 3600 });

  return user;
}
```

### Cache Invalidation

```typescript
// Invalidate cache on update
async function updateUser(id: string, data: UpdateUserInput): Promise<User> {
  const updated = await userRepository.update(id, data);
  await cache.delete(`user:${id}`); // Invalidate cache
  return updated;
}
```