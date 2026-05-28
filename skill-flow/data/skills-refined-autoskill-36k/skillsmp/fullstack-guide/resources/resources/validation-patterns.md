# Validation Patterns - Input Validation with Zod

Complete guide to input validation using Zod schemas for type-safe validation.

## Table of Contents

- [Why Zod?](#why-zod)
- [Basic Zod Patterns](#basic-zod-patterns)
- [Schema Examples](#schema-examples)
- [Controller Validation](#controller-validation)
- [DTO Pattern](#dto-pattern)
- [Error Handling](#error-handling)
- [Advanced Patterns](#advanced-patterns)

---

## Why Zod?

### Benefits

**Type Safety:**
- ✅ Full TypeScript inference
- ✅ Runtime + compile-time validation
- ✅ Automatic type generation

**Developer Experience:**
- ✅ Intuitive API
- ✅ Composable schemas
- ✅ Excellent error messages

**Performance:**
- ✅ Fast validation
- ✅ Small bundle size
- ✅ Tree-shakeable

---

## Basic Zod Patterns

### Primitive Types

```typescript
import { z } from 'zod';

// Strings
const nameSchema = z.string().min(2).max(100);
const emailSchema = z.string().email();
const uuidSchema = z.string().uuid();

// Numbers
const ageSchema = z.number().int().min(0).max(150);
const priceSchema = z.number().positive();

// Booleans
const isActiveSchema = z.boolean().default(true);

// Enums
const roleSchema = z.enum(['ADMIN', 'USER', 'GUEST']);
```

### Objects

```typescript
const userSchema = z.object({
    id: z.string().uuid(),
    email: z.string().email(),
    name: z.string().min(2),
    role: z.enum(['ADMIN', 'USER']).default('USER'),
    createdAt: z.date().optional(),
});

// Type inference
type User = z.infer<typeof userSchema>;
```

### Arrays

```typescript
const tagsSchema = z.array(z.string()).min(1).max(10);

const usersSchema = z.array(userSchema);
```

---

## Schema Examples

### Create User Schema

```typescript
export const createUserSchema = z.object({
    email: z.string().email('Invalid email format'),
    name: z.string()
        .min(2, 'Name must be at least 2 characters')
        .max(100, 'Name must be less than 100 characters'),
    password: z.string()
        .min(8, 'Password must be at least 8 characters')
        .regex(/[A-Z]/, 'Password must contain uppercase letter')
        .regex(/[0-9]/, 'Password must contain number'),
    role: z.enum(['ADMIN', 'USER']).default('USER'),
});

export type CreateUserDTO = z.infer<typeof createUserSchema>;
```

### Update User Schema (Partial)

```typescript
export const updateUserSchema = createUserSchema.partial().omit({ 
    password: true 
});

export type UpdateUserDTO = z.infer<typeof updateUserSchema>;
```

### Query Params Schema

```typescript
export const listUsersQuerySchema = z.object({
    page: z.coerce.number().int().min(1).default(1),
    limit: z.coerce.number().int().min(1).max(100).default(20),
    search: z.string().optional(),
    role: z.enum(['ADMIN', 'USER']).optional(),
    sortBy: z.enum(['name', 'createdAt', 'email']).default('createdAt'),
    sortOrder: z.enum(['asc', 'desc']).default('desc'),
});
```

---

## Controller Validation

### In Controller Method

```typescript
async create(req: Request, res: Response) {
    try {
        // Validate input
        const validated = createUserSchema.parse(req.body);
        
        // Use validated data (fully typed)
        const user = await this.userService.create(validated);
        
        this.handleSuccess(res, user, 'User created');
    } catch (error) {
        if (error instanceof z.ZodError) {
            return res.status(400).json({
                success: false,
                error: 'Validation failed',
                details: error.errors,
            });
        }
        this.handleError(error, res, 'create');
    }
}
```

### Safe Parse (No Throw)

```typescript
const result = createUserSchema.safeParse(req.body);

if (!result.success) {
    return res.status(400).json({
        success: false,
        errors: result.error.errors,
    });
}

// result.data is typed and validated
const user = await userService.create(result.data);
```

---

## DTO Pattern

### Define DTOs from Schemas

```typescript
// schemas/userSchemas.ts
export const createUserSchema = z.object({
    email: z.string().email(),
    name: z.string().min(2),
    password: z.string().min(8),
});

export const updateUserSchema = createUserSchema.partial();

export const userResponseSchema = z.object({
    id: z.string().uuid(),
    email: z.string().email(),
    name: z.string(),
    role: z.string(),
    createdAt: z.date(),
});

// Export types
export type CreateUserDTO = z.infer<typeof createUserSchema>;
export type UpdateUserDTO = z.infer<typeof updateUserSchema>;
export type UserResponse = z.infer<typeof userResponseSchema>;
```

### Use DTOs in Service Layer

```typescript
// services/UserService.ts
import { CreateUserDTO, UpdateUserDTO, UserResponse } from '../schemas/userSchemas';

export class UserService {
    async create(data: CreateUserDTO): Promise<UserResponse> {
        // data is fully typed
        const user = await this.userRepository.create(data);
        return this.toResponse(user);
    }

    async update(id: string, data: UpdateUserDTO): Promise<UserResponse> {
        const user = await this.userRepository.update(id, data);
        return this.toResponse(user);
    }

    private toResponse(user: User): UserResponse {
        return {
            id: user.id,
            email: user.email,
            name: user.name,
            role: user.role,
            createdAt: user.createdAt,
        };
    }
}
```

---

## Error Handling

### Format Zod Errors

```typescript
function formatZodError(error: z.ZodError): object {
    return {
        message: 'Validation failed',
        errors: error.errors.map(err => ({
            field: err.path.join('.'),
            message: err.message,
            code: err.code,
        })),
    };
}
```

### In BaseController

```typescript
protected handleError(error: any, res: Response, context: string) {
    if (error instanceof z.ZodError) {
        return res.status(400).json({
            success: false,
            error: formatZodError(error),
        });
    }
    
    // Handle other errors...
}
```

---

## Advanced Patterns

### Refine (Custom Validation)

```typescript
const passwordSchema = z.object({
    password: z.string().min(8),
    confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
});
```

### Transform

```typescript
const userInputSchema = z.object({
    email: z.string().email().transform(email => email.toLowerCase()),
    name: z.string().transform(name => name.trim()),
});
```

### Pick and Omit

```typescript
// Pick specific fields
const loginSchema = userSchema.pick({
    email: true,
    password: true,
});

// Omit fields
const userWithoutTimestamps = userSchema.omit({
    createdAt: true,
    updatedAt: true,
});
```

### Validation Middleware

```typescript
import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';

export function validateBody<T extends z.ZodType>(schema: T) {
    return (req: Request, res: Response, next: NextFunction) => {
        try {
            req.body = schema.parse(req.body);
            next();
        } catch (error) {
            if (error instanceof z.ZodError) {
                return res.status(400).json({
                    success: false,
                    error: {
                        message: 'Validation failed',
                        details: error.errors,
                    },
                });
            }
            next(error);
        }
    };
}

// Usage
router.post('/users',
    validateBody(createUserSchema),
    async (req, res) => {
        // req.body is validated and typed!
        const user = await userService.createUser(req.body);
        res.json({ success: true, data: user });
    }
);
```

---

**Related Files:**
- [SKILL.md](../SKILL.md) - Main guide
- [architecture-overview.md](architecture-overview.md) - Architecture patterns
- [async-and-errors.md](async-and-errors.md) - Error handling patterns
