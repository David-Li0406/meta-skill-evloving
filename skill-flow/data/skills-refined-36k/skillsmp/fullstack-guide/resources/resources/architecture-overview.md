# Architecture Overview - Backend Services

Complete guide to the layered architecture pattern used in backend microservices.

## Table of Contents

- [Layered Architecture Pattern](#layered-architecture-pattern)
- [Request Lifecycle](#request-lifecycle)
- [Directory Structure](#directory-structure)
- [Separation of Concerns](#separation-of-concerns)

---

## Layered Architecture Pattern

### The Four Layers

```
┌─────────────────────────────────────┐
│         HTTP Request                │
└───────────────┬─────────────────────┘
                ↓
┌─────────────────────────────────────┐
│  Layer 1: ROUTES                    │
│  - Route definitions only           │
│  - Middleware registration          │
│  - Delegate to controllers          │
│  - NO business logic                │
└───────────────┬─────────────────────┘
                ↓
┌─────────────────────────────────────┐
│  Layer 2: CONTROLLERS               │
│  - Input validation (Zod)           │
│  - Call services                    │
│  - Response formatting              │
│  - Error handling boundaries        │
└───────────────┬─────────────────────┘
                ↓
┌─────────────────────────────────────┐
│  Layer 3: SERVICES                  │
│  - Business logic                   │
│  - Orchestration                    │
│  - Cross-service calls              │
│  - Error handling                   │
└───────────────┬─────────────────────┘
                ↓
┌─────────────────────────────────────┐
│  Layer 4: REPOSITORIES              │
│  - Database access                  │
│  - PrismaService interactions       │
│  - Data transformation              │
│  - NO business logic                │
└─────────────────────────────────────┘
```

---

## Request Lifecycle

### Full Request Flow Example

```typescript
// 1. Request arrives at route
router.post('/users', middleware, (req, res) => userController.create(req, res));

// 2. Controller validates and delegates
async create(req: Request, res: Response) {
    try {
        const validated = createUserSchema.parse(req.body);  // Validation
        const user = await this.userService.create(validated);  // Delegate
        this.handleSuccess(res, user, 'User created');  // Response
    } catch (error) {
        this.handleError(error, res, 'create');  // Error handling
    }
}

// 3. Service contains business logic
async create(data: CreateUserDTO): Promise<User> {
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) throw new ConflictError('Email already exists');
    return await this.userRepository.create(data);
}

// 4. Repository handles database
async create(data: CreateUserDTO): Promise<User> {
    return PrismaService.main.user.create({ data });
}
```

---

## Directory Structure

### Recommended Layout

```
src/
├── routes/              # Route definitions
│   ├── index.ts         # Route aggregator
│   ├── userRoutes.ts
│   └── authRoutes.ts
├── controllers/         # Request handlers
│   ├── BaseController.ts
│   ├── UserController.ts
│   └── AuthController.ts
├── services/            # Business logic
│   ├── UserService.ts
│   └── AuthService.ts
├── repositories/        # Data access
│   ├── UserRepository.ts
│   └── BaseRepository.ts
├── schemas/             # Zod validation schemas
│   ├── userSchemas.ts
│   └── authSchemas.ts
├── middleware/          # Express middleware
│   ├── authMiddleware.ts
│   └── errorMiddleware.ts
├── errors/              # Custom error types
│   ├── AppError.ts
│   └── HttpErrors.ts
└── utils/               # Utilities
    └── asyncErrorWrapper.ts
```

---

## Separation of Concerns

### Route Layer

**DO:**
- Define endpoints
- Register middleware
- Delegate to controllers

**DON'T:**
- Put business logic
- Access database
- Format responses

```typescript
// ✅ Good route
router.post('/users',
    authMiddleware,
    (req, res) => userController.create(req, res)
);

// ❌ Bad route - business logic in route
router.post('/users', async (req, res) => {
    const user = await prisma.user.create({ data: req.body });
    res.json(user);
});
```

### Controller Layer

**DO:**
- Validate input
- Call services
- Format responses
- Handle errors

**DON'T:**
- Implement business logic
- Access database directly
- Make cross-service calls

```typescript
// ✅ Good controller
async create(req: Request, res: Response) {
    try {
        const validated = schema.parse(req.body);
        const result = await this.service.create(validated);
        this.handleSuccess(res, result);
    } catch (error) {
        this.handleError(error, res);
    }
}
```

### Service Layer

**DO:**
- Implement business logic
- Orchestrate operations
- Throw appropriate errors
- Call repositories

**DON'T:**
- Handle HTTP concerns
- Format responses
- Access req/res

```typescript
// ✅ Good service
async create(data: CreateDTO): Promise<Entity> {
    // Business rule validation
    const exists = await this.repository.findByEmail(data.email);
    if (exists) throw new ConflictError('Email exists');
    
    // Business logic
    return this.repository.create(data);
}
```

### Repository Layer

**DO:**
- Execute database queries
- Transform data models
- Handle database errors

**DON'T:**
- Implement business logic
- Validate business rules
- Know about HTTP

```typescript
// ✅ Good repository
async findByEmail(email: string): Promise<User | null> {
    return PrismaService.main.user.findUnique({ where: { email } });
}

async create(data: CreateUserDTO): Promise<User> {
    return PrismaService.main.user.create({ data });
}
```

---

## Complete Example: User Creation

**Route:**
```typescript
router.post('/users',
    authMiddleware,
    auditMiddleware,
    (req, res) => userController.create(req, res)
);
```

**Controller:**
```typescript
async create(req: Request, res: Response): Promise<void> {
    try {
        const validated = createUserSchema.parse(req.body);
        const user = await this.userService.create(validated);
        this.handleSuccess(res, user, 'User created');
    } catch (error) {
        this.handleError(error, res, 'create');
    }
}
```

**Service:**
```typescript
async create(data: CreateUserDTO): Promise<User> {
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) throw new ConflictError('Email already exists');
    return await this.userRepository.create(data);
}
```

**Repository:**
```typescript
async create(data: CreateUserDTO): Promise<User> {
    return PrismaService.main.user.create({ data });
}

async findByEmail(email: string): Promise<User | null> {
    return PrismaService.main.user.findUnique({ where: { email } });
}
```

**Notice:** Each layer has clear, distinct responsibilities!

---

**Related Files:**
- [SKILL.md](../SKILL.md) - Main guide
- [validation-patterns.md](validation-patterns.md) - Input validation
- [async-and-errors.md](async-and-errors.md) - Error handling
