---
name: backend-development
description: Use this skill for designing APIs, database schemas, and backend architecture, including microservices and test-driven development.
---

# Backend Development

## When to Use

- Creating new APIs or services
- Database schema design
- Service architecture decisions
- Performance optimization
- API versioning and documentation

## API Design

### RESTful Conventions
```
GET    /users          # List users
POST   /users          # Create user
GET    /users/:id      # Get user
PUT    /users/:id      # Update user (full)
PATCH  /users/:id      # Update user (partial)
DELETE /users/:id      # Delete user

GET    /users/:id/posts  # List user's posts
POST   /users/:id/posts  # Create post for user
```

### Response Format
```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 100
  }
}
```

### Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      { "field": "email", "message": "Invalid format" }
    ]
  }
}
```

### Consistent API Response Format
```typescript
type ApiResponse<T> = {
  success: true
  data: T
  meta?: {
    pagination?: {
      page: number
      limit: number
      total: number
    }
  }
} | {
  success: false
  error: string
  details?: any
}
```

## Database Patterns

### Schema Design
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  public_id UUID DEFAULT gen_random_uuid() UNIQUE,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  deleted_at TIMESTAMPTZ
);
```

### Query Patterns
```sql
SELECT * FROM posts
WHERE created_at < $cursor
ORDER BY created_at DESC
LIMIT 20;
```

### Transaction Patterns
```typescript
export async function transferFunds(fromId: string, toId: string, amount: number) {
  await db.$transaction(async (tx) => {
    const sender = await tx.accounts.findUnique({ where: { id: fromId } });
    if (!sender || sender.balance < amount) {
      throw new Error('Insufficient funds');
    }
    await tx.accounts.update({ where: { id: fromId }, data: { balance: { decrement: amount } } });
    await tx.accounts.update({ where: { id: toId }, data: { balance: { increment: amount } } });
  });
}
```

## Authentication

### JWT Pattern
```typescript
interface TokenPayload {
  sub: string;      // User ID
  iat: number;      // Issued at
  exp: number;      // Expiration
  scope: string[];  // Permissions
}

function verifyToken(token: string): TokenPayload {
  return jwt.verify(token, SECRET) as TokenPayload;
}
```

### Middleware
```typescript
async function authenticate(req: Request, res: Response, next: Next) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  try {
    req.user = verifyToken(token);
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
}
```

## Caching Strategy

```typescript
async function getUser(id: string): Promise<User> {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);
  const user = await db.users.findById(id);
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
  return user;
}
```

## Error Handling Patterns

### Structured Error Classes
```typescript
export class AppError extends Error {
  constructor(public statusCode: number, public message: string, public code?: string, public details?: any) {
    super(message);
    this.name = this.constructor.name;
  }
}
```

### Global Error Handler
```typescript
export function handleApiError(error: unknown): Response {
  if (error instanceof AppError) {
    return NextResponse.json({ success: false, error: error.message, code: error.code, details: error.details }, { status: error.statusCode });
  }
  return NextResponse.json({ success: false, error: 'Internal server error', code: 'INTERNAL_ERROR' }, { status: 500 });
}
```

## Best Practices

- **API Design**: Follow RESTful conventions, maintain a consistent response format, and implement versioning.
- **Validation**: Validate all inputs with schemas (e.g., Zod, Joi).
- **Error Handling**: Use structured error classes and a global error handler.
- **Database**: Utilize transactions, optimize queries, and add appropriate indexes.
- **Caching**: Implement cache-aside patterns and establish an invalidation strategy.
- **Security**: Ensure authentication on all protected routes and perform authorization checks.
- **Logging**: Maintain structured logs without sensitive data.
- **Testing**: Conduct unit tests for business logic and integration tests for APIs.
- **Documentation**: Create OpenAPI/Swagger specifications for APIs.
- **Monitoring**: Implement health checks, error tracking, and performance metrics.