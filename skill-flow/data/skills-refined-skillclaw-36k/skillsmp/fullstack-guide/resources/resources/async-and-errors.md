# Async Patterns and Error Handling

Complete guide to async/await patterns and custom error handling.

## Table of Contents

- [Async/Await Best Practices](#asyncawait-best-practices)
- [Promise Error Handling](#promise-error-handling)
- [Custom Error Types](#custom-error-types)
- [asyncErrorWrapper Utility](#asyncerrorwrapper-utility)
- [Error Propagation](#error-propagation)
- [Common Async Pitfalls](#common-async-pitfalls)

---

## Async/Await Best Practices

### Always Use Try-Catch

```typescript
// ❌ NEVER: Unhandled async errors
async function fetchData() {
    const data = await database.query(); // If throws, unhandled!
    return data;
}

// ✅ ALWAYS: Wrap in try-catch
async function fetchData() {
    try {
        const data = await database.query();
        return data;
    } catch (error) {
        Sentry.captureException(error);
        throw error;
    }
}
```

### Avoid .then() Chains

```typescript
// ❌ AVOID: Promise chains
function processData() {
    return fetchData()
        .then(data => transform(data))
        .then(transformed => save(transformed))
        .catch(error => {
            console.error(error);
            throw error;
        });
}

// ✅ PREFER: async/await
async function processData() {
    try {
        const data = await fetchData();
        const transformed = await transform(data);
        return await save(transformed);
    } catch (error) {
        console.error(error);
        throw error;
    }
}
```

### Parallel vs Sequential

```typescript
// Sequential - slower
const user = await fetchUser(id);
const posts = await fetchPosts(id);
const comments = await fetchComments(id);

// Parallel - faster when operations are independent
const [user, posts, comments] = await Promise.all([
    fetchUser(id),
    fetchPosts(id),
    fetchComments(id),
]);
```

---

## Custom Error Types

### Base AppError

```typescript
export class AppError extends Error {
    public readonly statusCode: number;
    public readonly isOperational: boolean;
    public readonly details?: any;

    constructor(message: string, statusCode = 500, details?: any) {
        super(message);
        this.statusCode = statusCode;
        this.isOperational = true;
        this.details = details;
        
        Error.captureStackTrace(this, this.constructor);
    }
}
```

### HTTP Errors

```typescript
export class NotFoundError extends AppError {
    constructor(message = 'Resource not found') {
        super(message, 404);
    }
}

export class ValidationError extends AppError {
    constructor(message: string, details?: any) {
        super(message, 400, details);
    }
}

export class UnauthorizedError extends AppError {
    constructor(message = 'Unauthorized') {
        super(message, 401);
    }
}

export class ForbiddenError extends AppError {
    constructor(message = 'Forbidden') {
        super(message, 403);
    }
}

export class ConflictError extends AppError {
    constructor(message: string) {
        super(message, 409);
    }
}
```

### Usage in Services

```typescript
async function getUserById(id: string): Promise<User> {
    const user = await userRepository.findById(id);
    
    if (!user) {
        throw new NotFoundError(`User ${id} not found`);
    }
    
    return user;
}
```

---

## asyncErrorWrapper Utility

### Implementation

```typescript
import { Request, Response, NextFunction, RequestHandler } from 'express';

export function asyncErrorWrapper(
    fn: (req: Request, res: Response, next: NextFunction) => Promise<any>
): RequestHandler {
    return (req, res, next) => {
        fn(req, res, next).catch(next);
    };
}
```

### Usage

```typescript
// Instead of try-catch in every route
router.get('/users/:id', asyncErrorWrapper(async (req, res) => {
    const user = await userService.findById(req.params.id);
    res.json(user);
}));
```

---

## Error Propagation

### Error Flow Through Layers

```
Repository throws → Service catches/re-throws → Controller handles → Response
```

### Example Flow

```typescript
// Repository
async findByEmail(email: string): Promise<User | null> {
    return PrismaService.main.user.findUnique({ where: { email } });
}

// Service - business logic errors
async create(data: CreateUserDTO): Promise<User> {
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) {
        throw new ConflictError('Email already exists');  // Throws
    }
    return this.userRepository.create(data);
}

// Controller - catches and handles
async create(req: Request, res: Response) {
    try {
        const validated = schema.parse(req.body);
        const user = await this.userService.create(validated);
        this.handleSuccess(res, user);
    } catch (error) {
        this.handleError(error, res, 'create');  // Catches
    }
}
```

---

## Common Async Pitfalls

### Fire and Forget (Bad)

```typescript
// ❌ NEVER: Fire and forget
async function processRequest(req, res) {
    sendEmail(user.email); // Fires async, errors unhandled!
    res.json({ success: true });
}

// ✅ ALWAYS: Await or handle
async function processRequest(req, res) {
    try {
        await sendEmail(user.email);
        res.json({ success: true });
    } catch (error) {
        Sentry.captureException(error);
        res.status(500).json({ error: 'Failed to send email' });
    }
}

// ✅ OR: Intentional background task
async function processRequest(req, res) {
    sendEmail(user.email).catch(error => {
        Sentry.captureException(error);
    });
    res.json({ success: true });
}
```

### Unhandled Rejections

```typescript
// ✅ Global handler for unhandled rejections
process.on('unhandledRejection', (reason, promise) => {
    Sentry.captureException(reason, {
        tags: { type: 'unhandled_rejection' }
    });
    console.error('Unhandled Rejection:', reason);
});

process.on('uncaughtException', (error) => {
    Sentry.captureException(error, {
        tags: { type: 'uncaught_exception' }
    });
    console.error('Uncaught Exception:', error);
    process.exit(1);
});
```

---

**Related Files:**
- [SKILL.md](../SKILL.md)
- [validation-patterns.md](validation-patterns.md)
- [testing-guide.md](testing-guide.md)
