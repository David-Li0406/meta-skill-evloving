---
name: backend-development
description: Provides specialized guidance for backend development including API design, database interactions, authentication, error handling, and security best practices. Use when working on backend code, API endpoints, server-side logic, database queries, authentication systems, or when the user mentions backend, API, server, or database development.
---

# Backend Development

## Core Principles

When developing backend code:

1. **Security First**: Always validate and sanitize inputs, use parameterized queries, implement proper authentication
2. **Error Handling**: Provide meaningful error messages without exposing sensitive information
3. **API Design**: Follow RESTful conventions, use appropriate HTTP status codes, version APIs
4. **Database**: Use transactions for multi-step operations, implement proper indexing, avoid N+1 queries
5. **Testing**: Write unit tests for business logic, integration tests for API endpoints

## API Design

### RESTful Endpoints

Use standard HTTP methods and status codes:

```typescript
// ✅ GOOD - RESTful design
GET    /api/users          // List users
GET    /api/users/:id      // Get specific user
POST   /api/users          // Create user (201 Created)
PUT    /api/users/:id      // Update user (200 OK or 204 No Content)
DELETE /api/users/:id      // Delete user (204 No Content)

// ❌ BAD - Non-standard
GET /api/getUser
POST /api/deleteUser
```

### Status Codes

Use appropriate HTTP status codes:

- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST creating a resource
- `204 No Content`: Successful DELETE or PUT with no response body
- `400 Bad Request`: Client error (validation failures)
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Authenticated but lacks permission
- `404 Not Found`: Resource doesn't exist
- `500 Internal Server Error`: Server-side error

### Request/Response Format

```typescript
// ✅ GOOD - Consistent structure
{
  "data": { ... },
  "meta": { "timestamp": "...", "version": "1.0" }
}

// Error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [ ... ]
  }
}
```

## Database Interactions

### Parameterized Queries

**Always** use parameterized queries to prevent SQL injection:

```typescript
// ✅ GOOD - Parameterized
const result = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
);

// ❌ BAD - String concatenation (SQL injection risk)
const result = await db.query(
  `SELECT * FROM users WHERE email = '${email}'`
);
```

### Transactions

Use transactions for operations that must succeed or fail together:

```typescript
// ✅ GOOD - Transaction
await db.transaction(async (trx) => {
  await trx.insert(user).into('users');
  await trx.insert(profile).into('profiles');
  // Both succeed or both rollback
});
```

### Avoiding N+1 Queries

```typescript
// ❌ BAD - N+1 query problem
const users = await db.select('*').from('users');
for (const user of users) {
  user.posts = await db.select('*').from('posts').where('user_id', user.id);
}

// ✅ GOOD - Single query with join
const users = await db
  .select('users.*', 'posts.*')
  .from('users')
  .leftJoin('posts', 'users.id', 'posts.user_id');
```

## Authentication & Authorization

### Token-Based Auth

```typescript
// Generate JWT token
const token = jwt.sign(
  { userId: user.id, email: user.email },
  process.env.JWT_SECRET,
  { expiresIn: '24h' }
);

// Verify token middleware
const authenticate = async (req, res, next) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};
```

### Authorization Checks

```typescript
// ✅ GOOD - Check permissions
const authorize = (requiredRole) => {
  return (req, res, next) => {
    if (req.user.role !== requiredRole) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
};
```

## Input Validation

Always validate and sanitize user input:

```typescript
// ✅ GOOD - Validation middleware
import { body, validationResult } from 'express-validator';

const validateUser = [
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 8 }),
  body('age').isInt({ min: 0, max: 120 }),
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    next();
  }
];
```

## Error Handling

### Structured Error Responses

```typescript
// ✅ GOOD - Meaningful errors
class AppError extends Error {
  constructor(message, statusCode, code) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
  }
}

// Usage
if (!user) {
  throw new AppError('User not found', 404, 'USER_NOT_FOUND');
}

// Error handler middleware
app.use((err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal server error';
  
  // Don't expose internal errors in production
  res.status(statusCode).json({
    error: {
      code: err.code || 'INTERNAL_ERROR',
      message: process.env.NODE_ENV === 'production' && statusCode === 500
        ? 'An error occurred'
        : message
    }
  });
});
```

## Security Best Practices

1. **Environment Variables**: Never commit secrets; use `.env` files
2. **Password Hashing**: Use bcrypt or argon2, never store plaintext
3. **Rate Limiting**: Implement rate limiting on authentication endpoints
4. **CORS**: Configure CORS properly for production
5. **HTTPS**: Always use HTTPS in production
6. **Input Sanitization**: Sanitize all user inputs
7. **SQL Injection**: Always use parameterized queries
8. **XSS Prevention**: Escape output, use Content Security Policy

```typescript
// ✅ GOOD - Password hashing
import bcrypt from 'bcrypt';

const hashedPassword = await bcrypt.hash(password, 10);
const isValid = await bcrypt.compare(password, hashedPassword);
```

## Testing

### Unit Tests

```typescript
// Test business logic
describe('calculateScore', () => {
  it('should calculate correct score', () => {
    const result = calculateScore(correctAnswers, totalQuestions);
    expect(result).toBe(85);
  });
});
```

### Integration Tests

```typescript
// Test API endpoints
describe('POST /api/users', () => {
  it('should create a new user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', password: 'password123' })
      .expect(201);
    
    expect(response.body.data.email).toBe('test@example.com');
  });
});
```

## Common Patterns

### Middleware Pattern

```typescript
// Chain middleware for authentication, validation, etc.
app.post('/api/users',
  authenticate,
  validateUser,
  createUser
);
```

### Repository Pattern

```typescript
// Separate data access from business logic
class UserRepository {
  async findById(id) {
    return db.select('*').from('users').where('id', id).first();
  }
  
  async create(userData) {
    return db.insert(userData).into('users').returning('*');
  }
}
```

## Performance Considerations

1. **Caching**: Cache frequently accessed data (Redis, in-memory)
2. **Pagination**: Always paginate large result sets
3. **Indexing**: Add database indexes for frequently queried fields
4. **Connection Pooling**: Use connection pools for database connections
5. **Async Operations**: Use async/await for I/O operations

```typescript
// ✅ GOOD - Pagination
const page = parseInt(req.query.page) || 1;
const limit = parseInt(req.query.limit) || 10;
const offset = (page - 1) * limit;

const users = await db
  .select('*')
  .from('users')
  .limit(limit)
  .offset(offset);
```
